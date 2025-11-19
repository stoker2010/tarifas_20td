"""Config Flow para Tarifas 2.0TD."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_GRID_SENSOR,
    CONF_SOLAR_SENSOR,
    CONF_POWER_VALLE,
    CONF_POWER_PUNTA,
    CONF_WORKDAY,
    DEFAULT_WORKDAY
)

class Tarifas20TDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial: Formulario de usuario."""
        errors = {}

        if user_input is not None:
            # Validación básica (opcional)
            return self.async_create_entry(title="Tarifas y Balance 2.0TD", data=user_input)

        # Esquema del formulario
        data_schema = vol.Schema(
            {
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
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
