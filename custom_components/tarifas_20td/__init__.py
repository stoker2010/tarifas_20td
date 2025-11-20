"""Inicialización de Tarifas 2.0TD."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_TYPE, TYPE_TERMO

# Plataformas soportadas
PLATFORMS: list[str] = ["sensor", "number", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurar desde una entrada de configuración (UI)."""

    # --- 🛠️ PARCHE DE AUTOCORRECCIÓN DE NOMBRE ---
    # Este bloque verifica si el título está vacío o es genérico y lo arregla a la fuerza.
    
    titulo_actual = entry.title
    tipo_config = entry.data.get(CONF_TYPE)

    # Definimos el nombre correcto según el tipo
    nuevo_titulo = "Gestión Casa 🏠"
    if tipo_config == TYPE_TERMO:
        nuevo_titulo = "Gestión Termo 🚿"

    # Si no tiene título, o el título no coincide con el que queremos... ¡Lo cambiamos!
    if not titulo_actual or titulo_actual != nuevo_titulo:
        hass.config_entries.async_update_entry(entry, title=nuevo_titulo)
    # ---------------------------------------------------------

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descargar una entrada de configuración."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
