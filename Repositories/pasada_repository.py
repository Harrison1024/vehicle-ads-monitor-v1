import sqlite3
from configuraciones import DB_REGISTRY
from Models.pasada import Pasada
from utilidades import log

# ======================================================
# INICIALIZACIÓN DE LA BASE DE DATOS SQLITE DE PASADAS
# ======================================================

def inicializar_db_pasadas():
    conn = sqlite3.connect(DB_REGISTRY)
    cursor = conn.cursor()
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Hora_inicio TEXT,
            Ultima_pasada TEXT,
            Numero_pasadas INTEGER,
            Fecha_pasada TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


# =======================================================
# GUARDAR INICIO PROGRAMA: BASE DE DATOS SQLITE REGISTRO
# =======================================================

def guardar_inicio_db(pasada:Pasada):
    conn = sqlite3.connect(DB_REGISTRY)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO registro (
            Hora_inicio,
            Ultima_pasada,
            Numero_pasadas,
            Fecha_pasada
        )
        VALUES(?, ?, ?, ?)
    ''',(
        pasada.hora_inicio,
        pasada.ultima_pasada,
        pasada.numero_pasadas,
        pasada.fecha_pasada
    ))

    conn.commit()
    
    ultimo_id = cursor.lastrowid
    pasada.id = ultimo_id
    
    conn.close()
   

# ===========================================
# ACTUALIZAR ANUNCIOS: BASE DE DATOS SQLITE
# ===========================================

def actualizar_registro_db(pasada:Pasada):
    conn = sqlite3.connect(DB_REGISTRY)
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE registro
            SET Ultima_pasada = ?, Numero_pasadas = ?
            WHERE Id = ?
        ''', (
            pasada.ultima_pasada,
            pasada.numero_pasadas,
            pasada.id
        ))
    
    conn.commit()
    conn.close()
    
