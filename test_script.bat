@echo off
REM Test script for generate_packer.py
REM Run this script to test the Packer HCL generator

echo ========================================
echo Testing generate_packer.py
echo ========================================

cd /d "%~dp0"

echo.
echo [Test 1] Generating Packer HCL for rocky97...
python generate_packer.py --config rocky97

echo.
echo [Test 2] Generating Packer HCL for rocky98...
python generate_packer.py --config rocky98

echo.
echo ========================================
echo Tests completed!
echo ========================================

pause
