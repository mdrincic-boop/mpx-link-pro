# MPX over IP Pro - Build Instructions

## Prerequisites

- Python 3.8 or higher installed
- All dependencies from requirements.txt installed
- Windows OS (for .exe files) or Linux/macOS (for standalone binaries)

## Quick Build

### Windows

Simply run the batch file:
```bash
build_executables.bat
```

### Linux/macOS

Make the script executable and run it:
```bash
chmod +x build_executables.sh
./build_executables.sh
```

## Manual Build Process

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Icon Files

```bash
python create_icon.py
```

This will generate:
- `icon.png` - PNG icon for display
- `icon.ico` - Windows icon format

### 3. Build Sender Executable

```bash
pyinstaller --clean --noconfirm mpx_sender_pro.spec
```

### 4. Build Receiver Executable

```bash
pyinstaller --clean --noconfirm mpx_receiver_pro.spec
```

## Output

After successful build, executables will be located in:

```
dist/
├── MPX_Sender_Pro.exe (or MPX_Sender_Pro on Linux/macOS)
└── MPX_Receiver_Pro.exe (or MPX_Receiver_Pro on Linux/macOS)
```

## Distribution

### Files to Include in Production Package

1. **Executables** (from `dist/` folder):
   - `MPX_Sender_Pro.exe`
   - `MPX_Receiver_Pro.exe`

2. **Configuration** (optional):
   - `.env` file with Supabase credentials (if using cloud features)

3. **Documentation**:
   - `README_MPX.txt`
   - `BUILD_INSTRUCTIONS.md` (this file)

### Recommended Folder Structure for Distribution

```
MPX_over_IP_Pro_v2.0/
├── MPX_Sender_Pro.exe
├── MPX_Receiver_Pro.exe
├── README_MPX.txt
├── .env.example (template for users)
└── logs/ (will be created automatically)
```

## Testing the Executables

### 1. Test Sender

Double-click `MPX_Sender_Pro.exe` or run from command line:
```bash
cd dist
MPX_Sender_Pro.exe
```

### 2. Test Receiver

Double-click `MPX_Receiver_Pro.exe` or run from command line:
```bash
cd dist
MPX_Receiver_Pro.exe
```

### 3. Test Connection

1. Start the Sender first (it will listen on specified port)
2. Start the Receiver and connect to sender's IP address
3. Click "Start Stream" on sender
4. Monitor VU meters and audio output

## Troubleshooting

### Build Issues

**Problem**: PyInstaller not found
```bash
pip install --upgrade pyinstaller
```

**Problem**: Missing dependencies during build
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem**: Icon file not found
```bash
python create_icon.py
```

### Runtime Issues

**Problem**: "Missing DLL" errors on Windows
- Install Visual C++ Redistributable 2015-2022
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Problem**: Audio device not detected
- Ensure PortAudio is installed on the system
- On Windows, it's included with sounddevice package
- On Linux: `sudo apt-get install portaudio19-dev`

**Problem**: Antivirus blocking executable
- Add executables to antivirus exclusion list
- This is common with PyInstaller-built applications

## Advanced Customization

### Changing Icon

1. Replace `icon.ico` with your custom icon
2. Rebuild using PyInstaller

### Changing Executable Name

Edit the `.spec` files and modify the `name` parameter:
```python
exe = EXE(
    ...
    name='Your_Custom_Name',
    ...
)
```

### Adding Resources

To include additional files (config, presets, etc.):

Edit the `.spec` file and add to `datas`:
```python
datas=[
    ('config.json', '.'),
    ('presets/*.json', 'presets'),
],
```

### Reducing File Size

Remove console window and enable UPX compression (already configured):
```python
console=False,
upx=True,
```

Current executable size: ~60-80 MB (includes Python runtime and all dependencies)

## Code Signing (Optional)

For production deployment, consider code signing your executables:

### Windows
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com MPX_Sender_Pro.exe
```

### macOS
```bash
codesign --deep --force --verify --verbose --sign "Developer ID" MPX_Sender_Pro
```

## Deployment Checklist

- [ ] All dependencies installed
- [ ] Icon files generated
- [ ] Executables built successfully
- [ ] Sender tested standalone
- [ ] Receiver tested standalone
- [ ] Connection tested between sender/receiver
- [ ] Audio quality verified
- [ ] All features tested (AGC, Limiter, Encryption, etc.)
- [ ] Documentation included
- [ ] .env.example provided
- [ ] Version number updated in code
- [ ] Code signed (if applicable)
- [ ] Antivirus tested
- [ ] Package compressed (ZIP/installer)

## Version Information

**MPX over IP Pro v2.0**
- Release Date: October 2025
- Build System: PyInstaller 6.11.1
- Python Version: 3.8+
- Target OS: Windows 10/11, Linux, macOS

## Support

For build issues or questions, check:
1. Python version compatibility
2. All requirements installed
3. No conflicting packages
4. Sufficient disk space (~500MB for build process)

## Notes

- First build may take 5-10 minutes
- Subsequent builds are faster (cached)
- UPX compression reduces file size but increases build time
- Console mode disabled for cleaner user experience
- Single-file executable contains entire Python runtime
