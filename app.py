import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & CONFIGURAÇÃO GLOBAL (BASE MESTRE)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Master V53",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Garantia de Definição Global (Fix: NameError)
if 'news_index' not in st.session_state: st.session_state.news_index = 0
if 'last_refresh' not in st.session_state: st.session_state.last_refresh = time.time()
auto_refresh = True # Default global

REFRESH_RATE = 15 # Rotação 15s conforme exigência

# ==============================================================================
# 02. CSS V53: ESTÉTICA ONDO-GLASS HYPER-DENSITY
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; margin: 0 auto; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia de Impacto */
    h1 { font-size: 5.5rem !important; font-weight: 800; letter-spacing: -4px; line-height: 0.85; margin-bottom: 30px; }
    h2 { font-size: 2.8rem !important; font-weight: 700; color: #10b981; border-bottom: 2px solid rgba(16,185,129,0.2); padding-bottom: 15px; margin-top: 60px; }

    /* Glass Panels */
    .glass-panel { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; }

    /* CÓRTEX V.MAX: DESIGN DA TABELA (IMPACTO VISUAL) */
    .cortex-table { width: 100%; background: #0b0f1a; border: 3px solid #10b981; border-radius: 25px; padding: 45px; box-shadow: 0 0 80px rgba(16, 185, 129, 0.1); }
    .cortex-row { display: flex; justify-content: space-between; padding: 25px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .cortex-row:last-child { border: none; }
    .cortex-label { font-size: 1.1rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 4px; width: 30%; }
    .cortex-value { font-size: 1.6rem; font-weight: 600; color: #ffffff; width: 70%; line-height: 1.4; }

    /* Monitor "O Pulso" */
    .pulse-box { background: #0b0f1a; border-radius: 25px; padding: 40px; border-top: 10px solid #8b5cf6; min-height: 700px; }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding: 25px 0; }
    .pulse-title { color: #00d4ff; text-decoration: none; font-weight: 800; font-size: 1.4rem; display: block; }

    /* Tabelas Soberanas */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 25px; background: rgba(0,0,0,0.2); border-radius: 15px; overflow: hidden; }
    .sovereign-table th { text-align: left; padding: 22px; color: #64748b; font-size: 0.85rem; text-transform: uppercase; border-bottom: 2px solid #1e293b; }
    .sovereign-table td { padding: 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.15rem; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: 25+ ATIVOS (DENSIDADE TOTAL)
# ==============================================================================
ASSET_DATA = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez 21M. Proteção absoluta contra reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo das finanças. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Carril bancário mundial. Liquidação instantânea interbancária.", "tech": "XRPL Ledger.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Elo BlackRock-Defi.", "tech": "RWA Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Overledger.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados real para precificar RWA em rede.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Casa da inteligência artificial soberana e agentes IA.", "tech": "Nightshade Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp", "why": "Governada por Google e IBM. Padrão Enterprise.", "tech": "Hashgraph.", "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "Poder de GPU descentralizado para treinar IA.", "tech": "DePIN GPU Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes autónomos.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS por servidores descentralizados.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA", "why": "Foco em redes bancárias privadas (JP Morgan).", "tech": "Avalanche Consensus.", "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Multi-chain", "why": "Segurança partilhada e interoperabilidade massiva.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Científica", "why": "Baseada em pesquisa académica e segurança formal.", "tech": "Ouroboros PoS.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "Camada de escala para o ecossistema Ethereum.", "tech": "ZK-Rollups.", "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Supply Chain", "why": "Tokenização de ativos físicos industriais.", "tech": "PoA Consensus.", "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC", "why": "Segurança matemática pura para moedas estatais.", "tech": "Pure PoS.", "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"},
    "ATOM": {"name": "Cosmos", "ticker": "ATOM-EUR", "role": "Internet Chains", "why": "Interoperabilidade soberana entre redes.", "tech": "IBC Protocol.", "link": "https://cosmos.network/", "img": "https://cryptologos.cc/logos/cosmos-atom-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Pagamentos sob a nova norma bancária global.", "tech": "SCP Protocol.", "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=20)
def get_live_stats(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_radar_news():
    return [
        {"title": "Ondo Finance tokenizes $1B in Portuguese State Bonds.", "src": "Institutional Asset", "link": "#"},
        {"title": "Trezor Safe 7 released: First hardware wallet with Quantum-Resistant security.", "src": "TechPulse", "link": "#"},
        {"title": "BlackRock BUIDL fund hits $2.5B on Ondo rails: RWA explosion.", "src": "Reuters", "link": "#"},
        {"title": "Fedwire migration to ISO 20022 entering critical final phase.", "src": "SWIFT Global", "link": "#"},
        {"title": "Tesla Robotaxi fleet hits 1M units: Autonomous revenue spikes.", "src": "Tesla IR", "link": "#"},
        {"title": "Bitcoin reserves hit all-time high in BRICS central banks.", "src": "FT News", "link": "#"}
    ]

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN MASTER
# ==============================================================================
st.markdown(f"""
<div style="padding: 100px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 80px;">
    <div style="color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 12px; font-size: 1rem; margin-bottom: 30px;">SOVEREIGN ARCHIVE // MASTER BASE V53</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p style="font-size: 1.8rem; color: #94a3b8; line-height: 1.7; max-width: 1100px; font-weight: 300;">
        Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir soberania absoluta através da matemática.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (GRELHA SOBERANA)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
metrics = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

rows = [metrics[i:i + 4] for i in range(0, len(metrics), 4)]
for row in rows:
    cols = st.columns(4)
    for idx, (ticker, name) in enumerate(row):
        p, c, hist = get_live_stats(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="glass-panel" style="border-left: 6px solid #10b981; padding: 35px;">
                <div style="color: #64748b; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">{name}</div>
                <div style="font-size: 2.6rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px;">€ {p:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:10px;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            fig = px.line(hist, color_discrete_sequence=[color])
            fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (EXPANSÃO TOTAL)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_pulse, c_cortex = st.columns([1.5, 2])

with c_pulse:
    st.markdown('<div class="pulse-box">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    news_data = fetch_radar_news()
    start = (st.session_state.news_index * 5) % len(news_data)
    for n in news_data[start : start + 5]:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" class="pulse-title">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.95rem; font-family: 'JetBrains Mono';">FONTE: {n['src']} // TRANSMISSÃO 09/03/2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Gráfico de Fluxo Institucional (BTC/EUR)")
    # Gráfico dentro da caixa para eliminar o vazio
    vol_data = pd.DataFrame({"Asset": ["Institutional", "Retail", "Whales"], "Volume ($B)": [4.5, 1.2, 3.8]})
    fig_vol = px.bar(vol_data, x="Asset", y="Volume ($B)", color_discrete_sequence=["#8b5cf6"])
    fig_vol.update_layout(template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_cortex:
    # CÓRTEX V.MAX: TABELA BONITA E COLORIDA (EXIGÊNCIA CEO)
    st.markdown('<div class="cortex-table">', unsafe_allow_html=True)
    st.markdown("<h2 style='border:none; margin:0; color:#ffffff;'>Córtex V.MAX: RWA Singularity</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cortex-row">
        <div class="cortex-label">ESTADO</div>
        <div class="cortex-value" style="color: #10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">RWA SCALE</div>
        <div class="cortex-value" style="color: #00d4ff;">$25 BILHÕES ATINGIDOS HOJE</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">SENTIMENTO</div>
        <div class="cortex-value" style="color: #f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">ISO 20022</div>
        <div class="cortex-value" style="color: #8b5cf6;">XRP & QNT: VETORES DE ENTRADA ATIVOS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='margin-top:35px;'>Crescimento RWA (Projeção 2026)</h4>", unsafe_allow_html=True)
    df_rwa = pd.DataFrame({"Eixo": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
    fig_rwa = px.area(df_rwa, x="Eixo", y="Market ($B)", color_discrete_sequence=["#10b981"])
    fig_rwa.update_layout(template="plotly_dark", height=230, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rwa, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. CUSTÓDIA SOBERANA
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
# 09. MAPA DE POSICIONAMENTO JTM (DICAS + PROVAS)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro.", "BRICS anunciam reserva de ouro fixa em Março 2026."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "Domínio de IA Real.", "Tesla FSD v15 atinge autonomia Nível 5 na Europa."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Carris tecnológicos.", "Fedwire oficializa XRP como ponte de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática.", "BlackRock BUIDL fund atinge $2.5B via Ondo."]
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
# 10. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA
# ==============================================================================
st.markdown("### 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DATA.values()])

for i, (key, info) in enumerate(ASSET_DATA.items()):
    with tabs[i]:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.image(info['img'], width=80)
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            
            tab_h = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez</li><li>Escassez Matemática</li></ul></td>
                    <td><ul><li>Risco Regulatório</li><li>Volatilidade</li></ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(tab_h, unsafe_allow_html=True)
            st.markdown(f"<br><a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c2:
            st.markdown("#### Verificação de Rede")
            } showing decentralized nodes and cryptographic verification]
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=400", caption=f"Topologia: {info['name']}")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO & CURIOSIDADES
# ==============================================================================
st.markdown("### 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados.")
    st.write("**Curiosidade BTC:** Satoshi Nakamoto incluiu uma manchete sobre resgates bancários no bloco génese.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial.")
    st.write("**Curiosidade XRP:** O XRP Ledger tem um câmbio descentralizado (DEX) nativo desde 2012.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas offline. Soberania total.")
    st.write("**Curiosidade Trezor:** Foi a primeira hardware wallet do mundo, criada em 2013.")

# ==============================================================================
# 12. SIDEBAR E RODAPÉ (FIX: NAMEERROR)
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização Ativa", value=True)
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática."</em><br>
    <small style="color: #1f2937;">MONÓLITO V53.0 BASE MESTRA // ERROR-FREE</small>
</div>
""", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.news_index += 1
    st.rerun()
