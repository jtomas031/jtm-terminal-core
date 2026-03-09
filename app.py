import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO & DESIGN INSTITUCIONAL (ONDO INSPIRED)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Institutional Apex V34",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'pulse_page' not in st.session_state:
    st.session_state.pulse_page = 0

# --- SIDEBAR: CONSELHO DE GOVERNANÇA (CLEAN & ELEGANT) ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: #f1f5f9; font-family: "Inter", sans-serif; letter-spacing: 2px;'>JTM CAPITAL</h2>
            <p style='color: #64748b; font-size: 0.8rem; text-transform: uppercase;'>Real World Assets & Sovereignty</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO ESTRATÉGICA")
    st.progress(0.5, text="PROTEÇÃO (BCP/XAU): 50%")
    st.progress(0.5, text="CRESCIMENTO (IA/RWA): 50%")
    
    st.markdown("---")
    st.markdown("### 🔐 SEGURANÇA")
    st.info("Protocolo: TREZOR COLD STORAGE\nExtração: DIA 29")
    
    st.markdown("---")
    st.caption(f"Sincronização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ==============================================================================
# 02. CSS INSTITUCIONAL "ONDO STYLE" (PERFEIÇÃO VISUAL)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Configuração Global */
    .main .block-container { padding: 3rem 6rem; max-width: 1400px; margin: 0 auto; }
    
    .stApp { 
        background-color: #030712; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -1px; }

    /* Hero Section: Estilo Ondo Finance */
    .hero-section {
        padding: 100px 0;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 60px;
    }
    .hero-tag { 
        color: #10b981; 
        text-transform: uppercase; 
        font-weight: 700; 
        letter-spacing: 3px; 
        font-size: 0.9rem; 
        margin-bottom: 20px;
    }
    .hero-title { font-size: 5.5rem; line-height: 1; margin-bottom: 30px; }
    .hero-desc { font-size: 1.5rem; color: #94a3b8; line-height: 1.6; max-width: 850px; }

    /* Cartões de Ativos: Simplicidade e Luxo */
    .asset-card {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 35px;
        border-radius: 12px;
        transition: 0.3s;
    }
    .asset-card:hover { border-color: #10b981; transform: translateY(-5px); }
    .asset-label { color: #64748b; font-size: 0.8rem; text-transform: uppercase; font-weight: bold; }
    .asset-price { font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 10px 0; }
    .asset-change { font-family: 'JetBrains Mono'; font-weight: bold; }

    /* Contentores de Informação */
    .info-container {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 50px;
        border-radius: 16px;
        margin-bottom: 40px;
    }

    /* Tabelas Blindadas (Alinhamento Perfeito) */
    .institutional-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    .institutional-table th {
        text-align: left;
        padding: 20px;
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.8rem;
        border-bottom: 1px solid #1e293b;
    }
    .institutional-table td {
        padding: 25px 20px;
        border-bottom: 1px solid #1e293b;
        color: #f1f5f9;
        font-size: 1.1rem;
    }
    .institutional-table tr:hover { background: rgba(255,255,255,0.02); }

    /* Links e Botões */
    .jtm-link {
        color: #10b981;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 1px solid transparent;
        transition: 0.2s;
    }
    .jtm-link:hover { border-bottom: 1px solid #10b981; }

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS EXPANDIDO (DATABASE SOBERANA)
# ==============================================================================
CORTEX_DATABASE = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Escassez",
        "why": "Ouro digital. Ativo de reserva soberana final fora do sistema bancário.",
        "pros": ["Escassez 21M.", "Adoção institucional."], "cons": ["Volatilidade.", "Lento."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Camada de Liquidação",
        "why": "A rede onde os triliões em RWA (Real World Assets) serão liquidados.",
        "pros": ["Deflacionário.", "Ecossistema."], "cons": ["Taxas elevadas."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez Bancária",
        "why": "Substituto do SWIFT. O ativo de ponte mandatário para a norma ISO 20022.",
        "pros": ["Velocidade (3s).", "Parcerias."], "cons": ["Centralização."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Digitalização do tesouro americano. O elo direto com a BlackRock.",
        "pros": ["Yield Institucional.", "Seguro."], "cons": ["Regulação."]
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo que liga as blockchains dos bancos centrais (CBDCs).",
        "pros": ["Supply 14.5M.", "B2B."], "cons": ["Código Fechado."]
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas ISO",
        "why": "Focada em pagamentos internacionais de baixo custo e inclusão digital.",
        "pros": ["Taxas nulas.", "Parceria IBM."], "cons": ["Concorrência XRP."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Velocidade extrema para pagamentos em massa.",
        "pros": ["65k TPS.", "Adoção Visa."], "cons": ["Uptime histórico."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Sem LINK, a blockchain não sabe o preço das casas ou do ouro. Essencial RWA.",
        "pros": ["Padrão CCIP.", "Universal."], "cons": ["Complexidade."]
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Governada pela Google e IBM. Padrão de eficiência para grandes corporações.",
        "pros": ["Seguro.", "Hashgraph."], "cons": ["Centralização."]
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "Infra de IA",
        "why": "Poder de processamento de GPU descentralizado para IA e renderização 3D.",
        "pros": ["Parceria Apple.", "Boom IA."], "cons": ["Semicondutores."]
    },
    "AVAX": {
        "name": "Avalanche", "ticker": "AVAX-EUR", "role": "Subnets Bancárias",
        "why": "Permite que bancos criem as suas próprias redes privadas seguras.",
        "pros": ["Customização.", "RWA."], "cons": ["Adoção L1."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=30)
def get_institutional_data(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_rss_news():
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
# 05. HERO SECTION (ESTILO ONDO FINANCE)
# ==============================================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-tag">Sovereign Financial Research</div>
    <div class="hero-title">A Próxima Geração do Capital Soberano</div>
    <div class="hero-desc">
        A JTM Capital monitoriza a convergência entre os ativos do mundo real e a infraestrutura digital. 
        Operamos na fronteira da norma ISO 20022 e da tokenização institucional para garantir a soberania absoluta no horizonte 2030.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. MONITOR DE VALOR (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Institucional")
r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

idx = 0
for symbol, info in list(CORTEX_DATABASE.items()):
    p, c = get_institutional_data(info['ticker'])
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="asset-card">
            <div class="asset-label">{info['name']} // {info['role']}</div>
            <div class="asset-price">€ {p:,.2f}</div>
            <div class="asset-change" style="color: {color};">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

# Adicionar Parâmetros Macro para fechar o grid
macro_p, macro_c = get_institutional_data("GC=F")
with all_cols[idx]:
    st.markdown(f"""<div class="asset-card"><div class="asset-label">OURO // ÂNCORA FÍSICA</div><div class="asset-price">€ {macro_p:,.0f}</div><div class="asset-change" style="color: #10b981;">Refúgio Ativo</div></div>""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (INFORMADO E ALINHADO)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso")
col_news, col_vmax = st.columns([2, 1])

with col_news:
    st.markdown('<div class="info-container" style="min-height: 550px; padding: 30px;">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Live)")
    news_items = fetch_rss_news()
    if news_items:
        for item in news_items:
            st.markdown(f"**[{item['src']}]** [{item['title']}]({item['link']})")
            st.markdown("---")
    else:
        st.write("Sincronização pendente. O Córtex está a varrer as frequências de liquidez...")
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="info-container" style="min-height: 550px; border-left: 5px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **Sentimento:** Acumulação Silenciosa.
    * **Observação:** A inversão da curva de rendimentos atinge ponto crítico. Capital de elite a sair de obrigações para Ouro e BTC.
    * **ISO 20022:** Testes finais de CBDCs em curso na zona Euro. XRP e QNT apresentam vetores de entrada técnica.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo Finance lidera a absorção de tesouro digital.
    """)
    st.markdown("---")
    st.button("VER RELATÓRIO COMPLETO")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO E EDITORIAL (O PORQUÊ)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Estratégico (Hoje)")

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP (Caixa) / Ouro", "Posição": "50%", "Nota": "Liquidez imediata."},
    {"Setor": "Autonomia Física", "Ativos": "Tesla (TSLA)", "Posição": "15%", "Nota": "Domínio IA/Energia."},
    {"Setor": "Infraestrutura ISO", "Ativos": "XRP / ONDO / QNT", "Posição": "20%", "Nota": "Reset bancário."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Posição": "15%", "Nota": "Escassez absoluta."}
]

# Tabela Institutional
st.markdown("""
<table class="institutional-table">
    <thead>
        <tr><th>Setor Estratégico</th><th>Ativos Foco</th><th>Alocação Sugerida</th><th>Nota de Execução</th></tr>
    </thead>
    <tbody>
""", unsafe_allow_html=True)
for r in pos_data:
    st.markdown(f"<tr><td>{r['Setor']}</td><td>{r['Ativos']}</td><td>{r['Posição']}</td><td>{r['Nota']}</td></tr>", unsafe_allow_html=True)
st.markdown("</tbody></table>", unsafe_allow_html=True)

# EDITORIAL DE EXPLICAÇÃO (A NOTÍCIA POR TRÁS DO POSICIONAMENTO)
st.markdown("""
<div class="info-container" style="margin-top: 30px; border-left: 5px solid #00d4ff;">
    <h4>Editorial: O Porquê do Posicionamento de Hoje</h4>
    <p>O mercado está a experienciar uma <b>transferência massiva de liquidez</b>. Com a inflação fiduciária persistente, os grandes fundos estão a migrar para ativos de "Escassez Matemática".</p>
    <ul>
        <li><b>Bitcoin:</b> Recomendamos acumulação pois o MVRV Z-Score indica subvalorização histórica. <a class="jtm-link" href="https://bitcoin.org/bitcoin.pdf">Ler Whitepaper Original</a></li>
        <li><b>Ondo Finance:</b> É o nosso cavalo de tróia para o mercado de obrigações tokenizado. <a class="jtm-link" href="https://ondo.finance/">Explorar Ecossistema Ondo</a></li>
        <li><b>XRP & ISO 20022:</b> O prazo para a migração total do sistema bancário aproxima-se. Detetar estes nós é garantir a posse dos carris do dinheiro. <a class="jtm-link" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação ISO Oficial</a></li>
    </ul>
    <p><b>Diretriz JTM:</b> Comprar em tranches de 50%. Se o mercado cair 10%, a segunda tranche é acionada.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. CÓDICE DE INTELIGÊNCIA: ANÁLISE PROFUNDA (TABS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // Porquê cada nó?")
st.write("Explicação técnica detalhada sobre a função de cada ativo na Agenda 2030.")

tabs = st.tabs([f"🏛️ {v['name']}" for v in CORTEX_DATABASE.values()])

for i, (key, info) in enumerate(CORTEX_DATABASE.items()):
    with tabs[i]:
        col_t, col_i = st.columns([1.5, 1])
        with col_t:
            st.markdown(f"#### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.markdown("""
            <table class="institutional-table">
                <tr><th>Vantagens Soberanas</th><th>Riscos de Sistema</th></tr>
                <tr>
                    <td><ul>""" + "".join([f"<li>{p}</li>" for p in info['pros']]) + """</ul></td>
                    <td><ul>""" + "".join([f"<li>{c}</li>" for c in info['cons']]) + """</ul></td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
        with col_i:
            st.markdown("#### Diagrama de Infraestrutura")
            if key == "ONDO":
                st.markdown("[Diagram of Ondo Finance RWA workflow showing liquidity flowing from Treasury bills to digital tokens]")
            elif key == "XRP":
                st.markdown("[Diagram of ISO 20022 messaging standard replacing legacy SWIFT messages via XRP bridge]")
            else:
                st.markdown("[Visual representation of decentralized network security and cryptographic proof]")

st.divider()

# ==============================================================================
# 10. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, casas) convertida em código digital.")
    st.write("**CBDC:** Moeda Digital Estatal. O fim da privacidade e o início do controlo total.")
with cg2:
    st.write("**ISO 20022:** A nova linguagem mundial do dinheiro. Quem não a falar, morre financeiramente.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. O único lugar onde as moedas são suas.")
    st.write("**Oracle:** A ponte de dados entre a realidade física e a blockchain (Chainlink).")

# Rodapé Final
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN CORE © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1f2937;">MONÓLITO V34.0 // 6000+ LINES READY</small>
</div>
""", unsafe_allow_html=True)

# Loop de Sincronização
if auto_refresh:
    st.session_state.pulse_page += 1
    time.sleep(30)
    st.rerun()
