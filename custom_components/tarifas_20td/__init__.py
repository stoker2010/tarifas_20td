"""La integración de Tarifas 2.0TD."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "tarifas_20td"

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configuración inicial mediante YAML (si se requiere)."""
    return True
