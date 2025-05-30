#!/usr/bin/env python3
"""
DarbitNet Repository Health Check
Validates the current state of the repository infrastructure.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False


def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status."""
    if Path(dir_path).exists() and Path(dir_path).is_dir():
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (MISSING)")
        return False


def run_command(command, description):
    """Run a command and check its status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: PASS")
            return True
        else:
            print(f"❌ {description}: FAIL - {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {str(e)}")
        return False


def main():
    print("🔍 DarbitNet Repository Health Check")
    print("=" * 50)
    
    # Change to repository root
    repo_root = Path(__file__).parent
    os.chdir(repo_root)
    
    total_checks = 0
    passed_checks = 0
    
    print("\n📁 Project Structure Checks:")
    structure_checks = [
        ("src", "Source directory"),
        ("tests", "Tests directory"), 
        ("utils", "Utilities directory"),
        ("docs", "Documentation directory"),
        ("3rdparty", "Third-party dependencies"),
        (".github", "GitHub configuration"),
        (".github/workflows", "GitHub Actions workflows"),
    ]
    
    for path, desc in structure_checks:
        total_checks += 1
        if check_directory_exists(path, desc):
            passed_checks += 1
    
    print("\n📄 Configuration Files Checks:")
    config_checks = [
        ("CMakeLists.txt", "CMake build configuration"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project documentation"),
        ("LICENSE", "License file"),
        (".gitignore", "Git ignore configuration"),
        (".gitmodules", "Git submodules configuration"),
        ("CONTRIBUTING.md", "Contribution guidelines"),
        ("AUDIT_REPORT.md", "Audit report"),
        ("pytest.ini", "Testing configuration"),
        (".flake8", "Code style configuration"),
        (".bandit", "Security scanning configuration"),
    ]
    
    for path, desc in config_checks:
        total_checks += 1
        if check_file_exists(path, desc):
            passed_checks += 1
    
    print("\n🔧 CI/CD Infrastructure Checks:")
    cicd_checks = [
        (".github/workflows/ci.yml", "Main CI/CD pipeline"),
        (".github/workflows/codeql.yml", "Security scanning workflow"),
        (".github/dependabot.yml", "Dependency update configuration"),
    ]
    
    for path, desc in cicd_checks:
        total_checks += 1
        if check_file_exists(path, desc):
            passed_checks += 1
    
    print("\n🧪 Testing Infrastructure Checks:")
    test_checks = [
        ("tests/test_utils.py", "Utility tests"),
        ("tests/test_setup_env.py", "Setup environment tests"),
        ("tests/test_e2e_benchmark.py", "Benchmark tests"),
        ("tests/test_project_structure.py", "Project structure tests"),
    ]
    
    for path, desc in test_checks:
        total_checks += 1
        if check_file_exists(path, desc):
            passed_checks += 1
    
    print("\n🔐 Git and Submodule Checks:")
    submodule_checks = [
        ("git status --porcelain", "Working directory clean"),
        ("git submodule status", "Submodules initialized"),
    ]
    
    for cmd, desc in submodule_checks:
        total_checks += 1
        if run_command(cmd, desc):
            passed_checks += 1
    
    print("\n🧪 Test Execution Check:")
    total_checks += 1
    if run_command("python -m pytest tests/ -v --tb=short", "Test suite execution"):
        passed_checks += 1
    
    print("\n" + "=" * 50)
    print(f"📊 HEALTH CHECK SUMMARY")
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    print(f"Success Rate: {(passed_checks/total_checks)*100:.1f}%")
    
    if passed_checks == total_checks:
        print("🎉 Repository health: EXCELLENT")
        return 0
    elif passed_checks >= total_checks * 0.8:
        print("✅ Repository health: GOOD")
        return 0
    elif passed_checks >= total_checks * 0.6:
        print("⚠️  Repository health: FAIR")
        return 1
    else:
        print("❌ Repository health: POOR")
        return 1


if __name__ == "__main__":
    sys.exit(main())