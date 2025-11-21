# Tarifas Eléctricas 20TD 🇪🇸

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub version](https://img.shields.io/github/v/release/stoker2010/tarifas_20td?style=for-the-badge&color=blue)](https://github.com/stoker2010/tarifas_20td/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/stoker2010/tarifas_20td/graphs/commit-activity)

**Tarifas 20TD** es una integración avanzada para **Home Assistant** diseñada para gestionar la facturación eléctrica en España. No solo visualiza los periodos (Punta, Llano, Valle), sino que ofrece servicios para interactuar con los datos de precios y optimizar el consumo.

---

## ✨ Características Principales

* 📊 **Monitorización de Periodos**: Visualización en tiempo real del periodo actual (P1, P2, P3).
* 📅 **Gestión de Calendario**: Detección automática de festivos nacionales y fines de semana.
* 🛠️ **Servicios Integrados**: Comandos ejecutables para forzar actualizaciones o gestionar datos manualmente.
* ⚡ **Estabilidad**: Basado en la versión v0.6.0 (Stable Release).

---

## 🚀 Instalación

### Vía HACS (Recomendado)

1.  Abre HACS > Integraciones > menú superior derecho > **Repositorios Personalizados**.
2.  Añade la URL: `https://github.com/stoker2010/tarifas_20td`
3.  Categoría: **Integration**.
4.  Pulsa **Descargar** (asegúrate de seleccionar la versión más reciente).
5.  Reinicia Home Assistant.

### Instalación Manual

1.  Descarga la última *release* desde GitHub.
2.  Copia la carpeta `custom_components/tarifas_20td` en tu directorio `custom_components`.
3.  Reinicia Home Assistant.

---

## ⚙️ Configuración YAML

Añade el sensor a tu archivo `configuration.yaml`:

```yaml
sensor:
  - platform: tarifas_20td
    name: "Tarifa Electricidad"
