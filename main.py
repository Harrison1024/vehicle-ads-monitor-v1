import time
import random
from utilidades import *
from Models.pasada import Pasada
from Services.neoauto_scraper import NeoAutoScraper
from Services.telegram_notifier import TelegramNotifier
from Repositories.anuncios_repository import *
from Repositories.pasada_repository import *
from Repositories.envios_repository import *
from Repositories.prices_history import *
from Repositories.revision_repository import *
from Repositories.estados_repository import *


#Inicialización de bases de datos
inicializar_db_anuncios()
inicializar_db_pasadas()
inicializar_db_envios()
inicializar_db_precios()
inicializar_db_estados()

# Instancias de clases
pasada = Pasada()
neoAuto_scraper = NeoAutoScraper()
telegram_notifier = TelegramNotifier()

guardar_inicio_db(pasada)

while dentro_de_horario_trabajo():
    if obtener_estado("Revisor"):
        log("[INACTIVE] Esperando a que el revisor termine")
        espera = random.randint(25, 35) 
        log(f"[WAIT] Esperando aproximadamente {espera} segundos...\n")
        time.sleep(espera)
        continue
    else:
        activar("Scraper")
        log("[START] Inicio de la pasada")

    try:
        # Scrapeo de NeoAuto
        anuncios_nuevos = neoAuto_scraper.scrape_page()
        
        # Guardar anuncios nuevos en SQLite y filtrar los que ya se habían enviado
        anuncios_nuevos_filtrados = guardar_anuncios_sqlite(anuncios_nuevos)
        
        # Enviar anuncios nuevos por Telegram
        anuncios_nuevos_envio = telegram_notifier.envio_masivo(anuncios_nuevos_filtrados)

        # Actualizar el estado de los anuncios enviados en SQLite
        guardar_envios_db(anuncios_nuevos_envio)

        # Actualizar la pasada en la base de datos
        pasada.actualizar_pasada()
        
        # Actualizar el registro de la pasada en la base de datos
        actualizar_registro_db(pasada)
        
        log("[END] Fin de la pasada")
        
        # Realizar espera
        espera = random.randint(300, 420)
        minutos = espera // 60
        log(f"[WAIT] Esperando aproximadamente {minutos} minutos...\n")
        desactivar("Scraper")
        time.sleep(espera)
        
    except Exception as e:
        espera = random.randint(120, 240)
        log(f"[ERROR] Error inesperado: {e}. Reintentando {espera} segundos...")
        time.sleep(espera)

