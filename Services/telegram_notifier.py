import time
import requests
from configuraciones import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, FILTRO_PRECIO, MODO_DEBUG, INTENTOS_REENVIO
from Repositories.prices_history import entregar_historial_precios
from Models.envio import Envio
from datetime import datetime
from utilidades import log, es_nuevo_minimo


class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.filtro_precio = FILTRO_PRECIO
    
        
    def send_telegram(self, message, image_url=None, nombre=""):
        intentos = 0
        while intentos < INTENTOS_REENVIO:
            try:
                if image_url:
                    intentos += 1
                    payload = {
                        "chat_id": self.chat_id,
                        "photo": image_url,
                        "caption": message,
                        "parse_mode": "HTML"
                    }
                    r = requests.post(
                        f"https://api.telegram.org/bot{self.token}/sendPhoto",
                        data=payload,
                        timeout=20
                    )
                    if MODO_DEBUG:
                        log(f"[DEBUG] Mensaje con imagen enviado de {nombre}")
                        log(f"[DEBUG] Estado del envío: {r.status_code}")
                        
                else:
                    intentos += 1
                    payload = {
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML"
                    }
                    r = requests.post(
                        f"https://api.telegram.org/bot{self.token}/sendMessage",
                        data=payload,
                        timeout=20
                    )
                    if MODO_DEBUG:
                        log(f"[DEBUG] Mensaje sin imagen enviado de {nombre}")
                        log(f"[DEBUG] Estado del envío: {r.status_code}")

                if r.status_code != 200:
                    if MODO_DEBUG:
                        log(f"""
                                [ERROR TELEGRAM]
                                Status Code: {r.status_code}
                                Reason: {r.reason}
                                URL: {r.url}
                                Respuesta: {r.text}
                                """)
                    else:
                        log(f"[ERROR] Telegram error: {r.text}")
                    log(f"[ERROR] Reintentando envío... Intento {intentos}/{INTENTOS_REENVIO}")
                    time.sleep(2)  # espera antes de reintentar
                    if intentos >= INTENTOS_REENVIO:
                        return (False, intentos,"")
                else:
                    if MODO_DEBUG:
                        log(f"[DEBUG] Mensaje enviado correctamente!")
                        log(f"[DEBUG] Intentos realizados: {intentos}")
                    
                    fecha_envio  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return (True, intentos,fecha_envio)
                    
            except Exception as e:
                log(f"[ERROR] Telegram exception: {e}")
                
        return (False, intentos,"")


    def envio_masivo(self, nuevos:list[Envio])->list[Envio]:
        nuevos_con_envio = []
        for envio in nuevos:

            if envio.tipo_anuncio == "nuevo":
                envio.descripcion = "Anuncio nuevo"
                msg = (
                    f"🚗 <b>{envio.anuncio.titulo.upper()}</b>\n"
                    f"💵 <b>US${envio.anuncio.precio}</b>\n"
                    f"📊 <b>{envio.anuncio.kilometraje} km</b>\n"
                    f"⚙️ <b>{envio.anuncio.transmision}</b>\n"
                    f"⛽ <b>{envio.anuncio.combustible}</b>\n"
                    f"👤 <b>{envio.anuncio.vendedor}</b>\n"
                    f"👉 <a href=\"{envio.anuncio.link}\">Ver anuncio</a>"
                )
            elif envio.tipo_anuncio == "actualizado":
                hitorial_precios = entregar_historial_precios(envio.anuncio)
                
                if es_nuevo_minimo(hitorial_precios, envio.precio_id):
                    envio.descripcion = "Nuevo minimo"
                    msg = (
                        f"🔥🔥 <b>PRECIO REDUCIDO</b> 🔥🔥\n\n"
                        f"🚗 <b>{envio.anuncio.titulo.upper()}</b>\n"
                        f"💵 <b>US${envio.anuncio.precio}</b>\n"
                        f"👤 <b>{envio.anuncio.vendedor}</b>\n"
                        f"👉 <a href=\"{envio.anuncio.link}\">Ver anuncio</a>"
                    )
                else:
                    envio.descripcion = "Precio No Atractivo"
                    nuevos_con_envio.append(envio)   
                    continue
            
            (logro_enviar, intentos, fecha_envio) = self.send_telegram(message=msg, image_url= envio.anuncio.imagen, nombre=envio.anuncio.titulo.upper())

            envio.enviado = logro_enviar
            envio.fecha_envio = fecha_envio
            envio.intentos = intentos

            nuevos_con_envio.append(envio)        
            time.sleep(8)
            
        return nuevos_con_envio

