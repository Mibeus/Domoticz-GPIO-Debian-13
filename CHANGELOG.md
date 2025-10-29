# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.0.0] - 2025-10-29

### 🎉 Major Rewrite - Universal GPIO Plugin

This is a complete rewrite of the plugin to make it universal and configurable.

### Added
- ✅ **JSON Configuration File** (`gpio_config.json`) for easy customization
- ✅ **Configurable GPIO pins** - no more hardcoded pins
- ✅ **Active LOW / Active HIGH support** - works with any relay board
- ✅ **Custom relay names** - name your devices as you want
- ✅ **Auto-detection** of plugin directory - works with any Domoticz installation
- ✅ **Flexible installation** - just clone to `domoticz/plugins/`
- ✅ **Better error handling** with detailed log messages
- ✅ **Configuration validation** on startup
- ✅ **Support for multiple GPIO chips** (gpiochip0, gpiochip1, etc.)

### Changed
- 🔄 **Plugin name**: "Waveshare Relay Board" → "Domoticz RPI GPIO"
- 🔄 **Installation method**: Now uses standard Domoticz plugin installation
- 🔄 **Configuration**: Moved from hardcoded values to JSON file
- 🔄 **Directory structure**: Simplified to `DomoticzRPIGPIO/`
- 🔄 **Documentation**: Complete rewrite with examples and use cases

### Removed
- ❌ Hardcoded GPIO pins
- ❌ Hardcoded relay logic (active_low only)
- ❌ Waveshare-specific naming
- ❌ Custom installation script (use standard git clone)
- ❌ Hardcoded Domoticz paths

### Technical Details
- Plugin now reads `gpio_config.json` on startup
- Validates configuration before initializing GPIO
- Supports any number of GPIO pins (1-28)
- Works with any relay board (Waveshare, SainSmart, generic, etc.)
- No modification of Domoticz core files needed

### Migration from v1.0.0
If upgrading from v1.0.0:
1. Remove old plugin directory: `rm -rf domoticz/plugins/WaveshareRelayGPIOD`
2. Install v2.0.0: `git clone ... DomoticzRPIGPIO`
3. Configure `gpio_config.json` with your GPIO pins
4. Restart Domoticz

---

## [1.0.0] - 2025-10-29

### Added
- Initial release
- Support for Waveshare RPi Relay Board (B)
- Control 8 GPIO relays via libgpiod
- Active LOW logic for relay boards
- Automatic installation script
- GPIO test script
- Complete Slovak documentation
- Debian 13 (Trixie) support
- Domoticz 2025.2+ support

### Technical Details
- Uses modern libgpiod library
- Python 3 implementation
- Hardcoded GPIO pins: 5, 6, 13, 16, 19, 20, 21, 26
- Safe shutdown - all relays turned off on plugin stop
- Auto-initialization of GPIO pins to HIGH (relays off)

---

## [Unreleased]

### Planned for v2.1.0
- [ ] Web-based configuration interface
- [ ] GPIO pin conflict detection
- [ ] Support for PWM outputs
- [ ] Input GPIO support (read button states)
- [ ] Pulse mode for momentary relays
- [ ] Scheduled relay timers

### Planned for v2.2.0
- [ ] Multi-board support (multiple instances)
- [ ] GPIO expander support (MCP23017, PCF8574)
- [ ] Custom scripts on relay state change
- [ ] Energy monitoring integration
- [ ] Backup/restore configuration

---

## Version History Summary

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 2.0.0 | 2025-10-29 | Major | Universal configurable GPIO plugin |
| 1.0.0 | 2025-10-29 | Initial | Waveshare-specific relay control |

---

## Breaking Changes

### v1.0.0 → v2.0.0

**⚠️ Breaking Changes:**
- Plugin directory changed: `WaveshareRelayGPIOD` → `DomoticzRPIGPIO`
- Installation method changed: custom script → standard git clone
- Configuration: hardcoded → JSON file
- Hardware name in Domoticz changed

**Migration Required:**
- Old installations will not automatically upgrade
- Must remove old plugin and install new version
- Devices will need to be re-added in Domoticz

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/Mibeus/Domoticz-GPIO-Debian-13/issues
- GitHub Discussions: https://github.com/Mibeus/Domoticz-GPIO-Debian-13/discussions
