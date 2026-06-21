import sqlite3
from utilidades import *
from configuraciones import *
from datetime import datetime


def inicializar_db_estados():
    conn = sqlite3.connect(DB_ESTATES)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estados (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT UNIQUE,
            Activo INTEGER NOT NULL DEFAULT 0,
            Ultimo_inicio TEXT,
            Ultimo_final TEXT
        )
    ''')

    # Scraper:
    cursor.execute('''
        INSERT OR IGNORE INTO estados (
            Nombre,
            Activo,
            Ultimo_inicio,
            Ultimo_final
        )
        VALUES (?, ?, ?, ?)
    ''', (
        "Scraper",
        0,
        "",
        ""
    ))
    
    # Revisor:
    cursor.execute('''
        INSERT OR IGNORE INTO estados (
            Nombre,
            Activo,
            Ultimo_inicio,
            Ultimo_final
        )
        VALUES (?, ?, ?, ?)
    ''', (
        "Revisor",
        0,
        "",
        ""
    ))
    
    conn.commit()
    conn.close()


def obtener_estado(nombre:str):
    conn = sqlite3.connect(DB_ESTATES)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Activo
        FROM estados
        WHERE Nombre = ?
    """, (nombre,))

    resultado = cursor.fetchone()

    conn.close()

    return bool(resultado[0])


def activar(nombre:str):
    conn = sqlite3.connect(DB_ESTATES)
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE estados
        SET
            Activo = 1,
            Ultimo_inicio = ?
        WHERE Nombre = ?
    """, (fecha,nombre))

    conn.commit()
    conn.close()


def desactivar(nombre:str):
    conn = sqlite3.connect(DB_ESTATES)
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE estados
        SET
            Activo = 0,
            Ultimo_final = ?
        WHERE Nombre = ?
    """, (fecha, nombre))

    conn.commit()
    conn.close()
    
