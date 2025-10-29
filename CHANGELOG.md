# Changelog

Všetky významné zmeny v tomto projekte budú zdokumentované v tomto súbore.

Formát je založený na [Keep a Changelog](https://keepachangelog.com/sk/1.0.0/),
a tento projekt dodržiava [Semantic Versioning](https://semver.org/lang/sk/).

## [1.0.0] - 2025-10-29

### Pridané
- Prvé vydanie pluginu
- Podpora pre Waveshare RPi Relay Board (B)
- Ovládanie 8 GPIO relé cez libgpiod
- Active LOW logika pre správne ovládanie relé
- Automatický inštalačný skript (`install.sh`)
- Test skript pre overenie GPIO funkčnosti (`test_relay.py`)
- Kompletná slovenská dokumentácia
- Podpora pre Debian 13 (Trixie)
- Podpora pre Domoticz 2025.2+
- MIT Licencia

### Technické detaily
- Použitie modernej `libgpiod` knižnice namiesto deprecated WiringPi
- Python 3 implementácia
- GPIO mapping: 5, 6, 13, 16, 19, 20, 21, 26
- Bezpečné vypnutie všetkých relé pri zastavení pluginu
- Automatická inicializácia GPIO pinov na HIGH (relé vypnuté)

### Dokumentácia
- README.md s kompletným návodom na inštaláciu
- Riešenie problémov (troubleshooting)
- Príklady použitia
- GPIO mapping tabuľka
- Technické vysvetlenia Active LOW logiky

---

## Plánované pre budúce verzie

### [1.1.0] - Plánované
- [ ] Podpora pre viacero Waveshare dosiek na jednom RPi
- [ ] Konfigurovateľné GPIO piny cez web rozhranie
- [ ] Podpora pre čítanie stavu GPIO pinov
- [ ] Podpora pre pulsné režimy

### [1.2.0] - Plánované
- [ ] Pridanie tlakom ovládaných režimov (momentary switch)
- [ ] Časovače pre automatické vypnutie
- [ ] Podpora pre iné typy relé dosiek

---

## Formát zmien

- **Pridané** - pre nové funkcie
- **Zmenené** - pre zmeny v existujúcich funkciách
- **Deprecated** - pre funkcie, ktoré budú čoskoro odstránené
- **Odstránené** - pre odstránené funkcie
- **Opravené** - pre opravy chýb
- **Bezpečnosť** - pre bezpečnostné opravy
