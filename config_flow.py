"""
Config flow for Exhaustion Meter integration.
Enables UI-based setup and options for the custom component.
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "exhaustion_meter"


class ExhaustionMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Exhaustion Meter."""

    async def async_step_user(self, user_input=None):
        """Show the setup form to the user and create entry if submitted."""
        if user_input is not None:
            return self.async_create_entry(title="Exhaustion Meter", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler for this config entry."""
        return ExhaustionMeterOptionsFlowHandler(config_entry)


class ExhaustionMeterOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Exhaustion Meter config entries."""

    def __init__(self, config_entry):
        """Initialize options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, _=None):
        """Handle the initial step of the options flow."""
        return self.async_create_entry(title="", data={})
