from Models.anuncio import Anuncio

class Envio:
    def __init__(self, anuncio:Anuncio, tipo_anuncio:str):
        self.fecha_envio = ""
        self.anuncio = anuncio
        self.enviado = False
        self.intentos = 0
        self.tipo_anuncio = tipo_anuncio
        self.precio_id: int | None = None
        self.descripcion = ""
    
     