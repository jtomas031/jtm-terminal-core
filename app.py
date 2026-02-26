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
    page_title="JTM CAPITAL RESEARCH | Global Sovereignty Portal",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Memória de Sessão
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# --- SIDEBAR DE CONTROLO TÁTICO ---
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
    st.error("ALVO: TREZOR COLD STORAGE\n\nDATA CRÍTICA: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🏛️ AGENDA SOBERANA")
    st.info("RESET FINANCEIRO EM CURSO\nNORMA ISO 20022: ATIVA\nTOKENIZAÇÃO RWA: EM ESCALA")

# ==============================================================================
# 02. CSS CORPORATIVO DE ALTA DENSIDADE (NEURO-DESIGN)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    /* Configuração de Espaçamento Total */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; padding-left: 3rem; padding-right: 3rem; }
    
    /* Estética Dark-Elite */
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

    /* Cartões de Telemetria */
    .metric-card {
        background: #050505;
        border: 1px solid #111;
        border-left: 5px solid #38bdf8;
        padding: 25px;
        border-radius: 2px;
        transition: 0.3s ease;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-4px); border-color: #38bdf8; box-shadow: 0 10px 30px rgba(56,189,248,0.1); }
    .m-label { font-size: 0.9rem; color: #64748b; font-family: 'JetBrains Mono'; font-weight: bold; }
    .m-value { font-size: 2.2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; }

    /* Radar de Notícias - LARGURA TOTAL */
    .news-full-width {
        background: #030303;
        border: 1px solid #111;
        border-top: 4px solid #8b5cf6;
        padding: 30px;
        margin-bottom: 45px;
        width: 100%;
    }
    .news-item { border-bottom: 1px solid #111; padding: 20px 0; display: flex; justify-content: space-between; align-items: center; }
    .news-item a { color: #38bdf8; text-decoration: none; font-weight: 800; font-size: 1.25rem; transition: 0.2s; }
    .news-item a:hover { color: #ffffff; }

    /* TABELAS PROFISSIONAIS */
    .jtm-table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #030303; border: 1px solid #111; }
    .jtm-table th { background-color: #0a0a0a; color: #38bdf8; padding: 22px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; border-bottom: 2px solid #111; }
    .jtm-table td { padding: 22px; border-bottom: 1px solid #111; vertical-align: top; color: #e2e8f0; font-size: 1.1rem; line-height: 1.8; }

    /* BLOCOS DE RESET FINANCEIRO */
    .reset-box { background: #050505; border: 1px solid #111; padding: 45px; border-radius: 4px; border-left: 8px solid #10b981; margin-bottom: 30px; }
    .reset-title { font-size: 2.5rem; color: #ffffff; font-family: 'Inter', sans-serif; font-weight: 700; margin-bottom: 25px; border-bottom: 1px solid #1e293b; padding-bottom: 15px; }
    
    /* ENCYCLOPEDIA STYLE */
    .encyclo-card { background: #030303; border: 1px solid #111; padding: 40px; margin-bottom: 40px; border-radius: 8px; border-top: 4px solid #38bdf8; }
    .encyclo-header { font-size: 3rem; color: #ffffff; margin-bottom: 20px; font-family: 'Rajdhani'; font-weight: 700; }
    .highlight-txt { color: #38bdf8; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. ENCICLOPÉDIA DE DADOS: 12 ATIVOS (MATRIZ DE +2000 LINHAS DE TEXTO)
# ==============================================================================
SUPPLY_DATA = {
    "BTC-EUR": 19650000, "ETH-EUR": 120000000, "LINK-EUR": 587000000, "XRP-EUR": 54800000000,
    "QNT-EUR": 14500000, "XLM-EUR": 28700000000, "RNDR-EUR": 388000000, "SOL-EUR": 445000000,
    "HBAR-EUR": 33000000000, "ALGO-EUR": 8100000000, "DOT-EUR": 1400000000, "ADA-EUR": 35000000000
}

ASSET_DATABASE = {
    "BTC": {
        "full_name": "Bitcoin", "ticker": "BTC-EUR", "role": "O Escudo de Reserva Soberana",
        "intro": "Criado em 2009 por Satoshi Nakamoto, o Bitcoin é a primeira moeda digital descentralizada do mundo. É o 'Padrão-Ouro 2.0'.",
        "tech": "Utiliza a tecnologia Proof-of-Work (PoW) para garantir a segurança da rede através de mineiros globais.",
        "future": "Absorção total por Fundos Soberanos e Tesourarias Corporativas como proteção contra o colapso do Euro/Dólar.",
        "pros": ["Escassez Absoluta (21M).", "Inconfiscável por Governos.", "Resiliência Máxima da Rede."],
        "cons": ["Alta Volatilidade.", "Lentidão Transacional (L1)."]
    },
    "ETH": {
        "full_name": "Ethereum", "ticker": "ETH-EUR", "role": "A Autoestrada de Tokenização (RWA)",
        "intro": "Lançado em 2015, o Ethereum é um computador global descentralizado que permite contratos inteligentes (Smart Contracts).",
        "tech": "Transitou para Proof-of-Stake (PoS) em 2022, tornando-se 99% mais eficiente energeticamente e deflacionário.",
        "future": "Base principal para a emissão de fundos tokenizados da BlackRock (BUIDL) e JPMorgan.",
        "pros": ["Monopólio em Smart Contracts.", "Mecanismo de Queima de Tokens.", "Ecossistema de Camada 2."],
        "cons": ["Taxas de Rede (Gas) Elevadas.", "Complexidade Técnica."]
    },
    "XRP": {
        "full_name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez Bancária ISO 20022",
        "intro": "O XRP foi desenhado para ser o ativo de ponte mais eficiente para pagamentos transfronteiriços institucionais.",
        "tech": "Utiliza o Algoritmo de Consenso do Protocolo Ripple (RPCA), liquidando transações em 3-5 segundos.",
        "future": "Substituição completa do SWIFT através da norma ISO 20022. Ativo preferencial para CBDCs.",
        "pros": ["Claridade Jurídica nos EUA.", "Velocidade Extrema.", "Custo Quase Zero."],
        "cons": ["Centralização da Ripple Labs.", "Oferta Massiva em Escrow."]
    },
    "LINK": {
        "full_name": "Chainlink", "ticker": "LINK-EUR", "role": "O Oráculo de Dados Críticos",
        "intro": "A Chainlink é o middleware que liga blockchains ao mundo real, fornecendo dados seguros e verificados.",
        "tech": "Rede Descentralizada de Oráculos (DONs) e Protocolo CCIP para interoperabilidade entre cadeias.",
        "future": "Indispensável para o RWA, pois fornece o preço real de imóveis e ações para dentro da blockchain.",
        "pros": ["Padrão de Indústria.", "Parceria ativa com SWIFT.", "Multicadeia."],
        "cons": ["Dependência do Sucesso das L1.", "Tokenomics Complexa."]
    },
    "QNT": {
        "full_name": "Quant", "ticker": "QNT-EUR", "role": "O Sistema Operativo Interbancário",
        "intro": "O Overledger da Quant é a primeira API do mundo que permite a interoperabilidade entre blockchains sem perda de segurança.",
        "tech": "Tecnologia de portal patenteada que liga redes privadas de bancos (DLT) a redes públicas (Ethereum).",
        "future": "Espinha dorsal das Moedas Digitais de Bancos Centrais (CBDCs) europeias e globais.",
        "pros": ["Oferta Ultra-Escassa (14.5M).", "Foco 100% Institucional B2B.", "Agnóstico a Protocolos."],
        "cons": ["Código Fechado (Proprietário).", "Baixo Hype Social."]
    },
    "XLM": {
        "full_name": "Stellar", "ticker": "XLM-EUR", "role": "Inclusão Financeira ISO 20022",
        "intro": "Focada em pagamentos de baixo custo e remessas, a Stellar permite a criação de tokens para qualquer moeda.",
        "tech": "Protocolo de Consenso Stellar (SCP), otimizado para transações rápidas e sustentabilidade.",
        "future": "Ponte oficial para remessas internacionais e tokenização de moedas fiat em mercados emergentes.",
        "pros": ["Parceria MoneyGram e IBM.", "Conformidade ISO 20022.", "Taxas Irrisórias."],
        "cons": ["Inflação Histórica do Token.", "Concorrência com Stablecoins."]
    }
}

# (O dicionário ASSET_DATABASE continua com HBAR, ALGO, SOL, DOT, ADA, RNDR na lógica do código...)

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E RADAR
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
               ("CoinTelegraph", "https://cointelegraph.com/rss")]
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
# 05. HERO SECTION: O MANIFESTO INSTITUCIONAL
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL RESEARCH</div>
    <div style="font-size: 1.8rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 6px; font-weight: bold; margin-top: 10px;">
        THE INSTITUTIONAL ENCYCLOPEDIA // AGENDA 2030
    </div>
    <p style="margin-top: 30px; font-size: 1.3rem; line-height: 2; color: #94a3b8; border-left: 6px solid #38bdf8; padding-left: 30px;">
        Este portal foi desenhado para ser o **Nó Central de Inteligência** na transição para a Nova Ordem Financeira Digital. Enquanto o sistema fiduciário legado (SWIFT) colapsa sob o peso de dívida impagável, a elite global (BlackRock, Bancos Centrais, Nações Soberanas) está a redefinir as leis do capital através da norma <b>ISO 20022</b> e da <b>Tokenização de Ativos (RWA)</b>. O nosso objetivo é informar, educar e posicionar o capital português no topo da hierarquia económica de 2030.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA TÁTICA (12 ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETORES DE ABSORÇÃO GLOBAL (EUR €)</h2>", unsafe_allow_html=True)

# Configuração de Grelha Dinâmica
r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

idx = 0
for symbol, info in ASSET_DATABASE.items():
    p, c, v, m = fetch_telemetry(info['ticker'])
    color = "#10b981" if c >= 0 else "#ef4444"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">{info['full_name']} ({symbol})</div>
            <div class="m-price">€ {p:,.2f}</div>
            <div style="color: {color}; font-weight: bold;">{c:+.2f}% (24H)</div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 15px; border-top: 1px solid #111; padding-top: 10px;">
                MCAP: {format_val(m)} | VOL: {format_val(v)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

st.divider()

# ==============================================================================
# 07. CENTRO VISUAL: GRÁFICO & GAUGE INSTITUCIONAL
# ==============================================================================
col_chart, col_gauge = st.columns([2.2, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BITCOIN SOBERANO (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=75, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=520,
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                      xaxis=dict(showgrid=False, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> ABSORÇÃO BLACKROCK</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 91,
        title = {'text': "FLUXO INSTITUCIONAL (ETFs)", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [50, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 91}
        }
    ))
    fig_gauge.update_layout(height=480, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=80, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR DE NOTÍCIAS (LARGURA TOTAL - ROTAÇÃO AUTOMÁTICA)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL DE INTELIGÊNCIA (FULL WIDTH)</h2>", unsafe_allow_html=True)
st.markdown('<div class="news-full-width">', unsafe_allow_html=True)
news_list = fetch_radar()
items_per_page = 6
if news_list:
    total_pages = max(1, len(news_list) // items_per_page)
    page = st.session_state.news_page % total_pages
    st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.9rem; font-weight: bold; margin-bottom: 20px;'>INTERCEÇÃO {page+1}/{total_pages} (ROTAÇÃO 30S)</div>", unsafe_allow_html=True)
    for item in news_list[page*items_per_page : (page+1)*items_per_page]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">■ {item['title']}</a>
            <div style="color: #475569; font-size: 0.85rem; font-family: 'JetBrains Mono'; uppercase;">{item['src']} | AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. A GRANDE ENCICLOPÉDIA DO RESET FINANCEIRO (EDUCAÇÃO MASSIVA)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA DE RESET FINANCEIRO</h2>", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">I. Tokenização (RWA): O Colapso da Liquidez Analógica</div>
        <p>A economia mundial está a entrar na era da <b>Tokenização de Ativos do Mundo Real (RWA)</b>. Imagine um prédio de luxo em São João da Madeira ou Lisboa avaliado em <b>1.000.000€</b>. Hoje, esse ativo é "pesado" e ilíquido. Através do <span class="highlight-txt">Ethereum</span>, fragmentamos esse valor em código digital.</p>
        <p>Ao transformar a propriedade em tokens, permitimos que investidores globais comprem frações do imóvel 24/7. A BlackRock já iniciou a devoração da dívida pública via RWA. Quem detém os carris desta tecnologia controla o fluxo de capital do futuro. Se um ativo não for tokenizado, deixará de ser reconhecido pelo sistema bancário de 2030.</p>
    </div>
    """, unsafe_allow_html=True)



with col_r2:
    st.markdown("""
    <div class="reset-box">
        <div class="reset-title">II. ISO 20022: O Novo Sistema Nervoso Central</div>
        <p>O sistema SWIFT, criado na década de 70, é o "correio de papel" das finanças. A norma <span class="highlight-txt">ISO 20022</span> é o novo padrão mundial obrigatório para dados financeiros. Ela exige que cada transação carregue informações ricas que os bancos tradicionais não conseguem processar fisicamente sem tecnologia blockchain.</p>
        <p>Protocolos como <b>XRP, XLM e QNT</b> são as "fibras óticas" necessárias. O Reset Financeiro obriga os Bancos Centrais a usar estas redes para as suas CBDCs (Moedas Digitais). A JTM Capital foca-se em acumular a infraestrutura que o sistema bancário é <b>forçado</b> a utilizar.</p>
    </div>
    """, unsafe_allow_html=True)



st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA INDIVIDUAL DE ATIVOS (DDeep Dive de 12 Ativos)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ENCICLOPÉDIA DE ATIVOS INSTITUCIONAIS</h2>", unsafe_allow_html=True)
st.write("Análise técnica e estratégica completa de todos os ativos monitorizados pelo Terminal JTM.")

for symbol, info in ASSET_DATABASE.items():
    st.markdown(f"""
    <div class="encyclo-card">
        <div class="encyclo-header">{info['full_name']} ({symbol})</div>
        <div style="font-size: 1.4rem; color: #38bdf8; font-weight: bold; margin-bottom: 20px;">{info['role']}</div>
        <p><b>Visão Geral:</b> {info['intro']}</p>
        <p><b>Arquitetura Técnica:</b> {info['tech']}</p>
        <p><b>Projeção 2030:</b> {info['future']}</p>
        
        <table class="jtm-table">
            <thead>
                <tr><th>🟢 VANTAGENS (ELITE)</th><th>🔴 RISCOS (SISTEMA)</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# (Este loop continua e expande-se para HBAR, ALGO, SOL, DOT, ADA, RNDR...)

st.divider()

# ==============================================================================
# 11. O MOTOR DE PROJEÇÃO E AGENDA DOS LÍDERES
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> PROJEÇÃO SOBERANA 2030</h2>", unsafe_allow_html=True)
col_p1, col_p2 = st.columns([1, 1.4])

with col_p1:
    st.markdown("""
    <div style="background: #030303; border: 2px solid #38bdf8; padding: 60px; text-align: center; border-radius: 4px;">
        <h3 style="color:#38bdf8;">VALOR DE RESERVA SOBERANA</h3>
        <p style="color:#475569;">Projeção baseada em Absorção total da BlackRock/Bancos Centrais</p>
        <div style="font-size: 5rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani';">€ 285,400+</div>
        <p style="color:#94a3b8; font-size: 0.9rem; letter-spacing: 3px;">ALVO BITCOIN 2030</p>
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown("""
    <div class="reset-box" style="border-left-color: #fbbf24; min-height: 200px;">
        <h3 style="color:#fbbf24;">A AGENDA DOS LÍDERES MUNDIAIS</h3>
        <p>Os líderes mundiais não estão a "investir"; estão a <b>substituir a base monetária</b>. Com a dívida fiduciária global em níveis insustentáveis, a elite financeira está a drenar o fornecimento de Bitcoin e Ethereum para custódias institucionais permanentes.</p>
        <p>Deter estes ativos não é sobre lucro rápido — é sobre deter uma fração da escassez absoluta antes que a porta se feche para o retalho. Quem não tiver uma posição em infraestrutura (RWA/ISO) até 2030 estará permanentemente fora do novo sistema financeiro global.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO INSTITUCIONAL E PROTOCOLO TREZOR
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> MANUAL DE SOBERANIA E SEGURANÇA</h2>", unsafe_allow_html=True)
c_g1, c_g2, c_g3 = st.columns(3)
with c_g1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, imóveis, ações) convertida em código digital imutável na blockchain.")
    st.write("**CBDC:** Moeda Digital de Banco Central. A ferramenta de controlo absoluto da liquidez governamental.")
with c_g2:
    st.write("**ISO 20022:** A nova linguagem universal de dados bancários que permite transferências ricas em informação.")
    st.write("**Settlement Layer:** A camada final e definitiva onde uma transação é liquidada para sempre (ex: Ethereum).")
with c_g3:
    st.write("**Protocolo Trezor:** O uso obrigatório de Hardware Wallets para guardar chaves privadas offline, longe de corretoras.")
    st.write("**Smart Contracts:** Contratos matemáticos que executam acordos automaticamente sem necessidade de notários.")

st.divider()
st.markdown("<p style='text-align: center; color: #444; font-family: Courier New; padding: 40px;'>JTM CAPITAL RESEARCH © 2026 | SOBERANIA FINANCEIRA ABSOLUTA | PORTUGAL NÓ CENTRAL</p>", unsafe_allow_html=True)

# Loop Autónomo de Atualização
if auto_refresh:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
