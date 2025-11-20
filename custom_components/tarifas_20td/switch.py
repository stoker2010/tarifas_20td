"""Plataforma Switch para Tarifas 2.0TD (Gestión Termo)."""
import logging
import asyncio
from datetime import timedelta
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, TYPE_TERMO, CONF_TYPE, CONF_TERMO_ENTITY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configura los switches desde una entrada de configuración."""
    config = config_entry.data

    # Solo creamos switches si es configuración de TERMO
    if config.get(CONF_TYPE) == TYPE_TERMO:
        termo_real = config[CONF_TERMO_ENTITY]
        async_add_entities([
            TermoForceSwitch(hass, termo_real),
            TermoBoostSwitch(hass, termo_real)
        ])

class TermoForceSwitch(SwitchEntity, RestoreEntity):
    """Interruptor para Forzar el Termo (Manual)."""

    def __init__(self, hass, termo_entity):
        self.hass = hass
        self._termo_entity = termo_entity
        self._is_on = False
        self._attr_name = "Termo Forzar Encendido"
        self._attr_unique_id = f"termo_force_{termo_entity}"
        self._attr_icon = "mdi:fire-alert"

    async def async_turn_on(self, **kwargs):
        """Activar forzado."""
        self._is_on = True
        # Encendemos el termo real
        await self.hass.services.async_call(
            "switch", "turn_on", {"entity_id": self._termo_entity}
        )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Desactivar forzado."""
        self._is_on = False
        # Opcional: Al quitar el forzado, podríamos apagar el termo
        # o dejar que la automatización decida. Por seguridad, no lo apagamos
        # drásticamente, pero lo lógico es que si quitas el forzado, se apague.
        await self.hass.services.async_call(
            "switch", "turn_off", {"entity_id": self._termo_entity}
        )
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

class TermoBoostSwitch(SwitchEntity, RestoreEntity):
    """Interruptor Temporizado 30 min (Boost)."""

    def __init__(self, hass, termo_entity):
        self.hass = hass
        self._termo_entity = termo_entity
        self._is_on = False
        self._attr_name = "Termo Boost 30m"
        self._attr_unique_id = f"termo_boost_{termo_entity}"
        self._attr_icon = "mdi:timer-outline"
        self._timer_cancel = None

    async def async_turn_on(self, **kwargs):
        """Activar Boost."""
        self._is_on = True
        # Encender termo real
        await self.hass.services.async_call(
            "switch", "turn_on", {"entity_id": self._termo_entity}
        )
        self.async_write_ha_state()

        # Programar apagado en 30 min
        target_time = dt_util.now() + timedelta(minutes=30)
        
        # Cancelar timer previo si existía
        if self._timer_cancel:
            self._timer_cancel()
            
        self._timer_cancel = async_track_point_in_time(
            self.hass, self._timer_callback, target_time
        )

    async def async_turn_off(self, **kwargs):
        """Desactivar Boost manual o automáticamente."""
        self._is_on = False
        if self._timer_cancel:
            self._timer_cancel()
            self._timer_cancel = None
            
        # Apagar el termo real
        await self.hass.services.async_call(
            "switch", "turn_off", {"entity_id": self._termo_entity}
        )
        self.async_write_ha_state()

    @callback
    def _timer_callback(self, now):
        """Se ejecuta cuando termina el tiempo."""
        self.hass.add_job(self.async_turn_off())

    @property
    def is_on(self):
        return self._is_on
