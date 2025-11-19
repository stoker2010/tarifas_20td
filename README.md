# Tarifas España 2.0TD & Balance Neto

[![GitHub release](https://img.shields.io/github/release/stoker2010/tarifas_20td.svg)](https://github.com/stoker2010/tarifas_20td/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-orange.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40stoker2010-blue.svg)](https://github.com/stoker2010)

**[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English Description

**Tarifas 2.0TD** is a comprehensive Home Assistant integration designed for Spanish households with solar panels. It manages electricity tariff periods (Valle, Punta, Llana), calculates **Hourly Net Balance** (Virtual Battery), and includes a smart **Water Heater (Termo) Manager** to maximize solar self-consumption.

### ✨ Key Features

* **Auto-Configuration:** Creates two distinct devices:
    1.  **Hogar (Home):** Main energy manager.
    2.  **Termo Eléctrico (Water Heater):** Dedicated smart controller.
* **Hourly Net Balance:** Calculates your "Virtual Battery" balance in real-time. Resets automatically at the start of each hour (XX:00).
* **Zero Export Helper:** The sensor `Intensidad vertido 0` tells you exactly how many Amps (+/-) you need to consume or reduce to finish the current hour at exactly 0 kWh balance.
* **Smart Water Heater Control:**
    * Divert surplus energy to heat water.
    * Configurable target temperatures and safety limits.

---

<a name="español"></a>
## 🇪🇸 Descripción en Español

Esta integración es un "Todo en Uno" para gestionar la energía en hogares españoles con paneles solares. Gestiona los **tramos horarios 2.0TD**, calcula el **Balance Neto Horario** (Batería Virtual) y gestiona inteligentemente los excedentes derivándolos a un **Termo Eléctrico**.

### 📸 Vistazo Rápido

La integración genera automáticamente dos dispositivos en Home Assistant para mantener todo organizado:

1.  **Hogar (Gestor Energético):** Sensores de tarifas, balance y contadores.
2.  **Termo Eléctrico (Control):** Interruptores y lógica de calentamiento de agua.

### 🚀 Características Detalladas

#### 1. Gestión de Tarifas y Balance (Dispositivo "Hogar")
* **Tarifa 2.0TD Tramo Actual:** Indica si estás en periodo `Punta`, `Llano` o `Valle` automáticamente, teniendo en cuenta festivos nacionales (vía integración `workday`).
* **Balance Neto Horario (Real):** Suma de Importación/Exportación dentro de la hora actual. Se resetea a 0 cada hora en punto (XX:00).
* **Balance Neto Horario (Estimado):** Predicción de cómo acabará la hora actual si el consumo se mantiene estable.
* **Intensidad Vertido 0:** Calcula los Amperios exactos que necesitas consumir (o dejar de consumir) para que, al acabar la hora, tu balance sea 0 kWh (ideal para no regalar excedentes ni pagar por importar si ya has exportado).

#### 2. Control Inteligente del Termo (Dispositivo "Termo Eléctrico")
Convierte un termo eléctrico convencional en una "Batería Térmica" usando un enchufe inteligente (switch) y un sensor de temperatura.

* **Modos de Funcionamiento:**
    * **Cargar con Excedentes:** Activa el termo solo cuando hay energía solar sobrante.
    * **Limitar carga a Temp Max:** Seguridad para no sobrecalentar el agua al usar excedentes.
* **Controles:** Slider visual para ajustar la temperatura objetivo (35ºC - 60ºC).

#### 3. Contadores Diarios
Sensores que se reinician cada noche (00:00) para estadísticas rápidas:
* Energía Importada Total.
* Energía Excedente.
* Consumo Hogar (Cálculo: Solar + Red - Inyección).

---

### ⚙️ Instalación y Configuración

1.  Instala este repositorio vía **HACS** (Integraciones > Explorar > Buscar "Tarifas 2.0TD").
2.  Reinicia Home Assistant.
3.  Ve a **Ajustes > Dispositivos y Servicios > Añadir Integración > Tarifas España 2.0TD**.

#### Formulario de Configuración (v0.6.3)

Se te pedirán los siguientes datos (puedes verlos en tus entidades actuales):

| Campo | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **sensor_energia_grid** | Tu sensor de consumo de red (W). Positivo=Importa, Negativo=Exporta (o viceversa según tu medidor). | `sensor.shelly_em_channel_2` |
| **sensor_produccion_solar** | Tu sensor de producción solar actual (W). | `sensor.envoy_current_production` |
| **potencia_contratada_valle** | Potencia contratada en periodo P3 (W). | `6000` |
| **potencia_contratada_punta** | Potencia contratada en periodo P1/P2 (W). | `4500` |
| **dias_laborables** | Entidad binary_sensor de `Workday` para detectar festivos. | `binary_sensor.workday_sensor` |
| **interruptor_termo** | El enchufe/relé que enciende el termo. | `switch.enchufe_termo` |
| **temperatura_termo** | Sonda de temperatura del agua. | `sensor.temp_agua_termo` |
| **sensor_consumo_termo** | Sensor de potencia actual del termo (W). | `sensor.enchufe_termo_power` |
| **potencia_maxima_termo** | Potencia nominal de la resistencia del termo (W). | `1500` |

---

### 📊 Entidades Creadas

Una vez configurado, verás lo siguiente en tu panel:

**En el dispositivo "Hogar":**
* `sensor.balance_neto_horario_real` (kWh)
* `sensor.balance_neto_horario_estimado` (kWh)
* `sensor.intensidad_vertido_0` (A)
* `sensor.tarifa_20td_tramo_actual` (Texto)
* `sensor.energia_excedente_diario` (kWh)
* `sensor.energia_importada_total_diario` (kWh)
* `sensor.consumo_hogar_diario` (kWh)

**En el dispositivo "Termo Eléctrico":**
* `number.temperatura_objetivo_termo` (Slider)
* `switch.cargar_con_excedentes`
* `switch.limitar_carga_exc_a_temp_max`
* `switch.limite_temperatura_maxima`

---

### 🙌 Agradecimientos y Créditos

Esta integración ha sido inspirada y desarrollada gracias a la comunidad de Home Assistant en español.
* Agradecimiento especial a los canales de **[@domotica_solar](https://www.youtube.com/@domotica_solar)**, **[@proyectosmicropic](https://www.youtube.com/@proyectosmicropic)** y **[@unlocoysutecnologia](https://www.youtube.com/@unlocoysutecnologia)** por la divulgación y sus excelentes tutoriales.
* Código base inspirado en trabajos de **[@MiguelAngelLV](https://github.com/MiguelAngelLV)**.

<p align="center">
  Desarrollado con ❤️ por <a href="https://github.com/stoker2010">@stoker2010</a>
</p>
