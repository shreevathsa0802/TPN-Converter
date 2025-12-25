"""
Setup file for creating Windows executable
"""

from cx_Freeze import setup, Executable
import sys

# Dependencies
build_exe_options = {
    "packages": ["tkinter", "numpy", "json", "os"],
    "excludes": [],
    "include_files": ["assets/", "converter.py"]
}

# Base for Windows GUI
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TPN Converter",
    version="2.0",
    description="Two-Port Network Parameter Converter",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", 
                          base=base,
                          target_name="TPN_Converter.exe",
                          icon="assets/icon.ico")]
)