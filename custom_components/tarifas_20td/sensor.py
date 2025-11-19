"""Sensores para Tarifas 2.0TD y Balance Neto."""
from __future__ import annotations
import logging
from datetime import timedelta, datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricCurrent,
    EntityCategory,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_track_point_in_time,
    async_track_state_change_event,
    async_track_time_change,
    async_track_time_interval,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_GRID_SENSOR,
    CONF_SOLAR_SENSOR,
    CONF_POWER_VALLE,
    CONF_POWER_PUNTA,
    CONF_WORKDAY,
    TRAMO_VALLE,
    TRAMO_LLANA,
    TRAMO_PUNTA,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar sensores desde ConfigEntry."""
    config = entry.data

    # Info del Dispositivo
    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Hogar",
        manufacturer="@stoker2010",
        model="Gestor Energético 2.0TD",
        sw_version="0.6.0",
        configuration_url="https://github.com/stoker2010/tarifas_20td",
    )

    entities = []

    # 1. Configuración (Potencias)
    entities.append(ConfigInfoSensor(hass, "Config: Potencia Valle", f"{config[CONF_POWER_VALLE]} W", device_info))
    entities.append(ConfigInfoSensor(hass, "Config: Potencia Punta", f"{config[CONF_POWER_PUNTA]} W", device_info))

    # 2. Sensor Tramo
    tramo_sensor = Tarifa20TDTramo(hass, config, device_info)
    entities.append(tramo_sensor)
    
    # 3. Sensor Balance Neto Real
    balance_real = BalanceNetoHorario(hass, config, device_info)
    entities.append(balance_real)

    # 4. Sensor Balance Neto Estimado
    balance_estimado = BalanceNetoEstimado(hass, config, balance_real, device_info)
    entities.append(balance_estimado)

    # 5. Sensor Intensidad Excedente (5 min)
    intensidad_sensor = IntensidadExcedente(hass, config, balance_real, device_info)
    entities.append(intensidad_sensor)

    # 6. Procesador de Energía y Sensores Diarios
    energy_processor = EnergyProcessor(hass, config, tramo_sensor, device_info)
    
    entities.extend([
        energy_processor.sensor_import_total, 
        energy_processor.sensor_export,
        energy_processor.sensor_home_consumption
    ])

    async_add_entities(entities)


# ------------------------------------------------------------------
# SENSORES DE DIAGNÓSTICO
# ------------------------------------------------------------------
class ConfigInfoSensor(SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:information-outline"

    def __init__(self, hass, name, value, device_info):
        self._hass = hass
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_conf_{name.lower().replace(' ', '_').replace(':', '')}"
        self._attr_native_value = value
        self._attr_device_info = device_info

# ------------------------------------------------------------------
# 1. SENSOR TRAMO HORARIO
# ------------------------------------------------------------------
class Tarifa20TDTramo(SensorEntity):
    def __init__(self, hass, config, device_info):
        self._hass = hass
        self._attr_device_info = device_info
        self._attr_name = "Tarifa 2.0TD Tramo Actual"
        self._attr_unique_id = f"{DOMAIN}_tramo_actual"
        self._attr_icon = "mdi:clock-time-four-outline"
        self._state = TRAMO_VALLE
        self._p_valle = config[CONF_POWER_VALLE]
        self._p_punta = config[CONF_POWER_PUNTA]
        self._workday_entity = config.get(CONF_WORKDAY)

    async def async_added_to_hass(self):
        self._update_state()
        self.async_on_remove(
            async_track_point_in_time(
                self._hass, self._timer_callback, dt_util.now().replace(second=0) + timedelta(minutes=1)
            )
        )

    async def _timer_callback(self, now):
        self._update_state()
        self.async_write_ha_state()
        async_track_point_in_time(
            self._hass, self._timer_callback, now.replace(second=0) + timedelta(minutes=1)
        )

    def _update_state(self):
        now = dt_util.now()
        hour = now.hour
        is_holiday = False
        wd_state = self._hass.states.get(self._workday_entity)
        
        if wd_state is None:
             if now.weekday() >= 5: is_holiday = True
        elif wd_state.state == "off":
            is_holiday = True

        if is_holiday:
            self._state = TRAMO_VALLE
        else:
            if 0 <= hour < 8: self._state = TRAMO_VALLE
            elif 8 <= hour < 10: self._state = TRAMO_LLANA
            elif 10 <= hour < 14: self._state = TRAMO_PUNTA
            elif 14 <= hour < 18: self._state = TRAMO_LLANA
            elif 18 <= hour < 2
