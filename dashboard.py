import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from configuraciones import DB_FILE

# ============================================
# CONFIGURACION DE PAGINA
# ============================================

st.set_page_config(
    page_title="NeoAuto Dashboard",
    page_icon="🚗",
    layout="wide",
)

# ============================================
# CONEXION SQLITE
# ============================================

conn = sqlite3.connect(DB_FILE)

# ============================================
# CARGAR DATOS
# ============================================

df = pd.read_sql_query("""
SELECT *
FROM anuncios
ORDER BY Fecha_registro DESC
""", conn)

df["Fecha_registro"] = pd.to_datetime(
    df["Fecha_registro"]
)

# ============================================
# LIMPIEZA BASICA
# ============================================

df["Marca"] = df["Marca"].fillna("No encontrado")
df["Modelo"] = df["Modelo"].fillna("No encontrado")

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("⚙️ Filtros")

# MARCAS
marcas = ["TODAS"] + sorted(df["Marca"].unique().tolist())
modelo_seleccionado = "TODOS"

marca_seleccionada = st.sidebar.selectbox(
    "Marca",
    marcas
)

# MODELO
if marca_seleccionada != "TODAS":

    modelos_filtrados = df[
        df["Marca"] == marca_seleccionada
    ]

    modelos = ["TODOS"] + sorted(
        modelos_filtrados["Modelo"]
        .dropna()
        .unique()
        .tolist()
    )

    modelo_seleccionado = st.sidebar.selectbox(
        "Modelo",
        modelos
    )

# TRANSMISION
transmisiones = ["TODAS"] + sorted(df["Transmision"].unique().tolist())

transmision_seleccionada = st.sidebar.selectbox(
    "Transmisión",
    transmisiones
)

# COMBUSTIBLE
combustibles = ["TODAS"] + sorted(df["Combustible"].unique().tolist())

combustible_seleccionado = st.sidebar.selectbox(
    "Combustible",
    combustibles
)

# PRECIO
precio_min = int(df["Precio"].min())
precio_max = int(df["Precio"].max())

rango_precio = st.sidebar.slider(
    "Rango de precio",
    precio_min,
    precio_max,
    (precio_min, precio_max)
)

# ============================================
# FILTROS
# ============================================

df_filtrado = df.copy()

if marca_seleccionada != "TODAS":
    df_filtrado = df_filtrado[
        df_filtrado["Marca"] == marca_seleccionada
    ]


if transmision_seleccionada != "TODAS":
    df_filtrado = df_filtrado[
        df_filtrado["Transmision"] == transmision_seleccionada
    ]

if combustible_seleccionado != "TODAS":
    df_filtrado = df_filtrado[
        df_filtrado["Combustible"] == combustible_seleccionado
    ]

df_filtrado = df_filtrado[
    (df_filtrado["Precio"] >= rango_precio[0]) &
    (df_filtrado["Precio"] <= rango_precio[1])
]

# ============================================
# TITULO
# ============================================

st.title("🚗 NeoAuto Dashboard")

st.markdown("""
Dashboard de monitoreo y análisis de anuncios automotrices.
""")

if marca_seleccionada == "TODAS":

    st.info("📊 Datos para todas las marcas")

else:

    st.info(f"📊 Datos para {marca_seleccionada}")

# ============================================
# METRICAS
# ============================================

col0, col1, col2, col3, col4, col5 = st.columns(6)

with col0:
    st.metric(
        "Total anuncios",
        len(df_filtrado)
    )
    

with col1:
    hoy = pd.Timestamp.now().date()
    anuncios_hoy = df_filtrado[
        df_filtrado["Fecha_registro"].dt.date == hoy
    ]
    st.metric(
        "Anuncios de hoy",
        len(anuncios_hoy)
    )


with col2:
    df_order_hora = df_filtrado.sort_values(
        by="Fecha_registro",
        ascending=False
    )
    index_ultimo_anuncio = df_order_hora["Fecha_registro"].idxmax()
    ultimo_anuncio = df_order_hora['Fecha_registro'].loc[index_ultimo_anuncio]
    fecha_ultimo_anuncio = ultimo_anuncio.strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]
    hora_ultimo_anuncio = ultimo_anuncio.strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]
    
    st.metric(
        "Fecha ultimo anuncio(AAAA-MM-DD)",
        f"{fecha_ultimo_anuncio}"
    )

    
with col3:
    st.metric(
        "Hora ultimo anuncio",
        f"{hora_ultimo_anuncio}"
    )

    
with col4:
    if marca_seleccionada == "TODAS":
        st.metric(
            "Marca más frecuente",
            df_filtrado["Marca"].mode()[0]
        )
    else:
         st.metric(
            "Modelo más frecuente",
            df_filtrado["Modelo"].mode()[0]
        )


with col5:
    st.metric(
        "Precio mínimo",
        f"${int(df_filtrado['Precio'].min())}"
    )
    
    st.metric(
        "Precio máximo",
        f"${int(df_filtrado['Precio'].max())}"
    )


# ============================================
# TABS
# ============================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Estadísticas",
    "📈 Gráficos",
    "📋 Tabla",
    "🔍 Explorador"
])


# ============================================
# TAB 1
# ============================================

with tab1:
    if marca_seleccionada == "TODAS":

        st.subheader("Top marcas")

        marcas_count = (
            df_filtrado["Marca"]
            .value_counts()
            .head(10)
        )

        st.bar_chart(marcas_count)
        
        st.subheader("Promedio de precios por marca")
        promedio_marca = (
            df_filtrado
            .groupby("Marca")["Precio"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(promedio_marca)
        
        st.subheader(
            "Cantidad de anuncios por hora"
        )

        solo_hoy = st.toggle(
            "Solo anuncios de hoy",
            value=False
        )

        df_horas = df_filtrado.copy()

        # --------------------------------
        # FILTRAR SOLO HOY
        # --------------------------------

        if solo_hoy:

            hoy = pd.Timestamp.now().date()

            df_horas = df_horas[
                df_horas["Fecha_registro"].dt.date == hoy
            ]

        # --------------------------------
        # EXTRAER HORA
        # --------------------------------

        df_horas["Hora"] = (
            df_horas["Fecha_registro"]
            .dt.hour
        )

        # --------------------------------
        # FILTRAR HORAS
        # --------------------------------

        df_horas = df_horas[
            (df_horas["Hora"] >= 6) &
            (df_horas["Hora"] <= 23)
        ]

        # --------------------------------
        # CONTAR
        # --------------------------------

        anuncios_por_hora = (
            df_horas["Hora"]
            .value_counts()
            .sort_index()
        )

        # --------------------------------
        # GRAFICO
        # --------------------------------

        st.bar_chart(anuncios_por_hora)
                
        
    else:
        st.subheader("Top modelos")

        modelos_count = (
            df_filtrado["Modelo"]
            .value_counts()
            .head(10)
        )

        st.bar_chart(modelos_count)
        st.subheader("Promedio de precios por modelo")
        promedio_modelo = (
            df_filtrado
            .groupby("Modelo")["Precio"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(promedio_modelo)


# ============================================
# TAB 2
# ============================================

with tab2:

    if modelo_seleccionado != "TODOS":
        st.subheader(
            f"Evolución de precios del {modelo_seleccionado}"
        )
        df_evolucion_precio = df_filtrado[df_filtrado["Modelo"]==modelo_seleccionado]
        precios_por_anho = (
            df_evolucion_precio
            .groupby("Año")["Precio"]
            .mean()
            .sort_index()
        )
        st.line_chart(precios_por_anho)
        
        
        st.subheader(
            f"Dispersión Año vs Precio del {modelo_seleccionado}"
        )
        
        color_selector = st.radio(
            "Colorear puntos por:",
            ["Transmision", "Combustible"],
            horizontal=True
        )

        fig = px.scatter(
            df_evolucion_precio,
            x="Año",
            y="Precio",
            color=color_selector,
            hover_data=["Titulo"],
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        
        st.subheader("Transmisiones")

        transmisiones_count = (
            df_evolucion_precio["Transmision"]
            .value_counts()
        )

        st.bar_chart(transmisiones_count)
        
        
        st.subheader("Combustibles")
        combustibles_count = (
            df_evolucion_precio["Combustible"]
            .value_counts()
        )
        st.bar_chart(combustibles_count)

    else:
        st.subheader("Distribución de precios")

        st.line_chart(
            df_filtrado["Precio"]
        )

        st.subheader("Transmisiones")

        transmisiones_count = (
            df_filtrado["Transmision"]
            .value_counts()
        )

        st.bar_chart(transmisiones_count)

        st.subheader("Combustibles")
        combustibles_count = (
            df_filtrado["Combustible"]
            .value_counts()
        )
        st.bar_chart(combustibles_count)


# ============================================
# TAB 3
# ============================================

with tab3:

    st.subheader("Tabla de anuncios")
    if modelo_seleccionado != "TODOS":
        df_filtrado_modelos = df_filtrado[df_filtrado["Modelo"]==modelo_seleccionado]
        st.dataframe(
            df_filtrado_modelos,
            use_container_width=True
        )
        
    else:    
        st.dataframe(
            df_filtrado,
            use_container_width=True
        )


# ============================================
# TAB 4
# ============================================

with tab4:

    st.subheader("Buscar modelo")

    texto_busqueda = st.text_input(
        "Escribe un modelo"
    )

    if texto_busqueda:

        resultados = df_filtrado[
            df_filtrado["Modelo"]
            .str.contains(
                texto_busqueda,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            resultados,
            use_container_width=True
        )


# ============================================
# BOTON RECARGAR
# ============================================

if st.button("🔄 Recargar dashboard"):
    st.rerun()

# ============================================
# CERRAR CONEXION
# ============================================

conn.close()