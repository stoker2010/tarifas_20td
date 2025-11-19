# Tarifas España 2.0TD & Balance Neto

[![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)](https://github.com/stoker2010/tarifas_20td/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40stoker2010-blue.svg)](https://github.com/stoker2010)

**[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English Description

This Home Assistant Custom Component manages **Spanish 2.0TD electricity tariff periods** and calculates the **Hourly Net Balance** (Virtual Battery) in real-time.

It is designed to simplify energy management for users with solar panels in Spain, providing "Total Increasing" energy sensors ready to be used in the Home Assistant **Energy Dashboard**.

### ✨ Features

* **Automatic 2.0TD Periods:** Detects **Peak (Punta)**, **Flat (Llana)**, and **Off-peak (Valle)** periods automatically.
* **Holidays Support:** Fully integrated with the official **[Workday](https://www.home-assistant.io/integrations/workday/)** integration to detect national and local holidays (applying Off-peak/Valle tariff accordingly).
* **Hourly Net Balance:** Calculates the net energy balance (kWh) and automatically resets to 0 at the beginning of every hour (XX:00), essential for "Virtual Battery" calculations.
* **Energy Dashboard Ready:** Automatically generates cumulative energy sensors (`state_class: total_increasing`) for imports (per period) and exports.

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
    * `sensor.tarifa_20td_tramo_actual`: Current period (`valle`, `llana`, `punta`). Attributes include current contracted power.
    * `sensor.balance_neto_horario`: Net kWh for the current hour. Resets at start of hour.

* **Energy Counters (Accumulated kWh):**
    * `sensor.energia_importada_valle`
    * `sensor.energia_importada_llana`
    * `sensor.energia_importada_punta`
    * `sensor.energia_excedente_total`
    * `sensor.consumo_hogar_total` (Calculated: Solar + Import - Export).

### 🙌 Acknowledgements

Thanks to the YouTube channels of Luis **@domotica_solar** and Manolo **@proyectosmicropic**, from whom I copied the automations and drew inspiration.

And also to **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** who has two very similar integrations: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** and **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración personalizada para Home Assistant gestiona los **tramos horarios de la tarifa eléctrica española 2.0TD** y calcula el **Balance Neto Horario** (Batería Virtual) en tiempo real.

Está diseñada para simplificar la gestión energética de usuarios con placas solares en España, generando sensores de energía acumulativos listos para usar en el **Panel de Energía** de Home Assistant.

### ✨ Características Principales

* **Control Automático 2.0TD:** Detecta automáticamente los periodos **Punta**, **Llana** y **Valle** según la hora del día.
* **Soporte de Festivos:** Se integra con la integración oficial **[Workday](https://www.home-assistant.io/integrations/workday/)** para detectar fines de semana y festivos (nacionales o locales), aplicando la tarifa Valle automáticamente.
* **Balance Neto Horario:** Calcula el saldo neto de energía (kWh) y se reinicia a 0 automáticamente al inicio de cada hora (XX:00).
* **Panel de Energía:** Genera sensores de energía acumulativos (`state_class: total_increasing`) para importación (por tramos) y exportación, listos para el dashboard oficial de HA.

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
    * `sensor.tarifa_20td_tramo_actual`: Estado actual (`valle`, `llana`, `punta`). Incluye atributos con la potencia contratada vigente.
    * `sensor.balance_neto_horario`: kWh netos de la hora en curso. Se resetea cada hora en punto.

* **Contadores de Energía (Acumulados kWh):**
    * `sensor.energia_importada_valle`
    * `sensor.energia_importada_llana`
    * `sensor.energia_importada_punta`
    * `sensor.energia_excedente_total`
    * `sensor.consumo_hogar_total` (Calculado: Solar + Importado - Exportado).

### 🙌 Agradecimientos

Agradecimiento a los canales de YouTube de Luis **@domotica_solar** y Manolo **@proyectosmicropic**, de los que copié las automatizaciones y en los que me he inspirado.

Y también a **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** que tiene dos integraciones muy parecidas: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** y **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---
<p align="center">
  Desarrollado por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
