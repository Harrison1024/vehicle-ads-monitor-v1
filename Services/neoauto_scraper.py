import time
from configuraciones import MARCAS, URL, BASE_URL, MODO_HEADLESS
from datetime import datetime
from playwright.sync_api import sync_playwright
from utilidades import log, limpiar_texto
from Models.anuncio import Anuncio


class NeoAutoScraper:
    def __init__(self):
        self.url = URL
        self.base_url= BASE_URL
        self.modo_headless = MODO_HEADLESS


    def scrape_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.modo_headless)
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            )
            
            log("[SCRAPING] Abriendo Neoauto...")
            page.goto(self.url, timeout=60000)
            page.wait_for_timeout(3000)
            
            self.hacer_scroll(page)
            valid_cards = self.extraer_cards(page)
            nuevos = self.extraer_anuncios(valid_cards)
            browser.close()
        log("[SCRAPING] Cerrando navegador...")
        
        for nuevo in reversed(nuevos):
            nuevo.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)
        return nuevos
                     

    def hacer_scroll(self, page):
        last_height = 0
        for _ in range(6): 
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)
            height = page.evaluate("document.body.scrollHeight")
            if height == last_height:
                break
            last_height = height
    
    
    def extraer_cards(self, page):
        cards = page.query_selector_all("div.relative.box-border")
        valid_cards = []
        for card in cards:
            links_en_card = card.query_selector_all(
                "a[href^='auto/usado/']"
            )
            hrefs = []

            for lk in links_en_card:
                href = lk.get_attribute("href")

                if href:
                    hrefs.append(href)
            if len(hrefs) >= 2 and len(set(hrefs)) == 1:
                valid_cards.append(card)

        return valid_cards
    

    def crear_anuncio(self, card):
        a = card.query_selector(
            "a[href^='auto/usado/']"
        )
        if not a:
            return None
        #IMAGEN
        # Intento 1: imagen dentro del <a>
        img = a.query_selector("img")

        # Intento 2: imagen dentro del card (fallback)
        if not img:
            img = card.query_selector("img")

        image_url = img.get_attribute("src") if img else None
        
        # LINK
        href = a.get_attribute("href")

        if not href:
            return None

        link = self.base_url + href

        # TITULO
        titulo_el = card.query_selector(
            "span.line-clamp-2"
        )

        titulo = (
            titulo_el.inner_text().strip()
            if titulo_el
            else "No encontrado"
        )
        
        # AÑO
        partes = titulo.split()
        anho = 0

        if partes[-1].isdigit():
            anho = int(partes[-1])
        
        # MARCA
        titulo_sin_año = " ".join(partes[:-1])
        MARCAS_ORDENADAS = sorted(MARCAS, key=len, reverse=True)
        
        marca_encontrada = "No encontrada"
        for marca in MARCAS_ORDENADAS:
            if titulo_sin_año.upper().startswith(marca):
                marca_encontrada = marca
                break
        
        # MODELO
        modelo = titulo_sin_año[len(marca_encontrada):].strip()
        
        # SPANS GENERALES
        spans = card.query_selector_all(
            "span.text-label-small"
        )

        # KM
        kilometraje = 0

        for s in spans:
            texto = s.inner_text().strip()

            if "km" in texto.lower():
                kilometraje = int(
                    texto
                    .replace("km", "")
                    .replace(",", "")
                    .strip()
                )
                break
        
        # TRANSMISION y COMBUSTIBLE
        transmision = "No encontrado"
        combustible = "No encontrado"

        combustibles_validos = [
            "gasolina",
            "diesel",
            "dual",
            "eléctrico",
            "híbrido",
            "gas glp"
            "glp",
            "gnv"
        ]

        for s in spans:

            title = s.get_attribute("title")

            if not title:
                continue

            title_lower = title.lower()

            # transmisión
            if (
                "autom" in title_lower
                or "mec" in title_lower
                or "secuencial" in title_lower
            ):
                transmision = title.strip()

            # combustible
            if title_lower in combustibles_validos:
                combustible = title.strip()
        
        # VENDEDOR
        vendedor_el = card.query_selector(
            "span.font-semibold"
        )

        vendedor = limpiar_texto(
            vendedor_el.inner_text()
            if vendedor_el
            else ""
        )
        
        # PRECIO
        precio_el = card.query_selector("div.text-title-large")
        precio_raw = (
            precio_el.inner_text()
            .replace("US$", "")
            .replace(",", "")
            .strip()
            if precio_el else "0"
        )
        
        try:
            precio = int(precio_raw)
        except:
            precio = 0
        
        anuncio = Anuncio(
            titulo=titulo,
            marca=marca_encontrada,
            modelo=modelo,
            anho=anho,
            precio=precio,
            kilometraje=kilometraje,
            transmision=transmision,
            combustible=combustible,
            vendedor=vendedor,
            link=link,
            imagen=image_url
        )
        
        anuncio.comprobar_datos_completos()
        
        return anuncio
        
        
    def extraer_anuncios(self, valid_cards):
        nuevos = []
        for card in valid_cards:
            anuncio = self.crear_anuncio(card)
            
            if anuncio == None:
                continue
            
            nuevos.append(anuncio)
            
        return nuevos

