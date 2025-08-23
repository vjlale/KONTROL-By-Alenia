from typing import Optional, Dict
from datetime import datetime


class SessionManager:
    """Gestiona la sesión del usuario autenticado en la aplicación."""

    def __init__(self) -> None:
        self.current_user: Optional[Dict] = None
        self.login_time: Optional[str] = None

    def login(self, user: Dict) -> None:
        # user esperado: { "username": str, "role": "admin"|"vendedor", ... }
        self.current_user = {
            "username": user.get("username"),
            "role": user.get("role", "vendedor"),
        }
        self.login_time = datetime.utcnow().isoformat()

    def logout(self) -> None:
        self.current_user = None
        self.login_time = None

    def is_logged_in(self) -> bool:
        return self.current_user is not None

    def is_admin(self) -> bool:
        return bool(self.current_user and self.current_user.get("role") == "admin")

    @property
    def username(self) -> Optional[str]:
        return self.current_user.get("username") if self.current_user else None

    @property
    def role(self) -> Optional[str]:
        return self.current_user.get("role") if self.current_user else None

