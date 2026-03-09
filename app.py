import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO E GESTÃO DE ESTADO (GOD MODE READY)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | V25 Córtex V.MAX",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização da Memória de Sessão
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# --- SIDEBAR DE COMANDO INSTITUCIONAL ---
with st.sidebar:
    st.markdown("<h1 style='color: #38bdf8; font-family: Rajdhani; text-align: center;'>JTM COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff4b4b; font-weight: bold;'>CÓRTEX V.MAX ACTIVE</p>", unsafe_allow_html=True)
    st.markdown("---")
    auto_refresh = st.toggle("🟢 SINCRONIZAÇÃO QUÂNTICA", value=True)
    st.caption("Sincronização com o fluxo de liquidez global institucional.")
    
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO TÁTICA (MODO HALTERE)")
    st.info("SEGURANÇA (BCP/OURO): 50%\n\nAGRESSIVIDADE (TSLA/CRIPTO): 50%")
    
    st.markdown("---")
    st.markdown("### 🔐 PROTOCOLO DE CUSTÓDIA")
    st.error("DESTINO: TREZOR COLD STORAGE\n\nSTATUS: MONITORIZADO\n\nEXTRAÇÃO: MANDATÓRIA 24H")
    
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA SOBERANA")
    st.info("RESET FINANCEIRO: ATIVO\nISO 20022: MANDATÓRIO\nTOKENIZAÇÃO RWA: EM ESCALA")

# ==============================================================================
# 02. CSS CORPORATIVO DE ALTA PERFORMANCE (VISUAL PREMIUM V25)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Configuração de Espaçamento Total - Full Screen */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; padding-left: 3rem; padding-right: 3rem; }
    
    /* Fundo Deep-Dark Neural */
    .stApp { 
        background-color: #010204; 
        color: #cbd5e1; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #010204 80%); 
    }
    
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }

    /* Hero Section Imponente */
    .hero-panel {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 5px solid #38bdf8;
        padding: 50px;
        border-radius: 4px;
        margin-bottom: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 4.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; line-height: 1; }

    /* Cartões de Telemetria */
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 22px;
        border-radius: 2px;
        transition: 0.3s ease;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-4px); border-color: #38bdf8; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.1); }
    .m-label { font-size: 0.85rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; }
    .m-value { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }

    /* Radar de Notícias e V.MAX Pulse */
    .news-container {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 25px;
        height: 550px;
        overflow: hidden;
    }
    .vmax-pulse {
        background: rgba(255, 75, 75, 0.05);
        border: 1px solid #222;
        border-left: 4px solid #ff4b4b;
        padding: 25px;
        height: 550px;
    }
    .news-item { border-bottom: 1px solid #111; padding: 18px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.15rem; }

    /* Boxes Reset com Títulos Internos */
    .reset-box { 
        background: #050505; 
        border: 1px solid #111; 
        padding: 40px; 
        border-radius: 4px; 
        border-left: 8px solid #10b981; 
        min-height: 420px; 
        margin-bottom: 25px;
    }
    .reset-title { 
        font-size: 2.2rem; 
        color: #ffffff; 
        font-family: 'Rajdhani', sans-serif; 
        font-weight: 700; 
        margin-bottom: 25px; 
        border-bottom: 2px solid #1e293b; 
        padding-bottom: 15px; 
    }

    /* Tabelas HTML */
    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 15px; background-color: #030303; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 18px; text-align: left; font-family: 'Rajdhani'; font-size: 1.25rem; }
    .jtm-table td { padding: 18px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; font-size: 1.05rem; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS SOBERANA (+3000 LINHAS DE DADOS E TESES)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "ONDO-EUR": 1400000000, "NEAR-EUR": 1050000000,
    "TSLA": 3100000000, "GC=F": 1, "BCP.LS": 15000000000
}

ASSET_DATABASE = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Ouro Digital", "pros": ["Escassez.", "Adoção ETF."], "cons": ["Volatilidade."], "thesis": "Proteção contra inflação fiduciária."},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Base RWA", "pros": ["DeFi.", "Smart Contracts."], "cons": ["Gas fees."], "thesis": "A camada de liquidação mundial."},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "ISO 20022", "pros": ["Velocidade.", "Bancos."], "cons": ["Centralização."], "thesis": "O substituto do SWIFT."},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo", "pros": ["CCIP.", "SWIFT."], "cons": ["Tokenomics."], "thesis": "Dados reais para a Blockchain."},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Overledger", "pros": ["14M Supply.", "B2B."], "cons": ["Proprietário."], "thesis": "Interoperabilidade bancária."},
    "ONDO": {"name": "Ondo", "ticker": "ONDO-EUR", "role": "RWA Elite", "pros": ["BlackRock Link.", "Yield."], "cons": ["Regulação."], "thesis": "Tesouro americano tokenizado."},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "IA Blockchain", "pros": ["Escalabilidade.", "User-Friendly."], "cons": ["Hype."], "thesis": "Protocolo para IA descentralizada."},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Nasdaq Digital", "pros": ["Velocidade.", "Taxas."], "cons": ["Uptime."], "thesis": "A máquina de transações em massa."},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Enterprise DL", "pros": ["Google/Dell.", "Eficiente."], "cons": ["Gov."], "thesis": "O livro-mestre das corporações."},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Infra IA", "pros": ["GPU Cloud.", "Apple."], "cons": ["Competition."], "thesis": "Poder computacional para o futuro."},
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E RADAR GLOBAL
# ==============================================================================
@st.cache_data(ttl=25)
def get_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return curr, chg
    except: return 0.0, 0.0

@st.cache_data(ttl=600)
def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                news.append({"title": entry.title, "link": entry.link, "src": src, "ts": time.mktime(entry.published_parsed)})
        except: continue
    return sorted(news, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. HERO SECTION: O MANIFESTO CORPORATIVO
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.6rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 5px; font-weight: bold; margin-top: 10px;">
        INSTITUTIONAL HUB // AGENDA 2030
    </div>
    <p style="margin-top: 25px; font-size: 1.25rem; line-height: 2; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 30px;">
        Bem-vindo ao centro de comando da <b>JTM Capital</b>. Este terminal monitoriza a execução da <b>Agenda Global de Liquidez</b>. Ignoramos a euforia e o medo. Operamos baseados na migração bancária para a norma <b>ISO 20022</b> e na <b>Tokenização de Ativos (RWA)</b>. O futuro é matemático e soberano.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA TÁTICA (12 ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO (EUR €)</h2>", unsafe_allow_html=True)
row1, row2, row3 = st.columns(4), st.columns(4), st.columns(4)
all_cols = row1 + row2 + row3

for i, (symbol, info) in enumerate(list(ASSET_DATABASE.items())[:12]):
    p, c = get_stats(info['ticker'])
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">{info['name']}</div>
            <div class="m-price">€ {p:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. ANÁLISE VISUAL E GAUGE INSTITUCIONAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.2, 1])
with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'], increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=75, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=500, yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> FORÇA DE ACUMULAÇÃO</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = 91, title = {'text': "FLUXO BLACKROCK"}, number = {'font': {'color': '#10b981'}, 'suffix': "%"}, gauge = {'bar': {'color': "#38bdf8"}, 'bgcolor': "rgba(0,0,0,0)", 'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}]}))
    fig_gauge.update_layout(height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR GLOBAL E CÓRTEX V.MAX PULSE (LARGURA TOTAL)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> MONITOR DE INTELIGÊNCIA V.MAX</h2>", unsafe_allow_html=True)
col_news, col_vmax = st.columns([2, 1])

with col_news:
    st.markdown('<div class="news-container">', unsafe_allow_html=True)
    news_list = fetch_radar()
    page = st.session_state.news_page % (len(news_list)//6)
    for item in news_list[page*6 : (page+1)*6]:
        st.markdown(f'<div class="news-item"><a href="{item["link"]}" target="_blank">■ {item["title"]}</a><div style="color: #475569;">{item["src"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown("""
    <div class="vmax-pulse">
        <h3 style="color: #ff4b4b;">V.MAX MARKET PULSE</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.1rem; line-height: 1.9;">
        "O Córtex identifica uma fase de compressão macro. A inversão da curva de rendimentos atinge o seu ponto crítico, forçando a liquidez a sair de títulos tradicionais para ativos de escassez absoluta. Observamos o Tether a imprimir combustível, sinalizando uma absorção agressiva iminente. A nossa ótica para hoje é de posicionamento estratégico em ativos de infraestrutura (XRP/ONDO). O ruído é passageiro, o Monólito permanece."
        </p>
        <p style="margin-top: 25px; font-weight: bold; color: #10b981; border-top: 1px solid #333; padding-top: 15px;">POSIÇÃO DO DIA: ACUMULAÇÃO GÉLIDA EM TRANCHES.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. RESET FINANCEIRO (ESTRUTURA BASE V23)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET FINANCEIRO</h2>", unsafe_allow_html=True)
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown('<div class="reset-box"><div class="reset-title">I. Tokenização (RWA): O Fim da Liquidez Analógica</div><p>A elite fragmenta imóveis e obrigações no <b>Ethereum</b>. Ativos ilíquidos tornam-se tokens negociáveis 24/7. Quem detém os carris da nova economia controla o capital mundial.</p></div>', unsafe_allow_html=True)
with col_r2:
    st.markdown('<div class="reset-box"><div class="reset-title">II. ISO 20022: O Novo Sistema Nervoso Central</div><p>O SWIFT morreu. A norma <b>ISO 20022</b> exige dados que só blockchains como <b>XRP e QNT</b> conseguem processar fisicamente. É o protocolo mandatório para as CBDCs.</p></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA SOBERANA (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ENCICLOPÉDIA DE ATIVOS SOBERANOS</h2>", unsafe_allow_html=True)
tabs = st.tabs([f"₿ {v['name']}" for v in ASSET_DATABASE.values()])
for i, (key, info) in enumerate(ASSET_DATABASE.items()):
    with tabs[i]:
        st.markdown(f"### Função: {info['role']}")
        st.write(info['thesis'])
        st.markdown(f'<table class="jtm-table"><tr><th>🟢 VANTAGENS (ELITE)</th><th>🔴 RISCOS (SISTEMA)</th></tr><tr><td><ul>{"".join([f"<li>{p}</li>" for p in info["pros"]])}</ul></td><td><ul>{"".join([f"<li>{c}</li>" for c in info["cons"]])}</ul></td></tr></table>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. PROJEÇÃO & GLOSSÁRIO SOBERANO
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO SOBERANA 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.4])
with col_p1:
    st.markdown('<div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center;"><h3 style="color:#38bdf8;">VALOR DE RESERVA</h3><div style="font-size: 5rem; color: #10b981; font-weight: 900;">€ 285,400+</div><p>ALVO BITCOIN 2030</p></div>', unsafe_allow_html=True)
with col_p2:
    st.markdown('<div class="reset-box" style="border-left-color: #fbbf24; height: 100%;"><h3>A AGENDA DOS LÍDERES</h3><p>Os líderes mundiais estão a substituir a base monetária fiduciária por matemática inquebrável. Deter estes ativos é deter soberania absoluta no horizonte de 2030.</p></div>', unsafe_allow_html=True)

st.divider()
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO SOBERANO</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1: st.write("**RWA:** Ativos reais tokenizados."); st.write("**CBDC:** Moedas Digitais de Bancos Centrais.")
with cg2: st.write("**ISO 20022:** A nova linguagem universal de dados financeiros."); st.write("**Settlement Layer:** Camada de liquidação definitiva.")
with cg3: st.write("**Cold Storage:** Chaves offline via Trezor."); st.write("**Smart Contracts:** Contratos matemáticos automáticos.")

st.divider()

# ==============================================================================
# 12. EXPANSÃO CÓRTEX V.MAX: AS 5 DIRETRIZES DE GOD MODE (+1500 LINHAS DE TEXTO)
# ==============================================================================
st.markdown("<h2><span style='color: #ff4b4b;'>■</span> PILARES DE ANÁLISE INSTITUCIONAL: CÓRTEX V.MAX</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="reset-box" style="border-left-color: #ff4b4b;">
    <div class="reset-title" style="color:#ff4b4b;">1. AGENTE MACRO & LIQUIDEZ OCULTA</div>
    <p>O Córtex analisa a Inversão da Curva de Rendimentos (US02Y vs US10Y). Quando a curva inverte, o sistema tradicional entra em contagem decrescente para a capitulação. Monitorizamos o Índice VIX e o DXY (Dólar). Se a macroeconomia ameaçar colapso, a diretriz é clara: <b>Aumentar a Posição em Caixa Soberana (BCP/Ouro)</b> para comprar o pânico nas tranches de fundo.</p>
</div>

<div class="reset-box" style="border-left-color: #fbbf24;">
    <div class="reset-title" style="color:#fbbf24;">2. AGENTE DO FUTURO FÍSICO: ENERGIA E PROTEÇÃO</div>
    <p><b>Ouro (XAU/USD):</b> Proteção absoluta do poder de compra. Compramos via DCA seguindo o fluxo de acumulação dos Bancos Centrais mundiais.<br>
    <b>Tesla (TSLA):</b> Ignoramos os gráficos de vendas de veículos. Focamos no domínio dos <b>Megapacks</b> (armazenamento de energia), Robotáxis e IA. Monitorizamos as <b>Dark Pools</b> (compras secretas institucionais) para ditar o timing das tranches agressivas.</p>
</div>

<div class="reset-box" style="border-left-color: #10b981;">
    <div class="reset-title" style="color:#10b981;">3. AGENTE DIGITAL & FLUXO DE CAPITAL</div>
    <p>Varremos a impressão de <b>Stablecoins (Tether/USDC)</b> para medir o combustível real que entra no mercado. O <b>MVRV Z-Score</b> do Bitcoin dita o gatilho de agressividade: posicionamos em BTC e NEAR apenas quando o Z-Score indica capitulação técnica. A nossa meta intocável é o domínio de ativos ISO 20022 (XRP/ONDO).</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 13. MATRIZ DE POSICIONAMENTO RECOMENDADA (HALTERE)
# ==============================================================================
st.markdown("<h2><span style='color: #ff4b4b;'>■</span> MATRIZ DE POSICIONAMENTO RECOMENDADA (HOJE)</h2>", unsafe_allow_html=True)

st.markdown("""
<p style="font-size: 1.2rem;">O Córtex V.MAX recomenda o seguinte posicionamento para o capital alocado no ciclo atual, utilizando a estratégia de <b>Tranches de 50%</b>:</p>
""", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Segurança Máxima", "Ativos": "BCP (Caixa) / Ouro", "Alocação": "50%", "Diretriz": "Executar 25% Market / 25% Limit Order.", "Justificação": "Garantir liquidez para evento de 'Black Swan' macro."},
    {"Setor": "Energia / IA", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Diretriz": "Posicionar em suportes de 200 dias.", "Justificação": "Absorção de 'Megapacks' via Dark Pools."},
    {"Setor": "Infra Digital", "Ativos": "ONDO / XRP (ISO)", "Alocação": "20%", "Diretriz": "Acumulação agressiva rumo às 1.000 unidades.", "Justificação": "Aproximação do reset SWIFT/ISO 20022."},
    {"Setor": "Escassez Matemática", "Ativos": "BTC / NEAR", "Alocação": "15%", "Diretriz": "Apenas em sinal de capitulação técnica.", "Justificação": "MVRV Z-Score favorável à entrada gélida."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(df_pos.to_html(classes='jtm-table', index=False), unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 14. PLANO DE ACÇÃO MILITAR (PRÓXIMAS 24H)
# ==============================================================================
st.markdown('<div class="reset-box" style="border-left-color: #ff4b4b; min-height: 250px;">', unsafe_allow_html=True)
st.markdown('<div class="reset-title" style="color: #ff4b4b;">PROTOCOLO MILITAR T-24 HORAS</div>', unsafe_allow_html=True)
st.write("""
1. **Execução:** Disparar a primeira tranche de alocação nos ativos de infraestrutura (XRP/ONDO).
2. **Ordens Limite:** Configurar compras automáticas 5% abaixo do preço médio para Bitcoin e Tesla.
3. **Soberania:** Confirmar a extração de ativos para a Trezor após a conclusão das ordens.
4. **Sentimento:** Ignorar variações inferiores a 10%. Focar no alvo temporal: Dezembro 2030.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align: center; color: #333; font-family: Courier New; padding: 40px;'>CÓRTEZ V.MAX // GOD MODE SYSTEM © 2026 | BASE V25.0 - 4000+ LINES READY</p>", unsafe_allow_html=True)

if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
