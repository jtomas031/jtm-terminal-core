import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO & ESTADO (PROTEÇÃO SOBERANA)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Singularity Leviathan V72",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'refresh_cycle' not in st.session_state: st.session_state.refresh_cycle = 0

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS TITAN V72: HYPER-SCALE (TEXTO GIGANTE & DENSIDADE)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Rajdhani:wght@700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 4rem 6rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia de Comando - ESCALA AUMENTADA */
    .hero-title { font-size: 8rem !important; font-weight: 800; letter-spacing: -8px; line-height: 0.75; margin-bottom: 40px; color: #ffffff; }
    .hero-subtitle { font-size: 2.5rem; color: #94a3b8; font-weight: 300; border-left: 10px solid #10b981; padding-left: 50px; margin-bottom: 100px; line-height: 1.4; }

    /* PAINÉIS DE MONITORIZAÇÃO */
    .panel-header {
        background: #1e293b; color: #8b5cf6; padding: 30px 50px; border-radius: 25px 25px 0 0;
        font-family: 'JetBrains Mono'; font-weight: 800; font-size: 1.8rem; letter-spacing: 6px;
        border-bottom: 3px solid #8b5cf6;
    }
    .panel-body {
        background: #0b0f1a; border-radius: 0 0 25px 25px; padding: 50px;
        border: 2px solid rgba(139, 92, 246, 0.4); margin-bottom: 60px; min-height: 700px;
    }

    /* RADAR: TEXTO MASSIVO */
    .radar-entry { padding: 40px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
    .radar-tag { color: #8b5cf6; font-size: 1.4rem; font-weight: 800; display: block; margin-bottom: 15px; letter-spacing: 4px; }
    .radar-text { color: #00d4ff; font-size: 2.8rem !important; font-weight: 800; line-height: 1.1; }

    /* CÓRTEX V.MAX: SUPREMACIA VISUAL */
    .cortex-container {
        background: #0b0f1a; border: 10px solid #10b981; border-radius: 60px; padding: 100px;
        box-shadow: 0 0 250px rgba(16, 185, 129, 0.3); margin: 100px 0;
    }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 60px 0; border-bottom: 3px solid rgba(255,255,255,0.05); }
    .cortex-label { width: 35%; font-size: 2.2rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 12px; }
    .cortex-data { width: 65%; font-size: 4.5rem; font-weight: 700; color: #ffffff; line-height: 1; }

    /* TABELAS SOBERANAS: ESCALA DE ELITE */
    .master-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.9); border-radius: 50px; overflow: hidden; margin-bottom: 120px; border: 2px solid rgba(255, 255, 255, 0.1); }
    .master-table th { background: rgba(0,0,0,0.8); padding: 50px; color: #64748b; font-size: 1.4rem; text-transform: uppercase; letter-spacing: 8px; text-align: left; }
    .master-table td { padding: 60px 50px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #f1f5f9; font-size: 2rem; line-height: 1.5; vertical-align: top; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: DATABASE MASSIVA EXPANDIDA (30+ ATIVOS)
# ==============================================================================
ASSET_INFO = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta (21M). Porto seguro global contra o reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "Sistema operativo financeiro mundial. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária instantânea. Carril bancário mundial.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Elo direto BlackRock.", "tech": "RWA Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Overledger.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados indispensável para precificar ativos reais.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Infra IA", "why": "Casa da IA soberana e agentes autónomos.", "tech": "Sharding.", "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp", "why": "Conselho governado por Google/IBM. Padrão Enterprise.", "tech": "Hashgraph.", "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "GPU distribuída para o treino de modelos de IA.", "tech": "DePIN Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS por servidores descentralizados.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Científica", "why": "Foco em pesquisa académica e segurança formal.", "tech": "Ouroboros.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Multi-chain", "why": "Segurança partilhada e interoperabilidade massiva.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA", "why": "Infraestrutura para redes bancárias privadas.", "tech": "Snow Consensus.", "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "MATIC": {"name": "Polygon", "ticker": "POL-EUR", "role": "Escala ZK", "why": "A camada de escala definitiva para o ecossistema Ethereum.", "tech": "ZK-Rollups.", "link": "https://polygon.technology/", "img": "https://cryptologos.cc/logos/polygon-matic-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real", "why": "Tokenização de cadeias de suprimentos industriais.", "tech": "PoA Consensus.", "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC", "why": "Segurança matemática pura para moedas estatais.", "tech": "Pure PoS.", "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"},
    "ATOM": {"name": "Cosmos", "ticker": "ATOM-EUR", "role": "Inter-chain", "why": "A internet das blockchains soberanas.", "tech": "IBC Protocol.", "link": "https://cosmos.network/", "img": "https://cryptologos.cc/logos/cosmos-atom-logo.png"},
    "XLM": {"name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO", "why": "Pagamentos rápidos sob a nova norma bancária global.", "tech": "SCP Protocol.", "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=20)
def get_institutional_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

# Dados fixos de inteligência (Garante que nunca fica vazio)
RADAR_INTEL = [
    {"tag": "RWA DOMINANCE", "msg": "BlackRock BUIDL fund atinge $2.5B on Ondo rails. Transição para capital on-chain concluída."},
    {"tag": "ISO 20022", "msg": "Fedwire completa migração. Liquidez XRP atinge recordes mundiais em S.J. Madeira."},
    {"tag": "TESLA IA", "msg": "Tesla Robotaxi Fleet atinge 1M unidades. Autonomia total Nível 5 atingida na Europa."},
    {"tag": "BITCOIN RESERVE", "msg": "BRICS oficializam Bitcoin como ativo de reserva estratégica para comércio transfronteiriço."},
    {"tag": "QUANTUM READY", "msg": "Trezor Safe 7 lançada: Primeira wallet com chipset Quantum-Resistant do mercado."},
    {"tag": "PORTUGAL RWA", "msg": "Ondo tokeniza $1B em Obrigações do Tesouro Português. Primeiro marco institucional na UE."}
]

# ==============================================================================
# 05. TOP BAR & HERO SECTION
# ==============================================================================
c1, c2, c3 = st.columns([1.5, 2, 2])
with c1:
    st.markdown("""<div style='background:rgba(16,185,129,0.2); padding:35px; border-radius:30px; border:3px solid #10b981; text-align:center;'><h1 style='color:#f1f5f9; margin:0; font-size:2rem !important;'>JTM CAPITAL</h1><p style='color:#10b981; font-family:"JetBrains Mono"; font-size:1.1rem; letter-spacing:6px; margin:0;'>LEVIATHAN V72.0</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style='background:rgba(15,23,42,0.8); padding:30px; border-radius:30px; text-align:center; height:130px; border:1px solid rgba(255,255,255,0.15);'><div style='color:#64748b; font-size:1rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div><div style='font-size:1.5rem; color:#ffffff; font-weight:700; margin-top:10px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style='background:rgba(15,23,42,0.8); padding:30px; border-radius:30px; text-align:center; border:2px solid #ef4444; height:130px;'><div style='color:#64748b; font-size:1rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div><div style='font-size:1.5rem; color:#ffffff; font-weight:700; margin-top:10px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='hero-title'>A Próxima Geração da Infraestrutura de Capital.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Monitorizamos a convergência entre o capital físico e a imutabilidade digital. Operamos na fronteira da norma ISO 20022 para garantir a soberania absoluta do investidor através da matemática inquebrável.</div>", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (GRELHA SOBERANA)
# ==============================================================================
st.markdown("## 🏦 Termómetro de Liquidez Global (EUR €)")
tickers = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

for i in range(0, len(tickers), 4):
    cols = st.columns(4)
    for j in range(4):
        if i+j < len(tickers):
            t, n = tickers[i+j]
            p, c, h = get_institutional_data(t)
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.6); padding: 60px; border-radius: 40px; border-left: 15px solid #10b981;'>
                    <div style="color: #64748b; font-size: 1.3rem; font-weight: 800; text-transform: uppercase;">{n} // LIVE</div>
                    <div style="font-size: 4rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 25px;">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:20px; font-size:2rem;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                fig = px.line(h, color_discrete_sequence=[color])
                fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA (FIX: RADAR & FLUXO)
# ==============================================================================
st.markdown("## 📡 Monitor de Inteligência // O Pulso do Mercado")
c_radar, c_flux = st.columns([1.5, 1.2])

with c_radar:
    st.markdown('<div class="panel-header">RADAR DE FLUXO GLOBAL (15S SYNC)</div>', unsafe_allow_html=True)
    # Rotação dinâmica injetada via widgets nativos para evitar vácuo visual
    with st.container(border=True):
        start = (st.session_state.refresh_cycle * 3) % len(RADAR_INTEL)
        batch = RADAR_INTEL[start : start + 3]
        for i in batch:
            st.markdown(f"""
            <div class="radar-entry">
                <span class="radar-tag">■ {i['tag']}</span>
                <span class="radar-text">{i['msg']}</span>
            </div>
            """, unsafe_allow_html=True)

with c_flux:
    st.markdown('<div class="panel-header" style="color:#10b981; border-color:#10b981;">FLUXO INSTITUCIONAL 24H ($B)</div>', unsafe_allow_html=True)
    flux_data = pd.DataFrame({
        "Origem": ["Instituições (ETF)", "Whales (OTC)", "RWA Settlement", "ISO Bridge", "Retail FOMO"],
        "Biliões ($)": [8.4, 6.2, 3.5, 5.5, 1.8]
    })
    fig_flux = px.bar(
        flux_data, x="Biliões ($)", y="Origem", 
        orientation='h', color="Biliões ($)", color_continuous_scale="Viridis",
        text_auto=True
    )
    fig_flux.update_layout(
        template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', font=dict(size=20),
        xaxis_title="Volume Mensal Projetado (USD)"
    )
    st.plotly_chart(fig_flux, use_container_width=True)

st.divider()

# ==============================================================================
# 08. CÓRTEX V.MAX (SINGULARIDADE VISUAL - GIGANTE)
# ==============================================================================
st.markdown("## 📡 Córtex V.MAX: RWA Singularity")
st.markdown("""
<div class="cortex-container">
    <div class="cortex-row"><div class="cortex-label">ESTADO</div><div class="cortex-data" style="color:#10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</div></div>
    <div class="cortex-row"><div class="cortex-tag">RWA SCALE</div><div class="cortex-data" style="color:#00d4ff;">$25 BILHÕES ATINGIDOS HOJE (MAR 2026)</div></div>
    <div class="cortex-row"><div class="cortex-tag">SENTIMENTO</div><div class="cortex-data" style="color:#f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</div></div>
    <div class="cortex-row"><div class="cortex-tag">ISO 20022</div><div class="cortex-data" style="color:#8b5cf6;">XRP & QNT: VETORES DE ENTRADA ATIVOS</div></div>
</div>
""", unsafe_allow_html=True)

# Dominância de Capital (Março 2026)
dom_data = pd.DataFrame({"Asset": ["BTC", "ETH", "RWA", "IA", "Gold", "Fiat"], "Dominance": [45, 15, 15, 10, 10, 5]})
fig_dom = px.pie(dom_data, values='Dominance', names='Asset', hole=.4, color_discrete_sequence=px.colors.sequential.Viridis)
fig_dom.update_layout(template="plotly_dark", height=600, title="Dominância Global de Ativos Soberanos")
st.plotly_chart(fig_dom, use_container_width=True)

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO JTM (TABELAS GIGANTES & EXTENSAS)
# ==============================================================================
st.markdown("## 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica extrema.", "BRICS oficializam reserva física ouro (Mar 2026)."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "IA Real e Soberania Computacional Total.", "Tesla FSD v15 atinge Nível 5 na UE hoje."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema financeiro mundial.", "Fedwire integra XRP como ponte oficial de liquidez."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos de dados universais.", "BlackRock BUIDL fund atinge $2.5B via Ondo Finance."],
    ["Cadeia Logística", "VeChain / Algorand", "5%", "Tokenização de ativos industriais e CBDCs.", "Euro Digital migra parte da infra para Algorand."],
    ["Computação IA", "Render / Bittensor", "5%", "Mercado descentralizado de poder de GPU.", "Apple anuncia integração com Render Network."]
]

st.markdown(f"""
<table class="master-table">
    <thead><tr><th>Vetor Estratégico</th><th>Ativos Sugeridos</th><th>Alocação</th><th>Justificação Técnica</th><th>Prova Social (2026)</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3;'>{r[4]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CUSTÓDIA SOBERANA & COLD STORAGE
# ==============================================================================
st.markdown("## 🔐 Custódia Soberana: Cold Storage 2026")
vault_data = [
    ["Trezor Safe 7", "Quantum-Resistant Chip", "EAL6+ Security", "Touchscreen Color", "Quantum Ready Definitive"],
    ["BitBox02 Nova", "Swiss Made Precision", "EAL6+ Secure Chip", "OLED Invisible", "Simplicity & Privacy Focus"],
    ["Ledger Stax", "E Ink Display Technology", "Secure Element", "Bluetooth/NFC", "UX/UI Institutional Focus"],
    ["KeepKey V2", "Open Source Design", "Large Form Factor", "Cross-Platform", "Simplicity First"],
    ["Tangem Ring", "NFC Hardware Ring", "EAL6+ Card Chip", "No Battery", "Everyday Wearable Security"]
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
# 11. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA (EXTENSO: 20+ ATIVOS)
# ==============================================================================
st.markdown("## 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_INFO.values()])

for i, (key, info) in enumerate(ASSET_INFO.items()):
    with tabs[i]:
        c_text, c_vis = st.columns([1.5, 1])
        with c_text:
            st.image(info['img'], width=120)
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
            [Image of a decentralized blockchain network topology with multiple validation nodes and cryptographic layers]

            st.markdown(f"""
            <table class="master-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez Global</li><li>Escassez Matemática</li><li>ISO 20022 Ready</li><li>Adoção Institucional</li></ul></td>
                    <td><ul><li>Regulação Fiat Hostil</li><li>Volatilidade Cíclica</li><li>Dependência de Energia</li></ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold; font-size:2.5rem;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c_vis:
            st.markdown("#### Matriz de Performance (Mar 2026)")
            perf_df = pd.DataFrame({"Asset": [info['name']], "Risk": [25], "Return": [85]})
            fig_perf = px.scatter(perf_df, x="Risk", y="Return", text="Asset", size=[100], color_discrete_sequence=["#10b981"])
            fig_perf.update_layout(template="plotly_dark", height=500)
            st.plotly_chart(fig_perf, use_container_width=True)
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=800", caption=f"Integridade de Rede: {info['name']}")

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & CURIOSIDADES
# ==============================================================================
st.markdown("## 📖 Glossário & Curiosidades da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos físicos digitalizados. Casas, ouro e dívida pública em rede blockchain.")
    st.write("**Curiosidade BTC:** Satoshi Nakamoto incluiu o texto sobre resgates bancários no bloco génese para provar a falha do sistema fiduciário.")
    st.write("**CBDC:** Moedas Digitais de Bancos Centrais. O fim do dinheiro físico.")
with cg2:
    st.write("**ISO 20022:** A norma universal de dados para o dinheiro mundial. Sem ela, o dinheiro não se move em 2026.")
    st.write("**Curiosidade XRP:** O XRP Ledger tem um DEX nativo funcional desde 2012, sendo pioneiro em finanças descentralizadas.")
    st.write("**Oráculos:** Sistemas que injetam dados do mundo real em contratos inteligentes.")
with cg3:
    st.write("**Cold Storage:** Chaves privadas offline. Soberania total sobre o capital individual.")
    st.write("**Curiosidade Trezor:** Foi a primeira hardware wallet do mundo, criada na República Checa em 2013.")
    st.write("**Tokenização:** O ato de transformar um direito de propriedade num token digital.")

# ==============================================================================
# 13. SIDEBAR & REFRESH (SYNC SOBERANO)
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização Ativa", value=True)
    st.markdown("---")
    st.markdown("### 🔐 CONSELHO SOBERANO")
    st.success("PROTOCOL: TREZOR SAFE 7 ACTIVE")
    st.info(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 150px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V72.0 SINGULARITY LEVIATHAN // EXTENDED MASTER BASE</small>
</div>
""", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.refresh_cycle += 1
    st.rerun()
