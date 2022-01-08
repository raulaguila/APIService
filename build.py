import os
from cx_Freeze import setup, Executable

packages_include = [
    "os",
    "logging.config",
    "uvicorn",
    "fastapi",
    "logging"
]

files_include = [
    os.path.join(os.getcwd(), 'configs')
]

options = {
    "build_exe": {
        "packages": packages_include,
        "includes": ["ServiceHandler", "cx_Logging"],
        "excludes": ["tkinter"],
        "include_files": files_include
    }
}

setup(
    name="API - Windows Service",
    version="0.0.1",
    description="Sample cx_Freeze Windows serice",
    executables=[Executable(
        "Config.py",
        base="Win32Service",
        target_name="APIWindowsService",
    )],
    options=options,
)
