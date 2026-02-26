import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DO SISTEMA & MEMÓRIA ROTATIVA
# ==============================================================================
st.set_page_config(page_title="JTM CAPITAL RESEARCH | Hub", layout="wide", page_icon="🏛️", initial_sidebar_state="expanded")

# Inicializar a memória de paginação das notícias (Roda a cada 30s)
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# Painel de Comando Lateral
with st.sidebar:
    st.markdown("### ⚙️ COMANDO CENTRAL JTM")
    st.markdown("---")
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Telemetria e rotação de notícias sincronizadas.")
    st.markdown("---")
    st.markdown("### 🔒 PROTOCOLO DE SEGURANÇA")
    st.warning("**OPERAÇÃO DCA:** ATIVA\n\n**DESTINO FINAL:** TREZOR\n\n**DATA CRÍTICA:** DIA 29")
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO MENSAL (360€)")
    st.progress(300/360, text="BASE (BTC/ETH): 300€")
    st.progress(60/360, text="SNIPER (ISO/DePIN): 60€")

# ==============================================================================
# 02. CSS CORPORATIVO (NEURO-DESIGN AVANÇADO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=Courier+New&display=swap');
    
    .stApp { background-color: #02040a; color: #e2e8f0; font-family: 'Inter', sans-serif; background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #02040a 80%); }
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1.5px; }
    p, li { line-height: 1.8; font-size: 1.05rem; color: #cbd5e1; }
    .highlight-blue { color: #38bdf8; font-weight: 700; }
    .highlight-green { color: #10b981; font-weight: 700; }
    
    .hero-container { background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.15); border-top: 3px solid #38bdf8; padding: 40px 40px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    .hero-title { font-size: 3rem; font-family: 'Courier New', monospace; font-weight: 900; color: #ffffff; letter-spacing: 2px; border-bottom: 2px solid #1e293b; padding-bottom: 10px; margin-bottom: 10px; }
    
    .metric-card { background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(2, 4, 10, 0.9)); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #38bdf8; padding: 20px; border-radius: 8px; transition: all 0.3s ease; height: 100%; }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.1); border-left: 4px solid #10b981; }
    .m-title { font-size: 1rem; color: #94a3b8; font-family: 'Courier New', monospace; font-weight: bold; }
    .m-price { font-size: 1.8rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; margin: 5px 0; }
    .m-data-row { display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 5px; }
    
    /* Radar Compacto Rotativo */
    .news-hub-compact { background: #080c17; border: 1px solid #1e293b; border-left: 4px solid #8b5cf6; border-radius: 8px; padding: 15px; height: 100%; min-height: 450px; }
    .news-item { background: rgba(15, 23, 42, 0.6); padding: 12px; margin-bottom: 10px; border-radius: 4px; border-left: 2px solid #38bdf8; transition: background 0.3s; }
    .news-item:hover { background: rgba(30, 41, 59, 0.9); }
    .news-item a { color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 0.95rem; }
    .news-meta { font-size: 0.75rem; color: #64748b; margin-top: 5px; text-transform: uppercase; }
    
    .edu-box { background-color: #0b1120; border: 1px solid #1e293b; border-top: 3px solid #34d399; padding: 30px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    .tactic-table { width: 100%; border-collapse: collapse; margin: 15px 0; background: #0b1120; border-radius: 8px; overflow: hidden; }
    .tactic-table th { background: #1e293b; color: #38bdf8; padding: 12px; text-align: left; font-family: 'Rajdhani'; font-size: 1.1rem; }
    .tactic-table td { border: 1px solid #1e293b; padding: 12px; color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MOTORES DE CÁLCULO
# ==============================================================================
SUPPLY_MATRIX = {
    "BTC-EUR": 19_650_000, "ETH-EUR": 120_000_000, "LINK-EUR": 587_000_000,
    "XRP-EUR": 54_800_000_000, "QNT-EUR": 14_500_000, "XLM-EUR": 28_700_000_000, "RNDR-EUR": 388_000_000
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

def format_currency(num):
    if num >= 1_000_000_000_000: return f"€ {(num / 1_000_000_000_000):.2f} T"
    if num >= 1_000_000_000: return f"€ {(num / 1_000_000_000):.2f} B"
    if num >= 1_000_000: return f"€ {(num / 1_000_000):.2f} M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_global_radar():
    sources = [
        ("CoinDesk Inst.", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("CoinTelegraph", "https://cointelegraph.com/rss"),
        ("CryptoSlate", "https://cryptoslate.com/feed/")
    ]
    radar_data = []
    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                radar_data.append({
                    "title": entry.title, "link": entry.link,
                    "date": entry.published[:22] if hasattr(entry, 'published') else "Recente",
                    "source": source_name,
                    "timestamp": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') and entry.published_parsed else 0
                })
        except: continue
    return sorted(radar_data, key=lambda x: x['timestamp'], reverse=True)

@st.cache_data(ttl=600)
def fetch_asset_specific_news(keyword):
    return [n for n in fetch_global_radar() if keyword.lower() in n['title'].lower()][:4]

# ==============================================================================
# 04. HERO SECTION
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH // INSTITUTIONAL HUB</div>
    <div style="font-size: 1.2rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 3px;">TRANSIÇÃO MACROECONÓMICA | RWA | ISO 20022</div>
    <p style="margin-top: 15px; color: #cbd5e1; max-width: 900px; font-size: 1rem;">
        Monitorização militar sobre o colapso fiduciário. Operamos baseados em utilidade matemática e fluxos de capital institucionais. Ruído de retalho descartado.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. PAINEL DE TELEMETRIA TÁTICA
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> TELEMETRIA DO IMPÉRIO (EUR €)</h2>", unsafe_allow_html=True)

assets_matrix = {
    "BTC": ("BITCOIN (ESCUDO)", "BTC-EUR"), "ETH": ("ETHEREUM (BASE)", "ETH-EUR"),
    "LINK": ("CHAINLINK (ORÁC)", "LINK-EUR"), "XRP": ("RIPPLE (ISO)", "XRP-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"), "XLM": ("STELLAR (ISO)", "XLM-EUR"),
    "RNDR": ("RENDER (DePIN)", "RNDR-EUR")
}

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
cols_array = [c1, c2, c3, c4, c5, c6, c7]

for i, (symbol, (name, ticker)) in enumerate(assets_matrix.items()):
    price, change, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    arrow = "▲" if change >= 0 else "▼"
    
    with cols_array[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {price:,.3f}</div>
            <div style="color: {color}; font-weight: bold; font-family: 'Courier New';">{arrow} {abs(change):.2f}% (24H)</div>
            <div class="m-data-row"><span>V: {format_currency(vol)}</span><span>MC: {format_currency(mcap)}</span></div>
        </div>
        """, unsafe_allow_html=True)

with c8:
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #8b5cf6; text-align: center;">
        <div style="color: #a78bfa; font-family: 'Courier New'; font-weight: bold; font-size: 1rem;">ESTADO DO NÓ</div>
        <div style="color: #ffffff; font-size: 1.3rem; font-weight: 800; margin-top: 15px;">ONLINE</div>
        <div style="color: #10b981; font-size: 0.8rem; margin-top: 5px;">Sincronizado</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. CENTRO VISUAL: GRÁFICO, MEDIDOR DE TENDÊNCIA E RADAR ROTATIVO
# ==============================================================================
col_chart, col_gauge, col_radar = st.columns([1.5, 1, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO (RESTAURADO)</h2>", unsafe_allow_html=True)
    
    @st.cache_data(ttl=900)
    def render_tactical_chart(ticker):
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#10b981', decreasing_line_color='#ef4444'
            )])
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=10, t=10, b=30), xaxis_rangeslider_visible=False, height=450,
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€"), 
                xaxis=dict(showgrid=False, color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
    render_tactical_chart("BTC-EUR")

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> FLUXO INSTITUCIONAL</h2>", unsafe_allow_html=True)
    # Gráfico de Velocímetro (Estilo Bloomberg/CoinDesk Trending)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 82,
        title = {'text': "FORÇA DE ACUMULAÇÃO (BlackRock/ETFs)", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.3)"},
                {'range': [40, 60], 'color': "rgba(245, 158, 11, 0.3)"},
                {'range': [60, 100], 'color': "rgba(16, 185, 129, 0.3)"}
            ],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 82}
        }
    ))
    fig_gauge.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR ROTATIVO</h2>", unsafe_allow_html=True)
    st.markdown('<div class="news-hub-compact">', unsafe_allow_html=True)
    
    global_news = fetch_global_radar()
    
    # Lógica de Paginação (Rotatividade Autónoma 5 em 5)
    items_per_page = 5
    if len(global_news) > 0:
        total_pages = max(1, len(global_news) // items_per_page)
        current_page = st.session_state.news_page % total_pages
        start_idx = current_page * items_per_page
        
        st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.8rem; margin-bottom: 10px;'>Página {current_page+1}/{total_pages} (Roda a cada 30s)</div>", unsafe_allow_html=True)
        
        for item in global_news[start_idx : start_idx + items_per_page]:
            st.markdown(f"""
            <div class="news-item">
                <a href="{item['link']}" target="_blank">{item['title']}</a>
                <div class="news-meta">{item['source']} | {item['date']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Sem sinal do radar no momento.")
        
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. THINK TANK EDUCACIONAL (ACELERADO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA MACROECONÓMICA 2026-2030</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="edu-box">
    <div style="font-size: 1.8rem; color: #f8fafc; margin-bottom: 15px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">I. O Colapso Fiduciário e a Tokenização (RWA)</div>
    <p>O Euro é inflacionado por dívida governamental. O <span class="highlight-green">Bitcoin (BTC)</span> protege contra a desvalorização através da escassez absoluta (21 milhões). A seguir à reserva de valor, temos a infraestrutura. A <span class="highlight-blue">Tokenização de Ativos do Mundo Real (RWA)</span> transforma imóveis, ações e obrigações do tesouro em tokens divisíveis na rede Ethereum. A BlackRock já aderiu. É a digitalização irreversível do capital global.</p>
</div>

<div class="edu-box">
    <div style="font-size: 1.8rem; color: #f8fafc; margin-bottom: 15px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">II. A Morte do SWIFT e a Norma ISO 20022</div>
    <p>O sistema SWIFT é arcaico. O mundo bancário exige a nova norma <span class="highlight-blue">ISO 20022</span>, que carrega dados pesados. Os bancos legados não aguentam a carga; pontes criptográficas como o <span class="highlight-green">XRP</span> e o <span class="highlight-green">XLM</span> liquidam a transferência em 3 segundos. Nós acumulamos a infraestrutura que os bancos serão forçados a comprar para sobreviverem.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. DOSSIÊS TÁTICOS
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> DOSSIÊS DE INFRAESTRUTURA (PELOTÃO JTM)</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["₿ BTC", "⟠ ETH", "🔗 LINK", "✕ XRP", "◎ XLM", "Ⓠ QNT", "🧊 RNDR"])

def render_asset_intel(name, role, thesis, pros, cons):
    st.markdown(f"### Função Tática: {role}")
    st.write(thesis)
    st.markdown("""
    <table class="tactic-table">
        <tr><th style="border-left: 4px solid #10b981;">🟢 PRÓS INSTITUCIONAIS</th><th style="border-left: 4px solid #ef4444;">🔴 RISCOS ESTRATÉGICOS</th></tr>
        <tr>
            <td style="vertical-align: top;"><ul>""" + "".join([f"<li>{p}</li>" for p in pros]) + """</ul></td>
            <td style="vertical-align: top;"><ul>""" + "".join([f"<li>{c}</li>" for c in cons]) + """</ul></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

with tab1: render_asset_intel("Bitcoin", "O Escudo Monetário (Camada 0)", "Imunidade total à inflação fiat e adoção institucional provada (ETFs).", ["Proteção final contra emissão de euros.", "Aprovado por Wall Street."], ["Rede lenta.", "Risco regulatório ambiental (energia)."])
with tab2: render_asset_intel("Ethereum", "A Autoestrada Global (RWA)", "A fundação da economia digital (DeFi) e emissão de fundos tokenizados da BlackRock.", ["Domínio absoluto em RWA.", "Rendimento passivo institucional."], ["Taxas (Gas) altas.", "Dependência de L2s."])
with tab3: render_asset_intel("Chainlink", "O Oráculo de Dados", "Fornece preços do mundo real aos Smart Contracts (ex: preço do ouro para tokenização).", ["Monopólio em Oráculos corporativos.", "Parceria SWIFT."], ["Tokenomics complexos."])
with tab4: render_asset_intel("Ripple", "Veículo de Liquidez (ISO 20022)", "A ponte de liquidação bancária rápida, desenhada para CBDCs e substituição do SWIFT.", ["Vitória jurídica (SEC).", "Transações em 3 segundos."], ["Empresa detém muito XRP (Escrow)."])
with tab5: render_asset_intel("Stellar", "Pagamentos Inclusivos (ISO)", "Alternativa focada em remessas e tokenização de moedas fiduciárias.", ["Parcerias IBM.", "Micro-pagamentos ideais."], ["Sombra de marketing face ao XRP."])
with tab6: render_asset_intel("Quant", "Sistema Operativo (Interop)", "Permite que redes privadas de bancos comuniquem com o Ethereum.", ["Liga B2B/B2G.", "Oferta extremamente escassa (14.5M)."], ["Código fechado.", "Foco estritamente corporativo."])
with tab7: render_asset_intel("Render", "Infraestrutura IA (DePIN)", "Aluguer global de placas gráficas (GPUs) para processamento de IA.", ["Fuga ao monopólio da Amazon AWS.", "Crescimento massivo devido à IA."], ["Correlacionado ao hype momentâneo da IA."])

st.divider()
st.markdown("<div style='text-align: center; color: #64748b; font-family: Courier New; padding: 20px;'><strong>JTM CAPITAL RESEARCH © 2026</strong><br>OPERAÇÃO DCA 360€ | PRÓXIMA EXTRAÇÃO TREZOR: DIA 29</div>", unsafe_allow_html=True)

# Loop Autónomo e Incremento da Página de Notícias
if auto_update:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
