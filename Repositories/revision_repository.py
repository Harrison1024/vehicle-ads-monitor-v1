import sqlite3
from configuraciones import DB_FILLER
from Models.anuncio import Anuncio
from Models.revision import Revision
from utilidades import log


# ======================================================
# INICIALIZACIÓN DE LA BASE DE DATOS SQLITE DE PRECIOS
# ======================================================

def inicializar_db_revision():
    conn = sqlite3.connect(DB_FILLER)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revision (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_anuncio INTEGER,
            Link_anuncio TEXT,
            Fecha_revision TEXT,
            Revisado BOOLEAN,
            Numero_revisiones INTEGER,
            Completado BOOLEAN,
            Caido BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()


def guardar_revision(revision:Revision):
    conn = sqlite3.connect(DB_FILLER)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO revision (
            Id_anuncio,
            Link_anuncio,
            Fecha_revision,
            Revisado,
            Numero_revisiones,
            Completado,
            Caido
        )
        VALUES(?, ?, ?, ?, ?, ?, ?)         
    ''',(
        revision.anuncio.id,
        revision.anuncio.link,
        revision.fecha_revision,
        revision.revisado,
        revision.num_revisiones,
        revision.completado,
        revision.caido
    ))
    
    conn.commit()
    conn.close()
    
    
def guardar_lista_revisados(lista_revisados:list[Revision]):
    if not lista_revisados:
        return []
    
    conn = sqlite3.connect(DB_FILLER)
    cursor = conn.cursor()
    
    for revision in lista_revisados:
        cursor.execute('''
            INSERT INTO revision (
                Id_anuncio,
                Link_anuncio,
                Fecha_revision,
                Revisado,
                Numero_revisiones,
                Completado,
                Caido
            )
            VALUES(?, ?, ?, ?, ?, ?, ?)         
        ''',(
            revision.anuncio.id,
            revision.anuncio.link,
            revision.fecha_revision,
            revision.revisado,
            revision.num_revisiones,
            revision.completado,
            revision.caido
        ))
    log(f"[SAVE] Se guardo un total {len(lista_revisados)}")
    conn.commit()
    conn.close()
    
