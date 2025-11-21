"""Config Flow para Tarifas 2.0TD."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_GRID_SENSOR,
    CONF_SOLAR_SENSOR,
    CONF_POWER_VALLE,
    CONF_POWER_PUNTA,
    CONF_WORKDAY,
    DEFAULT_WORKDAY,
    CONF_TERMO_SWITCH,
    CONF_TERMO_TEMP_SENSOR,
    CONF_TERMO_POWER_SENSOR,
    CONF_TERMO_NOMINAL_POWER,
)

class Tarifas20TDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial: Formulario de usuario."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Gestor Energético", data=user_input)

        data_schema = vol.Schema(
            {
                # Sección Hogar
                vol.Required(CONF_GRID_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_SOLAR_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_POWER_VALLE, default=3000): vol.Coerce(int),
                vol.Required(CONF_POWER_PUNTA, default=4000): vol.Coerce(int),
                vol.Optional(CONF_WORKDAY, default=DEFAULT_WORKDAY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="binary_sensor")
                ),

                # Sección Termo
                vol.Required(CONF_TERMO_SWITCH): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch") # Interruptor real del termo
                ),
                vol.Required(CONF_TERMO_TEMP_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
                ),
                vol.Required(CONF_TERMO_POWER_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="power")
                ),
                vol.Required(CONF_TERMO_NOMINAL_POWER, default=1500): vol.Coerce(int),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
