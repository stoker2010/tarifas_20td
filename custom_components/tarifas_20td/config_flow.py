"""Config flow para Tarifas 2.0TD."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    DOMAIN,
    MENU_OPTION_CASA,
    MENU_OPTION_TERMO,
    CONF_TYPE,
    TYPE_CASA,
    TYPE_TERMO,
    CONF_ENERGY_SENSOR_IMPORT,
    CONF_ENERGY_SENSOR_EXPORT,
    CONF_POWER_CONTRACTED,
    CONF_ZONE,
    CONF_TERMO_ENTITY,
    CONF_TEMP_SENSOR,
)

_LOGGER = logging.getLogger(__name__)

class Tarifas20TDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el flujo de configuración."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial: Menú de selección."""
        return self.async_show_menu(
            step_id="user",
            menu_options=[MENU_OPTION_CASA, MENU_OPTION_TERMO]
        )

    async def async_step_casa(self, user_input=None):
        """Configuración de Tarifas de la Casa."""
        errors = {}
        if user_input is not None:
            user_input[CONF_TYPE] = TYPE_CASA
            # FORZAMOS EL TÍTULO AQUÍ:
            return self.async_create_entry(
                title="Gestión Casa 🏠", 
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_ENERGY_SENSOR_IMPORT): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="energy")
            ),
            vol.Optional(CONF_ENERGY_SENSOR_EXPORT): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="energy")
            ),
            vol.Required(CONF_ZONE, default="Peninsula"): SelectSelector(
                SelectSelectorConfig(
                    options=["Peninsula", "Canarias", "Ceuta", "Melilla"],
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(CONF_POWER_CONTRACTED, default=3.3): float,
        })

        return self.async_show_form(
            step_id="casa", data_schema=schema, errors=errors
        )

    async def async_step_termo(self, user_input=None):
        """Configuración del Termo Eléctrico."""
        errors = {}
        if user_input is not None:
            user_input[CONF_TYPE] = TYPE_TERMO
            # FORZAMOS EL TÍTULO AQUÍ:
            return self.async_create_entry(
                title="Gestión Termo 🚿", 
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_TERMO_ENTITY): EntitySelector(
                EntitySelectorConfig(domain=["switch", "input_boolean"])
            ),
            vol.Required(CONF_TEMP_SENSOR): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
        })

        return self.async_show_form(
            step_id="termo", data_schema=schema, errors=errors
        )
