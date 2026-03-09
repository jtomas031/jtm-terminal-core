import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO & ESTADO SOBERANO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Master V44",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

auto_refresh = True

# --- SIDEBAR: CONSELHO DE GOVERNANÇA (ULTRA-LUXO) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.03); padding: 30px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center;'>
            <h1 style='color: #f1f5f9; font-family: "Inter", sans-serif; margin:0; font-size: 1.5rem;'>JTM CAPITAL</h1>
            <p style='color: #10b981; font-family: "JetBrains Mono"; font-size: 0.7rem; letter-spacing: 4px;'>V44.0 // ETERNAL ARCHIVE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização Ativa", value=True)
    
    st.markdown("### 🏛️ MATRIZ DE ALOCAÇÃO")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 CUSTÓDIA SOBERANA")
    st.error("Protocolo: TREZOR COLD STORAGE\nStatus: Blindagem Ativa")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: ONDO-INFINITY GLASS (ALINHAMENTO BLINDADO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Global Page Structure */
    .main .block-container { padding: 3rem 6rem; max-width: 1600px; margin: 0 auto; }
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }
    
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -2px; line-height: 1.1; }

    /* Hero Section: Institutional Mastery */
    .hero-panel {
        padding: 120px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
    }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 6px; font-size: 0.8rem; margin-bottom: 30px; }
    .hero-title { font-size: 6.5rem; margin-bottom: 45px; }
    .hero-desc { font-size: 1.7rem; color: #94a3b8; line-height: 1.8; max-width: 1000px; font-weight: 300; }

    /* Telemetry Cards */
    .q-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 45px;
        border-radius: 15px;
        transition: 0.5s ease;
        border-left: 5px solid #10b981;
        height: 100%;
    }
    .q-card:hover { border-color: #00d4ff; transform: translateY(-12px); background: rgba(15, 23, 42, 0.7); box-shadow: 0 40px 80px rgba(0, 212, 255, 0.1); }
    .q-label { font-size: 0.8rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; }
    .q-value { font-size: 2.8rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Tables: The Blinded System */
    .sovereign-table-wrapper { width: 100%; border-radius: 15px; overflow: hidden; border: 1px solid #1e293b; margin: 40px 0; }
    .sovereign-table { width: 100%; border-collapse: collapse; background: #0b0f1a; }
    .sovereign-table th { text-align: left; padding: 25px; background: rgba(0,0,0,0.3); color: #64748b; text-transform: uppercase; font-size: 0.8rem; border-bottom: 1px solid #1e293b; }
    .sovereign-table td { padding: 30px 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.1rem; line-height: 1.9; vertical-align: top; }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    /* Sections */
    .content-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 60px;
        border-radius: 20px;
        margin-bottom: 60px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS: TESES DE 30 MIL LINHAS (EXPANSÃO TOTAL)
# ==============================================================================
CORTEX_INTEL = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania Matemática",
        "why": """O Bitcoin é a única rede monetária no universo conhecido com escassez finita verificável (21M). 
        Enquanto os Bancos Centrais mundiais imprimem dívida a uma taxa exponencial, o Bitcoin atua como um 'Buraco Negro de Liquidez'. 
        Ele absorve o valor perdido pelo papel-moeda analógico. É a sua apólice de seguro definitiva contra a falência do sistema fiduciário.""",
        "future": "Em 2030, o Bitcoin será utilizado como ativo de reserva por bancos centrais soberanos para liquidar balanços comerciais internacionais.",
        "pros": ["Escassez Absoluta Imutável", "Adoção Institucional (ETFs)", "Resiliência Geopolítica"],
        "cons": ["Volatilidade temporária induzida por baleias", "Lentidão transacional na Camada 1"],
        "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Autoestrada da Tokenização (RWA)",
        "why": """O Ethereum é o sistema operativo das finanças globais. Através dos Smart Contracts, ele permite digitalizar triliões de dólares em ativos físicos. 
        O mercado imobiliário e as obrigações do tesouro mundial serão negociados 24/7 nesta rede. O Ethereum é o motor da eficiência bancária do futuro.""",
        "future": "Tornar-se-á a camada de liquidação definitiva para o mercado de capitais mundial de 100 triliões de dólares.",
        "pros": ["Monopólio em Contratos Inteligentes", "Mecanismo de 'Burn' Deflacionário", "Base para Stablecoins"],
        "cons": ["Custos de rede elevados", "Fragmentação em Camadas 2"],
        "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Protocolo de Liquidez ISO 20022",
        "why": """O XRP foi desenhado para substituir o arcaico sistema SWIFT. Ele permite que bancos mundiais movam valor instantaneamente por uma fração de cêntimo. 
        É a peça central da norma ISO 20022. Sem o XRP, o sistema bancário digital moderno não consegue liquidar pagamentos transfronteiriços em tempo real.""",
        "future": "Ativo de ponte oficial para todas as Moedas Digitais de Bancos Centrais (CBDCs) e liquidação interbancária.",
        "pros": ["Liquidação em 3-5 segundos", "Conformidade Bancária Absoluta", "Eficiência Energética"],
        "cons": ["Controlo histórico Ripple Labs", "Escrutínio Regulatório"],
        "link": "https://ripple.com/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA Institucional",
        "why": """O elo perdido entre a BlackRock e a Blockchain. ONDO permite que investidores acedam a rendimentos do tesouro americano de forma tokenizada. 
        É o líder absoluto no setor de RWA (Real World Assets), trazendo a liquidez das instituições para a rede.""",
        "future": "Será o veículo principal para a digitalização de fundos monetários institucionais globais.",
        "pros": ["Parceria BlackRock", "Ativos Lastreados em Valor Real", "Líder RWA"],
        "cons": ["Risco Regulatório Fiat", "Dependência de Parceiros Tradicionais"],
        "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Sistema Operativo Interbancário",
        "why": """O Overledger da Quant é a única tecnologia que permite que as blockchains dos bancos centrais (CBDCs) falem com as blockchains públicas. 
        É o conector universal que impede a fragmentação do novo sistema financeiro.""",
        "future": "Padrão de interoperabilidade para todas as transações de triliões entre governos e bancos mundiais.",
        "pros": ["Supply Ultra-Escassa (14.5M)", "Foco 100% Enterprise", "Conexão Universal"],
        "cons": ["Código Proprietário (Fechado)"],
        "link": "https://www.quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Integridade de Dados",
        "why": """As blockchains são surdas e cegas para o mundo real. O Chainlink é a ponte de dados que diz à blockchain o preço real de uma casa ou do ouro. 
        Sem LINK, a tokenização de ativos físicos (RWA) é matematicamente impossível.""",
        "future": "O padrão CCIP será o protocolo de comunicação obrigatório para toda a infraestrutura financeira global.",
        "pros": ["Padrão Global de Oráculos", "Parceria SWIFT", "Indispensável"],
        "cons": ["Tokenomics Lento"],
        "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Execução de Alta Performance",
        "why": """A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais mundial em milissegundos. 
        Escolha oficial da Visa e Shopify para pagamentos digitais em massa devido à sua velocidade extrema.""",
        "future": "Principal camada de execução para aplicações de consumo massivo e finanças de alta frequência.",
        "pros": ["Velocidade (65k TPS)", "Taxas Mínimas", "Adoção pela Visa"],
        "cons": ["Histórico de Uptime", "Hardware de Nó Caro"],
        "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"
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
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    return news

# ==============================================================================
# 05. HERO PANEL: JTM SOVEREIGN MASTER
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-tag">Sovereign Financial Hub // Horizon 2030</div>
    <div class="hero-title">A Próxima Geração da Infraestrutura de Capital.</div>
    <p class="hero-desc">Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas. 
    Operamos na fronteira da norma ISO 20022 para garantir soberania absoluta através da matemática inquebrável.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. LIVE TELEMETRY (GRELHA COMPLETA)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
items = list(CORTEX_INTEL.items())
EXTRA_ASSETS = [
    ("TSLA", {"name": "Tesla IA", "ticker": "TSLA", "role": "Autonomia"}),
    ("GOLD", {"name": "Ouro Físico", "ticker": "GC=F", "role": "Âncora"}),
    ("BCP", {"name": "BCP Liquidez", "ticker": "BCP.LS", "role": "Fiat"}),
    ("VIX", {"name": "Índice Medo", "ticker": "^VIX", "role": "Macro"})
]
full_display = items + EXTRA_ASSETS

for i in range(0, len(full_display), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(full_display):
            key, val = full_display[idx]
            p, c = get_stats(val['ticker'])
            color = "#10b981" if c >= 0 else "#ef4444"
            with cols[j]:
                st.markdown(f"""
                <div class="q-card">
                    <div class="q-label">{val['name']} // {val['role']}</div>
                    <div class="q-price">€ {p:,.2f}</div>
                    <div style="color:{color}; font-weight:800; font-family:JetBrains Mono;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (NOTÍCIAS REAIS)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_radar, c_vmax = st.columns([2, 1])

with c_radar:
    st.markdown('<div class="content-box" style="height:600px; overflow-y:auto; padding:40px;">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Live Feed)")
    news_list = fetch_radar()
    for n in news_list:
        st.markdown(f"**[{n['src']}]** [{n['title']}]({n['link']})")
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

with c_vmax:
    st.markdown('<div class="content-box" style="height:600px; border-left: 10px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa e Estratégica.
    * **MACRO:** Inversão da curva de rendimentos US10Y-US02Y indica migração para ativos de escassez absoluta.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo lidera a absorção do Tesouro Digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica antes do reset bancário mundial.
    """)
    st.success("**RECOMENDAÇÃO HOJE:** Acumular em tranches de 50%. Comprar no sangue; vender na euforia.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO E EDITORIAL (TEXTO MASSIVO)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Recomendado (Hoje)")

pos_data = [
    {"V": "Âncora de Proteção", "A": "BCP (Liquidez) / Ouro", "P": "50%", "N": "Garantia de solvência macro."},
    {"V": "Autonomia Física", "A": "Tesla (TSLA)", "P": "15%", "N": "Domínio IA e Energia Soberana."},
    {"V": "Infraestrutura ISO", "A": "XRP / ONDO / QNT", "P": "20%", "N": "Reset Bancário Mundial."},
    {"V": "Fronteira Digital", "A": "BTC / NEAR / ETH", "P": "15%", "N": "Escassez Matemática Absoluta."}
]

table_h = """
<div class="sovereign-table-wrapper">
    <table class="sovereign-table">
        <thead>
            <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Justificação de Execução</th></tr>
        </thead>
        <tbody>
"""
for r in pos_data:
    table_h += f"<tr><td>{r['V']}</td><td>{r['A']}</td><td>{r['P']}</td><td>{r['N']}</td></tr>"
table_h += "</tbody></table></div>"
st.markdown(table_h, unsafe_allow_html=True)

st.markdown("""
<div class="content-box" style="border-left: 10px solid #00d4ff;">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.3rem; line-height: 2; color: #f1f5f9;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital de elite está a migrar para redes que oferecem <b>Escassez Matemática</b>.
        A nossa estratégia de 50/50 garante que o monólito JTM Capital permanece líquido em caso de volatilidade, enquanto captura a explosão da tokenização (RWA).
    </p>
    <div style="display: flex; gap: 40px; margin-top: 40px;">
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>1. RWA (Real World Assets):</b> Digitalização de ativos físicos via Ondo Finance. 
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Explorar Ondo Finance →</a></p>
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>2. ISO 20022:</b> A norma bancária obrigatória. XRP e QNT são os carris do sistema.
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação ISO Oficial →</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. ARQUITETURA VISUAL: DIAGRAMAS DA TRANSIÇÃO
# ==============================================================================
st.markdown("### 🌐 Arquitetura da Transição Sistémica")
c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("#### I. O Ciclo de Tokenização RWA")
    st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=1200", caption="Tokenização de Ativos do Mundo Real")
    st.write("A ponte definitiva entre o mundo físico e a liquidez digital 24/7.")

with c_img2:
    st.markdown("#### II. A Norma Bancária ISO 20022")
    st.image("https://images.unsplash.com/photo-1642104704074-907c0698cbd9?auto=format&fit=crop&q=80&w=1200", caption="Arquitetura de Mensagens Bancárias")
    st.write("O novo sistema nervoso central dos triliões mundiais substitui o SWIFT legado.")

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS SOBERANOS: O PORQUÊ TÉCNICO (TEXTO INFINITO)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")
tabs = st.tabs([f"🏛️ {v['name']}" for v in CORTEX_INTEL.values()])

for i, (key, info) in enumerate(CORTEX_INTEL.items()):
    with tabs[i]:
        c_tx, c_vis = st.columns([1.5, 1])
        with c_tx:
            st.image(info['img'], width=100)
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Justificação Estratégica:** {info['why']}")
            st.write(f"**Visão 2030:** {info['future']}")
            
            # Tabela de Vantagens Blindada
            tab_h = f"""
            <div class="sovereign-table-wrapper">
                <table class="sovereign-table">
                    <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                    <tbody><tr>
                        <td><ul>{"".join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{"".join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr></tbody>
                </table>
            </div>
            """
            st.markdown(tab_h, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_vis:
            st.markdown("#### Verificação de Rede")
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Topologia Criptográfica: {info['name']}")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, imóveis, tesouro) convertida em código digital imutável.")
    st.write("**VIX (Índice do Medo):** Mede a volatilidade esperada. Se sobe, indica pânico e oportunidade institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais. Quem não a falar, morre financeiramente.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre em segundos.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas com as chaves offline.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão sobre os ativos de risco.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V44.0 // ETERNAL ARCHIVE READY</small>
</div>
""", unsafe_allow_html=True)

if auto_refresh:
    time.sleep(30)
    st.rerun()
