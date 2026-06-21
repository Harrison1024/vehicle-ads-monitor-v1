from Models.anuncio import Anuncio
from utilidades import log

class Revision:
    def __init__(self):
        self.id:int
        self.anuncio:Anuncio
        self.fecha_revision = ""
        self.revisado = False
        self.num_revisiones = 0
        self.completado = False
        self.caido = False
        self.datos_recuperados : list[str] = [] 
        
        
    def completar_datos_faltantes(self, diccionario:dict):
        if self.anuncio.transmision == "No encontrado":
            self.anuncio.transmision = diccionario["Transmision"]
            self.datos_recuperados.append("Transmision")
            self.completado = True
            
        if self.anuncio.combustible == "No encontrado":
            self.anuncio.combustible = diccionario["Combustible"]
            self.datos_recuperados.append("Combustible")
            self.completado = True
        
        if self.anuncio.vendedor == "No encontrado":
            self.anuncio.vendedor = diccionario["Vendedor"]
            self.datos_recuperados.append("Vendedor")
            self.completado = True
            
    def imprimir_revision_anuncio(self):
        log(f"{self.anuncio.id} {self.anuncio.titulo} {self.anuncio.transmision} {self.anuncio.combustible} {self.anuncio.vendedor} {self.completado}")
        
