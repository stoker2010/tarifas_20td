# Integración Sensor Tarifas 2.0TD

Este componente personalizado añade un sensor a Home Assistant que indica automáticamente el periodo tarifario actual (Punta, Llana o Valle) según la normativa española.

## Instalación

1. Añade este repositorio a HACS como **Integración Personalizada**.
2. Reinicia Home Assistant.

## Configuración

Añade lo siguiente a tu archivo `configuration.yaml`. 
Si no usas la integración `Workday`, el sensor usará solo sábados y domingos como festivos.

```yaml
sensor:
  - platform: tarifas_20td
    name: "Tarifa Electricidad"
    # Opcional: Entidad que indica si es día laborable (por defecto: binary_sensor.workday_sensor)
    workday_entity: binary_sensor.workday_sensor
