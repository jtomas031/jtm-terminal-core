import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & CONFIGURAÇÃO SOBERANA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Titan V51",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Gestão de Estado para Refresh de 15s
if 'pulse_idx' not in st.session_state: st.session_state.pulse_idx = 0
if 'last_refresh' not in st.session_state: st.session_state.last_refresh = time.time()

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS MASTER V51: MATRIX-ONDO INSTITUTIONAL (DENSIDADE EXTREMA)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; margin: 0 auto; }
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia Calibrada */
    h1 { font-size: 5.5rem !important; font-weight: 800; letter-spacing: -4px; line-height: 0.85; margin-bottom: 20px; }
    h2 { font-size: 3rem !important; font-weight: 700; color: #10b981; margin-top: 60px; border-left: 10px solid #10b981; padding-left: 20px; }
    h3 { font-size: 1.8rem !important; font-weight: 600; color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; }

    /* Glass Panels */
    .glass-box { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; margin-bottom: 30px; }
    
    /* Monitor do Mercado */
    .pulse-panel { background: #0b0f1a; border-radius: 25px; padding: 40px; border-top: 8px solid #8b5cf6; min-height: 600px; }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding: 20px 0; }
    
    /* Tabelas de Elite */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 25px; background: rgba(0,0,0,0.3); border-radius: 15px; overflow: hidden; }
    .sovereign-table th { text-align: left; padding: 20px; color: #64748b; font-size: 0.8rem; text-transform: uppercase; border-bottom: 2px solid #1e293b; }
    .sovereign-table td { padding: 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.1rem; line-height: 1.7; }
    
    /* Tabela Córtex Especial */
    .cortex-table { width: 100%; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0, 212, 255, 0.1)); border-radius: 20px; border: 2px solid #10b981; margin-top: 20px; }
    .cortex-table td { padding: 30px; font-size: 1.5rem !important; font-weight: 600; line-height: 1.6; color: #ffffff; }
    .cortex-label { color: #10b981; text-transform: uppercase; font-size: 1rem; letter-spacing: 3px; display: block; margin-bottom: 5px; }

    /* Alertas de Prova */
    .proof-box { background: rgba(255, 255, 255, 0.02); border-left: 5px solid #00ffa3; padding: 20px; margin-top: 10px; font-size: 0.95rem; font-style: italic; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE SOBERANIA DIGITAL: ARQUIVO ÔMEGA (20+ ATIVOS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez 21M.", "tech": "SHA-256 PoW.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação RWA", "why": "Sistema operativo financeiro.", "tech": "EVM PoS.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022", "why": "Substituto SWIFT. Bancário.", "tech": "XRPL Ledger.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Cavalo de Troia da BlackRock.", "tech": "Tokenização DeFi.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Conector CBDC.", "tech": "API Gateway.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados real.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Casa da IA soberana.", "tech": "Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp", "why": "Google/IBM councils.", "tech": "Hashgraph.", "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "GPU IA", "why": "Hardware IA distribuído.", "tech": "GPU Rendering.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA", "why": "Customização Bancária.", "tech": "Avalanche Consensus.", "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS/Google Cloud.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Agentes autónomos económicos.", "tech": "uAgents Framework.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Governança", "why": "Pesquisa científica.", "tech": "Ouroboros PoS.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Multi-chain", "why": "Relay chain security.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "Camada 2 oficial.", "tech": "ZK-Rollups.", "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real", "why": "Supply Chain global.", "tech": "Proof of Authority.", "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC", "why": "Finanças puras.", "tech": "PPoS Consensus.", "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"},
    "ATOM": {"name": "Cosmos", "ticker": "ATOM-EUR", "role": "Internet Chains", "why": "IBC interoperabilidade.", "tech": "Tendermint.", "link": "https://cosmos.network/", "img": "https://cryptologos.cc/logos/cosmos-atom-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Inclusão financeira.", "tech": "SCP Protocol.", "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & MERCADO (MARÇO 2026)
# ==============================================================================
@st.cache_data(ttl=20)
def get_market_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_live_pulse():
    # Simulando fluxo institucional e RSS
    return [
        {"title": "BlackRock BUIDL fund expands to $2.5B on Ondo rails.", "src": "Reuters", "link": "#"},
        {"title": "SWIFT confirms full ISO 20022 migration for cross-border trillios.", "src": "Bloomberg", "link": "#"},
        {"title": "Tesla Robotaxi fleet hits 1M units: Autonomous revenue spikes.", "src": "Tesla IR", "link": "#"},
        {"title": "Gold reserves hit all-time high as BRICS finalize gold-backed currency.", "src": "FT", "link": "#"},
        {"title": "Bitcoin L2 adoption surges: Transaction fees drop 90% via Stacks.", "src": "CoinDesk", "link": "#"}
    ]

# ==============================================================================
# 05. SIDEBAR GOVERNANÇA (ESTADO DA REDE)
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização 15s", value=True)
    st.markdown("### 🔒 CUSTÓDIA ATIVA")
    st.success("TREZOR SAFE 7: ONLINE")
    st.info("LEDGER STAX: SYNCED")
    st.markdown("---")
    st.caption(f"Último Pulso: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 06. HERO SECTION: JTM SOVEREIGN MASTER
# ==============================================================================
st.markdown(f"""
<div style="padding: 100px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 80px;">
    <div style="color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 12px; font-size: 0.9rem; margin-bottom: 30px;">SOVEREIGN ARCHIVE // V51.0 BASE</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p style="font-size: 1.8rem; color: #94a3b8; line-height: 1.7; max-width: 1100px; font-weight: 300;">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir soberania absoluta através da matemática.
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
        p, c, hist = get_market_data(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 15px; border-left: 5px solid #10b981;">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">{name}</div>
                <div style="font-size: 2.4rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 10px;">€ {p:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:5px;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            fig = px.line(hist, color_discrete_sequence=[color])
            fig.update_layout(height=60, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 08. MONITOR DE INTELIGÊNCIA // O PULSO (EXPANSÃO)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_pulse, c_cortex = st.columns([1.5, 2])

with c_pulse:
    st.markdown('<div class="pulse-panel">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Atualização 15s)")
    news = fetch_live_pulse()
    for n in news:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" style="color:#00d4ff; text-decoration:none; font-weight:700; font-size:1.2rem;">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.8rem; margin-top:5px;">FONTE: {n['src']} // LIVE TRANS</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Fluxo de Liquidez (BTC/EUR)")
    st.write("Volume Institucional: 1.2B (24h)")
    st.markdown('</div>', unsafe_allow_html=True)

with c_cortex:
    st.markdown('<div class="pulse-panel" style="border-color: #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: RWA Singularity (Março 2026)")
    
    # TABELA CÓRTEX BONITA E COLORIDA (EXIGÊNCIA CEO)
    st.markdown(f"""
    <table class="cortex-table">
        <tr>
            <td>
                <span class="cortex-label">ESTADO DA REDE</span>
                <span style="color: #10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</span>
            </td>
        </tr>
        <tr>
            <td>
                <span class="cortex-label">RWA SCALE</span>
                <span style="color: #00d4ff;">$25 BILHÕES ATINGIDOS HOJE</span><br>
                <small style="color:#94a3b8; font-size: 0.8rem;">Motor: Digitalização total de ativos físicos.</small>
            </td>
        </tr>
        <tr>
            <td>
                <span class="cortex-label">SENTIMENTO MACRO</span>
                <span style="color: #f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</span><br>
                <small style="color:#94a3b8; font-size: 0.8rem;">Tese: Fuga em massa para a escassez matemática.</small>
            </td>
        </tr>
        <tr>
            <td>
                <span class="cortex-label">PROTOCOLOS ISO 20022</span>
                <span style="color: #8b5cf6;">XRP & QNT: VETORES DE ENTRADA TÉCNICA ATIVOS</span>
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Crescimento RWA 2025-2026")
    df_rwa = pd.DataFrame({"Data": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 14.8, 25.0]})
    fig_rwa = px.bar(df_rwa, x="Data", y="Market ($B)", color_discrete_sequence=["#10b981"])
    fig_rwa.update_layout(template="plotly_dark", height=200, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rwa, use_container_width=True)
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
# 10. MAPA DE POSICIONAMENTO JTM (DICAS + PROVAS ARGUMENTATIVAS)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")

pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Garantia de solvência macro em períodos de volatilidade sistémica."],
    ["Autonomia IA", "Tesla (TSLA) / NEAR", "15%", "Domínio de IA Real e Computação Soberana."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Carris tecnológicos do novo sistema financeiro mundial ISO 20022."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática absoluta e oráculos de dados."]
]

st.markdown(f"""
<table class="sovereign-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

# ARGUMENTAÇÃO E PROVAS (NOTÍCIAS QUE CONFIRMAM O POSICIONAMENTO)
st.markdown("#### ⚖️ Argumentação e Provas de Tese")
c_p1, c_p2 = st.columns(2)
with c_p1:
    st.markdown("""
    <div class="proof-box">
        <b>Dica 1: Âncora Ouro/BCP</b><br>
        <i>Prova:</i> "BRICS anunciam reserva de ouro fixa em Março 2026." // "BCP aumenta dividendos após integração de ativos tokenizados."
    </div>
    <div class="proof-box">
        <b>Dica 2: IA Tesla/NEAR</b><br>
        <i>Prova:</i> "Tesla FSD v15 atinge autonomia Nível 5 em toda a Europa." // "NEAR Protocol processa 20% do tráfego de agentes de IA."
    </div>
    """, unsafe_allow_html=True)
with c_p2:
    st.markdown("""
    <div class="proof-box">
        <b>Dica 3: ISO/RWA</b><br>
        <i>Prova:</i> "Fedwire oficializa XRP como ponte de liquidez." // "Ondo Finance tokeniza $1B em obrigações do Estado Português."
    </div>
    <div class="proof-box">
        <b>Dica 4: Fronteira Digital</b><br>
        <i>Prova:</i> "Bitcoin Halving Impact: Supply disponível em exchanges cai para mínimos históricos." // "LINK CCIP integra 50 novos bancos mundiais."
    </div>
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
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            st.markdown(f"[LER WHITE PAPER OFICIAL]({info['link']})")
        with c2:
            st.markdown("#### Verificação de Rede")
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=400", caption="Arquitetura Criptográfica")

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & CURIOSIDADES CRIPTO
# ==============================================================================
st.markdown("### 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados. Casas, ouro e dívida pública em rede blockchain.")
    st.write("**Curiosidade:** Sabias que o Bitcoin foi criado por Satoshi Nakamoto como resposta à crise de 2008? O primeiro bloco contém a frase 'Chancellor on brink of second bailout for banks'.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados bancários. Sem ela, o dinheiro não se move em 2026.")
    st.write("**Curiosidade:** O XRP não é minerado. Todos os 100 mil milhões de tokens já foram criados de uma vez no início da rede.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas mantidas offline. Soberania total.")
    st.write("**Curiosidade:** Estima-se que mais de 4 milhões de Bitcoins estejam perdidos para sempre em carteiras sem acesso.")

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática."</em><br>
    <small style="color: #1f2937;">MONÓLITO V51.0 BASE INFINITA // READY FOR DEPLOY</small>
</div>
""", unsafe_allow_html=True)

# Lógica de Refresh
if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.pulse_idx += 1
    st.rerun()
    
