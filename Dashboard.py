# PARA EJECUTAR : streamlit run Dashboard.py o py -m streamlit run Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Fútbol Argentino",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    try:
        # Si el archivo está en la misma carpeta
        df = pd.read_excel('futbolargentino.xlsx')
        
        # Limpieza básica de datos
        df['Valor de mercado'] = pd.to_numeric(df['Valor de mercado'], errors='coerce')
        df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
        df['Altura'] = pd.to_numeric(df['Altura'], errors='coerce')
        df['Temporada'] = pd.to_numeric(df['Temporada'], errors='coerce')
        
        # Convertir fecha de fichaje
        df['Fichado'] = pd.to_datetime(df['Fichado'], errors='coerce')
        df['Año Fichaje'] = df['Fichado'].dt.year
        
        # Limpiar columnas categóricas - convertir a string y manejar NaN
        df['Club'] = df['Club'].astype(str)
        df['Posicion'] = df['Posicion'].astype(str)
        df['Pie'] = df['Pie'].astype(str)
        df['Equipo Anterior'] = df['Equipo Anterior'].astype(str)
        
        # Reemplazar 'nan' strings por NaN
        df = df.replace('nan', np.nan)
        
        return df
    except FileNotFoundError:
        st.error(" No se pudo encontrar el archivo 'futbolargentino.xlsx'")
        st.info(" Asegúrate de que el archivo esté en la misma carpeta que este script")
        return None

# Cargar datos
df = load_data()

# Sidebar para navegación
st.sidebar.title("⚽ Dashboard Fútbol Argentino")
st.sidebar.markdown("---")

# Botones de navegación
page = st.sidebar.radio(
    "Navegación",
    [" Introducción", " Dashboard Completo"]
)

# Página de Introducción
if page == " Introducción":
    st.title("Análisis del Fútbol Argentino (2008-2022)")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(" Descripción del Dashboard")
        st.markdown("""
        Este dashboard analiza datos completos de jugadores del fútbol argentino desde 2008 hasta 2022, 
        incluyendo información de **18 equipos** que más temporadas han jugado en primera división.
        
        ###  Datos Incluidos:
        - **Información de jugadores**: Nombre, posición, edad, altura
        - **Valores de mercado**: Evolución financiera de los jugadores
        - **Datos de fichajes**: Fechas y equipos anteriores
        - **Características físicas**: Altura y pie dominante
        - **Información por temporada**: Datos desde 2008 a 2022
        
        ###  Objetivos del Análisis:
        1. Identificar patrones en el mercado de fichajes
        2. Analizar la relación entre edad, posición y valor
        3. Comparar estrategias de los diferentes clubes
        4. Seguir la evolución del fútbol argentino
        """)
    
    with col2:
        if df is not None:
            st.metric("Total Jugadores", f"{len(df):,}")
            st.metric("Temporadas Analizadas", f"{df['Temporada'].nunique()}")
            st.metric("Clubs Incluidos", f"{df['Club'].nunique()}")
            st.metric("Valor Promedio", f"${df['Valor de mercado'].mean():,.0f}")
    
    st.markdown("---")
    
    st.header(" Métricas Clave del Dataset")
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            edad_promedio = df['Edad'].mean()
            st.metric("Edad Promedio", f"{edad_promedio:.1f} años")
        
        with col2:
            altura_promedio = df['Altura'].mean()
            st.metric("Altura Promedio", f"{altura_promedio:.2f} m")
        
        with col3:
            pie_data = df['Pie'].value_counts()
            pie_dominante = pie_data.index[0] if len(pie_data) > 0 else "N/A"
            st.metric("Pie Dominante", pie_dominante)
        
        with col4:
            posicion_data = df['Posicion'].value_counts()
            posicion_comun = posicion_data.index[0] if len(posicion_data) > 0 else "N/A"
            st.metric("Posición Más Común", posicion_comun)
        
        # Gráfico rápido de preview
        st.subheader("📈 Vista Previa de los Datos")
        
        tab1, tab2 = st.tabs(["Distribución de Edades", "Top Posiciones"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 4))
            df['Edad'].hist(bins=20, ax=ax, alpha=0.7, color='skyblue')
            ax.set_xlabel('Edad')
            ax.set_ylabel('Frecuencia')
            ax.set_title('Distribución de Edades de los Jugadores')
            st.pyplot(fig)
        
        with tab2:
            posiciones_count = df['Posicion'].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(10, 4))
            posiciones_count.plot(kind='bar', ax=ax, color='lightgreen', alpha=0.7)
            ax.set_xlabel('Posición')
            ax.set_ylabel('Cantidad de Jugadores')
            ax.set_title('Top 10 Posiciones Más Comunes')
            plt.xticks(rotation=45)
            st.pyplot(fig)

# Página del Dashboard Completo
elif page == " Dashboard Completo":
    if df is None:
        st.error("No hay datos disponibles. Por favor, verifica que el archivo esté en la ubicación correcta.")
        st.stop()
    
    st.title(" Dashboard Completo - Fútbol Argentino")
    st.markdown("---")
    
    # Filtros en sidebar
    st.sidebar.header("🔧 Filtros")
    
    # Filtro por temporada
    temporadas = sorted(df['Temporada'].dropna().unique())
    selected_seasons = st.sidebar.multiselect(
        "Seleccionar Temporadas",
        options=temporadas,
        default=temporadas[-3:] if len(temporadas) > 2 else temporadas
    )
    
    # Filtro por club - manejar posibles valores NaN
    clubs_data = df['Club'].dropna().unique()
    clubs = sorted([str(club) for club in clubs_data])
    selected_clubs = st.sidebar.multiselect(
        "Seleccionar Clubs",
        options=clubs,
        default=clubs[:3] if len(clubs) > 2 else clubs
    )
    
    # Filtro por posición - manejar posibles valores NaN
    posiciones_data = df['Posicion'].dropna().unique()
    posiciones = sorted([str(pos) for pos in posiciones_data])
    selected_positions = st.sidebar.multiselect(
        "Seleccionar Posiciones",
        options=posiciones,
        default=posiciones[:3] if len(posiciones) > 2 else posiciones
    )
    
    # Aplicar filtros
    filtered_df = df.copy()
    if selected_seasons:
        filtered_df = filtered_df[filtered_df['Temporada'].isin(selected_seasons)]
    if selected_clubs:
        filtered_df = filtered_df[filtered_df['Club'].isin(selected_clubs)]
    if selected_positions:
        filtered_df = filtered_df[filtered_df['Posicion'].isin(selected_positions)]
    
    # Mostrar estadísticas de filtrado
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jugadores Filtrados", len(filtered_df))
    with col2:
        valor_promedio = filtered_df['Valor de mercado'].mean()
        st.metric("Valor Promedio Filtrado", f"${valor_promedio:,.0f}" if not pd.isna(valor_promedio) else "N/A")
    with col3:
        edad_promedio = filtered_df['Edad'].mean()
        st.metric("Edad Promedio Filtrada", f"{edad_promedio:.1f} años" if not pd.isna(edad_promedio) else "N/A")
    with col4:
        st.metric("Clubs Incluidos", filtered_df['Club'].nunique())
    
    st.markdown("---")
    
    # Pestañas para diferentes análisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Perfil de Jugadores", 
        "💰 Valor de Mercado", 
        "🏟️ Equipos y Fichajes",
        "📈 Evolución Temporal"
    ])
    
    with tab1:
        st.header(" Perfil de los Jugadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de edades
            st.subheader("Distribución de Edades")
            fig = px.histogram(
                filtered_df, x='Edad', nbins=20,
                title='Distribución de Edades de los Jugadores',
                color_discrete_sequence=['skyblue']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Pie dominante
            st.subheader("Pie Dominante")
            pie_data = filtered_df['Pie'].value_counts()
            if len(pie_data) > 0:
                fig = px.pie(
                    values=pie_data.values, names=pie_data.index,
                    title='Distribución del Pie Dominante'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de pie dominante para los filtros seleccionados")
        
        with col2:
            # Altura por posición
            st.subheader("Altura Promedio por Posición")
            altura_posicion = filtered_df.groupby('Posicion')['Altura'].mean().dropna().sort_values(ascending=True)
            if len(altura_posicion) > 0:
                fig = px.bar(
                    x=altura_posicion.values, y=altura_posicion.index,
                    orientation='h',
                    title='Altura Promedio por Posición',
                    color=altura_posicion.values,
                    color_continuous_scale='viridis'
                )
                fig.update_layout(xaxis_title='Altura Promedio (m)', yaxis_title='Posición')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de altura para los filtros seleccionados")
            
            # Relación edad vs altura
            st.subheader("Relación Edad vs Altura")
            scatter_data = filtered_df.dropna(subset=['Edad', 'Altura'])
            if len(scatter_data) > 0:
                fig = px.scatter(
                    scatter_data, x='Edad', y='Altura', color='Posicion',
                    title='Edad vs Altura por Posición',
                    opacity=0.6
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para mostrar la relación edad vs altura")
    
    with tab2:
        st.header(" Análisis del Valor de Mercado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 jugadores más valiosos
            st.subheader("Top 10 Jugadores Más Valiosos")
            top_players_data = filtered_df.dropna(subset=['Valor de mercado']).nlargest(10, 'Valor de mercado')
            if len(top_players_data) > 0:
                fig = px.bar(
                    top_players_data, x='Valor de mercado', y='Jugadores',
                    orientation='h',
                    title='Top 10 Jugadores por Valor de Mercado',
                    color='Valor de mercado',
                    color_continuous_scale='thermal',
                    hover_data=['Posicion', 'Club']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de valor de mercado para los filtros seleccionados")
            
            # Valor por posición (boxplot)
            st.subheader("Distribución del Valor por Posición")
            boxplot_data = filtered_df.dropna(subset=['Valor de mercado', 'Posicion'])
            if len(boxplot_data) > 0:
                fig = px.box(
                    boxplot_data, x='Posicion', y='Valor de mercado',
                    title='Distribución del Valor de Mercado por Posición'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para el boxplot")
        
        with col2:
            # Valor total por club
            st.subheader("Valor Total por Club")
            valor_club_data = filtered_df.groupby('Club')['Valor de mercado'].sum().dropna().sort_values(ascending=True)
            if len(valor_club_data) > 0:
                fig = px.bar(
                    x=valor_club_data.values, y=valor_club_data.index,
                    orientation='h',
                    title='Valor Total del Plantel por Club',
                    color=valor_club_data.values,
                    color_continuous_scale='sunset'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de valor por club para los filtros seleccionados")
            
            # Relación edad vs valor
            st.subheader("Relación Edad vs Valor de Mercado")
            scatter_valor_data = filtered_df.dropna(subset=['Edad', 'Valor de mercado', 'Altura'])
            if len(scatter_valor_data) > 0:
                fig = px.scatter(
                    scatter_valor_data, x='Edad', y='Valor de mercado', 
                    color='Posicion', size='Altura',
                    title='Edad vs Valor de Mercado (tamaño: altura)',
                    opacity=0.6,
                    hover_data=['Jugadores', 'Club']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para mostrar la relación edad vs valor")
    
    with tab3:
        st.header(" Análisis de Equipos y Fichajes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de posiciones por club
            st.subheader("Distribución de Posiciones por Club")
            posicion_club_data = filtered_df.dropna(subset=['Club', 'Posicion'])
            if len(posicion_club_data) > 0:
                posicion_club = pd.crosstab(posicion_club_data['Club'], posicion_club_data['Posicion'])
                fig = px.imshow(
                    posicion_club,
                    title='Distribución de Posiciones por Club (Heatmap)',
                    aspect='auto',
                    color_continuous_scale='blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para el heatmap")
            
            # Cantidad de jugadores por club
            st.subheader("Cantidad de Jugadores por Club")
            jugadores_club_data = filtered_df['Club'].value_counts()
            if len(jugadores_club_data) > 0:
                fig = px.bar(
                    x=jugadores_club_data.values, y=jugadores_club_data.index,
                    orientation='h',
                    title='Número de Jugadores por Club',
                    color=jugadores_club_data.values,
                    color_continuous_scale='greens'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de jugadores por club")
        
        with col2:
            # Equipos anteriores más comunes
            st.subheader("Equipos Anteriores Más Comunes")
            equipos_anteriores_data = filtered_df['Equipo Anterior'].dropna().value_counts().head(15)
            if len(equipos_anteriores_data) > 0:
                fig = px.bar(
                    x=equipos_anteriores_data.values, y=equipos_anteriores_data.index,
                    orientation='h',
                    title='Top 15 Equipos Anteriores Más Comunes',
                    color=equipos_anteriores_data.values,
                    color_continuous_scale='purples'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de equipos anteriores")
            
            # Análisis de inferiores vs externos
            st.subheader("Procedencia de Jugadores")
            filtered_df['EsInferiores'] = filtered_df['Equipo Anterior'].str.contains('Inferiores', na=False)
            inferiores_count = filtered_df['EsInferiores'].value_counts()
            if len(inferiores_count) > 0:
                fig = px.pie(
                    values=inferiores_count.values, 
                    names=['Externos', 'Inferiores'],
                    title='Proporción de Jugadores de Inferiores vs Externos'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de procedencia de jugadores")
    
    with tab4:
        st.header(" Evolución Temporal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolución del valor promedio
            st.subheader("Evolución del Valor Promedio")
            valor_temporal_data = filtered_df.groupby('Temporada')['Valor de mercado'].mean().dropna()
            if len(valor_temporal_data) > 0:
                fig = px.line(
                    x=valor_temporal_data.index, y=valor_temporal_data.values,
                    title='Evolución del Valor de Mercado Promedio',
                    markers=True
                )
                fig.update_layout(xaxis_title='Temporada', yaxis_title='Valor Promedio')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos temporales de valor")
            
            # Fichajes por año
            st.subheader("Fichajes por Año")
            if 'Año Fichaje' in filtered_df.columns:
                fichajes_anio_data = filtered_df['Año Fichaje'].dropna().value_counts().sort_index()
                if len(fichajes_anio_data) > 0:
                    fig = px.line(
                        x=fichajes_anio_data.index, y=fichajes_anio_data.values,
                        title='Evolución de Fichajes por Año',
                        markers=True
                    )
                    fig.update_layout(xaxis_title='Año', yaxis_title='Número de Fichajes')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay datos de fichajes por año")
        
        with col2:
            # Evolución de la edad promedio
            st.subheader("Evolución de la Edad Promedio")
            edad_temporal_data = filtered_df.groupby('Temporada')['Edad'].mean().dropna()
            if len(edad_temporal_data) > 0:
                fig = px.line(
                    x=edad_temporal_data.index, y=edad_temporal_data.values,
                    title='Evolución de la Edad Promedio',
                    markers=True,
                    line_shape='spline'
                )
                fig.update_layout(xaxis_title='Temporada', yaxis_title='Edad Promedio')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos temporales de edad")
            
            # Heatmap de fichajes por temporada y club
            st.subheader("Fichajes por Temporada y Club")
            heatmap_data = filtered_df.dropna(subset=['Temporada', 'Club'])
            if len(heatmap_data) > 0:
                fichajes_heatmap = pd.crosstab(heatmap_data['Temporada'], heatmap_data['Club'])
                if len(fichajes_heatmap) > 0:
                    fig = px.imshow(
                        fichajes_heatmap,
                        title='Fichajes por Temporada y Club',
                        aspect='auto',
                        color_continuous_scale='reds'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay datos para el heatmap temporal")
    
    # Sección de datos crudos
    st.markdown("---")
    st.header("📋 Datos Filtrados")
    
    with st.expander("Ver datos completos filtrados"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # Opción de descarga
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar datos filtrados como CSV",
            data=csv,
            file_name="futbol_argentino_filtrado.csv",
            mime="text/csv"
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Dashboard creado para análisis del fútbol argentino**\n"
    "Datos: Transfermarkt (2008-2022)"
)