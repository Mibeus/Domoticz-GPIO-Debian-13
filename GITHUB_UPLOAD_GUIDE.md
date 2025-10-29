# Návod: Ako nahrať repozitár na GitHub z Windows

Tento návod ťa prevedie vytvorením GitHub repozitára a nahratím súborov **bez potreby Git príkazov**.

---

## 📋 Čo potrebuješ

- ✅ Windows PC
- ✅ GitHub účet (ak nemáš, vytvor si na https://github.com/signup)
- ✅ Webový prehliadač (Chrome, Firefox, Edge)
- ✅ Stiahnuté súbory z tohto projektu

---

## Metóda 1: Cez GitHub Web Interface (Najjednoduchšie)

### Krok 1: Vytvor nový repozitár na GitHub

1. **Prihlás sa** na https://github.com
2. Klikni na **zelené tlačidlo "New"** (hore vľavo vedľa "Repositories")
   - Alebo choď priamo na: https://github.com/new

3. **Vyplň údaje repozitára:**
   ```
   Repository name: domoticz-trixie-debian-gpio
   Description: Domoticz plugin for Waveshare Relay Board using libgpiod on Debian 13
   
   ☑️ Public (odporúčané - aby ho mohli ostatní používať)
   ☐ Private
   
   ☐ Add a README file (NEOZNAČ - máme vlastný)
   ☐ Add .gitignore (NEOZNAČ - máme vlastný)
   ☑️ Choose a license: MIT License
   ```

4. Klikni **"Create repository"**

### Krok 2: Nahraj súbory

1. Na stránke nového repozitára klikni na **"uploading an existing file"**
   - Alebo priamo: `https://github.com/Mibeus/domoticz-trixie-debian-gpio/upload/main`

2. **Drag & Drop** alebo klikni **"choose your files"**

3. **Vyber všetky tieto súbory:**
   ```
   ✅ plugin.py
   ✅ install.sh
   ✅ test_relay.py
   ✅ README.md
   ✅ LICENSE
   ✅ CHANGELOG.md
   ✅ .gitignore
   ```

4. Dole napíš commit message:
   ```
   Initial commit - Waveshare Relay Board plugin v1.0.0
   ```

5. Klikni **"Commit changes"**

6. **HOTOVO!** 🎉

---

## Metóda 2: Cez GitHub Desktop (Grafický nástroj)

### Krok 1: Nainštaluj GitHub Desktop

1. Stiahni GitHub Desktop: https://desktop.github.com/
2. Nainštaluj ho
3. Prihlás sa so svojím GitHub účtom

### Krok 2: Vytvor repozitár

1. Klikni **"File" → "New repository"**
2. Vyplň:
   ```
   Name: domoticz-trixie-debian-gpio
   Description: Domoticz plugin for Waveshare Relay Board
   Local path: C:\Users\Mibeus\Documents\GitHub\
   ☑️ Initialize with README (NEOZNAČ)
   Git ignore: None
   License: MIT License
   ```
3. Klikni **"Create repository"**

### Krok 3: Skopíruj súbory

1. Otvor priečinok repozitára vo Windows Exploreri:
   ```
   C:\Users\Mibeus\Documents\GitHub\domoticz-trixie-debian-gpio\
   ```

2. **Skopíruj** tam všetky súbory projektu:
   - plugin.py
   - install.sh
   - test_relay.py
   - README.md
   - LICENSE
   - CHANGELOG.md
   - .gitignore

### Krok 4: Commit a Push

1. Otvor **GitHub Desktop**
2. Uvidíš zoznam zmenených súborov vľavo
3. Dole vľavo napíš commit message:
   ```
   Initial commit - v1.0.0
   ```
4. Klikni **"Commit to main"**
5. Klikni **"Publish repository"** (hore)
6. Potvrď:
   - ☑️ Keep this code public
   - Klikni **"Publish repository"**

7. **HOTOVO!** 🎉

---

## Metóda 3: Cez Git Bash (Pre pokročilých)

### Krok 1: Nainštaluj Git

1. Stiahni Git: https://git-scm.com/download/win
2. Nainštaluj s defaultnými nastaveniami
3. Po inštalácii reštartuj PC

### Krok 2: Nakonfiguruj Git

Otvor **Git Bash** a spusti:

```bash
git config --global user.name "Tvoje Meno"
git config --global user.email "tvoj.email@example.com"
```

### Krok 3: Vytvor repozitár na GitHub

1. Choď na https://github.com/new
2. Vytvor repozitár s názvom: `domoticz-trixie-debian-gpio`
3. **NEOZNAČ** "Initialize this repository with a README"
4. Klikni "Create repository"

### Krok 4: Nahraj súbory

V **Git Bash** naviguj do priečinka so súbormi a spusti:

```bash
# Prejdi do priečinka so súbormi
cd /c/Users/Mibeus/Downloads/domoticz-trixie-debian-gpio

# Inicializuj Git repozitár
git init

# Pridaj všetky súbory
git add .

# Vytvor prvý commit
git commit -m "Initial commit - Waveshare Relay Board plugin v1.0.0"

# Pripoj sa na GitHub repozitár (ZMEŇ Mibeus)
git remote add origin https://github.com/Mibeus/domoticz-trixie-debian-gpio.git

# Premenuj branch na main
git branch -M main

# Nahraj na GitHub
git push -u origin main
```

Pri `git push` ťa GitHub požiada o prihlásenie.

**HOTOVO!** 🎉

---

## Overenie že všetko funguje

Po nahratí otvor v prehliadači:
```
https://github.com/Mibeus/domoticz-trixie-debian-gpio
```

Máš vidieť:
- ✅ README.md s pekným formátovaním
- ✅ Všetky súbory (plugin.py, install.sh, atď.)
- ✅ MIT License badge
- ✅ Zelené "Code" tlačidlo pre stiahnutie

---

## Ako aktualizovať repozitár neskôr

### Cez GitHub Web:

1. Otvor repozitár na GitHub
2. Klikni na súbor ktorý chceš upraviť
3. Klikni na ikonu ceruzky (Edit)
4. Uprav súbor
5. Commit changes

### Cez GitHub Desktop:

1. Uprav súbory lokálne
2. GitHub Desktop automaticky zdeteguje zmeny
3. Napíš commit message
4. Klikni "Commit to main"
5. Klikni "Push origin"

### Cez Git Bash:

```bash
# Uprav súbory
# Potom:
git add .
git commit -m "Popis zmeny"
git push
```

---

## Dôležité URL odkazy

Po vytvorení repozitára budeš mať:

- **Hlavná stránka:** `https://github.com/Mibeus/domoticz-trixie-debian-gpio`
- **Clone URL:** `https://github.com/Mibeus/domoticz-trixie-debian-gpio.git`
- **Raw súbory:** `https://raw.githubusercontent.com/Mibeus/domoticz-trixie-debian-gpio/main/plugin.py`

---

## Čo ďalej?

1. **Aktualizuj README.md** - zmeň `[TVOJ_USERNAME]` na tvoje skutočné GitHub meno
2. **Pridaj screenshot** - vlož obrázok Domoticz interface do `docs/images/`
3. **Napíš Issues template** - pre ľahšie reportovanie problémov
4. **Pridaj GitHub Topics** - (vo web interface: Settings → Topics)
   - `domoticz`
   - `raspberry-pi`
   - `gpio`
   - `home-automation`
   - `debian`
   - `relay-control`

---

## 💡 Tipy

- **GitHub badges** v README.md sa automaticky aktualizujú
- **Releases** - neskôr môžeš vytvoriť cez GitHub: Releases → Create a new release
- **Wiki** - môžeš pridať rozšírenú dokumentáciu
- **Discussions** - zapni v Settings pre komunitné diskusie

---

Ak máš akékoľvek problémy, daj vedieť! 🚀
