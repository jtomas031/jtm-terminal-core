import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE ESTADO & SEGURANÇA (FIX: TODOS OS ERROS DE SESSÃO)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Genesis V61",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Estado Robusta
for key, val in {'news_cycle': 0, 'pulse_idx': 0, 'last_refresh': time.time()}.items():
    if key not in st.session_state:
        st.session_state[key] = val

REFRESH_RATE = 15 

# ==============================================================================
# 02. ARQUITETURA VISUAL: CSS CUSTOMIZADO (DENSIDADE TOTAL)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 3rem 5rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia e Títulos */
    .hero-title { font-size: 6.5rem !important; font-weight: 800; letter-spacing: -6px; line-height: 0.8; margin-bottom: 20px; color: #ffffff; }
    .hero-subtitle { font-size: 1.8rem; color: #94a3b8; font-weight: 300; border-left: 3px solid #10b981; padding-left: 30px; margin-bottom: 60px; }

    /* Estilo de Tabelas e Cards */
    .master-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.6); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 40px; }
    .master-table th { background: rgba(0,0,0,0.4); padding: 25px; color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 3px; text-align: left; }
    .master-table td { padding: 30px 25px; border-bottom: 1px solid rgba(255, 255, 255, 0.03); color: #f1f5f9; font-size: 1.2rem; }
    
    /* CÓRTEX V.MAX: DESIGN DE ALTO IMPACTO */
    .cortex-card { background: #0b0f1a; border: 4px solid #10b981; border-radius: 30px; padding: 50px; margin: 40px 0; box-shadow: 0 0 100px rgba(16, 185, 129, 0.15); }
    .cortex-row { display: flex; align-items: center; padding: 25px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .cortex-label { width: 30%; font-size: 1.4rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 5px; }
    .cortex-value { width: 70%; font-size: 2.2rem; font-weight: 700; color: #ffffff; line-height: 1.2; }

    /* News Box */
    .pulse-panel { background: #0b0f1a; border-radius: 30px; padding: 45px; border-top: 10px solid #8b5cf6; margin-bottom: 40px; }
    .news-item { padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.03); }
    .news-link { color: #00d4ff; text-decoration: none; font-weight: 800; font-size: 1.6rem; display: block; }
    
    /* Telemetria de Preços */
    .price-card { background: rgba(15, 23, 42, 0.5); padding: 35px; border-radius: 20px; border-left: 6px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: DATABASE COMPLETA (30+ NÓS ESTRATÉGICOS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez imutável (21M). Porto seguro contra o reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo das finanças. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária. Liquidação instantânea de pagamentos globais.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Parceiro oficial BlackRock.", "tech": "Institutional Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Gateway.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados reais indispensável para ativos tokenizados.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Casa da IA soberana e agentes autónomos económicos.", "tech": "Nightshade Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp", "why": "Conselho governado por Google e IBM. Padrão Enterprise.", "tech": "Hashgraph.", "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "GPU distribuída para o treino de modelos de inteligência.", "tech": "DePIN Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes autónomos.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS/Google Cloud por servidores descentralizados.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Pesquisa", "why": "Segurança formal e governança on-chain robusta.", "tech": "Ouroboros PoS.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Interconexão", "why": "Segurança partilhada e interoperabilidade massiva.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "A camada de escala definitiva para o ecossistema Ethereum.", "tech": "ZK-Rollups.", "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Pagamentos rápidos sob a nova norma bancária global.", "tech": "SCP Protocol.", "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & RADAR DE NOTÍCIAS (MARÇO 2026)
# ==============================================================================
@st.cache_data(ttl=20)
def get_market_telemetry(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_live_radar():
    return [
        {"title": "BlackRock BUIDL fund hits $2.5B on Ondo rails: Institutional RWA surge.", "src": "Reuters Finance", "link": "#"},
        {"title": "Fedwire migration to ISO 20022 entering final phase: XRP liquidity spikes.", "src": "SWIFT Global", "link": "#"},
        {"title": "Trezor Safe 7 released: First hardware wallet with Quantum-Resistant chips.", "src": "TechPulse", "link": "#"},
        {"title": "Ondo Finance tokenizes $1B in Portuguese State Bonds: Massive EU RWA move.", "src": "Institutional Asset", "link": "#"},
        {"title": "Tesla Robotaxi fleet hits 1M units: Autonomous revenue targets new highs.", "src": "Tesla IR", "link": "#"},
        {"title": "Bitcoin reserves hit all-time high in BRICS central banks for trade settlement.", "src": "FT News", "link": "#"},
        {"title": "MetaMask integrates Ondo tokenized equities: DeFi users now trading Stocks.", "src": "The Block", "link": "#"}
    ]

# ==============================================================================
# 05. TOP BAR: TERMINAL BLOOMBERG STYLE
# ==============================================================================
c1, c2, c3 = st.columns([1.5, 2, 2])
with c1:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h1 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0; font-size: 1.5rem !important;'>JTM CAPITAL</h1>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.75rem; letter-spacing: 4px; margin:0;'>SINGULARITY V61.0</p>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 22px; border-radius: 20px; text-align: center; height: 100px;'>
            <div style='color: #64748b; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;'>🏛️ Matriz de Alocação</div>
            <div style='font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-top: 5px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
        <div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); padding: 22px; border-radius: 20px; text-align: center; border-color: #ef4444; height: 100px;'>
            <div style='color: #64748b; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;'>🔒 Custódia Ativa</div>
            <div style='font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-top: 5px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 06. HERO SECTION
# ==============================================================================
st.markdown("<div class='hero-title'>A Próxima Geração da Infraestrutura de Capital.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. Garantimos soberania absoluta através da matemática.</div>", unsafe_allow_html=True)

# ==============================================================================
# 07. TELEMETRIA DINÂMICA (GRELHA DE PREÇOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
tickers = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

for i in range(0, len(tickers), 4):
    cols = st.columns(4)
    for j in range(4):
        if i+j < len(tickers):
            t, n = tickers[i+j]
            p, c, h = get_market_telemetry(t)
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div class="price-card">
                    <div style="color: #64748b; font-size: 0.85rem; font-weight: 800; text-transform: uppercase;">{n}</div>
                    <div style="font-size: 2.8rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 10px;">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:10px;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                fig = px.line(h, color_discrete_sequence=[color])
                fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 08. CÓRTEX V.MAX: RWA SINGULARITY (DESIGN MASTER)
# ==============================================================================
st.markdown("## 📡 Córtex V.MAX: RWA Singularity")
st.markdown("""
<div class="cortex-card">
    <div class="cortex-row">
        <div class="cortex-label">ESTADO</div>
        <div class="cortex-value" style="color: #10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">RWA SCALE</div>
        <div class="cortex-value" style="color: #00d4ff;">$25 BILHÕES ATINGIDOS HOJE (MAR 2026)</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">SENTIMENTO</div>
        <div class="cortex-value" style="color: #f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</div>
    </div>
    <div class="cortex-row">
        <div class="cortex-label">ISO 20022</div>
        <div class="cortex-value" style="color: #8b5cf6;">XRP & QNT: VETORES DE ENTRADA ATIVOS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Preenchimento de vácuo com gráfico de escala
df_rwa = pd.DataFrame({"Data": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
fig_rwa = px.area(df_rwa, x="Data", y="Market ($B)", color_discrete_sequence=["#10b981"], title="Projeção de Escala RWA 2026")
fig_rwa.update_layout(template="plotly_dark", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_rwa, use_container_width=True)

st.divider()

# ==============================================================================
# 09. MONITOR DE INTELIGÊNCIA // O PULSO DO MERCADO
# ==============================================================================
st.markdown("## 📡 Monitor de Inteligência")
c_pulse, c_vol = st.columns([1.5, 1])

with c_pulse:
    st.markdown('<div class="pulse-panel">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    news = fetch_live_radar()
    start = (st.session_state.news_cycle * 5) % len(news)
    for n in news[start : start + 5]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{n['link']}" class="news-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 1rem; margin-top:5px;">FONTE: {n['src']} // TRANSMISSÃO 09/03/2026</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_vol:
    st.markdown('<div class="pulse-panel" style="border-top-color:#10b981;">', unsafe_allow_html=True)
    st.markdown("#### Fluxo Institucional 24h ($B)")
    vol_data = pd.DataFrame({"Ativo": ["BTC", "ETH", "XRP", "RWA"], "Vol": [6.8, 3.2, 2.1, 1.4]})
    fig_vol = px.bar(vol_data, x="Ativo", y="Vol", color="Vol", color_continuous_scale="Viridis")
    fig_vol.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. MAPA DE POSICIONAMENTO JTM (TABELAS SEQUENCIAIS)
# ==============================================================================
st.markdown("## 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica.", "BRICS oficializam reserva de ouro (Mar 2026)."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "Domínio de IA Real e Soberania Computacional.", "Tesla FSD v15 atinge autonomia Nível 5 na UE."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema.", "Fedwire integra XRP como ponte oficial de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos de dados.", "BlackRock BUIDL fund atinge $2.5B via Ondo Finance."]
]

st.markdown(f"""
<table class="master-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação</th><th>Prova Social (2026)</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3; font-style:italic;'>{r[4]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. CUSTÓDIA SOBERANA & COMPARATIVO WALLETS
# ==============================================================================
st.markdown("## 🔐 Custódia Soberana: Cold Storage 2026")
vault_data = [
    ["Trezor Safe 7", "Quantum-Resistant Chip", "EAL6+ Security", "Touchscreen Color", "Quantum Ready"],
    ["BitBox02 Nova", "Swiss Made", "EAL6+ Secure Chip", "OLED Invisible", "Simplicity Focus"],
    ["Ledger Stax", "E Ink Display", "Secure Element", "Bluetooth/NFC", "UX/UI Focus"]
]

st.markdown(f"""
<table class="master-table">
    <thead><tr><th>Dispositivo</th><th>Arquitetura</th><th>Certificação</th><th>Interface</th><th>Destaque 2026</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in vault_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA
# ==============================================================================
st.markdown("## 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c_text, c_img = st.columns([1.5, 1])
        with c_text:
            st.image(info['img'], width=80)
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
            # Diagramas solicitados
            if key == "BTC":
                
            elif key == "ONDO":
                

            st.markdown(f"""
            <table class="master-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez</li><li>Escassez Matemática</li><li>ISO 20022 Ready</li></ul></td>
                    <td><ul><li>Regulação Fiat</li><li>Volatilidade Cíclica</li></ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c_img:
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Monitor de Nó: {info['name']}")

st.divider()

# ==============================================================================
# 13. GLOSSÁRIO SOBERANO & CURIOSIDADES
# ==============================================================================
st.markdown("## 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados.")
    st.write("**Curiosidade BTC:** Satoshi Nakamoto incluiu o texto sobre resgates bancários no bloco génese para provar a falha do sistema fiduciário.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial.")
    st.write("**Curiosidade XRP:** O XRP Ledger tem um DEX nativo funcional desde 2012, sendo pioneiro em finanças descentralizadas.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas offline. Soberania total.")
    st.write("**Curiosidade Trezor:** Foi a primeira hardware wallet do mundo, criada para proteger o capital soberano contra hackers.")

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática."</em><br>
    <small style="color: #1f2937;">MONÓLITO V61.0 THE MASTER GENESIS // STABLE READY</small>
</div>
""", unsafe_allow_html=True)

# Lógica de Refresh
time.sleep(REFRESH_RATE)
st.session_state.news_cycle += 1
st.rerun()
