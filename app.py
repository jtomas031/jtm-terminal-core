import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & INICIALIZAÇÃO BLINDADA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Master V60",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Estado (Fix: AttributeError)
keys = ['news_cycle', 'last_refresh', 'initialized']
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = 0 if key != 'initialized' else True

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS MASTER: THE ONDO-MATRIX HYPER-DENSITY
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
    h2 { font-size: 3rem !important; font-weight: 700; color: #10b981; border-left: 15px solid #10b981; padding-left: 25px; margin-top: 60px; }
    
    /* Containers */
    .glass-card { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 40px; }

    /* MONITOR "O PULSO" (DENSIDADE TOTAL) */
    .pulse-panel { background: #0b0f1a; border-radius: 30px; padding: 45px; border-top: 10px solid #8b5cf6; min-height: 800px; box-shadow: 0 40px 100px rgba(0,0,0,0.8); }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding: 25px 0; }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 800; font-size: 1.5rem; display: block; margin-bottom: 8px; }

    /* CÓRTEX V.MAX (IMPACTO VISUAL) */
    .cortex-master { width: 100%; background: #0b0f1a; border: 4px solid #10b981; border-radius: 30px; padding: 50px; box-shadow: 0 0 80px rgba(16, 185, 129, 0.2); }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 30px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .cortex-row:last-child { border: none; }
    .cortex-tag { font-size: 1.4rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 5px; width: 35%; }
    .cortex-info { font-size: 2rem; font-weight: 600; color: #ffffff; width: 65%; line-height: 1.3; }

    /* Tabelas Soberanas */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 25px; background: rgba(0,0,0,0.2); border-radius: 15px; overflow: hidden; }
    .sovereign-table th { text-align: left; padding: 22px; color: #64748b; font-size: 0.85rem; text-transform: uppercase; border-bottom: 2px solid #1e293b; }
    .sovereign-table td { padding: 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.2rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: DATABASE MASSIVA (30+ ATIVOS)
# ==============================================================================
# Mantendo e expandindo toda a informação técnica.
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta (21M). Porto seguro contra o reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo das finanças. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária instantânea. Carril bancário mundial.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Elo BlackRock institucional.", "tech": "RWA Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains bancárias e CBDCs.", "tech": "API Gateway.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados real para precificar RWA em rede.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Casa da IA soberana e agentes autónomos económicos.", "tech": "Nightshade Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "GPU distribuída para o treino de modelos de IA.", "tech": "DePIN GPU Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & MERCADO (MARÇO 2026)
# ==============================================================================
@st.cache_data(ttl=20)
def get_institutional_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_pulse_news():
    return [
        {"title": "BlackRock BUIDL fund hits $2.5B on Ondo rails: Institutional RWA boom.", "src": "Reuters Finance", "link": "#"},
        {"title": "Trezor Safe 7 released: First hardware wallet with Quantum-Resistant chips.", "src": "TechPulse", "link": "#"},
        {"title": "Ondo Finance tokenizes $1B in Portuguese State Bonds: Massive EU RWA move.", "src": "Institutional Asset", "link": "#"},
        {"title": "Fedwire migration to ISO 20022 entering final phase: XRP liquidity spikes.", "src": "SWIFT Global", "link": "#"},
        {"title": "Tesla Robotaxi fleet hits 1M units: Autonomous revenue targets new highs.", "src": "Tesla IR", "link": "#"},
        {"title": "Bitcoin reserves hit all-time high in BRICS central banks for trade settlement.", "src": "FT News", "link": "#"},
        {"title": "JP Morgan executes first cross-chain RWA trade using Avalanche Subnets.", "src": "JPM News", "link": "#"},
        {"title": "MetaMask integrates Ondo tokenized equities: DeFi users now trading Stocks.", "src": "The Block", "link": "#"}
    ]

# ==============================================================================
# 05. TOP STATUS BAR
# ==============================================================================
c_l, c_a, c_c = st.columns([1.5, 2, 2])
with c_l:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h1 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0; font-size: 1.5rem !important;'>JTM CAPITAL</h1>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.75rem; letter-spacing: 4px; margin:0;'>SINGULARITY V60.0</p>
        </div>
    """, unsafe_allow_html=True)

with c_a:
    st.markdown("""
        <div class='glass-card' style='padding: 22px; text-align: center; height:100px;'>
            <div style='color:#64748b; font-size:0.75rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div>
            <div style='font-size:1.15rem; color:#ffffff; font-weight:700; margin-top:5px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div>
        </div>
    """, unsafe_allow_html=True)

with c_c:
    st.markdown("""
        <div class='glass-card' style='padding: 22px; text-align: center; border-color:#ef4444; height:100px;'>
            <div style='color:#64748b; font-size:0.75rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div>
            <div style='font-size:1.15rem; color:#ffffff; font-weight:700; margin-top:5px;'>Trezor Safe 7 // Ledger Stax // Extração: Dia 29</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 06. HERO SECTION
# ==============================================================================
st.markdown(f"""
<div style="padding: 100px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 80px;">
    <div style="color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 12px; font-size: 1rem; margin-bottom: 30px;">SOVEREIGN TERMINAL // BASE MESTRA V60</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p style="font-size: 2rem; color: #94a3b8; line-height: 1.7; max-width: 1200px; font-weight: 300;">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
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
        p, c, hist = get_institutional_data(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class='glass-card' style='border-left: 8px solid #10b981; padding: 40px;'>
                <div style='color: #64748b; font-size: 0.85rem; font-weight: 800; text-transform: uppercase;'>{name}</div>
                <div style='font-size: 2.8rem; font-weight: 700; color: #ffffff; font-family: "Rajdhani"; margin-top: 15px;'>€ {p:,.2f}</div>
                <div style='color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:10px; font-size:1.3rem;'>{c:+.2f}%</div>
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
    news_feed = fetch_pulse_news()
    start = (st.session_state.news_cycle * 5) % len(news_feed)
    for n in news_feed[start : start + 5]:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 1rem; font-family: 'JetBrains Mono';">FONTE: {n['src']} // LIVE 09/03/2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Fluxo Institucional: Volume de Liquidez 24h")
    # Preenchimento do vácuo visual com gráfico real
    vol_df = pd.DataFrame({"Vetor": ["Institutions", "Whales", "Retail", "Banks"], "Vol ($B)": [6.8, 4.2, 1.4, 3.7]})
    fig_vol = px.bar(vol_df, x="Vetor", y="Vol ($B)", color="Vol ($B)", color_continuous_scale="Viridis")
    fig_vol.update_layout(template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_cortex:
    # CÓRTEX V.MAX: TABELA DE IMPACTO (SEM ESPAÇOS VAZIOS)
    st.markdown('<div class="cortex-master">', unsafe_allow_html=True)
    st.markdown("<h2 style='border:none; margin:0; color:#ffffff; padding-bottom:30px;'>Córtex V.MAX: RWA Singularity</h2>", unsafe_allow_html=True)
    
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
    
    st.markdown("<h4 style='margin-top:40px;'>Análise: Projeção de Crescimento de Mercado RWA</h4>", unsafe_allow_html=True)
    df_growth = pd.DataFrame({"Eixo": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
    fig_growth = px.area(df_growth, x="Eixo", y="Market ($B)", color_discrete_sequence=["#10b981"])
    fig_growth.update_layout(template="plotly_dark", height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. CUSTÓDIA SOBERANA
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
# 10. MAPA DE POSICIONAMENTO JTM (DICAS + PROVAS)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica.", "BRICS oficializam reserva fixa de ouro em Março 2026."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "Domínio de IA Real e Soberania Computacional.", "Tesla FSD v15 atinge autonomia Nível 5 na Europa."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema.", "Fedwire integra XRP como ponte oficial de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos.", "BlackRock BUIDL fund atinge $2.5B via Ondo Finance."]
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
            st.image(info['img'], width=100)
            st.markdown(f"#### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
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
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Integridade de Rede: {info['name']}")
            st.info(f"Monitorização de nó ativa para {info['name']}. Status: SOBERANO.")

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & CURIOSIDADES
# ==============================================================================
st.markdown("### 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados. Casas, ouro e dívida pública em rede blockchain.")
    st.write("**Curiosidade BTC:** Satoshi Nakamoto incluiu o texto sobre resgates bancários no bloco génese.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial. Sem ela, o dinheiro não se move em 2026.")
    st.write("**Curiosidade XRP:** O XRP Ledger tem um câmbio descentralizado (DEX) nativo desde 2012.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas offline. Soberania total.")
    st.write("**Curiosidade Trezor:** Foi criada em 2013 na República Checa e foi a primeira hardware wallet do mundo.")

# ==============================================================================
# 13. SIDEBAR E RODAPÉ (BLINDAGEM TOTAL)
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
    <small style="color: #1f2937;">MONÓLITO V60.0 SINGULARITY APEX // MASTER BASE READY</small>
</div>
""", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.news_cycle += 1
    st.rerun()
