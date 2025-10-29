#!/bin/bash

# Inštalačný skript pre Waveshare Relay Board plugin pre Domoticz
# Autor: Custom
# Verzia: 1.0.0

echo "==================================================="
echo "Waveshare Relay Board Plugin - Inštalácia"
echo "==================================================="
echo ""

# Kontrola či sme root
if [ "$EUID" -ne 0 ]; then 
    echo "CHYBA: Tento skript musí byť spustený ako root (sudo)"
    exit 1
fi

# Inštalácia python3-gpiod
echo "[1/4] Inštalujem python3-gpiod..."
apt update
apt install -y python3-gpiod

if [ $? -ne 0 ]; then
    echo "CHYBA: Nepodarilo sa nainštalovať python3-gpiod"
    exit 1
fi

# Zistenie Domoticz adresára
DOMOTICZ_DIR=""
if [ -d "/home/pi/domoticz" ]; then
    DOMOTICZ_DIR="/home/pi/domoticz"
elif [ -d "/opt/domoticz" ]; then
    DOMOTICZ_DIR="/opt/domoticz"
else
    echo ""
    echo "Zadaj cestu k Domoticz adresáru (napr. /home/pi/domoticz):"
    read -r DOMOTICZ_DIR
    if [ ! -d "$DOMOTICZ_DIR" ]; then
        echo "CHYBA: Adresár $DOMOTICZ_DIR neexistuje"
        exit 1
    fi
fi

echo "[2/4] Používam Domoticz adresár: $DOMOTICZ_DIR"

# Vytvorenie plugin adresára
PLUGIN_DIR="$DOMOTICZ_DIR/plugins/WaveshareRelayGPIOD"
echo "[3/4] Vytváram plugin adresár: $PLUGIN_DIR"
mkdir -p "$PLUGIN_DIR"

# Kopírovanie plugin súboru
echo "[4/4] Kopírujem plugin.py..."
cp plugin.py "$PLUGIN_DIR/plugin.py"
chmod +x "$PLUGIN_DIR/plugin.py"

# Nastavenie správnych práv
DOMOTICZ_USER=$(stat -c '%U' "$DOMOTICZ_DIR")
chown -R $DOMOTICZ_USER:$DOMOTICZ_USER "$PLUGIN_DIR"

echo ""
echo "==================================================="
echo "Inštalácia DOKONČENÁ!"
echo "==================================================="
echo ""
echo "ĎALŠIE KROKY:"
echo "1. Reštartuj Domoticz: sudo systemctl restart domoticz"
echo "2. Otvor Domoticz web rozhranie"
echo "3. Choď do Setup -> Hardware"
echo "4. Pridaj nový hardvér:"
echo "   - Type: Waveshare Relay Board (gpiod)"
echo "   - Name: Relay Board (alebo čokoľvek chceš)"
echo "   - GPIO Chip: gpiochip0 (ponechaj default)"
echo "5. Klikni Add"
echo "6. Relé zariadenia (Relay 1-8) sa objavia v Switches"
echo ""
echo "GPIO mapping:"
echo "  Relay 1 -> GPIO 5"
echo "  Relay 2 -> GPIO 6"
echo "  Relay 3 -> GPIO 13"
echo "  Relay 4 -> GPIO 16"
echo "  Relay 5 -> GPIO 19"
echo "  Relay 6 -> GPIO 20"
echo "  Relay 7 -> GPIO 21"
echo "  Relay 8 -> GPIO 26"
echo ""
echo "POZNÁMKA: Relé sú ACTIVE LOW (ON = LOW signal)"
echo "==================================================="
