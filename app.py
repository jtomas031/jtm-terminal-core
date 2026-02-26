import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DO SISTEMA & CONFIGURAÇÃO TÁTICA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Global Strategy Hub",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

with st.sidebar:
    st.markdown("### ⚙️ COMANDO ESTRATÉGICO")
    st.markdown("---")
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Sincronização com o fluxo de liquidez dos Bancos Centrais.")
    st.markdown("---")
    st.markdown("### 🌐 MONITOR DE SOBERANIA")
    st.error("**STATUS:** TRANSIÇÃO ISO 20022\n\n**ALVO:** BLACKROCK BUIDL\n\n**RISCO:** COLAPSO FIAT")
    st.markdown("---")
    st.markdown("### 📈 ABSORÇÃO DE LIQUIDEZ")
    st.progress(0.85, text="ABSORÇÃO INSTITUCIONAL BTC")
    st.progress(0.65, text="CONVERSÃO RWA ETHEREUM")
    st.markdown("---")
    st.info(f"Relógio Global: {datetime.now().strftime('%H:%M:%S')} WET")

# ==============================================================================
# 02. CSS CORPORATIVO: DESIGN DE 2040 (NEGRO ABSOLUTO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@300;400;800&family=Courier+New&display=swap');
    
    .stApp { 
        background-color: #000000; 
        color: #cbd5e1; 
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    
    .hero-container {
        background: #000000;
        border: 1px solid #1e293b;
        border-top: 4px solid #38bdf8;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.05);
    }
    .hero-title {
        font-size: 4rem;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 0px;
    }
    
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 4px solid #38bdf8;
        padding: 25px;
        border-radius: 2px;
        transition: 0.3s;
    }
    .metric-card:hover { border-color: #38bdf8; background: #080808; }
    .m-title { font-size: 0.9rem; color: #64748b; font-family: 'Courier New'; font-weight: bold; }
    .m-price { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }
    
    .news-hub-compact { background: #030303; border: 1px solid #111; padding: 20px; min-height: 450px; }
    .news-item { border-bottom: 1px solid #111; padding: 15px 0; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: bold; font-size: 1.1rem; }
    
    .edu-box {
        background-color: #050505;
        border: 1px solid #111;
        padding: 40px;
        margin-bottom: 30px;
        border-left: 6px solid #10b981;
    }
    
    .tactic-table { width: 100%; border-collapse: collapse; margin: 20px 0; background: #050505; }
    .tactic-table th { background: #111; color: #38bdf8; padding: 15px; text-align: left; }
    .tactic-table td { border: 1px solid #111; padding: 15px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MOTORES DE DADOS (SOBERANIA INSTITUCIONAL)
# ==============================================================================
SUPPLY_MATRIX = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000,
    "XRP-EUR": 54800000000, "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000
}

@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if len(df) >= 2:
            current = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            change = ((current - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = current * SUPPLY_MATRIX.get(ticker, 0)
            return current, change, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except: return 0.0, 0.0, 0.0, 0.0

@st.cache_data(ttl=600)
def fetch_global_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    radar_data = []
    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                radar_data.append({"title": entry.title, "link": entry.link, "source": source_name, "timestamp": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(radar_data, key=lambda x: x['timestamp'], reverse=True)

# ==============================================================================
# 04. HERO: A AGENDA DOS LÍDERES MUNDIAIS
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.5rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 5px;">STRATEGIC SOVEREIGNTY TERMINAL</div>
    <p style="margin-top: 25px; font-size: 1.2rem; color: #94a3b8; line-height: 1.8;">
        Este terminal monitoriza a execução da <b>Agenda 2030 de Liquidez Global</b>. Enquanto o retalho especula, os Bancos Centrais (BCE, FED, PBoC) e os gigantes de Wall Street (BlackRock, Vanguard) estão a reescrever o protocolo do dinheiro. A transição para a norma <b>ISO 20022</b> e a <b>Tokenização de Ativos (RWA)</b> não são tendências — são as novas leis da física financeira impostas pela elite global para o próximo século.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. PAINEL DE TELEMETRIA
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)
assets = {
    "BTC": ("BITCOIN (RESERVA SOBERANA)", "BTC-EUR"),
    "ETH": ("ETHEREUM (SETTLEMENT LAYER)", "ETH-EUR"),
    "LINK": ("CHAINLINK (GLOBAL ORACLE)", "LINK-EUR"),
    "XRP": ("RIPPLE (ISO 20022 BRIDGE)", "XRP-EUR"),
    "XLM": ("STELLAR (RWA INFRA)", "XLM-EUR"),
    "QNT": ("QUANT (INTEROP OPERATING SYS)", "QNT-EUR"),
    "RNDR": ("RENDER (AI COMPUTE POWER)", "RNDR-EUR")
}

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols_array = [c1, c2, c3, c4, c5, c6, c7]

for i, (symbol, (name, ticker)) in enumerate(assets.items()):
    price, change, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    with cols_array[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{change:+.2f}% (24H)</div>
        </div>
        """, unsafe_allow_html=True)

with c8:
    st.markdown('<div class="metric-card" style="border-left: 4px solid #8b5cf6; text-align: center;"><div style="color: #a78bfa; font-weight: bold;">GLOBAL RESET</div><div style="color: #ffffff; font-size: 1.5rem; font-weight: 800;">ACTIVE</div></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. O MOVIMENTO DOS LÍDERES (CALENDÁRIO & RADAR)
# ==============================================================================
col_macro, col_radar = st.columns([1.5, 1])

with col_macro:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> A AGENDA DOS LÍDERES: EVENTOS DE RESET</h2>")
    
    events = [
        {"date": "Março 2026", "target": "FEDERAL RESERVE (FED)", "desc": "Manipulação das Taxas de Juro para forçar a migração de capital fiduciário para títulos tokenizados."},
        {"date": "Maio 2026", "target": "BLACKROCK / VANGUARD", "desc": "Expansão do fundo BUIDL para o mercado europeu. Início da devoração de obrigações do tesouro via Ethereum."},
        {"date": "Nov 2026", "target": "BIS / SWIFT", "desc": "Prazo Final ISO 20022. O desligamento dos sistemas legados obriga o uso de XRP e QNT para liquidez."},
        {"date": "Junho 2027", "target": "EUROPEAN CENTRAL BANK", "desc": "Lançamento do Euro Digital (CBDC) integrado em redes de interoperabilidade controlada."}
    ]
    
    for e in events:
        st.markdown(f"""
        <div style="background:#050505; border: 1px solid #111; padding: 20px; margin-bottom: 10px; border-right: 4px solid #38bdf8;">
            <span style="color:#fbbf24; font-weight:bold;">{e['date']}</span> | <b style="color:#fff;">{e['target']}</b><br>
            <span style="color:#94a3b8;">{e['desc']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR DE INTELIGÊNCIA</h2>")
    st.markdown('<div class="news-hub-compact">', unsafe_allow_html=True)
    news = fetch_global_radar()
    items_per_page = 5
    start_idx = (st.session_state.news_page % (len(news)//items_per_page)) * items_per_page
    for item in news[start_idx : start_idx + items_per_page]:
        st.markdown(f'<div class="news-item"><a href="{item["link"]}" target="_blank">{item["title"]}</a><br><small>{item["source"]}</small></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. PROJEÇÃO DE DOMINAÇÃO 2030 (PROJEÇÃO INSTITUCIONAL)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> MOTOR DE PROJEÇÃO: ABSORÇÃO GLOBAL 2030</h2>")
col_p1, col_p2 = st.columns([1, 1.2])

with col_p1:
    st.markdown("""
    <div style="background: linear-gradient(45deg, #050505, #000); border: 2px solid #38bdf8; padding: 40px; text-align: center; border-radius: 4px;">
        <h3 style="color:#38bdf8;">VETOR DE ESCASSEZ SOBERANA</h3>
        <p style="color:#64748b;">Projeção do valor de uma "Unidade de Reserva" (Baseado em Absorção de Bancos Centrais)</p>
        <div style="font-size: 4rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 0.9rem;">VALOR ESTIMADO POR BTC (AJUSTADO À INFLAÇÃO FIAT 2030)</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown("""
    <div class="edu-box">
        <h4 style="color:#10b981;">A ESTRATÉGIA DOS LÍDERES</h4>
        <p>Os líderes mundiais não estão a investir; estão a <b>substituir a base monetária</b>. A projeção de €285k/BTC não é otimismo, é matemática de absorção. 
        À medida que a BlackRock e os Fundos Soberanos (Arábia Saudita, Qatar) removem o suprimento das exchanges, o preço deixa de responder à oferta/demanda e passa a responder à <b>escassez absoluta de liquidação</b>.</p>
        <p>A JTM Capital rastreia este movimento: a liquidez institucional flui para o <b>Ethereum</b> para a infraestrutura e para o <b>XRP/QNT</b> para as mensagens financeiras. Quem detém os tokens, detém os carris da economia mundial.</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 08. MANIFESTO: A VISÃO DA ELITE
# ==============================================================================
st.markdown('<div class="edu-box" style="border-left-color: #38bdf8;">', unsafe_allow_html=True)
st.markdown("<h3>MANIFESTO: A GRANDE TRANSIÇÃO</h3>")
st.write("""
O sistema financeiro tradicional está a ser propositadamente desmantelado. Os líderes globais perceberam que a dívida fiduciária é insustentável. 
A solução da elite é o <b>Digital Asset Standard</b>.

1. **TOKENIZAÇÃO (RWA):** Ao transformar imóveis e ouro em código no Ethereum, a elite ganha controle total sobre a liquidez e a velocidade do capital.
2. **ISO 20022:** A norma de mensagens que exclui bancos que não se adaptarem. XRP e XLM são as ferramentas de exclusão e controle de fluxo.
3. **SOBERANIA ALGORÍTMICA:** O Bitcoin tornou-se o novo Padrão-Ouro. Quem não tiver reservas matemáticas até 2030 estará fora da mesa de decisões global.
""")
st.markdown('</div>', unsafe_allow_html=True)



st.divider()
st.markdown("<p style='text-align: center; color: #333; font-family: Courier New;'>JTM CAPITAL RESEARCH // NO RETAIL ALLOWED // GLOBAL RESET 2026-2030</p>", unsafe_allow_html=True)

if auto_update:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
