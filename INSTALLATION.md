# 🚀 Installation Guide - Domoticz RPI GPIO v2.0.0

Complete installation guide for universal GPIO control on Raspberry Pi with Domoticz.

---

## 📋 Prerequisites

### System Requirements
- Raspberry Pi 3, 4, or 5
- Debian 13 (Trixie) or Raspberry Pi OS
- Domoticz 2025.2 or newer
- Internet connection (for installation)

### Check Your System

```bash
# Check Debian version
cat /etc/os-release

# Check if Domoticz is running
sudo systemctl status domoticz

# Find Domoticz directory
ps aux | grep domoticz
```

---

## 📥 Step-by-Step Installation

### Step 1: Install Dependencies

```bash
# Update system
sudo apt update

# Install python3-libgpiod
sudo apt install python3-libgpiod -y
```

**If apt package not available** (on some systems):
```bash
sudo apt install python3-pip -y
sudo pip3 install gpiod --break-system-packages
```

**Verify installation:**
```bash
python3 -c "import gpiod; print('gpiod installed successfully')"
```

---

### Step 2: Install Plugin

```bash
# Navigate to Domoticz plugins directory
# IMPORTANT: Replace 'domoticz' with your actual path
cd domoticz/plugins

# Clone the repository
git clone https://github.com/Mibeus/Domoticz-GPIO-Debian-13.git DomoticzRPIGPIO

# Verify files
ls -la DomoticzRPIGPIO/
# Should see: plugin.py and gpio_config.json
```

**Common Domoticz paths:**
- `/opt/domoticz/plugins`
- `/home/pi/domoticz/plugins`
- `/usr/share/domoticz/plugins`

**Find your Domoticz path:**
```bash
ps aux | grep domoticz | grep -v grep | awk '{for(i=1;i<=NF;i++) if($i ~ /domoticz/) print $i}'
```

---

### Step 3: Configure GPIO Pins

```bash
# Navigate to plugin directory
cd domoticz/plugins/DomoticzRPIGPIO

# Edit configuration
nano gpio_config.json
```

**Default configuration (for Waveshare Relay Board):**
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

**Customize as needed:**
- Change `gpio_pins` to your BCM GPIO numbers
- Set `relay_logic` to `"active_low"` or `"active_high"`
- Customize `relay_names` to meaningful names

**Save and exit:** `CTRL+O`, `Enter`, `CTRL+X`

---

### Step 4: Restart Domoticz

```bash
# Restart Domoticz service
sudo systemctl restart domoticz

# Check if restarted successfully
sudo systemctl status domoticz

# Monitor log for plugin messages
tail -f /tmp/domoticz.log | grep GPIO
```

**Look for these messages in log:**
```
Domoticz RPI GPIO plugin starting
Plugin path: /path/to/plugins/DomoticzRPIGPIO
Configuration loaded successfully
GPIO Chip: gpiochip0
GPIO Pins: [5, 6, 13, 16, 19, 20, 21, 26]
Relay Logic: active_low
Created device: Relay 1 (Unit 1, GPIO 5)
...
Plugin started successfully
```

---

### Step 5: Add Hardware in Domoticz

1. **Open Domoticz web interface:**
   ```
   http://[YOUR_RPI_IP]:8080
   ```

2. **Go to Setup → Hardware**

3. **Click "Add" and configure:**
   - **Name:** `GPIO Control` (or any name)
   - **Type:** `Domoticz RPI GPIO`
   - **Debug:** `False` (set to `True` for troubleshooting)

4. **Click "Add"**

5. **Devices appear automatically** in **Switches** section

---

### Step 6: Test Relays

1. Go to **Switches** in Domoticz
2. Find your relay devices (Relay 1, Relay 2, etc.)
3. Click switch to turn ON
4. You should hear relay click on the board
5. Click again to turn OFF

**If relays don't respond, see Troubleshooting section below.**

---

## 🔧 Configuration Examples

### Example 1: Standard 8-Channel Waveshare Board

```json
{
  "gpio_pins": [5, 6, 13, 16, 19, 20, 21, 26],
  "relay_logic": "active_low",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "Light Living Room",
    "Light Kitchen",
    "Fan Bedroom",
    "Heater",
    "Pump",
    "Door Lock",
    "Garage Door",
    "Garden Light"
  ]
}
```

### Example 2: 4-Channel Board with Custom Pins

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

### Example 3: Active HIGH Logic (SSR or LEDs)

```json
{
  "gpio_pins": [18, 23, 24, 25],
  "relay_logic": "active_high",
  "gpio_chip": "gpiochip0",
  "relay_names": [
    "LED Strip Red",
    "LED Strip Green",
    "LED Strip Blue",
    "LED Strip White"
  ]
}
```

---

## 🐛 Troubleshooting

### Plugin doesn't appear in Hardware list

**Check plugin installation:**
```bash
cd domoticz/plugins
ls -la DomoticzRPIGPIO/
```

**Expected files:**
- `plugin.py`
- `gpio_config.json`
- `README.md`

**Check Domoticz log:**
```bash
tail -100 /tmp/domoticz.log | grep -i error
```

**Restart Domoticz:**
```bash
sudo systemctl restart domoticz
```

---

### "Unable to locate package python3-gpiod"

**Solution 1:** Use correct package name
```bash
sudo apt install python3-libgpiod -y
```

**Solution 2:** Install via pip
```bash
sudo pip3 install gpiod --break-system-packages
```

**Verify:**
```bash
python3 -c "import gpiod; print('OK')"
```

---

### Configuration file not found

**Error in log:**
```
Configuration file not found: /path/to/gpio_config.json
```

**Solution:**
```bash
cd domoticz/plugins/DomoticzRPIGPIO
ls -la gpio_config.json

# If missing, create it:
nano gpio_config.json
# Paste default configuration and save
```

---

### Invalid JSON in configuration

**Error in log:**
```
Invalid JSON in configuration file
```

**Validate JSON:**
```bash
cd domoticz/plugins/DomoticzRPIGPIO
python3 -c "import json; print(json.load(open('gpio_config.json')))"
```

**Common JSON errors:**
- Missing comma between array elements
- Extra comma at end of array
- Unquoted strings
- Wrong quotes (use `"` not `'`)

---

### Relays don't respond

**Test GPIO manually:**
```bash
# Install GPIO tools
sudo apt install gpiod -y

# Test GPIO 5 (Relay 1)
sudo gpioset gpiochip0 5=0   # ON for active_low
sleep 2
sudo gpioset gpiochip0 5=1   # OFF
```

**Check permissions:**
```bash
ls -la /dev/gpiochip*

# Add user to gpio group
sudo usermod -a -G gpio $USER
sudo reboot
```

**Check if GPIO already in use:**
```bash
sudo lsof | grep gpiochip
```

---

### Wrong relay logic (ON/OFF inverted)

**Solution:** Change `relay_logic` in configuration

```bash
nano domoticz/plugins/DomoticzRPIGPIO/gpio_config.json
```

Change:
```json
"relay_logic": "active_low"
```
to:
```json
"relay_logic": "active_high"
```

Save and restart Domoticz.

---

## 🔄 Updating Plugin

```bash
# Navigate to plugin directory
cd domoticz/plugins/DomoticzRPIGPIO

# Backup your configuration
cp gpio_config.json gpio_config.json.backup

# Pull latest changes
git pull

# Restore your configuration if overwritten
# (usually not needed as git doesn't overwrite local changes)

# Restart Domoticz
sudo systemctl restart domoticz
```

---

## 🗑️ Uninstallation

```bash
# Stop Domoticz
sudo systemctl stop domoticz

# Remove plugin directory
rm -rf domoticz/plugins/DomoticzRPIGPIO

# Start Domoticz
sudo systemctl start domoticz

# Remove hardware in Domoticz web interface
# Setup → Hardware → Delete "GPIO Control"
```

---

## 📊 GPIO Pin Reference

### Raspberry Pi 40-Pin GPIO Header

```
     3V3  (1) (2)  5V    
   GPIO2  (3) (4)  5V    
   GPIO3  (5) (6)  GND   
   GPIO4  (7) (8)  GPIO14
     GND  (9) (10) GPIO15
  GPIO17 (11) (12) GPIO18
  GPIO27 (13) (14) GND   
  GPIO22 (15) (16) GPIO23
     3V3 (17) (18) GPIO24
  GPIO10 (19) (20) GND   
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8 
     GND (25) (26) GPIO7 
   GPIO0 (27) (28) GPIO1 
   GPIO5 (29) (30) GND   
   GPIO6 (31) (32) GPIO12
  GPIO13 (33) (34) GND   
  GPIO19 (35) (36) GPIO16
  GPIO26 (37) (38) GPIO20
     GND (39) (40) GPIO21
```

**⚠️ Use BCM GPIO numbers in configuration, not physical pin numbers!**

---

## 🆘 Getting Help

**Check logs:**
```bash
tail -f /tmp/domoticz.log | grep GPIO
```

**Enable debug mode:**
In Domoticz Hardware settings, set Debug to `True`, then check log.

**Report issues:**
- GitHub Issues: https://github.com/Mibeus/Domoticz-GPIO-Debian-13/issues
- Include: OS version, Domoticz version, error messages from log

---

## ✅ Installation Checklist

- [ ] Debian 13 (Trixie) installed
- [ ] Domoticz 2025.2+ running
- [ ] python3-libgpiod installed
- [ ] Plugin cloned to `domoticz/plugins/DomoticzRPIGPIO`
- [ ] `gpio_config.json` configured with correct GPIO pins
- [ ] Domoticz restarted
- [ ] Hardware added in Domoticz
- [ ] Relays tested and working

---

**Installation complete!** 🎉

For more information, see [README.md](README.md)
