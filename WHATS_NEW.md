# What's New in MPX Link PRO v1.0.0

## 🎉 New Features

### 1. GitHub Actions - Automatic ISO Builds
- ✅ **Push to GitHub → Get ISO in 25 minutes!**
- ✅ No Linux machine needed for building
- ✅ Automatic builds on every push
- ✅ Release creation on version tags
- ✅ Cross-platform packages (Windows, Linux, macOS)

**Files Added:**
- `.github/workflows/build-iso.yml` - Main ISO builder workflow
- `.github/workflows/test.yml` - Quick test workflow
- `.github/README.md` - Workflows documentation

**Benefits:**
- No manual ISO building
- Consistent builds every time
- Free (2000 minutes/month on GitHub)
- Store all versions in Releases

---

### 2. Network Configuration GUI
- ✅ **Configure IP/Gateway/DNS from the app!**
- ✅ DHCP or Static IP with one click
- ✅ Shows current network configuration
- ✅ Common DNS servers presets (Google, Cloudflare, etc.)
- ✅ Interface selection (eth0, wlan0, etc.)
- ✅ Persistent configuration (survives reboot)

**Files Added:**
- `electron-app/src/renderer/components/NetworkPanel.tsx` - Network GUI
- `NETWORK_CONFIG_GUIDE.md` - Complete network setup guide

**Backend Changes:**
- `electron-app/src/python/backend.py` - Added `get_network_info()` and `configure_network()`
- Uses NetworkManager (nmcli) for configuration
- CIDR/Netmask conversion helpers

**How to Use:**
1. Open MPX Link PRO
2. Click "Network" tab
3. Choose DHCP or Static
4. Enter IP/Gateway/DNS
5. Click "Apply"

---

### 3. ISO Builder - Complete System
- ✅ **Bootable Debian 12 Linux ISO**
- ✅ Auto-boot to kiosk mode
- ✅ Electron app pre-installed
- ✅ All audio drivers included
- ✅ NetworkManager for easy network config
- ✅ ~500 MB compressed ISO

**Files Added:**
- `iso-builder/build-iso.sh` - ISO build script
- `iso-builder/README.md` - ISO builder documentation

**What's Inside:**
- Debian 12 (Bookworm) base
- Linux kernel 6.1
- Node.js 20
- Python 3.11
- Audio: ALSA, PulseAudio, PortAudio
- GUI: Openbox, LightDM
- Auto-login as `mpxuser` (password: `mpxlink`)

---

### 4. Documentation - Complete Guides
- ✅ **Step-by-step guides for everything!**
- ✅ GitHub Actions usage
- ✅ Network configuration
- ✅ ISO building and deployment
- ✅ Troubleshooting tips

**Files Added:**
- `UPLOAD_TO_GITHUB.md` - **START HERE** - GitHub upload guide
- `GITHUB_ACTIONS_GUIDE.md` - Complete GitHub Actions guide (Serbian)
- `NETWORK_CONFIG_GUIDE.md` - Network setup guide (Serbian)
- `QUICK_START.txt` - Quick start checklist
- `WHATS_NEW.md` - This file!

**Existing Updated:**
- `README.md` - Updated with new features
- `BUILD_AND_DEPLOY_GUIDE.md` - Added GitHub Actions info

---

### 5. Helper Scripts
- ✅ **Check if everything is ready before push!**

**Files Added:**
- `check-github-files.sh` - Linux/Mac file checker
- `check-github-files.bat` - Windows file checker

**Usage:**
```bash
# Linux/Mac
./check-github-files.sh

# Windows
check-github-files.bat
```

Shows which files are present and ready for GitHub!

---

## 📦 File Structure Changes

### New Directories:
```
.github/
  workflows/
    build-iso.yml       # Main ISO builder
    test.yml            # Quick tests
  ISSUE_TEMPLATE/
    bug_report.md       # Bug report template
  README.md             # Workflows docs

iso-builder/
  build-iso.sh          # ISO build script (executable)
  README.md             # ISO builder docs
```

### New Root Files:
```
GITHUB_ACTIONS_GUIDE.md   # GitHub Actions complete guide
NETWORK_CONFIG_GUIDE.md   # Network setup guide
UPLOAD_TO_GITHUB.md       # **START HERE** upload guide
QUICK_START.txt           # Quick checklist
WHATS_NEW.md              # This file
check-github-files.sh     # File checker (Linux/Mac)
check-github-files.bat    # File checker (Windows)
```

### Updated Files:
```
README.md                           # Added new features
electron-app/src/renderer/App.tsx   # Added Network tab
electron-app/src/python/backend.py  # Added network functions
electron-app/package-lock.json      # Generated (needed for GitHub Actions)
```

---

## 🚀 Workflow: From Code to ISO

### Old Way (Manual):
1. Install Linux
2. Install dependencies
3. Build Electron app
4. Run ISO builder script
5. Wait 20 minutes
6. Upload ISO somewhere
7. Share link

**Time:** 2-3 hours setup + 20 min per build

### New Way (GitHub Actions):
1. Push code to GitHub
2. Wait 25 minutes
3. Download ISO from Actions

**Time:** 25 minutes (fully automatic!)

---

## 🎯 Use Cases

### For Developers:
- Develop locally with `npm run dev`
- Push to GitHub when ready
- Get ISO automatically
- Test on real hardware
- Release with version tags

### For End Users:
- Download ISO from Releases
- Burn to USB
- Boot hardware
- Configure network in GUI
- Start streaming!

### For Broadcasting:
- Deploy to dedicated hardware (Intel NUC, etc.)
- Configure network via GUI
- Auto-start on boot
- Reliable 24/7 operation

---

## 🔧 Technical Details

### GitHub Actions Workflow:

```yaml
1. build-electron-app (3 min)
   - Install Node.js 20
   - npm ci (cached)
   - npm run build
   - Upload artifacts

2. build-iso (18 min)
   - Download Electron build
   - Install ISO tools
   - Run debootstrap (Debian base)
   - Install packages
   - Copy Electron app
   - Configure kiosk mode
   - Create squashfs
   - Generate bootable ISO
   - Upload ISO artifact

3. build-electron-packages (10 min)
   - Build for Windows/Linux/macOS
   - Create installers
   - Upload packages

Total: ~25 minutes
```

### Network Configuration:

```python
# Backend (Python)
get_network_info()
  → Reads: ip addr, ip route, /etc/resolv.conf
  → Returns: IP, netmask, gateway, DNS

configure_network(config)
  → Uses: nmcli (NetworkManager)
  → Creates connection: mpx-eth0
  → Applies: DHCP or Static IP
  → Persistent: Survives reboot
```

### ISO Contents:

```
Debian 12 Base         (~200 MB)
├─ Linux Kernel 6.1
├─ systemd
├─ NetworkManager
└─ Basic utilities

Software Layer         (~150 MB)
├─ Node.js 20
├─ Python 3.11
├─ ALSA + PulseAudio
└─ PortAudio

GUI Layer              (~50 MB)
├─ Xorg
├─ Openbox
├─ LightDM
└─ Basic fonts

Application Layer      (~50 MB)
├─ MPX Link PRO (Electron)
├─ React frontend
├─ Python backend
└─ Auto-start scripts

Total ISO: ~450-500 MB (compressed)
```

---

## 📊 Comparison Table

| Feature | Before | After |
|---------|--------|-------|
| ISO Build | Manual (Linux needed) | Automatic (GitHub) |
| Build Time | 20 min + setup | 25 min (no setup) |
| Network Config | CLI only (nmcli) | GUI + CLI |
| Documentation | Basic | Complete guides |
| Release Process | Manual upload | Automatic (tags) |
| Cross-platform | Linux only | Windows/Linux/macOS |
| Testing | Local only | CI/CD with Actions |

---

## 🎊 Benefits

### For You:
- ✅ No Linux VM needed
- ✅ Push code → Get ISO
- ✅ Version control for ISOs
- ✅ Easy network setup
- ✅ Professional deployment

### For Users:
- ✅ Easy network configuration
- ✅ No command line needed
- ✅ Plug & play hardware
- ✅ Reliable releases
- ✅ Complete documentation

---

## 🔜 What's Next?

### Planned Features:
- [ ] Web interface for remote control
- [ ] Docker container deployment
- [ ] Mobile app for monitoring
- [ ] Multi-language support
- [ ] Hardware encoder support
- [ ] Cloud configuration sync
- [ ] SNMP monitoring

### Improvements:
- [ ] Smaller ISO size (optimization)
- [ ] Faster boot time
- [ ] More audio drivers
- [ ] WiFi configuration GUI
- [ ] Firmware updater

---

## 📝 Migration Guide

If you have old version:

### 1. Backup your config
```bash
# Nothing to backup (old version had no persistent config)
```

### 2. Pull new code
```bash
git pull origin main
```

### 3. Check files
```bash
./check-github-files.sh
```

### 4. Push to GitHub
```bash
git add .
git commit -m "Update to v1.0.0"
git push origin main
```

### 5. Download new ISO
Wait 25 min → Actions → Download ISO

---

## 🐛 Known Issues

### GitHub Actions:
- First build might take longer (no cache)
- Need public repo for free Actions
- ISO artifact expires after 90 days (use Releases!)

### Network Config:
- Requires NetworkManager (already in ISO)
- GUI config only works on Linux
- Windows/Mac uses system network settings

### ISO Builder:
- Requires ~10 GB free space on GitHub runners (no problem)
- Debian mirror speed varies (5-15 min)
- USB write takes 5-10 minutes

---

## ✅ Tested On

### Hardware:
- Intel NUC (various models)
- Generic x86_64 PCs
- AMD Ryzen systems
- Laptops (Dell, HP, Lenovo)

### USB Drives:
- SanDisk (8GB+)
- Kingston (8GB+)
- Generic USB sticks

### Audio Interfaces:
- M-Audio interfaces
- Focusrite Scarlett series
- Behringer U-PHORIA
- Generic USB audio

### Networks:
- Direct Ethernet (crossover/straight)
- Gigabit switches
- VLAN setups
- VPN connections (WireGuard)

---

## 💬 Feedback

Found a bug? Have a suggestion?

- GitHub Issues: https://github.com/mdrincic-boop/mpx-link-pro/issues
- Pull Requests welcome!
- Discussions: https://github.com/mdrincic-boop/mpx-link-pro/discussions

---

## 🙏 Credits

Built with:
- Electron + React + TypeScript
- Python + PortAudio
- Debian GNU/Linux
- GitHub Actions
- NetworkManager
- And many open source libraries!

---

**Version 1.0.0** - October 2025

**Enjoy the new features!** 🎉🎊🚀
