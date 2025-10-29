# 🚀 Quick Start - Domoticz RPI GPIO v2.0.0

## Installation (3 simple steps)

```bash
# Step 1: Install dependency
sudo apt install python3-libgpiod -y

# Step 2: Install plugin
cd domoticz/plugins
git clone https://github.com/Mibeus/Domoticz-GPIO-Debian-13.git DomoticzRPIGPIO

# Step 3: Restart Domoticz
sudo systemctl restart domoticz
```

## Configuration

```bash
# Edit GPIO configuration
nano domoticz/plugins/DomoticzRPIGPIO/gpio_config.json
```

**Default config (Waveshare 8-channel relay board):**
```json
{
  "gpio_pins": [5, 6, 13, 16, 19, 20, 21, 26],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip0",
  "relay_names": ["Relay 1", "Relay 2", "Relay 3", "Relay 4", "Relay 5", "Relay 6", "Relay 7", "Relay 8"]
}
```

**After editing, restart:**
```bash
sudo systemctl restart domoticz
```

## Add in Domoticz

1. Open: `http://[IP]:8080`
2. Setup → Hardware → Add
3. Type: **Domoticz RPI GPIO**
4. Click Add
5. Find devices in Switches

## Test GPIO

```bash
sudo apt install gpiod -y
sudo gpioset gpiochip0 5=0  # Relay 1 ON (active_low)
sudo gpioset gpiochip0 5=1  # Relay 1 OFF
```

## Troubleshooting

```bash
# Check log
tail -f /tmp/domoticz.log | grep GPIO

# Verify config
cd domoticz/plugins/DomoticzRPIGPIO
python3 -c "import json; print(json.load(open('gpio_config.json')))"

# Check gpiod installed
python3 -c "import gpiod; print('OK')"
```

---

**Full docs:** [README.md](README.md)  
**Detailed install:** [INSTALLATION.md](INSTALLATION.md)  
**Changelog:** [CHANGELOG.md](CHANGELOG.md)
