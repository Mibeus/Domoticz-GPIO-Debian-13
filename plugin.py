"""
<plugin key="DomoticzRPIGPIO" name="Domoticz RPI GPIO" author="Mibeus" version="2.0.1">
    <description>
        <h2>Domoticz RPI GPIO - Universal GPIO Control</h2><br/>
        <h3>Features</h3>
        <ul>
            <li>Configurable GPIO pins via gpio_config.json</li>
            <li>Active LOW / Active HIGH support</li>
            <li>Custom relay names</li>
            <li>Auto-reload configuration on Domoticz restart</li>
            <li>Supports gpiod v1.x and v2.x</li>
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
    gpiod_version = 1  # Default to v1
    gpiod_module = None
    line_request = None  # For gpiod v2
    
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
        
        # Import gpiod and detect version
        try:
            import gpiod
            self.gpiod_module = gpiod
            
            # Detect gpiod version
            if hasattr(gpiod, '__version__'):
                version_str = gpiod.__version__
                Domoticz.Log(f"Detected gpiod version: {version_str}")
                major_version = int(version_str.split('.')[0])
                self.gpiod_version = major_version
            else:
                # Old version without __version__ attribute
                self.gpiod_version = 1
                Domoticz.Log("Detected gpiod version: 1.x (legacy)")
                
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
        Domoticz.Log(f"  Using gpiod API version: {self.gpiod_version}")
        
        try:
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
            
            # Initialize GPIO based on version
            if self.gpiod_version >= 2:
                self.init_gpio_v2(gpio_chip_name, gpio_pins, relay_logic)
            else:
                self.init_gpio_v1(gpio_chip_name, gpio_pins, relay_logic)
            
            self.enabled = True
            Domoticz.Log("Plugin started successfully")
            Domoticz.Log(f"Active relay logic: {relay_logic}")
            
        except Exception as e:
            Domoticz.Error(f"Failed to initialize GPIO: {str(e)}")
            import traceback
            Domoticz.Error(f"Traceback: {traceback.format_exc()}")
            self.enabled = False
    
    def init_gpio_v1(self, gpio_chip_name, gpio_pins, relay_logic):
        """Initialize GPIO using gpiod v1.x API"""
        Domoticz.Log("Initializing GPIO with v1.x API")
        
        # Open GPIO chip - use full path
        gpio_chip_path = f"/dev/{gpio_chip_name}"
        self.chip = self.gpiod_module.Chip(gpio_chip_path)
        Domoticz.Log(f"Opened GPIO chip: {gpio_chip_path}")
        
        # Determine initial GPIO state based on relay logic
        initial_state = 1 if relay_logic == "active_low" else 0
        
        # Request GPIO lines as outputs
        for idx, gpio_pin in enumerate(gpio_pins):
            unit_num = idx + 1
            try:
                line = self.chip.get_line(gpio_pin)
                line.request(
                    consumer="domoticz-gpio",
                    type=self.gpiod_module.LINE_REQ_DIR_OUT,
                    default_vals=[initial_state]
                )
                self.lines[unit_num] = {
                    'line': line,
                    'gpio_pin': gpio_pin
                }
                Domoticz.Log(f"Configured GPIO {gpio_pin} (Unit {unit_num}) as output, initial state: {initial_state}")
            except Exception as e:
                Domoticz.Error(f"Failed to configure GPIO {gpio_pin} (Unit {unit_num}): {str(e)}")
    
    def init_gpio_v2(self, gpio_chip_name, gpio_pins, relay_logic):
        """Initialize GPIO using gpiod v2.x API"""
        Domoticz.Log("Initializing GPIO with v2.x API")
        
        gpio_chip_path = f"/dev/{gpio_chip_name}"
        
        # Determine initial GPIO state based on relay logic
        from gpiod.line import Direction, Value
        initial_value = Value.INACTIVE if relay_logic == "active_low" else Value.ACTIVE
        
        # Create line settings for all pins
        line_settings = {}
        for gpio_pin in gpio_pins:
            line_settings[gpio_pin] = self.gpiod_module.LineSettings(
                direction=Direction.OUTPUT,
                output_value=initial_value
            )
        
        # Request all lines at once
        try:
            self.line_request = self.gpiod_module.request_lines(
                gpio_chip_path,
                consumer="domoticz-gpio",
                config=line_settings
            )
            
            # Store line info for each unit
            for idx, gpio_pin in enumerate(gpio_pins):
                unit_num = idx + 1
                self.lines[unit_num] = {
                    'gpio_pin': gpio_pin
                }
                Domoticz.Log(f"Configured GPIO {gpio_pin} (Unit {unit_num}) as output")
                
        except Exception as e:
            Domoticz.Error(f"Failed to configure GPIO lines: {str(e)}")
            raise
    
    def onStop(self):
        Domoticz.Log("Domoticz RPI GPIO plugin stopping")
        
        # Get relay logic from config
        relay_logic = self.config.get("relay_logic", "active_low")
        
        if self.gpiod_version >= 2:
            self.stop_gpio_v2(relay_logic)
        else:
            self.stop_gpio_v1(relay_logic)
        
        Domoticz.Log("Plugin stopped")
    
    def stop_gpio_v1(self, relay_logic):
        """Stop GPIO using v1.x API"""
        off_state = 1 if relay_logic == "active_low" else 0
        
        # Release all GPIO lines and turn off relays
        for unit_num, line_info in self.lines.items():
            try:
                line = line_info['line']
                gpio_pin = line_info['gpio_pin']
                line.set_value(off_state)
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
    
    def stop_gpio_v2(self, relay_logic):
        """Stop GPIO using v2.x API"""
        from gpiod.line import Value
        off_value = Value.INACTIVE if relay_logic == "active_low" else Value.ACTIVE
        
        # Turn off all relays
        if self.line_request:
            try:
                for unit_num, line_info in self.lines.items():
                    gpio_pin = line_info['gpio_pin']
                    self.line_request.set_value(gpio_pin, off_value)
                    Domoticz.Log(f"Turned off GPIO {gpio_pin} (Unit {unit_num})")
                
                # Release request
                self.line_request.release()
                Domoticz.Log("Released GPIO lines")
            except Exception as e:
                Domoticz.Error(f"Error releasing GPIO: {str(e)}")
    
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
            gpio_pin = line_info['gpio_pin']
            relay_logic = self.config.get("relay_logic", "active_low")
            
            if self.gpiod_version >= 2:
                self.set_gpio_v2(Unit, gpio_pin, Command, relay_logic)
            else:
                self.set_gpio_v1(Unit, gpio_pin, Command, relay_logic)
            
        except Exception as e:
            Domoticz.Error(f"Error controlling Unit {Unit}: {str(e)}")
    
    def set_gpio_v1(self, unit_num, gpio_pin, command, relay_logic):
        """Set GPIO using v1.x API"""
        line = self.lines[unit_num]['line']
        
        # Determine GPIO value based on relay logic and command
        if relay_logic == "active_low":
            gpio_value = 0 if command == "On" else 1
        else:
            gpio_value = 1 if command == "On" else 0
        
        # Set GPIO value
        line.set_value(gpio_value)
        
        # Update device status
        if command == "On":
            Devices[unit_num].Update(nValue=1, sValue="On")
            Domoticz.Log(f"Unit {unit_num} (GPIO {gpio_pin}) turned ON (GPIO={gpio_value})")
        elif command == "Off":
            Devices[unit_num].Update(nValue=0, sValue="Off")
            Domoticz.Log(f"Unit {unit_num} (GPIO {gpio_pin}) turned OFF (GPIO={gpio_value})")
    
    def set_gpio_v2(self, unit_num, gpio_pin, command, relay_logic):
        """Set GPIO using v2.x API"""
        from gpiod.line import Value
        
        # Determine GPIO value based on relay logic and command
        if relay_logic == "active_low":
            gpio_value = Value.ACTIVE if command == "On" else Value.INACTIVE
        else:
            gpio_value = Value.INACTIVE if command == "On" else Value.ACTIVE
        
        # Set GPIO value
        self.line_request.set_value(gpio_pin, gpio_value)
        
        # Update device status
        if command == "On":
            Devices[unit_num].Update(nValue=1, sValue="On")
            Domoticz.Log(f"Unit {unit_num} (GPIO {gpio_pin}) turned ON (GPIO={gpio_value})")
        elif command == "Off":
            Devices[unit_num].Update(nValue=0, sValue="Off")
            Domoticz.Log(f"Unit {unit_num} (GPIO {gpio_pin}) turned OFF (GPIO={gpio_value})")
    
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
