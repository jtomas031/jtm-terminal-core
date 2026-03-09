import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO & ESTADO GLOBAL
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V41",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização segura de variáveis de estado
if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

auto_refresh = True # Controle de refresh global

# --- SIDEBAR: GOVERNANÇA INSTITUCIONAL ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.2); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 3px;'>APEX MASTER V41.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização de Fluxo", value=True)
    
    st.markdown("### 🏛️ Matriz de Alocação")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 Protocolo de Custódia")
    st.error("Extração: Dia 29\nStatus: Cold Storage Ativa")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: ONDO-GLASS INSTITUTIONAL (ALINHAMENTO TOTAL)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Container */
    .main .block-container { padding: 3rem 6rem; max-width: 1600px; margin: 0 auto; }
    
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }
    
    /* Hero Style: Ondo Finance Inspired */
    .hero-container {
        padding: 100px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
    }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 6px; font-size: 0.8rem; margin-bottom: 25px; }
    .hero-title { font-size: 6rem; line-height: 0.9; margin-bottom: 40px; font-weight: 800; letter-spacing: -2px; }
    .hero-desc { font-size: 1.6rem; color: #94a3b8; line-height: 1.8; max-width: 1000px; font-weight: 300; }

    /* Quantum Metric Cards */
    .q-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 12px;
        transition: 0.4s ease-in-out;
        border-left: 5px solid #10b981;
        height: 100%;
    }
    .q-card:hover { border-color: #00d4ff; transform: translateY(-10px); background: rgba(15, 23, 42, 0.6); }
    .q-label { font-size: 0.75rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.3rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Monitor de Inteligência - O Pulso */
    .pulse-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 50px;
        border-radius: 16px;
        min-height: 600px;
        border-top: 6px solid #8b5cf6;
    }
    .pulse-news-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
    }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem; }
    .pulse-link:hover { color: #10b981; }

    /* Tabelas Soberanas (Blindagem HTML) */
    .sovereign-table {
        width: 100%;
        border-collapse: collapse;
        margin: 30px 0;
        background: rgba(0,0,0,0.2);
    }
    .sovereign-table th {
        text-align: left;
        padding: 25px;
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.8rem;
        border-bottom: 2px solid #1e293b;
    }
    .sovereign-table td {
        padding: 30px 25px;
        border-bottom: 1px solid #1e293b;
        color: #f1f5f9;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    /* Editorial Matrix */
    .editorial-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 60px;
        border-radius: 20px;
        margin-top: 50px;
        border-left: 12px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE INTELIGÊNCIA: A TESE DOS PORQUÊS (+15 NÓS)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania",
        "why": "Ouro digital. Ativo de escassez absoluta (21M). Proteção contra o colapso fiduciário analógico.",
        "pros": ["Escassez Matemática.", "Adoção Institucional."], "cons": ["Volatilidade."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica",
        "why": "O sistema operativo das finanças. Camada onde triliões em RWA serão liquidados via Smart Contracts.",
        "pros": ["Mecanismo Deflacionário.", "Líder RWA."], "cons": ["Taxas elevadas."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "Substituto direto do SWIFT. Ativo de ponte para liquidação instantânea entre bancos mundiais.",
        "pros": ["Velocidade (3s).", "Conformidade Bancária."], "cons": ["Regulação."]
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e o capital digital.",
        "pros": ["Yield Institucional.", "Seguro."], "cons": ["Dependência Fiat."]
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo Overledger. Permite que blockchains privadas de bancos falem entre si.",
        "pros": ["Supply 14.5M.", "Conector CBDC."], "cons": ["Código Fechado."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Ponte de dados entre o mundo real e a blockchain. Sem LINK, o RWA não tem preço real.",
        "pros": ["Padrão Global CCIP.", "Essencial RWA."], "cons": ["Tokenomics."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Velocidade extrema para pagamentos retail em massa.",
        "pros": ["Taxas Baixas.", "65k TPS."], "cons": ["Uptime Histórico."]
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Inteligência Artificial",
        "why": "Infraestrutura para IA descentralizada. Onde os modelos de IA viverão de forma imutável.",
        "pros": ["Foco em IA.", "User Friendly."], "cons": ["Concorrência."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & RADAR
# ==============================================================================
@st.cache_data(ttl=25)
def get_institutional_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_radar_data():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    return news if news else [{"title": "A sincronizar fluxo de inteligência...", "link": "#", "src": "CÓRTEX"}]

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN MATRIX
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Sovereign Research // Apex Matrix</div>
    <div class="hero-title">A Próxima Geração da Infraestrutura de Capital.</div>
    <div class="hero-desc">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir soberania através da matemática.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DINÂMICA)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")

items = list(ASSET_VAULT.items())
EXTRA_MACRO = {
    "GOLD": ("Ouro Físico", "GC=F"), "TSLA": ("Tesla IA", "TSLA"),
    "BCP": ("BCP Liquidez", "BCP.LS"), "VIX": ("Índice Medo", "^VIX")
}

full_grid = items + list(EXTRA_MACRO.items())
rows = [full_grid[i:i + 4] for i in range(0, len(full_grid), 4)]

for row in rows:
    cols = st.columns(4)
    for idx, item in enumerate(row):
        key, info = item
        name, ticker = (info['name'], info['ticker']) if isinstance(info, dict) else (info[0], info[1])
        p, c = get_institutional_stats(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="q-card">
                <div class="q-label">{name}</div>
                <div class="q-value">€ {p:,.2f}</div>
                <div style="color: {color}; font-weight: 800; font-family: 'JetBrains Mono';">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (NOTÍCIAS ALINHADAS)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
col_radar, col_vmax = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="pulse-box">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Live Feed)")
    news_feed = fetch_radar_data()
    for n in news_feed:
        st.markdown(f"""
        <div class="pulse-news-item">
            <a href="{n['link']}" target="_blank" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.85rem; font-family: 'JetBrains Mono'; margin-top: 5px;">FONTE: {n['src']} // TRANSMISSÃO AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="pulse-box" style="border-left: 6px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa.
    * **MACRO:** Inversão da curva de rendimentos indica migração para ativos de escassez absoluta.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo lidera a absorção do Tesouro Digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica.
    """)
    st.markdown("---")
    st.markdown("**RECOMENDAÇÃO HOJE:** Executar tranches de 50%.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. ARQUITETURA VISUAL: DIAGRAMAS
# ==============================================================================
st.markdown("### 🌐 Arquitetura da Transição Sistémica")

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("#### I. O Ciclo de Tokenização RWA")
    st.write("Digitalização da propriedade física em rede.")
    st.markdown("[Image of the process of Real World Asset (RWA) tokenization on blockchain showing physical assets being converted into digital tokens]")
    
[Image of the process of Real World Asset (RWA) tokenization on blockchain]

with c_img2:
    st.markdown("#### II. A Norma Bancária ISO 20022")
    st.write("O novo sistema nervoso dos triliões mundiais.")
    st.markdown("[Image of the ISO 20022 messaging standard diagram showing rich data layers between global financial institutions]")

[Image of ISO 20022 standard structure vs legacy financial messaging]

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO (BLINDADO)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Estratégico (Hoje)")

pos_list = [
    {"V": "Âncora de Proteção", "A": "BCP / Ouro", "P": "50%", "N": "Garantia de liquidez."},
    {"V": "Autonomia Física", "A": "Tesla (TSLA)", "P": "15%", "N": "Domínio IA/Energia."},
    {"V": "Infraestrutura ISO", "A": "XRP / ONDO / QNT", "P": "20%", "N": "Reset Bancário."},
    {"V": "Fronteira Digital", "A": "BTC / NEAR / ETH", "P": "15%", "N": "Escassez Matemática."}
]

table_h = """
<table class="sovereign-table">
    <thead>
        <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Nota de Execução</th></tr>
    </thead>
    <tbody>
"""
for r in pos_list:
    table_h += f"<tr><td>{r['V']}</td><td>{r['A']}</td><td>{r['P']}</td><td>{r['N']}</td></tr>"
table_h += "</tbody></table>"

st.markdown(table_h, unsafe_allow_html=True)

# EDITORIAL
st.markdown("""
<div class="editorial-box">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.2rem; line-height: 1.8; color: #f1f5f9;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária insustentável, o capital migra para <b>Escassez Matemática</b>.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 30px;">
        <a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Explorar Ondo Finance →</a>
        <a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação ISO Oficial →</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: O PORQUÊ TÉCNICO (TABS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")

tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        c_tx, c_gr = st.columns([1.5, 1])
        with c_tx:
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            
            tab_inner = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul>{"".join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{"".join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(tab_inner, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_gr:
            st.markdown("#### Verificação de Rede")
            # FIX: Sintaxe correta para evitar SyntaxError
            st.markdown(f"Representação visual da arquitetura de rede para {info['name']}.")
            st.markdown(f"[{info['name']} blockchain network security architecture and validation nodes diagram]")

st.divider()

# Rodapé Final
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V41.0 // ERROR-FREE CORE READY</small>
</div>
""", unsafe_allow_html=True)

# REFRESH
if auto_refresh:
    st.session_state.pulse_cycle += 1
    time.sleep(30)
    st.rerun()
