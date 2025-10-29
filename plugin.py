"""
<plugin key="DomoticzRPIGPIO" name="Domoticz RPI GPIO" author="Mibeus" version="2.0.0">
    <description>
        <h2>Domoticz RPI GPIO - Universal GPIO Control</h2><br/>
        <h3>Features</h3>
        <ul>
            <li>Configurable GPIO pins via gpio_config.json</li>
            <li>Active LOW / Active HIGH support</li>
            <li>Custom relay names</li>
            <li>Auto-reload configuration on Domoticz restart</li>
        </ul>
        <h3>Configuration</h3>
        Edit gpio_config.json in the plugin directory:<br/>
        <code>nano domoticz/plugins/DomoticzRPIGPIO/gpio_config.json</code><br/>
        <br/>
        Then restart Domoticz:<br/>
        <code>sudo systemctl restart domoticz</code><br/>
        <br/>
        <h3>GPIO Pins</h3>
        Configure your GPIO pins in gpio_config.json<br/>
        <br/>
        <h3>Relay Logic</h3>
        - active_low: GPIO LOW = Relay ON (default for most relay boards)<br/>
        - active_high: GPIO HIGH = Relay ON<br/>
    </description>
    <params>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import json
import os

class BasePlugin:
    enabled = False
    chip = None
    lines = {}
    config = {}
    plugin_path = ""
    
    def __init__(self):
        return
    
    def onStart(self):
        Domoticz.Log("Domoticz RPI GPIO plugin starting")
        
        # Get plugin directory path
        self.plugin_path = os.path.dirname(os.path.realpath(__file__))
        Domoticz.Log(f"Plugin path: {self.plugin_path}")
        
        # Load configuration from JSON file
        if not self.load_config():
            Domoticz.Error("Failed to load configuration. Plugin will not start.")
            self.enabled = False
            return
        
        # Import gpiod
        try:
            import gpiod
        except ImportError:
            Domoticz.Error("gpiod module not found! Install it with:")
            Domoticz.Error("  sudo apt install python3-libgpiod")
            Domoticz.Error("  or: sudo pip3 install gpiod --break-system-packages")
            self.enabled = False
            return
        
        # Get configuration values
        gpio_pins = self.config.get("gpio_pins", [])
        relay_logic = self.config.get("relay_logic", "active_low")
        gpio_chip_name = self.config.get("gpio_chip", "gpiochip0")
        relay_names = self.config.get("relay_names", [])
        
        # Validate configuration
        if not gpio_pins:
            Domoticz.Error("No GPIO pins configured in gpio_config.json")
            self.enabled = False
            return
        
        Domoticz.Log(f"Configuration loaded:")
        Domoticz.Log(f"  GPIO Chip: {gpio_chip_name}")
        Domoticz.Log(f"  GPIO Pins: {gpio_pins}")
        Domoticz.Log(f"  Relay Logic: {relay_logic}")
        Domoticz.Log(f"  Number of relays: {len(gpio_pins)}")
        
        try:
            # Open GPIO chip
            self.chip = gpiod.Chip(gpio_chip_name)
            Domoticz.Log(f"Opened GPIO chip: {gpio_chip_name}")
            
            # Create devices if they don't exist
            if len(Devices) == 0:
                Domoticz.Log("Creating relay devices...")
                for idx, gpio_pin in enumerate(gpio_pins):
                    unit_num = idx + 1
                    
                    # Get custom relay name or use default
                    if relay_names and idx < len(relay_names):
                        relay_name = relay_names[idx]
                    else:
                        relay_name = f"Relay {unit_num}"
                    
                    Domoticz.Device(
                        Name=relay_name,
                        Unit=unit_num,
                        TypeName="Switch",
                        Used=1
                    ).Create()
                    Domoticz.Log(f"Created device: {relay_name} (Unit {unit_num}, GPIO {gpio_pin})")
            
            # Determine initial GPIO state based on relay logic
            # For active_low: HIGH = OFF, for active_high: LOW = OFF
            initial_state = 1 if relay_logic == "active_low" else 0
            
            # Request GPIO lines as outputs with initial state (all relays OFF)
            for idx, gpio_pin in enumerate(gpio_pins):
                unit_num = idx + 1
                try:
                    line = self.chip.get_line(gpio_pin)
                    line.request(
                        consumer="domoticz-gpio",
                        type=gpiod.LINE_REQ_DIR_OUT,
                        default_vals=[initial_state]
                    )
                    self.lines[unit_num] = {
                        'line': line,
                        'gpio_pin': gpio_pin
                    }
                    Domoticz.Log(f"Configured GPIO {gpio_pin} (Unit {unit_num}) as output, initial state: {initial_state}")
                except Exception as e:
                    Domoticz.Error(f"Failed to configure GPIO {gpio_pin} (Unit {unit_num}): {str(e)}")
            
            self.enabled = True
            Domoticz.Log("Plugin started successfully")
            Domoticz.Log(f"Active relay logic: {relay_logic}")
            
        except Exception as e:
            Domoticz.Error(f"Failed to initialize GPIO: {str(e)}")
            self.enabled = False
    
    def onStop(self):
        Domoticz.Log("Domoticz RPI GPIO plugin stopping")
        
        # Get relay logic from config
        relay_logic = self.config.get("relay_logic", "active_low")
        off_state = 1 if relay_logic == "active_low" else 0
        
        # Release all GPIO lines and turn off relays
        for unit_num, line_info in self.lines.items():
            try:
                line = line_info['line']
                gpio_pin = line_info['gpio_pin']
                line.set_value(off_state)  # Turn relay OFF
                line.release()
                Domoticz.Log(f"Released GPIO {gpio_pin} (Unit {unit_num})")
            except Exception as e:
                Domoticz.Error(f"Error releasing GPIO for Unit {unit_num}: {str(e)}")
        
        # Close chip
        if self.chip:
            try:
                del self.chip
                Domoticz.Log("Closed GPIO chip")
            except Exception as e:
                Domoticz.Error(f"Error closing GPIO chip: {str(e)}")
        
        Domoticz.Log("Plugin stopped")
    
    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log(f"onCommand called for Unit {Unit}: Command={Command}, Level={Level}")
        
        if not self.enabled:
            Domoticz.Error("Plugin not properly initialized")
            return
        
        if Unit not in self.lines:
            Domoticz.Error(f"Invalid relay unit: {Unit}")
            return
        
        try:
            line_info = self.lines[Unit]
            line = line_info['line']
            gpio_pin = line_info['gpio_pin']
            
            # Get relay logic from config
            relay_logic = self.config.get("relay_logic", "active_low")
            
            # Determine GPIO value based on relay logic and command
            if relay_logic == "active_low":
                # Active LOW: ON = GPIO LOW (0), OFF = GPIO HIGH (1)
                gpio_value = 0 if Command == "On" else 1
            else:
                # Active HIGH: ON = GPIO HIGH (1), OFF = GPIO LOW (0)
                gpio_value = 1 if Command == "On" else 0
            
            # Set GPIO value
            line.set_value(gpio_value)
            
            # Update device status in Domoticz
            if Command == "On":
                Devices[Unit].Update(nValue=1, sValue="On")
                Domoticz.Log(f"Unit {Unit} (GPIO {gpio_pin}) turned ON (GPIO={gpio_value})")
            elif Command == "Off":
                Devices[Unit].Update(nValue=0, sValue="Off")
                Domoticz.Log(f"Unit {Unit} (GPIO {gpio_pin}) turned OFF (GPIO={gpio_value})")
            
        except Exception as e:
            Domoticz.Error(f"Error controlling Unit {Unit}: {str(e)}")
    
    def load_config(self):
        """Load configuration from gpio_config.json"""
        config_file = os.path.join(self.plugin_path, "gpio_config.json")
        
        Domoticz.Log(f"Loading configuration from: {config_file}")
        
        if not os.path.exists(config_file):
            Domoticz.Error(f"Configuration file not found: {config_file}")
            Domoticz.Error("Please create gpio_config.json in the plugin directory")
            Domoticz.Error("See README.md for example configuration")
            return False
        
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            
            # Validate required fields
            if "gpio_pins" not in self.config:
                Domoticz.Error("Missing 'gpio_pins' in configuration")
                return False
            
            if not isinstance(self.config["gpio_pins"], list):
                Domoticz.Error("'gpio_pins' must be a list")
                return False
            
            if len(self.config["gpio_pins"]) == 0:
                Domoticz.Error("'gpio_pins' list is empty")
                return False
            
            # Set defaults for optional fields
            if "relay_logic" not in self.config:
                self.config["relay_logic"] = "active_low"
                Domoticz.Log("Using default relay_logic: active_low")
            
            if "gpio_chip" not in self.config:
                self.config["gpio_chip"] = "gpiochip0"
                Domoticz.Log("Using default gpio_chip: gpiochip0")
            
            # Validate relay_logic value
            if self.config["relay_logic"] not in ["active_low", "active_high"]:
                Domoticz.Error(f"Invalid relay_logic: {self.config['relay_logic']}")
                Domoticz.Error("Must be 'active_low' or 'active_high'")
                return False
            
            Domoticz.Log("Configuration loaded successfully")
            return True
            
        except json.JSONDecodeError as e:
            Domoticz.Error(f"Invalid JSON in configuration file: {str(e)}")
            return False
        except Exception as e:
            Domoticz.Error(f"Error loading configuration: {str(e)}")
            return False

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)
