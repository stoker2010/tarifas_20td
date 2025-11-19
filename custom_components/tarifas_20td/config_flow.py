"""Config Flow para Tarifas 2.0TD."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_GRID_SENSOR,
    CONF_SOLAR_SENSOR,
    CONF_POWER_VALLE,
    CONF_POWER_PUNTA,
    CONF_WORKDAY,
    CONF_TERMO_SWITCH,
    CONF_TERMO_TEMP_SENSOR,
    CONF_TERMO_POWER_SENSOR,
    CONF_TERMO_NOMINAL_POWER,
)

class Tarifas20TDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Manejar el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial: Solicitar datos al usuario."""
        errors = {}

        if user_input is not None:
            # Validar que las entidades existan o validaciones extra si fueran necesarias
            return self.async_create_entry(title="Gestor Energético 2.0TD", data=user_input)

        # Esquema del formulario
        data_schema = vol.Schema({
            vol.Required(CONF_GRID_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="power")
            ),
            vol.Required(CONF_SOLAR_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="power")
            ),
            vol.Required(CONF_POWER_VALLE, default=3450): int,
            vol.Required(CONF_POWER_PUNTA, default=4600): int,
            vol.Optional(CONF_WORKDAY, default="binary_sensor.workday_sensor"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor")
            ),
            # Sección Termo
            vol.Required(CONF_TERMO_SWITCH): selector.EntitySelector(
                selector.EntitySelectorConfig(domain=["switch", "input_boolean"])
            ),
            vol.Required(CONF_TERMO_TEMP_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Required(CONF_TERMO_POWER_SENSOR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="power")
            ),
            vol.Required(CONF_TERMO_NOMINAL_POWER, default=1500): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
