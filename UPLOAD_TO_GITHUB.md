# 🚀 Kako Upload-ovati na GitHub - KORAK PO KORAK

## ⚠️ VAŽNO: Ovi fajlovi su NOVI i treba ih dodati!

GitHub Actions **NEĆE** raditi ako ne upload-uješ **ceo `.github` folder**!

---

## 📋 Checklist Pre Push-a:

Proveri da li ovi fajlovi postoje u projektu:

```
✅ .github/workflows/build-iso.yml    (glavni workflow za ISO)
✅ .github/workflows/test.yml         (brzi test)
✅ .github/README.md                  (dokumentacija)
✅ iso-builder/build-iso.sh           (ISO build script)
✅ iso-builder/README.md              (ISO dokumentacija)
✅ electron-app/package-lock.json     (za GitHub Actions cache)
✅ GITHUB_ACTIONS_GUIDE.md            (kompletna dokumentacija)
✅ NETWORK_CONFIG_GUIDE.md            (network setup vodič)
```

---

## 🔧 Korak 1: Proveri Git Status

```bash
# Idi u projekat
cd D:\PROJEKTI\MPX\PRO-ISO

# Proveri status
git status
```

**Trebalo bi da vidiš:**
```
.github/
iso-builder/
electron-app/package-lock.json
GITHUB_ACTIONS_GUIDE.md
NETWORK_CONFIG_GUIDE.md
...i mnogo drugih fajlova
```

---

## 📦 Korak 2: Dodaj SVE Fajlove

```bash
# Dodaj SVE fajlove
git add .

# Proveri šta će se commit-ovati
git status
```

**Mora da bude zeleno:**
```
new file:   .github/workflows/build-iso.yml
new file:   .github/workflows/test.yml
new file:   iso-builder/build-iso.sh
...
```

---

## 💾 Korak 3: Commit

```bash
git commit -m "Add GitHub Actions for automatic ISO builds + Network config"
```

---

## 🌐 Korak 4: Push na GitHub

```bash
# Ako je prvi push:
git branch -M main
git push -u origin main

# Ako već postoji main branch:
git push origin main
```

---

## ✅ Korak 5: Proveri GitHub Actions

1. Idi na: `https://github.com/mdrincic-boop/mpx-link-pro`
2. Klikni na **"Actions"** tab (gornji meni)
3. Trebalo bi da vidiš:
   - ✅ "Build MPX Link PRO ISO" workflow
   - 🟡 Žuti krug = "in progress"
   - ✅ Zeleni check = "completed"
   - ❌ Crveni X = "failed"

---

## 📥 Korak 6: Download ISO (posle 20-25 min)

Kad se završi workflow (zeleni ✅):

1. Klikni na workflow run
2. Scroll dole do **"Artifacts"** sekcije
3. Klikni **"mpx-link-pro-iso"** → download ZIP
4. Unzip → `mpx-link-pro-v1.0.0.iso` ✅

---

## 🎯 Alternativa: Manual Trigger (odmah pokreni build)

Ako workflow nije automatski pokrenuo:

1. **Actions** tab
2. Levo: "Build MPX Link PRO ISO"
3. Desno: **"Run workflow"** dropdown
4. Izaberi branch: `main`
5. Klikni zeleno **"Run workflow"**

Za 20-25 min → ISO ready!

---

## 🐛 Troubleshooting

### Problem 1: ".github" folder nije upload-ovan

```bash
# Proveri da li postoji lokalno
ls -la .github/

# Ako postoji ali nije u git-u:
git add .github/
git add iso-builder/
git commit -m "Add GitHub Actions workflows"
git push
```

### Problem 2: "No workflows found"

Znači `.github/workflows/` folder nije upload-ovan!

```bash
# Force add
git add --force .github/workflows/
git commit -m "Add workflows"
git push
```

### Problem 3: Workflow pada odmah

Check logs:
1. Actions → Failed workflow → Klikni
2. Čitaj error (obično package.json problem)

**Najčešći fix:**
```bash
cd electron-app
npm install
git add package-lock.json
git commit -m "Add package-lock.json"
git push
```

### Problem 4: ISO se ne kreira

ISO build traje 15-20 min. Ako pada pre toga:
- Check `iso-builder/build-iso.sh` je executable
- Check script syntax

**Fix:**
```bash
chmod +x iso-builder/build-iso.sh
git add iso-builder/build-iso.sh
git commit -m "Make build script executable"
git push
```

---

## 📝 Git Komande Sažetak

```bash
# Kompletna procedura (kopij-paste):
cd D:\PROJEKTI\MPX\PRO-ISO
git add .
git status                    # proveri da su .github/ i iso-builder/ tu
git commit -m "GitHub Actions + ISO builder + Network config"
git push origin main

# Posle 2 min → Actions tab → vidiš workflow
# Posle 20 min → Artifacts → download ISO!
```

---

## 🎊 Kada Vidiš Ovo = USPEH!

```
Actions Tab:
  ✅ Build MPX Link PRO ISO
     └─ build-electron-app   (✅ 3 min)
     └─ build-iso            (✅ 18 min)
     └─ build-packages       (✅ 10 min)

Artifacts:
  📦 mpx-link-pro-iso (485 MB)
  📦 electron-app-build (45 MB)
  📦 electron-package-ubuntu-latest
  📦 electron-package-windows-latest
  📦 electron-package-macos-latest
```

---

## 🚀 Next Steps Posle Uspešnog Build-a

1. Download ISO iz Artifacts
2. Test na USB stick:
   ```bash
   # Linux
   sudo dd if=mpx-link-pro-v1.0.0.iso of=/dev/sdX bs=4M status=progress

   # Windows
   # Koristi Rufus (DD mode)
   ```
3. Boot test mašinu
4. Test aplikaciju
5. Kreiraj release:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

---

## 💡 Pro Tips

### Tip 1: Watch Build Live
Otvori Actions → Click workflow → Vidiš live log!

### Tip 2: Build Badge
Dodaj u README.md:
```markdown
![Build](https://github.com/mdrincic-boop/mpx-link-pro/workflows/Build%20MPX%20Link%20PRO%20ISO/badge.svg)
```

### Tip 3: Email Notifications
Settings → Notifications → Email on workflow failure

### Tip 4: Faster Builds
Edituj `.github/workflows/build-iso.yml`:
```yaml
on:
  push:
    tags:
      - 'v*'  # Samo na tagove, ne svaki push
```

---

## ✅ Final Checklist

Pre push-a, proveri:

- [ ] `.github/workflows/build-iso.yml` postoji
- [ ] `.github/workflows/test.yml` postoji
- [ ] `iso-builder/build-iso.sh` postoji i executable
- [ ] `electron-app/package-lock.json` postoji
- [ ] `git status` pokazuje sve fajlove
- [ ] Commit message je descriptive
- [ ] Push na **main** branch (ne master)
- [ ] GitHub repo je **public** (za besplatne Actions)

---

**Sada može push! Za 25 min imaš ISO! 🎉**

**Pitanja? Čitaj `GITHUB_ACTIONS_GUIDE.md` za detalje!**
