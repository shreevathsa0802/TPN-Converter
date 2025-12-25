"""
Build script for creating Windows executable
"""

import os
import sys
import subprocess

def build_executable():
    print("Building TPN Converter executable...")
    print("-" * 50)
    
    # Install required packages
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Build executable
    print("\nBuilding executable...")
    subprocess.check_call([sys.executable, "setup.py", "build"])
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("Executable located in: build/exe.win-amd64-3.x/")
    print("You can share the entire folder as a portable application.")

if __name__ == "__main__":
    build_executable()