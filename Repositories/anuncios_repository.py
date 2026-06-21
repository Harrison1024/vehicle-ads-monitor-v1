import sqlite3
from configuraciones import DB_FILE
from utilidades import log
from Models.anuncio import Anuncio
from Models.envio import Envio
from Models.revision import Revision
from Models.anuncio import Anuncio
from Repositories.prices_history import guardar_precio_anuncio

# =============================================
# INICIALIZACIÓN DE LA BASE DE DATOS ANUNCIOS
# =============================================

def inicializar_db_anuncios():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anuncios (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT,
            Marca TEXT,
            Modelo TEXT,
            Año INTEGER,
            Precio INTEGER,
            Kilometraje INTEGER,
            Transmision TEXT,
            Combustible TEXT,
            Vendedor TEXT,
            Link TEXT UNIQUE,
            Imagen TEXT,
            Fecha_registro TEXT,
            Datos_completos BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()


# ==================
# GUARDAR ANUNCIOS
# ==================

def guardar_anuncios_sqlite(nuevos:list[Anuncio]) -> list[Envio]:
    
    if not nuevos:
        log("[SELECTION] No se encontro ningun anuncio nuevo ni por actualizar")
        return []
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    anuncios_para_enviar = []
    nuevos_cout = 0
    actualizados_count=0
    for anuncio in nuevos:
        try:
            cursor.execute("""
                SELECT Id, Precio
                FROM anuncios
                WHERE Link = ?
            """, (anuncio.link,))

            resultado = cursor.fetchone()

            if resultado is None:
                anuncio.nuevo = True
                cursor.execute("""
                    INSERT INTO anuncios (
                        Titulo,
                        Marca,
                        Modelo,
                        Año,
                        Precio,
                        Kilometraje,
                        Transmision,
                        Combustible,
                        Vendedor,
                        Link,
                        Imagen,
                        Fecha_registro,
                        Datos_completos
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    anuncio.titulo,
                    anuncio.marca,
                    anuncio.modelo,
                    anuncio.anho,
                    anuncio.precio,
                    anuncio.kilometraje,
                    anuncio.transmision,
                    anuncio.combustible,
                    anuncio.vendedor,
                    anuncio.link,
                    anuncio.imagen,
                    anuncio.fecha_registro,
                    anuncio.datos_completos
                ))
                
                id_generado = cursor.lastrowid
                conn.commit()
                               
                anuncio.id = id_generado
                
                envio = Envio(anuncio, "nuevo")
                envio.precio_id = guardar_precio_anuncio(anuncio)
                
                anuncios_para_enviar.append(envio)
                nuevos_cout += 1

            else:
                anuncio.nuevo = False
                anuncio.id = resultado[0]             
                precio_viejo = int(resultado[1])
                precio_nuevo = int(anuncio.precio)

                if precio_viejo != precio_nuevo:         

                    cursor.execute("""
                        UPDATE anuncios
                        SET Precio = ?
                        WHERE Link = ?
                    """, (
                        precio_nuevo,
                        anuncio.link
                    ))
                    conn.commit()
                    envio = Envio(anuncio, "actualizado")
                    envio.precio_id = guardar_precio_anuncio(anuncio)                      
                    anuncios_para_enviar.append(envio)
                    actualizados_count += 1

        except Exception as e:
            log(f"[ERROR] Error al procesar anuncio con link {anuncio.link}: {e}")
            continue
  
    conn.close()
    
    log(f"[SELECTION] Anuncios nuevos guardados sin enviar: {nuevos_cout}")
    log(f"[SELECTION] Anuncios actualizados: {actualizados_count}")
    log(f"[SELECTION] Lista de anuncios por enviar: {len(anuncios_para_enviar)}")
    return anuncios_para_enviar


# ===========================
# COMPLETAR DATOS FALTANTES
# ===========================

def completar_datos_anuncio(lista_revisados:list[Revision]):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor() 
    count = 0
    for revision in lista_revisados:

        if revision.datos_recuperados:

            campos = {
                "Transmision": revision.anuncio.transmision,
                "Combustible": revision.anuncio.combustible,
                "Vendedor": revision.anuncio.vendedor
            }

            for dato in revision.datos_recuperados:

                if dato not in campos:
                    continue

                try:
                    cursor.execute(
                        f"""
                        UPDATE anuncios
                        SET {dato} = ?
                        WHERE Id = ?
                        """,
                        (
                            campos[dato],
                            revision.anuncio.id
                        )
                    )
                    conn.commit()

                except Exception as e:
                    log(
                        f"[ERROR] Error al actualizar datos "
                        f"del anuncio con id {revision.anuncio.id}: {e}"
                    )

        datos_completados = (
            revision.anuncio.transmision != "No encontrado"
            and revision.anuncio.combustible != "No encontrado"
            and revision.anuncio.vendedor != "No encontrado"
        )
        if datos_completados == True:
            count+=1

        try:
            cursor.execute("""
                UPDATE anuncios
                SET Datos_completos = ?
                WHERE Id = ?
            """, (
                int(datos_completados),
                revision.anuncio.id
            ))
            conn.commit()

        except Exception as e:
            log(
                f"[ERROR] Error al actualizar "
                f"Datos_completos del anuncio "
                f"{revision.anuncio.id}: {e}"
            )
 
    
    conn.close()
    log(f"[REVISION] Anucios completados: {count}")


# =============================
# OBTENER ANUNCIOS INCOMPLETOS
# =============================

def obtener_anuncios_incompletos() -> list[Revision]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Id,
            Titulo,
            Marca,
            Modelo,
            Año,
            Precio,
            Kilometraje,
            Transmision,
            Combustible,
            Vendedor,
            Link,
            Imagen,
            Fecha_registro,
            Datos_completos
        FROM anuncios
        WHERE Datos_completos = 0
    """)

    resultados = cursor.fetchall()

    conn.close()

    lista_revision = []

    for fila in resultados:

        anuncio = Anuncio(
            fila[1],
            fila[2],
            fila[3],
            fila[4],
            fila[5],
            fila[6],
            fila[7],
            fila[8],
            fila[9],
            fila[10],
            fila[11]
        )

        anuncio.id = fila[0]
        anuncio.fecha_registro = fila[12]
        anuncio.datos_completos = bool(fila[13])

        revision = Revision()
        revision.anuncio = anuncio

        lista_revision.append(revision)

    if not lista_revision:
        log(f"[REVISION] No hay anuncios incompletos")
        return []
        
    log(f"[REVISION] Anuncios incompletos encontrados: {len(lista_revision)}")

    return lista_revision
    
