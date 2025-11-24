# Consulta AEMET: ¿Qué tiempo hace hoy?

Este script en Python consulta la API XML abierta de la Agencia Estatal de Meteorología (AEMET) de España para obtener la predicción del tiempo para un municipio específico. Muestra detalles como humedad relativa, temperatura, sensación térmica, rayos UV y estado del cielo para el día actual.

## Requisitos

- Python 3.6 o superior.
- Bibliotecas estándar: `xml.etree.ElementTree`, `requests`, `datetime`, `argparse`, `logging`.
- No se requieren instalaciones adicionales (usa bibliotecas built-in y `requests`, que puedes instalar con `pip install requests` si no la tienes).

## Instalación

1. Clona o descarga este repositorio.
2. Instala `requests` si es necesario:
   pip install requests

## Uso

Ejecuta el script desde la línea de comandos, opcionalmente especificando el código del municipio (por defecto: 38038 - Santa Cruz de Tenerife).

Ejemplos:

- Para Santa Cruz de Tenerife:
  python aemet.py

- Para Puerto de la Cruz (código 38028):
  python aemet.py 38028


### Cómo obtener el código de municipio
- Visita la página de AEMET: [Municipios](https://www.aemet.es/es/eltiempo/prediccion/municipios).
- Busca tu municipio y extrae el código de la URL (ej: `localidad_38038.xml` → código `38038`).

## Salida de ejemplo
- -> ¿Qué tiempo hace Hoy?
Previsión para la Localidad: Santa Cruz de Tenerife
Previsión elaborada el: 24/11/2025
- -> Humedad Relativa Max y Min ------------------------------
Humedad máxima: 75% - Demasiada humedad
Humedad mínima: 55% - Se puede estar
- -> Humedad Relativa por tramo Horario ------------------------------
Hora: 00:00, Valor: 70%
Hora: 06:00, Valor: 65%
Hora: 12:00, Valor: 55%
- -> Temperatura ------------------------------
Temperatura máxima: 22°C
Temperatura mínima: 18°C
Sensación térmica máxima: 23°C
- -> Rayos UV ------------------------------
Rayos UV: 5 - Ten cuidado con el sol
- -> Estado del Cielo ------------------------------
Periodo: 12-18, Descripción: Nuboso
Periodo: 18-24, Descripción: Poco nuboso
- -> El código se ejecutó a las 14:30:45 con fecha 24/11/2025


## Notas

- La API de AEMET es pública y no requiere clave API.
- El script selecciona automáticamente la predicción para el día actual.
- Si no hay datos para hoy, mostrará una advertencia.
- Para más detalles sobre la estructura XML de AEMET, consulta su documentación oficial.

## Autor

zebenpixel - [GitHub](https://github.com/zebenpixel)

## Licencia

MIT License - Siéntete libre de usar y modificar.
