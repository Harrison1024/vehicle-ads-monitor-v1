# Vehicle Ads Monitor V1

Sistema de monitoreo automatizado de anuncios de vehículos usados en NeoAuto desarrollado en Python.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Playwright](https://img.shields.io/badge/Playwright-Web%20Scraping-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## Descripción

Este proyecto fue desarrollado para monitorear publicaciones de vehículos en NeoAuto, detectar nuevos anuncios y cambios de precio, almacenar la información en bases de datos SQLite y enviar alertas automáticas mediante Telegram.

Además, incorpora herramientas de análisis y visualización de datos mediante un dashboard desarrollado en Streamlit.

## Tecnologías utilizadas

* Python
* Playwright
* SQLite
* Streamlit
* Telegram Bot API

## Funcionalidades

### Recolección de datos

El sistema realizaba revisiones periódicas de la sección de venta de vehículos usados de NeoAuto utilizando filtros de publicaciones más recientes.

Para cada anuncio se extraían datos como:

* Título
* Marca
* Modelo
* Año
* Precio
* Kilometraje
* Combustible
* Transmisión
* Vendedor
* Enlace del anuncio
* Imagen principal

### Almacenamiento y control de duplicados

Los anuncios eran almacenados en SQLite utilizando el enlace del anuncio como identificador único para evitar registros duplicados.

### Seguimiento de precios

El sistema registraba el historial de precios de cada vehículo y detectaba reducciones de precio para generar nuevas alertas.

### Gestión de envíos

Los anuncios detectados eran preparados para su envío mediante Telegram, registrando:

* Fecha de envío
* Estado del envío
* Número de intentos
* Resultado de la operación

### Compleción de datos

El proyecto incluía procesos adicionales para recuperar información faltante en anuncios incompletos y mejorar la calidad de los datos almacenados.

### Dashboard y análisis

Se desarrolló un dashboard con Streamlit para visualizar:

* Cantidad de anuncios registrados
* Distribución por marcas
* Últimos anuncios detectados
* Tendencias de precios
* Filtros por marca y modelo
* Gráficos de Precio vs Año

## Estructura del proyecto

```text
vehicle-ads-monitor-v1/
│
├── Models/
├── Repositories/
├── ScreeShots/
├── Services/
├── Data/
├── dashboard.py
├── main.py
├── configuraciones.py
├── utilidades.py
└── requirements.txt
```

## Estado del proyecto

⚠️ Legacy Version (V1)

Esta versión se encuentra archivada debido a cambios realizados por NeoAuto en la estructura de su sitio web.

El proyecto funcionó de manera continua durante aproximadamente cuatro meses antes de que dichos cambios afectaran el proceso de extracción de datos.

Actualmente se desarrolla una nueva versión con una arquitectura diferente.

## Instalacion y Uso

### Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Harrison1024/vehicle-ads-monitor-v1.git
cd vehicle-ads-monitor-v1
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Instalar navegadores de Playwright:

```bash
playwright install
```

### Configuración

Antes de ejecutar el proyecto es necesario configurar las credenciales de Telegram en el archivo de configuración correspondiente.

Por motivos de seguridad las credenciales originales fueron removidas de esta versión pública.

### Ejecución

#### Scraper

```bash
python main.py
```

#### Relleno de datos de anuncios incompletos

```bash
python secondary.py
```

#### Panel de Datos

```bash
streamlit run dashboard.py
```

## Aprendizajes

Durante el desarrollo de este proyecto se trabajó con:

* Web Scraping
* Automatización de procesos
* Bases de datos relacionales
* Diseño de arquitectura modular
* Dashboards interactivos
* Integración con Telegram
* Procesamiento y análisis de datos

## Resultados

Durante su funcionamiento el sistema permitió:

- Monitorear publicaciones de vehículos en NeoAuto.
- Detectar nuevas oportunidades de compra.
- Registrar históricos de precios.
- Generar alertas automáticas mediante Telegram.
- Construir una base de datos histórica para análisis posteriores.

## Evolución

Este proyecto corresponde a la primera versión del sistema.

Actualmente se encuentra en desarrollo una nueva versión enfocada en recolección de datos a mayor escala y análisis del mercado automotriz.

> Nota:
>
> Las bases de datos SQLite no se incluyen en este repositorio.
>
> El proyecto genera automáticamente las tablas necesarias durante la inicialización.
