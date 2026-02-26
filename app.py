import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time

# --- 1. CONFIGURAÇÃO DE COMANDO TÁTICO ---
st.set_page_config(page_title="JTM CAPITAL | Research", layout="wide", page_icon="⚡")

# Motor de Atualização Autônoma (60 Segundos)
st.sidebar.markdown("### ⚙️ CONTROLO DE SISTEMA")
auto_update = st.sidebar.toggle("ATIVAR RADAR AUTÔNOMO (60s)", value=True)
st.sidebar.caption("Monitorização do fluxo institucional em tempo real.")

# CSS Corporativo Premium
st.markdown("""
<style>
    .stApp { background-color: #040914; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -0.5px; }
    .hero-section { background: linear-gradient(90deg, #0f172a 0%, #040914 100%); border-bottom: 2px solid #2563eb; padding: 40px; border-radius: 10px; margin-bottom: 30px; }
    .hero-title { font-size: 3.8rem; background: -webkit-linear-gradient(#38bdf8, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; font-family: 'Courier New', monospace; font-weight: 900; }
    .crypto-card { background: linear-gradient(145deg, #0b1120, #0f172a); border: 1px solid #1e293b; padding: 25px; border-radius: 12px; height: 100%; transition: all 0.4s ease; border-top: 4px solid #38bdf8; }
    .crypto-card:hover { transform: translateY(-5px); border-top: 4px solid #f59e0b; box-shadow: 0 10px 25px rgba(56, 189, 248, 0.15); }
    .thesis-box { background-color: #0b1121; border: 1px solid #1e293b; padding: 30px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #10b981; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .news-container { background-color: #080c17; border: 1px solid #1e293b; padding: 20px; border-radius: 8px; height: 350px; overflow-y: auto; }
    .news-title { color: #38bdf8; font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; }
    .news-meta { color: #64748b; font-size: 0.75rem; text-transform: uppercase; font-weight: 600; margin-bottom: 12px; }
    [data-testid="stMetric"] { background-color: #080d1a; border: 1px solid #1e293b; border-left: 4px solid #38bdf8; padding: 15px; border-radius: 8px; }
    .highlight { color: #38bdf8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. CABEÇALHO DO THINK TANK ---
st.markdown('<div class="hero-section"><h1 class="hero-title">JTM CAPITAL RESEARCH</h1><h3>🌍 Monitorização de Transição RWA & ISO 20022</h3><p>Análise de infraestrutura matemática e fluxos de capital fiduciário para o novo sistema financeiro europeu e global.</p></div>', unsafe_allow_html=True)

# --- 3. TELEMETRIA TÁTICA (CONVERSÃO EUROS - €) ---
@st.cache_data(ttl=50)
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
    "BTC (ESCUDO)": "BTC-EUR",
    "ETH (BASE)": "ETH-EUR",
    "LINK (ORÁCULO)": "LINK-EUR",
    "XRP (ISO-1)": "XRP-EUR",
    "XLM (ISO-2)": "XLM-EUR",
    "QNT (INTEROP)": "QNT-EUR",
    "RNDR (DePIN)": "RNDR-EUR"
}

st.subheader("📡 VETORES DE LIQUIDEZ (EUR €)")
metric_cols = st.columns(len(assets))
for i, (name, ticker) in enumerate(assets.items()):
    price, change = get_market_data(ticker)
    metric_cols[i].metric(label=name, value=f"€ {price:,.3f}", delta=f"{change:+.2f}%")

st.divider()

# --- 4. CENTRO DE ANÁLISE: GRÁFICOS & RADAR DE NOTÍCIAS MULTI-FONTE ---
col_chart, col_news = st.columns([1.7, 1.3])

with col_chart:
    st.subheader("📊 Gráfico de Combate: Bitcoin (€)")
    @st.cache_data(ttl=900)
    def plot_asset_eur():
        df = yf.download("BTC-EUR", period="30d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=10, b=0), xaxis_rangeslider_visible=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
    plot_asset_eur()

with col_news:
    st.subheader("📰 Radar Institucional (Multi-Fonte)")
    st.markdown('<div class="news-container">', unsafe_allow_html=True)
    
    @st.cache_data(ttl=600)
    def fetch_global_news():
        urls = [
            ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
            ("CoinTelegraph", "https://cointelegraph.com/rss")
        ]
        all_news = []
        for source, url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:4]:
                    all_news.append({"title": entry.title, "date": entry.published[:16], "source": source, "link": entry.link})
            except:
                pass
        return all_news

    news_list = fetch_global_news()
    for item in news_list:
        st.markdown(f"<p class='news-title'><a href='{item['link']}' target='_blank' style='color:#38bdf8; text-decoration:none;'>■ {item['title']}</a></p>", unsafe_allow_html=True)
        st.markdown(f"<p class='news-meta'>{item['source']} | {item['date']}</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #1e293b; margin: 8px 0;'>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 5. O MANIFESTO DO IMPÉRIO JTM ---
st.header("A Arquitetura de 2030")
st.markdown("""
<div class="thesis-box">
    <h4 style="color: #10b981; margin-bottom: 10px;">A Liquidação do Dinheiro Fiduciário</h4>
    <p>O Euro e o Dólar perdem poder de compra diariamente devido à impressão descontrolada pelos Bancos Centrais. A transição não é uma possibilidade; é uma inevitabilidade matemática.</p>
    <p>A <span class="highlight">JTM CAPITAL</span> posiciona o seu capital na fundação do novo sistema. A tokenização de ativos (RWA) sobre redes blindadas por criptografia (como o Ethereum) e a comunicação interbancária instantânea (ISO 20022) substituem a burocracia humana por código inquebrável.</p>
</div>
""", unsafe_allow_html=True)

# --- 6. O PELOTÃO TÁTICO (OS ATIVOS) ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="crypto-card"><h3 style="color: #f7931a;">Bitcoin (BTC)</h3><p><b>A Base: Escudo de Reserva</b></p><p>Propriedade digital absoluta. A proteção final contra a inflação, absorvida agressivamente pela BlackRock e corporações.</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="crypto-card"><h3 style="color: #627eea;">Ethereum (ETH)</h3><p><b>A Base: Autoestrada Global</b></p><p>A camada de liquidação onde a tokenização de obrigações do tesouro e fundos RWA é executada através de Smart Contracts.</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="crypto-card"><h3 style="color: #2a5ada;">Chainlink (LINK)</h3><p><b>Sniper: Oráculo de Dados</b></p><p>A ponte de informação. Fornece o preço exato das ações e mercadorias reais para dentro da blockchain de forma descentralizada.</p></div>', unsafe_allow_html=True)

st.write("")

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown('<div class="crypto-card"><h3 style="color: #34d399;">XRP & XLM</h3><p><b>Sniper: Liquidez ISO 20022</b></p><p>As artérias do sistema bancário. Desenhadas para liquidações transfronteiriças instantâneas (CBDCs), substituindo a ineficiência do SWIFT.</p></div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="crypto-card"><h3 style="color: #94a3b8;">Quant (QNT)</h3><p><b>Sniper: O Sistema Operativo</b></p><p>O Overledger permite que blockchains privadas de bancos comuniquem com redes públicas de forma segura e certificada.</p></div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="crypto-card"><h3 style="color: #f43f5e;">Render (RNDR)</h3><p><b>Sniper: Infraestrutura DePIN</b></p><p>A economia da IA requer GPUs gigantescas. A rede Render distribui o poder computacional pelo mundo, desafiando a Amazon AWS e a Google Cloud.</p></div>', unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.85rem; font-family: Courier New;'>JTM CAPITAL © 2026 | PESQUISA INSTITUCIONAL INDEPENDENTE</p>", unsafe_allow_html=True)

# Loop de Atualização Autônoma
if auto_update:
    time.sleep(60)
    st.rerun()
