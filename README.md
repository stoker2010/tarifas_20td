# Tarifas España 2.0TD & Balance Neto

[![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)](https://github.com/stoker2010/tarifas_20td/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40stoker2010-blue.svg)](https://github.com/stoker2010)

**[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English Description

This Home Assistant Custom Component manages **Spanish 2.0TD electricity tariff periods**, calculates the **Hourly Net Balance** (Virtual Battery) in real-time, and provides **Daily Energy Counters**.

It is designed to simplify energy management for users with solar panels in Spain, providing estimated projections and daily statistics ready for the Home Assistant dashboard.

### ✨ Features

* **Automatic 2.0TD Periods:** Detects **Peak (Punta)**, **Flat (Llana)**, and **Off-peak (Valle)** periods automatically.
* **Holidays Support:** Fully integrated with the official **[Workday](https://www.home-assistant.io/integrations/workday/)** integration.
* **Hourly Net Balance:**
    * **Real:** Calculates the accumulated net balance (kWh) and resets to 0 at XX:00.
    * **Estimated:** Projects how the hour will end based on current instantaneous power.
* **Daily Energy Counters:** Tracks Imports (per period), Exports, and Home Consumption. **Resets automatically at 00:00 every night.**

### 🚀 Installation

1.  **Prerequisite:** You must have the **[Workday](https://www.home-assistant.io/integrations/workday/)** integration installed and configured in Home Assistant.
2.  Add this repository to **HACS** as a **Custom Repository**:
    * URL: `https://github.com/stoker2010/tarifas_20td`
    * Category: `Integration`
3.  Click **Install** in HACS and restart Home Assistant.

### ⚙️ Configuration

This integration supports **Config Flow** (UI Configuration). No YAML is needed.

1.  Go to **Settings** > **Devices & Services**.
2.  Click **+ Add Integration** and search for **Tarifas España 2.0TD**.
3.  Fill in the required fields:
    * **Grid Sensor (Watts):**
        * Positive value (+) = Surplus/Export (Sending energy to the grid).
        * Negative value (-) = Consumption (Pulling energy from the grid).
    * **Solar Sensor (Watts):** Solar production (always positive).
    * **Contracted Power:** Your power limit for Valle and Punta (in Watts).
    * **Workday Entity:** Usually `binary_sensor.workday_sensor`.

### 📊 Created Sensors

* **Management:**
    * `sensor.tarifa_20td_tramo_actual`: Current period (`valle`, `llana`, `punta`).
    * `sensor.balance_neto_horario_real`: Net kWh accumulated in the current hour (Resets at start of hour).
    * `sensor.balance_neto_horario_estimado`: **Projection** of the hourly balance at the end of the hour based on current power.

* **Daily Energy Counters (Reset at 00:00):**
    * `sensor.energia_importada_valle_diario`
    * `sensor.energia_importada_llana_diario`
    * `sensor.energia_importada_punta_diario`
    * `sensor.energia_excedente_diario`
    * `sensor.consumo_hogar_diario` (Calculated: Solar + Import - Export).

### 🙌 Acknowledgements

Thanks to the YouTube channels of Luis **[@domotica_solar](https://www.youtube.com/@domotica_solar)** and Manolo **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)**, from whom I copied the automations and drew inspiration.

And also to **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** who has two very similar integrations: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** and **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración personalizada para Home Assistant gestiona los **tramos horarios de la tarifa eléctrica española 2.0TD**, calcula el **Balance Neto Horario** (Batería Virtual) y ofrece **Contadores Diarios de Energía**.

Está diseñada para simplificar la gestión energética de usuarios con placas solares en España, ofreciendo proyecciones de cierre de hora y estadísticas diarias automáticas.

### ✨ Características Principales

* **Control Automático 2.0TD:** Detecta automáticamente los periodos **Punta**, **Llana** y **Valle** según la hora del día.
* **Soporte de Festivos:** Se integra con la integración oficial **[Workday](https://www.home-assistant.io/integrations/workday/)** para detectar fines de semana y festivos.
* **Balance Neto Horario:**
    * **Real:** Saldo neto de energía (kWh) acumulado en la hora actual. Se reinicia a 0 cada hora en punto (XX:00).
    * **Estimado:** Proyección de cómo acabará el saldo de la hora basándose en la potencia instantánea actual.
* **Contadores Diarios:** Sensores de energía (Importación por tramos, Excedentes y Consumo Hogar) que **se reinician automáticamente a las 00:00 cada noche**.

### 🚀 Instalación

1.  **Requisito:** Debes tener instalada y configurada la integración oficial **[Workday](https://www.home-assistant.io/integrations/workday/)** en Home Assistant.
2.  Añade este repositorio a **HACS** como **Repositorio Personalizado**:
    * URL: `https://github.com/stoker2010/tarifas_20td`
    * Categoría: `Integración`
3.  Pulsa **Descargar** en HACS y reinicia Home Assistant.

### ⚙️ Configuración

Esta integración se configura visualmente desde la interfaz de usuario (UI). No hace falta tocar ficheros YAML.

1.  Ve a **Ajustes** > **Dispositivos y servicios**.
2.  Pulsa **+ Añadir integración** y busca **Tarifas España 2.0TD**.
3.  Rellena los datos solicitados:
    * **Sensor de Red (Grid) en Watios:**
        * Valor Positivo (+) = Excedente (Venta/Inyección a la red).
        * Valor Negativo (-) = Consumo (Compra de la red).
    * **Sensor Solar en Watios:** Producción solar (siempre positivo).
    * **Potencias Contratadas:** Tu potencia en Valle y Punta (en Watios).
    * **Entidad Workday:** Normalmente `binary_sensor.workday_sensor`.

### 📊 Sensores Generados

* **Gestión:**
    * `sensor.tarifa_20td_tramo_actual`: Estado actual (`valle`, `llana`, `punta`).
    * `sensor.balance_neto_horario_real`: kWh netos acumulados en la hora en curso (Reset XX:00).
    * `sensor.balance_neto_horario_estimado`: **Estimación** de cierre de hora según tu consumo/producción actual.

* **Contadores Diarios (Reset a las 00:00):**
    * `sensor.energia_importada_valle_diario`
    * `sensor.energia_importada_llana_diario`
    * `sensor.energia_importada_punta_diario`
    * `sensor.energia_excedente_diario`
    * `sensor.consumo_hogar_diario` (Calculado: Solar + Importado - Exportado).

### 🙌 Agradecimientos

Agradecimiento a los canales de YouTube de Luis **[@domotica_solar](https://www.youtube.com/@domotica_solar)** y Manolo **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)**, de los que copié las automatizaciones y en los que me he inspirado.

Y también a **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** que tiene dos integraciones muy parecidas: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** y **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---
<p align="center">
  Desarrollado por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
