#!/bin/bash

echo "========================================"
echo "GitHub Actions - File Check"
echo "========================================"

ERROR=0

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ MISSING: $1"
        ERROR=1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ MISSING: $1/"
        ERROR=1
    fi
}

echo ""
echo "Checking GitHub Actions files..."
check_file ".github/workflows/build-iso.yml"
check_file ".github/workflows/test.yml"
check_file ".github/README.md"

echo ""
echo "Checking ISO builder files..."
check_file "iso-builder/build-iso.sh"
check_file "iso-builder/README.md"

echo ""
echo "Checking Electron app..."
check_file "electron-app/package.json"
check_file "electron-app/package-lock.json"
check_dir "electron-app/src"

echo ""
echo "Checking documentation..."
check_file "GITHUB_ACTIONS_GUIDE.md"
check_file "NETWORK_CONFIG_GUIDE.md"
check_file "UPLOAD_TO_GITHUB.md"

echo ""
echo "Checking if build-iso.sh is executable..."
if [ -x "iso-builder/build-iso.sh" ]; then
    echo "✅ build-iso.sh is executable"
else
    echo "⚠️  WARNING: build-iso.sh is NOT executable"
    echo "   Run: chmod +x iso-builder/build-iso.sh"
fi

echo ""
echo "========================================"
if [ $ERROR -eq 0 ]; then
    echo "✅ ALL FILES PRESENT!"
    echo "Ready to push to GitHub!"
    echo ""
    echo "Next steps:"
    echo "  git add ."
    echo "  git commit -m 'Add GitHub Actions'"
    echo "  git push origin main"
else
    echo "❌ SOME FILES ARE MISSING!"
    echo "Check the list above and add missing files."
fi
echo "========================================"

exit $ERROR
