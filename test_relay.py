#!/usr/bin/env python3
"""
Test script pre Waveshare Relay Board GPIO
Otestuje všetky relé bez Domoticz
"""

import sys
import time

try:
    import gpiod
except ImportError:
    print("ERROR: python3-gpiod nie je nainštalované!")
    print("Spusti: sudo apt install python3-gpiod")
    sys.exit(1)

# GPIO piny pre relé
RELAY_PINS = {
    1: 5,
    2: 6,
    3: 13,
    4: 16,
    5: 19,
    6: 20,
    7: 21,
    8: 26
}

def test_relay_board():
    print("=" * 60)
    print("Waveshare Relay Board - GPIO Test")
    print("=" * 60)
    print()
    
    try:
        # Otvor GPIO chip
        chip = gpiod.Chip('gpiochip0')
        print(f"✓ Otvorený GPIO chip: {chip.name()}")
        print()
        
        # Získaj všetky GPIO line objekty
        lines = {}
        print("Konfigurácia GPIO pinov:")
        for relay_num, gpio_pin in RELAY_PINS.items():
            line = chip.get_line(gpio_pin)
            line.request(
                consumer="relay-test",
                type=gpiod.LINE_REQ_DIR_OUT,
                default_vals=[1]  # HIGH = Relay OFF
            )
            lines[relay_num] = line
            print(f"  ✓ Relay {relay_num} -> GPIO {gpio_pin} (Pin {get_physical_pin(gpio_pin)})")
        
        print()
        print("-" * 60)
        print("ZAČÍNAM TEST - Pozoruj relé na doske!")
        print("-" * 60)
        print()
        
        # Test 1: Postupné zapínanie/vypínanie
        print("Test 1: Postupné zapínanie každého relé (1s)")
        for relay_num in range(1, 9):
            print(f"  → Relay {relay_num} ON", end="", flush=True)
            lines[relay_num].set_value(0)  # LOW = ON
            time.sleep(1)
            print(f" → OFF")
            lines[relay_num].set_value(1)  # HIGH = OFF
            time.sleep(0.5)
        
        print()
        
        # Test 2: Všetky naraz
        print("Test 2: Všetky relé ZAP")
        for relay_num in range(1, 9):
            lines[relay_num].set_value(0)  # LOW = ON
        print("  → Všetky relé sú zapnuté (počuj kliknutie)")
        time.sleep(3)
        
        print("Test 2: Všetky relé VYP")
        for relay_num in range(1, 9):
            lines[relay_num].set_value(1)  # HIGH = OFF
        print("  → Všetky relé sú vypnuté")
        time.sleep(2)
        
        print()
        
        # Test 3: Blikanie
        print("Test 3: Blikanie (3x)")
        for i in range(3):
            print(f"  → Bliknutie {i+1}/3")
            for relay_num in range(1, 9):
                lines[relay_num].set_value(0)  # ON
            time.sleep(0.3)
            for relay_num in range(1, 9):
                lines[relay_num].set_value(1)  # OFF
            time.sleep(0.3)
        
        print()
        print("-" * 60)
        print("TEST DOKONČENÝ!")
        print("-" * 60)
        print()
        
        # Cleanup - vypni všetky relé
        print("Čistenie: Vypínam všetky relé...")
        for relay_num, line in lines.items():
            line.set_value(1)  # HIGH = OFF
            line.release()
        
        print("✓ GPIO piny uvoľnené")
        print()
        print("=" * 60)
        print("Ak si videl/počul relé prepínať, GPIO funguje správne!")
        print("Môžeš pokračovať v inštalácii Domoticz pluginu.")
        print("=" * 60)
        
    except PermissionError:
        print()
        print("ERROR: Nemáš oprávnenie na prístup k GPIO!")
        print()
        print("Riešenia:")
        print("1. Spusti skript ako root: sudo python3 test_relay.py")
        print("2. Alebo pridaj používateľa do gpio skupiny:")
        print("   sudo usermod -a -G gpio $USER")
        print("   potom sa odhláš a znovu prihláš")
        sys.exit(1)
        
    except Exception as e:
        print()
        print(f"ERROR: {str(e)}")
        print()
        print("Možné problémy:")
        print("1. GPIO chip 'gpiochip0' neexistuje")
        print("2. GPIO piny sú už použité iným procesom")
        print("3. Hardvér nie je správne pripojený")
        print()
        print("Skús:")
        print("  ls -la /dev/gpiochip*")
        print("  gpioinfo gpiochip0")
        sys.exit(1)

def get_physical_pin(bcm_pin):
    """Vráti číslo fyzického pinu pre daný BCM pin"""
    pin_mapping = {
        5: 29,
        6: 31,
        13: 33,
        16: 36,
        19: 35,
        20: 38,
        21: 40,
        26: 37
    }
    return pin_mapping.get(bcm_pin, "?")

if __name__ == "__main__":
    print()
    print("POZOR: Tento test bude prepínať všetky relé!")
    print("Uisti sa, že:")
    print("  - Relay Board je správne pripojená k RPi")
    print("  - K relé NIČ nie je pripojené (alebo je to bezpečné)")
    print("  - Máš napájanie pripojené (ak je potrebné)")
    print()
    
    odpoved = input("Pokračovať? (ano/nie): ").strip().lower()
    if odpoved not in ['ano', 'a', 'y', 'yes']:
        print("Test zrušený.")
        sys.exit(0)
    
    print()
    test_relay_board()
