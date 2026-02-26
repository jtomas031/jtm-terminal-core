import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd

# --- 1. CONFIGURAÇÃO DE COMANDO (NEURO-DESIGN) ---
st.set_page_config(page_title="JTM CAPITAL | Intelligence", layout="wide", page_icon="⚡")

# Radar Autônomo (30 Segundos)
st.sidebar.markdown("### ⚙️ COMANDO CENTRAL")
auto_update = st.sidebar.toggle("🟢 RADAR ATIVO (30s)", value=True)
st.sidebar.caption("Sincronização com o mercado a cada 30 segundos.")

# CSS: Dopamina Institucional (Neon, Glassmorphism, Gradientes)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #02040a; color: #e2e8f0; font-family: 'Inter', sans-serif; background-image: radial-gradient(circle at 50% 0%, #111827 0%, #02040a 70%); }
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Hero Section Dinâmica */
    .hero-box { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(56, 189, 248, 0.2); padding: 40px; border-radius: 16px; margin-bottom: 40px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-top: 2px solid #38bdf8; }
    .hero-title { font-size: 4.5rem; background: linear-gradient(to right, #38bdf8, #818cf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; font-weight: 800; }
    .pulse-live { animation: pulse 2s infinite; color: #ef4444; font-weight: bold; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    
    /* Cartões de Telemetria (Glassmorphism) */
    .metric-card { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s; border-left: 4px solid #38bdf8; }
    .metric-card:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0 15px 35px rgba(56, 189, 248, 0.2); border-left: 4px solid #10b981; }
    .m-title { font-size: 1.2rem; color: #94a3b8; font-weight: 600; font-family: 'Rajdhani'; }
    .m-price { font-size: 2.2rem; color: #ffffff; font-weight: 800; margin: 5px 0; }
    .m-data { font-size: 0.85rem; color: #cbd5e1; display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }
    
    /* Artigos Educativos */
    .article-box { background: linear-gradient(145deg, #0f172a, #02040a); padding: 35px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 30px; font-size: 1.1rem; line-height: 1.7; color: #cbd5e1; border-right: 4px solid #34d399; }
    .article-header { color: #38bdf8; font-size: 2.2rem; margin-bottom: 20px; border-bottom: 1px solid #1e293b; padding-bottom: 10px; }
    
    /* Tabelas Prós e Contras */
    .pc-table { width: 100%; border-collapse: collapse; margin-top: 15px; background: rgba(15, 23, 42, 0.5); border-radius: 8px; overflow: hidden; }
    .pc-table th, .pc-table td { border: 1px solid #1e293b; padding: 15px; text-align: left; }
    .pc-table th { background-color: rgba(30, 41, 59, 0.8); color: #38bdf8; font-size: 1.1rem; }
    .pro-td { border-left: 3px solid #10b981 !important; color: #a7f3d0; }
    .con-td { border-left: 3px solid #ef4444 !important; color: #fecaca; }
</style>
""", unsafe_allow_html=True)

# --- 2. CABEÇALHO HERO ---
st.markdown("""
<div class="hero-box">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.4rem; color: #94a3b8; font-family: 'Rajdhani'; letter-spacing: 3px;">TERMINAL DE FLUXOS INSTITUCIONAIS E RWA</div>
    <div style="margin-top: 15px;"><span class="pulse-live">● LIVE</span> <span style="color:#64748b;">| Sincronização de Mercado Ativa</span></div>
</div>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE CÁLCULO NATIVO (IMUNE A BLOQUEIOS) ---
# Oferta circulante hardcoded para cálculo instantâneo de Market Cap
SUPPLY_DATA = {
    "BTC-EUR": 19_650_000,
    "ETH-EUR": 120_000_000,
    "LINK-EUR": 587_000_000,
    "XRP-EUR": 54_800_000_000,
    "QNT-EUR": 14_500_000,
    "XLM-EUR": 28_700_000_000,
    "RNDR-EUR": 388_000_000
}

@st.cache_data(ttl=25)
def fetch_tactical_data(ticker):
    try:
        # Puxamos dados de 5 dias para garantir que há sempre histórico, mesmo em fuso horários diferentes
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if len(df) >= 2:
            current = df['Close'].iloc[-1].item()
            prev = df['Close'].iloc[-2].item()
            change = ((current - prev) / prev) * 100
            vol = df['Volume'].iloc[-1].item()
        else:
            return 0.0, 0.0, 0, 0
            
        mcap = current * SUPPLY_DATA.get(ticker, 0)
        return current, change, vol, mcap
    except:
        return 0.0, 0.0, 0, 0

def format_number(num):
    if num >= 1_000_000_000: return f"€ {(num / 1_000_000_000):.2f} B"
    if num >= 1_000_000: return f"€ {(num / 1_000_000):.2f} M"
    return f"€ {num:,.0f}"

assets = {"Bitcoin": "BTC-EUR", "Ethereum": "ETH-EUR", "Chainlink": "LINK-EUR", "Ripple": "XRP-EUR", "Quant": "QNT-EUR", "Stellar": "XLM-EUR", "Render": "RNDR-EUR"}

st.markdown("<h2><span style='color:#38bdf8;'>01.</span> TELEMETRIA GLOBAL</h2>", unsafe_allow_html=True)

# Grelha de Cartões Dopamina
cols = st.columns(4)
for i, (name, ticker) in enumerate(assets.items()):
    c, chg, v, m = fetch_tactical_data(ticker)
    color = "#10b981" if chg >= 0 else "#ef4444"
    arrow = "▲" if chg >= 0 else "▼"
    
    with cols[i % 4]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {c:,.2f}</div>
            <div style="color: {color}; font-weight: 800; font-size: 1.1rem; text-shadow: 0 0 10px {color}40;">{arrow} {abs(chg):.2f}%</div>
            <div class="m-data">
                <span><b>Vol:</b> {format_number(v)}</span>
                <span><b>MCap:</b> {format_number(m)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

st.divider()

# --- 4. SECÇÃO DE EDUCAÇÃO INTENSIVA (ISO & RWA) ---
st.markdown("<h2><span style='color:#38bdf8;'>02.</span> INTELIGÊNCIA DE INFRAESTRUTURA</h2>", unsafe_allow_html=True)

col_ed1, col_ed2 = st.columns(2)

with col_ed1:
    st.markdown('<div class="article-box">', unsafe_allow_html=True)
    st.markdown('<div class="article-header">A Arquitetura ISO 20022</div>', unsafe_allow_html=True)
    st.write("""
    A transição para a **ISO 20022** não é uma escolha tecnológica, é um mandato global imposto aos bancos centrais. O sistema atual (SWIFT) é um telégrafo da era moderna. A nova norma transforma o dinheiro em *dados estruturados*.
    
    A grande revelação que o retalho ignora: a infraestrutura bancária não tem largura de banda para processar estas mensagens gigantescas em tempo real. É por isso que redes como a **Ripple (XRP)** e **Stellar (XLM)** foram construídas. Elas atuam como os cabos de fibra ótica de liquidação, permitindo que um banco na Europa envie milhões para o Japão em 3 segundos, a custo zero, em total conformidade legal.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col_ed2:
    st.markdown('<div class="article-box">', unsafe_allow_html=True)
    st.markdown('<div class="article-header">Tokenização: A Devoração do Mundo Real</div>', unsafe_allow_html=True)
    st.write("""
    A **Tokenização (RWA - Real World Assets)** é o processo de colocar ativos físicos e financeiros (imóveis, arte, obrigações do tesouro) na blockchain. Larry Fink, CEO da BlackRock, declarou que "a tokenização de ativos é a próxima geração dos mercados".
    
    Porquê? **Liquidez absoluta.** Um edifício de escritórios em Nova Iorque pode ser tokenizado e negociado em frações de cêntimo num telemóvel em Lisboa, no domingo à noite. Para que isto aconteça, a infraestrutura base **Ethereum** fornece a segurança, e a **Chainlink** injeta os preços reais nos contratos matemáticos.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 5. RAIOS-X DE ATIVOS (ANÁLISE E NOTÍCIAS) ---
st.markdown("<h2><span style='color:#38bdf8;'>03.</span> DOSSIÊS TÁTICOS (PRÓS & CONTRAS)</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=900)
def fetch_news_for_asset(keyword):
    urls = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]
    news = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if keyword.lower() in entry.title.lower():
                    news.append({"title": entry.title, "link": entry.link, "date": entry.published[:16]})
                if len(news) >= 4: break
        except: pass
    return news

tabs = st.tabs(list(assets.keys()))

def render_dossier(name, ticker, pros, cons, keyword):
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown(f"### MATRIZ DE RISCO: {name.upper()}")
        st.markdown(f"""
        <table class="pc-table">
            <tr><th>🟢 VANTAGENS INSTITUCIONAIS</th><th>🔴 VULNERABILIDADES</th></tr>
            <tr>
                <td class="pro-td"><ul>{''.join([f"<li>{p}</li>" for p in pros])}</ul></td>
                <td class="con-td"><ul>{''.join([f"<li>{c}</li>" for c in cons])}</ul></td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"### FEED DE INTELIGÊNCIA ({name})")
        news = fetch_news_for_asset(keyword)
        if news:
            for item in news:
                st.markdown(f"<div style='background:rgba(15,23,42,0.6); padding:10px; border-radius:6px; margin-bottom:8px; border-left:2px solid #38bdf8;'><a href='{item['link']}' target='_blank' style='color:#cbd5e1; text-decoration:none; font-weight:600;'>{item['title']}</a><br><small style='color:#64748b;'>{item['date']}</small></div>", unsafe_allow_html=True)
        else:
            st.info(f"O radar não detetou movimentações institucionais públicas para {name} nas últimas horas.")

with tabs[0]: render_dossier("Bitcoin", "BTC-EUR", ["Absorção total por ETFs da BlackRock e Wall Street.", "Reserva de valor descentralizada imune a inflação fiduciária.", "Rede computacional mais segura do planeta."], ["Falta de utilidade para contratos inteligentes nativos.", "Tecnologia rudimentar comparada a redes de nova geração."], "bitcoin")
with tabs[1]: render_dossier("Ethereum", "ETH-EUR", ["Padrão global para emissão de fundos tokenizados (RWA).", "Maior capital intelectual e programadores do mundo.", "Economia deflacionária em picos de utilização da rede."], ["Custos de operação (Gas fees) proibitivos para retalho.", "Fragmentação da liquidez por redes de camada 2 (L2)."], "ethereum")
with tabs[2]: render_dossier("Chainlink", "LINK-EUR", ["Ponte indispensável entre o mundo real e o código.", "Parcerias atestadas com o consórcio SWIFT e DTCC.", "Sem concorrência séria no setor de Oráculos corporativos."], ["Modelo de tokenomics complexo.", "Não possui a narrativa de 'dinheiro', dificultando a captação de retalho."], "chainlink")
with tabs[3]: render_dossier("Ripple", "XRP-EUR", ["Desenhado exclusivamente para liquidez bancária (ISO 20022).", "Velocidade extrema de liquidação interbancária.", "Claridade jurídica estabelecida no mercado norte-americano."], ["Forte rejeição pela comunidade 'purista' de criptomoedas.", "A empresa Ripple detém grande parte da oferta circulante."], "ripple")
with tabs[4]: render_dossier("Quant", "QNT-EUR", ["O Sistema Operativo para Moedas de Bancos Centrais (CBDCs).", "Permite que diferentes blockchains institucionais comuniquem.", "Tokenomics de extrema escassez (apenas ~14 milhões)."], ["Projeto altamente corporativo, fechado e de código privado.", "Baixa liquidez devido ao desinteresse de especuladores de retalho."], "quant")
with tabs[5]: render_dossier("Stellar", "XLM-EUR", ["Infraestrutura preferencial para pagamentos globais de baixo custo.", "Compatível com a norma ISO 20022 e suportado pela IBM.", "Permite a digitalização rápida de moedas fiduciárias."], ["Permanece na sombra do XRP em termos de marketing institucional.", "Historicamente possui grande inflação da oferta circulante."], "stellar")
with tabs[6]: render_dossier("Render", "RNDR-EUR", ["Alimenta a infraestrutura física (GPUs) para a expansão da IA.", "Descentraliza o poder computacional monopolizado pela Amazon.", "Crescimento exponencial de clientes no setor de renderização e IA."], ["Altamente exposto à volatilidade da narrativa de Inteligência Artificial.", "Dependência tecnológica do hardware global disponível."], "render")

st.divider()
st.markdown("<p style='text-align: center; color: #475569; font-family: Rajdhani;'>JTM CAPITAL // PROTOCOLO DE ACUMULAÇÃO A 30 SEG // DESTINO FINAL: TREZOR</p>", unsafe_allow_html=True)

# Loop de 30 Segundos
if auto_update:
    time.sleep(30)
    st.rerun()
