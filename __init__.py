# Exhaustion Meter integration for Home Assistant

"""
Exhaustion Meter integration for Home Assistant.
Handles setup and registration of the custom sensor platform.
"""
# Exhaustion Meter integration for Home Assistant

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "exhaustion_meter"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )
    return True
