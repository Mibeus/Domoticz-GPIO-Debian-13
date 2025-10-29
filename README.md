# Domoticz RPI GPIO Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Domoticz](https://img.shields.io/badge/Domoticz-2025.2+-green.svg)](https://www.domoticz.com/)
[![Debian](https://img.shields.io/badge/Debian-13%20Trixie-red.svg)](https://www.debian.org/)

Universal GPIO control plugin for Domoticz on Raspberry Pi. Control relay boards, LEDs, and other GPIO devices with configurable pins and logic levels.

---

## ✨ Features

- ✅ **Configurable GPIO pins** via JSON file
- ✅ **Active LOW / Active HIGH** support
- ✅ **Custom relay names**
- ✅ **Auto-detection** of Domoticz plugin directory
- ✅ **No hardcoded paths** - works with any Domoticz installation
- ✅ **Modern libgpiod** library (replaces deprecated WiringPi)
- ✅ **Easy configuration** via text editor (nano)
- ✅ **Support for multiple relay boards**

---

## 📋 Requirements

| Component | Version |
|-----------|---------|
| **Raspberry Pi** | 3/4/5 |
| **OS** | Debian 13 (Trixie) or Raspberry Pi OS |
| **Domoticz** | 2025.2+ |
| **Python** | 3.x (included in OS) |
| **python3-libgpiod** | Required |

---

## 📥 Installation

### Step 1: Install dependencies

```bash
# Install python3-libgpiod
sudo apt update
sudo apt install python3-libgpiod -y

# Alternative: Install via pip if apt package not available
sudo pip3 install gpiod --break-system-packages
```

### Step 2: Install plugin

```bash
# Navigate to Domoticz plugins directory
cd domoticz/plugins

# Clone the repository
git clone https://github.com/Mibeus/Domoticz-GPIO-Debian-13.git DomoticzRPIGPIO

# Restart Domoticz
sudo systemctl restart domoticz
```

---

## ⚙️ Configuration

### Edit Configuration File

The plugin reads its configuration from `gpio_config.json`. Edit this file to customize GPIO pins, relay logic, and names.

```bash
# Navigate to plugin directory
cd domoticz/plugins/DomoticzRPIGPIO

# Edit configuration
nano gpio_config.json
```

### Configuration File Format

```json
{
  "gpio_pins": [5, 6, 13, 16, 19, 20, 21, 26],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "Relay 1",
    "Relay 2",
    "Relay 3",
    "Relay 4",
    "Relay 5",
    "Relay 6",
    "Relay 7",
    "Relay 8"
  ]
}
```

### Configuration Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| **gpio_pins** | Array | List of BCM GPIO pin numbers to use | Required |
| **relay_logic** | String | `"active_low"` or `"active_high"` | `"active_low"` |
| **gpio_chip** | String | GPIO chip device name | `"gpiochip0"` |
| **relay_names** | Array | Custom names for each relay | `["Relay 1", ...]` |

### Relay Logic

- **active_low** (default): 
  - GPIO LOW (0) = Relay ON
  - GPIO HIGH (1) = Relay OFF
  - Used by most relay boards (Waveshare, SainSmart, etc.)

- **active_high**:
  - GPIO HIGH (1) = Relay ON
  - GPIO LOW (0) = Relay OFF
  - Used by some solid-state relays and LED boards

### After Configuration Changes

```bash
# Restart Domoticz to apply changes
sudo systemctl restart domoticz
```

---

## 🎮 Usage in Domoticz

### Add Hardware

1. Open Domoticz web interface: `http://[IP_ADDRESS]:8080`
2. Go to **Setup → Hardware**
3. Add new hardware:
   - **Name:** `GPIO Control` (or any name you want)
   - **Type:** `Domoticz RPI GPIO`
4. Click **Add**

### Devices

The plugin automatically creates switch devices based on your configuration:
- Number of switches = number of GPIO pins configured
- Switch names come from `relay_names` in config file

Find devices in **Switches** section.

---

## 🔌 GPIO Pin Reference

### Common GPIO Pins (BCM Numbering)

| BCM GPIO | Physical Pin | Waveshare Relay Board |
|----------|--------------|----------------------|
| GPIO 5   | Pin 29       | Relay 1              |
| GPIO 6   | Pin 31       | Relay 2              |
| GPIO 13  | Pin 33       | Relay 3              |
| GPIO 16  | Pin 36       | Relay 4              |
| GPIO 19  | Pin 35       | Relay 5              |
| GPIO 20  | Pin 38       | Relay 6              |
| GPIO 21  | Pin 40       | Relay 7              |
| GPIO 26  | Pin 37       | Relay 8              |

**⚠️ Important:** Use BCM GPIO numbers in configuration, not physical pin numbers!

### Check Available GPIO Pins

```bash
# List GPIO chips
ls -la /dev/gpiochip*

# Show GPIO information
gpioinfo gpiochip0
```

---

## 📝 Configuration Examples

### Example 1: Waveshare 8-Channel Relay Board

```json
{
  "gpio_pins": [5, 6, 13, 16, 19, 20, 21, 26],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "Light Living Room",
    "Light Kitchen",
    "Light Bedroom",
    "Light Bathroom",
    "Fan",
    "Pump",
    "Heater",
    "Door Lock"
  ]
}
```

### Example 2: 4-Channel Relay Board

```json
{
  "gpio_pins": [17, 27, 22, 23],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "Relay 1",
    "Relay 2",
    "Relay 3",
    "Relay 4"
  ]
}
```

### Example 3: LED Strip (Active High)

```json
{
  "gpio_pins": [18, 23, 24, 25],
  "relay_logic": "active_high",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "LED Red",
    "LED Green",
    "LED Blue",
    "LED White"
  ]
}
```

### Example 4: Using Different GPIO Chip

```json
{
  "gpio_pins": [0, 1, 2, 3],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip1",
  "relay_names": [
    "Expander 1",
    "Expander 2",
    "Expander 3",
    "Expander 4"
  ]
}
```

---

## 🐛 Troubleshooting

### Plugin doesn't appear in Hardware list

```bash
# Check Domoticz log
tail -f /tmp/domoticz.log

# Check if plugin directory exists
ls -la domoticz/plugins/DomoticzRPIGPIO/

# Check if files are present
ls -la domoticz/plugins/DomoticzRPIGPIO/
# Should see: plugin.py and gpio_config.json

# Restart Domoticz
sudo systemctl restart domoticz
```

### Relays don't respond

```bash
# Check if python3-libgpiod is installed
dpkg -l | grep libgpiod

# Check GPIO permissions
ls -la /dev/gpiochip*

# Test GPIO manually
sudo gpioset gpiochip0 5=0  # Turn on (if active_low)
sudo gpioset gpiochip0 5=1  # Turn off (if active_low)
```

### Configuration errors

```bash
# Check JSON syntax
cat domoticz/plugins/DomoticzRPIGPIO/gpio_config.json | python3 -m json.tool

# View Domoticz log for specific errors
tail -f /tmp/domoticz.log | grep GPIO
```

### Permission denied on GPIO

```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Or for domoticz user
sudo usermod -a -G gpio domoticz

# Reboot
sudo reboot
```

### GPIO already in use

```bash
# Find what's using GPIO
sudo lsof | grep gpiochip

# Release all GPIO pins (set to OFF state)
# For active_low relays:
sudo gpioset gpiochip0 5=1 6=1 13=1 16=1 19=1 20=1 21=1 26=1
```

---

## 🧪 Testing

### Test GPIO without Domoticz

```bash
# Install GPIO tools
sudo apt install gpiod

# Get GPIO chip info
gpioinfo gpiochip0

# Test relay 1 (GPIO 5)
sudo gpioset gpiochip0 5=0  # Relay ON (active_low)
sleep 2
sudo gpioset gpiochip0 5=1  # Relay OFF

# Test all relays at once
sudo gpioset gpiochip0 5=0 6=0 13=0 16=0 19=0 20=0 21=0 26=0  # All ON
sleep 2
sudo gpioset gpiochip0 5=1 6=1 13=1 16=1 19=1 20=1 21=1 26=1  # All OFF
```

### Verify Configuration

```bash
# Check JSON is valid
cd domoticz/plugins/DomoticzRPIGPIO
python3 -c "import json; print(json.load(open('gpio_config.json')))"
```

---

## 🔄 Updating the Plugin

```bash
# Navigate to plugin directory
cd domoticz/plugins/DomoticzRPIGPIO

# Pull latest changes
git pull

# Restart Domoticz
sudo systemctl restart domoticz
```

**⚠️ Note:** Your `gpio_config.json` will not be overwritten during update.

---

## 🎯 Use Cases

- **Home Automation:** Control lights, fans, heaters
- **Garden Automation:** Irrigation pumps, valves
- **Aquarium Control:** Lights, pumps, heaters
- **Industrial Control:** Relays, valves, motors
- **Security Systems:** Door locks, sirens
- **Custom Projects:** Any GPIO-controlled device

---

## 📚 Technical Details

### Why libgpiod?

| Library | Status | Debian 13 |
|---------|--------|-----------|
| **WiringPi** | ❌ Deprecated 2019 | Not available |
| **sysfs GPIO** | ❌ Deprecated kernel 4.8 | Not available |
| **libgpiod** | ✅ Active development | ✅ Fully supported |

### GPIO Character Device

Modern Linux kernels use character devices (`/dev/gpiochipX`) instead of sysfs. This provides:
- Better performance
- More reliable access
- Proper permission management
- Modern API

---

## 🔗 Links & Resources

- 📘 [libgpiod Documentation](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/about/)
- 📗 [Domoticz Python Plugin API](https://www.domoticz.com/wiki/Developing_a_Python_plugin)
- 📙 [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- 📕 [Linux GPIO Character Device](https://www.kernel.org/doc/html/latest/driver-api/gpio/using-gpio.html)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

You can:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/Mibeus/Domoticz-GPIO-Debian-13/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Mibeus/Domoticz-GPIO-Debian-13/discussions)
- **Domoticz Forum:** [Domoticz.com Forum](https://www.domoticz.com/forum/)

---

## 📊 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

---

**Author:** [@Mibeus](https://github.com/Mibeus)  
**Repository:** [Domoticz-GPIO-Debian-13](https://github.com/Mibeus/Domoticz-GPIO-Debian-13)  
**Version:** 2.0.0  
**Status:** Production ready  
**Tested on:** Raspberry Pi 4, Debian 13 Trixie, Domoticz 2025.2
