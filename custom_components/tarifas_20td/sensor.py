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
from homeassistant.helpers.event import async_track_point_in_time, async_track_state_change_event
from homeassistant.helpers.restore_state import RestoreEntity
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

    # Instanciamos los sensores
    # 1. Sensor Maestro de Tramo Horario
    tramo_sensor = Tarifa20TDTramo(hass, config)
    
    # 2. Sensor de Balance Neto Horario
    balance_sensor = BalanceNetoHorario(hass, config)

    # 3. Sensores Acumulativos de Energía (Contadores kWh)
    # Estos sensores permitirán ver estadísticas diarias/mensuales en el panel de Energía
    energy_processor = EnergyProcessor(hass, config, tramo_sensor)

    async_add_entities([
        tramo_sensor, 
        balance_sensor,
        energy_processor.sensor_import_valle,
        energy_processor.sensor_import_llana,
        energy_processor.sensor_import_punta,
        energy_processor.sensor_export,
        energy_processor.sensor_home_consumption
    ])

# ------------------------------------------------------------------
# SENSOR 1: TRAMO HORARIO
# ------------------------------------------------------------------
class Tarifa20TDTramo(SensorEntity):
    """Sensor que determina el tramo actual (Valle, Llana, Punta)."""

    def __init__(self, hass, config):
        self._hass = hass
        self._config = config
        self._attr_name = "Tarifa 2.0TD Tramo Actual"
        self._attr_unique_id = f"{DOMAIN}_tramo_actual"
        self._attr_icon = "mdi:clock-time-four-outline"
        self._state = TRAMO_VALLE
        self._p_valle = config[CONF_POWER_VALLE]
        self._p_punta = config[CONF_POWER_PUNTA]
        self._workday_entity = config.get(CONF_WORKDAY)

    async def async_added_to_hass(self):
        """Iniciar loop de tiempo."""
        self._update_state()
        # Actualizar cada minuto
        self.async_on_remove(
            async_track_point_in_time(
                self._hass, self._timer_callback, dt_util.now().replace(second=0) + timedelta(minutes=1)
            )
        )

    async def _timer_callback(self, now):
        self._update_state()
        self.async_write_ha_state()
        # Reprogramar
        async_track_point_in_time(
            self._hass, self._timer_callback, now.replace(second=0) + timedelta(minutes=1)
        )

    def _update_state(self):
        now = dt_util.now()
        hour = now.hour
        
        # Lógica Workday
        is_holiday = False
        wd_state = self._hass.states.get(self._workday_entity)
        
        if wd_state is None:
             if now.weekday() >= 5: is_holiday = True # Fallback Sáb/Dom
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
# SENSOR 2: BALANCE NETO HORARIO
# ------------------------------------------------------------------
class BalanceNetoHorario(RestoreEntity, SensorEntity):
    """Balance que se resetea cada hora."""
    _attr_state_class = SensorStateClass.TOTAL
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_icon = "mdi:scale-balance"

    def __init__(self, hass, config):
        self._hass = hass
        self._grid_entity = config[CONF_GRID_SENSOR]
        self._attr_name = "Balance Neto Horario"
        self._attr_unique_id = f"{DOMAIN}_balance_neto"
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
        
        # Escuchar cambios en Grid
        self.async_on_remove(async_track_state_change_event(
            self._hass, [self._grid_entity], self._on_sensor_change
        ))
        # Reset horario
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
            power = float(new_state.state) # W (Positivo=Excedente, Negativo=Consumo)
        except ValueError: return

        now = dt_util.now()
        if self._last_update:
            hours_diff = (now - self._last_update).total_seconds() / 3600.0
            # Integral: W * h / 1000 = kWh
            energy = (power / 1000.0) * hours_diff
            self._state += energy
            
        self._last_update = now
        self.async_write_ha_state()

    @property
    def native_value(self):
        return round(self._state, 4)

# ------------------------------------------------------------------
# LÓGICA DE ENERGÍA Y SENSORES ACUMULATIVOS
# ------------------------------------------------------------------
class EnergyProcessor:
    """Clase helper para integrar potencia W a energía kWh y repartirla."""

    def __init__(self, hass, config, tramo_sensor):
        self.hass = hass
        self.tramo_sensor = tramo_sensor
        self.grid_entity = config[CONF_GRID_SENSOR]
        self.solar_entity = config[CONF_SOLAR_SENSOR]
        
        # Sensores Públicos
        self.sensor_import_valle = CumulativeEnergySensor(hass, "Energía Importada Valle", "import_valle")
        self.sensor_import_llana = CumulativeEnergySensor(hass, "Energía Importada Llana", "import_llana")
        self.sensor_import_punta = CumulativeEnergySensor(hass, "Energía Importada Punta", "import_punta")
        self.sensor_export = CumulativeEnergySensor(hass, "Energía Excedente Total", "export_total")
        self.sensor_home_consumption = CumulativeEnergySensor(hass, "Consumo Hogar Total", "home_total")
        
        self._last_update = None
        
        # Iniciar escucha
        hass.bus.async_listen_once("homeassistant_start", self._start_listening)

    async def _start_listening(self, _):
        self._last_update = dt_util.now()
        async_track_state_change_event(
            self.hass, [self.grid_entity, self.solar_entity], self._on_change
        )

    @callback
    def _on_change(self, event):
        """Calcula energía cuando cambian los Watios."""
        now = dt_util.now()
        if self._last_update is None: 
            self._last_update = now
            return
            
        # Obtener valores actuales
        try:
            grid_st = self.hass.states.get(self.grid_entity)
            solar_st = self.hass.states.get(self.solar_entity)
            
            grid_w = float(grid_st.state) if grid_st and grid_st.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) else 0.0
            solar_w = float(solar_st.state) if solar_st and solar_st.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) else 0.0
        except ValueError:
            return

        # Calcular tiempo
        hours = (now - self._last_update).total_seconds() / 3600.0
        self._last_update = now
        
        # --- LÓGICA DE CÁLCULO ---
        # Grid: + Excedente (Venta), - Consumo (Compra)
        # Solar: + Producción
        
        # 1. Energía Grid (Import/Export)
        energy_grid_kwh = (grid_w / 1000.0) * hours
        
        if energy_grid_kwh > 0:
            # Positivo = Excedente
            self.sensor_export.add_energy(energy_grid_kwh)
        else:
            # Negativo = Importación (convertimos a positivo para el contador)
            imported_kwh = abs(energy_grid_kwh)
            
            # Asignar al tramo correspondiente
            tramo = self.tramo_sensor.native_value
            if tramo == TRAMO_VALLE:
                self.sensor_import_valle.add_energy(imported_kwh)
            elif tramo == TRAMO_LLANA:
                self.sensor_import_llana.add_energy(imported_kwh)
            elif tramo == TRAMO_PUNTA:
                self.sensor_import_punta.add_energy(imported_kwh)
        
        # 2. Energía Consumo Hogar
        # Consumo = Solar - Grid(Inyección) + Grid(Importación)
        # Matemáticamente con tu signo: Consumo = Solar - Grid
        # Ej: Solar 1000, Grid +200 (sobra). Consumo = 1000 - 200 = 800. Correcto.
        # Ej: Solar 0, Grid -500 (falta). Consumo = 0 - (-500) = 500. Correcto.
        
        home_w = solar_w - grid_w
        # Evitar valores negativos raros por latencia de sensores
        if home_w < 0: home_w = 0 
        
        energy_home_kwh = (home_w / 1000.0) * hours
        self.sensor_home_consumption.add_energy(energy_home_kwh)


class CumulativeEnergySensor(RestoreEntity, SensorEntity):
    """Sensor genérico para contadores de energía que crecen siempre."""
    
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, hass, name, uid_suffix):
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{uid_suffix}"
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

    @property
    def native_value(self):
        return round(self._state, 4)
