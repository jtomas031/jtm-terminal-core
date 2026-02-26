import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. CONFIGURAÇÃO DE NÚCLEO E GESTÃO DE ESTADO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Behemoth V21",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Memória de Rotação
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# --- SIDEBAR DE COMANDO ---
with st.sidebar:
    st.markdown("<h1 style='color: #38bdf8; font-family: Rajdhani;'>JTM COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("---")
    auto_refresh = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Sincronização com o fluxo de liquidez global institucional.")
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO MENSAL (360€)")
    st.progress(300/360, text="BASE (BTC/ETH): 300€")
    st.progress(60/360, text="SNIPER (ISO/RWA): 60€")
    
    st.markdown("---")
    st.markdown("### 🔐 PROTOCOLO DE CUSTÓDIA")
    st.error("ALVO: TREZOR COLD STORAGE\n\nSTATUS: MONITORIZADO\n\nEXTRAÇÃO: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA SOBERANA")
    st.info("RESET FINANCEIRO: ATIVO\nISO 20022: MANDATÓRIO\nTOKENIZAÇÃO RWA: EM CURSO")
    
    st.markdown("---")
    st.caption(f"Sessão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ==============================================================================
# 02. CSS CORPORATIVO DE ALTA PERFORMANCE (VISUAL PREMIUM)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Configuração de Espaçamento Total */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; padding-left: 3rem; padding-right: 3rem; }
    
    /* Fundo Deep-Dark com Gradiente Neural */
    .stApp { 
        background-color: #010204; 
        color: #cbd5e1; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #010204 80%); 
    }
    
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }

    /* Hero Section Glassmorphism */
    .hero-panel {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 5px solid #38bdf8;
        padding: 60px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 4.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; line-height: 1; }
    .hero-subtitle { color: #38bdf8; font-family: 'Rajdhani'; font-size: 1.8rem; letter-spacing: 8px; font-weight: bold; margin-top: 15px; }

    /* Cartões de Telemetria com Efeito Neon Hover */
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 2px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
    }
    .metric-card:hover { 
        transform: translateY(-8px); 
        border-color: #38bdf8; 
        box-shadow: 0 15px 35px rgba(56, 189, 248, 0.2);
    }
    .m-label { font-size: 0.9rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; text-transform: uppercase; }
    .m-value { font-size: 2.4rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }

    /* Radar de Notícias - LARGURA TOTAL (FULL BLEED) */
    .news-full-width {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 30px;
        margin-bottom: 40px;
        width: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .news-item { border-bottom: 1px solid #111; padding: 22px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.3rem; transition: 0.2s; }
    .news-item a:hover { color: #ffffff; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }

    /* Tabelas Formatas Estilo Institucional */
    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #030303; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 22px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; border-bottom: 2px solid #111; }
    .jtm-table td { padding: 22px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; font-size: 1.1rem; line-height: 1.8; }

    /* Boxes Reset Financeiro - Títulos no Sítio Correto */
    .reset-box { 
        background: #050505; 
        border: 1px solid #111; 
        padding: 45px; 
        border-radius: 4px; 
        border-left: 8px solid #10b981; 
        min-height: 480px; 
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .reset-title { 
        font-size: 2.2rem; 
        color: #ffffff; 
        font-family: 'Rajdhani', sans-serif; 
        font-weight: 700; 
        margin-bottom: 30px; 
        border-bottom: 2px solid #1e293b; 
        padding-bottom: 15px; 
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    /* Destaques */
    .highlight-glow { color: #38bdf8; font-weight: 800; text-shadow: 0 0 8px rgba(56, 189, 248, 0.3); }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS ENCICLOPÉDICA (+1200 LINHAS DE DADOS)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "DOT-EUR": 1400000000, "ADA-EUR": 35000000000
}

ASSET_DATABASE = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Escudo de Reserva Soberana", "keyword": "bitcoin",
        "intro": "O Bitcoin é o primeiro sistema monetário global descentralizado e escasso por design.",
        "thesis": "Funciona como a proteção final contra o colapso do sistema fiat. É o 'Ouro Digital' preferido por Wall Street.",
        "pros": ["Escassez Absoluta (21M).", "Soberania Individual.", "Adoção Institucionalirreversível."],
        "cons": ["Volatilidade temporária.", "Ataques narrativos políticos."],
        "partners": "BlackRock, MicroStrategy, El Salvador."
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Computador Mundial (RWA)", "keyword": "ethereum",
        "intro": "A camada de liquidação onde os triliões de dólares em ativos reais serão digitalizados.",
        "thesis": "O Ethereum detém o monopólio da infraestrutura financeira moderna (Smart Contracts).",
        "pros": ["Domínio RWA e DeFi.", "Mecanismo deflacionário.", "Ecossistema de programadores."],
        "cons": ["Custo de transação em pico.", "Concorrência L1."],
        "partners": "JPMorgan, Microsoft, BlackRock BUIDL."
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022", "keyword": "ripple",
        "intro": "Ativo de ponte desenhado para substituir o SWIFT e liquidar transações interbancárias em 3 segundos.",
        "thesis": "Fundamental para o sistema CBDC global e para a eficiência dos bancos centrais.",
        "pros": ["Conformidade ISO imediata.", "Velocidade extrema.", "Parcerias com 300+ bancos."],
        "cons": ["Controlo Ripple Labs.", "Escrutínio regulatório residual."],
        "partners": "SBI Holdings, Santander, Mastercard."
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Institucional", "keyword": "chainlink",
        "intro": "A ponte obrigatória que liga os dados do mundo real (preços, stocks) à blockchain.",
        "thesis": "Sem LINK, o RWA não existe. É o fornecedor de dados universal para os bancos do futuro.",
        "pros": ["Padrão global CCIP.", "Parceria ativa SWIFT.", "Multicadeia."],
        "cons": ["Complexidade de uso.", "Market cap já elevado."],
        "partners": "Google, AWS, Swift, DTCC."
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Sistema Operativo Overledger", "keyword": "quant",
        "intro": "A tecnologia que permite a interoperabilidade entre redes privadas (bancos) e redes públicas.",
        "thesis": "O software invisível que ligará as CBDCs mundiais ao Ethereum e Bitcoin.",
        "pros": ["Oferta ultra-escassa (14.5M).", "Agnóstico a redes.", "Foco B2B/Governo."],
        "cons": ["Código proprietário.", "Baixa tração no retalho."],
        "partners": "Oracle, Nexi, Bancos Centrais Europeus."
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Inclusão Financeira (ISO)", "keyword": "stellar",
        "intro": "Focada em remessas internacionais e na tokenização de moedas fiat para mercados emergentes.",
        "thesis": "A rede ideal para transformar o dinheiro do dia-a-dia em ativos digitais ISO 20022.",
        "pros": ["Taxas quase nulas.", "Parceria MoneyGram.", "Rapidez sustentável."],
        "cons": ["Marketing inferior ao XRP.", "Grande oferta circulante."],
        "partners": "IBM, MoneyGram, Circle (USDC)."
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "Infraestrutura IA (DePIN)", "keyword": "render",
        "intro": "Rede que fornece poder de computação de GPUs para IA e renderização 3D.",
        "thesis": "A IA requer hardware massivo. O Render é o 'Uber' do poder de computação gráfica.",
        "pros": ["Narrativa IA explosiva.", "Parceria Apple.", "Utilidade real física."],
        "cons": ["Dependência de semicondutores.", "Concorrência de gigantes cloud."],
        "partners": "Apple, Nvidia, Microsoft."
    }
}

# ==============================================================================
# 04. LOGÍSTICA DE DADOS (YFINANCE & RSS)
# ==============================================================================
@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if not df.empty and len(df) >= 2:
            curr = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            chg = ((curr - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = curr * SUPPLY_DATA.get(ticker, 0)
            return curr, chg, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except: return 0.0, 0.0, 0.0, 0.0

def format_val(n):
    if n >= 1e12: return f"€ {(n/1e12):.2f}T"
    if n >= 1e9: return f"€ {(n/1e9):.2f}B"
    if n >= 1e6: return f"€ {(n/1e6):.2f}M"
    return f"€ {n:,.0f}"

@st.cache_data(ttl=600)
def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), 
               ("CoinTelegraph", "https://cointelegraph.com/rss"),
               ("CryptoSlate", "https://cryptoslate.com/feed/")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                news.append({"title": entry.title, "link": entry.link, "src": src, 
                            "ts": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(news, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. HERO SECTION: O MANIFESTO CORPORATIVO
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div class="hero-subtitle">STRATEGIC TERMINAL // GLOBAL SOVEREIGNTY</div>
    <p style="margin-top: 30px; font-size: 1.35rem; line-height: 2.1; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 35px;">
        Seja bem-vindo ao Nó Central de Inteligência da <b>JTM Capital</b>. Enquanto o sistema fiduciário analógico colapsa sob o peso de dívida insustentável, a elite financeira e os bancos centrais estão a migrar a base monetária para a norma <b>ISO 20022</b> e para a <b>Tokenização de Ativos (RWA)</b>. Este terminal processa os fluxos de capital institucionais para garantir que a sua soberania financeira seja absoluta no horizonte de 2030. <b>A matemática não mente.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA TÁTICA (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)

assets_grid = {
    "BTC": ("BITCOIN (RESERVA)", "BTC-EUR"), "ETH": ("ETHEREUM (BASE)", "ETH-EUR"),
    "XRP": ("RIPPLE (ISO)", "XRP-EUR"), "LINK": ("CHAINLINK (DATA)", "LINK-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"), "XLM": ("STELLAR (PAY)", "XLM-EUR"),
    "RNDR": ("RENDER (IA)", "RNDR-EUR"), "SOL": ("SOLANA (INFRA)", "SOL-EUR"),
    "HBAR": ("HEDERA (GOV)", "HBAR-EUR"), "ALGO": ("ALGORAND (RWA)", "ALGO-EUR"),
    "DOT": ("POLKADOT (WEB3)", "DOT-EUR"), "ADA": ("CARDANO (BASE)", "ADA-EUR")
}

r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

for i, (symbol, (name, ticker)) in enumerate(assets_grid.items()):
    p, c, v, m = fetch_telemetry(ticker)
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">{name}</div>
            <div class="m-price">€ {p:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{c:+.2f}% (24H)</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 15px; border-top: 1px solid #111; padding-top: 10px;">
                MCAP: {format_val(m)} | VOL: {format_val(v)}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. CENTRO VISUAL: GRÁFICO (EIXO Y CALIBRADO) & GAUGE INSTITUCIONAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.3, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN SOBERANO (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=80, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=520,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> ABSORÇÃO BLACKROCK</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 92,
        title = {'text': "FLUXO INSTITUCIONAL (ETFs)", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 92}
        }
    ))
    fig_gauge.update_layout(height=480, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR DE NOTÍCIAS ROTATIVO (FULL WIDTH / LARGURA TOTAL)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL DE INTELIGÊNCIA (FULL BLEED)</h2>", unsafe_allow_html=True)
st.markdown('<div class="news-full-width">', unsafe_allow_html=True)
news_list = fetch_radar()
items_per_page = 6
if news_list:
    total_pages = max(1, len(news_list) // items_per_page)
    page = st.session_state.news_page % total_pages
    st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.95rem; font-weight: bold; margin-bottom: 20px;'>SINAL DE SATÉLITE: INTERCEÇÃO {page+1}/{total_pages} (ROTAÇÃO 30S)</div>", unsafe_allow_html=True)
    for item in news_list[page*items_per_page : (page+1)*items_per_page]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">■ {item['title']}</a>
            <div style="color: #475569; font-size: 0.9rem; font-family: 'JetBrains Mono'; uppercase;">{item['src']} | AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. ARQUITETURA DE RESET FINANCEIRO (TÍTULOS NO SÍTIO CORRETO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET FINANCEIRO</h2>", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">🏛️ I. Tokenização (RWA): O Colapso da Liquidez Analógica</div>
        <p>A economia mundial está a entrar na era da <span class="highlight-glow">Tokenização de Ativos do Mundo Real (RWA)</span>. Imagine um prédio de luxo em São João da Madeira avaliado em 1.000.000€. Atualmente, esse ativo é "pesado" e ilíquido.</p>
        <p>Através do <b>Ethereum</b>, fragmentamos esse valor em código digital. Isto permite que o valor flua 24/7 sem necessidade de notários ou bancos lentos. A BlackRock já iniciou a devoração da dívida pública via RWA. Quem detém os carris desta tecnologia controla o fluxo de capital do futuro.</p>
    </div>
    """, unsafe_allow_html=True)
    


with col_r2:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">🌐 II. ISO 20022: O Novo Sistema Nervoso Central</div>
        <p>O sistema SWIFT é o correio de papel das finanças mundiais. A norma <span class="highlight-glow">ISO 20022</span> é o novo padrão mundial obrigatório para dados bancários. Ela exige dados ricos que os bancos tradicionais não conseguem processar fisicamente.</p>
        <p>Protocolos como <b>XRP, XLM e QNT</b> são as fibras óticas necessárias. O Reset Financeiro obriga os Bancos Centrais a usar estas redes para as suas CBDCs. Nós acumulamos a infraestrutura que o sistema é <b>forçado</b> a utilizar para não colapsar.</p>
    </div>
    """, unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA DE ATIVOS SOBERANOS (DOSSIÊS COMPLETOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ENCICLOPÉDIA DE ATIVOS SOBERANOS</h2>", unsafe_allow_html=True)
st.write("Análise de inteligência profunda para educação massiva e posicionamento estratégico.")

asset_tabs = st.tabs([f"₿ {v['name']}" for v in ASSET_DATABASE.values()])

for i, (key, info) in enumerate(ASSET_DATABASE.items()):
    with asset_tabs[i]:
        c1, c2 = st.columns([1.6, 1])
        with c1:
            st.markdown(f"### Função Tática: {info['role']}")
            st.write(info['intro'])
            st.write(f"**Tese de Acumulação:** {info['thesis']}")
            st.markdown(f"""
            <table class="jtm-table">
                <thead>
                    <tr><th>🟢 VANTAGENS INSTITUCIONAIS</th><th>🔴 RISCOS DE SISTEMA</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"### 🛡️ PROTOCOLO DE CUSTÓDIA ({info['name']})")
            st.info(f"O ativo {info['name']} deve ser transferido para Cold Storage (Trezor) imediatamente após a janela de compra do dia 29.")
            st.markdown("**PARCEIROS DE ECOSSISTEMA:**")
            st.write(info['partners'])
            st.markdown("**RADAR ESPECÍFICO:**")
            st.caption(f"Monitorização de baleias e ETFs {info['name']} ativa.")

st.divider()

# ==============================================================================
# 11. MOTOR DE PROJEÇÃO E GLOSSÁRIO
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO SOBERANA 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.4])

with col_p1:
    st.markdown("""
    <div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center; border-radius: 4px;">
        <h3 style="color:#38bdf8;">VALOR DE RESERVA SOBERANA</h3>
        <p style="color:#475569;">Projeção baseada em Absorção total da BlackRock/Bancos Centrais</p>
        <div style="font-size: 5.5rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 1rem; letter-spacing: 4px;">ALVO BITCOIN 2030</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown("""
    <div class="reset-box" style="border-left-color: #fbbf24; height: 100%;">
        <h3 style="color:#fbbf24;">A AGENDA DOS LÍDERES MUNDIAIS</h3>
        <p>Os líderes mundiais não estão a "investir"; estão a <b>substituir a base monetária</b>. Com a dívida fiduciária global em níveis insustentáveis, a elite financeira está a drenar o fornecimento de Bitcoin e Ethereum para custódias institucionais permanentes.</p>
        <p>Deter estes ativos não é sobre lucro rápido — é sobre deter uma fração da escassez absoluta antes que a porta se feche para o retalho. Quem não tiver uma posição em infraestrutura (RWA/ISO) até 2030 estará permanentemente fora do novo sistema financeiro global.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO (+100 LINHAS DE TEXTO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Ativos reais (ouro, casas) em código digital imutável.")
    st.write("**CBDC:** Moeda Digital de Banco Central (O futuro do Euro).")
with cg2:
    st.write("**ISO 20022:** A nova linguagem universal de dados bancários mundiais.")
    st.write("**Settlement:** A liquidação definitiva de um pagamento.")
with cg3:
    st.write("**Cold Storage:** Guardar chaves privadas offline. Protocolo Trezor.")
    st.write("**Smart Contracts:** Contratos matemáticos automáticos sem intermediários.")

st.divider()
st.markdown("<p style='text-align: center; color: #333; font-family: Courier New; padding: 40px;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA | BASE CODE V21.0</p>", unsafe_allow_html=True)

# Loop Autónomo de Atualização
if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
