# Tarifas 2.0TD para Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/stoker2010/tarifas_20td)](https://github.com/stoker2010/tarifas_20td/releases)
[![Maintainer](https://img.shields.io/badge/maintainer-stoker2010-blue)](https://github.com/stoker2010)

Esta integración personalizada permite gestionar y visualizar de forma sencilla la información de la tarifa eléctrica española **2.0TD** en Home Assistant. Está diseñada para facilitar el control del gasto energético y la gestión de excedentes fotovoltaicos.

---

### 🇪🇸 Descripción

**Tarifas 2.0TD** automatiza la identificación de los periodos de facturación eléctrica en España. La integración calcula en tiempo real qué periodo está activo (Punta, Llano o Valle) tanto para el consumo de energía como para la potencia contratada, teniendo en cuenta fines de semana y festivos nacionales y autonómicos.

**Características principales:**
* **Detección automática de periodos:** P1 (Punta), P2 (Llano) y P3 (Valle).
* **Gestión de festivos:** Integra el calendario laboral para ajustar los periodos correctamente.
* **Sensores dedicados:** Crea sensores para el precio actual, el periodo activo y balances de energía.
* **Ideal para Fotovoltaica:** Facilita la creación de automatizaciones para inyectar excedentes o consumir energía en los momentos más económicos.

---

### 🇺🇸 Description

**Tarifas 2.0TD** is a custom integration for Home Assistant designed to manage the Spanish **2.0TD electricity tariff structure**. It simplifies energy cost tracking and solar surplus management by automatically identifying the current billing period.

**Key Features:**
* **Automatic Period Detection:** Identifies active energy periods: P1 (Peak), P2 (Flat), and P3 (Off-peak).
* **Holiday Awareness:** Automatically adjusts billing periods based on national and regional public holidays in Spain.
* **Real-time Sensors:** Provides sensors for current electricity prices, active periods, and energy balances.
* **Solar PV Optimization:** Perfect for users with solar panels, allowing for better decision-making on when to consume or inject energy into the grid.

---

### 🇫🇷 Description (Court)

Intégration pour gérer le tarif d'électricité espagnol **2.0TD** dans Home Assistant. Elle identifie automatiquement les périodes de facturation (Pointe, Pleine, Creuse) et prend en compte les jours fériés pour optimiser votre consommation et la gestion de vos panneaux solaires.

---

### 🇨🇳 描述 (简体中文)

Home Assistant 的自定义集成，用于管理西班牙 **2.0TD** 电费关税。它根据西班牙的日历和节假日自动识别当前的计费时段（高峰、平段、低谷），非常适合优化能源消耗和太阳能光伏管理。

---

## ⚙️ Instalación

1. Instala esta integración a través de **HACS** (Home Assistant Community Store).
2. Busca `Tarifas 2.0TD` en la sección de Integraciones.
3. Haz clic en `Descargar`.
4. Reinicia Home Assistant.

## 🛠️ Configuración

Una vez instalada, puedes configurar la integración a través de la interfaz de usuario (UI) de Home Assistant:

1. Ve a **Ajustes** -> **Dispositivos y servicios**.
2. Haz clic en **Añadir integración**.
3. Busca **Tarifas 2.0TD** y sigue los pasos del asistente.

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
