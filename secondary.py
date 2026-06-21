import time
import random
from Services.data_revision import DataRevision
from Repositories.anuncios_repository import *
from Repositories.revision_repository import *
from Repositories.estados_repository import *


#Inicialización de bases de datos
inicializar_db_revision()

# Instancias de clases
revision_data = DataRevision()

while dentro_de_horario_trabajo():
# while True:
    
    if obtener_estado("Scraper"):
        log("[INACTIVE] Esperando a que el scraper termine")
        espera = random.randint(25, 35)  # entre 25 y 30 segundos
        log(f"[WAIT] Esperando aproximadamente {espera} segundos...\n")
        time.sleep(espera)
        continue
    else:
        activar("Revisor")
        log("[START] Inicio de la pasada")
        time.sleep(5)
    try:
        # Obtener
        anuncios_incompletos = obtener_anuncios_incompletos()
        anuncios_completados = revision_data.completar_datos(anuncios_incompletos)

        
        guardar_lista_revisados(anuncios_completados)
        completar_datos_anuncio(anuncios_completados)
        
        
        time.sleep(5)
        log("[END] Fin de la pasada")
        
        # Realizar espera
        espera = random.randint(3000, 3500)  # entre 5 y 7 minutos
        minutos = espera // 60
        log(f"[END] Esperando aproximadamente {minutos} minutos...\n")
        desactivar("Revisor")
        time.sleep(espera)
        
    except Exception as e:
        espera = random.randint(120, 240)
        log(f"[ERROR] Error inesperado: {e}. Reintentando {espera} segundos...")
        time.sleep(espera)

