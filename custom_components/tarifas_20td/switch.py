"""Plataforma Switch para Tarifas 2.0TD (Termo)."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar entidades Switch."""

    device_info_termo = DeviceInfo(
        identifiers={(DOMAIN, f"{entry.entry_id}_termo")},
        name="Termo Eléctrico",
        manufacturer="@stoker2010",
        model="Control Termo v1",
        via_device=(DOMAIN, entry.entry_id),
    )

    async_add_entities([
        TermoConfigSwitch(hass, "Cargar con Excedentes", "charge_surplus", "mdi:solar-power", device_info_termo),
        TermoConfigSwitch(hass, "Limitar carga exc. a Temp Max", "limit_surplus_temp", "mdi:thermometer-check", device_info_termo),
        TermoConfigSwitch(hass, "Límite Temperatura Máxima", "limit_max_temp", "mdi:thermometer-alert", device_info_termo),
    ])

class TermoConfigSwitch(SwitchEntity):
    """Interruptor de configuración genérico."""

    def __init__(self, hass, name, uid_suffix, icon, device_info):
        self._hass = hass
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_termo_{uid_suffix}"
        self._attr_icon = icon
        self._attr_device_info = device_info
        self._attr_is_on = False # Por defecto apagado

    async def async_turn_on(self, **kwargs):
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._attr_is_on = False
        self.async_write_ha_state()
