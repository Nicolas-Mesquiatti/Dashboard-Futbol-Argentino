# PARA EJECUTAR : streamlit run Dashboard.py o py -m streamlit run Dashboard.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Dashboard Fútbol Argentino",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FONTS_CSS = """<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">"""
BASE_STYLE = """<style>*{box-sizing:border-box;margin:0;padding:0;}body{background:transparent;font-family:'DM Sans',sans-serif;color:#f0fdf4;overflow:hidden;}</style>"""

# ─── CUSTOM CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap');
    #MainMenu, footer, header, .stDeployButton {display: none !important; visibility: hidden !important;}
    [data-testid="stHeader"] { background: transparent !important; }
    .stApp, [data-testid="stAppViewContainer"], .main .block-container,
    [data-testid="stMainBlockContainer"] {
        background-color: #060e0a !important; color: #f0fdf4;
    }
    .block-container, [data-testid="stMainBlockContainer"] { padding-top: 0 !important; max-width: 1400px !important; }
    [data-testid="stSidebar"] { background: rgba(6,14,10,0.97) !important; border-right: 1px solid rgba(74,222,128,0.14) !important; }
    [data-testid="stSidebar"] * { color: #f0fdf4 !important; }
    [data-testid="stSidebar"] label { color: #4ade80 !important; font-weight: 600 !important; font-size: 11px !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div { background: rgba(10,20,13,0.88) !important; border: 1px solid rgba(74,222,128,0.2) !important; border-radius: 10px !important; }
    [data-testid="stSidebar"] [data-baseweb="tag"] { background: rgba(34,197,94,0.2) !important; border: 1px solid rgba(74,222,128,0.3) !important; }
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid rgba(30,52,38,0.9) !important; gap: 8px !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(10,20,13,0.5) !important; color: #5a9070 !important;
        border: 1px solid rgba(30,52,38,0.9) !important; border-bottom: none !important;
        border-radius: 10px 10px 0 0 !important; padding: 10px 24px !important;
        font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 13px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(10,20,13,0.88) !important; color: #4ade80 !important;
        border-color: rgba(74,222,128,0.3) !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }
    .stPlotlyChart { background: transparent !important; }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22c55e, #15803d) !important;
        color: #f0fdf4 !important; border: none !important; border-radius: 10px !important;
        font-weight: 700 !important; padding: 10px 24px !important;
    }
    .stDownloadButton > button:hover { box-shadow: 0 0 24px rgba(34,197,94,0.4) !important; }
    [data-testid="stExpander"] { border: 1px solid rgba(30,52,38,0.9) !important; border-radius: 12px !important; background: rgba(10,20,13,0.5) !important; }
    [data-testid="stExpander"] summary { color: #4ade80 !important; }
    [data-testid="stExpander"] summary span { color: #4ade80 !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #060e0a; }
    ::-webkit-scrollbar-thumb { background: #22c55e; border-radius: 3px; }
    iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)


PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="DM Sans, sans-serif", color="#5a9070", size=11),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor='rgba(30,52,38,0.6)', zerolinecolor='rgba(30,52,38,0.6)'),
    yaxis=dict(gridcolor='rgba(30,52,38,0.6)', zerolinecolor='rgba(30,52,38,0.6)'),
    hoverlabel=dict(bgcolor='#0a140d', bordercolor='rgba(74,222,128,0.3)', font=dict(color='#f0fdf4', family='DM Sans')),
)

GREEN_SEQ = ['#4ade80', '#22c55e', '#16a34a', '#15803d', '#166534', '#14532d', '#0f3d1f']
GOLD = '#fbbf24'
BLUE_AR = '#74acdf'
GREEN_ACCENT = '#4ade80'


@st.cache_data
def load_data():
    try:
        df = pd.read_excel('futbolargentino.xlsx')
        df['Valor de mercado'] = pd.to_numeric(df['Valor de mercado'], errors='coerce')
        df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
        df['Altura'] = pd.to_numeric(df['Altura'], errors='coerce')
        df['Temporada'] = pd.to_numeric(df['Temporada'], errors='coerce')
        df['Fichado'] = pd.to_datetime(df['Fichado'], errors='coerce')
        df['Año Fichaje'] = df['Fichado'].dt.year
        df['Club'] = df['Club'].astype(str)
        df['Posicion'] = df['Posicion'].astype(str)
        df['Pie'] = df['Pie'].astype(str)
        df['Equipo Anterior'] = df['Equipo Anterior'].astype(str)
        df = df.replace('nan', np.nan)
        return df
    except FileNotFoundError:
        st.error("No se pudo encontrar el archivo 'futbolargentino.xlsx'")
        return None


df = load_data()
if df is None:
    st.stop()

CLUB_COLORS = {
    'River Plate': {'ring': '#e3001b', 'bg': '#180008'},
    'Boca Juniors': {'ring': '#f5c400', 'bg': '#00144a'},
    'Racing Club': {'ring': '#74b4d4', 'bg': '#001234'},
    'Independiente': {'ring': '#cc0000', 'bg': '#180000'},
    'San Lorenzo': {'ring': '#cc0000', 'bg': '#001430'},
    'Vélez Sársfield': {'ring': '#4169e1', 'bg': '#000e30'},
    'Estudiantes (LP)': {'ring': '#cc0000', 'bg': '#180000'},
    'Rosario Central': {'ring': '#f5c400', 'bg': '#001430'},
    "Newell's Old Boys": {'ring': '#cc0000', 'bg': '#0d0d0d'},
    'Huracán': {'ring': '#e0e0e0', 'bg': '#141414'},
    'Colón': {'ring': '#cc0000', 'bg': '#0d0d0d'},
    'Lanús': {'ring': '#cc0022', 'bg': '#180005'},
    'Gimnasia (LP)': {'ring': '#4169e1', 'bg': '#000e30'},
    'Banfield': {'ring': '#22c55e', 'bg': '#001808'},
    'Argentinos Juniors': {'ring': '#cc0000', 'bg': '#180000'},
    'Godoy Cruz': {'ring': '#f5c400', 'bg': '#180000'},
    'Tigre': {'ring': '#4169e1', 'bg': '#001430'},
}

# ─── NAV BAR ───
components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<nav style="background:rgba(6,14,10,0.94);backdrop-filter:blur(18px);border-bottom:1px solid rgba(74,222,128,0.14);padding:0 48px;display:flex;align-items:center;justify-content:space-between;height:64px;">
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:38px;height:38px;background:linear-gradient(135deg,#22c55e,#15803d);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;box-shadow:0 0 18px rgba(34,197,94,0.4);">⚽</div>
        <span style="font-family:'Bebas Neue',cursive;font-size:22px;letter-spacing:3px;color:#f0fdf4;">Fútbol Argentino</span>
        <span style="background:rgba(74,222,128,0.1);color:#4ade80;padding:2px 12px;border-radius:100px;font-size:11px;font-weight:700;letter-spacing:1px;border:1px solid rgba(74,222,128,0.25);">2008 – 2022</span>
    </div>
    <div style="display:flex;gap:36px;">
        <span style="color:#86efac;font-size:14px;font-weight:500;">Clubes</span>
        <span style="color:#86efac;font-size:14px;font-weight:500;">Análisis</span>
        <span style="color:#86efac;font-size:14px;font-weight:500;">Evolución</span>
    </div>
</nav>
""", height=68)


# ─── HERO SECTION ───
total_jugadores = f"{len(df):,}"
total_temporadas = str(df['Temporada'].nunique())
total_clubs = str(df['Club'].nunique())
valor_prom = df['Valor de mercado'].mean()
valor_prom_str = f"${valor_prom/1e6:.2f}M" if valor_prom > 1e6 else f"${valor_prom:,.0f}"
edad_prom = f"{df['Edad'].mean():.1f}"
altura_prom = f"{df['Altura'].mean():.2f}m"

components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<style>
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(28px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
<section style="position:relative;overflow:hidden;padding:70px 24px 80px;display:flex;flex-direction:column;align-items:center;text-align:center;background:#060e0a;">
    <div style="position:absolute;inset:0;background:repeating-linear-gradient(90deg,#060e0a 0px,#060e0a 72px,#07100a 72px,#07100a 144px);pointer-events:none;"></div>
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse 65% 80% at 50% 40%,rgba(34,197,94,0.1),transparent 70%);pointer-events:none;"></div>
    <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:1px;height:80px;background:linear-gradient(to bottom,transparent,rgba(74,222,128,0.5));pointer-events:none;"></div>

    <div style="display:flex;align-items:center;gap:14px;margin-bottom:28px;position:relative;z-index:1;animation:fadeUp 0.5s ease both;">
        <div style="height:2px;width:40px;background:linear-gradient(to right,transparent,#74acdf);"></div>
        <span style="font-size:12px;font-weight:700;letter-spacing:5px;color:#74acdf;text-transform:uppercase;">República Argentina</span>
        <div style="height:2px;width:40px;background:linear-gradient(to left,transparent,#74acdf);"></div>
    </div>

    <h1 style="font-family:'Bebas Neue',cursive;font-size:clamp(60px,10vw,120px);line-height:0.88;color:#f0fdf4;margin-bottom:18px;position:relative;z-index:1;letter-spacing:3px;animation:fadeUp 0.6s 0.05s ease both;">
        Fútbol
        <span style="display:block;background:linear-gradient(120deg,#4ade80 0%,#22c55e 45%,#fbbf24 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Argentino</span>
    </h1>

    <p style="font-size:14px;color:#86efac;letter-spacing:7px;text-transform:uppercase;font-weight:600;margin-bottom:56px;position:relative;z-index:1;animation:fadeUp 0.6s 0.1s ease both;">
        Análisis Estadístico · 15 Temporadas
    </p>

    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:16px;width:100%;max-width:1100px;position:relative;z-index:1;animation:fadeUp 0.7s 0.2s ease both;">
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Jugadores</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#f0fdf4;line-height:1;margin-bottom:5px;">{total_jugadores}</div>
            <div style="font-size:11px;color:#3d6b4a;">Total registrados</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Temporadas</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#f0fdf4;line-height:1;margin-bottom:5px;">{total_temporadas}</div>
            <div style="font-size:11px;color:#3d6b4a;">2008 – 2022</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Clubes</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#f0fdf4;line-height:1;margin-bottom:5px;">{total_clubs}</div>
            <div style="font-size:11px;color:#3d6b4a;">Primera División</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(251,191,36,0.22);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#fbbf24;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Valor Prom.</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#fbbf24;line-height:1;margin-bottom:5px;">{valor_prom_str}</div>
            <div style="font-size:11px;color:#3d6b4a;">USD por jugador</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Edad Prom.</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#f0fdf4;line-height:1;margin-bottom:5px;">{edad_prom}</div>
            <div style="font-size:11px;color:#3d6b4a;">años promedio</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:22px 14px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Altura Prom.</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:36px;color:#f0fdf4;line-height:1;margin-bottom:5px;">{altura_prom}</div>
            <div style="font-size:11px;color:#3d6b4a;">talla media</div>
        </div>
    </div>
</section>
""", height=520)


# ─── DIVIDER ───
components.html(f'{BASE_STYLE}<div style="height:1px;background:linear-gradient(to right,transparent,rgba(74,222,128,0.22),transparent);"></div>', height=4)


# ─── CLUBES SECTION ───
clubs_stats = df.groupby('Club').agg(
    players=('Jugadores', 'count'),
    avg_val=('Valor de mercado', 'mean')
).reset_index().sort_values('avg_val', ascending=False)

club_cards_html = ""
for _, row in clubs_stats.iterrows():
    club_name = row['Club']
    players = int(row['players'])
    avg_val = row['avg_val']
    avg_val_str = f"{avg_val/1e6:.2f}M" if avg_val >= 1e6 else f"{avg_val/1e3:.0f}K"
    colors = CLUB_COLORS.get(club_name, {'ring': '#4ade80', 'bg': '#0a140d'})
    abbr = ''.join([w[0] for w in club_name.split()[:3]]).upper()[:3]

    club_cards_html += f"""
    <div class="club-card">
        <div style="width:68px;height:68px;border-radius:50%;background:{colors['bg']};border:2.5px solid {colors['ring']};display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 18px {colors['ring']}44;">
            <span style="font-family:'Bebas Neue',cursive;font-size:20px;letter-spacing:1px;color:{colors['ring']};">{abbr}</span>
        </div>
        <div style="text-align:center;">
            <div style="font-weight:700;font-size:13px;color:#f0fdf4;line-height:1.35;margin-bottom:4px;">{club_name}</div>
            <div style="font-size:11px;color:#3d6b4a;">{players} jugadores</div>
        </div>
        <div style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.2);border-radius:8px;padding:4px 12px;font-size:12px;font-weight:700;color:#fbbf24;">
            ${avg_val_str}
        </div>
    </div>"""

num_clubs = len(clubs_stats)
clubs_rows = (num_clubs + 5) // 6
clubs_height = 100 + clubs_rows * 220

components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<style>
.club-card {{
    background:rgba(10,20,13,0.7);border:1px solid rgba(30,52,38,0.9);border-radius:16px;padding:24px 12px;
    display:flex;flex-direction:column;align-items:center;gap:13px;cursor:pointer;
    transition:transform 0.25s,box-shadow 0.25s;
}}
.club-card:hover {{ transform:translateY(-7px);box-shadow:0 18px 48px rgba(0,0,0,0.45); }}
</style>
<section style="padding:60px 24px;background:#060e0a;">
    <div style="display:flex;align-items:baseline;gap:20px;margin-bottom:48px;">
        <h2 style="font-family:'Bebas Neue',cursive;font-size:52px;letter-spacing:2px;color:#f0fdf4;line-height:1;">Los Clubes</h2>
        <span style="font-size:14px;color:#3d6b4a;font-weight:500;">{num_clubs} equipos · Primera División Argentina</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:16px;">
        {club_cards_html}
    </div>
</section>
""", height=clubs_height)


# ─── DIVIDER ───
components.html(f'{BASE_STYLE}<div style="height:1px;background:linear-gradient(to right,transparent,rgba(74,222,128,0.22),transparent);"></div>', height=4)


# ─── SIDEBAR FILTERS ───
with st.sidebar:
    components.html(f"""
    {FONTS_CSS}{BASE_STYLE}
    <div style="display:flex;align-items:center;gap:12px;padding:8px;">
        <div style="width:32px;height:32px;background:linear-gradient(135deg,#22c55e,#15803d);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;box-shadow:0 0 14px rgba(34,197,94,0.4);">⚽</div>
        <span style="font-family:'Bebas Neue',cursive;font-size:19px;letter-spacing:2.5px;color:#f0fdf4;">Filtros</span>
    </div>
    """, height=55)
    st.markdown("---")

    temporadas = sorted(df['Temporada'].dropna().unique())
    selected_seasons = st.multiselect(
        "Temporadas", options=temporadas,
        default=temporadas[-3:] if len(temporadas) > 2 else temporadas
    )
    clubs = sorted(df['Club'].dropna().unique().tolist())
    selected_clubs = st.multiselect(
        "Clubes", options=clubs,
        default=clubs[:3] if len(clubs) > 2 else clubs
    )
    posiciones = sorted(df['Posicion'].dropna().unique().tolist())
    selected_positions = st.multiselect(
        "Posiciones", options=posiciones,
        default=posiciones[:3] if len(posiciones) > 2 else posiciones
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px;color:#3d6b4a;line-height:1.6;">
        <strong style="color:#4ade80;">Fuente:</strong> Transfermarkt<br>
        <strong style="color:#4ade80;">Datos:</strong> 12,092 jugadores<br>
        <strong style="color:#4ade80;">Período:</strong> 2008 – 2022
    </div>
    """, unsafe_allow_html=True)

filtered_df = df.copy()
if selected_seasons:
    filtered_df = filtered_df[filtered_df['Temporada'].isin(selected_seasons)]
if selected_clubs:
    filtered_df = filtered_df[filtered_df['Club'].isin(selected_clubs)]
if selected_positions:
    filtered_df = filtered_df[filtered_df['Posicion'].isin(selected_positions)]


# ─── FILTERED METRICS ───
f_jugadores = f"{len(filtered_df):,}"
f_valor = filtered_df['Valor de mercado'].mean()
f_valor_str = f"${f_valor/1e6:.2f}M" if not pd.isna(f_valor) and f_valor >= 1e6 else (f"${f_valor:,.0f}" if not pd.isna(f_valor) else "N/A")
f_edad = filtered_df['Edad'].mean()
f_edad_str = f"{f_edad:.1f}" if not pd.isna(f_edad) else "N/A"
f_clubs_count = str(filtered_df['Club'].nunique())

components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<section style="padding:40px 24px 10px;background:#060e0a;">
    <div style="display:flex;align-items:baseline;gap:20px;margin-bottom:28px;">
        <h2 style="font-family:'Bebas Neue',cursive;font-size:52px;letter-spacing:2px;color:#f0fdf4;line-height:1;">Análisis</h2>
        <span style="font-size:14px;color:#3d6b4a;font-weight:500;">Distribuciones y comparativas · Usá el sidebar para filtrar</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:18px 16px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:8px;">Jugadores Filtrados</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:32px;color:#f0fdf4;line-height:1;">{f_jugadores}</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(251,191,36,0.22);border-radius:14px;padding:18px 16px;">
            <div style="font-size:10px;color:#fbbf24;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:8px;">Valor Promedio</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:32px;color:#fbbf24;line-height:1;">{f_valor_str}</div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:18px 16px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:8px;">Edad Promedio</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:32px;color:#f0fdf4;line-height:1;">{f_edad_str} <span style="font-size:14px;color:#3d6b4a;font-family:'DM Sans';">años</span></div>
        </div>
        <div style="background:rgba(10,20,13,0.88);border:1px solid rgba(74,222,128,0.2);border-radius:14px;padding:18px 16px;">
            <div style="font-size:10px;color:#4ade80;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:8px;">Clubes Incluidos</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:32px;color:#f0fdf4;line-height:1;">{f_clubs_count}</div>
        </div>
    </div>
</section>
""", height=180)


def render_chart_card(label, title, label_color="#4ade80"):
    components.html(f"""
    {FONTS_CSS}{BASE_STYLE}
    <div style="background:rgba(10,20,13,0.7);border:1px solid rgba(30,52,38,0.9);border-radius:16px 16px 0 0;padding:20px 24px 12px;">
        <div style="font-size:10px;color:{label_color};letter-spacing:2.5px;text-transform:uppercase;font-weight:700;margin-bottom:4px;">{label}</div>
        <div style="font-weight:700;font-size:15px;color:#f0fdf4;">{title}</div>
    </div>
    """, height=72)


# ─── TABS ───
tab1, tab2, tab3, tab4 = st.tabs([
    "PERFIL DE JUGADORES",
    "VALOR DE MERCADO",
    "EQUIPOS Y FICHAJES",
    "EVOLUCIÓN TEMPORAL"
])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        render_chart_card("Distribución", "Edad de Jugadores")
        fig = px.histogram(filtered_df, x='Edad', nbins=20, color_discrete_sequence=[GREEN_ACCENT])
        fig.update_traces(marker_line_color='rgba(74,222,128,0.3)', marker_line_width=1)
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=260)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_chart_card("Breakdown", "Pie Dominante")
        pie_data = filtered_df['Pie'].value_counts()
        if len(pie_data) > 0:
            fig = px.pie(values=pie_data.values, names=pie_data.index, color_discrete_sequence=GREEN_SEQ, hole=0.65)
            fig.update_traces(textfont=dict(color='#f0fdf4', size=11), marker=dict(line=dict(color='#0a140d', width=2)))
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, height=260, legend=dict(font=dict(color='#5a9070', size=10)))
            st.plotly_chart(fig, use_container_width=True)

    with col3:
        render_chart_card("Comparativa", "Altura por Posición", GOLD)
        altura_pos = filtered_df.groupby('Posicion')['Altura'].mean().dropna().sort_values(ascending=True)
        if len(altura_pos) > 0:
            fig = px.bar(x=altura_pos.values, y=altura_pos.index, orientation='h', color_discrete_sequence=[GOLD])
            fig.update_traces(marker_line_color='rgba(251,191,36,0.3)', marker_line_width=1)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=260)
            st.plotly_chart(fig, use_container_width=True)

    render_chart_card("Scatter", "Relación Edad vs Altura por Posición")
    scatter_data = filtered_df.dropna(subset=['Edad', 'Altura'])
    if len(scatter_data) > 0:
        fig = px.scatter(scatter_data, x='Edad', y='Altura', color='Posicion', opacity=0.6,
                         color_discrete_sequence=GREEN_SEQ + [GOLD, BLUE_AR, '#e3001b', '#f5c400'])
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, height=340, legend=dict(font=dict(color='#5a9070', size=10)))
        st.plotly_chart(fig, use_container_width=True)


with tab2:
    col1, col2 = st.columns(2)

    with col1:
        render_chart_card("Ranking", "Top 10 Jugadores Más Valiosos", GOLD)
        top_players = filtered_df.dropna(subset=['Valor de mercado']).nlargest(10, 'Valor de mercado')
        if len(top_players) > 0:
            fig = px.bar(top_players, x='Valor de mercado', y='Jugadores', orientation='h',
                         color='Valor de mercado',
                         color_continuous_scale=[[0, '#15803d'], [0.5, '#22c55e'], [1, '#4ade80']],
                         hover_data=['Posicion', 'Club'])
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=340, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        render_chart_card("Distribución", "Valor por Posición (Box)", GOLD)
        boxplot_data = filtered_df.dropna(subset=['Valor de mercado', 'Posicion'])
        if len(boxplot_data) > 0:
            fig = px.box(boxplot_data, x='Posicion', y='Valor de mercado', color_discrete_sequence=[GREEN_ACCENT])
            fig.update_traces(marker_color=GREEN_ACCENT, line_color=GREEN_ACCENT)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=340, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_chart_card("Comparativa", "Valor Total por Club")
        valor_club = filtered_df.groupby('Club')['Valor de mercado'].sum().dropna().sort_values(ascending=True)
        if len(valor_club) > 0:
            fig = px.bar(x=valor_club.values, y=valor_club.index, orientation='h', color_discrete_sequence=[GREEN_ACCENT])
            fig.update_traces(marker_line_color='rgba(74,222,128,0.25)', marker_line_width=1)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=340)
            st.plotly_chart(fig, use_container_width=True)

        render_chart_card("Scatter", "Edad vs Valor de Mercado", GOLD)
        scatter_val = filtered_df.dropna(subset=['Edad', 'Valor de mercado', 'Altura'])
        if len(scatter_val) > 0:
            fig = px.scatter(scatter_val, x='Edad', y='Valor de mercado', color='Posicion', size='Altura',
                             opacity=0.6, hover_data=['Jugadores', 'Club'],
                             color_discrete_sequence=GREEN_SEQ + [GOLD, BLUE_AR])
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, height=340, legend=dict(font=dict(color='#5a9070', size=10)))
            st.plotly_chart(fig, use_container_width=True)


with tab3:
    col1, col2 = st.columns(2)

    with col1:
        render_chart_card("Heatmap", "Posiciones por Club")
        pos_club_data = filtered_df.dropna(subset=['Club', 'Posicion'])
        if len(pos_club_data) > 0:
            pos_club = pd.crosstab(pos_club_data['Club'], pos_club_data['Posicion'])
            fig = px.imshow(pos_club, aspect='auto',
                            color_continuous_scale=[[0, '#060e0a'], [0.3, '#14532d'], [0.6, '#22c55e'], [1, '#4ade80']])
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=380)
            st.plotly_chart(fig, use_container_width=True)

        render_chart_card("Ranking", "Jugadores por Club")
        jug_club = filtered_df['Club'].value_counts()
        if len(jug_club) > 0:
            fig = px.bar(x=jug_club.values, y=jug_club.index, orientation='h', color_discrete_sequence=[GREEN_ACCENT])
            fig.update_traces(marker_line_color='rgba(74,222,128,0.25)', marker_line_width=1)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=340)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_chart_card("Ranking", "Top 15 Equipos Anteriores", "#a78bfa")
        eq_ant = filtered_df['Equipo Anterior'].dropna().value_counts().head(15)
        if len(eq_ant) > 0:
            fig = px.bar(x=eq_ant.values, y=eq_ant.index, orientation='h', color_discrete_sequence=['#a78bfa'])
            fig.update_traces(marker_line_color='rgba(167,139,250,0.3)', marker_line_width=1)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=380)
            st.plotly_chart(fig, use_container_width=True)

        render_chart_card("Breakdown", "Procedencia de Jugadores")
        filtered_df_temp = filtered_df.copy()
        filtered_df_temp['EsInferiores'] = filtered_df_temp['Equipo Anterior'].str.contains('Inferiores', na=False)
        inf_count = filtered_df_temp['EsInferiores'].value_counts()
        if len(inf_count) > 0:
            labels = ['Externos' if not k else 'Inferiores' for k in inf_count.index]
            fig = px.pie(values=inf_count.values, names=labels, color_discrete_sequence=[GREEN_ACCENT, GOLD], hole=0.65)
            fig.update_traces(textfont=dict(color='#f0fdf4', size=11), marker=dict(line=dict(color='#0a140d', width=2)))
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=True, height=340, legend=dict(font=dict(color='#5a9070', size=10)))
            st.plotly_chart(fig, use_container_width=True)


with tab4:
    components.html(f"""
    {FONTS_CSS}{BASE_STYLE}
    <div style="display:flex;align-items:baseline;gap:20px;padding:8px 0;">
        <h2 style="font-family:'Bebas Neue',cursive;font-size:42px;letter-spacing:2px;color:#f0fdf4;line-height:1;">Evolución</h2>
        <span style="font-size:14px;color:#3d6b4a;font-weight:500;">Tendencias a lo largo del tiempo</span>
    </div>
    """, height=55)

    col1, col2 = st.columns([2, 1])

    with col1:
        render_chart_card("Tendencia", "Valor Promedio de Mercado")
        valor_temp = filtered_df.groupby('Temporada')['Valor de mercado'].mean().dropna()
        if len(valor_temp) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=valor_temp.index, y=valor_temp.values, mode='lines+markers',
                line=dict(color=GREEN_ACCENT, width=2.5, shape='spline'),
                marker=dict(color=GREEN_ACCENT, size=8, line=dict(color='#060e0a', width=2)),
                fill='tozeroy', fillcolor='rgba(74,222,128,0.08)',
                hovertemplate='Temporada: %{x}<br>Valor: $%{y:,.0f}<extra></extra>'))
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=320)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_chart_card("Evolución", "Edad Promedio por Temporada", BLUE_AR)
        edad_temp = filtered_df.groupby('Temporada')['Edad'].mean().dropna()
        if len(edad_temp) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=edad_temp.index, y=edad_temp.values, mode='lines+markers',
                line=dict(color=BLUE_AR, width=2.5, shape='spline'),
                marker=dict(color=BLUE_AR, size=7, line=dict(color='#060e0a', width=2)),
                fill='tozeroy', fillcolor='rgba(116,172,223,0.08)',
                hovertemplate='Temporada: %{x}<br>Edad: %{y:.1f} años<extra></extra>'))
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=320)
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        render_chart_card("Tendencia", "Fichajes por Año", GOLD)
        if 'Año Fichaje' in filtered_df.columns:
            fichajes = filtered_df['Año Fichaje'].dropna().value_counts().sort_index()
            if len(fichajes) > 0:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=fichajes.index, y=fichajes.values, mode='lines+markers',
                    line=dict(color=GOLD, width=2.5, shape='spline'),
                    marker=dict(color=GOLD, size=7, line=dict(color='#060e0a', width=2)),
                    fill='tozeroy', fillcolor='rgba(251,191,36,0.08)',
                    hovertemplate='Año: %{x}<br>Fichajes: %{y}<extra></extra>'))
                fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=280)
                st.plotly_chart(fig, use_container_width=True)

    with col2:
        render_chart_card("Heatmap", "Fichajes por Temporada y Club")
        hm_data = filtered_df.dropna(subset=['Temporada', 'Club'])
        if len(hm_data) > 0:
            fichajes_hm = pd.crosstab(hm_data['Temporada'], hm_data['Club'])
            if len(fichajes_hm) > 0:
                fig = px.imshow(fichajes_hm, aspect='auto',
                                color_continuous_scale=[[0, '#060e0a'], [0.3, '#7f1d1d'], [0.6, '#dc2626'], [1, '#fbbf24']])
                fig.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=280)
                st.plotly_chart(fig, use_container_width=True)


# ─── RAW DATA SECTION ───
components.html(f'{BASE_STYLE}<div style="height:1px;background:linear-gradient(to right,transparent,rgba(74,222,128,0.22),transparent);margin:20px 0;"></div>', height=6)

components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<div style="display:flex;align-items:baseline;gap:16px;padding:8px 0;">
    <div style="font-size:10px;color:#4ade80;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">Datos</div>
    <div style="font-weight:700;font-size:16px;color:#f0fdf4;">Datos Filtrados</div>
    <span style="margin-left:auto;font-size:12px;color:#3d6b4a;">Abrí el sidebar para ajustar filtros</span>
</div>
""", height=42)

with st.expander("Ver datos completos filtrados"):
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Descargar datos filtrados como CSV",
        data=csv, file_name="futbol_argentino_filtrado.csv", mime="text/csv"
    )


# ─── FOOTER ───
components.html(f"""
{FONTS_CSS}{BASE_STYLE}
<footer style="border-top:1px solid rgba(30,52,38,0.8);padding:28px 24px;display:flex;align-items:center;justify-content:space-between;background:#060e0a;">
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:28px;height:28px;background:linear-gradient(135deg,#22c55e,#15803d);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;">⚽</div>
        <span style="font-family:'Bebas Neue',cursive;font-size:17px;letter-spacing:2.5px;color:#3d6b4a;">Fútbol Argentino</span>
    </div>
    <div style="font-size:13px;color:#3d6b4a;">Fuente: Transfermarkt · 12,092 jugadores · 17 clubes · 15 temporadas</div>
    <div style="font-size:12px;color:#2a4d33;">Dashboard estadístico · Primera División Argentina</div>
</footer>
""", height=80)
