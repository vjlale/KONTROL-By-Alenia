import os
import json
import time
import hashlib
import binascii
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class AuthManager:
    """
    Maneja autenticación y persistencia de usuarios en usuarios.json.
    - Contraseñas con PBKDF2-HMAC-SHA256 + salt por usuario
    - Estructura de usuario:
      {
        "username": str,
        "role": "admin" | "vendedor",
        "password_hash": str (hex),
        "salt": str (hex),
        "created_at": ISO8601,
        "last_login": ISO8601 | None,
        "is_active": bool
      }
    - Throttling básico en memoria por intentos fallidos
    """

    def __init__(self, users_file_path: str = "usuarios.json") -> None:
        self.users_file_path = users_file_path
        self.users: List[Dict] = []
        # username -> { failed: int, lock_until: float }
        self._throttle: Dict[str, Dict[str, float]] = {}
        self._load_users()

    # ------------------- Persistencia -------------------
    def _load_users(self) -> None:
        if os.path.exists(self.users_file_path):
            try:
                with open(self.users_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.users = data
                    else:
                        # Estructura inesperada → reiniciar segura
                        self.users = []
            except Exception:
                # JSON corrupto → reiniciar en memoria (usuario podrá rehacer admin)
                self.users = []
        else:
            self.users = []

    def _save_users(self) -> None:
        tmp_path = self.users_file_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.users_file_path)

    # ------------------- Utilidades hash -------------------
    @staticmethod
    def _generate_salt() -> bytes:
        return os.urandom(16)

    @staticmethod
    def _hash_password(password: str, salt: bytes, iterations: int = 200_000) -> str:
        pwd = password.encode("utf-8")
        dk = hashlib.pbkdf2_hmac("sha256", pwd, salt, iterations)
        return binascii.hexlify(dk).decode("ascii")

    # ------------------- Consultas de estado -------------------
    def is_first_run(self) -> bool:
        """No existe admin activo registrado."""
        for u in self.users:
            if u.get("role") == "admin" and u.get("is_active", True):
                return False
        return True

    def _find_user(self, username: str) -> Optional[Dict]:
        username_l = username.strip().lower()
        for u in self.users:
            if u.get("username", "").lower() == username_l:
                return u
        return None

    # ------------------- Altas y cambios -------------------
    def register_admin(self, username: str, password: str) -> Dict:
        if not username or not password:
            raise ValueError("Usuario y contraseña son obligatorios.")
        if self._find_user(username):
            raise ValueError("El usuario ya existe.")
        # Si ya hay un admin activo, no permitir crear otro en onboarding
        if not self.is_first_run():
            raise ValueError("Ya existe un administrador registrado.")
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        salt = self._generate_salt()
        pwd_hash = self._hash_password(password, salt)
        now = datetime.utcnow().isoformat()
        user = {
            "username": username,
            "role": "admin",
            "password_hash": pwd_hash,
            "salt": binascii.hexlify(salt).decode("ascii"),
            "created_at": now,
            "last_login": None,
            "is_active": True,
        }
        self.users.append(user)
        self._save_users()
        return user

    def register_user(self, username: str, password: str, role: str = "vendedor") -> Dict:
        if role not in ("admin", "vendedor"):
            raise ValueError("Rol inválido.")
        if not username or not password:
            raise ValueError("Usuario y contraseña son obligatorios.")
        if self._find_user(username):
            raise ValueError("El usuario ya existe.")
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        salt = self._generate_salt()
        pwd_hash = self._hash_password(password, salt)
        now = datetime.utcnow().isoformat()
        user = {
            "username": username,
            "role": role,
            "password_hash": pwd_hash,
            "salt": binascii.hexlify(salt).decode("ascii"),
            "created_at": now,
            "last_login": None,
            "is_active": True,
        }
        self.users.append(user)
        self._save_users()
        return user

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        user = self._find_user(username)
        if not user:
            return False
        if not self._verify_password(user, old_password):
            return False
        if len(new_password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        salt = self._generate_salt()
        user["salt"] = binascii.hexlify(salt).decode("ascii")
        user["password_hash"] = self._hash_password(new_password, salt)
        self._save_users()
        return True

    # ------------------- Autenticación -------------------
    def _verify_password(self, user: Dict, password: str) -> bool:
        try:
            salt_hex = user.get("salt")
            if not salt_hex:
                return False
            salt = binascii.unhexlify(salt_hex.encode("ascii"))
            pwd_hash = self._hash_password(password, salt)
            return pwd_hash == user.get("password_hash")
        except Exception:
            return False

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        user = self._find_user(username)
        if not user or not user.get("is_active", True):
            return None
        # Verificar si está bloqueado por throttling
        can, _ = self.can_attempt(username)
        if not can:
            return None
        if self._verify_password(user, password):
            user["last_login"] = datetime.utcnow().isoformat()
            self._save_users()
            self.register_success(username)
            # Retornar copia sin secretos
            return {
                "username": user["username"],
                "role": user["role"],
                "last_login": user.get("last_login"),
                "is_active": user.get("is_active", True),
            }
        else:
            self.register_failure(username)
            return None

    # ------------------- Throttling básico -------------------
    def can_attempt(self, username: str) -> Tuple[bool, int]:
        info = self._throttle.get(username.lower())
        now = time.time()
        if info and info.get("lock_until", 0) > now:
            wait = int(round(info["lock_until"] - now))
            return False, max(wait, 1)
        return True, 0

    def register_failure(self, username: str) -> None:
        key = username.lower()
        info = self._throttle.get(key, {"failed": 0, "lock_until": 0.0})
        info["failed"] = info.get("failed", 0) + 1
        # Regla simple: 3+ fallos → 3s; 5+ → 10s
        if info["failed"] >= 5:
            info["lock_until"] = time.time() + 10
        elif info["failed"] >= 3:
            info["lock_until"] = time.time() + 3
        self._throttle[key] = info

    def register_success(self, username: str) -> None:
        key = username.lower()
        if key in self._throttle:
            self._throttle.pop(key, None)

    # ------------------- Administración -------------------
    def deactivate_user(self, username: str) -> bool:
        user = self._find_user(username)
        if not user:
            return False
        user["is_active"] = False
        self._save_users()
        return True

    def activate_user(self, username: str) -> bool:
        user = self._find_user(username)
        if not user:
            return False
        user["is_active"] = True
        self._save_users()
        return True

    def set_password(self, username: str, new_password: str) -> bool:
        """Cambia la contraseña sin requerir la anterior (uso admin)."""
        user = self._find_user(username)
        if not user:
            return False
        if len(new_password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        salt = self._generate_salt()
        user["salt"] = binascii.hexlify(salt).decode("ascii")
        user["password_hash"] = self._hash_password(new_password, salt)
        self._save_users()
        return True

    def set_role(self, username: str, role: str) -> bool:
        if role not in ("admin", "vendedor"):
            raise ValueError("Rol inválido.")
        user = self._find_user(username)
        if not user:
            return False
        user["role"] = role
        self._save_users()
        return True

    def list_users(self) -> List[Dict]:
        """Devuelve lista de usuarios sin exponer hashes ni salts."""
        sanitized: List[Dict] = []
        for u in self.users:
            sanitized.append({
                "username": u.get("username"),
                "role": u.get("role"),
                "created_at": u.get("created_at"),
                "last_login": u.get("last_login"),
                "is_active": u.get("is_active", True),
            })
        return sanitized
