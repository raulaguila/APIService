import os

from cx_Freeze import setup, Executable

packages_include = [
    "os",
    "logging.config",
    "uvicorn",
    "fastapi",
    "websockets"
]

files_include = [
    os.path.join(os.getcwd(), 'configs')
]

modules_exclude: list = ["tkinter"]

modules_include: list = ["ServiceHandler"]

# Get all your modules in src folder
for folder in os.listdir(os.path.join(os.getcwd(), 'src')):
    if folder != '__pycache__' and os.path.isdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
        modules_include.append(f'src.{folder}')
        for module in os.listdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
            if module != '__pycache__' and '.py' in module:
                modules_include.append(f'src.{folder}.{module[:-3]}')

    if folder != '__pycache__' and '.py' in folder:
        modules_include.append(f'src.{folder[:-3]}')

setup(
    name="API - Windows Service",
    version="0.0.1",
    description="Sample of API rest as a windows service in python with cx_Freeze",
    executables=[Executable(
        "Config.py",
        base="Win32Service",
        target_name="APIWindowsService",
    )],
    options={
        "build_exe": {
            "packages": packages_include,
            "includes": modules_include,
            "excludes": modules_exclude,
            "include_files": files_include
        }
    },
)
