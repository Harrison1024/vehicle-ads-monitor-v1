import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from Models.revision import Revision
from utilidades import *
import json


class DataRevision:
    def __init__(self):
        self.modo_headless = True

    def completar_datos(self, lista_revision:list[Revision]):
        if not lista_revision:
            log("[REVIEW] No se encontro ningun anuncios para revisar")
            return []
                
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.modo_headless)
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            )
            revisados = 0
            for revision in lista_revision:
                page.goto(revision.anuncio.link, timeout=60000)
                page.wait_for_timeout(3000)
                diccionario_datos = self.extraer_datos_jsonld(page)
                revision.fecha_revision = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                revision.num_revisiones +=1
                revision.revisado = True
                revisados += 1
                revision.completar_datos_faltantes(diccionario_datos)
                time.sleep(1)
            log(f"[REVIEW] Se revisaron {revisados} anuncios")
            browser.close()
       
        return lista_revision
                     

    def extraer_datos_jsonld(self, page) -> dict:
        diccionario = {}

        try:
            script = page.locator(
                'script[type="application/ld+json"]'
            ).inner_text()

            data = json.loads(script)

            product = next(
                item
                for item in data["@graph"]
                if item.get("@type") == "Product"
            )

            propiedades = {
                p["name"]: p["value"]
                for p in product["additionalProperty"]
            }

            diccionario["Transmision"] = propiedades.get(
                "Transmisión",
                "No encontrado"
            )

            diccionario["Combustible"] = propiedades.get(
                "Combustible",
                "No encontrado"
            )

            diccionario["Vendedor"] = (
                product["offers"]
                    ["seller"]
                    ["name"]
            )

        except Exception as e:

            log(f"Error obteniendo JSON-LD: {e}")

            diccionario["Transmision"] = "No encontrado"
            diccionario["Combustible"] = "No encontrado"
            diccionario["Vendedor"] = "No encontrado"

        return diccionario   
    
    
    