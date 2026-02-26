import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DO SISTEMA, MEMÓRIA ROTATIVA E CONFIGURAÇÃO TÁTICA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL RESEARCH | Terminal de Operações",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicializar a memória de paginação das notícias (Roda a cada 30s)
if 'news_page' not in st.session_state:
    st.session_state.news_page = 0

# Inicializar memória para o Simulador DCA
if 'dca_months' not in st.session_state:
    st.session_state.dca_months = 48 # Meses até 2030

# Painel de Comando Lateral (Side-Channel)
with st.sidebar:
    st.markdown("### ⚙️ COMANDO CENTRAL JTM")
    st.markdown("---")
    
    auto_update = st.toggle("🟢 RADAR ATIVO (30s)", value=True)
    st.caption("Telemetria de mercado e paginação de notícias em sincronia perfeita.")
    
    st.markdown("---")
    st.markdown("### 🔒 PROTOCOLO DE SOBERANIA")
    st.warning("""
    **OPERAÇÃO DCA:** ATIVA (DCA Implacável)
    **DESTINO FINAL:** TREZOR (Cold Storage)
    **DATA CRÍTICA:** DIA 29 DE CADA MÊS
    """)
    
    st.markdown("---")
    st.markdown("### 📊 ORÇAMENTO TÁTICO (360€/MÊS)")
    st.progress(300/360, text="A BASE (ETH/BTC): 300€")
    st.caption("Foco: Escudo Monetário e Autoestrada Global.")
    
    st.progress(60/360, text="PELOTÃO SNIPER: 60€")
    st.caption("Foco: ISO 20022 (XRP/XLM/QNT) & Oráculos/DePIN (LINK/RNDR).")
    
    st.markdown("---")
    st.markdown("### ⏱️ RELÓGIO DO SISTEMA")
    st.info(f"Sessão iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nModo: Operacional Nível 5")

# ==============================================================================
# 02. CSS CORPORATIVO: NEURO-DESIGN, DOPAMINA E LEITURA INSTITUCIONAL
# ==============================================================================
st.markdown("""
<style>
    /* Importação de Fontes Premium */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600;800&family=Courier+New&display=swap');
    
    /* Fundo Global: Abismo Institucional (Dark Mode Absoluto com Gradiente) */
    .stApp { 
        background-color: #02040a; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #02040a 80%); 
    }
    
    /* Tipografia de Comando e Títulos */
    h1, h2, h3, h4 { 
        color: #ffffff; 
        font-family: 'Rajdhani', sans-serif; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
    }
    p, li { 
        line-height: 1.8; 
        font-size: 1.05rem; 
        color: #cbd5e1; 
    }
    
    /* Destaques de Cor Tática */
    .highlight-blue { color: #38bdf8; font-weight: 700; }
    .highlight-green { color: #10b981; font-weight: 700; }
    .highlight-red { color: #ef4444; font-weight: 700; }
    .highlight-gold { color: #fbbf24; font-weight: 700; }
    
    /* Hero Section: Título Formal e Efeito Glassmorphism */
    .hero-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-top: 3px solid #38bdf8;
        padding: 40px 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        background: linear-gradient(135deg, transparent 0%, rgba(56, 189, 248, 0.05) 100%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 3.2rem;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 2px;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    
    /* Cartões de Telemetria (Efeitos Hover e Sombras Dinâmicas) */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(2, 4, 10, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 4px solid #38bdf8;
        padding: 20px;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover { 
        transform: translateY(-5px) scale(1.02); 
        box-shadow: 0 15px 30px rgba(56, 189, 248, 0.15); 
        border-left: 4px solid #10b981; 
    }
    .m-title { font-size: 1rem; color: #94a3b8; font-family: 'Courier New', monospace; font-weight: bold; }
    .m-price { font-size: 1.8rem; color: #ffffff; font-weight: 800; font-family: 'Rajdhani'; margin: 5px 0; }
    .m-data-row { display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 5px; }
    
    /* Radar Compacto Rotativo (Otimização de Espaço e Foco) */
    .news-hub-compact { 
        background: #080c17; 
        border: 1px solid #1e293b; 
        border-left: 4px solid #8b5cf6; 
        border-radius: 8px; 
        padding: 15px; 
        height: 100%; 
        min-height: 400px; 
    }
    .news-item { 
        background: rgba(15, 23, 42, 0.6); 
        padding: 12px; 
        margin-bottom: 10px; 
        border-radius: 4px; 
        border-left: 2px solid #38bdf8; 
        transition: background 0.3s; 
    }
    .news-item:hover { background: rgba(30, 41, 59, 0.9); border-left: 2px solid #10b981;}
    .news-item a { color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 0.95rem; }
    .news-meta { font-size: 0.75rem; color: #64748b; margin-top: 5px; text-transform: uppercase; }
    
    /* Containers de Artigos (Educação Profunda e Manifesto) */
    .edu-box {
        background-color: #0b1120;
        border: 1px solid #1e293b;
        border-top: 3px solid #34d399;
        padding: 35px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .edu-title { 
        font-size: 1.8rem; 
        color: #f8fafc; 
        margin-bottom: 20px; 
        border-bottom: 1px solid #1e293b; 
        padding-bottom: 10px; 
    }
    
    /* Tabelas Táticas e Matrizes de Risco */
    .tactic-table { 
        width: 100%; 
        border-collapse: collapse; 
        margin: 20px 0; 
        background: #0b1120; 
        border-radius: 8px; 
        overflow: hidden; 
    }
    .tactic-table th { 
        background: #1e293b; 
        color: #38bdf8; 
        padding: 15px; 
        text-align: left; 
        font-family: 'Rajdhani'; 
        font-size: 1.2rem; 
    }
    .tactic-table td { 
        border: 1px solid #1e293b; 
        padding: 15px; 
        color: #cbd5e1; 
        vertical-align: top;
    }
    
    /* Calendário Macro e Tabelas de Eventos */
    .event-row { display: flex; border-bottom: 1px solid #1e293b; padding: 10px 0; }
    .event-date { width: 120px; color: #fbbf24; font-family: 'Courier New'; font-weight: bold; }
    .event-desc { flex: 1; color: #cbd5e1; }
    
    /* Simulador DCA Container */
    .simulator-box {
        background: linear-gradient(45deg, #0f172a, #02040a);
        border: 1px solid #38bdf8;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        margin-top: 20px;
    }
    .sim-number { font-size: 3rem; color: #10b981; font-weight: 900; font-family: 'Rajdhani'; }
    .sim-label { font-size: 1rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZES DE DADOS INSTITUCIONAIS (ARQUITETURA MASSIVA)
# ==============================================================================
# Oferta Circulante (Circulating Supply) fixada para cálculo de Market Cap imune a bloqueios de API
SUPPLY_MATRIX = {
    "BTC-EUR": 19_650_000,
    "ETH-EUR": 120_000_000,
    "LINK-EUR": 587_000_000,
    "XRP-EUR": 54_800_000_000,
    "QNT-EUR": 14_500_000,
    "XLM-EUR": 28_700_000_000,
    "RNDR-EUR": 388_000_000
}

# Dossiê Tático Completo: Parceiros, Casos de Uso e Teses (Motor para as Tabs)
ASSET_DOSSIER = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "keyword": "bitcoin",
        "role": "O Escudo Monetário (Camada 0)",
        "thesis": "O Bitcoin é a base do portefólio. Funciona como propriedade digital imutável. A aprovação dos ETFs em Wall Street legitimizou o ativo permanentemente perante governos e fundos de pensões. É a nossa proteção primária contra a emissão infinita de euros promovida pelo Banco Central Europeu.",
        "pros": ["Adoção institucional irreversível (BlackRock, Fidelity, Ark Invest).", "Escassez absoluta e matematicamente provada (21 Milhões de unidades limite).", "Rede computacional descentralizada mais resiliente e segura do planeta.", "Funciona como a derradeira reserva de valor ('Ouro Digital')."],
        "cons": ["Velocidade de transação nativa lenta (se não utilizar a Lightning Network).", "Consumo energético frequentemente atacado por narrativas políticas ambientais.", "Incapacidade de correr contratos inteligentes complexos de forma nativa na camada 1."],
        "partners": "BlackRock, MicroStrategy, Fidelity, CME Group, Wall Street."
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "keyword": "ethereum",
        "role": "A Autoestrada Global (Infraestrutura RWA)",
        "thesis": "A fundação da economia digital descentralizada (DeFi) e da tokenização de ativos reais. Se o Bitcoin é o ouro, o Ethereum é o petróleo digital que faz os Smart Contracts funcionarem. Qualquer transação RWA de grande escala exige ETH para pagar o custo computacional da rede (Gas).",
        "pros": ["Dominância absoluta no mercado emergente de Tokenização RWA (ex: Fundo BUIDL da BlackRock).", "Modelo económico deflacionário (queima contínua de tokens de taxa de rede após EIP-1559).", "Gera rendimento passivo sustentável ('yield') através de Staking institucional.", "Maior comunidade de programadores e capital intelectual do mundo web3."],
        "cons": ["Taxas de rede (Gas fees) podem tornar-se proibitivas para o retalho durante congestionamentos.", "Forte dependência tecnológica de redes secundárias de Camada 2 (L2) para escalar globalmente.", "Concorrência agressiva de protocolos monolíticos mais recentes (Solana, Sui, Aptos)."],
        "partners": "BlackRock (BUIDL), JPMorgan (Onyx), Microsoft, EEA."
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "keyword": "chainlink",
        "role": "O Oráculo de Dados Institucional",
        "thesis": "As Blockchains são sistemas matemáticos fechados; são 'cegas' e não sabem o preço da ação da Apple, a temperatura exterior ou resultados logísticos. A Chainlink fornece estes dados ('Oráculos') de forma criptograficamente segura. Sem a Chainlink, a automação corporativa de contratos é impossível.",
        "pros": ["Monopólio prático e não oficial no fornecimento de dados seguros (Oráculos descentralizados).", "O seu protocolo CCIP está a estabelecer o padrão global para comunicação inter-blockchains.", "Parcerias ativas com o sistema SWIFT e DTCC (Depository Trust & Clearing Corp).", "Fundamental para a liquidação de derivativos e tokenização de imobiliário."],
        "cons": ["O investidor de retalho tem extrema dificuldade em entender a utilidade infraestrutural técnica.", "A geração de pressão de compra (Tokenomics) é complexa e depende da adoção de serviços.", "Sucesso indiretamente atrelado à adoção em massa da rede Ethereum e protocolos DeFi."],
        "partners": "SWIFT, DTCC, Google Cloud, Oracle, Synthetix, Aave."
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "keyword": "ripple",
        "role": "Veículo de Liquidez Interbancária (ISO 20022)",
        "thesis": "Desenhado estritamente como tecnologia B2B. O XRP foi programado matematicamente para ser a ponte de liquidação entre diferentes moedas fiduciárias e futuras moedas de bancos centrais (CBDCs). É a alternativa de alta velocidade, baixo custo e carbono neutro ao arcaico e lento sistema de mensagens SWIFT.",
        "pros": ["Atingiu claridade jurídica sem precedentes nos EUA após vitória massiva contra a SEC.", "Liquidação física de transações transfronteiriças em 3 a 5 segundos a custos fraionais.", "Integração profunda de raiz com os novos padrões obrigatórios de dados bancários ISO 20022.", "Capacidade de processar dezenas de milhares de transações por segundo em canais de pagamento."],
        "cons": ["A empresa detentora (Ripple Labs) ainda possui acesso a uma porção massiva de XRP bloqueado em Escrow.", "Enfrenta forte resistência filosófica da comunidade 'cypherpunk' devido ao seu alinhamento com a banca.", "A adoção plena depende da vontade geopolítica dos bancos centrais em abandonar o monopólio do SWIFT."],
        "partners": "SBI Holdings, Banco Santander, Autoridades Monetárias Asiáticas, Mastercard."
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "keyword": "stellar",
        "role": "Pagamentos Inclusivos e Remessas Globais (ISO)",
        "thesis": "Nascida a partir do mesmo código fundacional que o XRP, a Stellar foca-se menos nos bancos centrais de topo e mais nas remessas internacionais, parcerias corporativas e inclusão financeira. Uma ferramenta letal e testada para tokenizar moedas fiduciárias em países em desenvolvimento e mercados emergentes.",
        "pros": ["Parcerias corporativas históricas e firmes com gigantes tecnológicos (IBM, MoneyGram).", "Arquitetura técnica totalmente compatível com a norma ISO 20022 para uso institucional.", "Transações quase instantâneas e gratuitas, tornando-a a rede ideal para micro-pagamentos B2C.", "Fundação Stellar tem um foco forte na tokenização de ativos em jurisdições em desenvolvimento."],
        "cons": ["A narrativa de mercado perde frequentemente a batalha de marketing e atenção para o seu irmão/rival XRP.", "Historicamente sofreu com inflação da oferta circulante que suprimiu a apreciação exponencial do preço.", "Enfrenta competição feroz de stablecoins (USDC/USDT) a operar em redes de Camada 2 ou Solana."],
        "partners": "IBM (World Wire), MoneyGram, USDC (Circle), Governo Ucraniano (Pilotos CBDC)."
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "keyword": "quant",
        "role": "O Sistema Operativo Institucional (Interop)",
        "thesis": "A tese mais subvalorizada pelo retalho: Os Governos e Bancos Centrais NÃO vão utilizar blockchains públicas abertas para as suas CBDCs. Vão criar redes privadas fechadas (DLTs). O software Overledger da Quant é a API patenteada que permite a um Banco (na sua rede privada) interagir e enviar fundos para o Ethereum (rede pública) de forma certificada. O token QNT atua como a licença de pagamento obrigatória para usar este software B2B.",
        "pros": ["Abordagem única: Permite a interoperabilidade total sem criar ou forçar a adoção de mais uma nova blockchain.", "Oferta circulante absurdamente escassa (aproximadamente 14.5 milhões de tokens totais, a maioria em circulação).", "Foco cirúrgico e exclusivo em clientes de nível superior corporativo, institucional e governamental (B2B/B2G).", "Isolado do ruído especulativo de NFTs e Memecoins."],
        "cons": ["Código do Overledger é proprietário (fechado/patenteado), contrariando a filosofia open-source do mercado.", "A absoluta falta de ferramentas e incentivos para o investidor de retalho reduz drasticamente o 'hype' social.", "O sucesso e a captura de valor dependem inteiramente da emissão real e regulamentada de CBDCs mundiais."],
        "partners": "Oracle, SIA (Rede Interbancária Europeia), Nexi Group, LacChain."
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "keyword": "render",
        "role": "Infraestrutura Física DePIN (Revolução IA)",
        "thesis": "A maior narrativa tecnológica da década (Inteligência Artificial) colidiu com a barreira física: a falta extrema de poder de computação (GPUs). A rede Render resolve isto descentralizando o poder de hardware. Qualquer pessoa ou data-center no mundo pode alugar o poder da sua placa gráfica ociosa para estúdios 3D, criadores e empresas de treino de IA que necessitam desesperadamente de capacidade computacional. É a 'Uberização' global do hardware.",
        "pros": ["Resolve um estrangulamento físico e comercial massivo do mundo real: a falta global de chips e GPUs para processamento de IA.", "Desafia o oligopólio de serviços centralizados de cloud altamente dispendiosos (Amazon AWS, Google Cloud, Microsoft Azure).", "A base de clientes pagantes reais está em expansão massiva (Estúdios de Hollywood, Startups de renderização e IA generativa).", "Migração bem-sucedida para a rede Solana, permitindo micro-pagamentos super rápidos entre criadores e fornecedores de GPU."],
        "cons": ["O preço do token está perigosamente correlacionado com o ciclo de 'hype' especulativo em torno das empresas de IA tradicionais (Nvidia).", "Depende fortemente do fornecimento global contínuo de hardware avançado, sendo vulnerável a ruturas nas cadeias de abastecimento de chips.", "Concorrência intensificada no setor DePIN com a chegada de novos protocolos concorrentes (Akash Network, Bittensor, io.net)."],
        "partners": "Apple (integrações de software Octane), OTOY, Cinema4D, ecossistema Solana."
    }
}

# Base de Dados do Calendário Macroeconómico Institucional
MACRO_EVENTS = [
    {"date": "Março 2026", "event": "Reunião FOMC (Reserva Federal dos EUA)", "impact": "Alta", "desc": "Decisão sobre a taxa de juro diretora. Cortes injetam liquidez em ativos de risco (BTC/ETH)."},
    {"date": "Abril 2026", "event": "Halving Report (Efeito 2 Anos)", "impact": "Média", "desc": "Análise matemática do choque de oferta do Bitcoin pós-Halving de 2024."},
    {"date": "29 Mensal", "event": "Operação DCA JTM Capital", "impact": "Absoluta", "desc": "Injeção de 360€ de capital fiduciário (300 Base / 60 Sniper). A transferência para a Trezor ocorre nas 24h seguintes."},
    {"date": "Nov 2026", "event": "Prazo Mandatório SWIFT ISO 20022", "impact": "Extrema", "desc": "Todos os bancos e instituições financeiras de relevo são obrigados a transitar para a norma de mensagens rica em dados. Catalisador massivo para XRP, XLM e QNT."}
]

# ==============================================================================
# 04. MOTORES DE EXTRAÇÃO DE DADOS (CACHED PARA PREVENIR TIMEOUTS)
# ==============================================================================
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
    if num >= 1_000_000_000_000: return f"€ {(num / 1_000_000_000_000):.2f} T"
    if num >= 1_000_000_000: return f"€ {(num / 1_000_000_000):.2f} B"
    if num >= 1_000_000: return f"€ {(num / 1_000_000):.2f} M"
    return f"€ {num:,.0f}"

@st.cache_data(ttl=600)
def fetch_global_radar():
    """Agregador de notícias de espectro total (Múltiplas Fontes de topo)."""
    sources = [
        ("CoinDesk Inst.", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("CoinTelegraph", "https://cointelegraph.com/rss"),
        ("CryptoSlate", "https://cryptoslate.com/feed/")
    ]
    radar_data = []
    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]: 
                radar_data.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.published[:22] if hasattr(entry, 'published') else "Recente",
                    "source": source_name,
                    "timestamp": time.mktime(entry.published_parsed) if hasattr(entry, 'published_parsed') and entry.published_parsed else 0
                })
        except:
            continue
    # Ordenação temporal garantida
    return sorted(radar_data, key=lambda x: x['timestamp'], reverse=True)

@st.cache_data(ttl=600)
def fetch_asset_specific_news(keyword):
    """Filtro de interceção militar para ativos específicos do portefólio."""
    all_news = fetch_global_radar()
    filtered = [n for n in all_news if keyword.lower() in n['title'].lower()]
    return filtered[:4]

# ==============================================================================
# 05. HERO SECTION E DECLARAÇÃO DE MISSÃO (O MANIFESTO ORIGINAL)
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">JTM CAPITAL RESEARCH // INSTITUTIONAL THINK TANK</div>
    <div style="font-size: 1.3rem; color: #38bdf8; font-family: 'Rajdhani'; letter-spacing: 3px; font-weight: bold;">
        ARQUITETURA MACROECONÓMICA | RWA | ISO 20022
    </div>
    <p style="margin-top: 20px; color: #cbd5e1; max-width: 900px; font-size: 1.1rem; border-left: 4px solid #10b981; padding-left: 15px;">
        Bem-vindo ao centro de comando. Monitorizamos com precisão de grau militar o colapso estrutural do sistema fiduciário legado (SWIFT) e a adoção massiva de infraestrutura criptográfica por gestoras de triliões de dólares (BlackRock, Fidelity, Vanguard). A <b>JTM Capital</b> opera baseada exclusivamente em utilidade matemática verificada, tokenização (RWA) e fluxos de capital institucionais.<br><br>
        O ruído gerado por especuladores de retalho, memecoins e analistas de redes sociais são anomalias descartadas ativamente por este sistema. O nosso foco é a soberania financeira absoluta até 2030, acumulando a infraestrutura invisível que os bancos usarão amanhã.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. PAINEL DE TELEMETRIA (TICKER TAPE E ESTADO DA REDE)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> TELEMETRIA DO IMPÉRIO (EUR €)</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
columns_array = [c1, c2, c3, c4, c5, c6, c7]

assets_keys = list(ASSET_DOSSIER.keys())

for i, symbol in enumerate(assets_keys):
    ticker = ASSET_DOSSIER[symbol]["ticker"]
    name_display = f"{ASSET_DOSSIER[symbol]['name'].upper()} ({symbol})"
    
    price, change, vol, mcap = fetch_telemetry(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    arrow = "▲" if change >= 0 else "▼"
    
    with columns_array[i]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-title">{name_display}</div>
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
    <div class="metric-card" style="border-left: 4px solid #8b5cf6; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <div style="color: #a78bfa; font-family: 'Courier New'; font-weight: bold; font-size: 1.2rem; letter-spacing: 2px;">STATUS DO NÓ</div>
        <div style="color: #ffffff; font-size: 1.8rem; font-weight: 800; margin-top: 5px;">ONLINE</div>
        <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">Link Institucional Estabelecido</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. CENTRO VISUAL: GRÁFICO TÁTICO, MEDIDOR GAUGE E RADAR ROTATIVO
# ==============================================================================
col_chart, col_gauge, col_radar = st.columns([1.5, 1, 1])

with col_chart:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> VETOR DE PREÇO TÁTICO (BTC/EUR)</h2>", unsafe_allow_html=True)
    
    @st.cache_data(ttl=900)
    def render_tactical_chart(ticker):
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#10b981', decreasing_line_color='#ef4444'
            )])
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=55, r=20, t=10, b=30), # Margem esquerda cirurgicamente ajustada para os eixos Y
                xaxis_rangeslider_visible=False, height=420,
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€", showticklabels=True),
                xaxis=dict(showgrid=False, color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
    render_tactical_chart("BTC-EUR")

with col_gauge:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> FORÇA DE ACUMULAÇÃO</h2>", unsafe_allow_html=True)
    # Gráfico de Velocímetro (Estilo CoinDesk / Glassnode Trend)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 86,
        title = {'text': "FLUXO INSTITUCIONAL DE RWA", 'font': {'color': '#cbd5e1', 'size': 14}},
        number = {'font': {'color': '#10b981'}, 'suffix': "%"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.3)"},
                {'range': [40, 65], 'color': "rgba(245, 158, 11, 0.3)"},
                {'range': [65, 100], 'color': "rgba(16, 185, 129, 0.3)"}
            ],
            'threshold': {'line': {'color': "#10b981", 'width': 4}, 'thickness': 0.75, 'value': 86}
        }
    ))
    fig_gauge.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> RADAR GLOBAL (AO VIVO)</h2>", unsafe_allow_html=True)
    st.markdown('<div class="news-hub-compact">', unsafe_allow_html=True)
    
    global_news = fetch_global_radar()
    
    # Lógica de Paginação (Rotatividade Autónoma 5 em 5 notícias para poupar espaço)
    items_per_page = 5
    if len(global_news) > 0:
        total_pages = max(1, len(global_news) // items_per_page)
        current_page = st.session_state.news_page % total_pages
        start_idx = current_page * items_per_page
        
        st.markdown(f"<div style='text-align: right; color: #8b5cf6; font-size: 0.8rem; margin-bottom: 10px; font-weight: bold;'>[ PÁGINA DE INTERCEÇÃO {current_page+1}/{total_pages} ]</div>", unsafe_allow_html=True)
        
        for item in global_news[start_idx : start_idx + items_per_page]:
            st.markdown(f"""
            <div class="news-item">
                <a href="{item['link']}" target="_blank">{item['title']}</a>
                <div class="news-meta">{item['source']} | {item['date']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("A aguardar sinal do radar...")
        
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. SECÇÃO DE INTELIGÊNCIA AVANÇADA E MACROECONOMIA
# ==============================================================================
col_macro, col_sim = st.columns([1.5, 1])

with col_macro:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> CALENDÁRIO MACROECONÓMICO</h2>", unsafe_allow_html=True)
    st.write("A liquidez não surge do vazio. Ela move-se com base em reuniões do FED, relatórios de inflação e prazos tecnológicos.")
    
    st.markdown('<div style="background: rgba(15,23,42,0.5); padding: 20px; border-radius: 8px; border: 1px solid #1e293b;">', unsafe_allow_html=True)
    for event in MACRO_EVENTS:
        impact_color = "#ef4444" if event["impact"] in ["Extrema", "Absoluta"] else "#fbbf24"
        st.markdown(f"""
        <div class="event-row">
            <div class="event-date">{event['date']}</div>
            <div class="event-desc">
                <strong style="color: #f8fafc; font-size: 1.1rem;">{event['event']}</strong> 
                <span style="color: {impact_color}; font-size: 0.8rem; border: 1px solid {impact_color}; padding: 2px 6px; border-radius: 4px; margin-left: 10px;">Impacto: {event['impact']}</span>
                <br>
                <span style="color: #94a3b8; font-size: 0.95rem;">{event['desc']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_sim:
    st.markdown("<h2><span style='color:#38bdf8;'>■</span> MOTOR DE PROJEÇÃO DCA 2030</h2>", unsafe_allow_html=True)
    st.write("Cálculo matemático da acumulação base de **360€ mensais** até à meta temporal de 2030.")
    
    # Simulador estático matemático para manter a frieza institucional
    monthly_investment = 360
    total_months = st.session_state.dca_months
    total_capital_invested = monthly_investment * total_months
    
    # Projeção hiper-conservadora de crescimento institucional (2.5x médio do portefólio até 2030)
    conservative_multiplier = 2.5
    projected_value = total_capital_invested * conservative_multiplier
    
    st.markdown(f"""
    <div class="simulator-box">
        <div class="sim-label">Meses até Alvo (Dez 2030)</div>
        <div style="font-size: 2rem; color: #f8fafc; font-weight: bold; margin-bottom: 20px;">{total_months} MESES</div>
        
        <div class="sim-label">Capital Fiduciário Injetado (Acumulado)</div>
        <div style="font-size: 2rem; color: #94a3b8; font-weight: bold; margin-bottom: 20px;">€ {total_capital_invested:,.0f}</div>
        
        <div class="sim-label">Valorização de Base Projetada (Conservadora 2.5x)</div>
        <div class="sim-number">€ {projected_value:,.0f}</div>
        
        <p style="color: #64748b; font-size: 0.8rem; margin-top: 15px;">*A projeção assume uma compra cega (DCA Implacável) no dia 29 de cada mês, isolando completamente o ruído da volatilidade diária. A acumulação ignora emoções.*</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. THINK TANK EDUCACIONAL MASSIVO (EXPLICAÇÃO PROFUNDA PARA O PÚBLICO)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> O MANIFESTO: EDUCAÇÃO INSTITUCIONAL E RWA</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="edu-box">
    <div class="edu-title">I. O Colapso do Dinheiro de Papel e a Fuga para a Escassez</div>
    <p>O cidadão comum assume que o Euro ou o Dólar são unidades de medida estáveis e perpétuas. A matemática corporativa e a história económica provam exatamente o contrário. Desde a rutura do padrão-ouro em 1971 pelo Presidente Nixon, o dinheiro fiduciário é criado com base em dívida. Quando os bancos centrais (como o FED ou o BCE) imprimem triliões de unidades para cobrir défices governamentais ou resgatar bancos falidos, não estão a criar riqueza real; estão apenas a diluir o poder de compra da moeda que o trabalhador retém arduamente na sua conta bancária.</p>
    <p>A <span class="highlight-blue">JTM Capital</span> reconhece este fenómeno monetário como um "imposto oculto" e altamente regressivo. Para proteger a energia económica da desvalorização garantida, o capital institucional iniciou uma migração histórica e massiva para a <span class="highlight-green">Camada 0 da soberania financeira: O Bitcoin</span>. Sendo um protocolo matemático rigidamente blindado por criptografia e limitado a exatamente 21 milhões de unidades, o Bitcoin é inconfiscável, inalterável e imune à pressão política dos governos. É o escudo impenetrável da nossa Base.</p>
</div>

<div class="edu-box">
    <div class="edu-title">II. Tokenização de Ativos (RWA): O Mundo Físico na Blockchain</div>
    <p>Se o Bitcoin assumiu o papel de novo ouro digital, redes globais como o <span class="highlight-blue">Ethereum</span> são a nova bolsa de valores, notários e tribunais combinados numa só máquina global. A tokenização de <i>Real World Assets</i> (RWA) é, simplesmente, a representação digital de ativos físicos do mundo real em redes blockchain seguras.</p>
    <p><b>O Exemplo da Imobiliária Institucional:</b> Um edifício de escritórios avaliado em 100 milhões de euros no Dubai é tradicionalmente um ativo altamente ilíquido (difícil e demorado de vender rapidamente). Através da tecnologia RWA, a propriedade legal e os direitos aos rendimentos desse edifício são programados num "Smart Contract" no Ethereum e divididos em, por exemplo, 100 milhões de tokens de 1 euro cada. Qualquer investidor asiático, europeu ou americano pode comprar 500€ desse edifício instantaneamente num domingo à noite a partir do seu telemóvel, recebendo a sua fração das rendas automaticamente na sua carteira digital ao fim do mês. A gigante <b>BlackRock</b> já iniciou a digitalização total de obrigações do tesouro americano através do seu fundo BUIDL, pavimentando a autoestrada para que todos os outros fundos mundiais a sigam.</p>
</div>

<div class="edu-box">
    <div class="edu-title">III. Norma ISO 20022 e a Morte Anunciada do SWIFT</div>
    <p>O sistema SWIFT, que atualmente gere as transferências transfronteiriças de dinheiro entre países, funciona essencialmente como um serviço de correio da década de 70. Uma transferência de capital de uma empresa em Lisboa para um fornecedor em Tóquio pode demorar dias, falhar sem motivo aparente, e passar por múltiplos bancos correspondentes, com cada um a retirar uma comissão pesada.</p>
    <p>O mundo financeiro está a ser forçado regulatoriamente a adotar a <span class="highlight-blue">ISO 20022</span>, uma linguagem comum, ultra-rica em dados e em formato XML para mensagens financeiras eletrónicas. O problema massivo que os bancos enfrentam? Os seus servidores legados de COBOL não suportam o processamento deste volume colossal de dados em tempo real. A solução adotada pela banca de topo? Redes criptográficas institucionais de alta velocidade como a <span class="highlight-green">Ripple (XRP)</span> e a <span class="highlight-green">Stellar (XLM)</span>. Estas redes foram desenhadas de raiz, há uma década, especificamente para atuar como pontes. Um banco central europeu pode converter Euros em XRP na origem, enviá-lo para o Japão em 3 segundos reais, e na fração de segundo em que chega ao destino, ser convertido em Ienes e creditado na conta do fornecedor. Zero fricção, zero dias de espera, auditoria matemática total. A tese da JTM Capital baseia-se em acumular antecipadamente a infraestrutura obrigatória (XRP, XLM, QNT) que os bancos serão forçados a comprar para a sua própria sobrevivência tecnológica.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. PROTOCOLO DE SOBERANIA E SEGURANÇA MÁXIMA (TREZOR DEEP DIVE)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> O PROTOCOLO DE SOBERANIA (COLD STORAGE)</h2>", unsafe_allow_html=True)

col_sec1, col_sec2 = st.columns([1, 1])

with col_sec1:
    st.markdown("""
    <div style="background-color: #0b1120; border: 1px solid #1e293b; padding: 30px; border-radius: 8px; height: 100%;">
        <h3 style="color: #fbbf24; margin-bottom: 15px;">A Regra de Ouro: "Not Your Keys, Not Your Coins"</h3>
        <p>A ruína dos investidores de retalho não é a queda dos preços; é o roubo e a falência de entidades centralizadas (corretoras como FTX, Celsius, BlockFi). Quando compra Bitcoin ou Ethereum numa plataforma digital e os deixa lá, <b>o dinheiro não é seu</b>. É um número no ecrã e uma promessa de pagamento (IOU).</p>
        <p>A Soberania Financeira Absoluta só é atingida quando o ativo é removido do sistema da corretora e transferido para a sua própria custódia. O protocolo da JTM Capital exige que a injeção mensal de 360€ seja extraída para a <b>Hardware Wallet Trezor</b> até 24h após a compra.</p>
    </div>
    """, unsafe_allow_html=True)

with col_sec2:
    st.markdown("""
    <div style="background-color: #0b1120; border: 1px solid #1e293b; border-left: 4px solid #ef4444; padding: 30px; border-radius: 8px; height: 100%;">
        <h3 style="color: #ef4444; margin-bottom: 15px;">A Arquitetura da Hardware Wallet (Trezor)</h3>
        <ul style="color: #cbd5e1; font-size: 1.05rem;">
            <li style="margin-bottom: 10px;"><b>Isolamento Físico (Air-gapped):</b> A Trezor gera a sua frase-semente (12 ou 24 palavras) offline. As suas chaves privadas nunca tocam num computador ligado à internet, tornando-as imunes a hackers e malware.</li>
            <li style="margin-bottom: 10px;"><b>Confirmação Manual Obrigatória:</b> Nenhuma transação ou Smart Contract pode drenar a sua conta sem que você prima fisicamente o botão de confirmação no dispositivo de plástico.</li>
            <li style="margin-bottom: 10px;"><b>Código Open-Source:</b> Ao contrário dos bancos, o código que corre na sua Trezor é aberto. Milhares dos melhores engenheiros criptográficos do mundo auditam-no diariamente à procura de falhas, garantindo a sua integridade absoluta.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. DOSSIÊS TÁTICOS (GERAÇÃO AUTOMÁTICA VIA DICIONÁRIO DE DADOS)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> DOSSIÊS DE INFRAESTRUTURA (PELOTÃO JTM)</h2>", unsafe_allow_html=True)
st.write("Análise de inteligência, parceiros institucionais verificados, prós, contras e fluxo de notícias filtrado ativamente pelo radar.")

tabs_objects = st.tabs([f"{symbol}" for symbol in ASSET_DOSSIER.keys()])

for i, symbol in enumerate(ASSET_DOSSIER.keys()):
    with tabs_objects[i]:
        asset_data = ASSET_DOSSIER[symbol]
        c_left, c_right = st.columns([1.5, 1])
        
        with c_left:
            st.markdown(f"### Função Tática: {asset_data['role']}")
            st.write(asset_data['thesis'])
            st.markdown(f"<div style='margin-top: 15px; padding: 10px; background: rgba(56, 189, 248, 0.1); border-left: 3px solid #38bdf8; border-radius: 4px;'><strong style='color:#38bdf8;'>🔗 Validação Institucional (Parceiros):</strong> <span style='color:#cbd5e1;'>{asset_data['partners']}</span></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <table class="tactic-table">
                <tr>
                    <th style="border-left: 4px solid #10b981;">🟢 MATRIZ POSITIVA (PRÓS)</th>
                    <th style="border-left: 4px solid #ef4444;">🔴 MATRIZ NEGATIVA (CONTRAS)</th>
                </tr>
                <tr>
                    <td><ul>""" + "".join([f"<li style='margin-bottom:8px;'>{p}</li>" for p in asset_data['pros']]) + """</ul></td>
                    <td><ul>""" + "".join([f"<li style='margin-bottom:8px;'>{c}</li>" for c in asset_data['cons']]) + """</ul></td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
            
        with c_right:
            st.markdown(f"### 📡 Interceções de Radar ({asset_data['name']})")
            asset_news = fetch_asset_specific_news(asset_data['keyword'])
            
            if len(asset_news) > 0:
                for item in asset_news:
                    st.markdown(f"""
                    <div style="background: rgba(15,23,42,0.8); padding: 15px; margin-bottom: 12px; border-radius: 6px; border-left: 2px solid #38bdf8; font-size: 0.95rem; transition: background 0.3s;">
                        <a href="{item['link']}" target="_blank" style="color: #f8fafc; text-decoration: none; font-weight: bold;">{item['title']}</a><br>
                        <span style="color: #64748b; font-size: 0.8rem; text-transform: uppercase;">{item['date']} | {item['source']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"O sistema de escuta não detetou manchetes primárias recentes contendo a assinatura digital '{asset_data['keyword']}'. Aguardando novas interceções no próximo ciclo.")

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO INSTITUCIONAL EXPANDIDO (SOBERANIA LINGUÍSTICA)
# ==============================================================================
st.markdown("<h2><span style='color:#38bdf8;'>■</span> GLOSSÁRIO DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
c_glos1, c_glos2 = st.columns(2)

with c_glos1:
    st.markdown("""
    * <span class="highlight-blue">DCA (Dollar Cost Averaging):</span> A técnica militar de investimento. Consiste em comprar o ativo numa janela fixa (dia 29), eliminando as emoções da equação.
    * <span class="highlight-blue">Hardware Wallet:</span> Um cofre físico que guarda as chaves de acesso offline (ex: Trezor). A barreira intransponível contra o colapso de corretoras.
    * <span class="highlight-blue">Fiat / Fiduciário:</span> Moedas decretadas por governos (Euro, Dólar) geradas por emissão de dívida. Sofrem diluição perpétua (inflação).
    * <span class="highlight-blue">Halving:</span> Evento programado matematicamente no código do Bitcoin que reduz para metade a criação de novas moedas a cada 4 anos, gerando um choque de oferta sem precedentes.
    * <span class="highlight-blue">Liquidity Pool (LP):</span> Contratos inteligentes que armazenam grandes quantidades de capital para permitir negociações descentralizadas sem necessidade de um intermediário humano (Livro de Ordens).
    """, unsafe_allow_html=True)

with c_glos2:
    st.markdown("""
    * <span class="highlight-blue">Smart Contracts:</span> Código auto-executável na blockchain que impõe acordos matemáticos de forma cega, imparcial e sem necessidade de confiança entre as partes. Eliminam a burocracia judicial.
    * <span class="highlight-blue">CBDC (Central Bank Digital Currency):</span> Moedas digitais emitidas pelo Estado. São a antítese do Bitcoin: são centralizadas, censuráveis e programáveis para expirar ou limitar o que o cidadão pode comprar.
    * <span class="highlight-blue">DePIN (Decentralized Physical Infra):</span> O uso de tokens para incentivar cidadãos comuns a construírem redes de utilidade mundial (antenas de wi-fi, partilha de GPU para IA, mapeamento global de estradas).
    * <span class="highlight-blue">Self-Custody (Auto-custódia):</span> A assunção de responsabilidade total pelo próprio dinheiro. O indivíduo torna-se no seu próprio banco. Não há números de apoio ao cliente, mas também não há confisco governamental.
    * <span class="highlight-blue">Oráculo (Blockchain Oracle):</span> Entidades de software (como a Chainlink) que têm permissão de confiança para ler o mundo exterior e fornecer esses dados para dentro da blockchain de forma imutável.
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 13. RODAPÉ, CARIMBO DE DATA E MOTOR AUTÓNOMO (RERUN)
# ==============================================================================
st.markdown("""
<div style="text-align: center; color: #64748b; font-family: 'Courier New', monospace; padding: 30px; border-top: 1px solid #1e293b;">
    <strong style="font-size: 1.2rem; color: #f8fafc;">JTM CAPITAL RESEARCH © 2026</strong><br><br>
    NÓ ESTRATÉGICO DE PORTUGAL | INFRAESTRUTURA DE ACUMULAÇÃO DE ATIVOS RWA<br>
    <em style="color: #38bdf8;">"A soberania financeira exige a substituição do intermediário humano por matemática inquebrável."</em><br><br>
    <span style="font-size: 0.8rem;">SISTEMA PROTEGIDO POR CRIPTOGRAFIA DE CURVA ELÍPTICA. ACESSO CONDICIONADO.</span>
</div>
""", unsafe_allow_html=True)

# Lógica do Loop de Sincronização (Avanço Automático da Página de Notícias a cada 30 segundos)
if auto_update:
    st.session_state.news_page += 1
    time.sleep(30)
    st.rerun()
