# -*- coding: utf-8 -*-
# do not use __init__.py because pyinstaller puts it in _internal/__init__/__init__.pyc
# config.pyc is well directly in _internal/
import os


BUNDLE_NAME = "imio-scan-helpers"
COPY_BAT_NAME = "copy_release_files_and_restart.bat"
DOWNLOAD_DIR = "_downloads"
EXECUTABLE_NAME = "main.exe"
GITHUB_REPO = "IMIO/imio.scan_helpers"
INTERNAL_DIR = "_internal"
MAIN_EXE_NAME = BUNDLE_NAME
PROFILES_DIRS = ["c:\\ProgramData\\Kofax\\Kofax Express 3.3\\Jobs", "c:\\ProgramData\\Kofax\\Kofax Express 3.2\\Jobs"]
MAIN_BACKUP_DIR = "c:\\kofax_backup"

BUNDLE_DIR = os.path.dirname(__file__)
IS_PROD = False
if os.path.basename(BUNDLE_DIR) == INTERNAL_DIR:
    BUNDLE_DIR = os.path.dirname(BUNDLE_DIR)
    IS_PROD = True


def get_bundle_dir():
    """Get bundle dir in prod or dev environment"""
    if IS_PROD:
        return BUNDLE_DIR
    else:  # dev mode
        root_dir = os.path.dirname(os.path.dirname(BUNDLE_DIR))
        if os.path.exists(os.path.join(root_dir, "dist", BUNDLE_NAME)):
            return os.path.join(root_dir, "dist", BUNDLE_NAME)
        elif os.path.exists(os.path.join(root_dir, "dist")):
            return os.path.join(root_dir, "dist")
        return root_dir


def get_current_version():
    """Get current version. Here to be used in setup.py without namespace problem."""
    if os.path.exists(os.path.join(BUNDLE_DIR, INTERNAL_DIR, "version.txt")):
        v_path = os.path.join(BUNDLE_DIR, INTERNAL_DIR, "version.txt")
    elif os.path.exists(os.path.join(BUNDLE_DIR, "version.txt")):  # dev mode
        v_path = os.path.join(BUNDLE_DIR, "version.txt")
    else:
        return "0.0.0"
    with open(v_path, "r") as file:
        return file.readline().strip()
