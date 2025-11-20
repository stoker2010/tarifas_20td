# Tarifas 2.0TD para Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/stoker2010/tarifas_20td)](https://github.com/stoker2010/tarifas_20td/releases)
[![Maintainer](https://img.shields.io/badge/maintainer-stoker2010-blue)](https://github.com/stoker2010)

Esta integración personalizada proporciona una gestión integral de la estructura tarifaria eléctrica **2.0TD** vigente en España para Home Assistant. Está diseñada para usuarios que requieren un control preciso sobre sus costes energéticos y la gestión de excedentes de autoconsumo fotovoltaico.

---

# 🇪🇸 Documentación en Español

## 1. Descripción General y Funcionamiento Interno

El componente **Tarifas 2.0TD** actúa como un gestor lógico que se superpone a tus medidores de energía. Su núcleo de funcionamiento se basa en la discriminación horaria establecida por el BOE, permitiendo segmentar el consumo y la inyección de energía en los tres periodos oficiales: **Punta (P1), Llano (P2) y Valle (P3)**.

### Lógica de Funcionamiento
El sistema evalúa en cada cambio de estado (o intervalo de tiempo) las siguientes condiciones para determinar el periodo activo:
1.  **Hora del día:** Coteja la hora del sistema con las franjas horarias de la tarifa 2.0TD (Península/Canarias/Ceuta/Melilla).
2.  **Día de la semana:** Detecta automáticamente Sábados y Domingos para forzar el periodo **P3 (Valle)** las 24 horas.
3.  **Calendario de Festivos:** Se integra con calendarios locales o nacionales configurados en Home Assistant. Si el día actual es marcado como festivo nacional, el sistema fuerza el periodo **P3 (Valle)**, asegurando que la facturación simulada coincida con la real.

## 2. Variables de Configuración

Durante la instalación o configuración vía interfaz de usuario (UI), se pueden requerir los siguientes parámetros para adaptar el algoritmo a tu ubicación y contrato:

| Variable | Descripción |
| :--- | :--- |
| **Región / Zona Geográfica** | Define el huso horario y las particularidades festivas (Península, Canarias, Ceuta, Melilla). |
| **Sensor de Importación (Red)** | La entidad que mide la energía (kWh) consumida desde la red eléctrica. |
| **Sensor de Exportación (Solar)** | La entidad que mide la energía (kWh) inyectada a la red (excedentes). |
| **Potencia Contratada** | (Opcional) Permite establecer los límites de potencia para cálculos de costes fijos. |

## 3. Resultados: Entidades y Sensores Generados

Una vez configurada, la integración expone múltiples entidades en Home Assistant que se actualizan en tiempo real.

### A. Sensores de Estado
* **`sensor.periodo_actual`**: Muestra el periodo activo en ese instante (`P1`, `P2`, o `P3`). Ideal para condiciones en automatizaciones (ej: *Si periodo es P3, encender termo*).
* **`binary_sensor.es_festivo`**: Indica `on` si hoy es considerado festivo o fin de semana (tarifa reducida).

### B. Sensores de Energía y Balance
La integración desglosa tus sensores generales en contadores por periodo, esenciales para el panel de Energía de Home Assistant:

* **`sensor.energia_punta` / `llano` / `valle`**: Contadores acumulativos (kWh) del consumo en cada franja.
* **`sensor.excedentes_punta` / `llano` / `valle`**: Contadores acumulativos (kWh) de la inyección solar en cada franja.
* **`sensor.balance_neto_horario_estimado`**: Un sensor calculado avanzado que realiza el balance neto (Consumo - Inyección) según la normativa de compensación horaria, permitiendo estimar el coste real antes de impuestos.

---

# 🇺🇸 English Documentation

## 1. Overview and Internal Logic

The **Tarifas 2.0TD** custom integration provides comprehensive management of the **Spanish 2.0TD electricity tariff structure** within Home Assistant. It is designed for users who need precise control over energy costs and solar self-consumption surplus management.

### Internal Logic & Operation
The component acts as a logic layer on top of your physical energy meters. Its core function relies on the official Time-of-Use (ToU) periods defined by Spanish regulations (BOE), segmenting consumption and injection into three official periods: **Peak (P1), Flat (P2), and Off-Peak (P3)**.

1.  **Time Check:** It compares the system time against the 2.0TD time slots (Peninsula/Canary Islands).
2.  **Weekend Detection:** Automatically detects Saturdays and Sundays to force the **P3 (Off-Peak)** period for 24 hours.
3.  **Holiday Integration:** Connects with local or national calendars in Home Assistant. If the current day is flagged as a national holiday, the system forces the **P3 (Off-Peak)** period, ensuring simulated billing matches the utility bill.

## 2. Configuration Variables

During setup via the User Interface (UI), the following parameters define how the algorithm adapts to your location and contract:

| Variable | Description |
| :--- | :--- |
| **Region / Geographic Zone** | Defines the time zone and specific holiday rules (Peninsula, Canary Islands, etc.). |
| **Grid Import Sensor** | The entity measuring energy (kWh) consumed from the grid. |
| **Grid Export Sensor** | The entity measuring energy (kWh) injected into the grid (solar surplus). |
| **Contracted Power** | (Optional) Allows setting power limits for fixed cost calculations. |

## 3. Results: Generated Entities and Sensors

Once configured, the integration exposes multiple entities in Home Assistant updated in real-time.

### A. Status Sensors
* **`sensor.periodo_actual` (Current Period)**: Shows the active period (`P1`, `P2`, or `P3`). Perfect for automation conditions (e.g., *If period is P3, turn on water heater*).
* **`binary_sensor.es_festivo` (Is Holiday)**: Returns `on` if today is considered a holiday or weekend (reduced tariff).

### B. Energy and Balance Sensors
The integration breaks down your general sensors into period-specific counters, essential for the Home Assistant Energy Dashboard:

* **`sensor.energia_punta` / `llano` / `valle`**: Cumulative counters (kWh) for grid consumption in each slot.
* **`sensor.excedentes_punta` / `llano` / `valle`**: Cumulative counters (kWh) for solar injection in each slot.
* **`sensor.balance_neto_horario_estimado`**: An advanced calculated sensor that performs net metering (Import - Export) according to hourly compensation regulations, allowing for a real cost estimation before taxes.

---

## ⚙️ Instalación / Installation

1.  **HACS:** Search for `Tarifas 2.0TD` in HACS and install.
2.  **Restart:** Restart Home Assistant.
3.  **Configure:** Go to **Settings > Devices & Services > Add Integration** and search for **Tarifas 2.0TD**.

---

### 🙌 Agradecimientos y Créditos

Esta integración ha sido inspirada y desarrollada gracias a la gran comunidad de Home Assistant en español.

**Divulgación y Tutoriales**
Un agradecimiento especial a los canales que, con sus excelentes tutoriales, hacen posible que aprendamos y mejoremos nuestros hogares inteligentes:

🎥 @domotica_solar
🎥 @proyectosmicropic
🎥 @unlocoysutecnologia
🎥 @HomeAssistantFacil
🎥 @MiguelAngelLV
