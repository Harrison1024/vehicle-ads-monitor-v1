import sqlite3
from configuraciones import DB_SEND
from Models.envio import Envio
from utilidades import log

# ======================================================
# INICIALIZACIÓN DE LA BASE DE DATOS SQLITE DE PASADAS
# ======================================================

def inicializar_db_envios():
    conn = sqlite3.connect(DB_SEND)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS envios (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha_envio TEXT,
            Id_anuncio INTEGER,
            Enviado BOOLEAN,
            Intentos INTEGER,
            Descripcion TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
 
 
# ================
# GUARDAR ENVIOS
# ================

def guardar_envios_db(envios:list[Envio]):
    if not envios:
        log("[SENDING] No se encontro ningun anuncios para enviar")
        return 
    
    conn = sqlite3.connect(DB_SEND)
    cursor = conn.cursor()
    count = 0
    for envio in envios:
        cursor.execute('''
            INSERT INTO envios (
                Fecha_envio,
                Id_anuncio,
                Enviado,
                Intentos,
                Descripcion
            )
            VALUES(?, ?, ?, ?, ?)         
        ''',(
            envio.fecha_envio,
            envio.anuncio.id,
            envio.enviado,
            envio.intentos,
            envio.descripcion
        ))
        
        if envio.enviado == True:
            count +=1
    
    conn.commit()
    conn.close()
    log(f"[SENDING] Anuncios enviados regitrados: {count}")
    log(f"[SENDING] Anuncios no enviados regitrados: {len(envios)-count}")
    
