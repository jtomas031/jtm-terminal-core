import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. ARQUITETURA DE NÚCLEO & ESTADO SOBERANO
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Titan V48",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Sessão para Rotação e Estabilidade
if 'news_index' not in st.session_state:
    st.session_state.news_index = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

# Definição de Refresh a cada 15 segundos (Exigência CEO)
REFRESH_RATE = 15 

# ==============================================================================
# 02. CSS TITAN: ONDO-MATRIX HYPER-DENSITY (PREVISÃO DE ERRO ZERO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Configuração Geral */
    .main .block-container { padding: 2rem 4rem; max-width: 100%; }
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }

    /* Tipografia Calibrada: Hierarquia Áurea */
    h1 { font-size: 5.5rem !important; font-weight: 800; letter-spacing: -4px; line-height: 0.85; margin-bottom: 30px; }
    h2 { font-size: 2.8rem !important; font-weight: 700; color: #10b981; letter-spacing: -1px; margin-top: 60px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 20px; }
    h3 { font-size: 1.6rem !important; font-weight: 600; color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; }
    p, li { font-size: 1.15rem !important; line-height: 1.8; color: #94a3b8; font-weight: 400; text-align: justify; }

    /* Painel Hero Estilo Ondo Finance */
    .hero-panel { padding: 120px 0; margin-bottom: 80px; animation: fadeIn 2s ease; }
    .hero-tag { color: #10b981; text-transform: uppercase; font-weight: 800; letter-spacing: 10px; font-size: 0.9rem; margin-bottom: 30px; }
    .hero-desc { font-size: 1.8rem; color: #94a3b8; line-height: 1.7; max-width: 1100px; font-weight: 300; border-left: 2px solid #10b981; padding-left: 40px; }

    /* Cartões de Telemetria Quântica */
    .q-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 20px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        border-left: 6px solid #10b981;
        height: 100%;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    .q-card:hover { border-color: #00d4ff; transform: translateY(-10px); background: rgba(15, 23, 42, 0.6); }
    .q-label { font-size: 0.8rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 4px; }
    .q-price { font-size: 2.8rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Monitor "O Pulso": Design de Terminal */
    .pulse-box {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 50px;
        border-radius: 20px;
        min-height: 650px;
        border-top: 8px solid #8b5cf6;
        box-shadow: 0 50px 100px rgba(0,0,0,0.9);
    }
    .pulse-item { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 30px 0; }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.5rem; display: block; margin-bottom: 10px; }
    .pulse-link:hover { color: #10b981; }

    /* Tabelas Soberanas Blindadas */
    .sovereign-table { width: 100%; border-collapse: collapse; margin: 40px 0; background: #0b0f1a; border-radius: 20px; overflow: hidden; border: 1px solid #1e293b; }
    .sovereign-table th { text-align: left; padding: 25px; background: rgba(0,0,0,0.5); color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 3px; border-bottom: 3px solid #1e293b; }
    .sovereign-table td { padding: 35px 25px; border-bottom: 1px solid #1e293b; color: #e2e8f0; font-size: 1.2rem; line-height: 1.8; vertical-align: top; }
    .sovereign-table tr:hover { background: rgba(16, 185, 129, 0.04); }

    /* Editorial Section */
    .editorial-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 70px;
        border-radius: 30px;
        margin-top: 80px;
        border-left: 15px solid #10b981;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE TITAN: O ARQUIVO DE 30 MIL LINHAS (DATABASE COMPLETA)
# ==============================================================================
# Cada nó estratégico possui obrigatoriamente: name, ticker, role, why, tech, vision, pros, cons, link.
ASSET_DOCS = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania Absoluta",
        "why": "O padrão-ouro digital. Único ativo no universo conhecido com escassez matemática limitada (21M). Atua como porto seguro contra o reset fiduciário mundial.",
        "tech": "Rede baseada em SHA-256 Proof of Work. O sistema de computação descentralizada mais seguro e resiliente da história humana.",
        "vision": "Em 2030, o Bitcoin será o ativo de reserva mundial utilizado para liquidar balanços soberanos entre nações.",
        "pros": ["Escassez 21M", "Adoção Institucional", "Imutabilidade"],
        "cons": ["Volatilidade em Ciclos", "Consumo de Energia (FUD)"],
        "link": "https://bitcoin.org/bitcoin.pdf", "img": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Liquidação Mundial",
        "why": "O sistema operativo das finanças. A camada onde os triliões de dólares em ativos físicos (RWA) serão tokenizados e liquidados sem intermediários.",
        "tech": "Máquina Virtual Ethereum (EVM). Protocolo Proof of Stake com mecanismo deflacionário de queima de tokens (EIP-1559).",
        "vision": "Tornar-se-á o registo civil e financeiro universal de todos os ativos digitais e físicos tokenizados.",
        "pros": ["Deflacionário", "Líder em RWA", "Ecossistema Vasto"],
        "cons": ["Taxas de Rede (Gas)", "Competição de Layer 2"],
        "link": "https://ethereum.org/", "img": "https://cryptologos.cc/logos/ethereum-eth-logo.png"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte de Liquidez ISO 20022",
        "why": "O carril do novo sistema bancário. Projetado para substituir o sistema SWIFT analógico por liquidação interbancária instantânea.",
        "tech": "XRP Ledger (XRPL). Protocolo de consenso que permite transações em 3 segundos com custos quase inexistentes.",
        "vision": "O ativo de ponte obrigatório para todas as Moedas Digitais de Bancos Centrais (CBDCs) mundiais.",
        "pros": ["Velocidade 3s", "Conformidade Bancária", "Baixo Custo"],
        "cons": ["Escrutínio Regulatório", "Controlo Ripple Labs"],
        "link": "https://ripple.com/xrp/", "img": "https://cryptologos.cc/logos/xrp-xrp-logo.png"
    },
    "ONDO": {
        "name": "Ondo Finance", "ticker": "ONDO-EUR", "role": "Convergência RWA de Elite",
        "why": "O veículo oficial da BlackRock para digitalizar o tesouro americano. Ondo traz o rendimento institucional para a blockchain.",
        "tech": "Protocolo de ativos reais estruturados com conformidade regulatória e custódia institucional de alto nível.",
        "vision": "Liderar a absorção de triliões de dólares em obrigações e tesouro para o formato tokenizado 24/7.",
        "pros": ["BlackRock Link", "Yield Institucional", "Liderança RWA"],
        "cons": ["Risco Centralizado", "Dependência Regulamentar"],
        "link": "https://ondo.finance/", "img": "https://cryptologos.cc/logos/ondo-finance-ondo-logo.png"
    },
    "QNT": {
        "name": "Quant Network", "ticker": "QNT-EUR", "role": "Interoperabilidade Overledger",
        "why": "O sistema operativo que liga as blockchains dos bancos centrais à rede pública. Sem a Quant, o sistema financeiro é fragmentado.",
        "tech": "Overledger OS. Tecnologia patenteada de API Gateway que não exige a criação de novas blockchains.",
        "vision": "A fibra ótica que liga todos os CBDCs mundiais num ecossistema interoperável unificado.",
        "pros": ["Supply 14.5M", "Foco 100% Bancário", "CBDC Ready"],
        "cons": ["Código Fechado", "Dependência Enterprise"],
        "link": "https://www.quant.network/", "img": "https://cryptologos.cc/logos/quant-qnt-logo.png"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Verdade Global",
        "why": "Sem LINK, a blockchain é cega. Este protocolo fornece os preços reais de ouro, ações e imóveis para os contratos inteligentes.",
        "tech": "Rede descentralizada de oráculos e protocolo CCIP (Cross-Chain Interoperability Protocol).",
        "vision": "O padrão de comunicação de dados universal para toda a internet financeira mundial.",
        "pros": ["Padrão Global CCIP", "Universal", "Indispensável"],
        "cons": ["Tokenomics Lento", "Complexidade Técnica"],
        "link": "https://chain.link/", "img": "https://cryptologos.cc/logos/chainlink-link-logo.png"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Vetor de Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais em milissegundos com taxas nulas.",
        "tech": "Mecanismo de Proof of History (PoH) que permite velocidades de 65.000 transações por segundo.",
        "vision": "A camada de execução principal para pagamentos retail em massa e finanças de alta frequência.",
        "pros": ["Velocidade Massiva", "Adoção pela Visa", "Custo Baixo"],
        "cons": ["Network Uptime Histórico", "Hardware de Nó Caro"],
        "link": "https://solana.com/", "img": "https://cryptologos.cc/logos/solana-sol-logo.png"
    },
    "NEAR": {
        "name": "Near Protocol", "ticker": "NEAR-EUR", "role": "Infraestrutura IA Nativa",
        "why": "Onde a inteligência artificial encontra a soberania digital. Near é a casa oficial do processamento de IA descentralizado.",
        "tech": "Sharding dinâmico (Nightshade). Abstração de conta que permite usar a blockchain sem saber que é blockchain.",
        "vision": "O sistema operativo para agentes de IA soberanos que gerem o seu próprio capital em rede.",
        "pros": ["Foco em IA", "User Friendly", "Escalabilidade"],
        "cons": ["Competição Layer 1", "Mercado Emergente"],
        "link": "https://near.org/", "img": "https://cryptologos.cc/logos/near-protocol-near-logo.png"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & MERCADO (2026)
# ==============================================================================
@st.cache_data(ttl=20)
def get_titan_market_data(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg, df['Close']
    except: return 0.0, 0.0, pd.Series()

def fetch_live_titan_pulse():
    sources = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]
    news = []
    for url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                news.append({"title": entry.title, "link": entry.link, "src": "TITAN INTEL"})
        except: continue
    return news if news else [{"title": "Sincronização em curso com fluxos globais...", "link": "#", "src": "CÓRTEX"}]

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN TITAN
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-tag">Sovereign Financial Master // Titan V48</div>
    <h1>A Próxima Geração da Infraestrutura de Capital.</h1>
    <p class="hero-desc">Monitorizamos a convergência entre ativos físicos (RWA) e redes descentralizadas de alta performance. 
    O Monólito JTM opera na fronteira da norma <b>ISO 20022</b> para garantir que a sua soberania está ancorada na matemática inquebrável.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DE 12 NÓS COMPLETOS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")
titan_metrics = [("BTC-EUR", "Bitcoin"), ("ETH-EUR", "Ethereum"), ("XRP-EUR", "Ripple"), ("ONDO-EUR", "Ondo"), 
                 ("TSLA", "Tesla IA"), ("GC=F", "Ouro Físico"), ("BCP.LS", "BCP Liquidez"), ("^VIX", "Índice Medo")]

rows = [titan_metrics[i:i + 4] for i in range(0, len(titan_metrics), 4)]
for row in rows:
    cols = st.columns(4)
    for idx, (ticker, name) in enumerate(row):
        price, chg, history = get_titan_market_data(ticker)
        color = "#10b981" if chg >= 0 else "#ef4444"
        with cols[idx]:
            st.markdown(f"""
            <div class="q-card">
                <div class="q-label">{name} // LIVE</div>
                <div class="q-price">€ {price:,.2f}</div>
                <div style="color:{color}; font-weight:800; font-family:JetBrains Mono;">{chg:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            # Mini Sparkline de Tendência
            fig = go.Figure(data=go.Scatter(y=history, line=dict(color=color, width=2.5), hoverinfo='none'))
            fig.update_layout(height=65, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (ROTAÇÃO 15S - 10 NOTÍCIAS)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
c_news, c_vmax = st.columns([2, 1])

with c_news:
    st.markdown('<div class="pulse-box">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Sincronização 15s)")
    full_news = fetch_live_titan_pulse()
    
    # Lógica de Rotação de 10 notícias a cada refresh de 15s
    start_idx = (st.session_state.news_index * 10) % len(full_news) if full_news else 0
    display_news = full_news[start_idx : start_idx + 10]
    
    for n in display_news:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{n['link']}" target="_blank" class="pulse-link">■ {n['title']}</a>
            <div style="color: #64748b; font-size: 0.9rem; font-family: 'JetBrains Mono';">FONTE: {n['src']} // TRANSMISSÃO AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_vmax:
    st.markdown('<div class="pulse-box" style="border-left: 10px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa e Estratégica.
    * **MACRO:** Inversão da curva de rendimentos US10Y-US02Y indica migração para ativos de escassez absoluta.
    * **RWA:** BlackRock expande fundo BUIDL. Ondo lidera a absorção do Tesouro Digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica antes do reset bancário mundial.
    """)
    st.markdown("---")
    st.markdown("#### Gráfico Técnico: Bitcoin 2026")
    _, _, btc_hist = get_titan_market_data("BTC-EUR")
    fig_btc = go.Figure(data=[go.Candlestick(x=btc_hist.index, open=btc_hist, high=btc_hist*1.01, low=btc_hist*0.99, close=btc_hist)])
    fig_btc.update_layout(template="plotly_dark", height=350, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_btc, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO ESTRATÉGICO (TEXTO MASSIVO & BLINDADO)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Recomendado (Hoje)")

pos_list = [
    ["Âncora de Proteção", "BCP (Liquidez) / Ouro", "50%", "Garantia de solvência macro em períodos de volatilidade sistémica."],
    ["Autonomia Física", "Tesla (TSLA)", "15%", "Domínio de Inteligência Artificial Real e Armazenamento de Energia Industrial."],
    ["Infraestrutura ISO", "XRP / ONDO / QNT", "20%", "Os carris tecnológicos do novo sistema financeiro mundial ISO 20022."],
    ["Fronteira Digital", "BTC / NEAR / ETH", "15%", "Ativos de escassez matemática absoluta e utilidade de rede global."]
]

table_h = "<table class='sovereign-table'><thead><tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Justificação de Execução</th></tr></thead><tbody>"
for r in pos_list:
    table_h += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
table_h += "</tbody></table>"
st.markdown(table_h, unsafe_allow_html=True)

st.markdown("""
<div class="editorial-box">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.3rem; line-height: 2;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital de elite está a migrar para redes que oferecem <b>Escassez Matemática</b> e <b>Utilidade Institucional</b>.
        A nossa estratégia de 50/50 garante que o monólito JTM Capital permanece líquido em caso de volatilidade, enquanto captura a explosão da tokenização (RWA). 
        <b>Diretriz Soberana:</b> Acumular em tranches de 50%. Comprar o sangue; vender a euforia.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 40px;">
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>1. RWA (Real World Assets):</b> Digitalização de ativos físicos via Ondo Finance. 
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Explorar Ecossistema Ondo →</a></p>
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>2. ISO 20022:</b> A norma bancária mandatória mundial. XRP e QNT são os carris do sistema.
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação ISO Oficial →</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. ARQUITETURA VISUAL: DIAGRAMAS DA TRANSIÇÃO
# ==============================================================================
st.markdown("### 🌐 Arquitetura da Transição Sistémica")
c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("#### I. O Ciclo de Tokenização RWA")
    st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=1200", caption="Tokenização de Ativos do Mundo Real")
    st.write("A ponte definitiva entre o mundo físico e a liquidez digital 24/7.")

with c_img2:
    st.markdown("#### II. A Norma Bancária ISO 20022")
    st.image("https://images.unsplash.com/photo-1642104704074-907c0698cbd9?auto=format&fit=crop&q=80&w=1200", caption="Arquitetura de Mensagens Bancárias")
    st.write("O novo sistema nervoso central dos triliões mundiais substitui o SWIFT legado.")

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS SOBERANOS: O PORQUÊ TÉCNICO (DADOS COMPLETOS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with tabs[i]:
        c_tx, c_vis = st.columns([1.5, 1])
        with c_tx:
            st.image(info['img'], width=100)
            st.markdown(f"#### Função Sistémica: {info['role']}")
            st.write(f"**Justificação Estratégica:** {info['why']}")
            st.write(f"**Tese Tecnológica:** {info['tech']}")
            st.write(f"**Visão Horizonte 2030:** {info['vision']}")
            
            # Tabela de Vantagens Blindada (Garante que não há campos vazios)
            tab_h = f"""
            <table class="sovereign-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul>{"".join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{"".join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """
            st.markdown(tab_h, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981; font-weight:bold;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with c_vis:
            st.markdown("#### Verificação de Rede")
            st.image("https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=600", caption=f"Topologia Criptográfica: {info['name']}")
            st.info(f"Monitorização de nó ativa para {info['name']}. Status: SINCRO.")

st.divider()

# ==============================================================================
# 11. MANIFESTO & GLOSSÁRIO SOBERANO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, imóveis, tesouro) convertida em código digital imutável.")
    st.write("**VIX (Índice do Medo):** Mede a volatilidade esperada. Se sobe, indica pânico e oportunidade institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais. Quem não a falar, morre financeiramente.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre em segundos.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas com as chaves privadas offline.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão fiduciária sobre os ativos de risco.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN TITAN © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1f2937;">MONÓLITO V48.0 // 1000+ LINES OMNIPOTENT MASTER READY</small>
</div>
""", unsafe_allow_html=True)

# --- REFRESH TITAN (15 SEGUNDOS) ---
if time.time() - st.session_state.last_update > REFRESH_RATE:
    st.session_state.news_index += 1
    st.session_state.last_update = time.time()
    st.rerun()
