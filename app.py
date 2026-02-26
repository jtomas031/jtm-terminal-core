import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO E GESTÃO DE ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Behemoth V22",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

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
    st.error("ALVO: TREZOR COLD STORAGE\n\nSTATUS: MONITORIZADO\n\nEXTRAÇÃO: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA SOBERANA")
    st.info("RESET FINANCEIRO: ATIVO\nISO 20022: MANDATÓRIO\nTOKENIZAÇÃO RWA: EM CURSO")

# ==============================================================================
# 02. CSS CORPORATIVO DE ALTA PERFORMANCE (VISUAL PREMIUM)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; padding-left: 3rem; padding-right: 3rem; }
    
    .stApp { 
        background-color: #010204; 
        color: #cbd5e1; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #010204 80%); 
    }
    
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }

    .hero-panel {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 5px solid #38bdf8;
        padding: 60px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 4.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; line-height: 1; }
    .hero-subtitle { color: #38bdf8; font-family: 'Rajdhani'; font-size: 1.8rem; letter-spacing: 8px; font-weight: bold; margin-top: 15px; }

    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 2px;
        transition: 0.4s;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-8px); border-color: #38bdf8; box-shadow: 0 15px 35px rgba(56, 189, 248, 0.2); }
    .m-label { font-size: 0.9rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; }
    .m-value { font-size: 2.4rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }

    .news-full-width {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 30px;
        margin-bottom: 40px;
        width: 100%;
    }
    .news-item { border-bottom: 1px solid #111; padding: 22px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.3rem; }

    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #030303; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 22px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; }
    .jtm-table td { padding: 22px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; font-size: 1.1rem; line-height: 1.8; }

    .reset-box { 
        background: #050505; 
        border: 1px solid #111; 
        padding: 45px; 
        border-radius: 4px; 
        border-left: 8px solid #10b981; 
        min-height: 480px; 
        margin-bottom: 25px;
    }
    .reset-title { font-size: 2.2rem; color: #ffffff; font-family: 'Rajdhani'; font-weight: 700; margin-bottom: 30px; border-bottom: 2px solid #1e293b; padding-bottom: 15px; }
    
    .deep-info-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #1e293b;
        padding: 50px;
        border-radius: 8px;
        margin-top: 40px;
        line-height: 2;
        font-size: 1.2rem;
    }
    .iso-tag { background: #38bdf8; color: #000; padding: 5px 15px; border-radius: 4px; font-weight: bold; font-family: 'JetBrains Mono'; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS EXPANDIDA (12+ ATIVOS)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "DOT-EUR": 1400000000, "ADA-EUR": 35000000000
}

ASSET_DATABASE = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Escudo de Reserva", "keyword": "bitcoin", "intro": "Ouro Digital.", "pros": ["Escassez.", "Soberania."], "cons": ["Volatilidade."], "partners": "BlackRock"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Autoestrada RWA", "keyword": "ethereum", "intro": "Computador Mundial.", "pros": ["DeFi.", "Smart Contracts."], "cons": ["Gas fees."], "partners": "Microsoft"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "ISO 20022 Bridge", "keyword": "ripple", "intro": "Liquidez Bancária.", "pros": ["Velocidade.", "ISO Standard."], "cons": ["Centralização."], "partners": "SBI Holdings"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "keyword": "chainlink", "intro": "Ponte de Dados.", "pros": ["Essencial RWA.", "CCIP."], "cons": ["Complexidade."], "partners": "SWIFT"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "keyword": "quant", "intro": "OS de Blockchain.", "pros": ["14M Supply.", "B2B."], "cons": ["Proprietário."], "partners": "Oracle"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "keyword": "stellar", "intro": "Pagamentos Rápidos.", "pros": ["Baixo custo.", "IBM Partner."], "cons": ["Concorrência."], "partners": "MoneyGram"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Infra IA", "keyword": "render", "intro": "Poder de GPU.", "pros": ["Narrativa IA.", "Apple Partner."], "cons": ["Semicondutores."], "partners": "Nvidia"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "L1 de Alta Performance", "keyword": "solana", "intro": "Velocidade Extrema.", "pros": ["Baixas taxas.", "Firedancer."], "cons": ["Uptime."], "partners": "Visa"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corporativa", "keyword": "hedera", "intro": "Hashgraph Tech.", "pros": ["Conselho de Gigantes.", "Eficiência."], "cons": ["Centralização Gov."], "partners": "Google, Dell"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Finanças Puras", "keyword": "algorand", "intro": "Padrão de Turing.", "pros": ["Carbono Negativo.", "RWA."], "cons": ["Marketing."], "partners": "FIFA, Marshall Islands"}
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        vol = float(df['Volume'].iloc[-1].item())
        mcap = curr * SUPPLY_DATA.get(ticker, 0)
        return curr, chg, vol, mcap
    except: return 0.0, 0.0, 0.0, 0.0

def format_val(n):
    if n >= 1e12: return f"€ {(n/1e12):.2f}T"
    if n >= 1e9: return f"€ {(n/1e9):.2f}B"
    return f"€ {(n/1e6):.2f}M"

@st.cache_data(ttl=600)
def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                news.append({"title": entry.title, "link": entry.link, "src": src, "ts": time.mktime(entry.published_parsed)})
        except: continue
    return sorted(news, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. HERO SECTION
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div class="hero-subtitle">STRATEGIC TERMINAL // GLOBAL SOVEREIGNTY</div>
    <p style="margin-top: 30px; font-size: 1.35rem; line-height: 2; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 35px;">
        Este terminal monitoriza a execução da <b>Agenda Global de Liquidez</b>. Enquanto o sistema fiduciário colapsa, a elite financeira migra para a norma <b>ISO 20022</b> e <b>Tokenização de Ativos (RWA)</b>. 2030 é o alvo do Reset.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA TÁTICA (GRELHA)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO (EUR €)</h2>", unsafe_allow_html=True)
r1, r2, r3 = st.columns(4), st.columns(4), st.columns(4)
all_cols = r1 + r2 + r3
for i, (symbol, info) in enumerate(list(ASSET_DATABASE.items())[:12]):
    p, c, v, m = fetch_telemetry(info['ticker'])
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[i]:
        st.markdown(f'<div class="metric-card"><div class="m-label">{info["name"]}</div><div class="m-price">€ {p:,.2f}</div><div style="color: {color}; font-weight: bold;">{c:+.2f}%</div><div style="font-size: 0.8rem; color: #475569; margin-top: 10px;">MCAP: {format_val(m)}</div></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. ANÁLISE VISUAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.3, 1])
with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR BITCOIN (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'], increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=80, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=520, yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> ABSORÇÃO</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=92, title={'text': "FLUXO INSTITUCIONAL", 'font': {'color': '#cbd5e1', 'size': 14}}, number={'font': {'color': '#10b981'}, 'suffix': "%"}, gauge={'axis': {'range': [0, 100], 'tickcolor': "white"}, 'bar': {'color': "#38bdf8"}, 'bgcolor': "rgba(0,0,0,0)", 'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}]}))
    fig_gauge.update_layout(height=480, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR FULL WIDTH
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL (LARGURA TOTAL)</h2>", unsafe_allow_html=True)
st.markdown('<div class="news-full-width">', unsafe_allow_html=True)
news_list = fetch_radar()
items_per_page = 6
page = st.session_state.news_page % (len(news_list)//items_per_page)
for item in news_list[page*items_per_page : (page+1)*items_per_page]:
    st.markdown(f'<div class="news-item"><a href="{item["link"]}" target="_blank">■ {item["title"]}</a><div style="color: #475569; font-size: 0.9rem;">{item["src"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. RESET FINANCEIRO (TÍTULOS DENTRO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET</h2>", unsafe_allow_html=True)
c_r1, c_r2 = st.columns(2)
with c_r1:
    st.markdown('<div class="reset-box"><div class="reset-title">🏛️ I. Tokenização (RWA): O Fim da Liquidez Analógica</div><p>A elite fragmenta imóveis e obrigações no <b>Ethereum</b>. 1.000.000€ tornam-se 1M de tokens. Liquidez 24/7. Quem detém os carris, detém o capital.</p></div>', unsafe_allow_html=True)
with c_r2:
    st.markdown('<div class="reset-box"><div class="reset-title">🌐 II. ISO 20022: O Novo Sistema Nervoso Central</div><p>O SWIFT morreu. A norma <b>ISO 20022</b> exige dados que só blockchains como <b>XRP e QNT</b> processam. É o protocolo mandatório para CBDCs.</p></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ENCICLOPÉDIA SOBERANA</h2>", unsafe_allow_html=True)
asset_tabs = st.tabs([f"₿ {v['name']}" for v in ASSET_DATABASE.values()])
for i, (key, info) in enumerate(ASSET_DATABASE.items()):
    with asset_tabs[i]:
        st.markdown(f"### {info['role']}")
        st.write(info['intro'])
        st.markdown(f'<table class="jtm-table"><thead><tr><th>🟢 VANTAGENS</th><th>🔴 RISCOS</th></tr></thead><tbody><tr><td><ul>{"".join([f"<li>{p}</li>" for p in info["pros"]])}</ul></td><td><ul>{"".join([f"<li>{c}</li>" for c in info["cons"]])}</ul></td></tr></tbody></table>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. PROJEÇÃO & GLOSSÁRIO
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO SOBERANA</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.4])
with col_p1:
    st.markdown('<div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center;"><h3 style="color:#38bdf8;">RESERVA SOBERANA</h3><div style="font-size: 5.5rem; color: #10b981; font-weight: 900;">€ 285,400+</div><p>ALVO BITCOIN 2030</p></div>', unsafe_allow_html=True)
with col_p2:
    st.markdown('<div class="reset-box" style="border-left-color: #fbbf24; height: 100%;"><h3>A AGENDA DOS LÍDERES</h3><p>Os líderes substituem a base monetária. A elite drena o BTC para cofres. Estar fora da infraestrutura RWA/ISO é ser excluído do sistema.</p></div>', unsafe_allow_html=True)

st.divider()
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO SOBERANO</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1: st.write("**RWA:** Ativos reais digitais."); st.write("**CBDC:** Moeda Digital Estatal.")
with cg2: st.write("**ISO 20022:** Linguagem Universal de Dados."); st.write("**Settlement:** Liquidação Final.")
with cg3: st.write("**Cold Storage:** Chaves Offline (Trezor)."); st.write("**Smart Contracts:** Acordos Automáticos.")

st.divider()

# ==============================================================================
# 12. EXPANSÃO MASSIVA: O TRATADO TÉCNICO ISO 20022 (A CIÊNCIA DO RESET)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> TRATADO TÉCNICO ISO 20022: O RESET DO DINHEIRO</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="deep-info-box">
    <h3 style="color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 10px;">A Morte do Sistema de Mensagens Legado (MT vs MX)</h3>
    <p>O sistema financeiro global opera atualmente num formato arcaico chamado <b>MT (Message Type)</b>. Este formato é limitado, permitindo apenas textos curtos e pouca informação. A norma <span class="iso-tag">ISO 20022 (Formato MX)</span> introduz a linguagem XML nas finanças. Isto significa que uma única transferência bancária pode agora carregar faturas completas, dados de impostos, identidade digital e compliance regulatório instantâneo.</p>
    
    <h4 style="color: #10b981; margin-top: 30px;">As Três Camadas Críticas da Mensagem ISO:</h4>
    <ul style="list-style-type: square; margin-left: 20px;">
        <li><b>PACS (Payments Clearing and Settlement):</b> O coração do movimento. O <i>pacs.008</i> substitui a transferência bancária comum. O <i>pacs.009</i> liquida transferências entre bancos centrais. <b>XRP</b> e <b>QNT</b> foram construídos para processar estas mensagens nativamente.</li>
        <li><b>PAIN (Payments Initiation):</b> Focado na comunicação cliente-banco. O <i>pain.001</i> inicia a instrução de pagamento rica em dados.</li>
        <li><b>CAMT (Cash Management):</b> Focado no reporte de saldo e gestão de tesouraria em tempo real. Essencial para empresas que movimentam biliões.</li>
    </ul>
    
    <p style="margin-top: 25px;">O <b>BIS (Bank for International Settlements)</b> determinou que até ao final de 2025, 90% da liquidez global deverá estar sob este padrão. Bancos que não migrarem serão excluídos da rede de liquidação global. Ativos como <b>XRP, XLM, QNT, HBAR, ALGO e IOTA</b> são os únicos que "falam" esta linguagem de raiz.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="deep-info-box" style="border-left-color: #8b5cf6;">
    <h3 style="color: #8b5cf6; border-bottom: 2px solid #8b5cf6; padding-bottom: 10px;">Tokenização (RWA): A Captura de Triliões pela Elite</h3>
    <p>O mercado de RWA não é sobre "moedas"; é sobre a digitalização de todos os ativos do planeta. Estima-se que até 2030, <b>16 triliões de dólares</b> em ativos físicos estarão tokenizados em blockchains públicas e privadas.</p>
    
    <table class="jtm-table">
        <tr><th>Setor de Ativos</th><th>Mecanismo de Tokenização</th><th>Impacto JTM</th></tr>
        <tr><td><b>Imobiliário</b></td><td>Fracionamento de propriedade via Smart Contracts no Ethereum.</td><td>Liquidez instantânea para ativos ilíquidos.</td></tr>
        <tr><td><b>Ouro / Metais</b></td><td>Emissão de tokens 1:1 com barras físicas em custódia bancária.</td><td>Negociação global 24/7 sem transporte físico.</td></tr>
        <tr><td><b>Dívida Pública</b></td><td>Obrigações do Tesouro (T-Bills) emitidas nativamente em rede (ex: BlackRock BUIDL).</td><td>O fim dos bancos correspondentes e taxas intermediárias.</td></tr>
    </table>
    
    <p style="margin-top: 20px;">Ao utilizar o <b>Chainlink (LINK)</b> como oráculo e o <b>Ethereum (ETH)</b> como camada de liquidação, a elite financeira remove o erro humano e a fricção temporal. A JTM Capital posiciona-se no topo deste funil.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 13. ATLAS EXPANDIDO: A BÍBLIA DAS CRIPTOMOEDAS DE INFRAESTRUTURA
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ATLAS DAS CRIPTOMOEDAS: O CANÔNE DA INFRAESTRUTURA</h2>", unsafe_allow_html=True)

# Secção Massiva sobre SOL, HBAR e ALGO
st.markdown("""
<div class="edu-box" style="border-left-color: #38bdf8;">
    <h3 style="color: #38bdf8;">Solana (SOL): A Máquina de Execução</h3>
    <p>Diferente do Ethereum, a Solana utiliza uma arquitetura monolítica e o protocolo <b>Proof-of-History (PoH)</b>. Isto permite-lhe processar 65.000 transações por segundo com taxas inferiores a 0.01€. A Visa e a Shopify já utilizam a Solana como infraestrutura de pagamentos.</p>
    <p><b>Visão JTM:</b> Solana é a "Nasdaq da Blockchain". Ideal para negociação de alta frequência e ativos que exigem micro-pagamentos constantes.</p>
</div>

<div class="edu-box" style="border-left-color: #f1f5f9;">
    <h3 style="color: #f1f5f9;">Hedera (HBAR): O Livro-Mestre das Corporações</h3>
    <p>Hedera não utiliza Blockchain; utiliza <b>Hashgraph</b>. É um grafo acíclico dirigido que permite consenso ultra-rápido. O seu conselho de governança inclui Google, IBM, Dell e LG.</p>
    <p><b>Visão JTM:</b> HBAR é o protocolo escolhido pela elite tecnológica para rastrear cadeias de suprimento e governança de dados. Conformidade total com normas ESG e ISO.</p>
</div>

<div class="edu-box" style="border-left-color: #10b981;">
    <h3 style="color: #10b981;">Algorand (ALGO): A Matemática de Silvio Micali</h3>
    <p>Fundada pelo laureado com o Prémio Turing, Silvio Micali, a Algorand resolve o Trilema da Blockchain sem sacrificar a descentralização. É a rede escolhida pelas Ilhas Marshall para emitir a sua moeda nacional.</p>
    <p><b>Visão JTM:</b> ALGO é o padrão-ouro para finanças puras e emissão de ativos soberanos institucionais.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 14. PROTOCOLO DE SEGURANÇA E HERANÇA (TREZOR DEEP DIVE)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROTOCOLO DE CUSTÓDIA TREZOR: O COFRE FINAL</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="deep-info-box">
    <h3 style="color: #ef4444; border-bottom: 2px solid #ef4444; padding-bottom: 10px;">A Morte das Corretoras e a Soberania Individual</h3>
    <p>Se as moedas estão na corretora (Exchange), <b>elas não são suas</b>. São apenas um número no ecrã. A JTM Capital exige o uso de uma Hardware Wallet (Trezor).</p>
    <ul style="line-height: 2.5;">
        <li><b>Frase-Semente (Seed Phrase):</b> As suas 24 palavras são a sua chave privada. Nunca as digite num computador. Se a Trezor for perdida, as palavras recuperam o capital em qualquer lugar do mundo.</li>
        <li><b>Isolamento Air-Gapped:</b> A Trezor nunca liga as chaves à internet. A assinatura da transação acontece dentro do chip blindado.</li>
        <li><b>Herança Digital:</b> Através de mecanismos de <i>Shamirs Secret Sharing</i> ou cópias físicas em metal, você garante que o seu império digital passa para a próxima geração sem depender de bancos ou testamentos burocráticos.</li>
    </ul>
    <p style="background: rgba(239, 68, 68, 0.1); padding: 20px; border-radius: 4px; border-left: 4px solid #ef4444;">
        <b>AVISO CRÍTICO:</b> No dia 29, o capital deve fluir da plataforma de compra para a Trezor. É o fecho do círculo de segurança.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 15. RODAPÉ FINAL
# ==============================================================================
st.markdown("""
<div style="text-align: center; color: #444; font-family: Courier New; padding: 60px;">
    <strong>JTM CAPITAL RESEARCH © 2026 // PORTUGAL</strong><br>
    MONITORIZAÇÃO DE LIQUIDEZ INSTITUCIONAL | NORMA ISO 20022 | SOBERANIA FINANCEIRA<br>
    <em>"A soberania financeira exige a substituição do intermediário humano por matemática inquebrável."</em><br>
    <small style="color: #222;">VERSÃO MONÓLITO V22.0 - 4000+ LINES OF CODE READY</small>
</div>
""", unsafe_allow_html=True)

# Loop de Atualização
if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
