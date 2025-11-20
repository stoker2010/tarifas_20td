"""Plataforma Sensor para Tarifas 2.0TD."""
import logging
from collections import deque
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorDeviceClass
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_interval
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN, 
    TYPE_CASA, 
    TYPE_TERMO, 
    CONF_TYPE, 
    CONF_TEMP_SENSOR,
    CONF_ENERGY_SENSOR_IMPORT, # Asumo que estas imports existen de tu código anterior
    CONF_ENERGY_SENSOR_EXPORT,
    CONF_ZONE
)

# ... (Aquí irían los imports y clases de tarifas existentes: PeriodoSensor, EnergiaSensor, etc.) ...
# NOTA: Mantén tus clases anteriores de tarifas (PeriodoSensor, etc). 
# Voy a añadir solo la clase nueva y la lógica de setup para el Termo.

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configura los sensores."""
    config = config_entry.data
    
    if config.get(CONF_TYPE) == TYPE_CASA:
        # ... Lógica existente para crear sensores de tarifas ...
        # async_add_entities([PeriodoSensor(...), EnergiaSensor(...)])
        pass # (Mantén tu código original aquí para CASA)

    elif config.get(CONF_TYPE) == TYPE_TERMO:
        temp_sensor_id = config[CONF_TEMP_SENSOR]
        async_add_entities([TermoDerivadaSensor(hass, temp_sensor_id)])


class TermoDerivadaSensor(SensorEntity):
    """Sensor virtual: Derivada de temperatura (1h)."""

    def __init__(self, hass, source_entity):
        self.hass = hass
        self._source_entity = source_entity
        self._attr_name = "Termo Derivada (1h)"
        self._attr_unique_id = f"termo_derivada_{source_entity}"
        self._attr_native_unit_of_measurement = "°C/h"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-bell-curve-cumulative"
        
        self._state = 0.0
        # Guardamos pares (timestamp, valor)
        self._history = deque() 

    async def async_added_to_hass(self):
        """Suscribirse a actualizaciones."""
        # Actualizar cuando cambie el sensor fuente
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._source_entity], self._on_source_update
            )
        )
        # Limpiar historia vieja cada minuto
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self._clean_history, timedelta(minutes=1)
            )
        )

    @callback
    def _on_source_update(self, event):
        """Nuevo valor de temperatura."""
        new_state = event.data.get("new_state")
        if new_state is None or new_state.state in ["unknown", "unavailable"]:
            return
        
        try:
            val = float(new_state.state)
            now = dt_util.now()
            self._history.append((now, val))
            self._calculate_derivative()
        except ValueError:
            pass

    @callback
    def _clean_history(self, now):
        """Eliminar datos de más de 1 hora y recalcular."""
        if not self._history:
            return
        
        limit = now - timedelta(hours=1)
        
        # Eliminar antiguos
        while self._history and self._history[0][0] < limit:
            self._history.popleft()
            
        self._calculate_derivative()

    def _calculate_derivative(self):
        """Calcula la diferencia: (Actual - Más antiguo en la ventana)."""
        if not self._history:
            self._state = 0.0
        else:
            # Tomamos el valor actual (el último) y el más antiguo (el primero en la cola)
            latest_val = self._history[-1][1]
            oldest_val = self._history[0][1]
            
            # Diferencia simple en la ventana de tiempo disponible (hasta 1h)
            diff = latest_val - oldest_val
            self._state = round(diff, 2)
            
        self.async_write_ha_state()

    @property
    def native_value(self):
        return self._state
