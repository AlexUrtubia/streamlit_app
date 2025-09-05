import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# COnfiguración inicial app
st.set_page_config(page_title="Alojamientos Turísticos en Chile", layout="wide")
st.title("Alojamientos Turísticos en Chile")
st.caption("Visualización interactiva de alojamientos turísticos registrados por SERNATUR.")

# Parámetros de la API
RESOURCE_ID = "85f6d5c5-6ae6-4d99-b20d-9d88d04c7b64"
API_URL = "https://datos.gob.cl/api/3/action/datastore_search"
params = {"resource_id": RESOURCE_ID, "limit": 4500}

# Descarga y prepara datos, guarda en caché
@st.cache_data(show_spinner="Descargando datos...", ttl=3600)
def load_data():
    resp = requests.get(API_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()["result"]["records"]
    df = pd.DataFrame(data) # Crea dataframe
    df.columns = df.columns.str.strip() # Quita espacios en datos
    return df

# Intento de carga de datos, levanta error si falla
try:
    df = load_data()
except Exception as e:
    st.error(f"Error al descargar datos: {e}")
    st.stop()

# Concatena dirección
df["Dirección"] = df.get("Direccion Calle", "") + " " + df.get("Num", "").fillna("")
# Selección de columnas a mostrar
cols = [
    "Region", "Provincia", "Comuna", "Nombre del Establecimiento",
    "Dirección", "Telefono", "Web", "CLASE"
]
cols_presentes = [c for c in cols if c in df.columns]
df_show = df[cols_presentes] if cols_presentes else df

# Limpia filas vacías
df_show = df_show.dropna(how="all")

# Filtros interactivos
st.subheader("Filtros")
col1, col2, col3 = st.columns(3)

# Filtra de manera dinámica según Región > Provincia > Comuna
with col1:
    regiones = ["Todas"] + sorted(df_show["Region"].dropna().unique())
    region_sel = st.selectbox("Región", regiones, index=0)

with col2:
    prov_df = df_show if region_sel == "Todas" else df_show[df_show["Region"] == region_sel]
    provincias = ["Todas"] + sorted(prov_df["Provincia"].dropna().unique())
    provincia_sel = st.selectbox("Provincia", provincias, index=0)

with col3:
    comuna_df = prov_df if provincia_sel == "Todas" else prov_df[prov_df["Provincia"] == provincia_sel]
    comunas = ["Todas"] + sorted(comuna_df["Comuna"].dropna().unique())
    comuna_sel = st.selectbox("Comuna", comunas, index=0)

# Aplica filtros al dataframe
filtrado = df_show.copy()
if region_sel != "Todas":
    filtrado = filtrado[filtrado["Region"] == region_sel]
if provincia_sel != "Todas":
    filtrado = filtrado[filtrado["Provincia"] == provincia_sel]
if comuna_sel != "Todas":
    filtrado = filtrado[filtrado["Comuna"] == comuna_sel]

# Muestra tabla de datos filtrados
st.subheader("Tabla de Alojamientos")
st.dataframe(filtrado, use_container_width=True, height=400)

# Gráfica clases de alojamiento
st.subheader("Cantidad de alojamientos por tipo (CLASE)")
if not filtrado.empty and "CLASE" in filtrado.columns:
    clase_counts = filtrado["CLASE"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(clase_counts.index, clase_counts.values)
    ax.set_xlabel("Clase")
    ax.set_ylabel("Cantidad")
    ax.tick_params(axis='x', labelsize=8) 
    plt.xticks(rotation=30, ha="right")
    ax.grid(axis="y", alpha=0.2)
    st.pyplot(fig)
else:
    st.info("No se encontraron alojamientos para este filtro.")

