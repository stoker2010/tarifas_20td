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

* **Automatic 2.0TD Periods:** Detects **Peak (Punta)**, **Flat (Llana)**, and **Off-peak (Valle)**.
* **Holidays Support:** Fully integrated with the official **[Workday](https://www.home-assistant.io/integrations/workday/)** integration.
* **Hourly Net Balance:**
    * **Real:** Resets to 0 at XX:00.
    * **Estimated:** Projected balance for the end of the hour.
* **Surplus Current:** Calculates available Amps (at 240V) if the estimated balance is positive. **Updates every 5 minutes.**
* **Daily Counters:** Energy sensors reset at 00:00. Tracks Imports (Total & per period), Exports, and Home Consumption.

### 🚀 Installation & Config

1.  Install via **HACS** (Custom Repository).
2.  Add integration via **Settings > Devices & Services**.
3.  Configure Grid/Solar sensors and Contracted Power.

### 📊 Sensors

* `sensor.intensidad_excedente`: Amps available (240V). Updates every 5 minutes.
* `sensor.balance_neto_horario_estimado`: Projected kWh.
* `sensor.energia_importada_total_diario`: **Total** daily imported energy (24h).
* `sensor.energia_importada_[tramo]_diario`: Daily import counters per period (Billable consumption).
* `sensor.energia_excedente_diario`: Daily export.
* `sensor.consumo_hogar_diario`: Daily home consumption.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración gestiona los **tramos horarios 2.0TD**, calcula el **Balance Neto Horario** (Batería Virtual) y ofrece **Contadores Diarios** y cálculo de **Intensidad Excedente**.

### ✨ Características Principales

* **Control 2.0TD:** Punta, Llana y Valle automáticos (con festivos).
* **Balance Neto Horario:**
    * **Real:** kWh netos acumulados en la hora (Reset XX:00).
    * **Estimado:** Proyección de cierre de hora según potencia actual.
* **Intensidad Excedente:** Te indica cuántos Amperios (240V) te sobran. **Se actualiza estrictamente cada 5 minutos** para evitar fluctuaciones rápidas.
* **Contadores Diarios:** Sensores de energía (Importación Total y por Tramos, Excedentes y Consumo Hogar) que se ponen a 0 cada noche.

### 🚀 Instalación y Configuración

1.  Instala vía **HACS** (Repositorio Personalizado).
2.  Añade la integración desde **Ajustes > Dispositivos y Servicios**.
3.  Configura tus sensores de Red/Solar y potencias.

### 📊 Sensores Generados

* `sensor.intensidad_excedente`: Amperios disponibles (a 240V). **Actualiza cada 5 min.**
* `sensor.balance_neto_horario_estimado`: Estimación de fin de hora.
* `sensor.energia_importada_total_diario`: Total de energía importada de la red hoy (24h).
* `sensor.energia_importada_[tramo]_diario`: Contadores diarios por tramo (Consumo de la calle, lo que pagas).
* `sensor.energia_excedente_diario`: Excedente diario total.
* `sensor.consumo_hogar_diario`: Consumo de casa diario.

### 🙌 Agradecimientos

Agradecimiento a los canales de YouTube de Luis **[@domotica_solar](https://www.youtube.com/@domotica_solar)** y Manolo **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)**, de los que copié las automatizaciones y en los que me he inspirado.

Y también a **[@MiguelAngelLV](https://github.com/MiguelAngelLV)** que tiene dos integraciones muy parecidas: **[ha-tarifa-20td](https://github.com/MiguelAngelLV/ha-tarifa-20td)** y **[ha-balance-neto](https://github.com/MiguelAngelLV/ha-balance-neto)**.

---
<p align="center">
  Desarrollado por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
