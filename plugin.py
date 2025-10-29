"""
<plugin key="WaveshareRelayGPIOD" name="Waveshare Relay Board (gpiod)" author="Custom" version="1.0.0">
    <description>
        <h2>Waveshare RPi Relay Board (B) - GPIO Control via gpiod</h2><br/>
        Controls 8 relay channels via GPIO pins using libgpiod<br/>
        <br/>
        GPIO Mapping (BCM):<br/>
        - Relay 1: GPIO 5<br/>
        - Relay 2: GPIO 6<br/>
        - Relay 3: GPIO 13<br/>
        - Relay 4: GPIO 16<br/>
        - Relay 5: GPIO 19<br/>
        - Relay 6: GPIO 20<br/>
        - Relay 7: GPIO 21<br/>
        - Relay 8: GPIO 26<br/>
        <br/>
        Note: Relays are ACTIVE LOW (GPIO LOW = Relay ON)<br/>
    </description>
    <params>
        <param field="Mode1" label="GPIO Chip" width="200px" required="true" default="gpiochip0"/>
    </params>
</plugin>
"""

import Domoticz
import gpiod

class BasePlugin:
    enabled = False
    chip = None
    lines = {}
    
    # GPIO pin mapping for Waveshare Relay Board (B)
    RELAY_PINS = {
        1: 5,   # Relay 1 -> GPIO 5
        2: 6,   # Relay 2 -> GPIO 6
        3: 13,  # Relay 3 -> GPIO 13
        4: 16,  # Relay 4 -> GPIO 16
        5: 19,  # Relay 5 -> GPIO 19
        6: 20,  # Relay 6 -> GPIO 20
        7: 21,  # Relay 7 -> GPIO 21
        8: 26   # Relay 8 -> GPIO 26
    }
    
    def __init__(self):
        return
    
    def onStart(self):
        Domoticz.Log("Waveshare Relay Board (gpiod) plugin starting")
        
        # Get GPIO chip name from parameters
        chip_name = Parameters["Mode1"]
        
        try:
            # Open GPIO chip
            self.chip = gpiod.Chip(chip_name)
            Domoticz.Log(f"Opened GPIO chip: {chip_name}")
            
            # Create devices if they don't exist
            if len(Devices) == 0:
                Domoticz.Log("Creating relay devices...")
                for relay_num in range(1, 9):
                    Domoticz.Device(
                        Name=f"Relay {relay_num}",
                        Unit=relay_num,
                        TypeName="Switch",
                        Used=1
                    ).Create()
                    Domoticz.Log(f"Created Relay {relay_num} device")
            
            # Request GPIO lines as outputs with initial HIGH state (relays OFF)
            for relay_num, gpio_pin in self.RELAY_PINS.items():
                try:
                    line = self.chip.get_line(gpio_pin)
                    line.request(
                        consumer="domoticz-relay",
                        type=gpiod.LINE_REQ_DIR_OUT,
                        default_vals=[1]  # HIGH = Relay OFF (active low)
                    )
                    self.lines[relay_num] = line
                    Domoticz.Log(f"Configured GPIO {gpio_pin} (Relay {relay_num}) as output")
                except Exception as e:
                    Domoticz.Error(f"Failed to configure GPIO {gpio_pin} (Relay {relay_num}): {str(e)}")
            
            self.enabled = True
            Domoticz.Log("Plugin started successfully")
            
        except Exception as e:
            Domoticz.Error(f"Failed to initialize GPIO: {str(e)}")
            self.enabled = False
    
    def onStop(self):
        Domoticz.Log("Waveshare Relay Board plugin stopping")
        
        # Release all GPIO lines and turn off relays
        for relay_num, line in self.lines.items():
            try:
                line.set_value(1)  # HIGH = Relay OFF
                line.release()
                Domoticz.Log(f"Released GPIO for Relay {relay_num}")
            except Exception as e:
                Domoticz.Error(f"Error releasing GPIO for Relay {relay_num}: {str(e)}")
        
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
            line = self.lines[Unit]
            gpio_pin = self.RELAY_PINS[Unit]
            
            # IMPORTANT: Inverted logic for active-low relays
            # Domoticz "On" -> GPIO LOW (0) -> Relay physically ON
            # Domoticz "Off" -> GPIO HIGH (1) -> Relay physically OFF
            if Command == "On":
                line.set_value(0)  # LOW = Relay ON
                Devices[Unit].Update(nValue=1, sValue="On")
                Domoticz.Log(f"Relay {Unit} (GPIO {gpio_pin}) turned ON (LOW)")
            elif Command == "Off":
                line.set_value(1)  # HIGH = Relay OFF
                Devices[Unit].Update(nValue=0, sValue="Off")
                Domoticz.Log(f"Relay {Unit} (GPIO {gpio_pin}) turned OFF (HIGH)")
            
        except Exception as e:
            Domoticz.Error(f"Error controlling Relay {Unit}: {str(e)}")

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
