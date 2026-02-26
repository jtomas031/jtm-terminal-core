import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE INTELIGÊNCIA E GESTÃO DE ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Institutional Behemoth",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Memória de Sessão (Rotação e Simulação)
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0
if 'dca_months' not in st.session_state:
    st.session_state.dca_months = 58  # Meses até 2030

# --- SIDEBAR DE COMANDO ---
with st.sidebar:
    st.markdown("### ⚙️ COMANDO CENTRAL JTM")
    st.markdown("---")
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Sincronização de telemetria e rotação de inteligência.")
    
    st.markdown("---")
    st.markdown("### 🔒 PROTOCOLO DE SOBERANIA")
    st.warning("**OPERAÇÃO DCA:** ATIVA\n\n**CUSTÓDIA:** TREZOR\n\n**DATA CRÍTICA:** DIA 29")
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO TÁTICA (360€)")
    st.progress(300/360, text="BASE (BTC/ETH): 300€")
    st.progress(60/360, text="SNIPER (ISO/RWA): 60€")
    
    st.markdown("---")
    st.markdown("### ⏱️ RELÓGIO GLOBAL")
    st.info(f"Lisboa/S.J.Madeira: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS CORPORATIVO: NEURO-DESIGN & DOPAMINA (ESTILO BLOOMBERG/COINDESK)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=Courier+New&display=swap');
    
    /* Design Global: Abismo Institucional */
    .stApp { 
        background-color: #02040a; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #02040a 80%); 
    }
    
    /* Tipografia e Títulos */
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    p, li { line-height: 1.8; font-size: 1.1rem; color: #cbd5e1; }
    
    /* Hero Section: Título Formal */
    .hero-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 5px solid #38bdf8;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }
    .hero-title {
        font-size: 4rem;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 3px;
    }
    .hero-subtitle {
        font-size: 1.8rem;
        color: #38bdf8;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 6px;
        margin-top: 10px;
    }
    
    /* Cartões de Telemetria */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(2, 4, 10, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 4px;
        transition: 0.4s;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-5px); border-left-color: #10b981; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.2); }
    .m-title { font-size: 1rem; color: #94a3b8; font-family: 'Courier New'; font-weight: bold; }
    .m-price { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }
    
    /* Radar Rotativo (Preenchimento Total do Flanco) */
    .news-hub-sidebar {
        background: #080c17;
        border: 1px solid #1e293b;
        border-left: 4px solid #8b5cf6;
        padding: 25px;
        border-radius: 4px;
        height: 100%;
        min-height: 550px;
    }
    .news-item {
        background: rgba(15, 23, 42, 0.5);
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 2px;
        border-left: 2px solid #38bdf8;
        transition: 0.3s;
    }
    .news-item:hover { background: rgba(30, 41, 59, 0.9); }
    .news-item a { color: #f8fafc; text-decoration: none; font-weight: 700; font-size: 1.05rem; }
    .news-meta { font-size: 0.8rem; color: #64748b; margin-top: 8px; text-transform: uppercase; }
    
    /* Artigos Educativos Massivos */
    .edu-box {
        background-color: #0b1120;
        border: 1px solid #1e293b;
        border-top: 4px solid #34d399;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .edu-title { font-size: 2.5rem; color: #f8fafc; margin-bottom: 30px; border-bottom: 2px solid #1e293b; padding-bottom: 15px; }
    
    /* Tabelas Táticas */
    .tactic-table { width: 100%; border-collapse: collapse; margin: 25px 0; background: #0b1120; }
    .tactic-table th { background: #1e293b; color: #38bdf8; padding: 20px; text-align: left; font-size: 1.3rem; }
    .tactic-table td { border: 1px solid #1e293b; padding: 20px; color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZES DE DADOS E INTELIGÊNCIA (ALTA DENSIDADE)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000,
    "XRP-EUR": 54800000000, "QNT-EUR": 14500000, "XLM-EUR": 28700000000,
    "RNDR-EUR": 388000000, "HBAR-EUR": 33000000000, "ALGO-EUR": 8000000000,
    "SOL-EUR": 440000000
}

@st.cache_data(ttl=25)
def get_market_telemetry(ticker):
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

def format_euro(num):
    if num >= 1e12: return f"€ {(num/1e12):.2f} T"
    if num >= 1e9: return f"€ {(num/1e9):.2f} B"
    if num >= 1e6: return f"€ {(num/1e6):.2f} M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_global_intel():
    urls = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news_radar = []
    for source, url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                news_radar.append({"title": entry.title, "link": entry.link, "source": source, "ts": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(news_radar, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 04. HERO SECTION (AGENDA DOS LÍDERES MUNDIAIS)
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div class="hero-subtitle">INSTITUTIONAL STRATEGY // AGENDA 2030</div>
    <p style="margin-top: 30px; font-size: 1.3rem; line-height: 2; color: #cbd5e1; border-left: 6px solid #38bdf8; padding-left: 30px;">
        Este terminal monitoriza a execução da <b>Agenda Global de Liquidez</b>. Enquanto o retalho especula, os líderes mundiais, bancos centrais e as gestoras de triliões (BlackRock, Vanguard) estão a reescrever o código do dinheiro. A transição para a norma <b>ISO 20022</b> e a <b>Tokenização de Ativos (RWA)</b> são os novos instrumentos de soberania financeira absoluta impostos pela elite global para o horizonte de 2030.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. TELEMETRIA TÁTICA (EUROS €)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)

assets = {
    "BTC": ("BITCOIN (RESERVA)", "BTC-EUR"), "ETH": ("ETHEREUM (SETTLEMENT)", "ETH-EUR"),
    "LINK": ("CHAINLINK (ORACLE)", "LINK-EUR"), "XRP": ("RIPPLE (ISO 20022)", "XRP-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"), "XLM": ("STELLAR (ISO 20022)", "XLM-EUR"),
    "RNDR": ("RENDER (AI COMPUTE)", "RNDR-EUR"), "SOL": ("SOLANA (L1 INFRA)", "SOL-EUR")
}

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
col_list = [c1, c2, c3, c4, c5, c6, c7, c8]

for i, (symbol, (name, ticker)) in enumerate(assets.items()):
    price, chg, vol, mcap = get_market_telemetry(ticker)
    color = "#10b981" if chg >= 0 else "#ef4444"
    with col_list[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{chg:+.2f}% (24H)</div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 15px; border-top: 1px solid #1e293b; padding-top: 10px;">
                MCAP: {format_euro(mcap)} | VOL: {format_euro(vol)}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. CENTRO VISUAL: GRÁFICO, GAUGE E RADAR ROTATIVO (FLANCO DIREITO)
# ==============================================================================
col_chart, col_gauge, col_radar = st.columns([1.6, 0.9, 1.2])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=60, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=520,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> ACUMULAÇÃO</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 84,
        title = {'text': "FORÇA INSTITUCIONAL", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 84}
        }
    ))
    fig_gauge.update_layout(height=480, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=60, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR ROTATIVO</h2>", unsafe_allow_html=True)
    st.markdown('<div class="news-hub-sidebar">', unsafe_allow_html=True)
    news_all = fetch_global_intel()
    items_per_page = 5
    if news_all:
        total_pages = len(news_all) // items_per_page
        page = st.session_state.news_page % total_pages
        st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.85rem; margin-bottom: 15px; font-weight: 800;'>INTERCEÇÃO {page+1}/{total_pages}</div>", unsafe_allow_html=True)
        for item in news_all[page*items_per_page : (page+1)*items_per_page]:
            st.markdown(f'<div class="news-item"><a href="{item["link"]}" target="_blank">{item["title"]}</a><div class="news-meta">{item["source"]} | AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. EDUCAÇÃO MASSIVA (RWA & ISO 20022 - TEXTOS COMPLETOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> O THINK TANK DA JTM CAPITAL</h2>", unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.markdown('<div class="edu-box">', unsafe_allow_html=True)
    st.markdown('<div class="edu-title">I. Tokenização (RWA): O Software que Devora o Mundo</div>', unsafe_allow_html=True)
    st.write("""
    Imagine um apartamento de luxo avaliado em **500.000€**. Se você precisar de **5.000€** hoje, não pode vender apenas a "cozinha" do imóvel. O ativo é ilíquido. A **Tokenização de Ativos do Mundo Real (RWA)** resolve este problema físico através da matemática.
    
    Ao colocar este imóvel na rede **Ethereum**, dividimos a propriedade em 500.000 tokens de 1€. Agora, qualquer investidor em qualquer parte do mundo pode comprar uma fração deste edifício instantaneamente, 24/7. A **BlackRock** já iniciou este processo com o seu fundo BUIDL. Não estamos a falar de moedas de retalho; estamos a falar da digitalização total de toda a propriedade física do planeta.
    """)
    st.markdown('</div>', unsafe_allow_html=True)



with col_e2:
    st.markdown('<div class="edu-box">', unsafe_allow_html=True)
    st.markdown('<div class="edu-title">II. ISO 20022: O Novo Sistema Nervoso Bancário</div>', unsafe_allow_html=True)
    st.write("""
    Enviar dinheiro de Portugal para o Japão hoje via **SWIFT** é como enviar um telegrama na era da internet. É lento, caro e frequentemente opaco. A norma **ISO 20022** é o novo padrão global obrigatório que exige que as transações carreguem dados massivos.
    
    O problema? Os bancos tradicionais não têm largura de banda para isto. Redes como **XRP (Ripple)**, **XLM (Stellar)** e **QNT (Quant)** atuam como os cabos de fibra ótica. Elas permitem que o valor flua em 3 segundos a custo quase zero. Quem detém estes ativos detém os carris por onde os bancos centrais serão obrigados a transacionar biliões em liquidez CBDC.
    """)
    st.markdown('</div>', unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 08. MOTOR DE PROJEÇÃO 2030 (PROJEÇÃO INSTITUCIONAL)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ABSORÇÃO DE LIQUIDEZ GLOBAL 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.5])

with col_p1:
    st.markdown("""
    <div style="background: linear-gradient(45deg, #0f172a, #02040a); border: 2px solid #38bdf8; padding: 50px; text-align: center; border-radius: 8px;">
        <h3 style="color:#38bdf8;">VETOR DE ESCASSEZ SOBERANA</h3>
        <p style="color:#64748b;">Valor Estimado de Unidade de Reserva (Baseado em Absorção Bancária)</p>
        <div style="font-size: 4.5rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 0.9rem; letter-spacing: 2px;">PROJEÇÃO CONSERVADORA 2030 (DCA INSTITUCIONAL)</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown('<div class="edu-box" style="border-left-color: #fbbf24;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#fbbf24;">A AGENDA DOS LÍDERES</h3>', unsafe_allow_html=True)
    st.write("""
    Os líderes mundiais não estão a investir; estão a **substituir a base monetária**. À medida que a oferta de Bitcoin e Ethereum é sugada para os cofres de custódia da BlackRock e dos Fundos Soberanos (Qatar, Arábia Saudita), o preço deixa de responder à oferta e procura e passa a responder à **escassez absoluta**.
    
    Este motor de projeção assume que, até 2030, a moeda fiduciária (Euro/Dólar) terá perdido mais 40% do seu poder de compra. Deter os ativos de infraestrutura (RWA/ISO) é a única forma de sobreviver ao Reset Financeiro que está a ser executado agora.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. DOSSIÊS TÁTICOS (MATRIZ DE RISCO)
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
        st.markdown(f"### 🛡️ PROTOCOLO TREZOR ({name})")
        st.info(f"O ativo {name} deve ser removido da exchange no máximo 24h após a compra. Destino: Cold Storage.")
        st.markdown("**PARCEIROS INSTITUCIONAIS:**")
        st.write("BlackRock, Fidelity, SWIFT, JPMorgan.")

with tabs[0]: render_intel("Bitcoin", "Reserva Soberana", "O escudo contra a inflação fiduciária e o novo padrão-ouro digital absorvido por Wall Street.", ["Escassez absoluta matemática.", "Adoção por Fundos Soberanos."], ["Risco de regulação centralizada.", "Volatilidade de curto prazo."])
with tabs[1]: render_intel("Ethereum", "Autoestrada RWA", "O computador mundial onde a BlackRock e bancos emitem triliões em ativos tokenizados.", ["Monopólio em contratos inteligentes.", "Deflacionário após EIP-1559."], ["Custos de rede elevados.", "Fragmentação de liquidez."])
with tabs[2]: render_intel("Chainlink", "Oráculo de Dados", "A ponte indispensável que liga o SWIFT e bancos reais aos dados da blockchain.", ["Parcerias oficiais com bancos centrais.", "Padrão CCIP de interoperabilidade."], ["Complexidade tecnológica elevada."])
with tabs[3]: render_intel("Ripple", "Liquidez ISO 20022", "A ferramenta de liquidação bruta em tempo real para bancos e CBDCs globais.", ["Velocidade extrema de settlement.", "Conformidade legal estabelecida."], ["Controlo da Ripple Labs."])
with tabs[4]: render_intel("Stellar", "Pagamentos RWA", "Focada em remessas internacionais e tokenização de moedas fiat em mercados emergentes.", ["Parcerias com a IBM e governos.", "Custo de transação zero."], ["Sombra de marketing face ao XRP."])
with tabs[5]: render_intel("Quant", "Sistema Operativo", "O software que permite que as redes privadas de bancos comuniquem com redes públicas.", ["Interoperabilidade B2B exclusiva.", "Oferta escassa (14M)."], ["Código proprietário."])
with tabs[6]: render_intel("Render", "Infraestrutura IA", "A rede descentralizada que fornece poder de GPU para a expansão mundial da Inteligência Artificial.", ["Vital para o processamento de IA.", "Desafia a Google Cloud."], ["Correlacionado com a bolha de IA."])

# ==============================================================================
# 10. GLOSSÁRIO E RODAPÉ (FINALIZAÇÃO)
# ==============================================================================
st.divider()
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO INSTITUCIONAL</h2>", unsafe_allow_html=True)
c_g1, c_g2, c_g3 = st.columns(3)
with c_g1:
    st.write("**RWA:** Ativos reais (ouro, casas) em código digital.")
    st.write("**CBDC:** Moedas digitais de Bancos Centrais (Controlo).")
with c_g2:
    st.write("**ISO 20022:** A norma rica em dados do novo sistema bancário.")
    st.write("**Settlement:** A liquidação definitiva de um pagamento.")
with c_g3:
    st.write("**Cold Storage:** Guardar chaves privadas fora da internet (Trezor).")
    st.write("**Smart Contracts:** Acordos automáticos que eliminam notários.")

st.divider()
st.markdown("<p style='text-align: center; color: #444; font-family: Courier New; padding: 30px;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA | PORTUGAL NÓ CENTRAL</p>", unsafe_allow_html=True)

# Loop Autónomo (Avança notícias a cada 30 segundos)
if auto_update:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
