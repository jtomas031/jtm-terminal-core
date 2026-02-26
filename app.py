import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser

# --- 1. CONFIGURAÇÃO CORPORATIVA PÚBLICA ---
st.set_page_config(page_title="JTM CAPITAL | Research & Tese", layout="wide", page_icon="🏛️")

st.markdown("""
<style>
    .stApp { background-color: #020617; color: #cbd5e1; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #f8fafc; font-weight: 800; letter-spacing: -0.5px; }
    .hero-section { border-bottom: 1px solid #1e293b; padding-bottom: 30px; margin-bottom: 30px; }
    .hero-title { font-size: 3.5rem; color: #38bdf8; margin-bottom: 10px; font-family: 'Courier New', monospace; }
    .thesis-box { background-color: #0f172a; border: 1px solid #1e293b; padding: 25px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #38bdf8;}
    .crypto-card { background-color: #0b1120; border: 1px solid #1e293b; padding: 20px; border-radius: 8px; height: 100%; transition: 0.3s; }
    .crypto-card:hover { border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.1); }
    .highlight { color: #38bdf8; font-weight: bold; }
    
    /* Estilos Adicionados para Telemetria e Notícias */
    [data-testid="stMetric"] { background-color: #0f172a; border: 1px solid #1e293b; border-top: 3px solid #38bdf8; padding: 15px; border-radius: 5px; }
    .news-title { color: #38bdf8; font-weight: 600; font-size: 1.1rem; margin-bottom: 2px; }
    .news-date { color: #64748b; font-size: 0.8rem; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HERO SECTION (A MENSAGEM PRINCIPAL) ---
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">JTM CAPITAL RESEARCH</h1>', unsafe_allow_html=True)
st.markdown("### A Transição para a Economia da Inteligência Artificial e Tokenização Institucional.")
st.write("Não especulamos no ruído do retalho. Analisamos o fluxo de triliões de dólares da infraestrutura do amanhã.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. TELEMETRIA EM TEMPO REAL (TICKER TAPE INSTITUCIONAL) ---
@st.cache_data(ttl=300)
def get_market_data(ticker):
    try:
        df = yf.download(ticker, period="2d", interval="1h", progress=False)
        current_price = df['Close'].iloc[-1].item()
        open_price = df['Open'].iloc[0].item()
        change_pct = ((current_price - open_price) / open_price) * 100
        return current_price, change_pct
    except:
        return 0.0, 0.0

assets = {
    "BTC (RESERVA)": "BTC-USD",
    "ETH (INFRA)": "ETH-USD",
    "LINK (ORÁCULO)": "LINK-USD",
    "XRP (PAGAMENTOS)": "XRP-USD",
    "QNT (INTEROP)": "QNT-USD"
}

metric_cols = st.columns(len(assets))
for i, (name, ticker) in enumerate(assets.items()):
    price, change = get_market_data(ticker)
    metric_cols[i].metric(label=name, value=f"${price:,.2f}", delta=f"{change:+.2f}%")

st.divider()

# --- 4. CENTRO DE INTELIGÊNCIA: GRÁFICOS & RADAR DE NOTÍCIAS ---
col_chart, col_news = st.columns([1.8, 1])

with col_chart:
    st.subheader("Análise Vetorial: Escudo & Autoestrada")
    
    @st.cache_data(ttl=900)
    def plot_asset(ticker, title):
        df = yf.download(ticker, period="30d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#38bdf8', decreasing_line_color='#ef4444')])
            fig.update_layout(title=title, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=40, b=0), xaxis_rangeslider_visible=False, height=320)
            st.plotly_chart(fig, use_container_width=True)

    plot_asset("BTC-USD", "Vetor de Preço: BITCOIN (30 Dias)")
    plot_asset("ETH-USD", "Vetor de Preço: ETHEREUM (30 Dias)")

with col_news:
    st.subheader("Radar de Fluxo Institucional")
    st.write("Agregação automatizada das principais manchetes de infraestrutura digital.")
    
    @st.cache_data(ttl=1200)
    def fetch_news():
        try:
            feed = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")
            return feed.entries[:6]
        except:
            return []
            
    news = fetch_news()
    for item in news:
        st.markdown(f"<p class='news-title'>■ {item.title}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='news-date'>Publicado: {item.published[:16]} | Fonte: CoinDesk</p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 10px 0; border-color: #1e293b;'>", unsafe_allow_html=True)

st.divider()

# --- 5. A NOSSA VISÃO (O MANIFESTO) ---
st.header("A Nossa Tese para 2030")
st.markdown("""
<div class="thesis-box">
    <h4>O Fim do Sistema Fiduciário Obsoleto</h4>
    <p>Acreditamos que o sistema financeiro tradicional (SWIFT, compensação bancária em papel) está a atingir o seu limite físico e tecnológico. A <span class="highlight">Tokenização de Ativos do Mundo Real (RWA)</span> e a ascensão da <span class="highlight">Inteligência Artificial</span> exigem uma infraestrutura financeira que opere 24/7, sem confiança em intermediários humanos e à velocidade da luz.</p>
    <p>A criptografia não é uma "moeda alternativa"; é o software de base de dados que a BlackRock, Wall Street e os agentes de IA vão usar para transacionar valor na próxima década.</p>
</div>
""", unsafe_allow_html=True)

# --- 6. OS PILARES DA INFRAESTRUTURA (AS CRIPTOS) ---
st.header("Os Motores da Nova Economia")
st.write("A nossa pesquisa foca-se exclusivamente em protocolos com adoção institucional verificada e utilidade matemática.")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="crypto-card">
        <h3 style="color: #627eea;">Ethereum (ETH)</h3>
        <p><b>A Autoestrada Global.</b></p>
        <p>O Ethereum não é apenas dinheiro; é o computador mundial. É a camada de liquidação onde os grandes fundos e bancos estão a emitir fundos tokenizados. Se a internet de 1990 transmitia informação, o Ethereum transmite propriedade e contratos blindados por matemática.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="crypto-card">
        <h3 style="color: #2a5ada;">Chainlink (LINK)</h3>
        <p><b>O Oráculo de Dados.</b></p>
        <p>A blockchain é cega. Ela não sabe qual é o preço do ouro, o clima, ou se um contentor chegou ao porto. A Chainlink é a ponte que liga os dados do mundo real (SWIFT, Bancos) aos contratos inteligentes. Sem oráculos, a tokenização corporativa é impossível.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="crypto-card">
        <h3 style="color: #f7931a;">Bitcoin (BTC)</h3>
        <p><b>O Escudo de Reserva.</b></p>
        <p>Num mundo de inflação programada pelos Bancos Centrais, o Bitcoin representa o primeiro ativo de escassez absoluta e inconfiscável descoberto pela humanidade. É a fundação de confiança que baliza todo o restante mercado de ativos digitais.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

c4, c5 = st.columns(2)
with c4:
    st.markdown("""
    <div class="crypto-card">
        <h3 style="color: #cbd5e1;">Quant (QNT) / Ripple (XRP)</h3>
        <p><b>A Interoperabilidade Bancária.</b></p>
        <p>Os Bancos Centrais (CBDCs) não vão usar redes públicas não reguladas para todas as operações. Eles precisam de pontes corporativas. Protocolos que conectam o sistema financeiro legado (ISO 20022) com as novas redes distribuídas são cruciais para a transição institucional.</p>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="crypto-card">
        <h3 style="color: #10b981;">Redes DePIN</h3>
        <p><b>A Infraestrutura Física.</b></p>
        <p>A próxima revolução não acontece apenas no software. Redes de Infraestrutura Física Descentralizada (DePIN) usam tokens para incentivar pessoas a partilharem poder computacional (GPUs para IA), armazenamento ou dados de mapeamento (GPS), quebrando o monopólio das Big Techs.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 7. O PORQUÊ (CONCLUSÃO) ---
st.header("Porquê Esta Classe de Ativos?")
st.write("""
1. **Soberania:** Pela primeira vez na história, possuis um ativo ao portador que não depende da permissão de um banco ou governo para existir.
2. **Assimetria:** Estamos a investir na canalização da internet do futuro enquanto 99% da população mundial ainda discute o preço diário.
3. **Imunidade Inflacionária:** A infraestrutura de ativos digitais está desenhada matematicamente para proteger a energia económica do colapso fiduciário.
""")

st.markdown("<br><br><p style='text-align: center; color: #475569; font-size: 0.8rem;'>JTM CAPITAL © 2026 | Operando do Nó Estratégico em Portugal | Pesquisa Institucional Independente</p>", unsafe_allow_html=True)
