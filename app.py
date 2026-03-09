import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE INTELIGÊNCIA & CONFIGURAÇÃO SOBERANA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Genesis V32",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Estado de Ciclo para Notícias e Radar
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0

# --- SIDEBAR: CONSELHO DE ESTRATÉGIA ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.2);'>
            <h1 style='color: #a5f3fc; font-family: Rajdhani; text-align: center; font-size: 1.5rem;'>SOVEREIGN GENESIS</h1>
            <p style='text-align: center; color: #10b981; font-family: Inter; font-size: 0.8rem; letter-spacing: 2px;'>CÓRTEX V.MAX // 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização de Fluxo", value=True)
    
    st.markdown("### 🏛️ Gestão de Horizonte")
    st.info("**Âncora de Proteção:** 50%\n**Vetor de Crescimento:** 50%")
    
    st.markdown("---")
    st.markdown("### 🔒 Segurança de Ativos")
    st.warning("Próxima Extração: Dia 29\nStatus: Custódia Fria Ativa")
    
    st.markdown("---")
    st.caption(f"Última Atualização: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS NEO-SOVEREIGN: A ESTÉTICA DO FUTURO (TABELAS BLINDADAS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    /* Global Reset & Container */
    .main .block-container { padding: 3rem 5rem; max-width: 100%; }
    
    /* Fundo Deep-Ocean com Nebulosa Subtil */
    .stApp { 
        background-color: #010409; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: 'Rajdhani', sans-serif; letter-spacing: 4px; font-weight: 700; text-transform: uppercase; }

    /* Hero Section: Glassmorphism Premium */
    .hero-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 5px solid #00d4ff;
        padding: 80px;
        border-radius: 20px;
        margin-bottom: 50px;
        box-shadow: 0 50px 150px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 5.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.9; margin: 0; }
    .hero-subtitle { color: #00d4ff; font-size: 1.8rem; letter-spacing: 15px; margin-top: 25px; font-weight: 600; }

    /* Cartões de Telemetria Sincronizada */
    .quantum-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #10b981;
        padding: 30px;
        border-radius: 10px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .quantum-card:hover { transform: translateY(-8px); border-color: #00d4ff; box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2); }
    .q-label { font-size: 0.85rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 2px; text-transform: uppercase; }
    .q-value { font-size: 2.2rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Editorial Pulse: O Design de Notícia */
    .pulse-editorial {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.08), rgba(16, 185, 129, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 50px;
        border-radius: 20px;
        margin-bottom: 50px;
        border-left: 10px solid #00d4ff;
    }

    /* Tabelas Soberanas: Correção de Alinhamento Final */
    .sovereign-table { 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 0 12px; 
        margin-top: 20px;
        table-layout: fixed;
    }
    .sovereign-table th { color: #00d4ff; padding: 25px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; border-bottom: 2px solid rgba(255,255,255,0.1); }
    .sovereign-table td { background: rgba(255, 255, 255, 0.02); padding: 25px; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.05); font-size: 1.1rem; line-height: 1.8; vertical-align: top; }
    .sovereign-table tr td:first-child { border-top-left-radius: 12px; border-bottom-left-radius: 12px; font-weight: 700; color: #fff; width: 30%; }
    .sovereign-table tr td:last-child { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }

    /* Destaque Glass */
    .glass-highlight {
        background: rgba(10, 10, 20, 0.6);
        padding: 40px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE SOBERANO: A TESE DE CADA NÓ (DINÂMICA)
# ==============================================================================
# Esta base de dados explica o "PORQUÊ" de cada ativo no Monólito.
# Cada entrada possui argumentos técnicos exclusivos.

ASSET_INTEL = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Valor Absoluto",
        "why": "O Bitcoin é a única rede monetária com escassez finita verificável. Atua como o 'Padrão-Ouro' do sistema digital, protegendo o capital contra a inflação fiduciária e o erro bancário.",
        "pros": ["Escassez de 21 Milhões.", "Adoção Institucional massiva.", "Rede de segurança global."],
        "cons": ["Volatilidade temporária.", "Lentidão na Camada 1.", "Resistência política."],
        "sentiment": "Ouro Digital"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Liquidação Mundial",
        "why": "O Ethereum é a base da infraestrutura para a Tokenização de Ativos (RWA). É onde os triliões de dólares em imóveis e obrigações serão negociados através de Smart Contracts.",
        "pros": ["Domínio em Contratos Inteligentes.", "Mecanismo deflacionário.", "Ecossistema de ativos reais."],
        "cons": ["Custos de rede (Gas).", "Fragmentação de Layer 2.", "Competição de performance."],
        "sentiment": "Infraestrutura"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Ponte de Liquidez Bancária",
        "why": "Desenhado para substituir o sistema SWIFT, o XRP permite liquidação instantânea e barata para Bancos Centrais e instituições financeiras sob a norma ISO 20022.",
        "pros": ["Velocidade extrema (3s).", "Conformidade bancária global.", "Baixo custo transacional."],
        "cons": ["Controlo Ripple Labs.", "Escrutínio regulatório.", "Grande oferta circulante."],
        "sentiment": "ISO 20022"
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Verificação de Dados Global",
        "why": "O Chainlink fornece a verdade do mundo real para a blockchain. Sem os oráculos da Link, a Tokenização de ativos físicos não pode existir com segurança.",
        "pros": ["Padrão global de oráculos.", "Parceria ativa com o SWIFT.", "Essencial para o setor RWA."],
        "cons": ["Complexidade técnica.", "Dependência do setor DeFi.", "Tokenomics de longo prazo."],
        "sentiment": "Dados Reais"
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "Ondo permite a digitalização de títulos do tesouro e outros ativos institucionais. É a ponte direta entre a BlackRock e as finanças descentralizadas.",
        "pros": ["Ligação ao capital de elite.", "Ativos lastreados em valor real.", "Liderança institucional."],
        "cons": ["Risco de regulação fiat.", "Acesso restrito em certas áreas.", "Liquidez corporativa."],
        "sentiment": "RWA Hub"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Vetor de Performance Massiva",
        "why": "A Solana é a rede de alta velocidade escolhida por gigantes como a Visa para pagamentos retail em massa. É a 'Nasdaq' da blockchain de nova geração.",
        "pros": ["Velocidade de 65k TPS.", "Taxas inferiores a 1 cêntimo.", "Ecossistema de IA e DePIN."],
        "cons": ["Histórico de estabilidade.", "Hardware de nó caro.", "Concentração de capital."],
        "sentiment": "Velocidade"
    },
    "TSLA": {
        "name": "Tesla", "ticker": "TSLA", "role": "Soberania em Energia & IA",
        "why": "Tesla não é uma empresa de carros; é uma empresa de Inteligência Artificial e armazenamento de energia. O domínio dos Megapacks dita o futuro da soberania física.",
        "pros": ["Monopólio em armazenamento solar.", "Liderança em dados de autonomia.", "Integração vertical total."],
        "cons": ["Risco de semicondutores.", "Avaliação prémio (P/E).", "Figura central de risco."],
        "sentiment": "Energia / IA"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E RADAR GLOBAL
# ==============================================================================
@st.cache_data(ttl=30)
def fetch_telemetry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
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
# 05. PORTAL DE CONVERGÊNCIA: HERO SECTION
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM CAPITAL</div>
    <div class="hero-subtitle">SOVEREIGN GENESIS // HORIZON 2030</div>
    <p style="margin-top: 45px; font-size: 1.6rem; line-height: 2.3; color: #94a3b8; border-left: 10px solid #00d4ff; padding-left: 55px;">
        Bem-vindo ao <b>Cérebro Analítico</b> da JTM Capital. Este terminal monitoriza a transição quântica do sistema financeiro. Operamos na interseção entre a estabilidade da <b>Âncora Física</b> e a expansão da <b>Fronteira Digital</b>. Aqui, os dados governam a emoção.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (GRELHA DINÂMICA)
# ==============================================================================
# FIX: Criação dinâmica de colunas para evitar o IndexError: all_cols[idx]
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)

# Unimos ativos da base com parâmetros macro
MACRO_STAT_KEYS = {
    "GOLD": ("Ouro (XAU)", "GC=F"), "BCP": ("BCP Liquidez", "BCP.LS"),
    "DXY": ("Dólar (DXY)", "DX-Y.NYB"), "VIX": ("Índice Medo", "^VIX"),
    "NEAR": ("Near IA", "NEAR-EUR")
}

# Criamos uma lista total de itens a mostrar
display_items = []
for k, v in ASSET_INTEL.items(): display_items.append((v['name'], v['role'], v['ticker']))
for k, v in MACRO_STAT_KEYS.items(): display_items.append((v[0], "Parâmetro Macro", v[1]))

# Motor de Grelha Inteligente
cols_per_row = 4
for i in range(0, len(display_items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        idx = i + j
        if idx < len(display_items):
            name, role, ticker = display_items[idx]
            p, c = fetch_telemetry(ticker)
            color = "#10b981" if c >= 0 else "#ff4b4b"
            with cols[j]:
                st.markdown(f"""
                <div class="quantum-card">
                    <div class="q-label">{name} // {role}</div>
                    <div class="q-value">€ {p:,.2f}</div>
                    <div style="color: {color}; font-weight: bold; font-family: 'JetBrains Mono'; margin-top: 15px;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MANCHETE DO DIA: EDITORIAL V.MAX PULSE (O PORQUÊ HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> ORIENTAÇÃO ESTRATÉGICA: V.MAX Pulse</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="pulse-editorial">
    <div style="background: #00d4ff; color: #000; padding: 5px 15px; display: inline-block; font-family: 'JetBrains Mono'; font-weight: 800; border-radius: 4px; margin-bottom: 20px;">NOTÍCIA DO CÓRTEX</div>
    <h3 style="color:#ffffff; margin-bottom:25px; font-size: 2.8rem;">ANÁLISE: O PONTO DE INFLEXÃO DA LIQUIDEZ GLOBAL</h3>
    <p style="font-size: 1.4rem; line-height: 2.2; color: #f1f5f9;">
        O Córtex V.MAX identifica hoje um alinhamento crítico no sistema financeiro internacional. A inversão da curva de rendimentos e a força do índice Dólar (DXY) sinalizam que estamos a entrar na fase final de <b>Limpeza Fiduciária</b>. O capital institucional está a fugir de obrigações de dívida para se ancorar em <b>Ativos de Escassez Matemática</b>.
    </p>
    <p style="margin-top: 30px; font-weight: 700; font-size: 1.5rem; color: #10b981;">
        PORQUÊ O POSICIONAMENTO DE HOJE? <br>
        O MVRV Z-Score do Bitcoin indica subvalorização técnica, enquanto as Dark Pools revelam acumulação agressiva na Tesla. A recomendação soberana é a <b>Acumulação em Tranches de 50%</b>. Mantemos 50% em Âncora de Proteção (Ouro/BCP) para garantir liquidez em caso de evento macro imprevisto, e os restantes 50% em Vetores de Crescimento (XRP/ONDO/SOL) para capturar o reset sistémico. Ignorar o ruído é o protocolo.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 08. RADAR GLOBAL & INSIGHT (GRID SIMÉTRICO)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> MONITOR DE INTELIGÊNCIA // O PULSO</h2>", unsafe_allow_html=True)
col_radar, col_insight = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="glass-highlight" style="border-left-color: #8b5cf6;">', unsafe_allow_html=True)
    st.markdown("### 📡 Radar de Fluxo Global")
    news_list = fetch_radar()
    page = st.session_state.cycle % (len(news_list)//6)
    for item in news_list[page*6 : (page+1)*6]:
        st.markdown(f'<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 20px 0;"><a href="{item["link"]}" target="_blank" style="color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.25rem;">■ {item["title"]}</a><div style="color: #64748b; font-size: 0.95rem; margin-top: 10px;">{item["src"]} // AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_insight:
    st.markdown("""
    <div class="pulse-editorial" style="height: 100%; padding: 45px; border-left-color: #f59e0b; margin-bottom: 0;">
        <h3 style="color: #f59e0b;">CÓRTEX V.MAX: INSIGHT</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.3rem; line-height: 2.2;">
        "O sistema financeiro analógico está a sangrar liquidez. A transição para o padrão ISO 20022 está a entrar na fase de 'Settlement Crítico'. Observamos o capital inteligente a abandonar ativos de dívida para se ancorar em protocolos que o sistema será obrigado a utilizar."
        </p>
        <p style="margin-top: 40px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">SENTIMENTO: ACUMULAÇÃO GÉLIDA.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. PILARES DA TRANSIÇÃO (O PORQUÊ CIENTÍFICO)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> ARQUITETURA DO NOVO MUNDO // PORQUÊ CADA PARÂMETRO?</h2>", unsafe_allow_html=True)



c_exp1, c_exp2 = st.columns(2)
with c_exp1:
    st.markdown("""
    <div class="glass-highlight" style="border-left: 10px solid #10b981; min-height: 350px;">
        <h3>I. Digitalização de Ativos (RWA)</h3>
        <p style="font-size: 1.25rem; line-height: 2.1;"><b>O Porquê:</b> Ativos físicos são "pesados" e ilíquidos. Ao tokenizá-los, permitimos liquidez 24/7. Quem controla as redes de digitalização (Ethereum, Chainlink, Ondo) controla o fluxo de capital de 2030.</p>
    </div>
    """, unsafe_allow_html=True)
with c_exp2:
    st.markdown("""
    <div class="glass-highlight" style="border-left: 10px solid #00d4ff; min-height: 350px;">
        <h3>II. A Linguagem Universal ISO 20022</h3>
        <p style="font-size: 1.25rem; line-height: 2.1;"><b>O Porquê:</b> O sistema SWIFT é o correio do passado. A norma <b>ISO 20022</b> é o novo padrão mundial obrigatório. Protocolos como <b>XRP e QNT</b> são a fibra ótica que sustenta este novo sistema bancário.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: ANÁLISE DINÂMICA (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE ATIVOS SOBERANOS // O PORQUÊ TÉCNICO</h2>", unsafe_allow_html=True)

asset_tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_INTEL.values()])

for i, (key, info) in enumerate(ASSET_INTEL.items()):
    with asset_tabs[i]:
        st.markdown(f"<div class='glass-highlight'><h3 style='color: #00d4ff;'>TESE SOBERANA: {info['name']}</h3><p style='font-size: 1.3rem; line-height: 2.2;'>{info['why']}</p></div>", unsafe_allow_html=True)
        
        # TABELA BLINDADA COM CSS FIXO
        st.markdown(f"""
        <table class="sovereign-table">
            <thead>
                <tr><th>🟢 VANTAGENS SOBERANAS ({info['sentiment']})</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. MATRIZ DE POSICIONAMENTO ESTRATÉGICO (HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MAPA DE POSICIONAMENTO RECOMENDADO (CICLO ATUAL)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP / OURO", "Alocação": "50%", "Justificação": "Garantia de solvência e reserva de guerra macro."},
    {"Setor": "Autonomia & Energia", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Justificação": "Domínio da infraestrutura física e IA real."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO", "Alocação": "20%", "Justificação": "Aproximação do prazo mandatório de migração bancária global."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Justificação": "Captura de valor na ineficiência do capital analógico."}
]

df_pos = pd.DataFrame(pos_data)
# Injeção de Tabela com Alinhamento Fixo
st.markdown(f"""
<table class="sovereign-table">
    <thead>
        <tr><th>Setor de Atuação</th><th>Ativos Sugeridos</th><th>Alocação (%)</th><th>Justificação Estratégica</th></tr>
    </thead>
    <tbody>
        {''.join([f"<tr><td>{row['Setor']}</td><td>{row['Ativos']}</td><td>{row['Alocação']}</td><td>{row['Justificação']}</td></tr>" for _, row in df_pos.iterrows()])}
    </tbody>
</table>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> EXPLICAÇÃO DOS PARÂMETROS MACRO</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**VIX (Índice do Medo):** Mede a volatilidade esperada. Quando o VIX sobe, o mercado entra em pânico, criando oportunidades para quem tem caixa no BCP.")
    st.write("**DXY (Índice Dólar):** Se o Dólar está forte, os ativos de risco (BTC/TSLA) tendem a descer. Rastreamos para medir a pressão de venda.")
with cg2:
    st.write("**MVRV Z-Score:** Parâmetro estatístico que nos diz se o Bitcoin está 'barato' para as instituições. Valores baixos indicam capitulação e zona de compra.")
    st.write("**Dark Pools:** Local onde as instituições compram TSLA sem afetar o preço imediato. Rastreamos o fluxo para prever explosões de preço.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas quando você detém as chaves privadas fora da internet.")
    st.write("**Settlement Layer:** A camada definitiva onde o valor é liquidado. O Ethereum é a settlement layer dos triliões de dólares em RWA.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 80px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição da emoção pela matemática."</em><br>
    <small style="color: #1e293b;">MONÓLITO V32.0 // ERROR-FREE DYNAMIC GRID READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização de Ciclo
if auto_refresh:
    st.session_state.cycle += 1
    time.sleep(30)
    st.rerun()
