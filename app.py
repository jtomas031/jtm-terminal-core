import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE INTELIGÊNCIA & ESTADO GLOBAL
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Institutional Apex",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis Globais (Prevenção de NameError/IndexError)
if 'news_cycle' not in st.session_state:
    st.session_state.news_cycle = 0

auto_refresh = True  # Valor padrão fora de blocos de contexto

# ==============================================================================
# 02. CSS INSTITUCIONAL "ONDO STYLE" (AESTHETIC V35)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Configuração Geral do Workspace */
    .main .block-container { padding: 3rem 6rem; max-width: 1440px; margin: 0 auto; }
    
    /* Fundo Obsidian Deep */
    .stApp { 
        background-color: #030712; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -1.5px; font-family: 'Inter', sans-serif; }

    /* Painel Hero Estilo Gestão de Património */
    .hero-container {
        padding: 120px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
        animation: fadeIn 1.5s ease;
    }
    .hero-tag { 
        color: #10b981; 
        text-transform: uppercase; 
        font-weight: 800; 
        letter-spacing: 4px; 
        font-size: 0.85rem; 
        margin-bottom: 25px;
    }
    .hero-title { font-size: 6rem; line-height: 0.9; margin-bottom: 40px; }
    .hero-desc { font-size: 1.6rem; color: #94a3b8; line-height: 1.6; max-width: 900px; font-weight: 300; }

    /* Cartões de Ativos (Glassmorphism Minimalista) */
    .asset-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 12px;
        transition: 0.4s ease;
        height: 100%;
    }
    .asset-card:hover { border-color: #10b981; background: rgba(15, 23, 42, 0.8); transform: translateY(-5px); }
    .asset-label { color: #64748b; font-size: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 2px; }
    .asset-price { font-size: 2.4rem; font-weight: 800; color: #ffffff; margin: 15px 0; font-family: 'Rajdhani'; }

    /* News Box Alinhada (The Pulse) */
    .news-monitor {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 45px;
        border-radius: 16px;
        height: 600px;
        overflow-y: auto;
    }
    .news-entry {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
    }
    .news-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem; }
    .news-link:hover { color: #10b981; }

    /* Tabelas Blindadas Style Institutional */
    .sovereign-table {
        width: 100%;
        border-collapse: collapse;
        margin: 30px 0;
    }
    .sovereign-table th {
        text-align: left;
        padding: 25px;
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.85rem;
        border-bottom: 2px solid #1e293b;
    }
    .sovereign-table td {
        padding: 30px 25px;
        border-bottom: 1px solid #1e293b;
        color: #f1f5f9;
        font-size: 1.15rem;
        line-height: 1.8;
    }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS: PORQUÊ CADA NÓ? (DATABASE EXPANDIDA)
# ==============================================================================
CORTEX_INTEL = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Escassez Absoluta",
        "why": "O padrão-ouro digital. Único ativo com limite matemático de 21 milhões, livre de controlo governamental.",
        "pros": ["Reserva de valor imutável.", "Adoção por fundos de elite."], "cons": ["Volatilidade.", "Lentidão L1."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica",
        "why": "O sistema operativo das finanças globais. Onde os triliões em RWA serão liquidados.",
        "pros": ["Líder em Smart Contracts.", "Mecanismo deflacionário."], "cons": ["Custos de rede (Gas)."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022",
        "why": "Substituto do SWIFT. Ativo de liquidação imediata para bancos centrais e CBDCs.",
        "pros": ["Liquidez instantânea (3s).", "Parcerias bancárias."], "cons": ["Controlo Ripple Labs."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do tesouro americano. A ponte institucional direta para a BlackRock.",
        "pros": ["Yield institucional seguro.", "Líder de mercado RWA."], "cons": ["Risco regulatório fiat."]
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "Conecta as blockchains dos bancos mundiais através do sistema operativo Overledger.",
        "pros": ["Supply ultra-escassa (14M).", "Foco 100% B2B."], "cons": ["Código proprietário."]
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas Globais",
        "why": "Focada em pagamentos internacionais ultrarrápidos para o retalho e instituições.",
        "pros": ["Taxas nulas.", "Parceria IBM/MoneyGram."], "cons": ["Concorrência direta XRP."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Execução Massiva",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais mundial.",
        "pros": ["65k Transações por segundo.", "Taxas mínimas."], "cons": ["Uptime histórico."]
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Governada pela Google e Dell. A infraestrutura de eleição para o setor corporativo Fortune 500.",
        "pros": ["Tecnologia Hashgraph.", "Segurança absoluta."], "cons": ["Centralização do conselho."]
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "Infra de IA",
        "why": "Processamento de GPU descentralizado. A inteligência artificial precisa de hardware que a Render fornece.",
        "pros": ["Parceria Apple/Nvidia.", "Boom da IA."], "cons": ["Dependência de chips."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "A ponte de dados. Sem LINK, a blockchain não sabe o preço de nada no mundo real.",
        "pros": ["Padrão global CCIP.", "Essencial para RWA."], "cons": ["Complexidade técnica."]
    },
    "ALGO": {
        "name": "Algorand", "ticker": "ALGO-EUR", "role": "Finanças Puras",
        "why": "Rede carbono negativo, escolhida para emissão de CBDCs devido à sua segurança matemática.",
        "pros": ["Silvio Micali (Turing Award).", "Velocidade."], "cons": ["Marketing inferior."]
    },
    "AVAX": {
        "name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets Bancárias",
        "why": "Permite que bancos (JP Morgan) criem redes privadas seguras e customizadas.",
        "pros": ["Altamente customizável.", "Foco RWA."], "cons": ["Adoção institucional lenta."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=25)
def get_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_pulse_news():
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
# 05. HERO SECTION: MANIFESTO JTM (ONDO STYLE)
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">JTM Capital // Research & Sovereignty</div>
    <div class="hero-title">A Nova Infraestrutura do Capital Global.</div>
    <div class="hero-desc">
        Monitorizamos a convergência entre ativos do mundo real (RWA) e redes descentralizadas de alta performance. 
        Operamos na fronteira da norma ISO 20022 para garantir que o seu património está ancorado no futuro da liquidez bancária.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. MONITOR DE LIQUIDEZ (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("### 🏦 Telemetria de Ativos Soberanos")

# Motor de Grelha Inteligente (Prevenção de IndexError)
items = list(CORTEX_INTEL.items())
rows = [items[i:i + 4] for i in range(0, len(items), 4)]

for row in rows:
    cols = st.columns(4)
    for i, (symbol, info) in enumerate(row):
        p, c = get_stats(info['ticker'])
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[i]:
            st.markdown(f"""
            <div class="asset-card">
                <div class="asset-label">{info['name']} // {info['role']}</div>
                <div class="asset-price">€ {p:,.2f}</div>
                <div style="color: {color}; font-weight: 800; font-family: JetBrains Mono;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (NOTÍCIAS ALINHADAS)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
col_radar, col_vmax = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="news-monitor">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global")
    news_items = fetch_pulse_news()
    if news_items:
        for item in news_items:
            st.markdown(f"""
            <div class="news-entry">
                <a href="{item['link']}" target="_blank" class="news-link">■ {item['title']}</a>
                <div style="color: #64748b; font-size: 0.85rem; margin-top: 8px;">FONTE: {item['src']} // AO VIVO</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("A sincronizar com as frequências de liquidez globais...")
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="news-monitor" style="border-left: 6px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação em Tranches.
    * **LIQUIDEZ:** Observamos saída massiva de obrigações fiduciárias para Ouro e BTC.
    * **RWA:** ONDO lidera a absorção institucional de liquidez do Tesouro Americano.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica antes do reset bancário.
    """)
    st.markdown("---")
    st.markdown("**RECOMENDAÇÃO HOJE:** Manter 50% em Âncora Física (BCP/OURO) e 50% em Vetores de Crescimento.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO E EDITORIAL
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Estratégico (Ciclo Atual)")

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP (Caixa) / Ouro", "Posição": "50%", "Nota": "Garantia de liquidez."},
    {"Setor": "Autonomia Física", "Ativos": "Tesla (TSLA)", "Posição": "15%", "Nota": "Domínio IA/Energia."},
    {"Setor": "Infraestrutura ISO", "Ativos": "XRP / ONDO / QNT", "Posição": "20%", "Nota": "Reset Bancário mundial."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Posição": "15%", "Nota": "Escassez absoluta."}
]

st.markdown("""
<table class="sovereign-table">
    <thead>
        <tr><th>Setor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Justificação de Execução</th></tr>
    </thead>
    <tbody>
""", unsafe_allow_html=True)
for r in pos_data:
    st.markdown(f"<tr><td>{r['Setor']}</td><td>{r['Ativos']}</td><td>{r['Posição']}</td><td>{r['Nota']}</td></tr>", unsafe_allow_html=True)
st.markdown("</tbody></table>", unsafe_allow_html=True)

# EDITORIAL: O PORQUÊ DE TUDO (COM LINKS E DIAGRAMAS)
st.markdown("""
<div class="news-monitor" style="height: auto; margin-top: 40px; border-left: 8px solid #00d4ff;">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p>O mercado global está a atravessar um ponto de inflexão. Com a inflação persistente e a dívida pública em níveis insustentáveis, o capital de elite está a migrar para redes que oferecem <b>Escassez Matemática</b> e <b>Utilidade Institucional</b>.</p>
    
    <div style="display: flex; gap: 40px; margin: 40px 0;">
        <div style="flex: 1;">
            <p><b>1. RWA (Real World Assets):</b> Estamos a observar a maior transferência de riqueza da história. Ativos ilíquidos estão a ser tokenizados para permitir liquidez 24/7. 
            <br><a style="color:#00d4ff;" href="https://ondo.finance/">Explorar Ecossistema Ondo →</a></p>
        </div>
        <div style="flex: 1;">
            <p><b>2. ISO 20022:</b> A norma bancária mandatória para CBDCs. Quem não detém os carris (XRP/QNT) desta rede, estará fora do sistema.
            <br><a style="color:#00d4ff;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação Oficial ISO →</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# DIAGRAMA TÉCNICO
st.markdown("### Arquitetura de Fluxo: ISO 20022 & RWA")
st.write("Abaixo, o diagrama explicativo da transição do sistema SWIFT legado para a infraestrutura de ativos digitais.")
st.markdown("[Image of a technical flowchart showing the transition from legacy SWIFT MT messages to ISO 20022 XML messages using XRP as a bridge asset for bank liquidity]")

st.divider()

# ==============================================================================
# 09. CÓDICE DE ATIVOS SOBERANOS (ANÁLISE PROFUNDA)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // Porquê cada nó?")
tabs = st.tabs([f"🏛️ {v['name']}" for v in CORTEX_INTEL.values()])

for i, (key, info) in enumerate(CORTEX_INTEL.items()):
    with tabs[i]:
        c_txt, c_img = st.columns([1.5, 1])
        with c_txt:
            st.markdown(f"#### Tese: {info['role']}")
            st.write(f"**Justificação Técnica:** {info['why']}")
            st.markdown(f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE SISTEMA</th></tr></thead>
                <tbody><tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
        with c_img:
            st.markdown("#### Verificação de Infraestrutura")
            st.write("Representação visual da segurança criptográfica e liquidação do ativo.")
            st.markdown(f"[Image of {info['name']} blockchain network architecture showing nodes, security layers, and transaction verification process]")

st.divider()

# ==============================================================================
# 10. GLOSSÁRIO & RODAPÉ
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA:** Digitalização de ativos físicos (Ouro, Imóveis) via código.")
    st.write("**CBDC:** Moeda Digital Estatal. O início do controlo monetário programável.")
with cg2:
    st.write("**ISO 20022:** A linguagem universal obrigatória para os bancos mundiais.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas quando você detém as chaves privadas.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão sobre os ativos de risco.")

st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN CORE © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1f2937;">MONÓLITO V35.0 // DENSITY & PRECISION READY</small>
</div>
""", unsafe_allow_html=True)

# --- LOOP DE ATUALIZAÇÃO (CORREÇÃO DE NAMEERROR) ---
if auto_refresh:
    st.session_state.news_cycle += 1
    time.sleep(30)
    st.rerun()
    
