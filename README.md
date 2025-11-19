# Tarifas España 2.0TD & Balance Neto

[![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)](https://github.com/stoker2010/tarifas_20td/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40stoker2010-blue.svg)](https://github.com/stoker2010)

**[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English Description

This Home Assistant Custom Component manages **Spanish 2.0TD electricity tariff periods**, calculates the **Hourly Net Balance** (Virtual Battery), and provides **Daily Energy Counters** and **Surplus Current** estimation.

### ✨ Features

* **Hourly Net Balance:**
    * **Real:** Resets to 0 at XX:00.
    * **Estimated:** Projected balance for the end of the hour.
* **Surplus Current (Smart):** Calculates available Amps (at 240V) to finish the hour with exactly 0 kWh balance. **Updates every 5 minutes.**
* **Daily Counters:** Energy sensors reset at 00:00. Tracks Total Imports, Exports, and Home Consumption.

### 🚀 Installation & Config

1.  Install via **HACS** (Custom Repository).
2.  Add integration via **Settings > Devices & Services**.
3.  Configure Grid/Solar sensors and Contracted Power.

### 📊 Sensors

* `sensor.intensidad_excedente`: Amps available to use (calculated at 240V) to finish the hour at 0 balance. (Updates every 5 min).
* `sensor.balance_neto_horario_estimado`: Projected kWh.
* `sensor.energia_importada_total_diario`: **Total** daily imported energy (24h).
* `sensor.energia_excedente_diario`: Daily export.
* `sensor.consumo_hogar_diario`: Daily home consumption.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración gestiona los **tramos horarios 2.0TD**, calcula el **Balance Neto Horario** (Batería Virtual) y ofrece **Contadores Diarios** y cálculo de **Intensidad Excedente Inteligente**.

### ✨ Características Principales

* **Balance Neto Horario:**
    * **Real:** kWh netos acumulados en la hora (Reset XX:00).
    * **Estimado:** Proyección de cierre de hora.
* **Intensidad Excedente (Smart):** Calcula cuántos Amperios (240V) puedes consumir **ahora** para terminar la hora con el balance a 0 exacto. **Se actualiza cada 5 minutos.**
* **Contadores Diarios (Reset 00:00):** Importación Total, Excedentes y Consumo.

### 🚀 Instalación y Configuración

1.  Instala vía **HACS** (Repositorio Personalizado).
2.  Añade la integración desde **Ajustes > Dispositivos y Servicios**.
3.  Configura tus sensores de Red/Solar y potencias.

### 📊 Sensores Generados

* `sensor.intensidad_excedente`: Amperios disponibles (a 240V) para encender cargas y terminar la hora en 0 kWh (Actualizado cada 5 min).
* `sensor.balance_neto_horario_estimado`: Estimación de fin de hora.
* `sensor.energia_importada_total_diario`: Total de energía importada de la red hoy (24h).
* `sensor.energia_excedente_diario`: Excedente diario total.
* `sensor.consumo_hogar_diario`: Consumo de casa diario.

### 🙌 Agradecimientos

Agradecimiento a los canales de YouTube de Luis **[@domotica_solar](https://www.youtube.com/@domotica_solar)** y Manolo **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)**, de los que copié las automatizaciones y en los que me he inspirado.

Y también a **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** que tiene dos integraciones muy parecidas: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** y **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---
<p align="center">
  Desarrollado por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
