#!/bin/bash
set -e

echo "=== MPX Link PRO - ISO Builder ==="
echo "Building bootable Debian 12 Live ISO with MPX Link PRO pre-installed"
echo ""

# Configuration
ISO_NAME="mpx-link-pro-v1.0.0.iso"
WORK_DIR="$(pwd)/work"
ISO_DIR="$(pwd)/iso"
ROOTFS_DIR="$WORK_DIR/rootfs"

# Clean previous builds
echo "[1/8] Cleaning previous build..."
rm -rf "$WORK_DIR" "$ISO_DIR" "$ISO_NAME"
mkdir -p "$WORK_DIR" "$ISO_DIR" "$ROOTFS_DIR"

# Install required packages
echo "[2/8] Installing build dependencies..."
apt-get update
apt-get install -y \
    debootstrap \
    squashfs-tools \
    xorriso \
    isolinux \
    syslinux-efi \
    grub-pc-bin \
    grub-efi-amd64-bin \
    mtools \
    wget

# Create base Debian system
echo "[3/8] Creating Debian 12 (bookworm) base system..."
debootstrap --arch=amd64 bookworm "$ROOTFS_DIR" http://deb.debian.org/debian/

# Configure the system
echo "[4/8] Configuring system..."
cat > "$ROOTFS_DIR/etc/apt/sources.list" <<EOF
deb http://deb.debian.org/debian bookworm main contrib non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free-firmware
EOF

# Install packages in chroot
chroot "$ROOTFS_DIR" /bin/bash <<'CHROOT_SCRIPT'
export DEBIAN_FRONTEND=noninteractive

# Update and install packages
apt-get update
apt-get install -y \
    linux-image-amd64 \
    live-boot \
    systemd-sysv \
    network-manager \
    xorg \
    openbox \
    lightdm \
    sudo \
    python3 \
    python3-pip \
    python3-numpy \
    python3-sounddevice \
    portaudio19-dev \
    curl \
    wget \
    git

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Create user
useradd -m -s /bin/bash -G sudo mpxuser
echo "mpxuser:mpxlink" | chpasswd

# Auto-login configuration
mkdir -p /etc/lightdm/lightdm.conf.d/
cat > /etc/lightdm/lightdm.conf.d/autologin.conf <<EOF
[Seat:*]
autologin-user=mpxuser
autologin-user-timeout=0
EOF

# Cleanup
apt-get clean
rm -rf /var/lib/apt/lists/*
CHROOT_SCRIPT

echo "[5/8] Building Electron application..."
cd ../electron-app

# Build if not already built
if [ ! -d "dist" ]; then
    npm install
    npm run build
fi

# Install app to rootfs
echo "[6/8] Installing MPX Link PRO to ISO..."
mkdir -p "$ROOTFS_DIR/opt/mpx-link-pro"
cp -r dist node_modules src/python package.json "$ROOTFS_DIR/opt/mpx-link-pro/"

# Create autostart
mkdir -p "$ROOTFS_DIR/home/mpxuser/.config/openbox"
cat > "$ROOTFS_DIR/home/mpxuser/.config/openbox/autostart" <<'EOF'
#!/bin/bash
cd /opt/mpx-link-pro
npx electron . --kiosk &
EOF

chmod +x "$ROOTFS_DIR/home/mpxuser/.config/openbox/autostart"
chroot "$ROOTFS_DIR" chown -R mpxuser:mpxuser /home/mpxuser

# Create squashfs
echo "[7/8] Creating compressed filesystem..."
mkdir -p "$ISO_DIR/live"
mksquashfs "$ROOTFS_DIR" "$ISO_DIR/live/filesystem.squashfs" -comp xz -Xbcj x86

# Copy kernel and initrd
cp "$ROOTFS_DIR/boot/vmlinuz-"* "$ISO_DIR/live/vmlinuz"
cp "$ROOTFS_DIR/boot/initrd.img-"* "$ISO_DIR/live/initrd"

# Create GRUB config
mkdir -p "$ISO_DIR/boot/grub"
cat > "$ISO_DIR/boot/grub/grub.cfg" <<'EOF'
set timeout=5
set default=0

menuentry "MPX Link PRO Live" {
    linux /live/vmlinuz boot=live quiet splash
    initrd /live/initrd
}

menuentry "MPX Link PRO (Safe Mode)" {
    linux /live/vmlinuz boot=live nomodeset
    initrd /live/initrd
}
EOF

# Create ISO
echo "[8/8] Creating bootable ISO image..."
cd "$(dirname "$ISO_DIR")"

grub-mkrescue -o "../$ISO_NAME" "$ISO_DIR" \
    --volid "MPX_LINK_PRO" \
    --label "MPX_LINK_PRO"

cd ..
ls -lh "$ISO_NAME"
echo ""
echo "✅ ISO created successfully: $ISO_NAME"
echo "   Size: $(du -h "$ISO_NAME" | cut -f1)"
echo ""
echo "To write to USB:"
echo "   sudo dd if=$ISO_NAME of=/dev/sdX bs=4M status=progress"
