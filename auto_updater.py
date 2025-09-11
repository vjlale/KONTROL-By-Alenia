#!/usr/bin/env python3
"""
Sistema de auto-actualización para ALENIA GESTION-KONTROL+
Permite actualizar la aplicación automáticamente desde GitHub
"""

import os
import sys
import json
import requests
import zipfile
import shutil
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import hashlib
from urllib.parse import urlparse

class AutoUpdater:
    def __init__(self, current_version="2.3.0", github_repo="vjlale/KONTROL-By-Alenia"):
        self.current_version = current_version
        self.github_repo = github_repo
        self.api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
        self.download_url = None
        self.new_version = None
        self.download_size = 0
        self.temp_dir = Path.cwd() / "temp_update"
        self.backup_dir = Path.cwd() / "backup_update"
        
    def check_for_updates(self):
        """Verificar si hay actualizaciones disponibles"""
        try:
            print("🔍 Verificando actualizaciones...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            self.new_version = release_data["tag_name"].replace("v", "")
            
            # Comparar versiones
            if self._is_newer_version(self.new_version, self.current_version):
                # Buscar asset ZIP
                for asset in release_data["assets"]:
                    if asset["name"].endswith(".zip") and "Complete" in asset["name"]:
                        self.download_url = asset["browser_download_url"]
                        self.download_size = asset["size"]
                        break
                        
                if self.download_url:
                    return True, f"Nueva versión disponible: v{self.new_version}"
                else:
                    return False, "No se encontró archivo de actualización"
            else:
                return False, "Ya tienes la última versión"
                
        except requests.RequestException as e:
            return False, f"Error conectando con servidor: {e}"
        except Exception as e:
            return False, f"Error verificando actualizaciones: {e}"
            
    def _is_newer_version(self, new_version, current_version):
        """Comparar versiones (formato: x.y.z)"""
        try:
            new_parts = [int(x) for x in new_version.split('.')]
            current_parts = [int(x) for x in current_version.split('.')]
            
            # Igualar longitud de listas
            max_len = max(len(new_parts), len(current_parts))
            new_parts.extend([0] * (max_len - len(new_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return new_parts > current_parts
        except:
            return False
            
    def download_update(self, progress_callback=None):
        """Descargar actualización con progreso"""
        try:
            print(f"📥 Descargando actualización v{self.new_version}...")
            
            # Crear directorio temporal
            self.temp_dir.mkdir(exist_ok=True)
            
            # Descargar archivo
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()
            
            zip_path = self.temp_dir / f"update_v{self.new_version}.zip"
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback:
                            progress = (downloaded / self.download_size) * 100
                            progress_callback(progress)
                            
            print("✅ Descarga completada")
            return zip_path
            
        except Exception as e:
            print(f"❌ Error descargando: {e}")
            return None
            
    def install_update(self, zip_path):
        """Instalar actualización"""
        try:
            print("🔧 Instalando actualización...")
            
            # Crear backup
            self._create_backup()
            
            # Extraer actualización
            extract_dir = self.temp_dir / "extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                
            # Encontrar directorio de la aplicación en el ZIP
            app_dir = None
            for item in extract_dir.iterdir():
                if item.is_dir() and "KONTROL" in item.name.upper():
                    app_dir = item
                    break
                    
            if not app_dir:
                raise Exception("No se encontró directorio de aplicación en el ZIP")
                
            # Copiar archivos actualizados
            current_dir = Path.cwd()
            files_updated = []
            
            for item in app_dir.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(app_dir)
                    dest_path = current_dir / relative_path
                    
                    # Crear directorio padre si no existe
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copiar archivo
                    shutil.copy2(item, dest_path)
                    files_updated.append(str(relative_path))
                    
            print(f"✅ Actualización instalada: {len(files_updated)} archivos actualizados")
            return True
            
        except Exception as e:
            print(f"❌ Error instalando actualización: {e}")
            self._restore_backup()
            return False
            
    def _create_backup(self):
        """Crear backup de la versión actual"""
        try:
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
                
            self.backup_dir.mkdir()
            
            # Backup de archivos críticos
            critical_files = ["KONTROL+.exe", "KONTROL-PLUS.exe", "main.py", "auth.py"]
            
            for file_name in critical_files:
                source = Path.cwd() / file_name
                if source.exists():
                    shutil.copy2(source, self.backup_dir / file_name)
                    
            print("💾 Backup creado")
            
        except Exception as e:
            print(f"⚠️  Error creando backup: {e}")
            
    def _restore_backup(self):
        """Restaurar backup en caso de error"""
        try:
            if self.backup_dir.exists():
                for backup_file in self.backup_dir.iterdir():
                    dest_file = Path.cwd() / backup_file.name
                    shutil.copy2(backup_file, dest_file)
                print("🔄 Backup restaurado")
        except Exception as e:
            print(f"❌ Error restaurando backup: {e}")
            
    def cleanup(self):
        """Limpiar archivos temporales"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            print("🧹 Archivos temporales limpiados")
        except:
            pass

class UpdaterGUI:
    def __init__(self, updater):
        self.updater = updater
        self.root = None
        self.progress_var = None
        self.status_var = None
        
    def show_update_dialog(self, message):
        """Mostrar diálogo de actualización disponible"""
        result = messagebox.askyesno(
            "Actualización Disponible",
            f"{message}\n\n¿Deseas actualizar ahora?",
            icon="question"
        )
        return result
        
    def show_progress_window(self):
        """Mostrar ventana de progreso de actualización"""
        self.root = tk.Toplevel()
        self.root.title("Actualizando KONTROL+")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.grab_set()  # Modal
        
        # Centrar ventana
        self.root.transient()
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (200 // 2)
        self.root.geometry(f"400x200+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Actualizando KONTROL+", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Estado
        self.status_var = tk.StringVar(value="Preparando actualización...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                     maximum=100, length=300)
        progress_bar.pack(pady=(0, 10))
        
        # Progreso texto
        self.progress_text = tk.StringVar(value="0%")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_text)
        progress_label.pack()
        
        return self.root
        
    def update_progress(self, progress, status=None):
        """Actualizar progreso"""
        if self.progress_var:
            self.progress_var.set(progress)
            self.progress_text.set(f"{progress:.1f}%")
            
        if status and self.status_var:
            self.status_var.set(status)
            
        if self.root:
            self.root.update()
            
    def close_progress_window(self):
        """Cerrar ventana de progreso"""
        if self.root:
            self.root.destroy()
            self.root = None

def check_and_update():
    """Función principal para verificar y actualizar"""
    updater = AutoUpdater()
    gui = UpdaterGUI(updater)
    
    try:
        # Verificar actualizaciones
        has_update, message = updater.check_for_updates()
        
        if has_update:
            # Mostrar diálogo de confirmación
            if gui.show_update_dialog(message):
                # Mostrar ventana de progreso
                progress_window = gui.show_progress_window()
                
                def download_and_install():
                    try:
                        # Descargar
                        gui.update_progress(0, "Descargando actualización...")
                        
                        def progress_callback(progress):
                            gui.update_progress(progress * 0.8, f"Descargando... {progress:.1f}%")
                            
                        zip_path = updater.download_update(progress_callback)
                        
                        if zip_path:
                            # Instalar
                            gui.update_progress(80, "Instalando actualización...")
                            success = updater.install_update(zip_path)
                            
                            if success:
                                gui.update_progress(100, "¡Actualización completada!")
                                messagebox.showinfo("Éxito", 
                                    "Actualización instalada correctamente.\n"
                                    "Reinicia la aplicación para usar la nueva versión.")
                            else:
                                messagebox.showerror("Error", 
                                    "Error instalando la actualización.\n"
                                    "La versión anterior fue restaurada.")
                        else:
                            messagebox.showerror("Error", "Error descargando la actualización.")
                            
                    except Exception as e:
                        messagebox.showerror("Error", f"Error durante la actualización: {e}")
                        
                    finally:
                        updater.cleanup()
                        gui.close_progress_window()
                
                # Ejecutar descarga en hilo separado
                threading.Thread(target=download_and_install, daemon=True).start()
                
            else:
                print("Actualización cancelada por el usuario")
        else:
            print(message)
            
    except Exception as e:
        print(f"Error en el proceso de actualización: {e}")

# Función para usar dentro de la aplicación principal
def check_updates_background(callback=None):
    """Verificar actualizaciones en segundo plano"""
    def check():
        updater = AutoUpdater()
        has_update, message = updater.check_for_updates()
        if callback:
            callback(has_update, message)
            
    threading.Thread(target=check, daemon=True).start()

if __name__ == "__main__":
    # Testing del actualizador
    check_and_update()