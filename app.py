import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO & DESIGN INSTITUCIONAL
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V43",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Estado
if 'news_cycle' not in st.session_state:
    st.session_state.news_cycle = 0

# --- SIDEBAR: GOVERNANÇA (DESIGN ONDO) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 3px;'>CORE MASTER V43.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização de Fluxo", value=True)
    
    st.markdown("### 📊 ALOCAÇÃO")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔒 CUSTÓDIA")
    st.warning("Protocolo: TREZOR COLD STORAGE\nExtração: DIA 29")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: OBSIDIAN GLASS (TABELAS BLINDADAS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 3rem 6rem; max-width: 1600px; margin: 0 auto; }
    .stApp { background-color: #030712; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Hero Style */
    .hero-container { padding: 80px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 60px; }
    .hero-title { font-size: 5rem; font-weight: 800; line-height: 1; margin-bottom: 20px; }
    .hero-desc { font-size: 1.4rem; color: #94a3b8; max-width: 900px; font-weight: 300; }

    /* Asset Cards */
    .q-card {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 30px;
        border-radius: 12px;
        transition: 0.3s;
        border-left: 4px solid #10b981;
    }
    .q-card:hover { border-color: #10b981; transform: translateY(-5px); }
    .q-price { font-size: 2rem; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* News Monitor */
    .pulse-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 40px;
        border-radius: 16px;
        height: 600px;
        overflow-y: auto;
    }
    .news-item { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 20px 0; }
    .news-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.2rem; }

    /* Tables */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .sovereign-table th { text-align: left; padding: 20px; color: #64748b; font-size: 0.8rem; text-transform: uppercase; border-bottom: 2px solid #1e293b; }
    .sovereign-table td { padding: 20px; border-bottom: 1px solid #1e293b; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS (DATABASE COMPLETA)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Escassez",
        "why": "Ouro digital. Ativo de escassez absoluta finita (21M). Proteção contra o colapso fiduciário.",
        "pros": ["Escassez 21M", "Adoção Institucional", "Soberania"],
        "cons": ["Volatilidade", "Lentidão L1"],
        "link": "https://bitcoin.org/bitcoin.pdf",
        "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica",
        "why": "O sistema operativo das finanças. Camada onde triliões em RWA serão liquidados.",
        "pros": ["Deflacionário", "Líder RWA", "Ecossistema"],
        "cons": ["Gas fees", "Competição L1"],
        "link": "https://ethereum.org/",
        "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "Substituto do SWIFT. Ativo de ponte para liquidação instantânea entre bancos.",
        "pros": ["Velocidade (3s)", "Conformidade", "Baixo Custo"],
        "cons": ["Regulação", "Centralização"],
        "link": "https://ripple.com/",
        "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e o digital.",
        "pros": ["BlackRock Partnership", "Yield Seguro", "Líder RWA"],
        "cons": ["Dependência Fiat"],
        "link": "https://ondo.finance/",
        "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "Overledger OS. Permite que blockchains privadas de bancos falem entre si.",
        "pros": ["Supply 14.5M", "Foco Bancário", "ISO Ready"],
        "cons": ["Código Proprietário"],
        "link": "https://www.quant.network/",
        "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Sem LINK, a blockchain é cega. Essencial para precificar RWA em rede.",
        "pros": ["Padrão Global CCIP", "Universal", "Essencial"],
        "cons": ["Tokenomics"],
        "link": "https://chain.link/",
        "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Velocidade extrema para pagamentos em massa.",
        "pros": ["Taxas Baixas", "65k TPS", "Adoção Visa"],
        "cons": ["Uptime Histórico"],
        "link": "https://solana.com/",
        "img": "https://cryptologos.cc/logos/solana-sol-logo.png"
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Arquitetura IA",
        "why": "Infraestrutura para IA descentralizada. Modelos de IA soberanos.",
        "pros": ["Foco em IA", "Escalável", "User-Friendly"],
        "cons": ["Mercado Competitivo"],
        "link": "https://near.org/",
        "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Governada por Google e IBM. Livro-mestre para o setor corporativo.",
        "pros": ["Conselho de Elite", "Seguro", "Eficiente"],
        "cons": ["Perceção Centralizada"],
        "link": "https://hedera.com/",
        "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=30)
def get_crypto_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_radar_news():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    return news

# ==============================================================================
# 05. HERO SECTION
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Sovereign Financial Hub // Singularity</div>
    <div class="hero-title">A Próxima Geração da Infraestrutura de Capital.</div>
    <p class="hero-desc">Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
    Operamos na fronteira da norma ISO 20022 para garantir soberania absoluta.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (GRELHA DINÂMICA)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global")
full_grid = list(ASSET_VAULT.items()) + [
    ("GOLD", {"name": "Ouro", "ticker": "GC=F", "role": "Âncora"}),
    ("TSLA", {"name": "Tesla IA", "ticker": "TSLA", "role": "Autonomia"}),
    ("BCP", {"name": "BCP Liquidez", "ticker": "BCP.LS", "role": "Fiat"})
]

rows = [full_grid[i:i + 4] for i in range(0, len(full_grid), 4)]
for row in rows:
    cols = st.columns(4)
    for idx, (key, info) in enumerate(row):
        p, c = get_crypto_stats(info['ticker'])
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="q-card">
                <div style="color:#64748b; font-size:0.7rem; font-weight:800;">{info['name']} // {info['role']}</div>
                <div class="q-price">€ {p:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO
# ==============================================================================
c_news, c_vmax = st.columns([2, 1])

with c_news:
    st.markdown("### 📡 Radar de Fluxo Global")
    with st.container(height=500):
        news = fetch_radar_news()
        for n in news:
            st.markdown(f"**[{n['src']}]** [{n['title']}]({n['link']})")
            st.markdown("---")

with c_vmax:
    st.markdown("### 🧠 Córtex V.MAX")
    st.info("""
    **SENTIMENTO:** Acumulação Estratégica.
    **MACRO:** Inversão da curva indica fuga para ativos de escassez.
    **RWA:** BlackRock expande fundo BUIDL. Ondo lidera.
    **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica.
    """)
    st.success("**RECOMENDAÇÃO:** Acumular em tranches de 50%.")

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO (BLINDADO)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Recomendado")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Garantia de solvência."],
    ["Autonomia Física", "Tesla (TSLA)", "15%", "Domínio IA/Energia."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Reset Bancário."],
    ["Fronteira Digital", "BTC / NEAR / ETH", "15%", "Escassez Matemática."]
]

table_html = """
<table class="sovereign-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Nota</th></tr></thead>
    <tbody>
"""
for r in pos_data:
    table_html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. CÓDICE DE ATIVOS SOBERANOS (TABS + IMAGENS REAIS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        c_tx, c_img = st.columns([2, 1])
        with c_tx:
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            
            # Tabela de Vantagens
            v_html = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS</th><th>🔴 RISCOS</th></tr></thead>
                <tbody><tr>
                    <td><ul>{"".join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{"".join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(v_html, unsafe_allow_html=True)
            st.markdown(f"<br><a href='{info.get('link', '#')}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_img:
            # MOSTRAR IMAGEM REAL DO LOGO
            if "img" in info:
                st.image(info["img"], width=150)
            st.caption(f"Verificação de rede para {info['name']}")
            st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=400", caption="Arquitetura de Segurança")

st.divider()

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática."</em><br>
    <small>V43.0 // STABLE BUILD</small>
</div>
""", unsafe_allow_html=True)

if auto_refresh:
    time.sleep(30)
    st.rerun()
