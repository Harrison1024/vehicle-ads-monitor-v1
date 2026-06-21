import sqlite3
from configuraciones import DB_PRICE
from Models.anuncio import Anuncio


# ======================================================
# INICIALIZACIÓN DE LA BASE DE DATOS SQLITE DE PRECIOS
# ======================================================

def inicializar_db_precios():
    conn = sqlite3.connect(DB_PRICE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precios (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_anuncio INTEGER,
            Precio INTEGER,
            Fecha TEXT
        )
    ''')

    conn.commit()
    conn.close()
    
    

def guardar_precio_anuncio(anuncio:Anuncio):
    conn = sqlite3.connect(DB_PRICE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO precios (
            Id_anuncio,
            Precio,
            Fecha
        )
        VALUES(?, ?, ?)         
    ''',(
        anuncio.id,
        anuncio.precio,
        anuncio.fecha_registro
    ))
    
    id_precio = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return id_precio


def entregar_historial_precios(anuncio: Anuncio) -> list[tuple[int, int]]:
    conn = sqlite3.connect(DB_PRICE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Precio
        FROM precios
        WHERE Id_anuncio = ?
        ORDER BY Id
    """, (anuncio.id,))

    precios = cursor.fetchall()

    conn.close()

    return precios

