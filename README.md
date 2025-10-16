# MPX Link PRO - Professional Audio Streaming System

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Professional, low-latency audio streaming system with modern UI and bootable Linux appliance.

## 🎯 What is MPX Link PRO?

A complete audio streaming solution that connects two computers over network for real-time, high-quality audio transmission. Perfect for:

- 🎙️ **Broadcasting** - Studio to transmitter links
- 🎵 **Live Production** - Multi-room audio distribution
- 🎬 **Film Production** - On-set audio monitoring
- 📻 **Radio Stations** - Remote studio connections
- 🎧 **Recording Studios** - Distributed recording setups

## ✨ Features

### Audio Streaming
- ✅ 48 kHz / 96 kHz / 192 kHz sample rates
- ✅ Ultra-low latency (5-20 ms)
- ✅ Multiple channel modes (Mono / Stereo / Multi-channel)
- ✅ Professional audio interfaces supported
- ✅ Real-time VU meters and monitoring
- ✅ Automatic reconnection
- ✅ Network quality monitoring

### User Interface
- ✅ Modern React + Electron GUI
- ✅ Real-time system monitoring (CPU, RAM, Network)
- ✅ Network configuration panel (GUI for IP/Gateway/DNS setup)
- ✅ Touch screen support
- ✅ Dark theme
- ✅ Kiosk mode for dedicated hardware
- ✅ Web interface for remote control

### Deployment Options
- ✅ **Desktop Apps** - Windows, Linux, macOS
- ✅ **Bootable ISO** - Complete Linux OS with app pre-installed
- ✅ **GitHub Actions** - Automatic ISO build on every push
- ✅ **Docker** - Containerized deployment (planned)

## 🚀 Quick Start

### Option 1: Desktop Application (Development)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/mpx-link-pro.git
cd mpx-link-pro

# Install and run Electron app
cd electron-app
npm install
npm run dev
```

### Option 2: Bootable Linux ISO (Production)

**Automatic build with GitHub Actions:**

1. Fork this repository
2. Push to GitHub
3. Wait 20 minutes
4. Download ISO from Actions → Artifacts

**Manual build (Linux machine required):**

```bash
cd iso-builder
sudo ./build-iso.sh
```

**Deploy:**
```bash
# Write ISO to USB drive
sudo dd if=mpx-link-pro-v1.0.0.iso of=/dev/sdX bs=4M status=progress
```

Boot from USB and the app starts automatically!

## 📚 Documentation

- [**UPLOAD_TO_GITHUB.md**](UPLOAD_TO_GITHUB.md) - **START HERE!** Step-by-step upload guide
- [**GITHUB_ACTIONS_GUIDE.md**](GITHUB_ACTIONS_GUIDE.md) - Automatic ISO building with GitHub
- [**NETWORK_CONFIG_GUIDE.md**](NETWORK_CONFIG_GUIDE.md) - Network setup (IP, Gateway, DNS)
- [**BUILD_AND_DEPLOY_GUIDE.md**](BUILD_AND_DEPLOY_GUIDE.md) - Complete build and deployment guide
- [**iso-builder/README.md**](iso-builder/README.md) - ISO builder technical docs

## 🏗️ Project Structure

```
mpx-link-pro/
├── electron-app/              # Modern Electron + React application
│   ├── src/
│   │   ├── main/             # Electron main process (Node.js)
│   │   ├── renderer/         # React UI components
│   │   ├── python/           # Python audio backend
│   │   └── shared/           # Shared TypeScript types
│   └── package.json
│
├── iso-builder/              # Bootable Linux ISO builder
│   ├── build-iso.sh         # Main build script
│   ├── README.md            # Detailed documentation
│   └── QUICK_START.md       # Quick guide
│
├── .github/                  # GitHub Actions workflows
│   └── workflows/
│       ├── build-iso.yml    # Automatic ISO builder
│       └── test-build.yml   # CI tests
│
├── mpx_sender_pro.py        # Original Python sender (legacy)
├── mpx_receiver_pro.py      # Original Python receiver (legacy)
├── audio_processing.py      # Audio processing utilities
├── encryption.py            # Audio encryption (optional)
├── monitoring.py            # System monitoring
└── requirements.txt         # Python dependencies
```

## 💻 System Requirements

### Desktop Application
- **OS:** Windows 10+, Ubuntu 20.04+, macOS 11+
- **RAM:** 2 GB minimum, 4 GB recommended
- **Network:** 100 Mbps Ethernet (Gigabit recommended)
- **Audio:** USB or PCI audio interface

### Bootable ISO (Target Hardware)
- **CPU:** Dual-core 1.5 GHz+ (Intel NUC / AMD Mini PC)
- **RAM:** 2 GB minimum, 4 GB recommended
- **Disk:** 8 GB minimum, 16 GB SSD recommended
- **Audio:** USB audio interface (M-Audio, Focusrite, etc.)
- **Network:** Gigabit Ethernet

### Build Requirements (ISO)
- **OS:** Ubuntu 20.04+ / Debian 11+ or GitHub Actions
- **Disk:** 10 GB free space
- **RAM:** 4 GB
- **Internet:** For downloading packages

## 🔧 Technology Stack

### Frontend
- **Electron 28** - Desktop application framework
- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Modern styling
- **Vite** - Fast build tool
- **Lucide React** - Icon library

### Backend
- **Python 3.11** - Audio processing
- **PortAudio** - Cross-platform audio I/O
- **NumPy** - Numerical processing
- **sounddevice** - Python audio interface

### System
- **Debian 12** - Base Linux distribution
- **systemd** - Service management
- **Openbox** - Lightweight window manager
- **LightDM** - Display manager

### DevOps
- **GitHub Actions** - CI/CD automation
- **debootstrap** - Debian system builder
- **squashfs-tools** - Filesystem compression
- **xorriso** - ISO image creation

## 📖 Usage

### Basic Setup (Two Computers)

**Computer 1 (Sender):**
1. Launch MPX Link PRO
2. Select "Sender" mode
3. Choose input device
4. Enter Computer 2's IP address
5. Click "Start Streaming"

**Computer 2 (Receiver):**
1. Launch MPX Link PRO
2. Select "Receiver" mode
3. Choose output device
4. Click "Start Streaming"
5. Audio plays automatically!

### Default Credentials (ISO)
- **Username:** `mpxuser`
- **Password:** `mpxlink`
- **SSH:** Enabled on port 22
- **Web Interface:** http://IP-ADDRESS:3000

## 🎨 Screenshots

### Main Interface
![Main UI](https://via.placeholder.com/800x600.png?text=MPX+Link+PRO+Main+Interface)

### System Monitor
![Monitoring](https://via.placeholder.com/800x600.png?text=System+Monitoring)

### Settings
![Settings](https://via.placeholder.com/800x600.png?text=Settings+Panel)

## 🔐 Security

### Network
- TCP streaming (reliable)
- Optional encryption (AES-256)
- Authentication support
- Firewall ready

### System (ISO)
- Read-only root filesystem (optional)
- Minimal attack surface
- SSH key authentication recommended
- Regular security updates

## 🌐 Network Configuration

### Direct Connection (Simple)
```
Computer A: 192.168.1.10
Computer B: 192.168.1.20
Connection: Direct Ethernet cable
```

### Studio Network (Multiple Links)
```
Network: 10.0.0.0/24
Sender 1  (10.0.0.10) → Receiver 1 (10.0.0.20)
Sender 2  (10.0.0.11) → Receiver 2 (10.0.0.21)
```

### Remote Locations (VPN)
```
Site A: 10.8.0.10 (WireGuard VPN)
Site B: 10.8.0.20 (WireGuard VPN)
Stream over encrypted tunnel
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Electron team for the framework
- React team for the UI library
- Debian project for the stable Linux base
- PortAudio developers for cross-platform audio
- All open source contributors

## 📞 Support

- **Documentation:** See [docs](BUILD_AND_DEPLOY_GUIDE.md)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@mpxlink.pro (if applicable)

## 🗺️ Roadmap

- [x] Desktop application
- [x] Bootable Linux ISO
- [x] GitHub Actions automation
- [x] System monitoring
- [ ] Web interface (in progress)
- [ ] Docker container
- [ ] Mobile app for control
- [ ] Cloud configuration sync
- [ ] Multi-language support
- [ ] Hardware encoder support
- [ ] SNMP monitoring

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ for professional audio engineers**

**Version 1.0.0** | [Changelog](CHANGELOG.md) | [Releases](https://github.com/YOUR_USERNAME/mpx-link-pro/releases)
