"""Sensor para mostrar la tarifa eléctrica actual (2.0TD)."""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.const import CONF_Name
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

# Configuración por defecto
DEFAULT_NAME = "Tarifa Actual"
CONF_WORKDAY_SENSOR = "workday_entity"
DEFAULT_WORKDAY_SENSOR = "binary_sensor.workday_sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_Name, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_WORKDAY_SENSOR, default=DEFAULT_WORKDAY_SENSOR): cv.entity_id,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Configurar el sensor de tarifa."""
    name = config.get(CONF_Name)
    workday_entity = config.get(CONF_WORKDAY_SENSOR)

    add_entities([Tarifa20TDSensor(hass, name, workday_entity)], True)


class Tarifa20TDSensor(SensorEntity):
    """Representación del sensor de Tarifa."""

    def __init__(self, hass, name, workday_entity):
        """Inicializar el sensor."""
        self._hass = hass
        self._name = name
        self._workday_entity = workday_entity
        self._state = None
        self._attr_icon = "mdi:cash-clock"

    @property
    def name(self):
        """Nombre del sensor."""
        return self._name

    @property
    def native_value(self):
        """Devuelve el estado actual (valle, llana, punta)."""
        return self._state

    def update(self):
        """Calcula la tarifa actual basada en hora y día."""
        
        # 1. Obtener hora actual
        now = dt_util.now()
        hour = now.hour

        # 2. Comprobar si es laborable
        # Buscamos el estado del sensor workday configurado
        workday_state = self._hass.states.get(self._workday_entity)
        
        # Si no existe el sensor workday, asumimos que es laborable por seguridad,
        # o asumimos fin de semana si es Sábado(5) o Domingo(6) por Python.
        is_holiday = False
        if workday_state is None:
            # Fallback: Si no hay sensor, miramos si es fin de semana simple
            if now.weekday() >= 5:
                is_holiday = True
        elif workday_state.state == "off":
            is_holiday = True

        # 3. Lógica de decisión (Tu automatización convertida a código)
        if is_holiday:
            self._state = "valle"
        else:
            if 0 <= hour < 8:
                self._state = "valle"
            elif 8 <= hour < 10:
                self._state = "llana"
            elif 10 <= hour < 14:
                self._state = "punta"
            elif 14 <= hour < 18:
                self._state = "llana"
            elif 18 <= hour < 22:
                self._state = "punta"
            elif 22 <= hour <= 23:
                self._state = "llana"
            else:
                self._state = "valle" # Fallback
