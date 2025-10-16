# Network Configuration Guide - MPX Link PRO

## 🌐 Network Setup Options

MPX Link PRO nudi **3 načina** da podesite mrežu:

### 1. GUI (Graphical Interface) - NAJLAKŠE! ✅
### 2. CLI (Command Line) - Za napredne korisnike
### 3. nmcli (NetworkManager) - Direktno

---

## 🎨 **Opcija 1: GUI (u aplikaciji)**

### Kako koristiti:

1. Pokreni MPX Link PRO app
2. Klikni na **"Network"** tab (ikonica mreže)
3. Vidiš trenutnu konfiguraciju
4. Podesi kako hoćeš
5. Klikni **"Apply Network Configuration"**
6. Reboot (može biti potreban)

### DHCP (Automatski):
```
1. Izaberi network interface (eth0, wlan0...)
2. Klikni "DHCP (Automatic)"
3. Save
4. Gotovo! 🎉
```

### Static IP (Ručno):
```
1. Izaberi network interface
2. Klikni "Static IP"
3. Unesi:
   - IP Address:  192.168.1.100
   - Subnet Mask: 255.255.255.0
   - Gateway:     192.168.1.1
   - DNS 1:       8.8.8.8
   - DNS 2:       8.8.4.4
4. Save
5. Gotovo! 🎉
```

---

## 💻 **Opcija 2: CLI (Terminal commands)**

### Otvori terminal:
```bash
# Pritisni Ctrl+Alt+F2 (ako si u kiosk mode-u)
# Login: mpxuser / mpxlink
```

### Proveri trenutnu konfiguraciju:
```bash
# Vidi IP adresu
ip addr show

# Vidi gateway
ip route show default

# Vidi DNS
cat /etc/resolv.conf
```

### DHCP Setup:
```bash
# Kreiraj DHCP konekciju
sudo nmcli connection add \
  type ethernet \
  con-name mpx-eth0 \
  ifname eth0 \
  ipv4.method auto

# Aktiviraj
sudo nmcli connection up mpx-eth0
```

### Static IP Setup:
```bash
# Primer: 192.168.1.100/24, gateway 192.168.1.1
sudo nmcli connection add \
  type ethernet \
  con-name mpx-eth0 \
  ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 192.168.1.100/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns "8.8.8.8,8.8.4.4"

# Aktiviraj
sudo nmcli connection up mpx-eth0
```

---

## 🔧 **Opcija 3: nmcli (NetworkManager)**

NetworkManager je **built-in** u Debian/Ubuntu i kontroliše sve network konekcije.

### Osnovne komande:

```bash
# Lista svih interfejsa
nmcli device status

# Lista svih konekcija
nmcli connection show

# Vidi detalje konekcije
nmcli connection show mpx-eth0

# Obriši konekciju
sudo nmcli connection delete mpx-eth0

# Restartuj interface
sudo nmcli connection down mpx-eth0
sudo nmcli connection up mpx-eth0

# Restart NetworkManager servisa
sudo systemctl restart NetworkManager
```

---

## 📋 **Primeri Konfiguracija**

### Primer 1: Studio A i Studio B (Direct Link)

**Studio A (Sender):**
```
Interface:   eth0
Method:      Static
IP Address:  192.168.1.10
Netmask:     255.255.255.0
Gateway:     192.168.1.1
DNS:         8.8.8.8, 8.8.4.4
```

**Studio B (Receiver):**
```
Interface:   eth0
Method:      Static
IP Address:  192.168.1.20
Netmask:     255.255.255.0
Gateway:     192.168.1.1
DNS:         8.8.8.8, 8.8.4.4
```

**CLI komande:**

```bash
# Studio A
sudo nmcli connection add type ethernet con-name mpx-eth0 ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 192.168.1.10/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns "8.8.8.8,8.8.4.4"
sudo nmcli connection up mpx-eth0

# Studio B
sudo nmcli connection add type ethernet con-name mpx-eth0 ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 192.168.1.20/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns "8.8.8.8,8.8.4.4"
sudo nmcli connection up mpx-eth0
```

### Primer 2: Corporate Network (DHCP)

**Oba računara:**
```
Interface:   eth0
Method:      DHCP
```

**CLI:**
```bash
sudo nmcli connection add type ethernet con-name mpx-eth0 ifname eth0 ipv4.method auto
sudo nmcli connection up mpx-eth0
```

### Primer 3: Direct Cable (bez routera)

**Računar 1:**
```
IP: 10.0.0.1
Netmask: 255.255.255.0
Gateway: (prazno)
```

**Računar 2:**
```
IP: 10.0.0.2
Netmask: 255.255.255.0
Gateway: (prazno)
```

**CLI:**
```bash
# Računar 1
sudo nmcli connection add type ethernet con-name mpx-direct ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 10.0.0.1/24

# Računar 2
sudo nmcli connection add type ethernet con-name mpx-direct ifname eth0 \
  ipv4.method manual \
  ipv4.addresses 10.0.0.2/24
```

---

## 🔍 **Troubleshooting**

### Problem: Nema interneta

```bash
# Proveri IP
ip addr show eth0

# Proveri gateway
ip route show default

# Proveri DNS
cat /etc/resolv.conf

# Ping gateway
ping -c 4 192.168.1.1

# Ping Google DNS
ping -c 4 8.8.8.8

# Restart network
sudo systemctl restart NetworkManager
```

### Problem: Konekcija ne radi

```bash
# Proveri status interfejsa
nmcli device status

# Proveri da li je interface UP
ip link show eth0

# Dignute interface
sudo ip link set eth0 up

# Restart konekcije
sudo nmcli connection down mpx-eth0
sudo nmcli connection up mpx-eth0
```

### Problem: "Connection already exists"

```bash
# Obriši staru konekciju
sudo nmcli connection delete mpx-eth0

# Kreiraj novu
sudo nmcli connection add ...
```

### Problem: Promene se ne čuvaju posle reboot-a

```bash
# Proveri da li je konekcija autoconnect
nmcli connection show mpx-eth0 | grep autoconnect

# Postavi autoconnect
sudo nmcli connection modify mpx-eth0 connection.autoconnect yes
```

---

## 📡 **DNS Serveri (Preporuke)**

### Google DNS (Najbržii)
```
Primary:   8.8.8.8
Secondary: 8.8.4.4
```

### Cloudflare DNS (Privatnost)
```
Primary:   1.1.1.1
Secondary: 1.0.0.1
```

### Quad9 DNS (Sigurnost)
```
Primary:   9.9.9.9
Secondary: 149.112.112.112
```

### OpenDNS (Filtriranje)
```
Primary:   208.67.222.222
Secondary: 208.67.220.220
```

---

## 🌐 **Subnet Mask / CIDR Conversion**

| Subnet Mask     | CIDR | Usable IPs |
|-----------------|------|------------|
| 255.255.255.252 | /30  | 2          |
| 255.255.255.0   | /24  | 254        |
| 255.255.0.0     | /16  | 65,534     |
| 255.0.0.0       | /8   | 16,777,214 |

**Najčešće korišćeno:** 255.255.255.0 (/24)

---

## 🔐 **Security Best Practices**

### 1. Statične IP adrese za produkciju
```
✅ Lako upravljanje
✅ Predvidljivo rutiranje
✅ Lakše firewall pravila
```

### 2. Privatne IP adrese
```
10.0.0.0/8        (10.0.0.0 - 10.255.255.255)
172.16.0.0/12     (172.16.0.0 - 172.31.255.255)
192.168.0.0/16    (192.168.0.0 - 192.168.255.255)
```

### 3. Firewall (opciono)
```bash
# Instaliraj ufw
sudo apt install ufw

# Dozvoli SSH
sudo ufw allow 22/tcp

# Dozvoli MPX audio port
sudo ufw allow 5000/tcp

# Dozvoli web interface
sudo ufw allow 3000/tcp

# Enable firewall
sudo ufw enable
```

---

## 💡 **Pro Tips**

### Tip 1: Rezerviši IP na routeru
Ako koristiš DHCP, rezerviši IP adresu pomoću MAC adrese na routeru.

```bash
# Pronađi MAC adresu
ip link show eth0
```

### Tip 2: Napravi backup konfiguracije
```bash
# Export konekcije
nmcli connection export mpx-eth0 > ~/mpx-network-backup.nmconnection

# Import konekcije
sudo nmcli connection import type ethernet file ~/mpx-network-backup.nmconnection
```

### Tip 3: Koristi bond/team za redundancy
```bash
# Kreiraj bonded interface (za dual NICs)
sudo nmcli connection add type bond con-name bond0 ifname bond0 mode active-backup
sudo nmcli connection add type ethernet slave-type bond con-name bond0-slave1 ifname eth0 master bond0
sudo nmcli connection add type ethernet slave-type bond con-name bond0-slave2 ifname eth1 master bond0
```

---

## 📝 **Konfiguracioni Template**

Popuni ovaj template pre nego što kreneš:

```
===========================================
MPX Link PRO - Network Configuration
===========================================

Computer Name:    _________________________
Location:         _________________________

Network Settings:
  Interface:      [ ] eth0  [ ] wlan0  [ ] other: _______
  Method:         [ ] DHCP  [ ] Static IP

Static IP (if selected):
  IP Address:     ___.___.___.___
  Subnet Mask:    255.255.255.0
  Gateway:        ___.___.___.___
  DNS Primary:    8.8.8.8
  DNS Secondary:  8.8.4.4

Remote Connection:
  Remote IP:      ___.___.___.___
  Remote Port:    5000
  Local Port:     5000

Notes:
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## ✅ **Quick Checklist**

Pre nego što započneš streaming:

- [ ] IP adresa podešena i potvrđena
- [ ] Gateway dostupan (ping gateway)
- [ ] DNS radi (ping google.com)
- [ ] Remote računar dostupan (ping remote IP)
- [ ] Firewall pravila (ako ima)
- [ ] Konekcija se čuva posle reboot-a
- [ ] Testiran streaming 5+ minuta

---

## 🆘 **Hitna pomoć**

Ako ništa ne radi:

```bash
# 1. Reset NetworkManager
sudo systemctl restart NetworkManager

# 2. Obriši SVE konekcije i kreiraj novu
sudo nmcli connection delete $(nmcli -t -f NAME connection show)
sudo nmcli connection add type ethernet con-name mpx-eth0 ifname eth0 ipv4.method auto
sudo nmcli connection up mpx-eth0

# 3. Restart sistema
sudo reboot
```

---

**Sada imaš potpunu kontrolu nad mrežom! 🌐**

**Pitanja? Proveri GUI u aplikaciji ili koristi nmcli u terminalu!** 🚀
