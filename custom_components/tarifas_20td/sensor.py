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
    CONF_TERMO_NOMINAL_POWER, # Nueva constante importada
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

    # Info del Dispositivo Hogar (Principal)
    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Hogar",
        manufacturer="@stoker2010",
        model="Gestor Energético 2.0TD",
        sw_version="0.6.3",
        configuration_url="https://github.com/stoker2010/tarifas_20td",
    )
    
    # Info del Dispositivo Termo (Para agrupar la info del termo)
    device_info_termo = DeviceInfo(
        identifiers={(DOMAIN, f"{entry.entry_id}_termo")},
        name="Termo Eléctrico",
        manufacturer="@stoker2010",
        model="Control Termo v1",
        via_device=(DOMAIN, entry.entry_id),
    )

    entities = []

    # 1. Configuración (Potencias Hogar)
    entities.append(ConfigInfoSensor(hass, "Potencia Valle", f"{config[CONF_POWER_VALLE]} W", device_info))
    entities.append(ConfigInfoSensor(hass, "Potencia Punta", f"{config[CONF_POWER_PUNTA]} W", device_info))
    
    # 1b. Configuración (Potencia Termo - Nuevo)
    if CONF_TERMO_NOMINAL_POWER in config:
        entities.append(ConfigInfoSensor(hass, "Potencia Máxima Termo", f"{config[CONF_TERMO_NOMINAL_POWER]} W", device_info_termo))

    # 2. Sensor Tramo
    tramo_sensor = Tarifa20TDTramo(hass, config, device_info)
    entities.append(tramo_sensor)
    
    # 3. Sensor Balance Neto Real
    balance_real = BalanceNetoHorario(hass, config, device_info)
    entities.append(balance_real)

    # 4. Sensor Balance Neto Estimado
    balance_estimado = BalanceNetoEstimado(hass, config, balance_real, device_info)
    entities.append(balance_estimado)

    # 5. Sensor Intensidad Vertido 0 (Lógica +/-)
    intensidad_sensor = IntensidadVertidoCero(hass, config, balance_real, device_info)
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
# CLASES Y LÓGICA
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
        self.async_on_remove(async_track_point_in_time(self._hass, self._timer_callback, dt_util.now().replace(second=0) + timedelta(minutes=1)))

    async def _timer_callback(self, now):
        self._update_state()
        self.async_write_ha_state()
        async_track_point_in_time(self._hass, self._timer_callback, now.replace(second=0) + timedelta(minutes=1))

    def _update_state(self):
        now = dt_util.now()
        hour = now.hour
        is_holiday = False
        wd_state = self._hass.states.get(self._workday_entity)
        if wd_state is None:
             if now.weekday() >= 5: is_holiday = True
        elif wd_state.state == "off": is_holiday = True

        if is_holiday: self._state = TRAMO_VALLE
        else:
            if 0 <= hour < 8: self._state = TRAMO_VALLE
            elif 8 <= hour < 10: self._state = TRAMO_LLANA
            elif 10 <= hour < 14: self._state = TRAMO_PUNTA
            elif 14 <= hour < 18: self._state = TRAMO_LLANA
            elif 18 <= hour < 22: self._state = TRAMO_PUNTA
            elif 22 <= hour <= 24: self._state = TRAMO_LLANA
            else: self._state = TRAMO_VALLE

    @property
    def native_value(self): return self._state
    @property
    def extra_state_attributes(self):
        potencia = self._p_valle if self._state == TRAMO_VALLE else self._p_punta
        return {"potencia_contratada": potencia, "potencia_valle": self._p_valle, "potencia_punta": self._p_punta}

class BalanceNetoHorario(RestoreEntity, SensorEntity):
    _attr_state_class = SensorStateClass.TOTAL
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_icon = "mdi:scale-balance"

    def __init__(self, hass, config, device_info):
        self._hass = hass
        self._attr_device_info = device_info
        self._grid_entity = config[CONF_GRID_SENSOR]
        self._attr_name = "Balance Neto Horario (Real)"
        self._attr_unique_id = f"{DOMAIN}_balance_neto_real"
        self._state = 0.0
        self._last_update = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            try: self._state = float(last_state.state)
            except ValueError: self._state = 0.0
        self._last_update = dt_util.now()
        self.async_on_remove(async_track_state_change_event(self._hass, [self._grid_entity], self._on_sensor_change))
        self._schedule_reset()

    def _schedule_reset(self):
        now = dt_util.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        async_track_point_in_time(self._hass, self._reset_callback, next_hour)

    @callback
    def _reset_callback(self, now):
        self._state = 0.0
        self._last_update = now
        self.async_write_ha_state()
        self._schedule_reset()

    @callback
    def _on_sensor_change(self, event):
        new_state = event.data.get("new_state")
        if not new_state or new_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE): return
        try: power = float(new_state.state)
        except ValueError: return
        now = dt_util.now()
        if self._last_update:
            hours_diff = (now - self._last_update).total_seconds() / 3600.0
            energy = (power / 1000.0) * hours_diff
            self._state += energy
        self._last_update = now
        self.async_write_ha_state()

    @property
    def native_value(self): return round(self._state, 4)

class BalanceNetoEstimado(SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_icon = "mdi:chart-line"

    def __init__(self, hass, config, real_balance_sensor, device_info):
        self._hass = hass
        self._attr_device_info = device_info
        self._grid_entity = config[CONF_GRID_SENSOR]
        self._real_balance_sensor = real_balance_sensor
        self._attr_name = "Balance Neto Horario (Estimado)"
        self._attr_unique_id = f"{DOMAIN}_balance_neto_estimado"
        self._state = 0.0

    async def async_added_to_hass(self):
        self.async_on_remove(async_track_state_change_event(self._hass, [self._grid_entity, self._real_balance_sensor.entity_id], self._update_estimation))
        self.async_on_remove(async_track_time_change(self._hass, self._timer_update, second=0))

    @callback
    def _timer_update(self, now): self._update_estimation(None)

    @callback
    def _update_estimation(self, event):
        balance_real = self._real_balance_sensor.native_value
        if balance_real is None: balance_real = 0.0
        grid_state = self._hass.states.get(self._grid_entity)
        if not grid_state or grid_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._state = balance_real
            self.async_write_ha_state()
            return
        try: grid_power_w = float(grid_state.state)
        except ValueError: grid_power_w = 0.0
        now = dt_util.now()
        minutes_left = 60 - now.minute
        hours_left = minutes_left / 60.0
        projected_energy = (grid_power_w / 1000.0) * hours_left
        self._state = balance_real + projected_energy
        self.async_write_ha_state()

    @property
    def native_value(self): return round(self._state, 4)

class IntensidadVertidoCero(SensorEntity):
    """Calcula Amperios (+/-) para terminar 0."""
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_icon = "mdi:current-ac"

    def __init__(self, hass, config, real_balance_sensor, device_info):
        self._hass = hass
        self._attr_device_info = device_info
        self._grid_entity = config[CONF_GRID_SENSOR]
        self._real_balance_sensor = real_balance_sensor
        self._attr_name = "Intensidad vertido 0"
        self._attr_unique_id = f"{DOMAIN}_intensidad_vertido_0"
        self._state = 0.0
        self._voltage = 240.0 

    async def async_added_to_hass(self):
        self.async_on_remove(async_track_time_interval(self._hass, self._update_current, timedelta(minutes=5)))
        self._update_current(None)

    @callback
    def _update_current(self, now):
        balance_real = self._real_balance_sensor.native_value
        if balance_real is None: balance_real = 0.0
        grid_state = self._hass.states.get(self._grid_entity)
        if not grid_state or grid_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._state = 0.0
            self.async_write_ha_state()
            return
        try: grid_power_w = float(grid_state.state)
        except ValueError: grid_power_w = 0.0
        now_time = dt_util.now()
        minutes_left = 60 - now_time.minute
        if minutes_left == 0: minutes_left = 1 
        hours_left = minutes_left / 60.0
        projected_end_kwh = balance_real + (grid_power_w / 1000.0 * hours_left)
        power_correction_kw = projected_end_kwh / hours_left
        power_correction_w = power_correction_kw * 1000.0
        self._state = power_correction_w / self._voltage
        self.async_write_ha_state()

    @property
    def native_value(self): return round(self._state, 2)

class EnergyProcessor:
    def __init__(self, hass, config, tramo_sensor, device_info):
        self.hass = hass
        self.tramo_sensor = tramo_sensor
        self.grid_entity = config[CONF_GRID_SENSOR]
        self.solar_entity = config[CONF_SOLAR_SENSOR]
        self.sensor_import_total = DailyEnergySensor(hass, "Energía Importada Total (Diario)", "daily_import_total", device_info)
        self.sensor_export = DailyEnergySensor(hass, "Energía Excedente (Diario)", "daily_export", device_info)
        self.sensor_home_consumption = DailyEnergySensor(hass, "Consumo Hogar (Diario)", "daily_home", device_info)
        self._last_update = None
        if hass.is_running:
            import asyncio
            asyncio.create_task(self._start_listening(None))
        else: hass.bus.async_listen_once("homeassistant_start", self._start_listening)

    async def _start_listening(self, _):
        self._last_update = dt_util.now()
        async_track_state_change_event(self.hass, [self.grid_entity, self.solar_entity], self._on_change)
        async_track_time_change(self.hass, self._reset_daily_counters, hour=0, minute=0, second=0)

    @callback
    def _reset_daily_counters(self, now):
        self.sensor_import_total.reset()
        self.sensor_export.reset()
        self.sensor_home_consumption.reset()

    @callback
    def _on_change(self, event):
        now = dt_util.now()
        if self._last_update is None: 
            self._last_update = now
            return
        try:
            grid_st = self.hass.states.get(self.grid_entity)
            solar_st = self.hass.states.get(self.solar_entity)
            grid_w = float(grid_st.state) if grid_st and grid_st.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) else 0.0
            solar_w = float(solar_st.state) if solar_st and solar_st.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) else 0.0
        except ValueError: return
        hours = (now - self._last_update).total_seconds() / 3600.0
        self._last_update = now
        energy_grid_kwh = (grid_w / 1000.0) * hours
        if energy_grid_kwh > 0: self.sensor_export.add_energy(energy_grid_kwh)
        else: self.sensor_import_total.add_energy(abs(energy_grid_kwh))
        home_w = solar_w - grid_w
        if home_w < 0: home_w = 0 
        energy_home_kwh = (home_w / 1000.0) * hours
        self.sensor_home_consumption.add_energy(energy_home_kwh)

class DailyEnergySensor(RestoreEntity, SensorEntity):
    _attr_state_class = SensorStateClass.TOTAL
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    def __init__(self, hass, name, uid_suffix, device_info):
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{uid_suffix}"
        self._attr_device_info = device_info
        self._state = 0.0
    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state and state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            try: self._state = float(state.state)
            except ValueError: self._state = 0.0
    def add_energy(self, kwh):
        self._state += kwh
        self.async_write_ha_state()
    def reset(self):
        self._state = 0.0
        self.async_write_ha_state()
    @property
    def native_value(self): return round(self._state, 4)
