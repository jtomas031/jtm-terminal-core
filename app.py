import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO E GESTÃO DE ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Global Sovereignty Portal",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Memória de Rotação do Sistema
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# --- SIDEBAR DE COMANDO ---
with st.sidebar:
    st.markdown("<h1 style='color: #38bdf8; font-family: Rajdhani;'>JTM COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("---")
    auto_refresh = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Sincronização com o fluxo de liquidez global institucional.")
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO MENSAL (360€)")
    st.progress(300/360, text="BASE (BTC/ETH): 300€")
    st.progress(60/360, text="SNIPER (ISO/RWA): 60€")
    
    st.markdown("---")
    st.markdown("### 🔐 PROTOCOLO DE CUSTÓDIA")
    st.error("ALVO: TREZOR COLD STORAGE\n\nDATA CRÍTICA: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA SOBERANA")
    st.info("RESET FINANCEIRO EM CURSO\nNORMA ISO 20022: ATIVA\nTOKENIZAÇÃO RWA: EM ESCALA")

# ==============================================================================
# 02. CSS CORPORATIVO (ELIMINAÇÃO DE ESPAÇOS E DESIGN DOPAMINA)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Configuração de Espaçamento Total */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; padding-left: 3rem; padding-right: 3rem; }
    
    /* Fundo Deep-Dark */
    .stApp { 
        background-color: #010204; 
        color: #cbd5e1; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #010204 80%); 
    }
    
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }

    /* Hero Section Imponente */
    .hero-panel {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-top: 5px solid #38bdf8;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 4rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; }

    /* Cartões de Telemetria */
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 22px;
        border-radius: 2px;
        transition: 0.3s ease;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-4px); border-color: #38bdf8; box-shadow: 0 10px 30px rgba(56,189,248,0.1); }
    .m-label { font-size: 0.85rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; }
    .m-value { font-size: 2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }

    /* Radar de Notícias - LARGURA TOTAL */
    .news-full-width {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 30px;
        margin-bottom: 35px;
        width: 100%;
    }
    .news-item { border-bottom: 1px solid #111; padding: 20px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.25rem; transition: 0.2s; }
    .news-item a:hover { color: #ffffff; }

    /* Tabelas HTML */
    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 15px; background-color: #030303; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 18px; text-align: left; font-family: 'Rajdhani'; font-size: 1.25rem; border-bottom: 2px solid #111; }
    .jtm-table td { padding: 18px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; font-size: 1.05rem; line-height: 1.6; }

    /* Boxes Reset com Títulos Internos */
    .reset-box { 
        background: #050505; 
        border: 1px solid #111; 
        padding: 40px; 
        border-radius: 4px; 
        border-left: 8px solid #10b981; 
        min-height: 400px; 
        margin-bottom: 20px;
    }
    .reset-title { 
        font-size: 2rem; 
        color: #ffffff; 
        font-family: 'Inter', sans-serif; 
        font-weight: 700; 
        margin-bottom: 25px; 
        border-bottom: 1px solid #1e293b; 
        padding-bottom: 15px; 
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS ENCICLOPÉDICA (12 ATIVOS)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "DOT-EUR": 1400000000, "ADA-EUR": 35000000000
}

ASSET_DATABASE = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Reserva Soberana", "keyword": "bitcoin",
        "intro": "O Bitcoin é a primeira rede monetária global e digital. É a proteção final contra a inflação dos Bancos Centrais.",
        "pros": ["Escassez Absoluta (21M).", "Inconfiscável.", "Adoção Institucional (ETFs)."],
        "cons": ["Lento para pagamentos diários.", "Risco regulatório."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Autoestrada RWA", "keyword": "ethereum",
        "intro": "A camada de liquidação onde a elite mundial (BlackRock) emite fundos tokenizados e contratos inteligentes.",
        "pros": ["Monopólio em Smart Contracts.", "Mecanismo deflacionário.", "Ecossistema massivo."],
        "cons": ["Taxas (Gas) elevadas.", "Dependência de Layer 2."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados", "keyword": "chainlink",
        "intro": "A ponte que liga o mundo real (preços, dados) à blockchain. Sem LINK, o RWA não funciona.",
        "pros": ["Indispensável para bancos.", "Padrão CCIP interoperável.", "Parceria SWIFT."],
        "cons": ["Complexidade tecnológica.", "Tokenomics lenta."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "keyword": "ripple",
        "intro": "O ativo desenhado para substituir o SWIFT bancário, permitindo liquidação bruta em 3 segundos.",
        "pros": ["Claridade jurídica.", "Velocidade interbancária.", "Conformidade ISO."],
        "cons": ["Centralização corporativa.", "Grande oferta em circulação."]
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "keyword": "quant",
        "intro": "O software Overledger que liga as redes privadas dos bancos às blockchains públicas.",
        "pros": ["Oferta ultra-escassa (14M).", "Foco em CBDCs.", "Software patenteado."],
        "cons": ["Código fechado.", "Baixo interesse de retalho."]
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas Globais", "keyword": "stellar",
        "intro": "Alternativa de baixo custo para remessas internacionais e tokenização de moedas fiat (ISO 20022).",
        "pros": ["Taxas irrisórias.", "Parceria IBM.", "Foco em inclusão financeira."],
        "cons": ["Sombra do XRP.", "Inflação do token."]
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "Infraestrutura IA", "keyword": "render",
        "intro": "Rede DePIN que fornece poder de GPU (placas gráficas) para o treino de Inteligência Artificial.",
        "pros": ["Narrativa IA fortíssima.", "Parceria Apple.", "Utilidade real de hardware."],
        "cons": ["Bolha de tecnologia.", "Dependência de hardware Nvidia."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E RADAR
# ==============================================================================
@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if not df.empty and len(df) >= 2:
            current = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            change = ((current - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = current * SUPPLY_DATA.get(ticker, 0)
            return current, change, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except: return 0.0, 0.0, 0.0, 0.0

def format_val(n):
    if n >= 1e12: return f"€ {(n/1e12):.2f}T"
    if n >= 1e9: return f"€ {(n/1e9):.2f}B"
    if n >= 1e6: return f"€ {(n/1e6):.2f}M"
    return f"€ {n:,.0f}"

@st.cache_data(ttl=600)
def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), 
               ("CoinTelegraph", "https://cointelegraph.com/rss")]
    radar_data = []
    for source, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                radar_data.append({"title": entry.title, "link": entry.link, "source": source, 
                                  "ts": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(radar_data, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. HERO SECTION: O MANIFESTO INSTITUCIONAL
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.6rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 5px; font-weight: bold; margin-top: 10px;">
        INSTITUTIONAL HUB // AGENDA 2030
    </div>
    <p style="margin-top: 25px; font-size: 1.25rem; line-height: 2; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 30px;">
        Este terminal monitoriza a execução da <b>Agenda Global de Liquidez</b>. Enquanto o retalho especula, os bancos centrais e gestoras de triliões (BlackRock, Fidelity) estão a consolidar o novo padrão monetário baseado na norma <b>ISO 20022</b> e na <b>Tokenização de Ativos (RWA)</b>. O nosso objetivo é informar e posicionar o capital estratégico para o Reset Financeiro de 2030.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA TÁTICA (12 ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)

r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

idx = 0
for symbol, info in ASSET_DATABASE.items():
    p, c, v, m = fetch_telemetry(info['ticker'])
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">{info['name']}</div>
            <div class="m-price">€ {p:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{c:+.2f}% (24H)</div>
            <div style="font-size: 0.8rem; color: #475569; margin-top: 15px; border-top: 1px solid #111; padding-top: 8px;">
                MCAP: {format_val(m)} | VOL: {format_val(v)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

st.divider()

# ==============================================================================
# 07. ANÁLISE VISUAL E GAUGE INSTITUCIONAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.2, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN SOBERANO (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=75, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=500,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> FORÇA DE ACUMULAÇÃO</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 89,
        title = {'text': "FLUXO BLACKROCK (ETFs)", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 89}
        }
    ))
    fig_gauge.update_layout(height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR DE NOTÍCIAS (LARGURA TOTAL - AUTO-ROTATE)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL DE INTELIGÊNCIA (FULL WIDTH)</h2>", unsafe_allow_html=True)
st.markdown('<div class="news-full-width">', unsafe_allow_html=True)
news_list = fetch_radar()
items_per_page = 6
if news_list:
    total_pages = max(1, len(news_list) // items_per_page)
    page = st.session_state.news_page % total_pages
    st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.9rem; font-weight: bold; margin-bottom: 15px;'>INTERCEÇÃO {page+1}/{total_pages} (AUTO-ROTATE 30S)</div>", unsafe_allow_html=True)
    for item in news_list[page*items_per_page : (page+1)*items_per_page]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">■ {item['title']}</a>
            <div style="color: #475569; font-size: 0.85rem; font-family: 'JetBrains Mono';">{item['source']} | AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. ARQUITETURA DE RESET FINANCEIRO (TÍTULOS DENTRO DAS BOXES)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET FINANCEIRO</h2>", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">I. Tokenização (RWA): O Colapso da Liquidez Analógica</div>
        <p>A economia mundial está a entrar na era da <b>Tokenização de Ativos do Mundo Real (RWA)</b>. Imagine um prédio de luxo em São João da Madeira avaliado em 1.000.000€. Através do <span style="color:#38bdf8; font-weight:bold;">Ethereum</span>, fragmentamos esse valor em código digital.</p>
        <p>Ao transformar o valor físico em tokens, permitimos liquidação instantânea 24/7. A BlackRock já iniciou a devoração da dívida pública via RWA. Quem detém os carris desta tecnologia controla o fluxo de capital do futuro.</p>
    </div>
    """, unsafe_allow_html=True)



with col_r2:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">II. ISO 20022: O Novo Sistema Nervoso Central</div>
        <p>O sistema SWIFT é o correio do passado. A norma <span style="color:#38bdf8; font-weight:bold;">ISO 20022</span> é o novo padrão mundial obrigatório. Ela exige dados ricos que os bancos tradicionais não conseguem processar fisicamente sem tecnologia blockchain.</p>
        <p>Protocolos como <b>XRP, XLM e QNT</b> são as pontes de liquidez necessárias. O Reset Financeiro obriga os Bancos Centrais a usar estas redes para as suas CBDCs. Nós acumulamos a infraestrutura que o sistema é <b>forçado</b> a usar.</p>
    </div>
    """, unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA DE ATIVOS SOBERANOS (REVERTIDA PARA TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ENCICLOPÉDIA DE ATIVOS SOBERANOS</h2>", unsafe_allow_html=True)
st.write("Dossiê técnico completo sobre a utilidade e o futuro de cada ativo estratégico.")

asset_tabs = st.tabs([f"₿ {ASSET_DATABASE[k]['name']}" for k in ASSET_DATABASE.keys()])

for i, (key, info) in enumerate(ASSET_DATABASE.items()):
    with asset_tabs[i]:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown(f"### Função: {info['role']}")
            st.write(info['intro'])
            st.markdown(f"""
            <table class="jtm-table">
                <thead>
                    <tr><th>🟢 VANTAGENS (ELITE)</th><th>🔴 RISCOS (SISTEMA)</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"### 📡 Interceção de Radar ({info['name']})")
            news = fetch_asset_specific_news = [n for n in news_list if info['keyword'] in n['title'].lower()]
            if news:
                for n in news[:3]:
                    st.markdown(f"<div style='background: #0a0a0a; padding: 15px; margin-bottom: 10px; border-left: 2px solid #38bdf8;'><a href='{n['link']}' style='color: white;'>{n['title']}</a></div>", unsafe_allow_html=True)
            else:
                st.info("A aguardar sinal institucional...")

st.divider()

# ==============================================================================
# 11. MOTOR DE PROJEÇÃO E GLOSSÁRIO
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO SOBERANA 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.4])

with col_p1:
    st.markdown("""
    <div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center; border-radius: 4px;">
        <h3 style="color:#38bdf8;">VALOR DE RESERVA SOBERANA</h3>
        <p style="color:#475569;">Projeção baseada em Absorção total da BlackRock/Bancos Centrais</p>
        <div style="font-size: 5rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 0.9rem; letter-spacing: 3px;">ALVO BITCOIN 2030</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown("""
    <div class="reset-box" style="border-left-color: #fbbf24; min-height: 200px;">
        <h3 style="color:#fbbf24;">A AGENDA DOS LÍDERES MUNDIAIS</h3>
        <p>Os líderes mundiais não estão a investir; estão a <b>substituir a base monetária</b>. Com a dívida fiduciária insustentável, a elite está a drenar o BTC e ETH para cofres institucionais permanentes. Deter estes ativos é deter uma fração da escassez absoluta antes que a porta se feche para o retalho.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align: center; color: #333; font-family: Courier New; padding: 40px;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA | BASE CODE V20.0</p>", unsafe_allow_html=True)

if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
