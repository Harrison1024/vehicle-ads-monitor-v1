from datetime import datetime
from configuraciones import CARACTERES_VACIOS


#===============================================
# LOG: Muestra los datos de hora y dia exactos
#===============================================

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


#===============================================
# Limpia el texto de caracteres vacios y espacios
#===============================================

def limpiar_texto(texto):

    if not texto:
        return "No encontrado"

    for c in CARACTERES_VACIOS:
        texto = texto.replace(c, "")

    texto = texto.strip()

    return texto if texto else "No encontrado"


#===================================================
# Verifica si estamos dentro del horario de trabajo
#==================================================

def dentro_de_horario_trabajo():
    # return True
    hour = datetime.now().hour
    minutes = datetime.now().minute
    horario = False
        
    if hour > 6 and hour <=23 :
        horario = True
        if hour == 23 and minutes <=45:
            log("Dentro del horario de trabajo...")
            horario = True
            return horario
        elif hour == 23 and minutes > 45:
            log("Fuera del horario de trabajo...")
            horario = False
            return horario 
    else:
        log("Fuera del horario de trabajo...")
    
    return horario


#==========================================================================
# Calcular el minimo de precios exceptuando el precio del anuncio a enviar 
#==========================================================================

def es_nuevo_minimo(precios, id_precio_actual):
    precio_actual = None
    otros_precios = []

    for id_precio, precio in precios:
        if id_precio == id_precio_actual:
            precio_actual = precio
        else:
            otros_precios.append(precio)

    if precio_actual is None:
        return False

    if not otros_precios:
        return True

    return precio_actual < min(otros_precios)

