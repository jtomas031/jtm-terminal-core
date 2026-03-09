import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & INICIALIZAÇÃO (FIX: NAMEERROR)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Master V46",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização global das variáveis de controle (Blinda o erro do auto_refresh)
if 'cycle_count' not in st.session_state:
    st.session_state.cycle_count = 0

auto_refresh = True  # Definido globalmente no início

# --- SIDEBAR: CONSELHO DE GOVERNANÇA (DESIGN DE ELITE) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 4px;'>OMNIPOTENT CORE V46</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização Ativa", value=True)
    
    st.markdown("### 🏛️ Matriz de Alocação")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 Segurança")
    st.error("Protocolo: TREZOR COLD STORAGE\nExtração: DIA 29")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: MATRIX-ONDO HYBRID (ESTÉTICA BLINDADA)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 3rem 6rem; max-width: 1600px; margin: 0 auto; }
    .stApp { background-color: #010409; color: #f1f5f9; font-family: 'Inter', sans-serif; background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%); }
    
    /* Hero */
    .hero-panel { padding: 100px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 60px; }
    .hero-title { font-size: 6rem; font-weight: 800; line-height: 0.9; letter-spacing: -2px; }
    .hero-desc { font-size: 1.6rem; color: #94a3b8; line-height: 1.7; max-width: 1000px; font-weight: 300; }

    /* Cards */
    .q-card { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); padding: 35px; border-radius: 12px; transition: 0.4s; border-left: 5px solid #10b981; height: 100%; }
    .q-card:hover { transform: translateY(-10px); border-color: #00d4ff; }
    .q-price { font-size: 2.2rem; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Pulse Box News */
    .pulse-box { background: #0b0f1a; border: 1px solid #1e293b; padding: 40px; border-radius: 20px; min-height: 550px; border-top: 5px solid #8b5cf6; }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 20px 0; }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.2rem; }

    /* Tables */
    .sovereign-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: rgba(0,0,0,0.2); }
    .sovereign-table th { text-align: left; padding: 20px; color: #64748b; font-size: 0.8rem; border-bottom: 2px solid #1e293b; text-transform: uppercase; }
    .sovereign-table td { padding: 25px 20px; border-bottom: 1px solid #1e293b; font-size: 1.1rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS: O ARQUIVO ETERNO (15+ MOEDAS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania",
        "why": "Ouro digital. Ativo de escassez absoluta finita (21M). Proteção central contra o colapso fiduciário.",
        "tech": "Rede PoW imutável. Reserva de valor mundial.",
        "pros": ["Escassez 21M", "Adoção Institucional"], "cons": ["Volatilidade", "Lentidão L1"],
        "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Liquidação",
        "why": "O sistema operativo das finanças. Onde os triliões em RWA serão liquidados via Smart Contracts.",
        "pros": ["Deflacionário", "Líder RWA"], "cons": ["Gas fees", "L2 Fragmentação"],
        "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022",
        "why": "Substituto do SWIFT. Ativo de ponte mandatório para liquidação bancária instantânea.",
        "pros": ["Velocidade 3s", "Conformidade"], "cons": ["Controlo Ripple Labs"],
        "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Líder RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e a Blockchain.",
        "pros": ["Yield Real", "BlackRock Link"], "cons": ["Dependência Fiat"],
        "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "Overledger OS. Permite que as blockchains dos bancos falem entre si.",
        "pros": ["Supply 14.5M", "CBDC Ready"], "cons": ["Código Fechado"],
        "link": "https://www.quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Global",
        "why": "A ponte de dados. Essencial para precificar ativos do mundo real em rede.",
        "pros": ["Padrão CCIP", "Indispensável"], "cons": ["Tokenomics Lento"],
        "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para pagamentos massivos em milissegundos.",
        "pros": ["65k TPS", "Taxas Baixas"], "cons": ["Uptime"],
        "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Cérebro IA",
        "why": "Infraestrutura para IA descentralizada e modelos de inteligência soberanos.",
        "pros": ["Foco em IA", "User Friendly"], "cons": ["Concorrência"],
        "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Corp",
        "why": "Governada por Google e IBM. Padrão enterprise para triliões de dados.",
        "pros": ["Hashgraph", "Segurança"], "cons": ["Centralização"],
        "link": "https://hedera.com/", "img": "https://cryptologos.cc/logos/hedera-hbar-logo.png"
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "GPU IA",
        "why": "Poder de GPU descentralizado para IA. A Render fornece o hardware da nova economia.",
        "pros": ["Nvidia Link", "Utility"], "cons": ["Semicondutores"],
        "link": "https://render.x.ai/", "img": "https://cryptologos.cc/logos/render-token-rndr-logo.png"
    },
    "AVAX": {
        "name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets RWA",
        "why": "Customização para bancos (JP Morgan). Redes privadas para ativos digitais.",
        "pros": ["Subnets", "Foco RWA"], "cons": ["Adoção L1"],
        "link": "https://www.avax.network/", "img": "https://cryptologos.cc/logos/avalanche-avax-logo.png"
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO",
        "why": "Inclusão financeira e pagamentos transfronteiriços de baixo custo.",
        "pros": ["MoneyGram Link", "Rápido"], "cons": ["Sombra do XRP"],
        "link": "https://stellar.org/", "img": "https://cryptologos.cc/logos/stellar-xlm-logo.png"
    },
    "ALGO": {
        "name": "Algorand", "ticker": "ALGO-EUR", "role": "Padrão CBDC",
        "why": "Segurança matemática extrema para emissão de moedas digitais estatais.",
        "pros": ["Tecnologia Turing", "Eco"], "cons": ["Marketing"],
        "link": "https://algorand.co/", "img": "https://cryptologos.cc/logos/algorand-algo-logo.png"
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Infra IA",
        "why": "Abstração de conta e inteligência artificial nativa.",
        "pros": ["Escala Sharding", "AI Lab"], "cons": ["Adoção"],
        "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"
    },
    "VET": {
        "name": "VeChain", "ticker": "VET-EUR", "role": "Logística Real",
        "why": "Tokenização de cadeias de suprimento e ativos físicos industriais.",
        "pros": ["Uso Real", "Walmart Link"], "cons": ["Economia do Token"],
        "link": "https://www.vechain.org/", "img": "https://cryptologos.cc/logos/vechain-vet-logo.png"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & MERCADO
# ==============================================================================
@st.cache_data(ttl=30)
def get_market_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_pulse():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    return news

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN MATRIX
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div style="color:#10b981; font-weight:800; letter-spacing:6px; margin-bottom:20px;">SOVEREIGN ARCHIVE // SINGULARITY</div>
    <h1 class="hero-title">A Próxima Geração da Infraestrutura de Capital.</h1>
    <p class="hero-desc">Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
    A JTM Capital opera na fronteira da norma ISO 20022 para garantir soberania através da matemática inquebrável.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA (GRELHA DE 16 NÓS - SEM ESPAÇOS VAZIOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
items = list(ASSET_DOCS.items())
EXTRA = [
    ("GOLD", {"name": "Ouro Físico", "ticker": "GC=F", "role": "Âncora"}),
    ("TSLA", {"name": "Tesla IA", "ticker": "TSLA", "role": "Autonomia"}),
    ("BCP", {"name": "BCP Liquidez", "ticker": "BCP.LS", "role": "Fiat"}),
    ("VIX", {"name": "Índice Medo", "ticker": "^VIX", "role": "Macro"})
]
full_display = items + EXTRA

for i in range(0, len(full_display), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(full_display):
            key, val = full_display[idx]
            p, c = get_market_telemetry(val['ticker'])
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div class="q-card">
                    <div style="color:#64748b; font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:2px;">{val['name']} // {val['role']}</div>
                    <div class="q-price">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (NOTÍCIAS REAIS)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_news, c_vmax = st.columns([2, 1])

with c_news:
    st.markdown('<div class="pulse-box" style="height:600px; overflow-y:auto;">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Live Feed)")
    news_list = fetch_pulse()
    for n in news_list:
        st.markdown(f"**[{n['src']}]** [{n['title']}]({n['link']})")
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

with c_vmax:
    st.markdown('<div class="pulse-box" style="height:600px; border-left: 10px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa e Estratégica.
    * **MACRO:** Inversão da curva indica fuga para ativos de escassez física.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo lidera o tesouro digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada antes do reset.
    """)
    st.markdown("---")
    st.success("**RECOMENDAÇÃO HOJE:** Manter tranches de 50%.")
    st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=400", caption="Análise de Rede")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO & DIAGRAMAS
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Recomendado (Ciclo 2026)")
pos_data = [
    ["Âncora de Proteção", "BCP (Liquidez) / Ouro", "50%", "Garantia de solvência macro."],
    ["Autonomia Física", "Tesla (TSLA)", "15%", "Domínio IA e Energia Soberana."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Reset Bancário Mundial."],
    ["Fronteira Digital", "BTC / NEAR / ETH", "15%", "Escassez Matemática Absoluta."]
]

t_html = "<table class='sovereign-table'><thead><tr><th>Vetor</th><th>Ativos</th><th>Alocação</th><th>Nota</th></tr></thead><tbody>"
for r in pos_data:
    t_html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
t_html += "</tbody></table>"
st.markdown(t_html, unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(0, 212, 255, 0.05); padding: 40px; border-radius: 20px; border-left: 10px solid #00d4ff; margin-top: 40px;">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.2rem; line-height: 1.8;">O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital migra para a <b>Escassez Matemática</b>.
    A tokenização de ativos reais (RWA) via Ondo Finance e o novo padrão ISO 20022 são os carris por onde os próximos triliões vão fluir.</p>
    <div style="display:flex; gap:30px; margin-top:20px;">
        <a href="https://ondo.finance/" style="color:#10b981; font-weight:bold; text-decoration:none;">Explorar Ondo →</a>
        <a href="https://ripple.com/" style="color:#10b981; font-weight:bold; text-decoration:none;">Ver Sistema Ripple →</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. CÓDICE DE ATIVOS SOBERANOS (TESE TOTAL)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.image(info['img'], width=80)
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            
            v_html = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS</th><th>🔴 RISCOS</th></tr></thead>
                <tbody><tr>
                    <td><ul>{"".join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{"".join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(v_html, unsafe_allow_html=True)
            st.markdown(f"<br><a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with c2:
            st.markdown("#### Verificação de Rede")
            st.image("https://images.unsplash.com/photo-1642104704074-907c0698cbd9?auto=format&fit=crop&q=80&w=500", caption="Arquitetura ISO 20022")
            st.info(f"Nó Ativo: {info['name']} Sovereign Hub")

st.divider()

# ==============================================================================
# 10. GLOSSÁRIO & MANIFESTO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física convertida em código digital imutável.")
    st.write("**VIX:** Índice de pânico institucional. Oportunidade no sangue.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais.")
    st.write("**Settlement:** Liquidação matemática final e instantânea.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas offline.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão sobre os ativos.")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    <em>"A soberania é o resultado da substituição do medo pela matemática."</em><br>
    <small>V46.0 // STABLE GENESIS READY</small>
</div>
""", unsafe_allow_html=True)

# --- REFRESH SOBERANO ---
if auto_refresh:
    time.sleep(30)
    st.rerun()
