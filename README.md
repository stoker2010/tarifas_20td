# Tarifas 2.0TD y Balance Neto (Batería Virtual)

![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)

Integración personalizada ("todo en uno") para Home Assistant que gestiona los tramos horarios de España (2.0TD), calcula el Balance Neto Horario y genera contadores de energía para el control de excedentes y consumo.

## Características
* 🕒 **Sensor de Tramo 2.0TD:** Detecta automáticamente Valle, Llana y Punta (incluyendo festivos nacionales/locales mediante la integración Workday).
* ⚖️ **Balance Neto Horario:** Calcula el saldo de energía (kWh) y se reinicia a 0 cada hora en punto.
* 📊 **Contadores de Energía:** Genera sensores acumulativos (`total_increasing`) listos para usarse en el Panel de Energía de HA.

## 🚀 Instalación

1. **Requisito:** Tener instalada y configurada la integración oficial [Workday](https://www.home-assistant.io/integrations/workday/) (Día Laborable).
2. Añade este repositorio a HACS como **Repositorio Personalizado** (Categoría: Integración).
3. Busca "Tarifas España 2.0TD & Balance" e instálalo.
4. Reinicia Home Assistant.

## ⚙️ Configuración

Esta integración se configura **visualmemente** desde la interfaz de Home Assistant:

1. Ve a **Ajustes** > **Dispositivos y servicios**.
2. Pulsa **Añadir Integración**.
3. Busca **Tarifas 2.0TD**.
4. Rellena los datos solicitados:
   - **Sensor Grid (Red):** Debe ser POSITIVO (+) cuando viertes excedentes y NEGATIVO (-) cuando consumes de la calle.
   - **Sensor Solar:** Producción solar (siempre positivo).
   - **Potencias:** Tu potencia contratada en Valle y Punta.
   - **Entidad Workday:** Normalmente `binary_sensor.workday_sensor`.

## 📊 Sensores Generados

### Gestión
* `sensor.tarifa_2_0td_tramo_actual`: Estado actual (valle/llana/punta). Atributos con la potencia contratada vigente.
* `sensor.balance_neto_horario`: kWh netos en la hora actual (reset a XX:00).

### Estadísticas (Compatibles con Panel de Energía)
La integración crea sensores acumulativos. Para ver los datos **Diarios, Semanales, Mensuales y Anuales**, simplemente añade estos sensores al **Panel de Energía** o usa tarjetas de estadísticas:

* `sensor.energia_importada_valle`
* `sensor.energia_importada_llana`
* `sensor.energia_importada_punta`
* `sensor.energia_excedente_total`
* `sensor.consumo_hogar_total`

---
Desarrollado por [@stoker2010](https://github.com/stoker2010)
