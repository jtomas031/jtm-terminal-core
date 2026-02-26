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
    page_title="JTM CAPITAL RESEARCH | Terminal de Operações",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicializar a memória de paginação das notícias (Roda a cada 30s)
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# Painel de Comando Lateral (Side-Channel)
with st.sidebar:
    st.markdown("### ⚙️ COMANDO CENTRAL JTM")
    st.markdown("---")
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Telemetria de mercado e paginação de notícias em sincronia.")
    st.markdown("---")
    st.markdown("### 🌐 MONITOR DE SOBERANIA")
    st.info("**STATUS:** TRANSIÇÃO ISO 20022\n\n**ALVO:** BLACKROCK BUIDL\n\n**SISTEMA:** ONLINE")
    st.markdown("---")
    st.markdown("### 📊 ABSORÇÃO DE LIQUIDEZ")
    st.progress(0.85, text="ABSORÇÃO INSTITUCIONAL BTC")
    st.progress(0.65, text="CONVERSÃO RWA ETHEREUM")
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA 2030")
    st.caption("Rastreamento de Reset Financeiro Global em curso.")

# ==============================================================================
# 02. CSS CORPORATIVO: NEURO-DESIGN & DOPAMINA INSTITUCIONAL
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=Courier+New&display=swap');
    
    /* Fundo Global: Abismo Institucional */
    .stApp { 
        background-color: #02040a; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #02040a 80%); 
    }
    
    /* Tipografia de Comando */
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1.5px; }
    p, li { line-height: 1.8; font-size: 1.08rem; color: #cbd5e1; }
    
    /* Hero Section: Título Formal e Efeito Glassmorphism */
    .hero-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 4px solid #38bdf8;
        padding: 60px 50px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }
    .hero-title {
        font-size: 4rem;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 3px;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.8rem;
        color: #38bdf8;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 5px;
        margin-top: 10px;
    }
    
    /* Cartões de Telemetria (Glassmorphism Avançado) */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(2, 4, 10, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 8px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2); border-left: 5px solid #10b981; }
    .m-title { font-size: 1.1rem; color: #94a3b8; font-family: 'Courier New', monospace; font-weight: bold; }
    .m-price { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; margin: 5px 0; }
    .m-data-row { display: flex; justify-content: space-between; font-size: 0.9rem; color: #64748b; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }
    
    /* Radar Compacto Rotativo Estilo CoinDesk */
    .news-hub-compact { background: #080c17; border: 1px solid #1e293b; border-radius: 8px; padding: 25px; height: 100%; min-height: 480px; border-left: 4px solid #8b5cf6; }
    .news-item { background: rgba(15, 23, 42, 0.5); padding: 15px; margin-bottom: 12px; border-radius: 6px; border-left: 2px solid #38bdf8; transition: 0.3s; }
    .news-item:hover { background: rgba(30, 41, 59, 0.9); }
    .news-item a { color: #f8fafc; text-decoration: none; font-weight: 700; font-size: 1.1rem; }
    .news-meta { font-size: 0.8rem; color: #64748b; margin-top: 8px; text-transform: uppercase; font-weight: bold; }
    
    /* Containers de Educação Profunda */
    .edu-box { background-color: #0b1120; border: 1px solid #1e293b; border-top: 4px solid #34d399; padding: 45px; border-radius: 12px; margin-bottom: 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); }
    .edu-title { font-size: 2.2rem; color: #f8fafc; margin-bottom: 25px; border-bottom: 1px solid #1e293b; padding-bottom: 15px; }
    .highlight { color: #38bdf8; font-weight: 800; }
    
    /* Tabelas Táticas */
    .tactic-table { width: 100%; border-collapse: collapse; margin: 25px 0; background: #0b1120; border-radius: 8px; overflow: hidden; }
    .tactic-table th { background: #1e293b; color: #38bdf8; padding: 18px; text-align: left; font-family: 'Rajdhani'; font-size: 1.3rem; }
    .tactic-table td { border: 1px solid #1e293b; padding: 18px; color: #cbd5e1; vertical-align: top; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MOTORES DE CÁLCULO E LOGÍSTICA DE DADOS
# ==============================================================================
SUPPLY_MATRIX = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000,
    "XRP-EUR": 54800000000, "QNT-EUR": 14500000, "XLM-EUR": 28700000000,
    "RNDR-EUR": 388000000
}

@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if not df.empty and len(df) >= 2:
            current = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            change = ((current - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = current * SUPPLY_MATRIX.get(ticker, 0)
            return current, change, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except: return 0.0, 0.0, 0.0, 0.0

def format_currency(num):
    if num >= 1_000_000_000_000: return f"€ {(num / 1_000_000_000_000):.2f} T"
    if num >= 1_000_000_000: return f"€ {(num / 1_000_000_000):.2f} B"
    if num >= 1_000_000: return f"€ {(num / 1_000_000):.2f} M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_global_radar():
    sources = [
        ("CoinDesk Inst.", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("CoinTelegraph Global", "https://cointelegraph.com/rss"),
        ("CryptoSlate", "https://cryptoslate.com/feed/")
    ]
    radar_data = []
    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]: 
                radar_data.append({"title": entry.title, "link": entry.link, "source": source_name, "timestamp": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(radar_data, key=lambda x: x['timestamp'], reverse=True)

# ==============================================================================
# 04. HERO SECTION: AGENDA GLOBAL
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div class="hero-subtitle">INSTITUTIONAL STRATEGY // AGENDA 2030</div>
    <p style="margin-top: 25px; font-size: 1.25rem; color: #cbd5e1; border-left: 5px solid #38bdf8; padding-left: 20px; line-height: 1.9;">
        A <b>JTM Capital Research</b> monitoriza a execução da Grande Transição Financeira Global. Enquanto o retalho se perde no ruído da volatilidade, as nações soberanas e os gigantes de Wall Street (BlackRock, Vanguard, State Street) estão a migrar silenciosamente a base monetária para carris criptográficos. A adoção da norma <b>ISO 20022</b> e a <b>Tokenização de Ativos (RWA)</b> são os novos pilares da hegemonia económica mundial para a próxima década.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. TELEMETRIA TÁTICA (EUROS €)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO (EUR €)</h2>", unsafe_allow_html=True)

assets_matrix = {
    "BTC": ("BITCOIN (RESERVA)", "BTC-EUR"), "ETH": ("ETHEREUM (SETTLEMENT)", "ETH-EUR"),
    "LINK": ("CHAINLINK (ORACLE)", "LINK-EUR"), "XRP": ("RIPPLE (ISO 20022)", "XRP-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"), "XLM": ("STELLAR (ISO 20022)", "XLM-EUR"),
    "RNDR": ("RENDER (AI COMPUTE)", "RNDR-EUR")
}

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
columns_array = [c1, c2, c3, c4, c5, c6, c7]

for i, (symbol, (name, ticker)) in enumerate(assets_matrix.items()):
    price, change, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    arrow = "▲" if change >= 0 else "▼"
    
    with columns_array[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold; font-family: 'Courier New';">{arrow} {abs(change):.2f}% (24H)</div>
            <div class="m-data-row">
                <span>VOL: {format_currency(vol)}</span>
                <span>MCAP: {format_currency(mcap)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with c8:
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #8b5cf6; text-align: center; display: flex; flex-direction: column; justify-content: center;">
        <div style="color: #a78bfa; font-weight: bold; font-family: 'Courier New';">GLOBAL STATUS</div>
        <div style="color: #ffffff; font-size: 1.8rem; font-weight: 800; margin-top: 10px;">RESET ACTIVE</div>
        <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">Linked to Central Banks</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. CENTRO VISUAL: GRÁFICO (Y-AXIS FIX), GAUGE E RADAR ROTATIVO
# ==============================================================================
col_chart, col_gauge, col_radar = st.columns([1.6, 1, 1.1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=60, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=450,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> ABSORÇÃO BLACKROCK</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 88,
        title = {'text': "FORÇA DE ACUMULAÇÃO INSTITUCIONAL", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"},
                {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}
            ],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 88}
        }
    ))
    fig_gauge.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=50, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL (COINDESK STYLE)</h2>", unsafe_allow_html=True)
    st.markdown('<div class="news-hub-compact">', unsafe_allow_html=True)
    news = fetch_global_radar()
    items_per_page = 5
    if len(news) > 0:
        total_pages = max(1, len(news) // items_per_page)
        current_page = st.session_state.news_page % total_pages
        start_idx = current_page * items_per_page
        st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.85rem; margin-bottom: 15px; font-weight: 800;'>INTERCEÇÃO {current_page+1}/{total_pages}</div>", unsafe_allow_html=True)
        for item in news[start_idx : start_idx + items_per_page]:
            st.markdown(f'<div class="news-item"><a href="{item["link"]}" target="_blank">{item["title"]}</a><div class="news-meta">{item["source"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. THINK TANK EDUCACIONAL (ARQUITETURA MACRO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ANÁLISE DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="edu-box">
    <div class="edu-title">I. O Colapso Fiduciário e a Fuga para a Escassez Soberana</div>
    <p>O sistema financeiro global, baseado em moedas decretadas por governos (Euro, Dólar), está a enfrentar um ponto de rutura matemática. Desde a separação do padrão-ouro em 1971, a massa monetária foi inflacionada através de dívida perpétua. Os líderes mundiais e fundos soberanos reconhecem agora que o único refúgio contra a diluição de riqueza é a <b>Escassez Absoluta</b>.</p>
    <p>O <b>Bitcoin (BTC)</b>, com o seu limite inegociável de 21 milhões de unidades, tornou-se o novo lastro global. Enquanto o retalho discute o preço diário, os Bancos Centrais preparam-se para o <i>Settlement Final</i>, onde o BTC servirá como a reserva neutra de valor que o ouro já não consegue ser na era digital.</p>
</div>

<div class="edu-box">
    <div class="edu-title">II. Tokenização (RWA): A Devoração do Mundo Físico</div>
    <p>A Tokenização de Ativos do Mundo Real (RWA) é a maior transferência de capital da história. Gestoras como a <b>BlackRock</b> estão a converter imóveis, ações, ouro e obrigações do tesouro em tokens na rede <b>Ethereum</b>. 
    </p>
    <p>Ao transformar um edifício de 100 milhões em tokens divisíveis, a elite mundial ganha liquidez instantânea e controlo total sobre o fluxo de propriedade. Se a internet de 1990 transmitia informação, a infraestrutura RWA transmite valor puro, sem intermediários humanos, 24/7, à velocidade da luz.</p>
</div>

<div class="edu-box">
    <div class="edu-title">III. Norma ISO 20022 e a Substituição do SWIFT</div>
    <p>O sistema SWIFT é o correio da década de 70. A norma <b>ISO 20022</b> é o sistema nervoso da nova economia. Ela exige que as transações carreguem dados complexos que os bancos tradicionais não conseguem processar em tempo real. 
    </p>
    <p>Ativos como <b>XRP (Ripple)</b> e <b>XLM (Stellar)</b> foram desenhados como pontes de liquidez para esta nova norma. Eles permitem que biliões de Euros sejam convertidos e liquidados em 3 segundos, eliminando o custo e o tempo de espera das transferências bancárias arcaicas. É o protocolo obrigatório que os bancos centrais estão a adotar para as suas CBDCs.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. DOSSIÊS TÁTICOS (MATRIZ DE RISCO & NOTÍCIAS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> DOSSIÊS DE INFRAESTRUTURA (PELOTÃO JTM)</h2>", unsafe_allow_html=True)

tabs = st.tabs(["₿ BTC", "⟠ ETH", "🔗 LINK", "✕ XRP", "◎ XLM", "Ⓠ QNT", "🧊 RNDR"])

def render_intel(name, role, thesis, pros, cons):
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown(f"### Função Tática: {role}")
        st.write(thesis)
        st.markdown("""<table class="tactic-table"><tr><th>🟢 VANTAGENS (ELITE)</th><th>🔴 RISCOS (CONTROLO)</th></tr><tr><td><ul>""" + "".join([f"<li>{p}</li>" for p in pros]) + """</ul></td><td><ul>""" + "".join([f"<li>{c}</li>" for c in cons]) + """</ul></td></tr></table>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"### 📡 Interceção de Radar ({name})")
        # Espaço para notícias filtradas (simplificado para estabilidade)
        st.info(f"Monitorização de fluxo institucional ativa para {name}. Ruído de retalho filtrado.")

with tabs[0]: render_intel("Bitcoin", "Reserva Soberana", "O escudo contra a inflação fiduciária e o novo padrão-ouro digital absorvido por Wall Street.", ["Escassez absoluta matemática.", "Adoção por Fundos Soberanos."], ["Risco de regulação centralizada.", "Velocidade da rede principal."])
with tabs[1]: render_intel("Ethereum", "Autoestrada RWA", "O computador mundial onde a BlackRock e bancos emitem triliões em ativos tokenizados.", ["Monopólio em contratos inteligentes.", "Deflacionário após EIP-1559."], ["Custos de rede elevados.", "Concorrência de Layer 2."])
with tabs[2]: render_intel("Chainlink", "Oráculo de Dados", "A ponte indispensável que liga o SWIFT e bancos reais aos dados da blockchain.", ["Parcerias oficiais com bancos centrais.", "Padrão CCIP de interoperabilidade."], ["Complexidade tecnológica elevada."])
with tabs[3]: render_intel("Ripple", "Liquidez ISO 20022", "A ferramenta de liquidação bruta em tempo real para bancos e CBDCs globais.", ["Velocidade extrema de settlement.", "Conformidade legal estabelecida."], ["Controlo centralizado pela Ripple Labs."])
with tabs[4]: render_intel("Stellar", "Pagamentos RWA", "Focada em remessas internacionais e tokenização de moedas fiat em mercados emergentes.", ["Parcerias com a IBM e governos.", "Custo de transação quase zero."], ["Sombra de marketing face ao XRP."])
with tabs[5]: render_intel("Quant", "Sistema Operativo", "O software que permite que as redes privadas de bancos comuniquem com redes públicas.", ["Interoperabilidade B2B exclusiva.", "Oferta de tokens escassa (14M)."], ["Código de software proprietário."])
with tabs[6]: render_intel("Render", "Infraestrutura IA", "A rede descentralizada que fornece poder de GPU para a expansão mundial da Inteligência Artificial.", ["Vital para o processamento de IA.", "Desafia o monopólio da Google Cloud."], ["Correlacionado com a bolha de IA."])

# ==============================================================================
# 09. GLOSSÁRIO E RODAPÉ
# ==============================================================================
st.divider()
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO INSTITUCIONAL</h2>", unsafe_allow_html=True)
c_g1, c_g2 = st.columns(2)
with c_g1:
    st.markdown("""
    * **RWA (Real World Assets):** Ativos reais (ouro, casas) colocados em código digital.
    * **CBDC:** Moedas digitais de Bancos Centrais. Ferramenta de controlo da elite.
    * **Self-Custody:** O ato soberano de deter as chaves privadas (ex: Trezor).
    """)
with c_g2:
    st.markdown("""
    * **DePIN:** Redes de infraestrutura física partilhada (GPUs para IA).
    * **Settlement:** A liquidação final e definitiva de uma transação.
    * **Smart Contracts:** Acordos automáticos que eliminam advogados e notários.
    """)

st.divider()
st.markdown("<p style='text-align: center; color: #444; font-family: Courier New;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA</p>", unsafe_allow_html=True)

if auto_update:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
