import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO E GESTÃO DE ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Global Intelligence Terminal",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Gestão de Estado para Rotação de Notícias e Simulação
if 'news_index' not in st.session_state:
    st.session_state.news_index = 0
if 'sim_step' not in st.session_state:
    st.session_state.sim_step = 1

# --- SIDEBAR DE COMANDO ---
with st.sidebar:
    st.markdown("### 🛰️ COMANDO CENTRAL")
    st.markdown("---")
    auto_refresh = st.toggle("RECARGA AUTOMÁTICA (30s)", value=True)
    st.caption("Sincronização com o fluxo de capitais de Wall Street.")
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO ESTRATÉGICA")
    st.progress(0.83, text="300€: BASE (BTC/ETH)")
    st.progress(0.17, text="60€: SNIPER (ISO/RWA)")
    
    st.markdown("---")
    st.markdown("### 🔒 PROTOCOLO TREZOR")
    st.error("SISTEMA DE CUSTÓDIA: ATIVO\n\nALVO: COLD STORAGE\n\nEXTRAÇÃO: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🌍 RELÓGIO DE MERCADO")
    st.info(f"Londres: {datetime.now().strftime('%H:%M')} WET\nNova Iorque: {datetime.now().strftime('%H:%M')} EST")

# ==============================================================================
# 02. CSS CUSTOMIZADO (DOPAMINA & ESTÉTICA BLOOMBERG TERMINAL)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@500;700&family=Inter:wght@300;400;700;900&display=swap');

    /* Design de Fundo e Containers */
    .stApp { 
        background-color: #010409; 
        color: #c9d1d9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 10%, #0d1117 0%, #010409 100%);
    }

    /* Hero Section Imponente */
    .hero-panel {
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid #30363d;
        border-top: 5px solid #238636;
        padding: 60px;
        border-radius: 4px;
        margin-bottom: 50px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.8);
    }
    .hero-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }
    .hero-tagline {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        color: #238636;
        text-transform: uppercase;
        letter-spacing: 6px;
    }

    /* Cartões de Métrica com Glassmorphism */
    .metric-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-left: 4px solid #1f6feb;
        padding: 25px;
        border-radius: 4px;
        transition: 0.3s;
    }
    .metric-card:hover { border-color: #58a6ff; box-shadow: 0 0 20px rgba(88, 166, 255, 0.2); }
    .metric-label { font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #8b949e; text-transform: uppercase; }
    .metric-value { font-family: 'Rajdhani'; font-size: 2.5rem; font-weight: 700; color: #f0f6fc; }

    /* Feed de Notícias Compacto & Rotativo */
    .news-container {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 20px;
        height: 520px;
        overflow: hidden;
        border-left: 4px solid #8957e5;
    }
    .news-item {
        border-bottom: 1px solid #21262d;
        padding: 15px 0;
        transition: background 0.2s;
    }
    .news-item:hover { background: #161b22; }
    .news-link { color: #58a6ff; text-decoration: none; font-weight: bold; font-size: 1.1rem; }
    .news-source { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; margin-top: 5px; }

    /* Estilo para Artigos de Educação Profunda */
    .edu-content {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 40px;
        line-height: 2;
        font-size: 1.15rem;
    }
    .edu-header { font-family: 'Rajdhani'; font-size: 2.5rem; color: #ffffff; border-bottom: 2px solid #238636; padding-bottom: 15px; margin-bottom: 30px; }
    .highlight { color: #58a6ff; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZES DE DADOS E DICIONÁRIOS (INTELIGÊNCIA MASSIVA)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000,
    "XRP-EUR": 54800000000, "QNT-EUR": 14500000, "XLM-EUR": 28700000000,
    "RNDR-EUR": 388000000, "SOL-EUR": 440000000, "HBAR-EUR": 33000000000, "ALGO-EUR": 8000000000
}

ASSET_INTEL = {
    "BITCOIN": {
        "ticker": "BTC-EUR",
        "role": "Reserva de Valor Soberana",
        "vision": "O Bitcoin é o novo padrão-ouro digital. Com o halving e a entrada dos ETFs, o capital institucional está a drenar a oferta das exchanges.",
        "pros": ["Escassez Absoluta (21M)", "Inconfiscável", "Adoção por Fundos Soberanos"],
        "cons": ["Lentidão na Camada 1", "Volatilidade de curto prazo"],
        "partners": "BlackRock, Fidelity, MicroStrategy"
    },
    "ETHEREUM": {
        "ticker": "ETH-EUR",
        "role": "Infraestrutura RWA Global",
        "vision": "A camada de liquidação definitiva onde a BlackRock emite os seus fundos tokenizados. O computador mundial.",
        "pros": ["Dominância RWA", "Queima de Tokens (Deflação)", "Staking Institucional"],
        "cons": ["Taxas de Gas elevadas", "Fragmentação L2"],
        "partners": "JPMorgan, Microsoft, Goldman Sachs"
    },
    "RIPPLE (XRP)": {
        "ticker": "XRP-EUR",
        "role": "Liquidez ISO 20022",
        "vision": "O substituto do SWIFT. Liquidação bruta em tempo real para bancos centrais e remessas transfronteiriças.",
        "pros": ["Velocidade (3s)", "Conformidade ISO 20022", "Claridade Jurídica"],
        "cons": ["Centralização da Ripple Labs", "Competição de CBDCs"],
        "partners": "Banco Santander, SBI Holdings, MoneyGram"
    },
    "QUANT": {
        "ticker": "QNT-EUR",
        "role": "Interoperabilidade B2B",
        "vision": "O sistema operativo Overledger que liga redes bancárias privadas à blockchain pública.",
        "pros": ["Oferta de 14M (Ultra Escasso)", "Parcerias Governamentais", "Agnóstico a Redes"],
        "cons": ["Código Fechado", "Baixa Liquidez de Retalho"],
        "partners": "Oracle, Nexi, SIA"
    },
    "CHAINLINK": {
        "ticker": "LINK-EUR",
        "role": "Oráculo de Dados Críticos",
        "vision": "O fornecedor de dados que liga os bancos do mundo real aos Smart Contracts. Sem LINK, o RWA não existe.",
        "pros": ["Monopólio de Oráculos", "Protocolo CCIP", "Essencial para DeFi"],
        "cons": ["Tokenomics complexa", "Baixa utilidade para retalho"],
        "partners": "SWIFT, Google Cloud, AWS"
    },
    "RENDER": {
        "ticker": "RNDR-EUR",
        "role": "Infraestrutura de IA (DePIN)",
        "vision": "A rede que fornece poder de GPU para a expansão mundial da IA. O aluguer de hardware descentralizado.",
        "pros": ["Narrativa IA Forte", "Demanda Real de Hardware", "Eficiência Energética"],
        "cons": ["Dependência da Bolha IA", "Custo de Hardware Nvidia"],
        "partners": "Apple, Nvidia, Microsoft"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E NOTÍCIAS
# ==============================================================================
@st.cache_data(ttl=25)
def get_live_stats(ticker):
    try:
        df = yf.download(ticker, period="2d", interval="1h", progress=False)
        current = df['Close'].iloc[-1].item()
        change = ((current - df['Open'].iloc[0].item()) / df['Open'].iloc[0].item()) * 100
        vol = df['Volume'].iloc[-1].item()
        mcap = current * SUPPLY_DATA.get(ticker, 0)
        return current, change, vol, mcap
    except: return 0.0, 0.0, 0.0, 0.0

@st.cache_data(ttl=600)
def get_institutional_news():
    feeds = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]
    parsed_news = []
    for f in feeds:
        try:
            feed = feedparser.parse(f)
            for entry in feed.entries[:15]:
                parsed_news.append({"title": entry.title, "link": entry.link, "source": "INTELLIGENCE SOURCE"})
        except: pass
    return parsed_news

# ==============================================================================
# 05. LAYOUT DE COMANDO: HERO & TELEMETRIA
# ==============================================================================
st.markdown(f"""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div class="hero-tagline">The New Financial Architecture // 2026-2030</div>
    <p style="margin-top: 20px; color: #8b949e; max-width: 900px;">
        Este terminal monitoriza a execução da <b>Agenda de Soberania Financeira</b>. Rastreio absoluto de fluxos institucionais, 
        ISO 20022 e a transição para Ativos do Mundo Real (RWA). Ignoramos o ruído; focamos na matemática do Reset Global.
    </p>
</div>
""", unsafe_allow_html=True)

# Grelha de Telemetria
st.markdown("### 📡 MONITOR DE ABSORÇÃO INSTITUCIONAL (EUR €)")
cols = st.columns(4)
assets_to_show = ["BTC-EUR", "ETH-EUR", "XRP-EUR", "LINK-EUR", "QNT-EUR", "RNDR-EUR", "HBAR-EUR", "SOL-EUR"]

for i, ticker in enumerate(assets_to_show):
    price, chg, vol, mcap = get_live_stats(ticker)
    color = "#3fb950" if chg >= 0 else "#f85149"
    with cols[i % 4]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{ticker.split('-')[0]}</div>
            <div class="metric-value">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{chg:+.2f}% (24H)</div>
            <div style="font-size: 0.8rem; color: #8b949e; margin-top: 10px;">
                MCAP: € {mcap/1e9:.2f}B | VOL: € {vol/1e6:.2f}M
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

st.divider()

# ==============================================================================
# 06. ANÁLISE VISUAL E RADAR DE NOTÍCIAS
# ==============================================================================
col_chart, col_news = st.columns([1.8, 1])

with col_chart:
    st.markdown("### 📊 VETOR DE PREÇO TÁTICO: BITCOIN (€)")
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#238636', decreasing_line_color='#da3633')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=60, r=20, t=20, b=20), xaxis_rangeslider_visible=False, height=480,
                      yaxis=dict(showgrid=True, gridcolor='#30363d', tickprefix="€", showticklabels=True))
    st.plotly_chart(fig, use_container_width=True)

with col_news:
    st.markdown("### 📰 RADAR ROTATIVO (COINDESK STYLE)")
    st.markdown('<div class="news-container">', unsafe_allow_html=True)
    news_list = get_institutional_news()
    if news_list:
        # Lógica de rotação: mostra 5 de cada vez
        page = st.session_state.news_index % (len(news_list) // 5)
        for item in news_list[page*5 : (page+1)*5]:
            st.markdown(f"""
            <div class="news-item">
                <a href="{item['link']}" target="_blank" class="news-link">■ {item['title']}</a>
                <div class="news-source">{item['source']} // AGORA</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. EDUCAÇÃO PROFUNDA: O MANIFESTO DOS TRILIÕES
# ==============================================================================
st.markdown('<div class="edu-header">THINK TANK: A NOVA ORDEM FINANCEIRA</div>', unsafe_allow_html=True)

col_edu_1, col_edu_2 = st.columns(2)

with col_edu_1:
    st.markdown(f"""
    <div class="edu-content">
        <h3>I. Tokenização (RWA): O Software que Devora o Mundo</h3>
        A <span class="highlight">Tokenização de Ativos do Mundo Real (RWA)</span> é a representação digital de propriedades, ouro, ações e obrigações do tesouro 
        em redes blockchain (principalmente Ethereum). <br><br>
        Larry Fink (BlackRock) declarou que a tokenização é a "próxima geração dos mercados". Ao fragmentar um edifício de 100M€ em tokens de 1€, 
        a elite financeira ganha liquidez instantânea e controlo total. A JTM Capital posiciona-se na infraestrutura que permite esta transferência 
        de triliões do sistema analógico para o digital.
    </div>
    """, unsafe_allow_html=True)



with col_edu_2:
    st.markdown(f"""
    <div class="edu-content">
        <h3>II. ISO 20022: O Reset das Mensagens Bancárias</h3>
        O sistema SWIFT arcaico está a ser substituído pela norma <span class="highlight">ISO 20022</span>. Esta norma exige que as transações carreguem 
        metadados densos que os bancos tradicionais não conseguem processar em tempo real. <br><br>
        Protocolos como <b>XRP, XLM e QNT</b> foram desenhados nativamente para esta norma. Eles atuam como a ponte de liquidez. Quem detém estes ativos 
        detém as chaves da comunicação interbancária global de 2026 a 2030.
    </div>
    """, unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 08. DOSSIÊS TÁTICOS (MATRIZ DE RISCO)
# ==============================================================================
st.markdown("### 🔍 DOSSIÊS DE INFRAESTRUTURA")
tabs = st.tabs(list(ASSET_INTEL.keys()))

for i, name in enumerate(ASSET_INTEL.keys()):
    with tabs[i]:
        intel = ASSET_INTEL[name]
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown(f"**Função:** {intel['role']}")
            st.write(intel['vision'])
            st.markdown(f"""
            <table class="tactic-table">
                <tr><th>🟢 VANTAGENS INSTITUCIONAIS</th><th>🔴 RISCOS ESTRATÉGICOS</th></tr>
                <tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in intel['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in intel['cons']])}</ul></td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"**🔗 PARCEIROS DE ECOSSISTEMA:**")
            st.info(intel['partners'])
            st.markdown("**ESTADO DE ACUMULAÇÃO:**")
            st.warning("DCA ATIVO // MODO SOV (Soberania)")

st.divider()

# ==============================================================================
# 09. GLOSSÁRIO INSTITUCIONAL (EDUCAÇÃO DE MASSAS)
# ==============================================================================
st.markdown("### 📖 GLOSSÁRIO DA SOBERANIA")
c_g1, c_g2, c_g3 = st.columns(3)

with c_g1:
    st.write("**DCA (Dollar Cost Averaging):** Técnica militar de investimento. Compras cegas no dia 29 para ignorar a volatilidade e focar na acumulação de unidades.")
    st.write("**DePIN:** Redes de Infraestrutura Física Descentralizada. Uso de tokens para incentivar pessoas a partilharem hardware (ex: GPUs para IA).")

with c_g2:
    st.write("**Self-Custody:** O ato soberano de deter as suas chaves privadas na Trezor. Moedas na exchange não são suas; moedas na hardware wallet são o seu império.")
    st.write("**Settlement Layer:** A camada final e definitiva de liquidação de uma transação. O Ethereum é a Settlement Layer das finanças mundiais.")

with c_g3:
    st.write("**Smart Contracts:** Código que executa acordos automáticos. Substituem advogados, notários e bancos. Matemática inquebrável.")
    st.write("**CBDC:** Moedas Digitais de Bancos Centrais. A ferramenta de controlo absoluto do Estado que a JTM Capital ajuda a navegar.")

st.divider()

# ==============================================================================
# 10. RODAPÉ E REINICIALIZAÇÃO
# ==============================================================================
st.markdown(f"""
<div style="text-align: center; color: #484f58; font-family: 'JetBrains Mono'; padding: 20px;">
    JTM CAPITAL RESEARCH © 2026 | INFRAESTRUTURA DE ACESSO NÍVEL 5 | SÃO JOÃO DA MADEIRA, PORTUGAL<br>
    <em>"In math we trust, in sovereignty we live."</em>
</div>
""", unsafe_allow_html=True)

# Loop de Atualização e Rotação
if auto_refresh:
    st.session_state.news_index += 1
    time.sleep(30)
    st.rerun()
