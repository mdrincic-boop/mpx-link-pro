@echo off
echo ========================================
echo GitHub Actions - File Check
echo ========================================
echo.

set ERROR=0

echo Checking GitHub Actions files...
if exist ".github\workflows\build-iso.yml" (echo [OK] .github\workflows\build-iso.yml) else (echo [MISSING] .github\workflows\build-iso.yml & set ERROR=1)
if exist ".github\workflows\test.yml" (echo [OK] .github\workflows\test.yml) else (echo [MISSING] .github\workflows\test.yml & set ERROR=1)
if exist ".github\README.md" (echo [OK] .github\README.md) else (echo [MISSING] .github\README.md & set ERROR=1)

echo.
echo Checking ISO builder files...
if exist "iso-builder\build-iso.sh" (echo [OK] iso-builder\build-iso.sh) else (echo [MISSING] iso-builder\build-iso.sh & set ERROR=1)
if exist "iso-builder\README.md" (echo [OK] iso-builder\README.md) else (echo [MISSING] iso-builder\README.md & set ERROR=1)

echo.
echo Checking Electron app...
if exist "electron-app\package.json" (echo [OK] electron-app\package.json) else (echo [MISSING] electron-app\package.json & set ERROR=1)
if exist "electron-app\package-lock.json" (echo [OK] electron-app\package-lock.json) else (echo [MISSING] electron-app\package-lock.json & set ERROR=1)
if exist "electron-app\src" (echo [OK] electron-app\src\) else (echo [MISSING] electron-app\src\ & set ERROR=1)

echo.
echo Checking documentation...
if exist "GITHUB_ACTIONS_GUIDE.md" (echo [OK] GITHUB_ACTIONS_GUIDE.md) else (echo [MISSING] GITHUB_ACTIONS_GUIDE.md & set ERROR=1)
if exist "NETWORK_CONFIG_GUIDE.md" (echo [OK] NETWORK_CONFIG_GUIDE.md) else (echo [MISSING] NETWORK_CONFIG_GUIDE.md & set ERROR=1)
if exist "UPLOAD_TO_GITHUB.md" (echo [OK] UPLOAD_TO_GITHUB.md) else (echo [MISSING] UPLOAD_TO_GITHUB.md & set ERROR=1)

echo.
echo ========================================
if %ERROR%==0 (
    echo ALL FILES PRESENT!
    echo Ready to push to GitHub!
    echo.
    echo Next steps:
    echo   git add .
    echo   git commit -m "Add GitHub Actions"
    echo   git push origin main
) else (
    echo SOME FILES ARE MISSING!
    echo Check the list above and add missing files.
)
echo ========================================
echo.
pause
