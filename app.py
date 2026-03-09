import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO & ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Architect V71",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'refresh_cycle' not in st.session_state: st.session_state.refresh_cycle = 0

REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS TITAN V71: DESIGN DE ALTA DENSIDADE (TEXTO GIGANTE)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Rajdhani:wght@700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 3rem 5rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Cabeçalhos Massivos */
    .hero-title { font-size: 7rem !important; font-weight: 800; letter-spacing: -6px; line-height: 0.8; margin-bottom: 30px; }
    .hero-subtitle { font-size: 2.2rem; color: #94a3b8; font-weight: 300; border-left: 8px solid #10b981; padding-left: 45px; margin-bottom: 90px; }

    /* Estilo de Painéis de Inteligência */
    .panel-header {
        background: #1e293b; color: #8b5cf6; padding: 20px 40px; border-radius: 20px 20px 0 0;
        font-family: 'JetBrains Mono'; font-weight: 800; font-size: 1.4rem; letter-spacing: 5px;
        border-bottom: 2px solid #8b5cf6;
    }
    .panel-body {
        background: #0b0f1a; border-radius: 0 0 20px 20px; padding: 40px;
        border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 40px; min-height: 600px;
    }

    /* Texto do Radar */
    .radar-entry { padding: 30px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
    .radar-tag { color: #8b5cf6; font-size: 1.2rem; font-weight: 800; display: block; margin-bottom: 10px; }
    .radar-text { color: #00d4ff; font-size: 2.5rem !important; font-weight: 800; line-height: 1.1; }

    /* CÓRTEX V.MAX: DESIGN MESTRE */
    .cortex-container {
        background: #0b0f1a; border: 8px solid #10b981; border-radius: 50px; padding: 80px;
        box-shadow: 0 0 200px rgba(16, 185, 129, 0.3); margin: 80px 0;
    }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 50px 0; border-bottom: 2px solid rgba(255,255,255,0.05); }
    .cortex-label { width: 35%; font-size: 2rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 10px; }
    .cortex-data { width: 65%; font-size: 3.8rem; font-weight: 700; color: #ffffff; line-height: 1; }

    /* Tabelas Soberanas */
    .master-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.9); border-radius: 40px; overflow: hidden; margin-bottom: 100px; }
    .master-table th { background: rgba(0,0,0,0.7); padding: 45px; color: #64748b; font-size: 1.2rem; text-transform: uppercase; text-align: left; }
    .master-table td { padding: 55px 45px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #f1f5f9; font-size: 1.8rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. DATABASE SOBERANA (ARQUIVO ÔMEGA)
# ==============================================================================
ASSET_INFO = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta (21M). Porto seguro global contra o reset fiduciário.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "Sistema operativo financeiro mundial. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária instantânea. Carril bancário mundial.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Elo direto BlackRock.", "tech": "RWA Tokenization.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Overledger.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados indispensável para precificar ativos reais.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE MERCADO & TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=20)
def get_live_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

# Dados fixos de inteligência para o Radar
RADAR_INTEL = [
    {"tag": "RWA DOMINANCE", "msg": "BlackRock BUIDL fund atinge $2.5B on Ondo rails. Transição completa."},
    {"tag": "ISO 20022", "msg": "Fedwire completa migração. Liquidez XRP atinge recordes mundiais."},
    {"tag": "TESLA IA", "msg": "Tesla Robotaxi Fleet atinge 1M unidades. Autonomia Nível 5 na UE."},
    {"tag": "BITCOIN RESERVE", "msg": "BRICS oficializam Bitcoin como ativo de reserva estratégica."},
    {"tag": "QUANTUM READY", "msg": "Trezor Safe 7 lançada: Proteção contra computação quântica ativa."},
    {"tag": "PORTUGAL RWA", "msg": "Ondo tokeniza $1B em Obrigações do Tesouro Português em S.J. Madeira."}
]

# ==============================================================================
# 05. TOP BAR & HERO SECTION
# ==============================================================================
c1, c2, c3 = st.columns([1.5, 2, 2])
with c1:
    st.markdown("""<div style='background:rgba(16,185,129,0.15); padding:30px; border-radius:25px; border:2px solid #10b981; text-align:center;'><h1 style='color:#f1f5f9; margin:0; font-size:1.8rem !important;'>JTM CAPITAL</h1><p style='color:#10b981; font-family:"JetBrains Mono"; font-size:0.9rem; letter-spacing:5px; margin:0;'>ARCHITECT V71.0</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style='background:rgba(15,23,42,0.6); padding:22px; border-radius:25px; text-align:center; height:115px; border:1px solid rgba(255,255,255,0.1);'><div style='color:#64748b; font-size:0.9rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div><div style='font-size:1.3rem; color:#ffffff; font-weight:700; margin-top:8px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style='background:rgba(15,23,42,0.6); padding:22px; border-radius:25px; text-align:center; border:2px solid #ef4444; height:115px;'><div style='color:#64748b; font-size:0.9rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div><div style='font-size:1.3rem; color:#ffffff; font-weight:700; margin-top:8px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='hero-title'>A Próxima Geração da Infraestrutura de Capital.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Terminal Sovereign Master. Monitorizamos a convergência entre o capital físico e a imutabilidade digital.</div>", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (TERMÓMETRO GLOBAL)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
tickers = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
           ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

for i in range(0, len(tickers), 4):
    cols = st.columns(4)
    for j in range(4):
        if i+j < len(tickers):
            t, n = tickers[i+j]
            p, c, h = get_live_data(t)
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.5); padding: 55px; border-radius: 30px; border-left: 12px solid #10b981;'>
                    <div style="color: #64748b; font-size: 1.1rem; font-weight: 800; text-transform: uppercase;">{n} // LIVE</div>
                    <div style="font-size: 3.5rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 20px;">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:15px; font-size:1.8rem;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                fig = px.line(h, color_discrete_sequence=[color])
                fig.update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA (FIX: RADAR & FLUXO PREENCHIDOS)
# ==============================================================================
st.markdown("## 📡 Monitor de Inteligência // O Pulso do Mercado")
c_radar, c_flux = st.columns([1.5, 1.2])

with c_radar:
    st.markdown('<div class="panel-header">RADAR DE FLUXO GLOBAL (15S SYNC)</div>', unsafe_allow_html=True)
    # Rotação dinâmica injetada via texto direto (Garante que nunca fica vazio)
    start = (st.session_state.refresh_cycle * 3) % len(RADAR_INTEL)
    batch = RADAR_INTEL[start : start + 3]
    
    radar_html = "".join([f'<div class="radar-entry"><span class="radar-tag">■ {i["tag"]}</span><span class="radar-text">{i["msg"]}</span></div>' for i in batch])
    st.markdown(f'<div class="panel-body">{radar_html}</div>', unsafe_allow_html=True)

with c_flux:
    st.markdown('<div class="panel-header" style="color:#10b981; border-color:#10b981;">FLUXO INSTITUCIONAL 24H ($B)</div>', unsafe_allow_html=True)
    # GRÁFICO DE FLUXO (PLOTLY DIRETO - EVITA VÁCUO)
    flux_data = pd.DataFrame({
        "Origem": ["Instituições", "Whales", "RWA", "ISO Bridge", "Retail"],
        "Biliões ($)": [8.4, 6.2, 3.1, 5.5, 1.4]
    })
    fig_flux = px.bar(
        flux_data, x="Biliões ($)", y="Origem", 
        orientation='h', color="Biliões ($)", color_continuous_scale="Viridis",
        text_auto=True
    )
    fig_flux.update_layout(
        template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', font=dict(size=18),
        xaxis_title="Volume Mensal Projetado"
    )
    st.plotly_chart(fig_flux, use_container_width=True)

st.divider()

# ==============================================================================
# 08. CÓRTEX V.MAX (SINGULARIDADE VISUAL)
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

# Mais Gráficos: Distribuição de Dominância
dom_data = pd.DataFrame({"Asset": ["BTC", "ETH", "RWA", "IA", "Outros"], "Dominance": [52, 18, 15, 10, 5]})
fig_dom = px.pie(dom_data, values='Dominance', names='Asset', hole=.4, color_discrete_sequence=px.colors.sequential.Viridis)
fig_dom.update_layout(template="plotly_dark", height=450, title="Dominância de Capital (Março 2026)")
st.plotly_chart(fig_dom, use_container_width=True)

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO JTM (TABELAS GIGANTES)
# ==============================================================================
st.markdown("## 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica extrema.", "BRICS reserva física ouro (Mar 2026)."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "IA Real e Soberania Computacional Total.", "Tesla FSD v15 atinge Nível 5 na UE."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Carris tecnológicos do novo sistema financeiro.", "Fedwire integra XRP como ponte oficial."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos de dados.", "BlackRock BUIDL fund atinge $2.5B."]
]

st.markdown(f"""
<table class="master-table">
    <thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação Técnica</th><th>Prova Social (2026)</th></tr></thead>
    <tbody>
        {''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3;'>{r[4]}</td></tr>" for r in pos_data])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE ÔMEGA (RECUPERADO E EXPANDIDO)
# ==============================================================================
st.markdown("## 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_INFO.values()])

for i, (key, info) in enumerate(ASSET_INFO.items()):
    with tabs[i]:
        c_text, c_vis = st.columns([1.5, 1])
        with c_text:
            st.image(info['img'], width=100)
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
            st.markdown(f"""
            <table class="master-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul><li>Alta Liquidez</li><li>Escassez Matemática</li><li>ISO 20022 Ready</li></ul></td>
                    <td><ul><li>Regulação Fiat</li><li>Volatilidade Cíclica</li></ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold; font-size:1.8rem;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c_vis:
            st.markdown("#### Matriz de Volatilidade vs Retorno (Mar 2026)")
            # Mais Gráficos: Scatter plot de performance
            perf_df = pd.DataFrame({"Asset": [info['name']], "Risk": [25], "Return": [85]})
            fig_perf = px.scatter(perf_df, x="Risk", y="Return", text="Asset", size=[50], color_discrete_sequence=["#10b981"])
            fig_perf.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig_perf, use_container_width=True)
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Integridade de Rede: {info['name']}")

st.divider()

# ==============================================================================
# 11. SIDEBAR & REFRESH (SYNC SOBERANO)
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização Ativa", value=True)
    st.markdown("---")
    st.markdown("### 🔐 CONSELHO SOBERANO")
    st.success("PROTOCOL: TREZOR SAFE 7 ACTIVE")
    st.info(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V71.0 ARCHITECT APEX // MASTER BASE READY</small>
</div>
""", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.refresh_cycle += 1
    st.rerun()
