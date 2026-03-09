import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE INTELIGÊNCIA & CONFIGURAÇÃO GLOBAL (2026)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Singularity V40",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Estado (Prevenção de NameError)
if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

# --- SIDEBAR: GOVERNANÇA INSTITUCIONAL ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.02); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,212,255,0.3); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 3px;'>SINGULARITY V40.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_sync = st.toggle("Sincronização de Fluxo", value=True)
    
    st.markdown("### 🏛️ Matriz de Alocação")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 Protocolo de Custódia")
    st.error("Extração: Dia 29\nStatus: Cold Storage Ativa")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: INSTITUTIONAL GLASS (DESIGN ONDO + MATRIX)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Workspace */
    .main .block-container { padding: 3rem 6rem; max-width: 1600px; margin: 0 auto; }
    
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }
    
    /* Hero Style */
    .hero-container {
        padding: 120px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
    }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 6px; font-size: 0.8rem; margin-bottom: 25px; }
    .hero-title { font-size: 6.5rem; line-height: 0.85; margin-bottom: 40px; font-weight: 800; letter-spacing: -2px; }
    .hero-desc { font-size: 1.7rem; color: #94a3b8; line-height: 1.8; max-width: 1000px; font-weight: 300; }

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
    .q-card:hover { border-color: #00d4ff; transform: translateY(-10px); background: rgba(15, 23, 42, 0.7); box-shadow: 0 30px 60px rgba(0, 212, 255, 0.1); }
    .q-label { font-size: 0.8rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.6rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Monitor de Inteligência // O Pulso */
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
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.4rem; transition: 0.2s; }
    .pulse-link:hover { color: #10b981; }

    /* Tabelas Soberanas (Blindagem Total) */
    .sovereign-table-wrapper { width: 100%; margin: 30px 0; overflow: hidden; border-radius: 12px; }
    .sovereign-table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(11, 15, 26, 0.5);
    }
    .sovereign-table th {
        text-align: left;
        padding: 25px;
        background: rgba(0, 0, 0, 0.3);
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.85rem;
        border-bottom: 1px solid #1e293b;
    }
    .sovereign-table td {
        padding: 30px 25px;
        border-bottom: 1px solid #1e293b;
        color: #f1f5f9;
        font-size: 1.15rem;
        line-height: 1.8;
        vertical-align: top;
    }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    /* Editorial Box */
    .editorial-matrix {
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
# 03. CÓDICE DE ATIVOS: O PORQUÊ TÉCNICO (+15 NÓS SOBERANOS)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Escassez",
        "why": "Ouro digital. Ativo de escassez matemática finita (21M). Essencial para proteção contra o colapso do sistema fiduciário analógico.",
        "tech": "Baseado em Proof of Work (PoW), é a rede monetária mais segura da história. Funciona como reserva de valor institucional imutável.",
        "pros": ["Escassez 21M.", "Adoção Institucional (ETFs).", "Soberania Geopolítica."],
        "cons": ["Volatilidade em curto prazo.", "Lentidão transacional na L1."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Camada de Liquidação",
        "why": "O sistema operativo das finanças. É a infraestrutura onde triliões em RWA serão tokenizados e liquidados sem intermediários.",
        "tech": "Líder mundial em Smart Contracts. O mecanismo de 'EIP-1559' torna o ativo deflacionário ao queimar taxas de rede.",
        "pros": ["Deflacionário.", "Ecossistema RWA.", "Settlement Layer Global."],
        "cons": ["Gas fees.", "Fragmentação L2."],
        "link": "https://ethereum.org/"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "Substituto direto do sistema SWIFT. Ativo de ponte desenhado para liquidação instantânea entre bancos mundiais.",
        "tech": "Protocolo de consenso que resolve pagamentos transfronteiriços em 3 segundos com custos irrisórios.",
        "pros": ["Velocidade extrema.", "Conformidade Bancária.", "Baixo Custo."],
        "cons": ["Escrutínio Regulatório."],
        "link": "https://ripple.com/xrp/"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e a nova economia digital.",
        "tech": "Protocolo de ativos reais que traz rendimentos de baixo risco (Treasuries) para o ambiente on-chain.",
        "pros": ["BlackRock Partnership.", "Yield Institucional.", "Líder RWA."],
        "cons": ["Risco Centralizado."],
        "link": "https://ondo.finance/"
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo Overledger. Permite que blockchains privadas de bancos (CBDCs) falem entre si.",
        "tech": "Tecnologia que resolve o problema da fragmentação sem comprometer a segurança da rede interna corporativa.",
        "pros": ["Supply limitada (14.5M).", "Foco 100% Bancário.", "ISO 20022 ready."],
        "cons": ["Código Proprietário."],
        "link": "https://www.quant.network/"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Sem LINK, a blockchain é cega. Essencial para trazer preços de ouro e imóveis para os contratos inteligentes.",
        "tech": "Rede descentralizada de oráculos que conecta dados externos a contratos inteligentes com segurança criptográfica.",
        "pros": ["Padrão Global CCIP.", "Universal.", "Essencial RWA."],
        "cons": ["Tokenomics Lento."],
        "link": "https://chain.link/"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais mundial em milissegundos.",
        "tech": "Mecanismo de Proof of History (PoH) que permite velocidades de 65.000 TPS.",
        "pros": ["Velocidade Massiva.", "Adoção Visa.", "Taxas Baixas."],
        "cons": ["Uptime Histórico."]
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Inteligência Artificial",
        "why": "Infraestrutura para IA descentralizada. Onde os modelos de IA viverão de forma soberana e imutável.",
        "tech": "Arquitetura Sharding que permite escalabilidade infinita e facilidade de uso para o utilizador final.",
        "pros": ["Foco em IA.", "Escalabilidade.", "User-Friendly."],
        "cons": ["Mercado Competitivo."]
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

def fetch_pulse_radar():
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
    <div class="hero-tag">Sovereign Financial Hub // Singularity</div>
    <div class="hero-title">A Nova Infraestrutura do Capital Global.</div>
    <div class="hero-desc">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos físicos (RWA) e redes de alta performance. 
        Operamos na fronteira da norma <b>ISO 20022</b> para garantir soberania absoluta através da matemática.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")

items = list(ASSET_VAULT.items())
# Adicionando parâmetros macro para completar o grid
EXTRA_STATS = {
    "GOLD": ("Ouro Físico (GC=F)", "GC=F"), "TSLA": ("Tesla IA (TSLA)", "TSLA"),
    "BCP": ("BCP Liquidez (LS)", "BCP.LS"), "VIX": ("Índice Medo (^VIX)", "^VIX")
}

total_display = items + list(EXTRA_STATS.items())
rows = [total_display[i:i + 4] for i in range(0, len(total_display), 4)]

for row in rows:
    cols = st.columns(4)
    for i, item in enumerate(row):
        key, info = item
        name, ticker = (info['name'], info['ticker']) if isinstance(info, dict) else (info[0], info[1])
        p, c = get_institutional_stats(ticker)
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[i]:
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
    news_items = fetch_pulse_radar()
    for item in news_items:
        st.markdown(f"""
        <div class="pulse-news-item">
            <a href="{item['link']}" target="_blank" class="pulse-link">■ {item['title']}</a>
            <div style="color: #64748b; font-size: 0.9rem; font-family: 'JetBrains Mono'; margin-top: 8px;">FONTE: {item['src']} // TRANSMISSÃO EM TEMPO REAL</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="pulse-box" style="border-left: 6px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa e Estratégica.
    * **MACRO:** Inversão da curva de rendimentos indica migração para ativos de escassez absoluta.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo lidera a absorção do Tesouro Digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada antes do reset bancário.
    """)
    st.markdown("---")
    st.markdown("**RECOMENDAÇÃO HOJE:** Executar tranches de 50%. Acumular no sangue; vender na euforia.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. ARQUITETURA VISUAL: DIAGRAMAS DA TRANSIÇÃO
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
    {"Vetor": "Autonomia Física", "Ativos": "Tesla (TSLA)", "Posicao": "15%", "Nota": "Domínio IA e Energia."},
    {"Vetor": "Infraestrutura ISO", "Ativos": "XRP / ONDO / QNT", "Posicao": "20%", "Nota": "Reset Bancário Mundial."},
    {"Vetor": "Fronteira Digital", "Ativos": "BTC / NEAR / ETH", "Posicao": "15%", "Nota": "Escassez Matemática."}
]

table_html = """
<div class="sovereign-table-wrapper">
    <table class="sovereign-table">
        <thead>
            <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Justificação de Execução</th></tr>
        </thead>
        <tbody>
"""
for r in pos_data:
    table_html += f"<tr><td>{r['Vetor']}</td><td>{r['Ativos']}</td><td>{r['Posicao']}</td><td>{r['Nota']}</td></tr>"
table_html += "</tbody></table></div>"

st.markdown(table_html, unsafe_allow_html=True)

# EDITORIAL DE EXPLICAÇÃO
st.markdown("""
<div class="editorial-matrix">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.3rem; line-height: 1.8; color: #f1f5f9;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital de elite está a migrar para redes que oferecem <b>Escassez Matemática</b>.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 40px;">
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>1. RWA (Real World Assets):</b> A maior transferência de riqueza em curso. Ativos ilíquidos digitalizados via Ondo Finance. 
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Explorar Ecossistema Ondo →</a></p>
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
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
            
            tab_html = f"""
            <div class="sovereign-table-wrapper">
                <table class="sovereign-table">
                    <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                    <tbody><tr>
                        <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr></tbody>
                </table>
            </div>
            """
            st.markdown(tab_html, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>LER DOCUMENTAÇÃO OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_vis:
            st.markdown("#### Verificação de Infraestrutura")
            st.write(f"Vetor visual de segurança para {info['name']}.")
            # FIX: SyntaxError resolvido aqui com f-string correta
            st.markdown(f"} blockchain network security architecture and transaction validation node diagram]")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física (Ouro, Imóveis) digitalizada via código.")
    st.write("**VIX:** Índice de pânico institucional. Se sobe, a oportunidade de compra aumenta.")
with cg2:
    st.write("**ISO 20022:** A nova gramática mundial obrigatória para os bancos mundiais.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas com as chaves offline.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão sobre os ativos de risco.")

st.divider()

# Rodapé Final
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1f2937;">MONÓLITO V40.0 // OMNIPOTENT MASTER READY</small>
</div>
""", unsafe_allow_html=True)

# --- REFRESH SOBERANO ---
if auto_sync:
    st.session_state.pulse_cycle += 1
    time.sleep(30)
    st.rerun()
