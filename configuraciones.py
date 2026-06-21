# Configuracion del scraper
import os

# Selector de modos
MODO_PRUEBAS = True
MODO_HEADLESS = True
MODO_DEBUG = False
FILTRO_PRECIO = False


# CONSTANTES DE LA EJECUCION
URL = "https://neoauto.com/venta-de-autos-usados?sort=publication_desc"
BASE_URL = "https://neoauto.com/"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "Data", "anuncios.db")
DB_REGISTRY = os.path.join(BASE_DIR, "Data", "registro.db")
DB_PRICE = os.path.join(BASE_DIR, "Data", "precios.db")
DB_SEND = os.path.join(BASE_DIR, "Data", "envios.db")
DB_FILLER = os.path.join(BASE_DIR, "Data", "revision.db")
DB_ESTATES = os.path.join(BASE_DIR, "Data", "estados.db")


# Para conectarse con el bot y el chat del grupo de anuncios NeoAuto
TOKEN_PRUEBAS = "TU TOKEN" # PRUEBAS
TOKEN_PRODUCCION = "TU TOKEN" # PRODUCCION

CHAT_ID_PRUEBAS = "TU CHAT ID" # Prueba grupo privado

# Chat del grupo Anuncios #1
CHAT_ID_PRODUCCION = "TU CHAT ID"

# Logica de seleccion de modo debug
if MODO_PRUEBAS:
    TELEGRAM_TOKEN = TOKEN_PRUEBAS
    TELEGRAM_CHAT_ID = CHAT_ID_PRUEBAS
else:
    TELEGRAM_TOKEN = TOKEN_PRODUCCION
    TELEGRAM_CHAT_ID = CHAT_ID_PRODUCCION

# Intentos de reenvio
INTENTOS_REENVIO = 3

# Caracteres vacios a eliminar
CARACTERES_VACIOS = [
    "ㅤ",
    "\xa0",
    "\u200b"
]

# Arreglo de marcas a buscar
MARCAS = [
    "ACURA",
    "AGRALE",
    "ALFA ROMEO",
    "AMC",
    "ARO",
    "ASIA",
    "ASTON MARTIN",
    "AUDI",
    "AUSTIN",
    "AUTOCRAFT",
    "BAIC",
    "BAIC YINXIANG",
    "BAW",
    "BENTLEY",
    "BMW",
    "BRILLIANCE",
    "BUGGY",
    "BUICK",
    "BYD",
    "CADILLAC",
    "CAKY",
    "CATERHAM",
    "CERTIFICADO",
    "CHANGAN",
    "CHANGFENG",
    "CHANGHE",
    "CHERY",
    "CHEVROLET",
    "CHRYSLER",
    "CHUKY",
    "CITROEN",
    "CLUBCAR",
    "CNJ",
    "CUPRA",
    "DACIA",
    "DAEWOO",
    "DAIHATSU",
    "DATSUN",
    "DE SOTO",
    "DFSK",
    "DIM",
    "DODGE",
    "DONGFENG",
    "DS",
    "EAGLE",
    "EMGRAND",
    "FAW",
    "FERRARI",
    "FIAT",
    "FORD",
    "FOTON",
    "GAC",
    "GEELY",
    "GEO",
    "GMC",
    "GMW",
    "GOLDEN DRAGON",
    "GONOW",
    "GREAT WALL",
    "GURGEL",
    "HAFEI",
    "HAIMA",
    "HARLEY DAVIDSON",
    "HAVAL",
    "HILLMAN",
    "HONDA",
    "HUANG HAI",
    "HUDSON",
    "HUMMER",
    "HYUNDAI",
    "INCA POWER GONOW",
    "INCAPOWER",
    "INFINITI",
    "INTERNATIONAL",
    "ISUZU",
    "JAC",
    "JAGUAR",
    "JDMC",
    "JEEP",
    "JETOUR",
    "JIM",
    "JINBEI",
    "JINCHENG",
    "JMC",
    "JMEV",
    "JONWAY",
    "JOYLONG",
    "JOYNER",
    "KAIYI",
    "KAMA",
    "KARRY",
    "KEYTON",
    "KIA",
    "KING LONG",
    "KUMI",
    "KYC",
    "LADA",
    "LAMBORGHINI",
    "LANCIA",
    "LAND ROVER",
    "LANDWIND",
    "LEXUS",
    "LIEBAO",
    "LIFAN",
    "LIMOUSINE",
    "LINCOLN",
    "LOTUS",
    "MAHINDRA",
    "MASERATI",
    "MAXUS",
    "MAZDA",
    "MC LAREN",
    "MERCEDES-BENZ",
    "MERCURY",
    "MG",
    "MINI",
    "MITSUBISHI",
    "MORGAN",
    "MORRIS",
    "MORRIS GARAGES",
    "NISSAN",
    "NSU",
    "OLDSMOBILE",
    "OPEL",
    "PACKARD",
    "PEUGEOT",
    "PLYMOUTH",
    "POLARIS",
    "POLARSUN",
    "PONTIAC",
    "PORSCHE",
    "PROTON",
    "PUMA TAT",
    "RAM",
    "RAMBLER",
    "RENAULT",
    "REO",
    "RICH",
    "RMC",
    "ROLLS ROYCE",
    "ROUSH",
    "ROVER",
    "SAAB",
    "SAIC",
    "SAMSUNG",
    "SATURN",
    "SCION",
    "SEAT",
    "SEUNG HWA",
    "SHACMAN",
    "SHINERAY",
    "SIMCA",
    "SKODA",
    "SMA",
    "SMART",
    "SOUEAST",
    "SSANGYONG",
    "STUDEBAKER",
    "SUBARU",
    "SUZUKI",
    "SWM",
    "TATA",
    "TERRAMOTO",
    "TESLA",
    "TIANMA",
    "TOYOTA",
    "TRIUMPH",
    "TUBULAR",
    "VAUXHALL",
    "VGV",
    "VICTORY",
    "VOLKSWAGEN",
    "VOLVO",
    "WARRIOR",
    "WEICHAI",
    "WILLYS",
    "WULING",
    "XIAOMI",
    "XINKAI",
    "YEMA AUTO",
    "YUGO",
    "ZHONGXING",
    "ZNA",
    "ZOTYE",
    "ZXAUTO",
    "OTROS"
]

