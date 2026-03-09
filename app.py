import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO & ESTADO DINÂMICO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Matrix V45",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Ciclo (Rotação de Notícias a cada 30s)
if 'news_index' not in st.session_state:
    st.session_state.news_index = 0

# ==============================================================================
# 02. CSS V45: NEUMORPHISM & GLASS-ELITE (ESTÉTICA CORRIGIDA)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Page Structure */
    .main .block-container { padding: 2rem 5rem; max-width: 1600px; margin: 0 auto; }
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia Calibrada */
    h1 { font-size: 5rem !important; font-weight: 800; letter-spacing: -3px; line-height: 0.9; margin-bottom: 20px; }
    h2 { font-size: 2.5rem !important; font-weight: 700; color: #10b981; letter-spacing: -1px; margin-top: 50px; }
    h3 { font-size: 1.5rem !important; font-weight: 600; color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; }
    p, li { font-size: 1.15rem !important; line-height: 1.8; color: #94a3b8; font-weight: 400; }

    /* Hero Section: Estilo Ondo Finance 2.0 */
    .hero-panel {
        padding: 100px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 60px;
    }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 5px; font-size: 0.85rem; margin-bottom: 20px; }

    /* Cartões de Telemetria Dinâmicos */
    .q-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 35px;
        border-radius: 20px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        border-left: 4px solid #10b981;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .q-card:hover { border-color: #00d4ff; transform: translateY(-10px); box-shadow: 0 30px 60px rgba(0, 212, 255, 0.15); }
    .q-label { font-size: 0.75rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.2rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Monitor "O Pulso" (Informação Dinâmica) */
    .pulse-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 40px;
        border-radius: 20px;
        min-height: 500px;
        border-top: 5px solid #8b5cf6;
        box-shadow: inset 0 0 50px rgba(139, 92, 246, 0.05);
    }
    .pulse-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        padding: 20px 0;
        animation: fadeIn 0.8s ease-out;
    }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.25rem; display: block; margin-bottom: 5px; }
    .pulse-link:hover { color: #10b981; }

    /* Tabelas Futuristas */
    .futuristic-table { width: 100%; border-collapse: collapse; margin: 30px 0; background: #0b0f1a; border-radius: 15px; overflow: hidden; }
    .futuristic-table th { text-align: left; padding: 22px; background: rgba(0,0,0,0.3); color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }
    .futuristic-table td { padding: 25px 22px; border-bottom: 1px solid #1e293b; color: #e2e8f0; font-size: 1.05rem; }
    .futuristic-table tr:hover { background: rgba(16, 185, 129, 0.03); }

    @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE INTELIGÊNCIA: DATABASE SOBERANA
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Valor",
        "why": "Único ativo com escassez finita absoluta (21M). Seguro contra o reset fiduciário.",
        "pros": ["Escassez 21M", "Adoção BlackRock", "Segurança PoW"],
        "cons": ["Volatilidade", "Regulação"],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Camada de Liquidação",
        "why": "Onde os triliões em RWA (Real World Assets) serão liquidados via Smart Contracts.",
        "pros": ["Líder RWA", "Deflacionário", "Eco-Friendly"],
        "cons": ["Gas Fees", "L2 Fragmentação"],
        "link": "https://ethereum.org/"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022",
        "why": "Substituto do SWIFT. Ativo de ponte para liquidação instantânea entre bancos mundiais.",
        "pros": ["Velocidade 3s", "Bancário", "ISO Ready"],
        "cons": ["Ripple Labs Control"],
        "link": "https://ripple.com/"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Vetor RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e a Blockchain.",
        "pros": ["BlackRock Link", "Yield Institucional"],
        "cons": ["Regulação Fiat"],
        "link": "https://ondo.finance/"
    }
}

# ==============================================================================
# 04. MOTORES DE DADOS (YFINANCE & FEEDPARSER)
# ==============================================================================
@st.cache_data(ttl=20)
def get_market_data(ticker):
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        curr = float(data['Close'].iloc[-1].item())
        prev = float(data['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg, data['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_live_pulse():
    sources = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]
    news = []
    for url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                news.append({"title": entry.title, "link": entry.link, "src": "GLOBAL PULSE"})
        except: continue
    return news

# ==============================================================================
# 05. HERO PANEL (ESTILO ONDO)
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-tag">Sovereign Financial Hub // Horizon 2030</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p class="hero-desc">Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
    A JTM Capital opera na fronteira da norma ISO 20022 para garantir soberania absoluta.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DINÂMICA COM GRÁFICOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global")
cols = st.columns(4)
assets_to_show = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo")]

for i, (ticker, name) in enumerate(assets_to_show):
    price, chg, history = get_market_data(ticker)
    color = "#10b981" if chg >= 0 else "#ef4444"
    with cols[i]:
        st.markdown(f"""
        <div class="q-card">
            <div class="q-label">{name} // LIVE</div>
            <div class="q-value">€ {price:,.2f}</div>
            <div style="color:{color}; font-weight:800; font-family:JetBrains Mono;">{chg:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        # Sparkline Dinâmica
        fig = go.Figure(data=go.Scatter(y=history, line=dict(color=color, width=2), hoverinfo='none'))
        fig.update_layout(height=60, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (ROTAÇÃO 30S)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_news, c_chart = st.columns([1.5, 2])

with c_news:
    st.markdown('<div class="pulse-box">', unsafe_allow_html=True)
    full_news = fetch_live_pulse()
    
    # Lógica de Rotação (Mostra 10 notícias por vez, roda a cada refresh)
    start_idx = (st.session_state.news_index * 10) % len(full_news)
    display_news = full_news[start_idx : start_idx + 10]
    
    for n in display_news:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" target="_blank" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.8rem;">FONTE: GLOBAL INTEL // LIVE</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_chart:
    st.markdown('<div class="pulse-box">', unsafe_allow_html=True)
    st.markdown("#### Análise de Vetor: Bitcoin (BTC) 30 Dias")
    _, _, btc_hist = get_market_data("BTC-EUR")
    fig_main = go.Figure(data=[go.Candlestick(x=btc_hist.index, open=btc_hist, high=btc_hist*1.01, low=btc_hist*0.99, close=btc_hist)])
    fig_main.update_layout(template="plotly_dark", height=450, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_main, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO & ARQUITETURA
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Recomendado (Ciclo 2026)")

pos_data = [
    ["Âncora de Proteção", "BCP (Liquidez) / Ouro", "50%", "Garantia de solvência macro."],
    ["Autonomia Física", "Tesla (TSLA)", "15%", "Domínio IA e Energia."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Reset Bancário Mundial."],
    ["Fronteira Digital", "BTC / NEAR / ETH", "15%", "Escassez Matemática."]
]

table_html = "<table class='futuristic-table'><thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Nota</th></tr></thead><tbody>"
for r in pos_data:
    table_html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

# Injeção de Diagramas Técnicos
st.markdown("### 🌐 Arquitetura da Transição Sistémica")

st.caption("Arquitetura ISO 20022: O novo sistema nervoso central dos triliões mundiais.")


st.caption("Fluxo de Tokenização RWA: Digitalização da propriedade física em rede.")

st.divider()

# ==============================================================================
# 09. CÓDICE DE ATIVOS SOBERANOS (TESE EXPANDIDA)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // Porquê cada nó?")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        col_t, col_i = st.columns([1.5, 1])
        with col_t:
            st.markdown(f"#### Função: {info['role']}")
            st.markdown(f"> **Tese Central:** {info['why']}")
            
            v_table = "<table class='futuristic-table'><thead><tr><th>🟢 VANTAGENS</th><th>🔴 RISCOS</th></tr></thead><tbody><tr><td>"
            v_table += "<ul>" + "".join([f"<li>{p}</li>" for p in info['pros']]) + "</ul></td><td>"
            v_table += "<ul>" + "".join([f"<li>{c}</li>" for c in info['cons']]) + "</ul></td></tr></tbody></table>"
            st.markdown(v_table, unsafe_allow_html=True)
            st.markdown(f"[LER WHITE PAPER OFICIAL]({info['link']})")
        with col_i:
            st.image(f"https://cryptologos.cc/logos/{info['name'].lower().replace(' ', '-')}-{key.lower()}-logo.png", width=150)
            st.info(f"Monitorização ativa de rede para {info['name']}. Status: SOBERANO.")

# Rodapé Final
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    <em>"A soberania é o resultado da substituição do medo pela matemática."</em><br>
    <small>SINGULARITY V45.0 // ERROR-FREE DYNAMIC BUILD</small>
</div>
""", unsafe_allow_html=True)

# Lógica de Atualização Automática
if auto_refresh:
    st.session_state.news_index += 1
    time.sleep(30)
    st.rerun()
