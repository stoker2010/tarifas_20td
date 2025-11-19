# Tarifas España 2.0TD & Balance Neto

[![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)](https://github.com/stoker2010/tarifas_20td/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40stoker2010-blue.svg)](https://github.com/stoker2010)

**[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English Description

This Home Assistant Custom Component manages **Spanish 2.0TD electricity tariff periods**, calculates the **Hourly Net Balance** (Virtual Battery), provides **Daily Energy Counters**, and now includes a dedicated **Electric Water Heater (Termo) Manager**.

### ✨ Features

* **Two Devices Created:**
    1.  **Hogar (Home):** Main energy manager (2.0TD, Net Balance, Daily Counters).
    2.  **Termo Eléctrico (Water Heater):** Dedicated controls for your water heater.
* **Hourly Net Balance:** Real & Estimated calculations (Resets at XX:00).
* **Zero Export Current (Bidirectional):** Calculates Amps (at 240V) to finish the hour at 0 balance (+ Surplus / - Deficit).
* **Termo Controls:**
    * Target Temperature Slider (35-60ºC).
    * Configuration Switches (Surplus Charge, Limit to Max Temp, etc.).
* **Daily Counters:** Total Import, Export, Consumption (Reset at 00:00).

### 🚀 Installation & Config

1.  Install via **HACS**.
2.  Add integration via **Settings > Devices & Services**.
3.  **New (v0.6.3):** You will be asked for simplified inputs:
    * **Sensor Energía Grid** (Grid Power)
    * **Sensor Producción Solar** (Solar Power)
    * **Potencia Contratada** (Valle/Punta)
    * **Días Laborables** (Workday entity)
    * **Termo Data:** Switch, Temp Sensor, Power Sensor, and Max Power.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración gestiona los **tramos horarios 2.0TD**, calcula el **Balance Neto Horario** y ahora incluye un **Gestor de Termo Eléctrico**.

### ✨ Características Principales

* **Dos Dispositivos:**
    1.  **Hogar:** Gestor principal (Tarifas, Balance, Excedentes).
    2.  **Termo Eléctrico:** Nuevo dispositivo con controles específicos.
* **Balance Neto Horario:** Real y Estimado (Reset XX:00).
* **Intensidad Vertido 0:** Amperios (+/-) necesarios para acabar la hora en 0 kWh.
* **Controles del Termo:**
    * Slider de Temperatura Objetivo (35-60ºC).
    * Interruptores de configuración (Carga con excedentes, Límites, etc.).
* **Contadores Diarios:** Importación Total, Excedentes y Consumo (Reset 00:00).

### 🚀 Instalación

1.  Instala vía **HACS**.
2.  Configura desde **Dispositivos y Servicios**.
3.  **Nuevo (v0.6.3):** Formulario renovado con nombres más claros:
    * **Sensor Energía Grid**: Tu sensor de consumo de red (W).
    * **Sensor Producción Solar**: Tu sensor de inversor (W).
    * **Potencia Contratada en Valle / Punta**.
    * **Días Laborables**: Entidad `workday` (para festivos).
    * **Datos del Termo**: Interruptor, Temperatura, Sensor Consumo y Potencia Máxima.

### 🙌 Agradecimientos

Agradecimiento a los canales de YouTube de Luis **[@domotica_solar](https://www.youtube.com/@domotica_solar)** y Manolo **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)**.
Y también a **[@MiguelAngelLV](https://github.com/MiguelAngelLV)**.

---
<p align="center">
  Desarrollado por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
