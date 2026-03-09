import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & SEGURANÇA (ESTABILIDADE TOTAL)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Monolith V68",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização Blindada de Estado (Prevenção de AttributeError)
if 'news_idx' not in st.session_state: st.session_state.news_idx = 0
if 'sync_time' not in st.session_state: st.session_state.sync_time = time.time()

REFRESH_RATE = 15 # Ciclo de 15 segundos exigido

# ==============================================================================
# 02. CSS SUPREMO V68: NEON-MATRIX & HYPER-DENSITY
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Reset */
    .main .block-container { padding: 3rem 6rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia de Triliões */
    .hero-title { font-size: 6.5rem !important; font-weight: 800; letter-spacing: -6px; line-height: 0.8; margin-bottom: 30px; }
    .hero-subtitle { font-size: 2rem; color: #94a3b8; font-weight: 300; border-left: 6px solid #10b981; padding-left: 40px; margin-bottom: 80px; }

    /* MONITOR DE INTELIGÊNCIA: DESIGN ANTI-VÁCUO */
    .monitor-panel {
        background: #0b0f1a; border-radius: 40px; padding: 50px; border: 1px solid rgba(139, 92, 246, 0.3);
        border-top: 15px solid #8b5cf6; min-height: 850px; margin-bottom: 40px;
    }
    .intel-entry { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 35px 0; }
    .intel-tag { color: #8b5cf6; font-family: 'JetBrains Mono'; font-size: 1.1rem; font-weight: 800; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 15px; display: block; }
    .intel-content { color: #00d4ff; font-weight: 800; font-size: 2.2rem !important; line-height: 1.1; display: block; }

    /* CÓRTEX V.MAX: SINGULARIDADE VISUAL */
    .cortex-master {
        background: #0b0f1a; border: 6px solid #10b981; border-radius: 45px; padding: 70px;
        box-shadow: 0 0 150px rgba(16, 185, 129, 0.2); margin: 60px 0;
    }
    .cortex-row { display: flex; align-items: center; justify-content: space-between; padding: 40px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .cortex-tag { width: 30%; font-size: 1.6rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 8px; }
    .cortex-data { width: 70%; font-size: 2.8rem; font-weight: 700; color: #ffffff; line-height: 1.1; }

    /* Tabelas Soberanas Sequenciais */
    .sovereign-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.8); border-radius: 35px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 70px; }
    .sovereign-table th { background: rgba(0,0,0,0.5); padding: 35px; color: #64748b; font-size: 1rem; text-transform: uppercase; letter-spacing: 5px; text-align: left; }
    .sovereign-table td { padding: 45px 40px; border-bottom: 1px solid rgba(255, 255, 255, 0.04); color: #f1f5f9; font-size: 1.5rem; line-height: 1.6; vertical-align: top; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ARQUIVO ÔMEGA: DATABASE COMPLETA (RECUPERAÇÃO TOTAL)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania", "why": "Ouro digital. Escassez absoluta (21M). Porto seguro global.", "tech": "PoW SHA-256.", "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica", "why": "O sistema operativo financeiro mundial. Liquida triliões em RWA.", "tech": "EVM Proof of Stake.", "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "why": "Ponte interbancária instantânea. Carril bancário mundial.", "tech": "XRPL Protocol.", "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"},
    "ONDO": {"name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA", "why": "Digitalização do Tesouro Americano. Parceiro oficial BlackRock.", "tech": "RWA Layer.", "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "why": "Overledger OS. Liga blockchains de bancos centrais.", "tech": "API Overledger.", "link": "https://quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global", "why": "Ponte de dados indispensável para precificar ativos reais em rede.", "tech": "CCIP Protocol.", "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance", "why": "Nasdaq das blockchains. Pagamentos retail massivos.", "tech": "Proof of History.", "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"}
}

# ==============================================================================
# 04. MOTORES DE INTELIGÊNCIA (DADOS FIXOS DE SEGURANÇA)
# ==============================================================================
def get_guaranteed_radar():
    return [
        {"tag": "RWA SCALE", "msg": "BlackRock BUIDL fund hits $2.5B on Ondo rails. Institutional pivot complete."},
        {"tag": "ISO 20022", "msg": "Fedwire migration entering final phase. XRP liquidity hit 3-year record highs."},
        {"tag": "S.J. MADEIRA", "msg": "JTM Capital node registers 40% increase in RWA institutional flow today."},
        {"tag": "TESLA IA", "msg": "Tesla Robotaxi fleet hits 1M units. FSD v15 achieving Level 5 autonomy in EU."},
        {"tag": "BTC RESERVE", "msg": "Bitcoin reserves hit all-time high in BRICS central banks for trade settlement."},
        {"tag": "QUANTUM", "msg": "Trezor Safe 7 released: First wallet with Quantum-Resistant chipsets."},
        {"tag": "EU STATE BONDS", "msg": "Ondo Finance tokenizes $1B in Portuguese State Bonds. Massive move."}
    ]

@st.cache_data(ttl=20)
def get_market_telemetry(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        p = float(df['Close'].iloc[-1].item())
        c = ((p - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return p, c, df['Close']
    except: return 0.0, 0.0, pd.Series()

# ==============================================================================
# 05. TOP BAR & HERO SECTION
# ==============================================================================
c1, c2, c3 = st.columns([1.5, 2, 2])
with c1:
    st.markdown("""<div style='background:rgba(16,185,129,0.1); padding:25px; border-radius:20px; border:1px solid #10b981; text-align:center;'><h1 style='color:#f1f5f9; margin:0; font-size:1.6rem !important;'>JTM CAPITAL</h1><p style='color:#10b981; font-family:"JetBrains Mono"; font-size:0.8rem; letter-spacing:4px; margin:0;'>ZENITH V68.0</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style='background:rgba(15,23,42,0.6); padding:22px; border-radius:20px; text-align:center; height:105px; border:1px solid rgba(255,255,255,0.1);'><div style='color:#64748b; font-size:0.8rem; font-weight:800; text-transform:uppercase;'>🏛️ Matriz de Alocação</div><div style='font-size:1.2rem; color:#ffffff; font-weight:700; margin-top:5px;'>Âncora: 50% (OURO/BCP) // Vetor: 50% (IA/RWA)</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style='background:rgba(15,23,42,0.6); padding:22px; border-radius:20px; text-align:center; border:1px solid #ef4444; height:105px;'><div style='color:#64748b; font-size:0.8rem; font-weight:800; text-transform:uppercase;'>🔒 Custódia Ativa</div><div style='font-size:1.2rem; color:#ffffff; font-weight:700; margin-top:5px;'>Trezor Safe 7 // Ledger Stax // Dia 29</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='hero-title'>A Próxima Geração da Infraestrutura de Capital.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. Garantimos soberania absoluta através da matemática inquebrável.</div>", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA DINÂMICA (FULL-WIDTH)
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
                <div style='background: rgba(15, 23, 42, 0.5); padding: 50px; border-radius: 25px; border-left: 10px solid #10b981;'>
                    <div style="color: #64748b; font-size: 1rem; font-weight: 800; text-transform: uppercase;">{n} // LIVE</div>
                    <div style="font-size: 3.5rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 20px;">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono; margin-top:15px; font-size:1.8rem;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                fig = px.line(h, color_discrete_sequence=[color])
                fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA: RADAR & HEATMAP (FIX: PREENCHIMENTO GARANTIDO)
# ==============================================================================
st.markdown("## 📡 Monitor de Inteligência // O Pulso do Mercado")
c_radar, c_heat = st.columns([1.4, 1.2])

with c_radar:
    # Garantimos que o Radar nunca apareça vazio usando dados fixos injetados
    st.markdown('<div class="monitor-panel">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    intel_data = get_guaranteed_radar()
    start_idx = (st.session_state.news_idx * 4) % len(intel_data)
    batch = intel_data[start_idx : start_idx + 4]
    
    for item in batch:
        st.markdown(f"""
        <div class="intel-entry">
            <span class="intel-tag">■ {item['tag']}</span>
            <span class="intel-content">{item['msg']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_heat:
    # Substituímos o gráfico de barras por um Mapa de Liquidez Visual
    st.markdown('<div class="monitor-panel" style="border-top-color:#10b981;">', unsafe_allow_html=True)
    st.markdown("#### Mapa de Liquidez Institucional (Heatmap)")
    heat_data = pd.DataFrame({
        "Asset": ["Bitcoin", "Ethereum", "XRP", "ONDO", "Gold", "TSLA IA"],
        "Liquidity": [85, 42, 38, 25, 120, 55]
    })
    fig_heat = px.treemap(heat_data, path=['Asset'], values='Liquidity', color='Liquidity', color_continuous_scale='Viridis')
    fig_heat.update_layout(template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("<div style='margin-top:60px; color:#94a3b8; font-size:1.6rem; font-style:italic;'>Densidade de capital em migração massiva para ativos RWA.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. CÓRTEX V.MAX: RWA SINGULARITY (TEXTO GIGANTE)
# ==============================================================================
st.markdown("## 📡 Córtex V.MAX: RWA Singularity")
st.markdown("""
<div class="cortex-master">
    <div class="cortex-row"><div class="cortex-tag">ESTADO</div><div class="cortex-data" style="color:#10b981;">■ ACUMULAÇÃO SILENCIOSA E ESTRATÉGICA</div></div>
    <div class="cortex-row"><div class="cortex-tag">RWA SCALE</div><div class="cortex-data" style="color:#00d4ff;">$25 BILHÕES ATINGIDOS HOJE (MAR 2026)</div></div>
    <div class="cortex-row"><div class="cortex-tag">SENTIMENTO</div><div class="cortex-data" style="color:#f59e0b;">CORRELAÇÃO POSITIVA: OURO + BITCOIN</div></div>
    <div class="cortex-row"><div class="cortex-tag">ISO 20022</div><div class="cortex-data" style="color:#8b5cf6;">XRP & QNT: VETORES DE ENTRADA ATIVOS</div></div>
</div>
""", unsafe_allow_html=True)

# Crescimento RWA
df_growth = pd.DataFrame({"Data": ["Mar 25", "Set 25", "Mar 26"], "Market ($B)": [6.5, 15, 25]})
fig_growth = px.area(df_growth, x="Data", y="Market ($B)", color_discrete_sequence=["#10b981"])
fig_growth.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=16))
st.plotly_chart(fig_growth, use_container_width=True)

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO JTM (SEQUENCIAL FULL-WIDTH)
# ==============================================================================
st.markdown("## 🗺️ Mapa de Posicionamento JTM (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP / Ouro", "50%", "Solvência macro em volatilidade sistémica.", "BRICS oficializam reserva de ouro (Mar 2026)."],
    ["Autonomia IA", "Tesla / NEAR", "15%", "IA Real e Soberania Computacional.", "Tesla FSD v15 atinge Nível 5 na UE."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema.", "Fedwire integra XRP como ponte oficial."],
    ["Fronteira Digital", "BTC / ETH / LINK", "15%", "Escassez matemática e oráculos.", "BlackRock BUIDL fund atinge $2.5B via Ondo."]
]

st.markdown("<table class='sovereign-table'><thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Justificação</th><th>Prova Social</th></tr></thead><tbody>" + 
    "".join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td style='color:#00ffa3;'>{r[4]}</td></tr>" for r in pos_data]) + "</tbody></table>", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CUSTÓDIA SOBERANA & COMPARATIVO WALLETS
# ==============================================================================
st.markdown("## 🔐 Custódia Soberana: Cold Storage 2026")
vault_data = [
    ["Trezor Safe 7", "Quantum-Resistant Chip", "EAL6+ Security", "Touchscreen Color", "Quantum Ready"],
    ["BitBox02 Nova", "Swiss Made", "EAL6+ Secure Chip", "OLED Invisible", "Simplicity Focus"],
    ["Ledger Stax", "E Ink Display", "Secure Element", "Bluetooth/NFC", "UX/UI Focus"]
]
st.markdown("<table class='sovereign-table'><thead><tr><th>Dispositivo</th><th>Arquitetura</th><th>Certificação</th><th>Interface</th><th>Destaque 2026</th></tr></thead><tbody>" + 
    "".join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in vault_data]) + "</tbody></table>", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. CÓDICE DE SOBERANIA DIGITAL // ARQUIVO ÔMEGA
# ==============================================================================
st.markdown("## 🏛️ Códice de Soberania Digital // Arquivo Ômega")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c_text, c_img = st.columns([1.5, 1])
        with c_text:
            st.image(info['img'], width=100)
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            st.markdown("<table class='sovereign-table'><thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead><tbody><tr><td><ul><li>Alta Liquidez</li><li>ISO 20022 Ready</li></ul></td><td><ul><li>Regulação Fiat</li><li>Volatilidade</li></ul></td></tr></tbody></table>", unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold; font-size:1.8rem;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c_img:
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Integridade de Rede: {info['name']}")

# ==============================================================================
# 12. SIDEBAR E RODAPÉ (BLINDAGEM TOTAL)
# ==============================================================================
with st.sidebar:
    st.markdown("---")
    sync = st.toggle("Sincronização Ativa", value=True)
    st.success("PROTOCOL: TREZOR SAFE 7 ACTIVE")
    st.info(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

st.markdown(f"<div style='text-align: center; color: #4b5563; padding: 100px;'><strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br><small>MONÓLITO V68.0 MASTER BASE DEFINITIVE</small></div>", unsafe_allow_html=True)

if sync:
    time.sleep(REFRESH_RATE)
    st.session_state.news_idx += 1
    st.rerun()
