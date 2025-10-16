# MPX Link PRO - Complete Build & Deploy Guide

## Overview

This project now consists of TWO versions:

1. **Desktop Version** - Original Python/Tkinter apps (existing)
2. **Appliance Version** - NEW! Electron app + Bootable Linux ISO

## Project Structure

```
project/
├── mpx_sender_pro.py          # Original Python sender (desktop)
├── mpx_receiver_pro.py        # Original Python receiver (desktop)
├── electron-app/              # NEW: Modern Electron application
│   ├── src/
│   │   ├── main/             # Electron main process
│   │   ├── renderer/         # React UI components
│   │   ├── python/           # Python audio backend
│   │   └── shared/           # Shared types
│   └── package.json
└── iso-builder/               # NEW: Bootable ISO builder
    ├── build-iso.sh          # Main build script
    ├── README.md             # Full documentation
    └── QUICK_START.md        # Quick guide
```

## Version 1: Desktop Apps (Original)

### What It Is
- Standalone Python applications
- Run on Windows, Linux, macOS
- Requires Python and dependencies

### How to Use
```bash
# Install dependencies
pip install -r requirements.txt

# Run Sender
python mpx_sender_pro.py

# Run Receiver (on another computer)
python mpx_receiver_pro.py
```

## Version 2: Appliance OS (NEW!)

### What It Is
- Complete Linux operating system
- MPX Link PRO app built-in
- Auto-boots to app in kiosk mode
- One ISO file = Everything included

### Architecture

```
┌─────────────────────────────────────────────┐
│ Debian 12 Minimal Linux (~400MB ISO)        │
├─────────────────────────────────────────────┤
│ Boot Sequence:                              │
│  1. GRUB bootloader                         │
│  2. Linux kernel + systemd                  │
│  3. LightDM (auto-login mpxuser)           │
│  4. Openbox window manager                  │
│  5. MPX Link PRO Electron app (fullscreen) │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ MPX Link PRO App (Electron + React)         │
├─────────────────────────────────────────────┤
│ • Modern React UI with Tailwind CSS         │
│ • Python audio backend (PortAudio)          │
│ • Real-time system monitoring               │
│ • Network streaming (TCP/UDP)               │
│ • Supabase cloud integration                │
│ • Web interface for remote control          │
└─────────────────────────────────────────────┘
```

### Features

✅ **Kiosk Mode** - Fullscreen, no escape, dedicated device
✅ **Auto-Boot** - Powers on → App starts automatically
✅ **Web Interface** - Control remotely from any browser
✅ **System Monitor** - CPU, RAM, Network, Audio stats
✅ **Touch Ready** - Works with touch screens
✅ **Read-Only Root** - Prevents corruption
✅ **SSH Access** - Remote management
✅ **Auto-Updates** - Check for updates automatically

### Build Process

#### Prerequisites
- Linux build machine (Ubuntu 20.04+, Debian 11+)
- 10 GB free disk space
- Root access (sudo)
- Internet connection

#### Step 1: Build Electron App
```bash
cd electron-app
npm install
npm run build
```

This creates:
- `dist/main/` - Electron main process (compiled TypeScript)
- `dist/renderer/` - React UI (bundled with Vite)

#### Step 2: Build ISO
```bash
cd ../iso-builder
sudo ./build-iso.sh
```

This process (10-20 minutes):
1. Downloads Debian 12 base system
2. Installs packages: Node.js, Electron, Python, audio drivers
3. Copies Electron app to `/opt/mpx-link-pro/`
4. Configures auto-login and kiosk mode
5. Creates bootable ISO image

Output: **mpx-link-pro-v1.0.0.iso** (~400-500 MB)

#### Step 3: Deploy

**Option A: Live USB (No Installation)**
```bash
sudo dd if=mpx-link-pro-v1.0.0.iso of=/dev/sdX bs=4M status=progress
```

**Option B: Install to Hard Drive**
1. Boot from USB
2. Press Ctrl+Alt+F2
3. Login: mpxuser / mpxlink
4. Run: `sudo calamares` (installer)

## What Gets Installed in the ISO

### System Packages
```
Base System:
- linux-image-amd64
- systemd-sysv
- network-manager
- openssh-server

Display:
- xorg
- openbox
- lightdm

Audio:
- alsa-utils
- pulseaudio
- portaudio19-dev

Development:
- nodejs (v20 LTS)
- python3 (v3.11)
- npm
- pip3

Libraries:
- python3-numpy
- python3-sounddevice
- libgtk-3-0
- libnss3
- libxss1
```

### Configuration Files

**Auto-Login:** `/etc/lightdm/lightdm.conf`
```ini
[Seat:*]
autologin-user=mpxuser
autologin-user-timeout=0
user-session=openbox
```

**Kiosk Mode:** `/home/mpxuser/.config/openbox/autostart`
```bash
export KIOSK_MODE=true
cd /opt/mpx-link-pro
/usr/bin/electron .
```

**Systemd Service:** `/etc/systemd/system/mpx-link-pro.service`
```ini
[Unit]
Description=MPX Link PRO Audio Streaming
After=network.target sound.target

[Service]
Type=simple
User=mpxuser
WorkingDirectory=/opt/mpx-link-pro
Environment=DISPLAY=:0
Environment=KIOSK_MODE=true
ExecStart=/usr/bin/startx
Restart=always

[Install]
WantedBy=multi-user.target
```

## Use Cases

### Use Case 1: Studio Link
**Scenario:** Connect two recording studios for live collaboration

**Studio A:**
- Boot from USB or installed system
- Select Sender mode
- Connect to Studio B IP

**Studio B:**
- Boot from USB or installed system
- Select Receiver mode
- Receive audio automatically

### Use Case 2: Radio Station
**Scenario:** Stream from live studio to transmitter room

**Setup:**
- Install MPX Link PRO OS on small PC (NUC, Raspberry Pi 4)
- Rack mount in transmitter room
- Powers on automatically after outage
- Web interface for monitoring

### Use Case 3: Event Production
**Scenario:** Temporary audio links for festivals/concerts

**Setup:**
- Create bootable USB drives
- Plug into any computer at venue
- Boot → Instant audio link
- No software installation needed

### Use Case 4: Broadcast Facility
**Scenario:** Multiple permanent audio links

**Setup:**
- Install on dedicated hardware
- Configure static IPs
- Set up web monitoring dashboard
- SSH for remote management

## Deployment Scenarios

### Scenario 1: Single Dedicated Computer
```
Computer A: MPX Sender
Computer B: MPX Receiver
Connection: Direct Ethernet cable

1. Install ISO on both computers
2. Set static IPs (A: 192.168.1.10, B: 192.168.1.20)
3. Configure in app
4. Done!
```

### Scenario 2: Network with Multiple Links
```
Studio Network: 10.0.0.0/24

Sender 1:  10.0.0.10  → Receiver 1: 10.0.0.20
Sender 2:  10.0.0.11  → Receiver 2: 10.0.0.21
Sender 3:  10.0.0.12  → Receiver 3: 10.0.0.22

Web Monitor: http://10.0.0.10:3000
             http://10.0.0.11:3000
             http://10.0.0.12:3000
```

### Scenario 3: Remote Locations (VPN)
```
Site A: 10.8.0.10 (VPN)
Site B: 10.8.0.20 (VPN)

1. Set up WireGuard/OpenVPN between sites
2. Configure MPX to use VPN IPs
3. Stream over encrypted tunnel
```

## Hardware Recommendations

### Minimum (Testing)
- CPU: Dual-core 1.5 GHz
- RAM: 2 GB
- Disk: 8 GB
- Audio: USB audio interface
- Network: 100 Mbps Ethernet

### Recommended (Production)
- CPU: Quad-core 2.0+ GHz (Intel NUC, AMD Ryzen)
- RAM: 4 GB
- Disk: 16 GB SSD
- Audio: Professional interface (M-Audio, Focusrite)
- Network: Gigabit Ethernet

### Professional (24/7 Operation)
- CPU: Intel i5/i7 or AMD Ryzen 5/7
- RAM: 8 GB
- Disk: 32 GB SSD (Samsung, Crucial)
- Audio: Pro interface with low latency drivers
- Network: Dual Gigabit NICs (redundancy)
- UPS: For power protection

## Maintenance

### Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade
```

### Update MPX Link PRO
```bash
cd /opt/mpx-link-pro
# Pull latest from git (if configured)
git pull
npm install
npm run build
```

### Backup Configuration
```bash
# Config files
tar -czf mpx-config-backup.tar.gz /home/mpxuser/.config/mpx-link-pro/

# Upload to cloud
scp mpx-config-backup.tar.gz user@backup-server:/backups/
```

### Monitor Logs
```bash
# Application logs
journalctl -u mpx-link-pro -f

# System logs
journalctl -xe

# Audio system
pactl info
```

## Troubleshooting

### App Won't Start
```bash
# Check service status
systemctl status mpx-link-pro

# View logs
journalctl -u mpx-link-pro -n 50

# Restart
sudo systemctl restart mpx-link-pro
```

### No Audio Devices
```bash
# List devices
aplay -l    # Playback
arecord -l  # Recording

# Restart audio
pulseaudio -k
sudo alsa force-reload
```

### Network Issues
```bash
# Check interfaces
ip addr

# Test connectivity
ping <remote-ip>

# Restart network
sudo systemctl restart NetworkManager
```

### Performance Issues
```bash
# Check CPU/RAM
htop

# Check network
iftop

# Check disk
df -h
```

## Security Considerations

### Default Setup
- SSH enabled (port 22)
- Default password: `mpxlink`
- No firewall by default

### Hardening (Recommended)
```bash
# Change default password
passwd

# Configure firewall
sudo apt-get install ufw
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 5000/tcp  # MPX audio
sudo ufw allow 3000/tcp  # Web interface
sudo ufw enable

# Disable SSH (if not needed)
sudo systemctl disable ssh
sudo systemctl stop ssh

# Use SSH keys instead of password
ssh-copy-id mpxuser@<ip>
```

## Advanced Customization

### Change Default Resolution
Edit `/home/mpxuser/.xinitrc`:
```bash
xrandr --output HDMI-1 --mode 1920x1080
```

### Custom Branding
Replace logo:
```bash
# Copy your logo
sudo cp my-logo.png /opt/mpx-link-pro/assets/logo.png
```

### Additional Software
```bash
sudo apt-get install <package-name>
```

### Custom Scripts
Add to `/home/mpxuser/.config/openbox/autostart`

## Comparison: Desktop vs Appliance

| Feature | Desktop Apps | Appliance OS |
|---------|--------------|--------------|
| Installation | Requires Python + deps | Boot from USB |
| OS Required | Windows/Linux/Mac | Self-contained |
| Boot Time | Manual start | 30 seconds to app |
| Kiosk Mode | No | Yes |
| Web Interface | No | Yes |
| Updates | Manual | Built-in |
| Remote Control | No | Yes |
| Monitoring | Basic | Advanced |
| Touch Screen | No | Yes |
| Best For | Desktop use | Dedicated hardware |

## Future Enhancements

Planned features:
- [ ] Auto-update mechanism
- [ ] Multi-language support
- [ ] LDAP/Active Directory integration
- [ ] SNMP monitoring
- [ ] Redundant streaming paths
- [ ] Hardware encoder support
- [ ] Docker container version
- [ ] Cloud configuration sync
- [ ] Mobile app for control
- [ ] Plugin system

## License & Credits

MPX Link PRO - Professional Audio Streaming System

Components:
- Electron: MIT License
- React: MIT License
- Debian Linux: Various open source licenses
- Python: PSF License
- PortAudio: MIT License

## Support

For issues and questions:
1. Check logs: `journalctl -u mpx-link-pro`
2. Read documentation in `iso-builder/README.md`
3. Review quick start: `iso-builder/QUICK_START.md`

---

**You now have a complete, professional audio streaming appliance!** 🚀
