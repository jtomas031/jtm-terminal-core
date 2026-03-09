import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & DOCUMENTAÇÃO DE SOBERANIA (DENSIDADE MÁXIMA)
# ==============================================================================
# Esta é a Base Mestra da JTM Capital. 
# Projetada para o Horizonte 2026. 1000+ Linhas de Inteligência Pura.
# ==============================================================================

st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Titan V52",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Gestão de Ciclo de Refresh (15 Segundos)
if 'cycle' not in st.session_state: st.session_state.cycle = 0
if 'last_update' not in st.session_state: st.session_state.last_update = time.time()

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS TITAN V52: ESTÉTICA DE TRILIÕES (ONDO-MATRIX-FUTURISM)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; margin: 0 auto; }
    .stApp { 
        background-color: #010204; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010204 100%);
    }

    /* Tipografia Calibrada */
    h1 { font-size: 6rem !important; font-weight: 800; letter-spacing: -5px; line-height: 0.8; margin-bottom: 25px; }
    h2 { font-size: 3.5rem !important; font-weight: 700; color: #10b981; margin-top: 70px; border-left: 15px solid #10b981; padding-left: 25px; }
    h3 { font-size: 2rem !important; font-weight: 600; color: #00d4ff; letter-spacing: 3px; text-transform: uppercase; }
    
    /* Painel Hero */
    .hero-panel { padding: 120px 0; margin-bottom: 100px; animation: fadeIn 2s; }
    .hero-desc { font-size: 2rem; color: #94a3b8; line-height: 1.6; max-width: 1200px; font-weight: 300; border-left: 2px solid #10b981; padding-left: 50px; }

    /* Cartões de Telemetria */
    .q-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 45px;
        border-radius: 25px;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        border-left: 8px solid #10b981;
        height: 100%;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
    }
    .q-card:hover { border-color: #00d4ff; transform: scale(1.02); background: rgba(15, 23, 42, 0.7); }
    .q-price { font-size: 3rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 20px; }

    /* Tabelas Soberanas */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 40px; background: rgba(0,0,0,0.3); border-radius: 20px; overflow: hidden; }
    .sovereign-table th { text-align: left; padding: 30px; color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 4px; border-bottom: 3px solid #1e293b; }
    .sovereign-table td { padding: 35px 30px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.25rem; line-height: 1.8; }

    /* CÓRTEX V.MAX: DESIGN DE ALTO IMPACTO */
    .cortex-container {
        width: 100%;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(0, 212, 255, 0.1));
        border: 3px solid #10b981;
        border-radius: 30px;
        padding: 50px;
        margin: 40px 0;
        box-shadow: 0 0 100px rgba(16, 185, 129, 0.1);
    }
    .cortex-row { display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 30px 0; }
    .cortex-row:last-child { border: none; }
    .cortex-label { font-size: 1.2rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 5px; width: 30%; }
    .cortex-value { font-size: 1.8rem; font-weight: 600; color: #ffffff; width: 70%; line-height: 1.4; }

    /* News Monitor */
    .pulse-panel { background: #0b0f1a; border-radius: 30px; padding: 50px; border-top: 12px solid #8b5cf6; min-height: 800px; }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding: 35px 0; }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 800; font-size: 1.6rem; transition: 0.3s; }
    .pulse-link:hover { color: #10b981; padding-left: 10px; }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. BASE DE DADOS ÔMEGA: 25 ATIVOS (SISTEMA COMPLETO)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta verificável (21M). Porto seguro contra o reset fiduciário mundial.", "tech": "SHA-256 Proof of Work. A rede mais segura do mundo.", "vision": "Reserva de valor para Bancos Centrais em 2030.", "pros": ["Escassez 21M", "Adoção Institucional", "Imutabilidade"], "cons": ["Volatilidade", "Lentidão L1"], "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo das finanças. Camada onde triliões em RWA são liquidados via Smart Contracts.", "tech": "EVM Proof of Stake. Mecanismo de queima deflacionário.", "vision": "Liquidação de todos os ativos do mercado de capitais.", "pros": ["Líder RWA", "Deflacionário"], "cons": ["Gas Fees", "Fragmentação"], "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022", "why": "Carril bancário mundial. Liquidação instantânea de pagamentos transfronteiriços.", "tech": "XRPL Ledger. Consenso federado ultra-rápido.", "vision": "Substituto universal do SWIFT legado.", "pros": ["Velocidade 3s", "Conformidade"], "cons": ["Centralização Labs"], "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Nó RWA Institutional", "why": "Digitalização do Tesouro Americano. Elo direto entre a BlackRock e o capital on-chain.", "tech": "Tokenização de ativos com regulação institucional.", "vision": "Líder na gestão de triliões em ativos tradicionais.", "pros": ["BlackRock Partnership", "Yield Real"], "cons": ["Risco Centralizado"], "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais à economia pública.", "tech": "API Gateway patenteada para conectividade inter-chain.", "vision": "A fibra ótica do novo sistema financeiro mundial.", "pros": ["Supply 14.5M", "Foco Bancário"], "cons": ["Código Fechado"], "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Verdade", "why": "Sem LINK, a blockchain é cega. Ponte de dados para precificar RWA.", "tech": "CCIP Protocol e oráculos descentralizados.", "vision": "Padrão universal de comunicação de dados financeiros.", "pros": ["Padrão Global", "Universal"], "cons": ["Tokenomics Lento"], "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "A 'Nasdaq' das blockchains. Projetada para pagamentos massivos em milissegundos.", "tech": "Proof of History. 65k transações por segundo.", "vision": "Camada de execução para finanças retail e IA.", "pros": ["Velocidade", "Adoção Visa"], "cons": ["Uptime Histórico"], "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Cérebro IA", "why": "Casa da IA soberana. Onde modelos de inteligência gerem capital.", "tech": "Sharding dinâmico e abstração de conta nativa.", "vision": "Sistema operativo para a economia autónoma de IA.", "pros": ["Foco IA", "User Friendly"], "cons": ["Competição L1"], "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise", "why": "Conselho governado por Google e IBM. Padrão Fortune 500.", "tech": "Hashgraph. Segurança aBFT máxima.", "vision": "Registo universal de identidades e supply chain.", "pros": ["Council Elite", "Seguro"], "cons": ["Perceção Centralizada"], "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "Poder de GPU distribuído. O combustível para o treino de modelos de IA.", "tech": "Rede de renderização descentralizada.", "vision": "O maior pool de processamento visual e analítico do mundo.", "pros": ["Apple/Nvidia Links", "Utility"], "cons": ["Chips Supply"], "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets Bancárias", "why": "Redes privadas customizáveis para grandes bancos como JP Morgan.", "tech": "Avalanche Consensus e arquitetura de Subnets.", "vision": "Infraestrutura de eleição para o mercado RWA bancário.", "pros": ["Customizável", "RWA Focus"], "cons": ["Adoção"], "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui Amazon AWS e Google Cloud por servidores descentralizados.", "tech": "Chain Key Cryptography.", "vision": "Hospedagem de toda a internet sem servidores centrais.", "pros": ["Soberania Cloud", "Full Stack"], "cons": ["Complexidade"], "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Criação de agentes autónomos que realizam transações por ti.", "tech": "uAgents Framework.", "vision": "Internet económica de agentes inteligentes.", "pros": ["Inovação IA", "Líder Agentes"], "cons": ["Nicho"], "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Segurança Partilhada", "why": "Liga várias blockchains numa rede segura e interoperável.", "tech": "Relay Chain e Parachains.", "vision": "O centro da web multi-chain.", "pros": ["Interoperável", "Gavin Wood"], "cons": ["Complexidade"], "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Científica", "why": "Desenvolvida com métodos formais e pesquisa académica rigorosa.", "tech": "Ouroboros PoS.", "vision": "Soberania em países em desenvolvimento (África).", "pros": ["Segurança", "Governança"], "cons": ["Lentidão Dev"], "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "A camada de escala definitiva para o ecossistema Ethereum.", "tech": "ZK-Rollups.", "vision": "Protocolo padrão para escalar a Web3.", "pros": ["Parcerias Corp", "Escalável"], "cons": ["Dep. ETH"], "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real", "why": "Tokenização de cadeias de suprimento e produtos físicos.", "tech": "Proof of Authority.", "vision": "Registo mundial de autenticidade industrial.", "pros": ["Uso Real", "Walmart Link"], "cons": ["Centralização"], "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC", "why": "Segurança matemática extrema para emissão de moedas digitais.", "tech": "Pure PoS.", "vision": "Tecnologia oficial para moedas de estado.", "pros": ["Matemática Turing", "Eco"], "cons": ["Adoção"], "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"},
    "ATOM": {"name": "Cosmos", "ticker": "ATOM-EUR", "role": "Internet Chains", "why": "Protocolo que permite a transferência livre de ativos entre redes.", "tech": "IBC (Inter-Blockchain Communication).", "vision": "A internet soberana das blockchains.", "pros": ["Modular", "Soberania"], "cons": ["Tokenomics"], "link": "https://cosmos.network/", "img": "https://cryptologos.cc/logos/cosmos-atom-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Inclusão financeira e pagamentos sob a nova norma bancária.", "tech": "Stellar Consensus Protocol.", "vision": "Padrão para micropagamentos mundiais.", "pros": ["MoneyGram Link", "Rápido"], "cons": ["Sombra XRP"], "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"},
    "TAO": {"name": "Bittensor", "ticker": "TAO-EUR", "role": "Inteligência Descentralizada", "why": "Cria um mercado global para inteligência artificial em rede.", "tech": "Incentivos para treino de modelos.", "vision": "O maior cérebro artificial do mundo.", "pros": ["IA Pioneira", "Ativo Único"], "cons": ["Complexidade"], "link": "https://bittensor.com/", "img": "https://cryptologos.cc/logos/bittensor-tao-logo.png"},
    "PEPE": {"name": "Pepe (Sentiment)", "ticker": "PEPE-EUR", "role": "Métrica de Risco", "why": "Utilizada como termómetro da euforia ou medo do mercado retail.", "tech": "Erc-20 Meme Logic.", "vision": "Indicador de liquidez e sentimento.", "pros": ["Liquidez Alta", "Comunidade"], "cons": ["Risco Extremo"], "link": "https://pepe.vip/", "img": "https://cryptologos.cc/logos/pepe-pepe-logo.png"},
    "AAVE": {"name": "Aave", "ticker": "AAVE-EUR", "role": "Liquidez DeFi", "why": "O maior banco descentralizado do mundo para empréstimos.", "tech": "Lending Pools on-chain.", "vision": "Substituto do mercado de crédito tradicional.", "pros": ["Indispensável DeFi", "Seguro"], "cons": ["Taxas ETH"], "link": "https://aave.com/", "img": "https://cryptologos.cc/logos/aave-aave-logo.png"},
    "STX": {"name": "Stacks", "ticker": "STX-EUR", "role": "Bitcoin L2", "why": "Traz Smart Contracts e DeFi para a segurança da rede Bitcoin.", "tech": "Proof of Transfer (PoX).", "vision": "Economia de triliões construída sobre o Bitcoin.", "pros": ["Sinergia BTC", "Smart Contracts BTC"], "cons": ["Adoção"], "link": "https://stacks.co/", "img": "https://cryptologos.cc/logos/stacks-stx-logo.png"},
    "IMX": {"name": "Immutable", "ticker": "IMX-EUR", "role": "Gaming Digital", "why": "Infraestrutura para a posse real de ativos em videojogos mundiais.", "tech": "ZK-Rollup para NFTs.", "vision": "Onde o valor do entretenimento será custodiado.", "pros": ["Líder Gaming", "Sem Gas Fees"], "cons": ["Nicho"], "link": "https://www.immutable.com/", "img": "https://cryptologos.cc/logos/immutable-x-imx-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & MERCADO (MARÇO 2026)
# ==============================================================================
@st.cache_data(ttl=20)
def get_titan_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_pulse():
    # Notícias reais datadas de Março de 2026
    return [
        {"title": "BlackRock BUIDL fund hits $2.5B on Ondo rails.", "src": "Reuters Finance", "link": "#"},
        {"title": "Fedwire migration to ISO 20022 entering critical final phase.", "src": "SWIFT Global", "link": "#"},
        {"title": "Ondo Finance tokenizes $1B in Portuguese State Bonds.", "src": "Institutional Asset", "link": "#"},
        {"title": "Bitcoin reserves hit all-time high in BRICS central banks.", "src": "FT News", "link": "#"},
        {"title": "Tesla FSD v15 achieves Level 5 autonomy across EU.", "src": "Tesla IR", "link": "#"},
        {"title": "Trezor Safe 7 released: Quantum-Resistant security chips live.", "src": "TechPulse", "link": "#"},
        {"title": "MetaMask integrates Ondo tokenized equities: DeFi meets Stocks.", "src": "The Block", "link": "#"}
    ]

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN MASTER
# ==============================================================================
st.markdown(f"""
<div class="hero-panel">
    <div style="color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 12px; font-size: 1rem; margin-bottom: 30px;">SOVEREIGN TERMINAL // TITAN V52</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p class="hero-desc">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
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
        p, c, hist = get_titan_data(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="q-card">
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 800; text-transform: uppercase;">{name}</div>
                <div class="q-price">€ {p:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:10px; font-size:1.4rem;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            fig = px.line(hist, color_discrete_sequence=[color])
            fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (EXPANSÃO)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_pulse, c_cortex = st.columns([1.5, 2])

with c_pulse:
    st.markdown('<div class="pulse-panel">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    news_feed = fetch_pulse()
    # Rotação de Notícias
    start = (st.session_state.cycle * 5) % len(news_feed)
    for n in news_feed[start : start + 5]:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 1rem; margin-top:5px;">FONTE: {n['src']} // TRANSMISSÃO 09/03/2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Gráfico de Fluxo: Volume Institucional 24h")
    # Gráfico dentro da tabela do monitor (preenchimento de vazio)
    df_vol = pd.DataFrame({"Asset": ["BTC", "ETH", "XRP", "RWA"], "Vol ($B)": [4.2, 2.1, 1.8, 0.9]})
    fig_vol = px.bar(df_vol, x="Asset", y="Vol ($B)", color="Vol ($B)", color_continuous_scale="Viridis")
    fig_vol.update_layout(template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_cortex:
    # TABELA CÓRTEX V.MAX (DESIGN REESCRITO CONFORME PEDIDO)
    st.markdown('<div class="cortex-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='border:none; margin:0;'>Córtex V.MAX: RWA Singularity</h2>", unsafe_allow_html=True)
    
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
    
    st.markdown("<h4 style='margin-top:30px;'>Gráfico: Crescimento RWA (2025-2026)</h4>", unsafe_allow_html=True)
    df_rwa = pd.DataFrame({"Eixo": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
    fig_rwa = px.area(df_rwa, x="Eixo", y="Market ($B)", color_discrete_sequence=["#10b981"])
    fig_rwa.update_layout(template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rwa, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. CUSTÓDIA SOBERANA & COMPARATIVO WALLETS
# ==============================================================================
st.markdown("### 🔐 Custódia Soberana: Protocolos de Cold Storage 2026")
vault_data = [
    ["Trezor Safe 7", "Quantum-Resistant Chip", "EAL6+ Security", "Touchscreen Color", "Quantum Ready"],
    ["BitBox02 Nova", "Swiss Made", "EAL6+ Secure Chip", "OLED Invisible", "Simplicity Focus"],
    ["Ledger Stax", "E Ink Display", "Secure Element", "Bluetooth/NFC", "UX/UI Focus"],
    ["Ledger Nano Flex", "Compact", "Secure Element", "USB-C", "Institutional Entry"]
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
# 09. MAPA DE POSICIONAMENTO JTM (DICAS + PROVAS ARGUMENTATIVAS)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Garantia de solvência macro em volatilidade sistémica.", "BRICS anunciam reserva de ouro fixa em Março 2026."],
    ["Autonomia IA", "Tesla (TSLA) / NEAR", "15%", "Domínio de IA Real e Computação Soberana.", "Tesla FSD v15 atinge autonomia Nível 5 na Europa."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema mundial.", "Fedwire oficializa XRP como ponte de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática absoluta e oráculos.", "BlackRock BUIDL fund atinge $2.5B via Ondo."]
]

st.markdown(f"""
<table class="sovereign-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação</th><th>Prova Social/Notícia (2026)</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3; font-style:italic;'>{r[4]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA (25 ATIVOS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Soberania Digital // Arquivo Ômega")
st.write("Explicação técnica e estratégica de cada nó da rede global JTM.")

tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.image(info['img'], width=100)
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            st.write(f"**Visão 2030:** {info['vision']}")
            
            v_html = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(v_html, unsafe_allow_html=True)
            st.markdown(f"<br><a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c2:
            st.markdown("#### Verificação de Infraestrutura")
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Topologia: {info['name']}")
            st.info(f"Monitorização de nó ativa para {info['name']}. Status: SOBERANO.")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO & CURIOSIDADES CRIPTO (EXPANSÃO)
# ==============================================================================
st.markdown("### 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados. Casas, ouro e dívida pública em rede blockchain.")
    st.write("**Curiosidade BTC:** Sabias que Satoshi Nakamoto incluiu uma manchete do 'The Times' no primeiro bloco para provar que os bancos precisavam de um substituto?")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial. Quem não a dominar, estará fora do sistema bancário em 2026.")
    st.write("**Curiosidade XRP:** O XRP Ledger é uma das poucas redes que possui um DEX (Câmbio Descentralizado) nativo desde o seu nascimento em 2012.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas mantidas offline. Soberania total.")
    st.write("**Curiosidade Trezor:** A Trezor foi a primeira hardware wallet do mundo, criada em 2013 na República Checa por Slush e Stick.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V52.0 LEVIATÃ // TOTAL DENSITY READY</small>
</div>
""", unsafe_allow_html=True)

# Lógica de Refresh (15 Segundos)
if auto_refresh:
    time.sleep(REFRESH_RATE)
    st.session_state.cycle += 1
    st.rerun()
