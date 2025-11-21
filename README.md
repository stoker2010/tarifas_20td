# Tarifas Eléctricas 20TD 🇪🇸

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub version](https://img.shields.io/github/v/release/stoker2010/tarifas_20td?style=for-the-badge&color=blue)](https://github.com/stoker2010/tarifas_20td/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/stoker2010/tarifas_20td/graphs/commit-activity)

**Tarifas 20TD** es un componente personalizado para **Home Assistant** que permite integrar y visualizar los periodos de facturación eléctrica en España (Punta, Llano, Valle) y precios asociados, facilitando el ahorro energético mediante automatizaciones inteligentes.

---

## ✨ Características

* 📊 **Monitorización en tiempo real**: Conoce el periodo tarifario actual al instante.
* 📅 **Gestión de Festivos**: Detecta automáticamente fines de semana y festivos nacionales para aplicar la tarifa Valle.
* 🔌 **Integración sencilla**: Compatible con la configuración estándar de sensores de Home Assistant.
* ⚡ **Optimizado**: Código ligero y eficiente (Basado en v0.6.0 Stable).

---

## 🚀 Instalación

### Opción 1: A través de HACS (Recomendado)

1.  Asegúrate de tener [HACS](https://hacs.xyz/) instalado.
2.  Ve a **HACS** > **Integraciones**.
3.  En el menú de los 3 puntos (arriba a la derecha), selecciona **"Repositorios personalizados"**.
4.  Añade la URL: `https://github.com/stoker2010/tarifas_20td`
5.  Categoría: **Integration**.
6.  Busca "Tarifas 20TD" y pulsa **Descargar**.
7.  Reinicia Home Assistant.

### Opción 2: Manual

1.  Descarga la última *release* desde GitHub.
2.  Copia la carpeta `custom_components/tarifas_20td` dentro de tu carpeta `custom_components` en Home Assistant.
3.  Reinicia Home Assistant.

---

## ⚙️ Configuración

Añade la siguiente configuración a tu archivo `configuration.yaml`. 

```yaml
sensor:
  - platform: tarifas_20td
    # Opcional: Nombre personalizado para el sensor
    name: "Tarifa Electricidad"
