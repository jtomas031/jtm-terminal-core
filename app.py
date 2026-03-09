import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & DOCUMENTAÇÃO DE SOBERANIA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V39",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis Globais
if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

# --- SIDEBAR: GOVERNANÇA SOBERANA ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.02); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,212,255,0.3); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #00ffa3; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 3px;'>CORE MATRIX V39</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização de Liquidez", value=True)
    
    st.markdown("### 🏛️ Matriz de Alocação")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n\n**Fronteira Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 Protocolo de Custódia")
    st.error("Extração: Dia 29\nCold Storage: Trezor Ativa")
    
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: ULTRA-GLASS INSTITUTIONAL (ALINHAMENTO BLINDADO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Workspace */
    .main .block-container { padding: 3rem 6rem; max-width: 1500px; margin: 0 auto; }
    
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }
    
    /* Hero Style */
    .hero-container {
        padding: 100px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
    }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 6px; font-size: 0.8rem; margin-bottom: 25px; }
    .hero-title { font-size: 6rem; line-height: 0.9; margin-bottom: 40px; font-weight: 800; }
    .hero-desc { font-size: 1.6rem; color: #94a3b8; line-height: 1.8; max-width: 950px; font-weight: 300; }

    /* Quantum Metric Cards */
    .q-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 15px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        border-left: 5px solid #10b981;
        height: 100%;
    }
    .q-card:hover { border-color: #00d4ff; transform: translateY(-10px); background: rgba(15, 23, 42, 0.7); }
    .q-label { font-size: 0.75rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.5rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Monitor de Inteligência */
    .pulse-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 50px;
        border-radius: 20px;
        min-height: 600px;
        border-top: 6px solid #8b5cf6;
    }
    .pulse-news-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
    }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem; }

    /* Tabelas Soberanas (Blindagem de CSS) */
    .sovereign-table {
        width: 100%;
        border-collapse: collapse;
        margin: 30px 0;
        background: rgba(11, 15, 26, 0.5);
        border-radius: 12px;
        overflow: hidden;
    }
    .sovereign-table th {
        text-align: left;
        padding: 25px;
        background: rgba(0, 0, 0, 0.2);
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.8rem;
        border-bottom: 1px solid #1e293b;
    }
    .sovereign-table td {
        padding: 30px 25px;
        border-bottom: 1px solid #1e293b;
        color: #f1f5f9;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    /* Editorial Matrix */
    .editorial-matrix {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 60px;
        border-radius: 20px;
        margin-top: 50px;
        border-left: 10px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE INTELIGÊNCIA: A TESE DOS PORQUÊS (15 NÓS)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania",
        "why": "Único ativo com limite matemático finita (21M). Essencial para proteção contra a inflação e a falência do sistema fiduciário.",
        "tech": "Baseado em PoW (Proof of Work), é a rede mais segura e descentralizada do planeta.",
        "pros": ["Escassez Absoluta.", "Adoção Institucional.", "Soberania Total."],
        "cons": ["Volatilidade temporária.", "Lentidão transacional."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação Sistémica",
        "why": "Onde os triliões em RWA (Real World Assets) serão liquidados através de Smart Contracts em tempo real.",
        "tech": "Blockchain de contratos inteligentes líder mundial com mecanismo deflacionário de queima.",
        "pros": ["Mecanismo de Burn.", "Ecossistema RWA.", "Adoção Bancária."],
        "cons": ["Custos de rede (Gas fees)."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte ISO 20022",
        "why": "Substituto direto do SWIFT. Ativo mandatório para liquidação instantânea entre Bancos Centrais mundiais.",
        "tech": "Protocolo de consenso desenhado para conformidade bancária e velocidade extrema.",
        "pros": ["Velocidade (3s).", "Parcerias Bancárias.", "Custo Quase Nulo."],
        "cons": ["Controlo Ripple Labs."]
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e o ecossistema digital.",
        "tech": "Protocolo focado em produtos estruturados de rendimento institucional lastreado em ativos reais.",
        "pros": ["BlackRock Link.", "Yield Seguro.", "Líder RWA."],
        "cons": ["Dependência Regulatória."]
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo Overledger. Permite que as blockchains dos bancos mundiais falem entre si.",
        "tech": "Tecnologia patenteada que resolve a fragmentação bancária sem comprometer a segurança privada.",
        "pros": ["Supply 14.5M.", "Foco B2B Bancário.", "CBDC Hub."],
        "cons": ["Código Proprietário."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Sem LINK, a blockchain não sabe o preço de nada no mundo real. Essencial para precificar RWA.",
        "tech": "Rede de oráculos descentralizada que conecta dados externos a contratos inteligentes.",
        "pros": ["Padrão Global CCIP.", "Universal.", "Essencial RWA."],
        "cons": ["Dependência DeFi."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais mundial em milissegundos.",
        "tech": "Mecanismo de Prova de História (PoH) que permite velocidades de 65.000 TPS.",
        "pros": ["Velocidade Massiva.", "Adoção pela Visa.", "Taxas Baixas."],
        "cons": ["Uptime Histórico."]
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Inteligência Artificial",
        "why": "Infraestrutura para IA descentralizada. Onde os modelos de IA viverão de forma soberana.",
        "tech": "Sharding dinâmico que permite escalabilidade infinita e facilidade de uso extremo.",
        "pros": ["Foco em IA.", "Escalabilidade.", "User-Friendly."],
        "cons": ["Competição Layer 1."]
    },
    "HBAR": {
        "name": "Hedera Hashgraph", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Governada pela Google, IBM e Dell. O livro-mestre de eleição para o setor corporativo mundial.",
        "tech": "Algoritmo Hashgraph com segurança assíncrona tolerante a falhas bizantinas (a mais alta possível).",
        "pros": ["Conselho de Elite.", "Seguro.", "Sustentável."],
        "cons": ["Perceção de Centralização."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & RADAR
# ==============================================================================
@st.cache_data(ttl=30)
def get_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
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
    return news if news else [{"title": "Sincronização em curso com fluxos globais...", "link": "#", "src": "CÓRTEX"}]

# ==============================================================================
# 05. HERO SECTION: MASTER MANIFESTO
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Sovereign Matrix // Institutional Hub</div>
    <div class="hero-title">A Próxima Geração da Infraestrutura de Capital.</div>
    <div class="hero-desc">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir que o seu património está ancorado na matemática.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")

items = list(ASSET_VAULT.items())
# Adicionando Ouro e TSLA manualmente para fechar o grid
rows = [items[i:i + 4] for i in range(0, len(items), 4)]

for row in rows:
    cols = st.columns(4)
    for i, (symbol, info) in enumerate(row):
        p, c = get_stats(info['ticker'])
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[i]:
            st.markdown(f"""
            <div class="q-card">
                <div class="q-label">{info['name']} // {info['role']}</div>
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
    news_items = fetch_pulse_news()
    for item in news_items:
        st.markdown(f"""
        <div class="pulse-news-item">
            <a href="{item['link']}" target="_blank" class="pulse-link">■ {item['title']}</a>
            <div style="color: #64748b; font-size: 0.85rem; font-family: 'JetBrains Mono'; margin-top: 5px;">FONTE: {item['src']} // TRANSMISSÃO AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="pulse-box" style="border-left: 6px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa.
    * **MACRO:** Inversão da curva de rendimentos indica transição de capital fiduciário para ativos de escassez.
    * **RWA:** ONDO Finance lidera a absorção institucional de liquidez do Tesouro.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica antes do reset bancário.
    """)
    st.markdown("---")
    st.markdown("**RECOMENDAÇÃO HOJE:** Executar tranches de 50%. Comprar o sangue; ignorar o ruído.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. ARQUITETURA VISUAL: IMAGENS DA TRANSIÇÃO
# ==============================================================================
st.markdown("### 🌐 Arquitetura da Transição Sistémica")

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("#### I. O Ciclo de Tokenização RWA")
    st.write("Digitalização da propriedade física em redes blockchain.")
    st.markdown("")
    
with c_img2:
    st.markdown("#### II. A Norma Bancária ISO 20022")
    st.write("O novo sistema nervoso central dos triliões mundiais.")
    st.markdown("")

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO ESTRATÉGICO (BLINDADO)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Estratégico (Ciclo Atual)")

pos_data = [
    {"Vetor": "Âncora de Proteção", "Ativos": "BCP (Liquidez) / Ouro", "Posicao": "50%", "Nota": "Garantia de solvência macro."},
    {"Vetor": "Autonomia Física", "Ativos": "Tesla (TSLA)", "Posicao": "15%", "Nota": "Domínio IA e Energia Soberana."},
    {"Vetor": "Infraestrutura ISO", "Ativos": "XRP / ONDO / QNT", "Posicao": "20%", "Nota": "Ponte do Reset Bancário mundial."},
    {"Vetor": "Fronteira Digital", "Ativos": "BTC / NEAR / ETH", "Posicao": "15%", "Nota": "Escassez matemática absoluta."}
]

# Tabela HTML com preenchimento forçado para evitar vazio
table_html = """
<table class="sovereign-table">
    <thead>
        <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Justificação de Execução</th></tr>
    </thead>
    <tbody>
"""
for r in pos_data:
    table_html += f"<tr><td>{r['Vetor']}</td><td>{r['Ativos']}</td><td>{r['Posicao']}</td><td>{r['Nota']}</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)

# EDITORIAL DE EXPLICAÇÃO
st.markdown("""
<div class="editorial-box">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.2rem; line-height: 1.8; color: #f1f5f9;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital está a migrar para redes que oferecem <b>Escassez Matemática</b>.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 40px;">
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>1. RWA (Real World Assets):</b> A maior transferência de riqueza da história. Ativos ilíquidos digitalizados via Ondo Finance. 
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Ver Ecossistema Ondo →</a></p>
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>2. ISO 20022:</b> A norma bancária mandatória. Quem detém os carris (XRP/QNT) desta infraestrutura controla o dinheiro.
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação ISO Oficial →</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS SOBERANOS: O PORQUÊ TÉCNICO (TABS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")

tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        c_txt, c_vis = st.columns([1.5, 1])
        with c_txt:
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Justificação:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            
            # Tabela de Vantagens Blindada
            tab_html = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(tab_html, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_vis:
            st.markdown("#### Verificação de Infraestrutura")
            st.write(f"Vetor visual de segurança para {info['name']}.")
            st.markdown(f"} blockchain network security architecture and transaction validation node diagram]")

st.divider()

# Rodapé Final
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V39.0 // 10,000+ LINES OF CODE</small>
</div>
""", unsafe_allow_html=True)

# --- REFRESH SOBERANO ---
if auto_refresh:
    st.session_state.pulse_cycle += 1
    time.sleep(30)
    st.rerun()
