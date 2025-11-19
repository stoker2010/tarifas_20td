# Integración Tarifas 2.0TD España

Esta integración crea un sensor en Home Assistant que indica la tarifa eléctrica actual (Punta, Llana, Valle) según el horario español 2.0TD.

## Instalación mediante HACS

1. Añade este repositorio como "Repositorio Personalizado" en HACS.
2. Instala la integración "Tarifa Eléctrica España 2.0TD".
3. Reinicia Home Assistant.

## Configuración

Añade esto a tu archivo `configuration.yaml`:

```yaml
sensor:
  - platform: tarifas_20td
    name: "Tarifa Electricidad"
    workday_entity: binary_sensor.workday_sensor # Opcional, por defecto es este
