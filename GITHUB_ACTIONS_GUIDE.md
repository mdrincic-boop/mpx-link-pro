# GitHub Actions - Automatic ISO Build Guide

## 🎯 Zašto GitHub Actions?

**Umesto da instaliraš Linux lokalno, GitHub će build-ovati ISO za tebe - BESPLATNO!**

GitHub će:
✅ Automatski build-ovati ISO svaki put kad push-uješ kod
✅ Kreirati Release sa download linkom
✅ Čuvati sve verzije
✅ Besplatno (2000 minuta mesečno)

---

## 🚀 Setup (5 minuta)

### Korak 1: Kreiraj GitHub Repo

```bash
# Na GitHub.com
1. Klikni "New Repository"
2. Ime: mpx-link-pro
3. Public (mora biti public za besplatne Actions)
4. Klikni "Create Repository"
```

### Korak 2: Push Projekat na GitHub

```bash
# U Windows-u (Git Bash ili PowerShell)
cd C:\Path\To\Your\Project

# Inicijalizuj git (ako već nije)
git init

# Dodaj sve fajlove
git add .

# Commit
git commit -m "Initial commit - MPX Link PRO"

# Dodaj remote
git remote add origin https://github.com/YOUR_USERNAME/mpx-link-pro.git

# Push
git push -u origin main
```

### Korak 3: GitHub Actions se automatski pokreće!

GitHub će detektovati `.github/workflows/build-iso.yml` i odmah pokrenuti build!

---

## 📥 Kako downloadovati ISO

### Metoda 1: Actions Artifacts (posle svakog push-a)

1. Idi na tvoj GitHub repo
2. Klikni na **"Actions"** tab
3. Klikni na najnoviji workflow run (zeleni check mark ✅)
4. Scroll dole do **"Artifacts"** sekcije
5. Klikni **"mpx-link-pro-iso"** da download-uješ ZIP
6. Unzip → dobijaš ISO fajl! 🎉

**Artifacts se čuvaju 90 dana**

### Metoda 2: GitHub Releases (samo za verzije)

```bash
# Kreiraj verziju sa tagom
git tag v1.0.0
git push origin v1.0.0
```

Posle 20 min:
1. Idi na **"Releases"** tab
2. Vidiš "v1.0.0"
3. Download ISO direktno!

**Releases se čuvaju zauvek!**

---

## ⏱️ Build Times

| Faza | Vreme |
|------|-------|
| Build Electron app | 2-3 min |
| Build Linux ISO | 15-20 min |
| Upload artifacts | 1-2 min |
| **UKUPNO** | **~20-25 min** |

---

## 🎮 Workflow Options

### Opcija 1: Automatski na svaki push (default)

```bash
# Svaki put kad push-uješ:
git add .
git commit -m "Update feature"
git push

# GitHub automatski build-uje ISO!
```

### Opcija 2: Samo na tagove (štedi build minute)

Edituj `.github/workflows/build-iso.yml`:

```yaml
on:
  push:
    tags:
      - 'v*'  # Samo kad push-uješ v1.0.0, v1.0.1, itd.
```

Onda:
```bash
# ISO se pravi samo kad kreiras verziju
git tag v1.0.1
git push origin v1.0.1
```

### Opcija 3: Manual (kad ti trebaš)

1. Idi na **Actions** tab
2. Levo: "Build MPX Link PRO ISO"
3. Desno: Klikni **"Run workflow"**
4. Izaberi branch
5. Klikni zeleno "Run workflow"

---

## 📊 Što dobijaš nakon build-a?

### Artifacts (Actions tab):

1. **mpx-link-pro-iso** (500 MB)
   - Bootable ISO fajl
   - Spreman za burn na USB

2. **electron-app-build** (50 MB)
   - Compiled Electron app
   - Za ručnu instalaciju

3. **electron-package-ubuntu-latest**
   - Linux AppImage/deb paketi

4. **electron-package-windows-latest**
   - Windows installer (.exe)

5. **electron-package-macos-latest**
   - macOS app bundle

---

## 🔍 Kako pratiti build?

### Real-time praćenje:

1. Push kod
2. Odmah idi na **Actions** tab
3. Vidiš "workflow in progress" (žuti krug)
4. Klikni na njega
5. Vidiš live log (real-time)

### Email notifikacije:

GitHub šalje email ako build fail-uje!

### Badge u README:

Dodaj u README.md:
```markdown
![Build Status](https://github.com/YOUR_USERNAME/mpx-link-pro/workflows/Build%20MPX%20Link%20PRO%20ISO/badge.svg)
```

Pokazuje: ✅ passing ili ❌ failing

---

## 💰 Cena (BESPLATNO!)

### GitHub Free tier:
- **2000 minuta mesečno** (public repo)
- Jedan build = ~25 minuta
- **= 80 build-ova mesečno!**

### Artifact storage:
- Besplatno do 500 MB
- ISO je ~400-500 MB
- Artifacts se brišu posle 90 dana (auto)

### Releases:
- Neograničeno storage
- Zauvek se čuvaju

---

## 🛠️ Troubleshooting

### Problem 1: Build fails

**Check logs:**
1. Actions tab → Failed workflow
2. Klikni na crveni X
3. Expand failed step
4. Čitaj error

**Česti problemi:**
- **npm ci failed** → Proveravaj package.json
- **Permission denied** → Workflow ima sudo pristup (ne brini)
- **Out of disk space** → Retraži GitHub Actions, oni će fixati

### Problem 2: ISO nije kreiran

**Check:**
- Da li je `build-iso` job uspeo?
- Da li je `electron-app` build uspeo?
- Pogledaj logs

### Problem 3: Artifact missing

**Wait 2-3 min posle build-a** - upload traje!

Refresh page!

---

## 🎨 Customization

### Build samo main branch:

```yaml
on:
  push:
    branches: [ main ]
```

### Build svakog ponedeljka u 2AM:

```yaml
on:
  schedule:
    - cron: '0 2 * * 1'
```

### Skip Electron packages (brži build):

Edituj workflow, obriši `build-electron-packages` job.

---

## 📦 Šta tačno radi workflow?

### Job 1: Build Electron App (2-3 min)
```
1. Checkout code
2. Install Node.js 20
3. npm ci (install dependencies)
4. npm run build (compile TypeScript + bundle React)
5. Upload artifacts
```

### Job 2: Build ISO (15-20 min)
```
1. Download Electron build
2. Install debootstrap, squashfs-tools, xorriso...
3. Run ./build-iso.sh:
   - Download Debian 12 base (~200 MB)
   - Install packages (Node, Python, audio drivers)
   - Copy Electron app to /opt/mpx-link-pro
   - Configure auto-login + kiosk mode
   - Create squashfs filesystem
   - Generate bootable ISO
4. Upload ISO
```

### Job 3: Create Release (samo za tagove)
```
1. Detektuj tag (v1.0.0)
2. Kreiraj GitHub Release
3. Attach ISO file
4. Add release notes
```

---

## 📝 Example: Full Release Workflow

```bash
# 1. Razvoj lokalno
cd electron-app
npm run dev
# ... test, fix bugs ...

# 2. Commit changes
git add .
git commit -m "Add new audio processing feature"
git push

# 3. Wait 25 min, test ISO from Actions artifacts

# 4. Ako sve radi, release verziju:
git tag v1.0.0
git push origin v1.0.0

# 5. After 25 min → GitHub Release ready!
# Share link: https://github.com/USERNAME/mpx-link-pro/releases/tag/v1.0.0
```

---

## 🎯 Best Practices

### Za development:
- Test lokalno (`npm run dev`)
- Push samo kad je feature gotova
- Koristi branches za WIP

### Za releases:
- Semantic versioning: v1.0.0, v1.1.0, v2.0.0
- Tag only stable versions
- Write release notes

### Za štednju minuta:
- Build samo na tagove (ne svaki push)
- Koristi cache (već konfigurisano)
- Skip nepotrebne job-ove

---

## 🔥 Quick Commands

```bash
# Setup
git init
git remote add origin https://github.com/USER/REPO.git
git add .
git commit -m "Initial commit"
git push -u origin main

# Regular update
git add .
git commit -m "Update X"
git push

# Create release
git tag v1.0.0
git push origin v1.0.0

# View logs
git log --oneline

# Delete tag (if mistake)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

---

## ✅ Checklist

Pre prvog push-a:

- [ ] GitHub repo kreiran
- [ ] `.github/workflows/build-iso.yml` postoji
- [ ] `electron-app/package.json` ispravan
- [ ] `iso-builder/build-iso.sh` executable
- [ ] Git remote dodat
- [ ] README.md ažuriran

---

## 🎉 Rezultat

**Posle 25 minuta:**

✅ ISO fajl ready za download
✅ Windows/Linux/Mac paketi (opciono)
✅ Sve verzije sačuvane
✅ Automatski na svaki push
✅ 100% besplatno!

**Više nikad ne trebaš Linux mašinu za build! 🚀**

---

## 💡 Pro Tips

1. **Branch protection:** Konfiguriraj da workflow mora uspeti pre merge-a
2. **Matrix builds:** Testiraj na više Node verzija odjednom
3. **Caching:** Već konfigurisano (node_modules cache)
4. **Secrets:** Koristi za API keys (Settings → Secrets)
5. **Self-hosted runners:** Ako ti treba više moći (advanced)

---

## 🆘 Podrška

Ako nešto ne radi:
1. Check Actions logs (najdetaljnije)
2. Test lokalno prvo
3. Google error message
4. Check GitHub Actions status: https://www.githubstatus.com/

---

**Push, wait 25 min, download ISO! To je to! 🎊**
