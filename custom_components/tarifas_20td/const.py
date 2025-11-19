"""Constantes para Tarifas 2.0TD."""

DOMAIN = "tarifas_20td"

# Nombres de claves de configuración (Internal Keys)
# Estos coinciden ahora con los nombres solicitados en la v0.6.3
CONF_GRID_SENSOR = "sensor_energia_grid"
CONF_SOLAR_SENSOR = "sensor_produccion_solar"
CONF_POWER_VALLE = "potencia_contratada_valle"
CONF_POWER_PUNTA = "potencia_contratada_punta"
CONF_WORKDAY = "dias_laborables"

# Configuración Termo
CONF_TERMO_SWITCH = "interruptor_termo_electrico"
CONF_TERMO_TEMP_SENSOR = "temperatura_termo_electrico"
CONF_TERMO_POWER_SENSOR = "sensor_consumo_termo_electrico"
CONF_TERMO_NOMINAL_POWER = "potencia_maxima_termo"

# Tramos
TRAMO_VALLE = "Valle"
TRAMO_PUNTA = "Punta"
TRAMO_LLANA = "Llana"
