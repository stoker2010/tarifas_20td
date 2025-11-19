"""Constantes para la integración Tarifas 2.0TD."""

DOMAIN = "tarifas_20td"

# Configuración Hogar
CONF_GRID_SENSOR = "grid_sensor"
CONF_SOLAR_SENSOR = "solar_sensor"
CONF_POWER_VALLE = "power_valle"
CONF_POWER_PUNTA = "power_punta"
CONF_WORKDAY = "workday_entity"

# Configuración Termo
CONF_TERMO_SWITCH = "termo_switch"
CONF_TERMO_TEMP_SENSOR = "termo_temp_sensor"
CONF_TERMO_POWER_SENSOR = "termo_power_sensor"
CONF_TERMO_NOMINAL_POWER = "termo_nominal_power"

DEFAULT_WORKDAY = "binary_sensor.workday_sensor"

# Tramos
TRAMO_VALLE = "valle"
TRAMO_LLANA = "llana"
TRAMO_PUNTA = "punta"
