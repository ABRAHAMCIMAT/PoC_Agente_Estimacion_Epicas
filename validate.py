#!/usr/bin/env python3
"""
Validation script to check if all project files are in place.
"""

import os
import json
import sys
from pathlib import Path

def check_file(path, description=""):
    """Check if a file exists."""
    exists = Path(path).exists()
    status = "[OK]" if exists else "[MISS]"
    print(f"  {status} {path.replace(chr(92), '/')} {description}")
    return exists

def check_json(path):
    """Validate JSON file."""
    try:
        with open(path) as f:
            json.load(f)
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False

def main():
    os.chdir(Path(__file__).parent)
    print("Epic Estimation System - Validation Report\n")
    print("=" * 60)
    
    all_ok = True
    
    # Check backend structure
    print("\n[Backend Structure]")
    backend_files = [
        ("backend/__init__.py", ""),
        ("backend/app/__init__.py", ""),
        ("backend/app/main.py", "FastAPI application"),
        ("backend/models/__init__.py", ""),
        ("backend/models/epic_estimation_models.py", "ML models"),
        ("backend/utils/__init__.py", ""),
        ("backend/utils/data_preprocessing.py", "Data processing"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/Dockerfile", "Docker image"),
    ]
    
    for file, desc in backend_files:
        if not check_file(file, desc):
            all_ok = False
    
    # Check frontend structure
    print("\n[Frontend Structure]")
    frontend_files = [
        ("frontend/package.json", "Node dependencies"),
        ("frontend/next.config.js", "Next.js config"),
        ("frontend/pages/index.jsx", "Main page"),
        ("frontend/pages/_app.jsx", "App wrapper"),
        ("frontend/components/Header.jsx", "Header component"),
        ("frontend/components/ExcelUpload.jsx", "Upload component"),
        ("frontend/components/EstimationResults.jsx", "Results component"),
        ("frontend/styles/globals.css", "Styles"),
        ("frontend/Dockerfile", "Docker image"),
    ]
    
    for file, desc in frontend_files:
        if not check_file(file, desc):
            all_ok = False
    
    # Check documentation
    print("\n[Documentation]")
    docs = [
        ("README.md", "Main documentation"),
        ("QUICKSTART.md", "Quick start guide"),
        ("API_TESTING.md", "API testing guide"),
        ("IMPLEMENTATION_SUMMARY.md", "Summary"),
    ]
    
    for file, desc in docs:
        if not check_file(file, desc):
            all_ok = False
    
    # Check configuration files
    print("\n[Configuration]")
    config_files = [
        ("docker-compose.yml", "Docker Compose"),
        ("start.bat", "Windows startup"),
        (".gitignore", "Git ignore"),
    ]
    
    for file, desc in config_files:
        if not check_file(file, desc):
            all_ok = False
    
    # Check data files
    print("\n[Data Files]")
    data_files = [
        ("Jira (3).csv", "Training data"),
        ("HU_260226.xlsx", "Test data"),
    ]
    
    for file, desc in data_files:
        exists = Path(file).exists()
        status = "[OK]" if exists else "[WARN]"
        print(f"  {status} {file} {desc} {'(required for training)' if not exists else ''}")
    
    # Validate JSON files
    print("\n[JSON Validation]")
    
    if check_json("frontend/package.json"):
        print(f"  [OK] frontend/package.json is valid JSON")
    else:
        print(f"  [ERR] frontend/package.json is INVALID")
        all_ok = False
    
    # Check Python syntax
    print("\n[Python Syntax Check]")
    import subprocess
    
    python_files = [
        "backend/app/main.py",
        "backend/models/epic_estimation_models.py",
        "backend/utils/data_preprocessing.py",
    ]
    
    for file in python_files:
        try:
            result = subprocess.run(
                ["py", "-3", "-m", "py_compile", file],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"  [OK] {file}")
            else:
                print(f"  [ERR] {file}: {result.stderr.decode()}")
                all_ok = False
        except Exception as e:
            print(f"  [WARN] {file}: Could not check ({e})")
    
    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("[SUCCESS] All critical files are in place!")
        print("\nNext steps:")
        print("1. Run: start.bat")
        print("2. Wait for services to start")
        print("3. Open: http://localhost:3000")
        print("4. Upload Jira (3).csv to train models")
        print("5. Upload HU_260226.xlsx for testing")
        return 0
    else:
        print("[WARNING] Some files are missing!")
        print("\nPlease ensure all files are created properly.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
