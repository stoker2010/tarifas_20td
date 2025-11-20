import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict,
)

# Asegúrate de que esto coincida con tu const.py
from .const import DOMAIN 

# Opciones para la región
REGIONS = [
    SelectOptionDict(value="peninsula", label="Península / Baleares / Canarias"),
    SelectOptionDict(value="ceuta", label="Ceuta"),
    SelectOptionDict(value="melilla", label="Melilla"),
]

class Tarifas20TDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Tarifas 2.0TD."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Paso inicial: El usuario elige qué quiere configurar."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["casa", "termo"]
        )

    # --- MÓDULO 1: CASA (TARIFAS) ---
    async def async_step_casa(self, user_input=None):
        """Configuración del gestor de tarifas y potencia."""
        errors = {}

        if user_input is not None:
            # ✅ AQUÍ ESTÁ EL ARREGLO: Forzamos el título "Gestión Casa"
            return self.async_create_entry(
                title="Gestión Casa 🏠", 
                data={**user_input, "type": "casa"}
            )

        # Esquema del formulario (Ajusta los nombres de variables si usas otros en tu sensor.py)
        schema = vol.Schema({
            vol.Required("region", default="peninsula"): SelectSelector(
                SelectSelectorConfig(options=REGIONS)
            ),
            vol.Required("grid_import"): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="energy")
            ),
            vol.Required("grid_export"): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="energy")
            ),
            vol.Optional("power_contracted", default=3.3): float,
        })

        return self.async_show_form(
            step_id="casa", 
            data_schema=schema, 
            errors=errors,
            description_placeholders={"title": "Configurar Tarifas"}
        )

    # --- MÓDULO 2: TERMO INTELIGENTE ---
    async def async_step_termo(self, user_input=None):
        """Configuración del termo eléctrico."""
        errors = {}

        if user_input is not None:
            # ✅ AQUÍ ESTÁ EL ARREGLO: Forzamos el título "Gestión Termo"
            return self.async_create_entry(
                title="Gestión Termo 🚿", 
                data={**user_input, "type": "termo"}
            )

        schema = vol.Schema({
            vol.Required("heater_switch"): EntitySelector(
                EntitySelectorConfig(domain=["switch", "input_boolean"])
            ),
            vol.Required("heater_temp_sensor"): EntitySelector(
                EntitySelectorConfig(domain="sensor", device_class="temperature")
            ),
            vol.Optional("boost_time", default=30): int,
        })

        return self.async_show_form(
            step_id="termo", 
            data_schema=schema, 
            errors=errors
        )
