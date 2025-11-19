"""Sensor para mostrar la tarifa eléctrica actual (2.0TD) en España."""
from __future__ import annotations
import logging
from datetime import datetime

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

# Configuración
DEFAULT_NAME = "Tarifa Actual"
CONF_WORKDAY_SENSOR = "workday_entity"
DEFAULT_WORKDAY_SENSOR = "binary_sensor.workday_sensor"

# Validación de configuración YAML
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_WORKDAY_SENSOR, default=DEFAULT_WORKDAY_SENSOR): cv.entity_id,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Configura la plataforma del sensor."""
    name = config.get(CONF_NAME)
    workday_entity = config.get(CONF_WORKDAY_SENSOR)

    add_entities([Tarifa20TDSensor(hass, name, workday_entity)], True)


class Tarifa20TDSensor(SensorEntity):
    """Representación del sensor de Tarifa 2.0TD."""

    def __init__(self, hass, name, workday_entity):
        """Inicializar el sensor."""
        self._hass = hass
        self._name = name
        self._workday_entity = workday_entity
        self._state = None
        self._attr_icon = "mdi:cash-clock"
        self._attr_unique_id = f"tarifa_20td_{name.lower().replace(' ', '_')}"

    @property
    def name(self):
        """Devuelve el nombre del sensor."""
        return self._name

    @property
    def native_value(self):
        """Devuelve el estado actual (valle, llana, punta)."""
        return self._state

    def update(self):
        """Actualiza el estado del sensor aplicando la lógica 2.0TD."""
        
        # 1. Obtener hora actual del sistema
        now = dt_util.now()
        hour = now.hour

        # 2. Comprobar si es festivo/fin de semana
        # Leemos el estado de la entidad Workday configurada
        workday_state = self._hass.states.get(self._workday_entity)
        
        is_holiday = False
        
        if workday_state is None:
            # Si el usuario no tiene configurado Workday, usamos fallback de Python (Sáb/Dom)
            if now.weekday() >= 5: # 5=Sábado, 6=Domingo
                is_holiday = True
        elif workday_state.state == "off":
            # Si workday está en OFF, es que NO es laborable (es festivo)
            is_holiday = True

        # 3. Lógica de Tramos Horarios
        if is_holiday:
            # Festivos y Fines de Semana siempre es VALLE
            self._state = "valle"
        else:
            # Día Laborable
            if 0 <= hour < 8:
                self._state = "valle"      # 00:00 - 08:00
            elif 8 <= hour < 10:
                self._state = "llana"      # 08:00 - 10:00
            elif 10 <= hour < 14:
                self._state = "punta"      # 10:00 - 14:00
            elif 14 <= hour < 18:
                self._state = "llana"      # 14:00 - 18:00
            elif 18 <= hour < 22:
                self._state = "punta"      # 18:00 - 22:00
            elif 22 <= hour <= 23:
                self._state = "llana"      # 22:00 - 24:00
            else:
                self._state = "valle"      # Fallback por seguridad
