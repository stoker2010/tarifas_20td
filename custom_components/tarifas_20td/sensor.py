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
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_track_point_in_time,
    async_track_state_change_event,
    async_track_time_change,
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
        sw_version="0.2.0",
        configuration_url="https://github.com/stoker2010/tarifas_20td",
    )

    # 1. Sensor Tramo
    tramo_sensor = Tarifa20TDTramo(hass, config, device_info)
    
    # 2. Sensor Balance Neto Real
    balance_real = BalanceNetoHorario(hass, config, device_info)

    # 3. Sensor Balance Neto Estimado (NUEVO)
    balance_estimado = BalanceNetoEstimado(hass, config, balance_real, device_info)

    # 4. Procesador de Energía y Sensores Diarios
    energy_processor = EnergyProcessor(hass, config, tramo_sensor, device_info)

    async_add_entities([
        tramo_sensor, 
        balance_real,
        balance_estimado,
        energy_processor.sensor_import_valle,
        energy_processor.sensor_import_llana,
        energy_processor.sensor_import_punta,
        energy_processor.sensor_export,
        energy_processor.sensor_home_consumption
    ])

# ------------------------------------------------------------------
# 1. SENSOR TRAMO HORARIO
# ------------------------------------------------------------------
class Tarifa20TDTramo(SensorEntity):
    """Sensor que determina el tramo actual."""
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
            elif 18 <= hour < 22: self._state = TRAMO_PUNTA
            elif 22 <= hour <= 24: self._state = TRAMO_LLANA
            else: self._state = TRAMO_VALLE

    @property
    def native_value(self):
        return self._state
    
    @property
    def extra_state_attributes(self):
        potencia = self._p_valle if self._state == TRAMO_VALLE else self._p_punta
        return {
            "potencia_contratada": potencia,
            "potencia_valle": self._p_valle,
            "potencia_punta": self._p_punta
        }

# ------------------------------------------------------------------
# 2. BALANCE NETO HORARIO (REAL)
# ------------------------------------------------------------------
class BalanceNetoHorario(RestoreEntity, SensorEntity):
    """Balance acumulado real que se resetea cada hora."""
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
            try:
                self._state = float(last_state.state)
            except ValueError:
                self._state = 0.0
        
        self._last_update = dt_util.now()
        
        self.async_on_remove(async_track_state_change_event(
            self._hass, [self._grid_entity], self._on_sensor_change
        ))
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
        try:
            power = float(new_state.state)
        except ValueError: return

        now = dt_util.now()
        if self._last_update:
            hours_diff = (now - self._last_update).total_seconds() / 3600.0
            energy = (power / 1000.0) * hours_diff
            self._state += energy
            
        self._last_update = now
        self.async_write_ha_state()

    @property
    def native_value(self):
        return round(self._state, 4)

# ------------------------------------------------------------------
# 3. BALANCE NETO ESTIMADO (PROYECCIÓN)
# ------------------------------------------------------------------
class BalanceNetoEstimado(SensorEntity):
    """Estima cómo acabará la hora basándose en el balance actual y la potencia actual."""
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
        """Escuchar cambios en el grid y en el balance real."""
        self.async_on_remove(
            async_track_state_change_event(
                self._hass, 
                [self._grid_entity, self._real_balance_sensor.entity_id], 
                self._update_estimation
            )
        )
        # También actualizar cada minuto por si la potencia es constante
        self.async_on_remove(
            async_track_time_change(self._hass, self._timer_update, second=0)
        )

    @callback
    def _timer_update(self, now):
        self._update_estimation(None)

    @callback
    def _update_estimation(self, event):
        # 1. Obtener Balance Real Acumulado
        balance_real = self._real_balance_sensor.native_value
        if balance_real is None: balance_real = 0.0

        # 2. Obtener Potencia Instantánea Grid
        grid_state = self._hass.states.get(self._grid_entity)
        if not grid_state or grid_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._state = balance_real # Sin datos de potencia, la estimación es el real
            self.async_write_ha_state()
            return

        try:
            grid_power_w = float(grid_state.state)
        except ValueError:
            grid_power_w = 0.0

        # 3. Calcular tiempo restante de la hora
        now = dt_util.now()
        minutes_left = 60 - now.minute
        hours_left = minutes_left / 60.0

        # 4. Proyección: Energía = Potencia(kW) * Tiempo(h)
        # Grid positivo = Excedente, Grid negativo = Consumo
        projected_energy = (grid_power_w / 1000.0) * hours_left

        # 5. Estimación Final
        self._state = balance_real + projected_energy
        self.async_write_ha_state()

    @property
    def native_value(self):
        return round(self._state, 4)

# ------------------------------------------------------------------
# 4. PROCESADOR DE ENERGÍA Y SENSORES DIARIOS
# ------------------------------------------------------------------
class EnergyProcessor:
    """Gestiona los contadores diarios."""

    def __init__(self, hass, config, tramo_sensor, device_info):
        self.hass = hass
        self.tramo_sensor = tramo_sensor
        self.grid_entity = config[CONF_GRID_SENSOR]
        self.solar_entity = config[CONF_SOLAR_SENSOR]
        
        # Sensores Diarios (DailyEnergySensor)
        self.sensor_import_valle = DailyEnergySensor(hass, "Energía Importada Valle (Diario)", "daily_import_valle", device_info)
        self.sensor_import_llana = DailyEnergySensor(hass, "Energía Importada Llana (Diario)", "daily_import_llana", device_info)
        self.sensor_import_punta = DailyEnergySensor(hass, "Energía Importada Punta (Diario)", "daily_import_punta", device_info)
        self.sensor_export = DailyEnergySensor(hass, "Energía Excedente (Diario)", "daily_export", device_info)
        self.sensor_home_consumption = DailyEnergySensor(hass, "Consumo Hogar (Diario)", "daily_home", device_info)
        
        self._last_update = None
        
        if hass.is_running:
            import asyncio
            asyncio.create_task(self._start_listening(None))
        else:
            hass.bus.async_listen_once("homeassistant_start", self._start_listening)

    async def _start_listening(self, _):
        self._last_update = dt_util.now()
        async_track_state_change_event(
            self.hass, [self.grid_entity, self.solar_entity], self._on_change
        )
        # Programar reset a las 00:00:00
        async_track_time_change(self.hass, self._reset_daily_counters, hour=0, minute=0, second=0)

    @callback
    def _reset_daily_counters(self, now):
        """Resetea todos los sensores a 0 a medianoche."""
        _LOGGER.debug("Reseteando contadores diarios a 0")
        self.sensor_import_valle.reset()
        self.sensor_import_llana.reset()
        self.sensor_import_punta.reset()
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
        except ValueError:
            return

        hours = (now - self._last_update).total_seconds() / 3600.0
        self._last_update = now
        
        # Cálculos
        energy_grid_kwh = (grid_w / 1000.0) * hours
        
        # 1. Exportación / Importación
        if energy_grid_kwh > 0:
            self.sensor_export.add_energy(energy_grid_kwh)
        else:
            imported_kwh = abs(energy_grid_kwh)
            tramo = self.tramo_sensor.native_value
            if tramo == TRAMO_VALLE: self.sensor_import_valle.add_energy(imported_kwh)
            elif tramo == TRAMO_LLANA: self.sensor_import_llana.add_energy(imported_kwh)
            elif tramo == TRAMO_PUNTA: self.sensor_import_punta.add_energy(imported_kwh)
        
        # 2. Consumo Hogar
        home_w = solar_w - grid_w
        if home_w < 0: home_w = 0 
        energy_home_kwh = (home_w / 1000.0) * hours
        self.sensor_home_consumption.add_energy(energy_home_kwh)


class DailyEnergySensor(RestoreEntity, SensorEntity):
    """Sensor de energía que se resetea diariamente."""
    
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
            try:
                self._state = float(state.state)
            except ValueError:
                self._state = 0.0

    def add_energy(self, kwh):
        self._state += kwh
        self.async_write_ha_state()

    def reset(self):
        self._state = 0.0
        self.async_write_ha_state()

    @property
    def native_value(self):
        return round(self._state, 4)
