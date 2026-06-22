# 🌤️ ¿Qué tiempo hace?

Un script de Python sencillo y eficiente para consultar la predicción meteorológica en tiempo real directamente desde la **API abierta de AEMET (España)** a través de tu terminal.

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/status-active-green.svg)

---

## 🚀 Características
* **Ligero:** Basado en bibliotecas estándar y `requests`.
* **Preciso:** Datos directos desde la fuente oficial (AEMET).
* **Fácil de usar:** Obtén información del clima con un solo comando.
* **Flexible:** Soporta búsqueda por código de municipio.

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/zebenpixel/que_tiempo_hace.git](https://github.com/zebenpixel/que_tiempo_hace.git)
   cd que_tiempo_hace

2. Instala la dependencia necesaria:
   pip install requests


# Consulta AEMET: ¿Qué tiempo hace hoy?

Este script en Python consulta la API XML abierta de la Agencia Estatal de Meteorología (AEMET) de España para obtener la predicción del tiempo para un municipio específico. Muestra detalles como humedad relativa, temperatura, sensación térmica, rayos UV y estado del cielo para el día actual.

## Requisitos

- Python 3.6 o superior.
- Bibliotecas estándar: `xml.etree.ElementTree`, `requests`, `datetime`, `argparse`, `logging`.
- No se requieren instalaciones adicionales (usa bibliotecas built-in y `requests`, que puedes instalar con `pip install requests` si no la tienes).

## Uso

Ejecuta el script desde la línea de comandos, opcionalmente especificando el código del municipio (por defecto: 38038 - Santa Cruz de Tenerife).

Ejemplos:

- Para Santa Cruz de Tenerife:
  python aemet.py

- Para Puerto de la Cruz (código 38028):
  python aemet.py 38028

📍 ¿Cómo obtener el código de municipio?
Accede a la web oficial de AEMET Predicción Municipios.

Busca tu localidad.

El código aparece en la URL, por ejemplo: ...localidad_38038.xml -> el código es 38038.
- Visita la página de AEMET: [Municipios](https://www.aemet.es/es/eltiempo/prediccion/municipios).
  
📊 Ejemplo de salida
Al ejecutar el script, obtendrás un reporte detallado en tu terminal como el que se muestra a continuación:
- Busca tu municipio y extrae el código de la URL (ej: `localidad_38038.xml` → código `38038`).-> Santa Cruz de Tenerife

📝 Notas técnicas
Este script procesa el XML de AEMET para extraer datos clave: temperatura, humedad, sensación térmica, índice UV y estado del cielo.

Asegúrate de tener conexión a internet para realizar la consulta en tiempo real.

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes una idea para mejorar el formato de salida o añadir nuevas funcionalidades, abre un issue o envía un pull request.


## Notas:

- La API de AEMET es pública y no requiere clave API.
- El script selecciona automáticamente la predicción para el día actual y mañana.
- Para días futuros, algunos datos detallados (como horarios de humedad o temperatura) podrían no estar disponibles y se indicará en la salida.
- Si no hay datos para hoy o mañana, mostrará una advertencia.
- Para más detalles sobre la estructura XML de AEMET, consulta su documentación oficial.
- El script selecciona automáticamente la predicción para el día actual.
- Si no hay datos para hoy, mostrará una advertencia.
- Para más detalles sobre la estructura XML de AEMET, consulta su documentación oficial.

## Autor

zebenpixel - [GitHub](https://github.com/zebenpixel)

## Licencia

MIT License - Siéntete libre de usar y modificar.
