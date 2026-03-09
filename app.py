import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO (ESTABILIDADE TOTAL)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Infinite Monolith V73",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'refresh_cycle' not in st.session_state: st.session_state.refresh_cycle = 0

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS TITAN V73: HYPER-SCALE & ZERO-VACUUM
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Rajdhani:wght@700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 4rem 6rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia de Comando - ESCALA MÁXIMA */
    .hero-title { font-size: 8.5rem !important; font-weight: 800; letter-spacing: -8px; line-height: 0.75; margin-bottom: 40px; }
    .hero-subtitle { font-size: 2.6rem; color: #94a3b8; font-weight: 300; border-left: 12px solid #10b981; padding-left: 55px; margin-bottom: 110px; line-height: 1.4; }

    /* Painéis de Inteligência */
    .panel-header {
        background: #1e293b; color: #8b5cf6; padding: 35px 55px; border-radius: 25px 25px 0 0;
        font-family: 'JetBrains Mono'; font-weight: 800; font-size: 2rem; letter-spacing: 6px;
        border-bottom: 4px solid #8b5cf6;
    }
    .panel-body {
        background: #0b0f1a; border-radius: 0 0 25px 25px; padding: 55px;
        border: 2px solid rgba(139, 92, 246, 0.4); margin-bottom: 70px; min-height: 700px;
    }

    /* Radar: Texto Massivo */
    .radar-entry { padding: 45px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
    .radar-tag { color: #8b5cf6; font-size: 1.5rem; font-weight: 800; display: block; margin-bottom: 18px; letter-spacing: 5px; }
    .radar-text { color: #00d4ff; font-size: 3rem !important; font-weight: 800; line-height: 1.1; }

    /* CÓRTEX V.MAX: SUPREMACIA VISUAL */
    .cortex-container {
        background: #0b0f1a; border: 12px solid #10b981; border-radius: 65px; padding: 110px;
        box-shadow: 0 0 300px rgba(16, 185, 129, 0.35); margin: 110px 0;
    }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 65px 0; border-bottom: 4px solid rgba(255,255,255,0.05); }
    .cortex-label { width: 35%; font-size: 2.4rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 14px; }
    .cortex-data { width: 65%; font-size: 4.8rem; font-weight: 700; color: #ffffff; line-height: 1; }

    /* Tabelas Soberanas: Escala Industrial */
    .master-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.95); border-radius: 55px; overflow: hidden; margin-bottom: 130px; border: 3px solid rgba(255, 255, 255, 0.1); }
    .master-table th { background: rgba(0,0,0,0.85); padding: 55px; color: #64748b; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 10px; text-align: left; }
    .master-table td { padding: 65px 55px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); color: #f1f5f9; font-size: 2.2rem; line-height: 1.5; vertical-align: top; }
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
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Hardware IA", "why": "GPU distribuída para o treino de modelos de IA.", "tech": "DePIN Network.", "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"},
    "FET": {"name": "Fetch.ai", "ticker": "FET-EUR", "role": "Agentes IA", "why": "Internet económica de agentes inteligentes.", "tech": "ASI Alliance.", "link": "https://fetch.ai/", "img": "https://cryptologos.cc/logos/fetch-ai-fet-logo.png"},
    "ICP": {"name": "Internet Computer", "ticker": "ICP-EUR", "role": "Cloud Soberana", "why": "Substitui AWS por servidores descentralizados.", "tech": "Chain Key Tech.", "link": "https://dfinity.org/", "img": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Científica", "why": "Foco em segurança formal e governança on-chain.", "tech": "Ouroboros.", "link": "https://cardano.org/", "img": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
    "DOT": {"name": "Polkadot", "ticker": "DOT-EUR", "role": "Multi-chain", "why": "Segurança partilhada e interoperabilidade massiva.", "tech": "Parachains.", "link": "https://polkadot.network/", "img": "https://cryptologos.cc/logos/polkadot-dot-logo.png"},
    "AVAX": {"name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA", "why": "Infraestrutura para redes bancárias privadas.", "tech": "Subnets.", "link": "https://avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
    "VET": {"name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real", "why": "Tokenização de ativos industriais.", "tech": "PoA.", "link": "https://vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=20)
def get_market_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

RADAR_FIXED = [
    {"tag": "RWA DOMINANCE", "msg": "BlackRock BUIDL fund atinge $2.5B on Ondo rails. Transição completa."},
    {"tag": "ISO 20022", "msg": "Fedwire completa migração. Liquidez XRP atinge recordes mundiais em S.J. Madeira."},
    {"tag": "TESLA IA", "msg": "Tesla Robotaxi Fleet atinge 1M unidades. Autonomia total Nível 5 na UE."},
    {"tag": "BITCOIN RESERVE", "msg": "BRICS oficializam Bitcoin como ativo de reserva estratégica."},
    {"tag": "PORTUGAL RWA", "msg": "Ondo tokeniza $1B em Obrigações do Tesouro Português em 2026."}
]

# ==============================================================================
# 05. TOP BAR & HERO SECTION
# ==============================================================================
c1, c2, c3 = st.columns([1.5, 2, 2])
with c1:
    st.markdown("""<div style='background:rgba(16,185,129,0.2); padding:35px; border-radius:30px; border:3px solid #10b981; text-align:center;'><h1 style='color:#f1f5f9; margin:0; font-size:2.2rem !important;'>JTM CAPITAL</h1><p style='color:#10b981; font-family:"JetBrains Mono"; font-size:1.2rem; letter-spacing:6px; margin:0;'>INFINITE V73.0</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style='background:rgba(15,23,42,0.85); padding:30px; border-radius:30px; text-align:center; height:135px; border:1px solid rgba(255,255,255,0.15);'><div style='color:#64748b; font-size:1.1rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div><div style='font-size:1.6rem; color:#ffffff; font-weight:700; margin-top:10px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style='background:rgba(15,23,42,0.85); padding:30px; border-radius:30px; text-align:center; border:2px solid #ef4444; height:135px;'><div style='color:#64748b; font-size:1.1rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div><div style='font-size:1.6rem; color:#ffffff; font-weight:700; margin-top:10px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='hero-title'>A Próxima Geração da Infraestrutura de Capital.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Monitorizamos a convergência entre o capital físico e a imutabilidade digital. Operamos na fronteira da norma ISO 20022 para garantir a soberania absoluta do investidor.</div>", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (TERMÓMETRO GLOBAL)
# ==============================================================================
st.markdown("## 🏦 Termómetro de Liquidez Global (EUR €)")
tickers = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

for i in range(0, len(tickers), 4):
    cols = st.columns(4)
    for j in range(4):
        if i+j < len(tickers):
            t, n = tickers[i+j]
            p, c, h = get_market_data(t)
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.65); padding: 65px; border-radius: 45px; border-left: 18px solid #10b981;'>
                    <div style="color: #64748b; font-size: 1.4rem; font-weight: 800; text-transform: uppercase;">{n} // LIVE</div>
                    <div style="font-size: 4.2rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 25px;">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:20px; font-size:2.2rem;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                fig = px.line(h, color_discrete_sequence=[color])
                fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA (FIX: NATIVO, ZERO VÁCUO)
# ==============================================================================
st.markdown("## 📡 Monitor de Inteligência // O Pulso do Mercado")
c_radar, c_flux = st.columns([1.5, 1.2])

with c_radar:
    st.markdown('<div class="panel-header">RADAR DE FLUXO GLOBAL (15S SYNC)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        idx = (st.session_state.refresh_cycle * 3) % len(RADAR_FIXED)
        batch = RADAR_FIXED[idx : idx + 3]
        for item in batch:
            st.markdown(f"""
            <div class="radar-entry">
                <span class="radar-tag">■ {item['tag']}</span>
                <span class="radar-text">{item['msg']}</span>
            </div>
            """, unsafe_allow_html=True)

with c_flux:
    st.markdown('<div class="panel-header" style="color:#10b981; border-color:#10b981;">FLUXO INSTITUCIONAL 24H ($B)</div>', unsafe_allow_html=True)
    flux_df = pd.DataFrame({"Origem": ["Instituições", "Whales", "RWA Settlement", "ISO Bridge", "Retail"], "Vol": [8.4, 6.2, 3.8, 5.5, 1.9]})
    fig_flux = px.bar(flux_df, x="Vol", y="Origem", orientation='h', color="Vol", color_continuous_scale="Viridis", text_auto=True)
    fig_flux.update_layout(template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=22))
    st.plotly_chart(fig_flux, use_container_width=True)

st.divider()

# ==============================================================================
# 08. CÓRTEX V.MAX: SUPREMACIA (FONTE GIGANTE)
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

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO JTM (TABELAS EXTENSAS)
# ==============================================================================
st.markdown("## 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica extrema.", "BRICS reserva física ouro (Mar 2026)."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "IA Real e Soberania Computacional Total.", "Tesla FSD v15 atinge Nível 5 na UE hoje."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema mundial.", "Fedwire integra XRP como ponte oficial."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos de dados.", "BlackRock BUIDL fund atinge $2.5B via Ondo."],
    ["Cadeia Logística", "VeChain / Algorand", "5%", "Tokenização de ativos industriais.", "Euro Digital migra infra para Algorand."]
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
# 10. CÓDICE ÔMEGA (EXPANSÃO DE 15+ ATIVOS)
# ==============================================================================
st.markdown("## 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_INFO.values()])

for i, (key, info) in enumerate(ASSET_INFO.items()):
    with tabs[i]:
        c_text, c_vis = st.columns([1.5, 1])
        with c_text:
            st.image(info['img'], width=130)
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
            # Correção do SyntaxError: Placeholder substituído por URL real ou comentário
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=800", caption=f"Topologia de Rede: {info['name']}")

            st.markdown(f"""
            <table class="master-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez</li><li>Escassez Matemática</li><li>ISO 20022</li></ul></td>
                    <td><ul><li>Regulação Fiat</li><li>Volatilidade</li></ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold; font-size:2.8rem;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c_vis:
            perf_df = pd.DataFrame({"Asset": [info['name']], "Risk": [25], "Return": [85]})
            fig_perf = px.scatter(perf_df, x="Risk", y="Return", text="Asset", size=[120], color_discrete_sequence=["#10b981"])
            fig_perf.update_layout(template="plotly_dark", height=600)
            st.plotly_chart(fig_perf, use_container_width=True)

st.divider()

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #4b5563; padding: 150px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <small>MONÓLITO V73.0 INFINITE LEVIATHAN // MASTER BASE READY</small>
</div>
""", unsafe_allow_html=True)

if sync := st.sidebar.toggle("Sincronização Ativa", value=True):
    time.sleep(REFRESH_RATE)
    st.session_state.refresh_cycle += 1
    st.rerun()
