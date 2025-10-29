# Domoticz Trixie Debian GPIO Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Domoticz](https://img.shields.io/badge/Domoticz-2025.2+-green.svg)](https://www.domoticz.com/)
[![Debian](https://img.shields.io/badge/Debian-13%20Trixie-red.svg)](https://www.debian.org/)

Moderný Python plugin pre Domoticz na ovládanie **Waveshare RPi Relay Board (B)** pomocou **libgpiod** knižnice. Riešenie pre **Debian 13 (Trixie)** kde už nefunguje staré WiringPi.

---

## 🎯 Problém a riešenie

### Problém
- **WiringPi** je deprecated od 2019
- **sysfs GPIO** (`/sys/class/gpio`) je deprecated od Linux kernel 4.8
- Na Debian 13 (Trixie) už **neexistuje cesta** ako ovládať GPIO cez staré metódy
- Máte stovky vyrobených DPS s relé a potrebujete ich prevádzkovať

### Riešenie
✅ Tento plugin používa **libgpiod** - moderný, oficiálne podporovaný GPIO interface  
✅ Funguje na **Debian 13 Trixie** + **Domoticz 2025.2**  
✅ **Minimálna inštalácia** - len jeden balík (`python3-gpiod`)  
✅ **Active LOW logika** správne implementovaná pre Waveshare dosky  

---

## ✨ Funkcie

- ✅ Ovládanie **8 relé kanálov** cez GPIO
- ✅ Použitie modernej **libgpiod** knižnice
- ✅ **Active LOW** logika (správne pre Waveshare Relay Board)
- ✅ Automatické vytvorenie 8 switch zariadení v Domoticz
- ✅ Bezpečné vypnutie všetkých relé pri zastavení pluginu
- ✅ **Minimálna inštalácia** - len jeden APT balík
- ✅ Kompletná slovenská dokumentácia

---

## 📋 Požiadavky

| Komponent | Verzia |
|-----------|--------|
| **Raspberry Pi** | 3/4/5 (testované) |
| **OS** | Debian 13 (Trixie) / Raspberry Pi OS |
| **Domoticz** | 2025.2 alebo novší |
| **Python** | 3.x (už v systéme) |
| **Hardware** | Waveshare RPi Relay Board (B) |

---

## 🔌 GPIO Mapping

| Relé    | BCM GPIO | Fyzický Pin | Logika |
|---------|----------|-------------|--------|
| Relay 1 | GPIO 5   | Pin 29      | Active LOW |
| Relay 2 | GPIO 6   | Pin 31      | Active LOW |
| Relay 3 | GPIO 13  | Pin 33      | Active LOW |
| Relay 4 | GPIO 16  | Pin 36      | Active LOW |
| Relay 5 | GPIO 19  | Pin 35      | Active LOW |
| Relay 6 | GPIO 20  | Pin 38      | Active LOW |
| Relay 7 | GPIO 21  | Pin 40      | Active LOW |
| Relay 8 | GPIO 26  | Pin 37      | Active LOW |

**Active LOW znamená:**
- GPIO **LOW (0)** = Relé **ZAP** ✅
- GPIO **HIGH (1)** = Relé **VYP** ❌

---

## 📥 Inštalácia

### Metóda 1: Automatická inštalácia (odporúčané)

```bash
# 1. Stiahni repozitár
git clone https://github.com/Mibeus/Domoticz-GPIO-Debian-13.git
cd Domoticz-GPIO-Debian-13

# 2. Spusti inštalačný skript
chmod +x install.sh
sudo ./install.sh

# 3. Reštartuj Domoticz
sudo systemctl restart domoticz
```

### Metóda 2: Manuálna inštalácia

```bash
# 1. Nainštaluj python3-gpiod
sudo apt update
sudo apt install -y python3-gpiod

# 2. Vytvor plugin adresár
sudo mkdir -p /home/pi/domoticz/plugins/WaveshareRelayGPIOD

# 3. Skopíruj plugin
sudo cp plugin.py /home/pi/domoticz/plugins/WaveshareRelayGPIOD/

# 4. Nastav práva
sudo chown -R pi:pi /home/pi/domoticz/plugins/WaveshareRelayGPIOD
sudo chmod +x /home/pi/domoticz/plugins/WaveshareRelayGPIOD/plugin.py

# 5. Reštartuj Domoticz
sudo systemctl restart domoticz
```

---

## ⚙️ Konfigurácia v Domoticz

1. Otvor Domoticz web rozhranie: `http://[IP_ADRESA]:8080`
2. Choď do **Setup → Hardware**
3. Pridaj nový hardvér:
   - **Name:** `Relay Board` (alebo čokoľvek chceš)
   - **Type:** `Waveshare Relay Board (gpiod)`
   - **GPIO Chip:** `gpiochip0` (default)
4. Klikni **Add**
5. Plugin automaticky vytvorí 8 switch zariadení (`Relay 1-8`)
6. Zariadenia nájdeš v sekcii **Switches**

---

## 🧪 Testovanie GPIO

Pred inštaláciou pluginu môžeš otestovať či GPIO funguje:

```bash
# Spusti test skript
sudo python3 test_relay.py
```

Test skript:
- ✅ Otestuje všetky GPIO piny
- ✅ Postupne zapne/vypne každé relé
- ✅ Overí že relé fyzicky prepínajú
- ✅ Nepoškodí žiadne nastavenia

---

## 🎮 Použitie

Po pridaní hardvéru máš k dispozícii **8 prepínačov**:
- **Relay 1** až **Relay 8**

Každý prepínač má dva stavy:
- **ON** 🟢 = Relé zapnuté (GPIO LOW)
- **OFF** ⚫ = Relé vypnuté (GPIO HIGH)

Ovládanie:
- 🌐 Cez web rozhranie
- 📱 Cez mobilnú aplikáciu
- 🎬 Cez scény a scripty
- 🔌 Cez Domoticz API
- 🏠 Cez integrácie (Home Assistant, MQTT, atď.)

---

## 🐛 Riešenie problémov

### Plugin sa nezobrazuje v Domoticz

```bash
# Skontroluj Domoticz log
tail -f /tmp/domoticz.log

# Skontroluj či je plugin správne nainštalovaný
ls -la /home/pi/domoticz/plugins/WaveshareRelayGPIOD/

# Reštartuj Domoticz
sudo systemctl restart domoticz
```

### Relé nereagujú

```bash
# Skontroluj či python3-gpiod je nainštalované
dpkg -l | grep gpiod

# Skontroluj oprávnenia GPIO
ls -la /dev/gpiochip*

# Otestuj GPIO manuálne
sudo gpioinfo gpiochip0 | grep -E "(5|6|13|16|19|20|21|26)"
```

### Chyba "Permission denied" na GPIO

```bash
# Pridaj Domoticz používateľa do gpio skupiny
sudo usermod -a -G gpio pi

# Reštartuj systém
sudo reboot
```

### GPIO sú už použité

```bash
# Zisti ktorý proces používa GPIO
sudo lsof | grep gpiochip

# Uvoľni GPIO (nastav všetky na HIGH = vypnuté)
sudo gpioset gpiochip0 5=1 6=1 13=1 16=1 19=1 20=1 21=1 26=1
```

---

## 🔧 Pokročilé nastavenia

### Testovanie GPIO bez Domoticz

```bash
# Nainštaluj gpio tools
sudo apt install gpiod

# Zisti informácie o GPIO
gpioinfo gpiochip0

# Nastav GPIO 5 na LOW (relé ZAP)
gpioset gpiochip0 5=0

# Nastav GPIO 5 na HIGH (relé VYP)
gpioset gpiochip0 5=1

# Otestuj všetky relé naraz
gpioset gpiochip0 5=0 6=0 13=0 16=0 19=0 20=0 21=0 26=0  # Všetky ZAP
gpioset gpiochip0 5=1 6=1 13=1 16=1 19=1 20=1 21=1 26=1  # Všetky VYP
```

### Zmena GPIO Chip

V nastaveniach hardvéru môžeš zmeniť `GPIO Chip` parameter:
- `gpiochip0` - hlavný GPIO chip (default)
- `gpiochip1` - dodatočný GPIO expandér
- atď.

---

## 📚 Technické detaily

### Prečo gpiod namiesto WiringPi?

| Vlastnosť | WiringPi | libgpiod |
|-----------|----------|----------|
| **Podpora** | ❌ Deprecated 2019 | ✅ Aktívne udržiavaná |
| **Sysfs** | ❌ Deprecated kernel 4.8 | ✅ Moderné character device |
| **Debian 13** | ❌ Nefunguje | ✅ Plná podpora |
| **Dokumentácia** | ❌ Zastaralá | ✅ Aktuálna |

### Active LOW logika

Waveshare Relay Board používa **optočleny** s Active LOW logikou:

```
GPIO HIGH (1) → optočlen nevedie → relé VYP
GPIO LOW (0)  → optočlen vedie   → relé ZAP
```

Plugin **automaticky invertuje** logiku:
```
Domoticz ON  → GPIO LOW  → Relé ZAP ✅
Domoticz OFF → GPIO HIGH → Relé VYP ✅
```

---

## 📖 Referencie a linky

- 📘 [Waveshare RPi Relay Board (B) Wiki](https://www.waveshare.com/wiki/RPi_Relay_Board_(B))
- 📗 [libgpiod Documentation](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/about/)
- 📙 [Domoticz Python Plugin API](https://www.domoticz.com/wiki/Developing_a_Python_plugin)
- 📕 [Linux GPIO Character Device](https://www.kernel.org/doc/html/latest/driver-api/gpio/using-gpio.html)

---

## 🤝 Prispievanie

Príspevky sú vítané! Ak máš nápad na zlepšenie:

1. Fork repozitára
2. Vytvor feature branch (`git checkout -b feature/AmazingFeature`)
3. Commitni zmeny (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otvor Pull Request

---

## 📝 Licencia

Tento projekt je licencovaný pod **MIT License** - pozri [LICENSE](LICENSE) súbor pre detaily.

Znamená to že môžeš:
- ✅ Komerčne používať
- ✅ Modifikovať
- ✅ Distribuovať
- ✅ Súkromne používať

---

## 👨‍💻 Autor

Plugin vytvorený pre komunitu používateľov Domoticz, ktorí potrebujú riešenie pre GPIO na Debian 13.

---

## 🆘 Podpora

Pri problémoch:
1. Skontroluj `/tmp/domoticz.log`
2. Otestuj GPIO manuálne pomocou `gpioset`
3. Skontroluj `dmesg` pre kernel chyby
4. Over správnosť zapojenia podľa Waveshare wiki
5. Otvor [Issue](../../issues) na GitHube

---

## 🎉 Ďakujeme

Tento plugin vznikol z potreby komunity prevádzkovať existujúce hardvérové riešenia na moderných systémoch. Ďakujeme všetkým, ktorí prispeli nápadmi a testovaním!

---

**Verzia:** 1.0.0  
**Posledná aktualizácia:** Október 2025  
**Stav:** Stabilný a pripravený na produkčné použitie
