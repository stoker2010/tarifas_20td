"""Constantes para la integración Tarifas 2.0TD."""

DOMAIN = "tarifas_20td"

# Opciones de Menú
MENU_OPTION_CASA = "casa"
MENU_OPTION_TERMO = "termo"

# Tipos de configuración
CONF_TYPE = "config_type"
TYPE_CASA = "type_casa"
TYPE_TERMO = "type_termo"

# Variables Casa
CONF_ENERGY_SENSOR_IMPORT = "energy_sensor_import"
CONF_ENERGY_SENSOR_EXPORT = "energy_sensor_export"
CONF_POWER_CONTRACTED = "power_contracted"
CONF_ZONE = "zone"

# Variables Termo
CONF_TERMO_ENTITY = "termo_entity" # El interruptor real (ej: switch.shelly...)
CONF_TEMP_SENSOR = "temp_sensor"   # El sensor de temperatura real

# Valores por defecto
DEFAULT_NAME = "Tarifas 2.0TD"
