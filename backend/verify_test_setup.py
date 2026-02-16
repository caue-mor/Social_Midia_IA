#!/usr/bin/env python3
"""
Test Setup Verification Script

Verifies that the test foundation is correctly installed and configured.
Run this script to check if all test dependencies are available.

Usage:
    python verify_test_setup.py
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False


def check_module(module_name, package_name=None):
    """Check if a Python module is installed."""
    package = package_name or module_name
    try:
        __import__(module_name)
        print(f"✅ {package}")
        return True
    except ImportError:
        print(f"❌ {package} - Install with: pip install {package}")
        return False


def check_file(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (missing)")
        return False


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("AgenteSocial Backend - Test Setup Verification")
    print("=" * 60 + "\n")

    all_checks = []

    # Python version
    print("\n1. Python Environment")
    print("-" * 40)
    all_checks.append(check_python_version())

    # Required modules
    print("\n2. Required Test Dependencies")
    print("-" * 40)
    all_checks.append(check_module("pytest"))
    all_checks.append(check_module("pytest_asyncio", "pytest-asyncio"))
    all_checks.append(check_module("pytest_env", "pytest-env"))
    all_checks.append(check_module("pytest_cov", "pytest-cov"))
    all_checks.append(check_module("jose", "python-jose"))

    # FastAPI dependencies
    print("\n3. FastAPI Dependencies")
    print("-" * 40)
    all_checks.append(check_module("fastapi"))
    all_checks.append(check_module("uvicorn"))
    all_checks.append(check_module("pydantic"))

    # Supabase
    print("\n4. Supabase Client")
    print("-" * 40)
    all_checks.append(check_module("supabase"))

    # Configuration files
    print("\n5. Configuration Files")
    print("-" * 40)
    all_checks.append(check_file("pyproject.toml", "PyProject config"))
    all_checks.append(check_file("pytest.ini", "Pytest config"))
    all_checks.append(check_file(".coveragerc", "Coverage config"))
    all_checks.append(check_file("Makefile", "Makefile"))

    # Test files
    print("\n6. Test Infrastructure")
    print("-" * 40)
    all_checks.append(check_file("tests/__init__.py", "Tests package"))
    all_checks.append(check_file("tests/conftest.py", "Fixtures"))
    all_checks.append(check_file("tests/utils.py", "Utilities"))
    all_checks.append(check_file("tests/factories.py", "Factories"))

    # Test files
    print("\n7. Test Files")
    print("-" * 40)
    all_checks.append(check_file("tests/test_health.py", "Health tests"))
    all_checks.append(check_file("tests/test_auth.py", "Auth tests"))
    all_checks.append(check_file("tests/test_chat.py", "Chat tests"))
    all_checks.append(check_file("tests/test_content.py", "Content tests"))

    # Documentation
    print("\n8. Documentation")
    print("-" * 40)
    all_checks.append(check_file("tests/README.md", "Full documentation"))
    all_checks.append(check_file("tests/QUICK_START.md", "Quick start"))
    all_checks.append(check_file("tests/INDEX.md", "Test index"))

    # Summary
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100 if total > 0 else 0

    print(f"Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("=" * 60 + "\n")

    if passed == total:
        print("✅ All checks passed! Test foundation is ready.")
        print("\nNext steps:")
        print("  1. Run tests: make test")
        print("  2. View coverage: make test-cov")
        print("  3. Read documentation: tests/README.md")
        return 0
    else:
        print("❌ Some checks failed. Please install missing dependencies.")
        print("\nTo install all dependencies:")
        print("  make install")
        print("\nOr manually:")
        print("  pip install pytest pytest-asyncio pytest-env pytest-cov")
        print("  pip install python-jose[cryptography]")
        print("  pip install fastapi uvicorn pydantic supabase")
        return 1


if __name__ == "__main__":
    sys.exit(main())
