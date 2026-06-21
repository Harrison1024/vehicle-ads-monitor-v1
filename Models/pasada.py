from datetime import datetime

class Pasada:
    def __init__(self):
        
        ahora = datetime.now()
        self.id:int | None = None
        self.hora_inicio = ahora.strftime("%H:%M:%S")
        self.ultima_pasada = self.hora_inicio
        self.numero_pasadas = 0
        self.fecha_pasada = ahora.strftime("%Y-%m-%d")
    
    def actualizar_pasada(self):
        hoy = datetime.now()
        hora = hoy.strftime("%H:%M:%S")
        self.ultima_pasada = hora
        self.numero_pasadas += 1

