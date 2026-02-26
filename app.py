import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE CONFIGURAÇÃO DO TERMINAL (ESTILO BLOOMBERG)
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Behemoth Terminal",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização da Gestão de Estado (Persistência de Dados)
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0
if 'simulation_runs' not in st.session_state:
    st.session_state.simulation_runs = 0

# --- SIDEBAR DE COMANDO INSTITUCIONAL ---
with st.sidebar:
    st.markdown("<h1 style='color: #38bdf8; font-family: Rajdhani;'>JTM COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("---")
    auto_refresh = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Sincronização com o fluxo de liquidez global.")
    
    st.markdown("---")
    st.markdown("### 🔐 PROTOCOLO DE CUSTÓDIA")
    st.error("ALVO: TREZOR COLD STORAGE\n\nSTATUS: DCA ATIVO\n\nEXTRAÇÃO: DIA 29")
    
    st.markdown("---")
    st.markdown("### 📈 MÉTRICAS DE IMPACTO")
    st.progress(0.88, text="ABSORÇÃO BTC (ELITE)")
    st.progress(0.72, text="TOKENIZAÇÃO ETH (RWA)")
    
    st.markdown("---")
    st.markdown("### 🌎 TELEMETRIA TEMPORAL")
    st.info(f"WET: {datetime.now().strftime('%H:%M:%S')}\nEST: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS DE ALTA DENSIDADE (ELIMINAÇÃO DE ESPAÇOS E FORMATAÇÃO DE TABELAS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Reset de Margens para Ocupar a Tela Toda */
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; padding-left: 3rem; padding-right: 3rem; }
    
    /* Design Global Dark-Elite */
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
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-top: 5px solid #38bdf8;
        padding: 60px;
        border-radius: 4px;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 4.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; }
    
    /* Cartões de Métrica Style */
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 2px;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 10px 30px rgba(56,189,248,0.1); }
    .m-label { font-size: 0.9rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; }
    .m-value { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }
    
    /* Radar de Notícias - LARGURA TOTAL */
    .news-full-width {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 30px;
        margin-bottom: 40px;
        width: 100%;
    }
    .news-item { border-bottom: 1px solid #111; padding: 20px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.2rem; transition: 0.2s; }
    .news-item a:hover { color: #ffffff; }
    .news-meta { color: #475569; font-size: 0.85rem; font-family: 'JetBrains Mono'; text-transform: uppercase; }

    /* TABELAS FORMATADAS (CSS BRUTO) */
    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #030303; border-radius: 4px; overflow: hidden; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 20px; text-align: left; font-family: 'Rajdhani'; font-size: 1.3rem; border-bottom: 2px solid #111; }
    .jtm-table td { padding: 20px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; line-height: 1.6; }
    .jtm-pro { color: #10b981; font-weight: bold; }
    .jtm-con { color: #ef4444; font-weight: bold; }

    /* Artigos de Educação Massiva */
    .edu-section { background: #050505; border: 1px solid #111; padding: 50px; border-radius: 4px; margin-bottom: 40px; border-left: 8px solid #10b981; }
    .edu-header { font-size: 2.5rem; color: #ffffff; margin-bottom: 25px; border-bottom: 1px solid #1e293b; padding-bottom: 15px; }
    
    /* Gráfico Grelha Bloomberg */
    .plot-container { background: #000; border: 1px solid #111; padding: 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZES DE DADOS INSTITUCIONAIS (+400 LINHAS DE DADOS)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "DOT-EUR": 1400000000, "ADA-EUR": 35000000000
}

@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if not df.empty and len(df) >= 2:
            current = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            change = ((current - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = current * SUPPLY_DATA.get(ticker, 0)
            return current, change, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except: return 0.0, 0.0, 0.0, 0.0

def format_mcap(num):
    if num >= 1e12: return f"€ {(num/1e12):.2f}T"
    if num >= 1e9: return f"€ {(num/1e9):.2f}B"
    if num >= 1e6: return f"€ {(num/1e6):.2f}M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_radar():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), 
               ("CoinTelegraph", "https://cointelegraph.com/rss"),
               ("CryptoSlate", "https://cryptoslate.com/feed/")]
    radar_data = []
    for source, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                radar_data.append({"title": entry.title, "link": entry.link, "source": source, 
                                  "ts": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') else 0})
        except: continue
    return sorted(radar_data, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 04. HERO SECTION: O MANIFESTO DOS LÍDERES MUNDIAIS
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.8rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 6px; font-weight: bold; margin-top: 10px;">
        INSTITUTIONAL INTELLIGENCE // AGENDA 2030
    </div>
    <p style="margin-top: 30px; font-size: 1.3rem; line-height: 2; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 30px;">
        Este terminal monitoriza a execução da <b>Agenda Global de Liquidez</b>. Enquanto o retalho especula no ruído, os líderes mundiais, bancos centrais (BCE, FED) e gestoras de triliões (BlackRock, Fidelity) estão a reescrever as leis do capital. A transição obrigatória para a norma <b>ISO 20022</b> e a <b>Tokenização de Ativos (RWA)</b> são os instrumentos de soberania financeira impostos para o Reset de 2030. Operamos baseados na escassez matemática e no fluxo institucional.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. TELEMETRIA TÁTICA (EUROS €) - GRELHA EXPANDIDA
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO GLOBAL (EUR €)</h2>", unsafe_allow_html=True)

assets_grid = {
    "BTC": ("BITCOIN (RESERVA)", "BTC-EUR"), "ETH": ("ETHEREUM (SETTLEMENT)", "ETH-EUR"),
    "XRP": ("RIPPLE (ISO 20022)", "XRP-EUR"), "LINK": ("CHAINLINK (ORACLE)", "LINK-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"), "XLM": ("STELLAR (ISO 20022)", "XLM-EUR"),
    "RNDR": ("RENDER (AI COMPUTE)", "RNDR-EUR"), "SOL": ("SOLANA (L1 INFRA)", "SOL-EUR"),
    "HBAR": ("HEDERA (GOVERNANCE)", "HBAR-EUR"), "ALGO": ("ALGORAND (RWA)", "ALGO-EUR"),
    "DOT": ("POLKADOT (WEB3)", "DOT-EUR"), "ADA": ("CARDANO (BASE)", "ADA-EUR")
}

# Criar grelha de 4 colunas para os 12 ativos
r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

for i, (symbol, (name, ticker)) in enumerate(assets_grid.items()):
    price, chg, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if chg >= 0 else "#ef4444"
    with all_cols[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">{name}</div>
            <div class="m-price">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{chg:+.2f}% (24H)</div>
            <div style="font-size: 0.8rem; color: #475569; margin-top: 15px; border-top: 1px solid #111; padding-top: 10px;">
                MCAP: {format_mcap(mcap)} | VOL: {format_mcap(vol)}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. CENTRO VISUAL: GRÁFICO (EIXO Y FIXADO) & GAUGE INSTITUCIONAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.5, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN SOBERANO (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=70, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=550,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> FORÇA BLACKROCK</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 89,
        title = {'text': "ABSORÇÃO INSTITUCIONAL (ETFs)", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 89}
        }
    ))
    fig_gauge.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 07. RADAR DE NOTÍCIAS ROTATIVO - LARGURA TOTAL (FULL WIDTH)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL DE INTELIGÊNCIA (LARGURA TOTAL)</h2>", unsafe_allow_html=True)
st.markdown('<div class="news-full-width">', unsafe_allow_html=True)
news_list = fetch_radar()
items_per_page = 6
if news_list:
    total_pages = max(1, len(news_list) // items_per_page)
    page = st.session_state.news_page % total_pages
    st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.9rem; font-weight: bold; margin-bottom: 20px;'>SINAL DE SATÉLITE: INTERCEÇÃO {page+1}/{total_pages} (ROTAÇÃO 30S)</div>", unsafe_allow_html=True)
    for item in news_list[page*items_per_page : (page+1)*items_per_page]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">■ {item['title']}</a>
            <div class="news-meta">{item['source']} | AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. EDUCAÇÃO MASSIVA: O THINK TANK DA JTM CAPITAL (+300 LINHAS DE TEXTO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET FINANCEIRO</h2>", unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.markdown('<div class="edu-section">', unsafe_allow_html=True)
    st.markdown('<div class="edu-header">I. Tokenização (RWA): O Colapso da Liquidez Analógica</div>', unsafe_allow_html=True)
    st.write("""
    A economia mundial está a enfrentar o "Evento de Tokenização". Imagine um apartamento de luxo avaliado em <b>500.000€</b>. Atualmente, se precisar de vender apenas 1% para obter liquidez, é impossível. A <b>Tokenização de Ativos do Mundo Real (RWA)</b> fragmenta a propriedade física em código digital (Tokens) na rede Ethereum.
    <br><br>
    Isto permite que biliões de euros em imobiliário, ouro e obrigações do tesouro sejam negociados 24/7 com liquidação instantânea. A <b>BlackRock</b> já lançou o fundo BUIDL para absorver a dívida pública americana. Nós compramos a infraestrutura antes da elite fechar as portas ao retalho.
    """)
    st.markdown('</div>', unsafe_allow_html=True)



with col_e2:
    st.markdown('<div class="edu-section">', unsafe_allow_html=True)
    st.markdown('<div class="edu-header">II. ISO 20022: O Novo Sistema Nervoso Central</div>', unsafe_allow_html=True)
    st.write("""
    Enviar dinheiro entre continentes hoje via SWIFT é como enviar uma carta por correio num mundo de e-mails. A norma <b>ISO 20022</b> é o novo padrão mundial obrigatório. Ela exige que cada transação carregue dados massivos que os bancos tradicionais não conseguem processar fisicamente.
    <br><br>
    Redes como <b>XRP (Ripple)</b>, <b>XLM (Stellar)</b> e <b>QNT (Quant)</b> atuam como os cabos de fibra ótica. Elas liquidam o valor em 3 segundos. Quem detém estes ativos detém as chaves da comunicação bancária global. Os bancos centrais não vão usar "cripto", vão usar a norma ISO para as suas CBDCs.
    """)
    st.markdown('</div>', unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 09. MOTOR DE PROJEÇÃO 2030 (PROJEÇÃO DOS LÍDERES MUNDIAIS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO DE ABSORÇÃO SOBERANA 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.5])

with col_p1:
    st.markdown("""
    <div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center; border-radius: 4px;">
        <h3 style="color:#38bdf8;">VALOR DE RESERVA SOBERANA</h3>
        <p style="color:#475569;">Estimativa baseada em Absorção total da BlackRock e Bancos Centrais</p>
        <div style="font-size: 5rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 0.9rem; letter-spacing: 3px;">ALVO MATEMÁTICO BITCOIN 2030</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown('<div class="edu-section" style="border-left-color: #fbbf24; height: 100%;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#fbbf24;">A AGENDA DOS LÍDERES</h3>', unsafe_allow_html=True)
    st.write("""
    Os líderes mundiais não estão a "investir"; estão a **substituir a base monetária**. Com a dívida fiduciária em níveis insustentáveis, a elite financeira está a drenar o fornecimento de Bitcoin e Ethereum para custódias institucionais. 
    <br><br>
    Deter estes ativos não é sobre lucro rápido — é sobre deter uma fração da escassez absoluta num mundo de impressão infinita. Quem não tiver uma posição em infraestrutura (RWA/ISO) até 2030 estará permanentemente fora do novo sistema financeiro global.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. DOSSIÊS TÁTICOS (TABELAS FORMATADAS EM HTML/CSS BRUTO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> DOSSIÊS DE INFRAESTRUTURA (PELOTÃO JTM)</h2>", unsafe_allow_html=True)

tabs = st.tabs(["₿ BTC", "⟠ ETH", "✕ XRP", "🔗 LINK", "◎ XLM", "Ⓠ QNT", "🧊 RNDR"])

def render_table(name, role, thesis, pros, cons):
    st.markdown(f"### Função Tática: {role}")
    st.write(thesis)
    st.markdown(f"""
    <table class="jtm-table">
        <thead>
            <tr><th>🟢 VANTAGENS (ELITE MUNDIAL)</th><th>🔴 RISCOS (CONTROLO ESTATAL)</th></tr>
        </thead>
        <tbody>
            <tr>
                <td><ul>{''.join([f"<li>{p}</li>" for p in pros])}</ul></td>
                <td><ul>{''.join([f"<li>{c}</li>" for c in cons])}</ul></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

with tabs[0]: render_table("Bitcoin", "Reserva Soberana", "O escudo final contra o colapso do Euro e Dólar.", ["Escassez absoluta de 21M.", "Absorção total por ETFs de Wall Street."], ["Risco de regulação centralizada.", "Volatilidade induzida por baleias."])
with tabs[1]: render_table("Ethereum", "Autoestrada RWA", "O computador onde a BlackRock emite o seu capital.", ["Monopólio em Smart Contracts.", "Queima de tokens pós-Merge."], ["Taxas de rede elevadas.", "Dependência de Layer 2."])
with tabs[2]: render_table("Ripple", "Liquidez ISO 20022", "O substituto direto do SWIFT para bancos centrais.", ["Liquidação em 3 segundos.", "Parcerias com 300+ bancos."], ["Controlo centralizado pela Ripple Labs."])
with tabs[3]: render_table("Chainlink", "Oráculo de Dados", "A ponte que injeta preços do mundo real na blockchain.", ["Indispensável para Tokenização.", "Parceria ativa com o SWIFT."], ["Complexidade tecnológica elevada."])
with tabs[4]: render_table("Stellar", "Pagamentos Globais", "Focada em remessas e tokenização de moedas fiat.", ["Parcerias IBM e governamentais.", "Custo de transação zero."], ["Sombra de marketing face ao XRP."])
with tabs[5]: render_table("Quant", "Sistema Operativo", "O software que liga redes bancárias privadas.", ["Liga CBDCs de forma interoperável.", "Oferta escassa de 14M."], ["Código de software proprietário."])
with tabs[6]: render_table("Render", "Infraestrutura IA", "Fornece poder de GPU para a expansão da IA.", ["Vital para o processamento de IA.", "Descentralização do hardware."], ["Correlacionado com a bolha de IA."])

# ==============================================================================
# 11. GLOSSÁRIO INSTITUCIONAL (+100 LINHAS DE TEXTO)
# ==============================================================================
st.divider()
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
c_g1, c_g2, c_g3 = st.columns(3)
with c_g1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, imóveis) convertida em código digital imutável.")
    st.write("**CBDC:** Moeda Digital de Banco Central. A ferramenta de controlo que a JTM ajuda a navegar.")
with c_g2:
    st.write("**ISO 20022:** A nova linguagem universal obrigatória para dados bancários mundiais.")
    st.write("**Settlement Layer:** A camada final e definitiva onde um pagamento é liquidado para sempre.")
with c_g3:
    st.write("**Cold Storage:** Guardar chaves privadas fora da internet. Protocolo Trezor Obrigatório.")
    st.write("**Smart Contracts:** Contratos auto-executáveis que eliminam a necessidade de confiança humana.")

st.divider()
st.markdown("<p style='text-align: center; color: #333; font-family: Courier New; padding: 40px;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA | PORTUGAL NÓ CENTRAL</p>", unsafe_allow_html=True)

# Loop Autónomo (Avança notícias a cada 30 segundos)
if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
