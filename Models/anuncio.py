from datetime import datetime

class Anuncio:
    def __init__(
        self,
        titulo: str,
        marca: str,
        modelo: str,
        anho: int,
        precio: int,
        kilometraje: int,
        transmision: str,
        combustible: str,
        vendedor: str,
        link: str,
        imagen: str | None,
        
    ):
        
        self.titulo = titulo
        self.marca = marca
        self.modelo = modelo
        self.anho = anho
        self.precio = precio
        self.kilometraje = kilometraje
        self.transmision = transmision
        self.combustible = combustible
        self.vendedor = vendedor
        self.link = link
        self.imagen = imagen
        self.id: int | None = None
        self.fecha_registro: str | None = None
        self.datos_completos = False
        self.nuevo: bool | None = None
 
    def comprobar_datos_completos(self):
        self.datos_completos = True
        
        if self.titulo == "No encontrado":
            self.datos_completos = False
        elif self.marca == "No encontrado":
            self.datos_completos = False
        elif self.modelo == "No encontrado":
            self.datos_completos = False
        elif self.anho == "No encontrado":
            self.datos_completos = False
        elif self.precio == "No encontrado":
            self.datos_completos = False
        elif self.kilometraje == "No encontrado":
            self.datos_completos = False    
        elif self.transmision == "No encontrado":
            self.datos_completos = False    
        elif self.combustible == "No encontrado":
            self.datos_completos = False    
        elif self.vendedor == "No encontrado":
            self.datos_completos = False
        elif self.link == "No encontrado":
            self.datos_completos = False
        else:
            pass

