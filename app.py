import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DO SISTEMA & CONFIGURAÇÃO TÁTICA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Institutional Hub",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Painel de Comando Lateral (Side-Channel)
with st.sidebar:
    st.markdown("### ⚙️ COMANDO CENTRAL JTM")
    st.markdown("---")
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Telemetria de mercado sincronizada.")
    st.markdown("---")
    st.markdown("### 🔒 PROTOCOLO DE SEGURANÇA")
    st.warning("**OPERAÇÃO DCA:** ATIVA\n\n**DESTINO FINAL:** TREZOR\n\n**DATA CRÍTICA:** DIA 29")
    st.markdown("---")
    st.markdown("### 📊 ALOCAÇÃO MENSAL (360€)")
    st.progress(300/360, text="BASE (BTC/ETH): 300€")
    st.progress(60/360, text="SNIPER (ISO/DePIN): 60€")

# ==============================================================================
# 02. CSS CORPORATIVO: NEURO-DESIGN & DOPAMINA INSTITUCIONAL
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=Courier+New&display=swap');
    
    /* Fundo Global: Abismo Institucional */
    .stApp { 
        background-color: #02040a; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #02040a 80%); 
    }
    
    /* Tipografia de Comando */
    h1, h2, h3, h4 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1.5px; }
    p, li { line-height: 1.8; font-size: 1.05rem; color: #cbd5e1; }
    .highlight-blue { color: #38bdf8; font-weight: 700; }
    .highlight-green { color: #10b981; font-weight: 700; }
    .highlight-red { color: #ef4444; font-weight: 700; }
    
    /* Hero Section: Título Formal Original */
    .hero-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 3px solid #38bdf8;
        padding: 50px 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: left;
    }
    .hero-title {
        font-size: 3.5rem;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 2px;
        margin-bottom: 10px;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #38bdf8;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 4px;
        margin-top: 10px;
    }
    
    /* Cartões de Telemetria (Glassmorphism Avançado) */
    .telemetry-grid { display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; }
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(2, 4, 10, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 4px solid #38bdf8;
        padding: 20px;
        border-radius: 8px;
        flex: 1;
        min-width: 200px;
        transition: all 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.1); border-left: 4px solid #10b981; }
    .m-title { font-size: 1rem; color: #94a3b8; font-family: 'Courier New', monospace; font-weight: bold; }
    .m-price { font-size: 2rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; margin: 5px 0; }
    .m-data-row { display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 5px; }
    
    /* Containers de Artigos (Educação Profunda) */
    .edu-box {
        background-color: #0b1120;
        border: 1px solid #1e293b;
        border-top: 3px solid #34d399;
        padding: 35px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .edu-title { font-size: 2rem; color: #f8fafc; margin-bottom: 20px; border-bottom: 1px solid #1e293b; padding-bottom: 10px; }
    
    /* Feed de Notícias Global e Específico */
    .news-hub {
        background: #080c17;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 20px;
        height: 500px;
        overflow-y: auto;
    }
    .news-item {
        border-left: 2px solid #38bdf8;
        padding-left: 15px;
        margin-bottom: 15px;
        background: rgba(15, 23, 42, 0.4);
        padding: 15px;
        border-radius: 4px;
        transition: background 0.3s;
    }
    .news-item:hover { background: rgba(30, 41, 59, 0.8); }
    .news-item a { color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 1.1rem; }
    .news-item a:hover { color: #38bdf8; }
    .news-meta { font-size: 0.8rem; color: #64748b; margin-top: 5px; text-transform: uppercase; }
    
    /* Tabelas Táticas */
    .tactic-table { width: 100%; border-collapse: collapse; margin: 20px 0; background: #0b1120; border-radius: 8px; overflow: hidden; }
    .tactic-table th { background: #1e293b; color: #38bdf8; padding: 15px; text-align: left; font-family: 'Rajdhani'; font-size: 1.2rem; }
    .tactic-table td { border: 1px solid #1e293b; padding: 15px; color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MOTORES DE CÁLCULO E EXTRAÇÃO DE DADOS (CACHED)
# ==============================================================================

# Oferta Circulante (Circulating Supply) fixada para contornar bloqueios do Yahoo Finance
SUPPLY_MATRIX = {
    "BTC-EUR": 19_650_000,
    "ETH-EUR": 120_000_000,
    "LINK-EUR": 587_000_000,
    "XRP-EUR": 54_800_000_000,
    "QNT-EUR": 14_500_000,
    "XLM-EUR": 28_700_000_000,
    "RNDR-EUR": 388_000_000
}

@st.cache_data(ttl=25)
def fetch_telemetry(ticker):
    """Extração cirúrgica de dados de preço, volume e cálculo de Market Cap."""
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if len(df) >= 2:
            current = float(df['Close'].iloc[-1].item())
            prev = float(df['Close'].iloc[-2].item())
            change = ((current - prev) / prev) * 100
            vol = float(df['Volume'].iloc[-1].item())
            mcap = current * SUPPLY_MATRIX.get(ticker, 0)
            return current, change, vol, mcap
        return 0.0, 0.0, 0.0, 0.0
    except:
        return 0.0, 0.0, 0.0, 0.0

def format_currency(num):
    """Formatação matemática para leitura humana instantânea."""
    if num >= 1_000_000_000_000: return f"€ {(num / 1_000_000_000_000):.2f} T"
    if num >= 1_000_000_000: return f"€ {(num / 1_000_000_000):.2f} B"
    if num >= 1_000_000: return f"€ {(num / 1_000_000):.2f} M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_global_radar():
    """Agregador de notícias de espectro total (Múltiplas Fontes)."""
    sources = [
        ("CoinDesk Institutional", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("CoinTelegraph Global", "https://cointelegraph.com/rss"),
        ("CryptoSlate Analysis", "https://cryptoslate.com/feed/")
    ]
    radar_data = []
    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # Top 5 de cada fonte = 15 notícias
                radar_data.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.published[:22],
                    "source": source_name,
                    "timestamp": time.mktime(entry.published_parsed) if entry.published_parsed else 0
                })
        except:
            continue
    # Ordenar por data mais recente
    radar_data = sorted(radar_data, key=lambda x: x['timestamp'], reverse=True)
    return radar_data

@st.cache_data(ttl=600)
def fetch_asset_specific_news(keyword):
    """Filtro de inteligência militar para ativos específicos."""
    all_news = fetch_global_radar()
    filtered = [n for n in all_news if keyword.lower() in n['title'].lower()]
    return filtered[:4]

# ==============================================================================
# 04. HERO SECTION (APRESENTAÇÃO FORMAL E INSTITUCIONAL)
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH // INSTITUTIONAL THINK TANK</div>
    <div class="hero-subtitle">TRANSIÇÃO MACROECONÓMICA | RWA | ISO 20022</div>
    <p style="margin-top: 20px; color: #cbd5e1; max-width: 800px; font-size: 1.1rem;">
        Monitorização de grau militar sobre o colapso do sistema fiduciário legado (SWIFT) e a adoção massiva de infraestrutura criptográfica por gestoras de triliões de dólares (BlackRock, Fidelity). A JTM Capital opera baseada em utilidade matemática e fluxos de capital institucionais. Ruído de retalho e emoções são anomalias descartadas pelo sistema.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 05. PAINEL DE TELEMETRIA (TICKER TAPE DINÂMICO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> TELEMETRIA DO IMPÉRIO (EUR €)</h2>", unsafe_allow_html=True)

assets_matrix = {
    "BTC": ("BITCOIN (ESCUDO)", "BTC-EUR"),
    "ETH": ("ETHEREUM (BASE)", "ETH-EUR"),
    "LINK": ("CHAINLINK (ORÁCULO)", "LINK-EUR"),
    "XRP": ("RIPPLE (ISO 20022)", "XRP-EUR"),
    "QNT": ("QUANT (INTEROP)", "QNT-EUR"),
    "XLM": ("STELLAR (ISO 20022)", "XLM-EUR"),
    "RNDR": ("RENDER (DePIN)", "RNDR-EUR")
}

# Renderizar Cartões de Topo
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)

columns_array = [c1, c2, c3, c4, c5, c6, c7]

for i, (symbol, (name, ticker)) in enumerate(assets_matrix.items()):
    price, change, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    arrow = "▲" if change >= 0 else "▼"
    
    with columns_array[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name}</div>
            <div class="m-price">€ {price:,.3f}</div>
            <div style="color: {color}; font-weight: bold; font-family: 'Courier New';">{arrow} {abs(change):.2f}% (24H)</div>
            <div class="m-data-row">
                <span>V: {format_currency(vol)}</span>
                <span>MC: {format_currency(mcap)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with c8:
    st.markdown("""
    <div class="metric-card" style="border-left: 4px solid #8b5cf6; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 100%;">
        <div style="color: #a78bfa; font-family: 'Courier New'; font-weight: bold; font-size: 1.2rem;">ESTADO DA REDE</div>
        <div style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin-top: 10px;">SISTEMA ONLINE</div>
        <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">Sincronizado</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 06. CENTRO DE ANÁLISE GLOBAL (GRÁFICOS & RADAR DE NOTÍCIAS)
# ==============================================================================
col_chart, col_radar = st.columns([1.5, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO: BASE INSTITUCIONAL</h2>", unsafe_allow_html=True)
    
    @st.cache_data(ttl=900)
    def render_tactical_chart(ticker, title):
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#10b981', decreasing_line_color='#ef4444'
            )])
            fig.update_layout(
                title=dict(text=title, font=dict(color='#e2e8f0', size=16, family='Rajdhani')),
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=0), xaxis_rangeslider_visible=False, height=450,
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)'), xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
            
    render_tactical_chart("BTC-EUR", "BITCOIN (BTC/EUR) - Ação de Preço (60 Dias)")

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR DE INTELIGÊNCIA GLOBAL</h2>", unsafe_allow_html=True)
    st.markdown('<div class="news-hub">', unsafe_allow_html=True)
    
    global_news = fetch_global_radar()
    for item in global_news:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">{item['title']}</a>
            <div class="news-meta">{item['source']} | {item['date']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. THINK TANK EDUCACIONAL (O MANIFESTO E EXPLICAÇÃO PROFUNDA)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> ARQUITETURA MACROECONÓMICA 2026-2030</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="edu-box">
    <div class="edu-title">I. O Colapso do Dinheiro de Papel e a Fuga para a Escassez</div>
    <p>O cidadão comum assume que o Euro ou o Dólar são unidades de medida estáveis. A matemática corporativa prova o contrário. Desde a rutura do padrão-ouro em 1971, o dinheiro fiduciário é criado com base em dívida. Quando os bancos centrais (FED, BCE) imprimem triliões para cobrir défices governamentais, não estão a criar riqueza; estão a diluir o poder de compra da moeda que o trabalhador retém na sua conta bancária.</p>
    <p>A <span class="highlight-blue">JTM Capital</span> reconhece este fenómeno como um "imposto oculto". Para proteger a energia económica, o capital institucional iniciou uma migração massiva para a <span class="highlight-green">Camada 0 da soberania financeira: O Bitcoin</span>. Sendo um protocolo matemático rigidamente limitado a 21 milhões de unidades, o Bitcoin é inconfiscável, inalterável e imune a governos. É o escudo da nossa Base.</p>
</div>

<div class="edu-box">
    <div class="edu-title">II. Tokenização de Ativos (RWA): O Mundo Físico na Blockchain</div>
    <p>Se o Bitcoin é o novo ouro, redes como o <span class="highlight-blue">Ethereum</span> são a nova bolsa de valores, notários e tribunais combinados. A tokenização de Real World Assets (RWA) é a representação digital de ativos físicos em redes blockchain.</p>
    <p><b>O Exemplo da Imobiliária:</b> Um arranha-céus de 100 milhões de euros no Dubai é um ativo ilíquido (difícil de vender rapidamente). Através da RWA, a propriedade desse edifício é programada num "Smart Contract" no Ethereum e dividida em 100 milhões de tokens de 1 euro. Qualquer investidor asiático, europeu ou americano pode comprar 50€ desse edifício instantaneamente num domingo à noite, recebendo rendas proporcionais automaticamente na sua carteira digital. A BlackRock já está a fazer isto com obrigações do tesouro americano através do seu fundo BUIDL. É a digitalização total do capital mundial.</p>
</div>

<div class="edu-box">
    <div class="edu-title">III. Norma ISO 20022 e a Morte do SWIFT</div>
    <p>O sistema SWIFT, que atualmente gere as transferências de dinheiro entre países, funciona como um serviço de correio da década de 70. Uma transferência de Lisboa para Tóquio pode demorar dias e passar por múltiplos bancos correspondentes, cada um cobrando a sua taxa.</p>
    <p>O mundo financeiro está a ser forçado a adotar a <span class="highlight-blue">ISO 20022</span>, uma linguagem comum para dados financeiros eletrónicos. O problema? Os servidores legados dos bancos não suportam o volume de dados em tempo real. A solução? Redes criptográficas institucionais como a <span class="highlight-green">Ripple (XRP)</span> e a <span class="highlight-green">Stellar (XLM)</span>. Estas redes foram desenhadas especificamente para atuar como pontes. Um banco central europeu pode converter Euros em XRP, enviá-lo para o Japão em 3 segundos, e lá ser convertido em Ienes. Zero fricção. Zero dias de espera. A JTM Capital acumula a infraestrutura (XRP/QNT) que os bancos serão obrigados a usar.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. DOSSIÊS TÁTICOS (ANÁLISE INDIVIDUAL DE ATIVOS & NOTÍCIAS ESPECÍFICAS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> DOSSIÊS DE INFRAESTRUTURA (PELOTÃO JTM)</h2>", unsafe_allow_html=True)
st.write("Análise de inteligência, prós, contras e fluxo de notícias filtrado por ativo. Clique nos separadores abaixo para aceder ao terminal individual.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "₿ BITCOIN (BTC)", "⟠ ETHEREUM (ETH)", "🔗 CHAINLINK (LINK)", 
    "✕ RIPPLE (XRP)", "◎ STELLAR (XLM)", "Ⓠ QUANT (QNT)", "🧊 RENDER (RNDR)"
])

def render_asset_intel(name, ticker, role, thesis, pros, cons, keyword):
    c_left, c_right = st.columns([1.5, 1])
    
    with c_left:
        st.markdown(f"### Função Tática: {role}")
        st.write(thesis)
        
        st.markdown("""
        <table class="tactic-table">
            <tr><th style="border-left: 4px solid #10b981;">🟢 MATRIZ POSITIVA (PRÓS)</th><th style="border-left: 4px solid #ef4444;">🔴 MATRIZ NEGATIVA (CONTRAS)</th></tr>
            <tr>
                <td style="vertical-align: top;"><ul>""" + "".join([f"<li>{p}</li>" for p in pros]) + """</ul></td>
                <td style="vertical-align: top;"><ul>""" + "".join([f"<li>{c}</li>" for c in cons]) + """</ul></td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
    with c_right:
        st.markdown(f"### 📡 Interceções de Radar ({name})")
        asset_news = fetch_asset_specific_news(keyword)
        
        if len(asset_news) > 0:
            for item in asset_news:
                st.markdown(f"""
                <div style="background: rgba(15,23,42,0.8); padding: 12px; margin-bottom: 10px; border-radius: 6px; border-left: 2px solid #38bdf8; font-size: 0.9rem;">
                    <a href="{item['link']}" target="_blank" style="color: #cbd5e1; text-decoration: none; font-weight: bold;">{item['title']}</a><br>
                    <span style="color: #64748b; font-size: 0.8rem;">{item['date']} | {item['source']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"O sistema de escuta não detetou manchetes primárias recentes contendo o alvo '{keyword}'.")

with tab1:
    render_asset_intel(
        "Bitcoin", "BTC-EUR", "O Escudo Monetário (Camada 0)",
        "O Bitcoin é a base do portefólio. Funciona como propriedade digital imutável. A aprovação dos ETFs em Wall Street legitimizou o ativo permanentemente perante governos e fundos de pensões. É a nossa proteção primária contra a emissão infinita de euros.",
        ["Adoção institucional irreversível (BlackRock).", "Escassez absoluta e provada (21M).", "Rede computacional mais resiliente do mundo."],
        ["Velocidade de transação lenta (sem uso da Lightning Network).", "Consumo energético criticado por políticos (risco regulatório ambiental).", "Incapacidade de correr contratos inteligentes nativamente."],
        "bitcoin"
    )

with tab2:
    render_asset_intel(
        "Ethereum", "ETH-EUR", "A Autoestrada Global (Infraestrutura RWA)",
        "A fundação da economia digital descentralizada (DeFi) e da tokenização de ativos. Se o Bitcoin é ouro, o Ethereum é o petróleo digital que faz os Smart Contracts funcionarem. Qualquer transação RWA de grande escala exige ETH para pagar a rede (Gas).",
        ["Dominância absoluta no mercado de Tokenização RWA.", "Modelo económico deflacionário (queima de tokens após EIP-1559).", "Gera rendimento passivo ('yield') através de Staking institucional."],
        ["Taxas de rede (Gas fees) podem tornar-se exorbitantes.", "Dependência de redes de Camada 2 (Layer 2) para escalar.", "Concorrência de protocolos mais recentes (Solana, Sui)."],
        "ethereum"
    )

with tab3:
    render_asset_intel(
        "Chainlink", "LINK-EUR", "O Oráculo de Dados (O Olho da Blockchain)",
        "Blockchains são sistemas fechados; não sabem o preço da Apple, a temperatura exterior ou resultados eleitorais. A Chainlink fornece estes dados ('Oráculos') de forma descentralizada. Sem a Chainlink, as corporações não podem criar contratos baseados no mundo real.",
        ["Monopólio prático no fornecimento de dados seguros (Oráculos).", "Protocolo CCIP estabelece o padrão para comunicação entre blockchains diferentes.", "Parcerias ativas com o SWIFT para modernização bancária."],
        ["O retalho tem dificuldade em entender a utilidade técnica, preferindo moedas especulativas.", "Dependência indireta do sucesso da rede Ethereum.", "Complexidade na tokenomics para gerar pressão de compra massiva."],
        "chainlink"
    )

with tab4:
    render_asset_intel(
        "Ripple", "XRP-EUR", "Veículo de Liquidez Bancária (ISO 20022)",
        "Ocultado por controvérsias jurídicas (já vencidas), o XRP foi desenhado matematicamente para ser a ponte de liquidação entre moedas de bancos centrais (CBDCs). É a alternativa rápida, barata e verde ao arcaico sistema SWIFT.",
        ["Claridade jurídica nos EUA após vitória contra a SEC.", "Liquidação de transações em 3-5 segundos a custos residuais.", "Integração profunda e desde o início com os padrões ISO 20022."],
        ["A empresa Ripple Labs ainda detém uma porção massiva de XRP bloqueado (Escrow).", "Forte resistência da comunidade 'cypherpunk' devido à sua natureza corporativa.", "Depende da vontade política dos bancos em abandonar o SWIFT inteiramente."],
        "ripple"
    )

with tab5:
    render_asset_intel(
        "Stellar", "XLM-EUR", "Pagamentos Transfronteiriços Inclusivos (ISO 20022)",
        "Nascida do mesmo núcleo tecnológico que o XRP, a Stellar foca-se em remessas internacionais e parcerias corporativas (como a IBM). Uma ferramenta letal para tokenizar moedas fiduciárias em países em desenvolvimento.",
        ["Parcerias estabelecidas com gigantes tecnológicos (IBM, MoneyGram).", "Arquitetura ISO 20022 pronta para uso institucional.", "Transações quase gratuitas ideais para micro-pagamentos."],
        ["A narrativa de mercado perde frequentemente a batalha de marketing para a Ripple.", "Abundância histórica de oferta circulante afetou o preço no passado.", "Competição feroz não só da Ripple, mas de stablecoins em outras redes."],
        "stellar"
    )

with tab6:
    render_asset_intel(
        "Quant", "QNT-EUR", "O Sistema Operativo Institucional (Interop)",
        "Bancos Centrais não vão usar blockchains públicas abertas. Vão criar as suas redes privadas. O Overledger da Quant é o software que permite a um Banco em França (rede privada) interagir com o Ethereum (rede pública) de forma segura. O token QNT é a licença de software.",
        ["Permite interoperabilidade sem criar uma nova blockchain (é um Sistema Operativo).", "Oferta circulante extremamente limitada (apenas 14.5M de QNT).", "Foco cirúrgico em clientes corporativos e governamentais (B2B/B2G)."],
        ["Código proprietário (não open-source) contraria a filosofia descentralizada.", "O retalho não utiliza a rede, o que reduz o 'hype' social.", "Sucesso depende inteiramente da adoção de CBDCs pelos governos."],
        "quant"
    )

with tab7:
    render_asset_intel(
        "Render", "RNDR-EUR", "Rede DePIN (Infraestrutura de IA)",
        "A ascensão da Inteligência Artificial requer quantidades insanas de poder de computação (GPUs). A rede Render permite que qualquer pessoa no mundo alugue o poder da sua placa gráfica ociosa para criadores e empresas de IA. É a Uberização do hardware.",
        ["Resolve um problema físico real: a falta global de GPUs para processamento de IA.", "Substitui modelos centralizados e caros como a Amazon AWS e Google Cloud.", "Base de clientes em expansão massiva (Estúdios de Hollywood, Startups de IA)."],
        ["Fortemente correlacionado com bolhas especulativas de IA; se a IA abrandar, o Render cai.", "Depende do fornecimento global de hardware (Nvidia, AMD).", "Concorrência de outros projetos DePIN (Akash, Bittensor) a surgir."],
        "render"
    )

st.divider()

# ==============================================================================
# 09. GLOSSÁRIO INSTITUCIONAL (EDUCAÇÃO DE MASSAS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
c_glos1, c_glos2 = st.columns(2)

with c_glos1:
    st.markdown("""
    * **DCA (Dollar Cost Averaging):** A técnica militar de investimento. Consiste em comprar o ativo num dia fixo do mês (ex: dia 29), independentemente de o preço estar alto ou baixo. Elimina as emoções e a tentativa falhada de "adivinhar" o mercado.
    * **Hardware Wallet (ex: Trezor):** Um dispositivo físico semelhante a uma pen USB que guarda as chaves criptográficas offline. Moedas deixadas numa corretora (Binance, Coinbase) pertencem à corretora. Moedas na Trezor pertencem a si.
    * **Fiat / Dinheiro Fiduciário:** Moedas decretadas por governos (Euro, Dólar) que não têm lastro em ouro ou qualquer ativo físico. O seu valor é mantido apenas pela confiança e pela imposição governamental de pagamento de impostos.
    """)

with c_glos2:
    st.markdown("""
    * **Smart Contracts (Contratos Inteligentes):** Programas de computador alojados na blockchain (como no Ethereum) que executam um acordo automaticamente quando as condições são cumpridas. Eliminam advogados, notários e intermediários bancários.
    * **CBDC (Central Bank Digital Currency):** Moedas digitais emitidas por bancos centrais (ex: Euro Digital). Ao contrário das criptomoedas como o Bitcoin (descentralizadas e livres), as CBDCs são centralizadas e permitem controlo total do Estado sobre os gastos dos cidadãos.
    * **DePIN:** Decentralized Physical Infrastructure Networks. O uso de tokens blockchain para incentivar as pessoas a construírem redes de infraestrutura no mundo real (antenas de wi-fi, partilha de poder de computação para IA, mapas).
    """)

st.divider()

# ==============================================================================
# 10. RODAPÉ E MOTOR AUTÓNOMO DE RERUN
# ==============================================================================
st.markdown("""
<div style="text-align: center; color: #64748b; font-family: 'Courier New', monospace; padding: 20px;">
    <strong>JTM CAPITAL RESEARCH © 2026</strong><br>
    NÓ ESTRATÉGICO DE PORTUGAL | OPERAÇÃO DE ACUMULAÇÃO DE ATIVOS RWA<br>
    <em>"A soberania financeira exige a substituição do intermediário humano por matemática inquebrável."</em>
</div>
""", unsafe_allow_html=True)

# Loop de Sincronização
if auto_update:
    time.sleep(30)
    st.rerun()
