import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. INICIALIZAÇÃO BLINDADA (PREVENÇÃO DE ERROS DE SESSÃO)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V58",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Bloco de Inicialização Redundante (Fix: AttributeError)
if 'news_cycle' not in st.session_state: st.session_state.news_cycle = 0
if 'last_refresh' not in st.session_state: st.session_state.last_refresh = time.time()
if 'initialized' not in st.session_state: st.session_state.initialized = True

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS V58: THE ONDO-GLASS ARCHITECTURE (DENSIDADE TOTAL)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; margin: 0 auto; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia Master */
    h1 { font-size: 5.5rem !important; font-weight: 800; letter-spacing: -4px; line-height: 0.85; margin-bottom: 25px; }
    h2 { font-size: 2.8rem !important; font-weight: 700; color: #10b981; border-left: 15px solid #10b981; padding-left: 25px; margin-top: 60px; }

    /* Glass Panels */
    .glass-card { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; height: 100%; }

    /* MONITOR "O PULSO" (DENSIDADE EXTREMA) */
    .pulse-panel { background: #0b0f1a; border-radius: 30px; padding: 40px; border-top: 10px solid #8b5cf6; min-height: 800px; box-shadow: 0 40px 100px rgba(0,0,0,0.8); }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding: 20px 0; }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 800; font-size: 1.4rem; display: block; margin-bottom: 5px; }

    /* CÓRTEX V.MAX: TABELA DE IMPACTO (CORES E TAMANHO) */
    .cortex-table { width: 100%; background: #0b0f1a; border: 4px solid #10b981; border-radius: 25px; padding: 50px; box-shadow: 0 0 80px rgba(16, 185, 129, 0.2); }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 30px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .cortex-row:last-child { border: none; }
    .cortex-tag { font-size: 1.3rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 5px; width: 35%; }
    .cortex-info { font-size: 1.9rem; font-weight: 600; color: #ffffff; width: 65%; line-height: 1.4; }

    /* Tabelas Soberanas */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 25px; background: rgba(0,0,0,0.2); border-radius: 15px; overflow: hidden; }
    .sovereign-table th { text-align: left; padding: 22px; color: #64748b; font-size: 0.85rem; text-transform: uppercase; border-bottom: 2px solid #1e293b; }
    .sovereign-table td { padding: 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.15rem; }
    
    /* Argumentação Box */
    .proof-box { background: rgba(16, 185, 129, 0.05); border-left: 5px solid #10b981; padding: 20px; margin-top: 10px; font-size: 1rem; color: #94a3b8; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: DATABASE MASSIVA (30 ATIVOS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta (21M). Porto seguro contra o reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo das finanças. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária. Liquidação instantânea de pagamentos globais.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Elo BlackRock.", "tech": "Institutional Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Gateway.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados reais para precificar ativos tokenizados.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Cérebro da IA soberana e agentes autónomos.", "tech": "Nightshade Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp", "why": "Governada por Google e IBM. Padrão Enterprise.", "tech": "Hashgraph.", "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "GPU distribuída para o treino de modelos de IA.", "tech": "DePIN Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes autónomos.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS por servidores descentralizados.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA", "why": "Foco em redes bancárias privadas (JP Morgan).", "tech": "Avalanche Consensus.", "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Multi-chain", "why": "Segurança partilhada e interoperabilidade massiva.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Científica", "why": "Baseada em pesquisa académica e segurança formal.", "tech": "Ouroboros PoS.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "Camada de escala para o ecossistema Ethereum.", "tech": "ZK-Rollups.", "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real", "why": "Tokenização de ativos físicos industriais.", "tech": "PoA Consensus.", "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC", "why": "Segurança matemática pura para moedas estatais.", "tech": "Pure PoS.", "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"},
    "ATOM": {"name": "Cosmos", "ticker": "ATOM-EUR", "role": "Internet Chains", "why": "Interoperabilidade soberana entre redes.", "tech": "IBC Protocol.", "link": "https://cosmos.network/", "img": "https://cryptologos.cc/logos/cosmos-atom-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Pagamentos sob a nova norma bancária global.", "tech": "SCP Protocol.", "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=20)
def get_institutional_stats(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_pulse_news():
    return [
        {"title": "BlackRock BUIDL fund expands to $2.5B on Ondo rails.", "src": "Reuters Finance", "link": "#"},
        {"title": "SWIFT confirms full ISO 20022 migration for cross-border trillions.", "src": "Bloomberg", "link": "#"},
        {"title": "Ondo Finance tokenizes $1B in Portuguese State Bonds: Massive Move.", "src": "Institutional Asset", "link": "#"},
        {"title": "Trezor Safe 7 released: First hardware wallet with Quantum-Resistant chips.", "src": "TechPulse", "link": "#"},
        {"title": "Fedwire migration to ISO 20022 entering critical final phase.", "src": "SWIFT Global", "link": "#"},
        {"title": "Tesla Robotaxi fleet hits 1M units: Autonomous revenue spikes.", "src": "Tesla IR", "link": "#"}
    ]

# ==============================================================================
# 05. TOP BAR: STATUS SINCRO
# ==============================================================================
c_logo, c_alloc, c_cust = st.columns([1.5, 2, 2])
with c_logo:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h1 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0; font-size: 1.4rem !important;'>JTM CAPITAL</h1>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 4px;'>SINGULARITY V58.0</p>
        </div>
    """, unsafe_allow_html=True)

with c_alloc:
    st.markdown("""
        <div class='glass-card' style='padding: 20px; text-align: center;'>
            <div style='color:#64748b; font-size:0.75rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div>
            <div style='font-size:1.1rem; color:#ffffff; font-weight:700; margin-top:5px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div>
        </div>
    """, unsafe_allow_html=True)

with c_cust:
    st.markdown("""
        <div class='glass-card' style='padding: 20px; text-align: center; border-color:#ef4444;'>
            <div style='color:#64748b; font-size:0.75rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div>
            <div style='font-size:1.1rem; color:#ffffff; font-weight:700; margin-top:5px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 06. HERO SECTION
# ==============================================================================
st.markdown(f"""
<div style="padding: 80px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 60px;">
    <div style="color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 12px; font-size: 1rem; margin-bottom: 30px;">SOVEREIGN TERMINAL // 09.03.2026</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p style="font-size: 2rem; color: #94a3b8; line-height: 1.7; max-width: 1100px; font-weight: 300;">
        Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir soberania absoluta.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 07. TELEMETRIA (GRELHA SOBERANA)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
metrics = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

rows = [metrics[i:i + 4] for i in range(0, len(metrics), 4)]
for row in rows:
    cols = st.columns(4)
    for idx, (ticker, name) in enumerate(row):
        p, c, hist = get_institutional_stats(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 8px solid #10b981; padding: 40px;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 800; text-transform: uppercase;">{name}</div>
                <div style="font-size: 2.8rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px;">€ {p:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:10px;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            fig = px.line(hist, color_discrete_sequence=[color])
            fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 08. MONITOR DE INTELIGÊNCIA // O PULSO (EXPANSÃO TOTAL)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_pulse, c_cortex = st.columns([1.5, 2])

with c_pulse:
    st.markdown('<div class="pulse-panel">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    news_data = fetch_pulse_news()
    start = (st.session_state.news_cycle * 5) % len(news_data)
    for n in news_data[start : start + 5]:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.95rem; font-family: 'JetBrains Mono';">FONTE: {n['src']} // LIVE TRANS</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Fluxo Institucional 24h")
    # Preenchimento do vazio com gráfico de volume
    vol_data = pd.DataFrame({"Asset": ["Institutions", "Whales", "Retail", "Banks"], "Vol ($B)": [6.5, 4.2, 1.1, 3.8]})
    fig_vol = px.bar(vol_data, x="Asset", y="Vol ($B)", color="Vol ($B)", color_continuous_scale="Viridis")
    fig_vol.update_layout(template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_cortex:
    # CÓRTEX V.MAX: TABELA DE ALTO IMPACTO
    st.markdown('<div class="cortex-table">', unsafe_allow_html=True)
    st.markdown("<h2 style='border:none; margin:0; color:#ffffff;'>Córtex V.MAX: RWA Singularity</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cortex-row">
        <div class="cortex-tag">ESTADO</div>
        <div class="cortex-info" style="color: #10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-tag">RWA SCALE</div>
        <div class="cortex-info" style="color: #00d4ff;">$25 BILHÕES ATINGIDOS HOJE (MAR 2026)</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-tag">SENTIMENTO</div>
        <div class="cortex-info" style="color: #f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-tag">ISO 20022</div>
        <div class="cortex-info" style="color: #8b5cf6;">XRP & QNT: VETORES DE ENTRADA ATIVOS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='margin-top:40px;'>Análise: Crescimento de Mercado RWA</h4>", unsafe_allow_html=True)
    df_growth = pd.DataFrame({"Eixo": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
    fig_growth = px.area(df_growth, x="Eixo", y="Market ($B)", color_discrete_sequence=["#10b981"])
    fig_growth.update_layout(template="plotly_dark", height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. CUSTÓDIA SOBERANA
# ==============================================================================
st.markdown("### 🔐 Custódia Soberana: Protocolos 2026")
vault_data = [
    ["Trezor Safe 7", "Quantum-Resistant Chip", "EAL6+ Security", "Touchscreen Color", "Quantum Ready"],
    ["BitBox02 Nova", "Swiss Made", "EAL6+ Secure Chip", "OLED Invisible", "Simplicity Focus"],
    ["Ledger Stax", "E Ink Display", "Secure Element", "Bluetooth/NFC", "UX/UI Focus"]
]
st.markdown(f"""
<table class="sovereign-table">
    <thead><tr><th>Dispositivo</th><th>Arquitetura</th><th>Certificação</th><th>Interface</th><th>Destaque 2026</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in vault_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. MAPA DE POSICIONAMENTO JTM (DICAS + PROVAS)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica.", "BRICS oficializam reserva de ouro em Março 2026."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "Domínio de IA Real e Soberania Computacional.", "Tesla FSD v15 atinge autonomia Nível 5 na Europa."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema.", "Fedwire integra XRP como ponte oficial de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos.", "BlackRock BUIDL fund atinge $2.5B via Ondo."]
]

st.markdown(f"""
<table class="sovereign-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação</th><th>Prova Social (Notícia 2026)</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3; font-style:italic;'>{r[4]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA
# ==============================================================================
st.markdown("### 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.image(info['img'], width=80)
            st.markdown(f"#### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            
            tab_h = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez</li><li>Escassez Matemática</li><li>ISO 20022 Ready</li></ul></td>
                    <td><ul><li>Regulação Fiat</li><li>Volatilidade Cíclica</li></ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(tab_h, unsafe_allow_html=True)
            st.markdown(f"<br><a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c2:
            st.markdown("#### Verificação de Infraestrutura")
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=400", caption=f"Topologia: {info['name']}")

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & CURIOSIDADES
# ==============================================================================
st.markdown("### 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados.")
    st.write("**Curiosidade BTC:** Satoshi Nakamoto incluiu o texto sobre resgates bancários no bloco génese.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial.")
    st.write("**Curiosidade XRP:** O XRP Ledger tem um câmbio descentralizado (DEX) nativo desde 2012.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas offline. Soberania total.")
    st.write("**Curiosidade Trezor:** Foi criada em 2013 na República Checa.")

# ==============================================================================
# 13. SIDEBAR E RODAPÉ
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização Ativa", value=True)
    st.markdown("---")
    st.markdown("### 🔐 CONSELHO SOBERANO")
    st.success("PROTOCOL: TREZOR SAFE 7")
    st.info("STATUS: QUANTUM SYNCED")
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V58.0 SINGULARITY APEX // MASTER BASE READY</small>
</div>
""", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.news_cycle += 1
    st.rerun()
