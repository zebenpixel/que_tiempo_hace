#  Consulta AEMET que tiempo hace hoy 
#  
#  2024 zebenpixel <https://github.com/zebenpixel>
#  

import xml.etree.ElementTree as ET
import requests
import datetime



# Obtener el contenido del XML desde la URL de AEMET

# todos los municipios ->https://www.aemet.es/es/eltiempo/prediccion/municipios?p=38&w=t
# Santa Cruz 
url = "https://www.aemet.es/xml/municipios/localidad_38038.xml"
#Puerto de la cruz
#url = "https://www.aemet.es/xml/municipios/localidad_38028.xml"

response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Analizar el contenido XML
    root = ET.fromstring(response.content)

    # Extraer el nombre de la localidad y fecha actual
    print(f"-> Que tiempo hace Hoy")
    nombre_localidad = root.find(".//nombre").text
    print(f" Prevision para la Localidad: {nombre_localidad}")
    elaborado = root.find(".//elaborado").text
    partes = elaborado.split("T")[0].split("-")
    convertida = "/".join(reversed(partes)) 
    print(f" Prevision para el día:  {convertida}")
   
    # Buscar el elemento que contiene la fecha de la predicción
    fecha_prediccion_element = root.find(".//prediccion/dia")

    

    # Buscar el elemento que contiene la humedad maxima y minima
    print("-> Humedad Relativa Max y Min " + 30*"-")
    humedad_max_element = root.find(".//humedad_relativa/maxima")
    humedad_min_element = root.find(".//humedad_relativa/minima")
    if humedad_max_element is not None and humedad_min_element is not None:
        try:
            # Extraer y convertir a enteros los valores de humedad
            humedad_maxima = int(humedad_max_element.text)
            humedad_minima = int(humedad_min_element.text)

            # Evaluar la humedad máxima
            if humedad_maxima >= 70:
                print(f" La humedad máxima: {humedad_maxima} - Demasiada humedad")
            elif 40 <= humedad_maxima <= 69:
                print(f" La humedad máxima: {humedad_maxima} - Se puede estar")
            elif 0 <= humedad_maxima <= 39:
                print(f" La humedad máxima: {humedad_maxima} - Demasiado seco")
            else:
                print(f" La humedad máxima: {humedad_maxima} - Valor fuera de rango")

            # Evaluar la humedad mínima
            if humedad_minima >= 70:
                print(f" La humedad mínima: {humedad_minima} - Demasiada humedad")
            elif 40 <= humedad_minima <= 69:
                print(f" La humedad mínima: {humedad_minima} - Se puede estar")
            elif 0 <= humedad_minima <= 39:
                print(f" La humedad mínima: {humedad_minima} - Demasiado seco")
            else:
                print(f" La humedad mínima: {humedad_minima} - Valor fuera de rango")

        except ValueError:
            print("Error: No se pudo obtener el valor de humedad")
    else:
        print("No se pudo encontrar información sobre la humedad máxima o mínima.")

    # Buscar el elemento que contiene la humedad por tramo horario
    print("-> Humedad Relativa por tramo Horario"+ 30*"-")
    
    for dato in root.findall(".//humedad_relativa/dato")[:3]:
        hora = dato.get('hora')  # Obtener el atributo "hora"
        valor = dato.text  # Obtener el valor del elemento
        print(f" Hora: {hora}, Valor: {valor}")

    # Buscar el elemento que contiene la temperatura máxima y temperatura minima
    print("-> Temperatura "+ 30*"-")
    temperatura_maxima_element = root.find(".//temperatura/maxima")
    temperatura_minima_element = root.find(".//temperatura/minima")
    sensacion_termica_element = root.find(".//sens_termica/maxima")
    if temperatura_maxima_element is not None and temperatura_minima_element is not None:
        try:
            temperatura_maxima = int(temperatura_maxima_element.text)
            temperatura_minima = int(temperatura_minima_element.text)
            sensacion_termica = int(sensacion_termica_element.text)
            print(f" La Temperatura máxima: {temperatura_maxima}°C")
            print(f" La Temperatura minima: {temperatura_minima}°C")
            print(f" La Sensacion térmica : {sensacion_termica}°C")
        except ValueError:
            print("Error: No se pudo obtener el valor de temperatura")
    else:
        print("No se pudo encontrar información sobre la temperatura máxima y minima.")
        

    # Buscar el elemento que contiene los rayos UV
    print("-> Rayos UV "+ 30*"-")
    rayos_uv_element = root.find(".//uv_max")
    if rayos_uv_element is not None:
        try:
            #Extraer y convertir a enteros los valores de humedad
            rayos_uv = int(rayos_uv_element.text)
            if rayos_uv >= 7:
                print(f" Los rayos UV para hoy: {rayos_uv} - Protegete del sol")
            elif 4 <= humedad_minima <= 6:
                print(f" Los rayos UV para hoy: {rayos_uv} - Ten cuidado con el sol")
            elif 0 <= humedad_minima <= 3:
                print(f" Los rayos UV para hoy: {rayos_uv} - Puedes cojer un poco de sol")
            else:
                print(f"Los rayos UV para hoy: {rayos_uv} - Valor fuera de rango")
        except ValueError:
            print("Error: No se pudo obtener el valor de rayos UV")
    else:
        print("No se pudo encontrar información sobre los rayos UV.")

    print("-> Estado del Cielo "+ 30*"-")
    for dato in root.findall(".//estado_cielo")[4:7]:
        periodo = dato.get('periodo')  # Obtener el atributo "periodo"
        descripcion = dato.get('descripcion')  # Obtener el atributo "descripcion"
        #valor = dato.text  # Obtener el valor del elemento

        print(f" Periodo: {periodo}, Descripción: {descripcion}")

hora_actual = datetime.datetime.now()
print("-> El codigo se ejecuto = %s:%s:%s " % (hora_actual.hour, hora_actual.minute, hora_actual.second))
print("   con fecha de =  %s/%s/%s" % (hora_actual.day, hora_actual.month, hora_actual.year))