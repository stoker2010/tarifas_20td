"""Plataforma Number para Tarifas 2.0TD (Termo)."""
from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar entidades Number."""
    
    # Dispositivo Termo
    device_info_termo = DeviceInfo(
        identifiers={(DOMAIN, f"{entry.entry_id}_termo")},
        name="Termo Eléctrico",
        manufacturer="@stoker2010",
        model="Control Termo v1",
        via_device=(DOMAIN, entry.entry_id), # Vinculado al Hogar
    )

    async_add_entities([
        TermoMaxTempNumber(hass, device_info_termo)
    ])

class TermoMaxTempNumber(NumberEntity):
    """Seleccion de Temperatura Máxima Objetivo."""
    _attr_native_min_value = 35
    _attr_native_max_value = 60
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:thermometer-water"

    def __init__(self, hass, device_info):
        self._hass = hass
        self._attr_device_info = device_info
        self._attr_name = "Temperatura Objetivo Termo"
        self._attr_unique_id = f"{DOMAIN}_termo_target_temp"
        self._attr_native_value = 45 # Valor por defecto

    async def async_set_native_value(self, value: float) -> None:
        """Guardar el valor."""
        self._attr_native_value = value
        self.async_write_ha_state()
