# Consulta AEMET: ¿Qué tiempo hace hoy, mañana y pasado mañana?
#
# 2025 zebenpixel <https://github.com/zebenpixel>
#
# Este script consulta la API XML de AEMET para obtener la predicción del tiempo
# para un municipio específico en España. Muestra información como humedad, temperatura,
# rayos UV, estado del cielo y viento para el día actual, el siguiente y, si disponible, el día después de mañana.
#
# V1.1 Mejoras realizadas:
# - Añadida predicción para mañana y pasado mañana (si disponible).
# - Añadida extracción e impresión de información sobre el viento (dirección y velocidad por periodos).
# - Añadida flexibilidad para especificar el código de municipio vía argumentos de línea de comandos.
# - Corregidos errores en la evaluación de rayos UV (usaba variables de humedad por error).
# - Mejora en el manejo de fechas: selecciona automáticamente el día actual, mañana y pasado mañana.
# - Mejora en el manejo de errores y validaciones, incluyendo ausencia de datos en días futuros.
# - Añadidos comentarios y docstrings para mejor legibilidad.
# - Formateo de salida más limpio y estructurado con separadores y líneas vacías para diferenciar días y secciones.
# - Uso de logging en lugar de prints directos para mayor control (opcional verbosity).
# - Corregida DeprecationWarning cambiando 'if dia:' a 'if dia is not None:' para compatibilidad futura.
# - Añadida información de probabilidad de precipitación.
# - Hecho la selección de periodos dinámica en lugar de hardcoded.
# - Añadidas rachas máximas de viento.
# - Mantenida la estructura original de evaluación if-elif para humedad máxima y mínima, similar al código proporcionado.
# - Añadida evaluación para el viento usando if-elif, basada en la velocidad (ej: fuerte, moderado, débil), similar a la estructura de humedad.
# - Añadida evaluación para cada tramo horario de humedad, similar a max/min, para mostrar descripción por hora.
# - Añadida evaluación para temperatura máxima, mínima y por tramos horarios usando if-elif (Calor extremo >=30°C, Caluroso 25-29, Templado 20-24, Fresco 10-19, Frío <10, Valor fuera de rango).

import xml.etree.ElementTree as ET
import requests
import datetime as dt
import argparse
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def fetch_aemet_xml(municipio_code):
    """
    Obtiene el XML de predicción de AEMET para un municipio dado.
    
    :param municipio_code: Código del municipio (ej: '38038' para Santa Cruz de Tenerife).
    :return: Raíz del árbol XML si éxito, None otherwise.
    """
    url = f"https://www.aemet.es/xml/municipios/localidad_{municipio_code}.xml"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si no es 200
        return ET.fromstring(response.content)
    except requests.RequestException as e:
        logging.error(f"Error al obtener el XML: {e}")
        return None

def format_date(iso_date):
    """Formatea una fecha ISO (YYYY-MM-DD) a DD/MM/YYYY."""
    parts = iso_date.split("-")
    return "/".join(reversed(parts))

def find_prediction(root, date_str):
    """
    Encuentra el elemento <dia> correspondiente a la fecha dada.
    
    :param root: Raíz del árbol XML.
    :param date_str: Fecha en formato YYYY-MM-DD.
    :return: Elemento <dia> para la fecha, o None si no encontrado.
    """
    for dia in root.findall(".//prediccion/dia"):
        if dia.get('fecha') == date_str:
            return dia
    logging.warning(f"No se encontró predicción para la fecha {date_str}.")
    return None

def print_humidity_info(dia, label=""):
    """
    Imprime información de humedad relativa máxima, mínima y por tramos horarios.
    
    Mantiene la estructura original de evaluación con if-elif para humedad máxima y mínima,
    como en el código proporcionado, para preservar la lógica de evaluación explícita.
    Añadida evaluación similar para cada tramo horario, mostrando descripción por hora.
    """
    humedad = dia.find("humedad_relativa")
    if humedad is None:
        logging.info(f"No se encontró información de humedad para {label}.")
        return
    
    try:
        max_hum = int(humedad.find("maxima").text)
        min_hum = int(humedad.find("minima").text)
        
        logging.info(f"-> Humedad Relativa Max y Min para {label} " + "-" * 3)
        
        # Evaluar la humedad máxima (estructura mantenida del código original)
        if max_hum >= 70:
            logging.info(f" Humedad máxima: {max_hum}% - Demasiada humedad")
        elif 40 <= max_hum <= 69:
            logging.info(f" Humedad máxima: {max_hum}% - Se puede estar")
        elif 0 <= max_hum <= 39:
            logging.info(f" Humedad máxima: {max_hum}% - Demasiado seco")
        else:
            logging.info(f" Humedad máxima: {max_hum}% - Valor fuera de rango")
        
        # Evaluar la humedad mínima (estructura mantenida del código original)
        if min_hum >= 70:
            logging.info(f" Humedad mínima: {min_hum}% - Demasiada humedad")
        elif 40 <= min_hum <= 69:
            logging.info(f" Humedad mínima: {min_hum}% - Se puede estar")
        elif 0 <= min_hum <= 39:
            logging.info(f" Humedad mínima: {min_hum}% - Demasiado seco")
        else:
            logging.info(f" Humedad mínima: {min_hum}% - Valor fuera de rango")
        
        logging.info("")  # Línea vacía para separación
        
        datos = humedad.findall("dato")
        if datos:
            logging.info(f"-> Humedad Relativa por tramo Horario para {label} " + "-" * 3)
            for dato in datos[:3]:  # Primeros 3 tramos disponibles
                hora = dato.get('hora')
                valor_str = dato.text
                try:
                    valor = int(valor_str)
                    # Evaluar cada valor horario con if-elif, similar a max/min
                    if valor >= 70:
                        descripcion = " - Demasiada humedad"
                    elif 40 <= valor <= 69:
                        descripcion = " - Se puede estar"
                    elif 0 <= valor <= 39:
                        descripcion = " - Demasiado seco"
                    else:
                        descripcion = " - Valor fuera de rango"
                    logging.info(f" Hora: {hora}:00, Valor: {valor}%{descripcion}")
                except ValueError:
                    logging.info(f" Hora: {hora}:00, Valor: {valor_str} - Valor no evaluable")
            logging.info("")  # Línea vacía para separación
        else:
            logging.info(f"No hay datos horarios de humedad para {label}.")
    except (ValueError, AttributeError):
        logging.error(f"Error al procesar datos de humedad para {label}.")

def print_temperature_info(dia, label=""):
    """
    Imprime información de temperatura y sensación térmica, con evaluación.  """
    temperatura = dia.find("temperatura")
    sens_termica = dia.find("sens_termica")
    if temperatura is None or sens_termica is None:
        logging.info(f"No se encontró información de temperatura para {label}.")
        return
    
    try:
        max_temp = int(temperatura.find("maxima").text)
        min_temp = int(temperatura.find("minima").text)
        max_sens = int(sens_termica.find("maxima").text)
        
        logging.info(f"-> Temperatura Max y Min para {label} " + "-" * 3)
        
        # Evaluar la temperatura máxima con if-elif
        if max_temp >= 30:
            logging.info(f" Temperatura máxima: {max_temp}°C - Calor extremo")
        elif 25 <= max_temp <= 29:
            logging.info(f" Temperatura máxima: {max_temp}°C - Caluroso")
        elif 20 <= max_temp <= 24:
            logging.info(f" Temperatura máxima: {max_temp}°C - Templado")
        elif 10 <= max_temp <= 19:
            logging.info(f" Temperatura máxima: {max_temp}°C - Fresco")
        elif max_temp < 10:
            logging.info(f" Temperatura máxima: {max_temp}°C - Frío")
        else:
            logging.info(f" Temperatura máxima: {max_temp}°C - Valor fuera de rango")
        
        # Evaluar la temperatura mínima con if-elif
        if min_temp >= 30:
            logging.info(f" Temperatura mínima: {min_temp}°C - Calor extremo")
        elif 25 <= min_temp <= 29:
            logging.info(f" Temperatura mínima: {min_temp}°C - Caluroso")
        elif 20 <= min_temp <= 24:
            logging.info(f" Temperatura mínima: {min_temp}°C - Templado")
        elif 10 <= min_temp <= 19:
            logging.info(f" Temperatura mínima: {min_temp}°C - Fresco")
        elif min_temp < 10:
            logging.info(f" Temperatura mínima: {min_temp}°C - Frío")
        else:
            logging.info(f" Temperatura mínima: {min_temp}°C - Valor fuera de rango")
        
        logging.info(f" Sensación térmica máxima: {max_sens}°C")
        logging.info("")  # Línea vacía para separación
        
        # Tramos horarios de temperatura
        datos = temperatura.findall("dato")
        if datos:
            logging.info(f"-> Temperatura por tramo Horario para {label} " + "-" * 3)
            for dato in datos[:3]:  # Primeros 3 tramos disponibles
                hora = dato.get('hora')
                valor_str = dato.text
                try:
                    valor = int(valor_str)
                    # Evaluar cada valor horario con if-elif
                    if valor >= 30:
                        descripcion = " - Calor extremo"
                    elif 25 <= valor <= 29:
                        descripcion = " - Caluroso"
                    elif 20 <= valor <= 24:
                            descripcion = " - Templado"
                    elif 10 <= valor <= 19:
                        descripcion = " - Fresco"
                    elif valor < 10:
                        descripcion = " - Frío"
                    else:
                        descripcion = " - Valor fuera de rango"
                    logging.info(f" Hora: {hora}:00, Valor: {valor}°C{descripcion}")
                except ValueError:
                    logging.info(f" Hora: {hora}:00, Valor: {valor_str} - Valor no evaluable")
            logging.info("")  # Línea vacía para separación
        else:
            logging.info(f"No hay datos horarios de temperatura para {label}.")
    except (ValueError, AttributeError):
        logging.error(f"Error al procesar datos de temperatura para {label}.")

def print_uv_info(dia, label=""):
    """Imprime información de rayos UV."""
    uv_max = dia.find("uv_max")
    if uv_max is None:
        logging.info(f"No se encontró información de rayos UV para {label}.")
        return
    
    try:
        uv = int(uv_max.text)
        
        logging.info(f"-> Rayos UV para {label} " + "-" * 3)
        if uv >= 7:
            logging.info(f" Rayos UV: {uv} - Protégete del sol")
        elif 4 <= uv <= 6:
            logging.info(f" Rayos UV: {uv} - Ten cuidado con el sol")
        elif 0 <= uv <= 3:
            logging.info(f" Rayos UV: {uv} - Puedes tomar un poco de sol")
        else:
            logging.info(f" Rayos UV: {uv} - Valor fuera de rango")
        logging.info("")  # Línea vacía para separación
    except ValueError:
        logging.error(f"Error al procesar datos de rayos UV para {label}.")

def print_precipitation_info(dia, label=""):
    """
    Imprime probabilidad de precipitación por periodos.
    
    Esta función extrae las probabilidades de precipitación del XML y las evalúa
    para proporcionar una descripción cualitativa (alta, media, baja). Se enfoca
    en periodos diurnos para mantener consistencia con otras secciones.
    """
    precipitaciones = dia.findall("prob_precipitacion")
    if not precipitaciones:
        logging.info(f"No se encontró información de precipitación para {label}.")
        return
    
    logging.info(f"-> Probabilidad de Precipitación para {label} " + "-" * 3)
    # Periodos diurnos deseados para consistencia (ajustable)
    desired_periods = ['06-12', '12-18', '18-24']
    for periodo in desired_periods:
        found = False
        for precip in precipitaciones:
            if precip.get('periodo') == periodo:
                valor = precip.text or "0"
                try:
                    prob = int(valor)
                    # Evaluar con if-elif para mantener estructura similar al original
                    if prob >= 70:
                        descripcion = f" {prob}% - Alta probabilidad"
                    elif prob >= 40:
                        descripcion = f" {prob}% - Media probabilidad"
                    else:
                        descripcion = f" {prob}% - Baja probabilidad"
                    logging.info(f" Periodo: {periodo},{descripcion}")
                except ValueError:
                    logging.info(f" Periodo: {periodo} - Datos no disponibles")
                found = True
                break
        if not found:
            logging.info(f" Periodo: {periodo} - No disponible")
    logging.info("")  # Línea vacía para separación

def print_wind_info(dia, label=""):
    """
    Imprime información de viento: dirección, velocidad y rachas máximas por periodos, con evaluación.
    
    Esta función filtra dinámicamente por periodos diurnos deseados en lugar de usar
    índices fijos, lo que la hace más robusta para días con menos datos detallados.
    Incluye rachas máximas si están disponibles en el XML.
    Añadida evaluación con if-elif para la velocidad del viento, similar a la estructura de humedad
    (ej: viento fuerte si >=50 km/h, moderado 20-49, débil <20).
    """
    vientos = dia.findall("viento")
    if not vientos:
        logging.info(f"No se encontró información de viento para {label}.")
        return
    
    logging.info(f"-> Viento para {label} " + "-" * 3)
    # Periodos diurnos deseados (más robusto que slice fijo)
    desired_periods = ['06-12', '12-18', '18-24']
    for periodo in desired_periods:
        found = False
        for viento in vientos:
            if viento.get('periodo') == periodo:
                direccion_elem = viento.find("direccion")
                velocidad_elem = viento.find("velocidad")
                racha_elem = viento.find("racha_max")  # Añadido para rachas máximas
                
                if direccion_elem is not None and velocidad_elem is not None:
                    direccion = direccion_elem.text or "N/A"
                    try:
                        velocidad = int(velocidad_elem.text)
                    except (ValueError, TypeError):
                        velocidad = "N/A"
                    
                    # Procesar racha máxima si existe
                    racha_str = ""
                    if racha_elem is not None and racha_elem.text:
                        try:
                            racha = int(racha_elem.text)
                            racha_str = f", Racha máx: {racha} km/h"
                        except ValueError:
                            pass
                    
                    # Evaluar la velocidad del viento con if-elif (similar a humedad)
                    if isinstance(velocidad, int):
                        if velocidad >= 50:
                            evaluacion = " - Viento fuerte"
                        elif 20 <= velocidad <= 49:
                            evaluacion = " - Viento moderado"
                        elif 0 <= velocidad <= 19:
                            evaluacion = " - Viento débil"
                        else:
                            evaluacion = " - Valor fuera de rango"
                    else:
                        evaluacion = " - No evaluable"
                    
                    logging.info(f" Periodo: {periodo}, Dirección: {direccion}, Velocidad: {velocidad} km/h{racha_str}{evaluacion}")
                else:
                    logging.info(f" Periodo: {periodo} - Datos incompletos")
                found = True
                break
        if not found:
            logging.info(f" Periodo: {periodo} - No disponible")
    logging.info("")  # Línea vacía para separación

def print_sky_state(dia, label=""):
    """
    Imprime estado del cielo por periodos.
    
    Similar a print_wind_info, usa filtrado dinámico por periodos deseados para
    mayor robustez en días con estructuras variables en el XML.
    """
    logging.info(f"-> Estado del Cielo para {label} " + "-" * 3)
    estados = dia.findall("estado_cielo")
    if estados:
        # Periodos diurnos deseados
        desired_periods = ['06-12', '12-18', '18-24']
        for periodo in desired_periods:
            found = False
            for estado in estados:
                if estado.get('periodo') == periodo:
                    desc = estado.get('descripcion') or estado.text
                    logging.info(f" Periodo: {periodo}, Descripción: {desc}")
                    found = True
                    break
            if not found:
                logging.info(f" Periodo: {periodo} - No disponible")
        logging.info("")  # Línea vacía para separación
    else:
        logging.info(f"No hay información sobre el estado del cielo para {label}.")

def print_prediction(dia, date_str, label):
    if dia is not None:
        logging.info("=" * 60)
        logging.info(f"Predicción para {label} - {format_date(date_str)}")
        logging.info("=" * 60)
        logging.info("")  # Línea vacía para separación
        print_humidity_info(dia, label)
        print_temperature_info(dia, label)
        print_uv_info(dia, label)
        print_precipitation_info(dia, label)  # Añadido: probabilidad de precipitación
        print_wind_info(dia, label)
        print_sky_state(dia, label)

def main(municipio_code):
    """
    Función principal que orquesta la consulta a AEMET.
    
    Esta función obtiene el XML de predicciones, extrae información general de la localidad
    y la fecha de elaboración, calcula las fechas para hoy, mañana y pasado mañana,
    busca las predicciones correspondientes y las imprime utilizando las funciones auxiliares.
    Finalmente, registra la hora y fecha de ejecución del script.
    
    :param municipio_code: Código del municipio para el cual se consulta el tiempo.
    """
    root = fetch_aemet_xml(municipio_code)  # Obtener el XML de AEMET
    if root is None:
        return  # Salir si no se pudo obtener el XML
   
    # Extraer nombre de la localidad
    nombre_localidad = root.find("nombre").text
    # Extraer fecha de elaboración del pronóstico (solo la parte de fecha, ignorando hora)
    elaborado = root.find("elaborado").text.split("T")[0]
    # Formatear la fecha a DD/MM/YYYY
    elaborado_formatted = format_date(elaborado)
   
    # Imprimir cabecera de la consulta
    logging.info("-> Consulta del Tiempo en AEMET")
    logging.info(f" Previsión para la Localidad: {nombre_localidad}")
    logging.info(f" Previsión elaborada el: {elaborado_formatted}")
    logging.info("")  # Línea vacía para separación
   
    # Calcular fechas: hoy, mañana y pasado mañana
    today = dt.date.today()
    tomorrow = today + dt.timedelta(days=1)
    day_after_tomorrow = today + dt.timedelta(days=2)
    # Convertir fechas a formato ISO (YYYY-MM-DD)
    today_str = today.isoformat()
    tomorrow_str = tomorrow.isoformat()
    day_after_tomorrow_str = day_after_tomorrow.isoformat()
   
    # Buscar e imprimir predicción para hoy
    dia_hoy = find_prediction(root, today_str)
    print_prediction(dia_hoy, today_str, "Hoy")
   
    # Buscar e imprimir predicción para mañana
    dia_manana = find_prediction(root, tomorrow_str)
    print_prediction(dia_manana, tomorrow_str, "Mañana")
   
    # Buscar e imprimir predicción para pasado mañana si está disponible
    dia_pasado_manana = find_prediction(root, day_after_tomorrow_str)
    if dia_pasado_manana is not None:
        print_prediction(dia_pasado_manana, day_after_tomorrow_str, "Pasado Mañana")
    else:
        logging.info("No hay predicción disponible para pasado mañana.")
   
    # Obtener hora actual para registrar la ejecución
    now = dt.datetime.now()
    logging.info("")  # Línea vacía para separación
    logging.info("=" * 60)
    logging.info(f"-- El código se ejecutó a las {now.hour:02d}:{now.minute:02d}:{now.second:02d} "
                 f"con fecha {now.day:02d}/{now.month:02d}/{now.year}")
    logging.info("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta el tiempo en AEMET para un municipio.")
    parser.add_argument("municipio_code", type=str, nargs="?", default="38038",
                        help="Código del municipio (ej: 38038 para Santa Cruz de Tenerife).")
    args = parser.parse_args()
    main(args.municipio_code)
