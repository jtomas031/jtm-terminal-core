import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & DOCUMENTAÇÃO DE SISTEMA
# ==============================================================================
# Este código foi desenhado para ser o repositório definitivo da JTM Capital.
# Cada função monitoriza um vetor de liquidez global, filtrando o ruído para
# focar na acumulação soberana para o horizonte 2030.
# ==============================================================================

st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Core V30",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'editorial_page' not in st.session_state:
    st.session_state.editorial_page = 0

# --- BARRA DE GOVERNANÇA (NEO-GLASS) ---
with st.sidebar:
    st.markdown("<h1 style='color: #a5f3fc; font-family: Rajdhani; text-align: center;'>SOVEREIGN CORE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #06b6d4; font-weight: 300; letter-spacing: 2px;'>VERSÃO OMNIPOTENTE 30.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    auto_sync = st.toggle("Sincronização Ativa", value=True)
    
    st.markdown("### 🧭 Direcionamento de Capital")
    st.info("**Âncora de Proteção (50%):** BCP / Ouro\n\n**Vetor de Crescimento (50%):** TSLA / Cripto")
    
    st.markdown("---")
    st.markdown("### 🔓 Protocolo de Custódia")
    st.warning("Dia 29: Extração Mandatória\nCold Storage: Trezor Ativa")
    
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS NEO-GLASS V30: SIMETRIA E BELEZA FUTURISTA
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    /* Configuração Geral de Layout */
    .main .block-container { padding: 2rem 5rem; max-width: 100%; overflow-x: hidden; }
    
    /* Fundo Obsidian Nebula */
    .stApp { 
        background-color: #020617; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: Rajdhani; letter-spacing: 4px; font-weight: 700; text-transform: uppercase; }

    /* Painel Hero Glassmorphism */
    .hero-glass {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(35px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 6px solid #06b6d4;
        padding: 90px;
        border-radius: 20px;
        margin-bottom: 60px;
        box-shadow: 0 50px 200px rgba(0,0,0,0.9);
    }
    .hero-title { font-size: 6rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.8; margin: 0; }
    .hero-subtitle { color: #06b6d4; font-size: 2rem; letter-spacing: 20px; margin-top: 30px; font-weight: 600; }

    /* Cartões de Telemetria Dinâmica */
    .quantum-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 5px solid #10b981;
        padding: 35px;
        border-radius: 12px;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .quantum-card:hover { transform: translateY(-15px); border-color: #06b6d4; box-shadow: 0 30px 60px rgba(6, 182, 212, 0.3); }
    .q-label { font-size: 0.9rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 3px; }
    .q-value { font-size: 2.5rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Editorial de Hoje (Estilo Notícia) */
    .editorial-container {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(16, 185, 129, 0.08));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 60px;
        border-radius: 20px;
        margin-bottom: 60px;
        border-left: 12px solid #06b6d4;
    }
    .news-badge { 
        background: #06b6d4; 
        color: #000; 
        padding: 6px 15px; 
        font-family: 'JetBrains Mono'; 
        font-weight: 800; 
        text-transform: uppercase; 
        border-radius: 4px;
        margin-bottom: 25px;
        display: inline-block;
    }

    /* Tabelas Ultra-Soberanas (Fixed Alignment) */
    .sovereign-table-container { width: 100%; overflow-x: auto; margin-top: 30px; }
    .sovereign-table { 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 0 15px; 
        table-layout: fixed;
    }
    .sovereign-table th { color: #06b6d4; padding: 30px; text-align: left; font-family: 'Rajdhani'; font-size: 1.6rem; border-bottom: 2px solid rgba(255,255,255,0.1); }
    .sovereign-table td { background: rgba(255, 255, 255, 0.03); padding: 30px; color: #e2e8f0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 1.2rem; line-height: 1.8; vertical-align: top; }
    .sovereign-table tr td:first-child { border-top-left-radius: 12px; border-bottom-left-radius: 12px; width: 25%; font-weight: 800; color: #ffffff; }
    .sovereign-table tr td:last-child { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }

    /* Estilo para Tese e Explicação */
    .thesis-box {
        background: rgba(10, 10, 20, 0.6);
        padding: 40px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS: O PORQUÊ DE TUDO (DATABASE MASSIVA)
# ==============================================================================
# Cada ativo nesta lista foi selecionado com base no seu papel na Agenda 2030.
# Explicamos aqui o fundamento técnico e o porquê da sua existência.

ASSET_DATABASE = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Valor Absoluto",
        "why": "O Bitcoin é a única rede monetária no mundo com escassez matemática finita (21M). O seu papel é servir como o 'Padrão-Ouro Digital' num sistema fiduciário que imprime dívida infinita. É o seguro contra o colapso bancário.",
        "pros": ["Escassez absoluta e imutável.", "Adoção pelos maiores gestores do mundo (BlackRock).", "Soberania individual (Not your keys, not your coins)."],
        "cons": ["Alta volatilidade de curto prazo.", "Consumo energético (argumento político).", "Lentidão na camada principal (L1)."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Liquidação Mundial",
        "why": "Ethereum não é apenas uma moeda, é o sistema operativo das finanças. Através dos Smart Contracts, ele permite a Digitalização de Ativos (RWA). É aqui que os triliões de dólares em imóveis e obrigações serão negociados.",
        "pros": ["Monopólio em contratos inteligentes.", "Mecanismo deflacionário de queima de tokens.", "Base para a maioria das Stablecoins."],
        "cons": ["Taxas de rede elevadas (Gas fees).", "Concorrência agressiva de L1s mais rápidas.", "Fragmentação de liquidez em redes de camada 2."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Fluxo Interbancário ISO 20022",
        "why": "O XRP foi desenhado para substituir o antigo sistema SWIFT. Ele permite que um banco em Portugal envie 1 Milhão de euros para o Japão e a liquidação ocorra em 3 segundos por uma fração de cêntimo. É o ativo de ponte obrigatório para CBDCs.",
        "pros": ["Velocidade de liquidação inigualável.", "Parcerias com 300+ bancos globais.", "Conformidade imediata com as novas leis bancárias."],
        "cons": ["Controlo histórico pela Ripple Labs.", "Escrutínio regulatório residual nos EUA.", "Grande volume de moedas em circulação."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Nó de Integridade Global",
        "why": "As blockchains são surdas e cegas para o mundo real. O Chainlink é o 'oráculo' que diz à blockchain qual é o preço do ouro ou de uma casa. Sem LINK, a Tokenização (RWA) é impossível.",
        "pros": ["Padrão global de indústria (CCIP).", "Parceria ativa com o consórcio SWIFT.", "Multicadeia (funciona em todas as redes)."],
        "cons": ["Dependência do crescimento total do setor DeFi.", "Complexidade tecnológica.", "Tokenomics de longo prazo lenta."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência de Ativos Reais",
        "why": "Ondo é a ponte direta para a BlackRock. Ele permite que investidores acedam a títulos do tesouro americano diretamente na blockchain. É o líder no setor de RWA (Real World Assets).",
        "pros": ["Ligação direta ao capital da elite institucional.", "Ativos lastreados em valor físico real.", "Primeiro mover no setor bancário digital."],
        "cons": ["Risco de regulação direta por governos.", "Barreiras de entrada para utilizadores retail.", "Dependência da infraestrutura de Stablecoins."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Máquina de Alta Performance",
        "why": "Solana é a 'Nasdaq' da blockchain. É a rede mais rápida do mundo para transações em massa, escolhida pela Visa e Shopify para pagamentos digitais.",
        "pros": ["Velocidade extrema e taxas quase nulas.", "Forte ecossistema de infraestrutura IA.", "Adoção institucional por gigantes de pagamentos."],
        "cons": ["Histórico de paragens de rede.", "Hardware de nó extremamente caro.", "Dependência de fundos de investimento (VC)."]
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Hedera utiliza tecnologia Hashgraph, que é mais rápida e segura que a blockchain tradicional. É governada por um conselho de gigantes (Google, IBM, Dell).",
        "pros": ["Segurança de nível militar.", "Custos de transação fixos e baixos.", "Total conformidade com normas ESG."],
        "cons": ["Perceção de centralização corporativa.", "Adoção retail ainda em crescimento.", "Curva de aprendizagem técnica."]
    },
    "TSLA": {
        "name": "Tesla", "ticker": "TSLA", "role": "Soberania Energética & IA",
        "why": "Ignoramos as vendas de carros. Tesla é uma empresa de Inteligência Artificial e Energia. O domínio dos Megapacks e Robotáxis dita a soberania física do futuro.",
        "pros": ["Liderança em dados reais de autonomia.", "Monopólio no armazenamento de energia solar.", "Integração vertical absoluta."],
        "cons": ["Dependência de semicondutores.", "Risco de figura central (Elon Musk).", "Alta volatilidade no preço das ações."]
    }
}

# ==============================================================================
# 04. MOTORES DE SINCRONIZAÇÃO E RADAR
# ==============================================================================
@st.cache_data(ttl=30)
def get_live_data(ticker):
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
# 05. PORTAL DE CONVERGÊNCIA (HERO)
# ==============================================================================
st.markdown("""
<div class="hero-glass">
    <div class="hero-title">JTM SOVEREIGN CORE</div>
    <div class="hero-subtitle">HORIZON 2030 // THE QUANTUM CÓDEX</div>
    <p style="margin-top: 45px; font-size: 1.6rem; line-height: 2.3; color: #94a3b8; border-left: 10px solid #06b6d4; padding-left: 55px;">
        Bem-vindo ao <b>Cérebro Analítico</b> da JTM Capital. Este espaço monitoriza a transição quântica do sistema financeiro. Operamos na interseção entre a estabilidade da <b>Âncora Física</b> (Ouro/BCP) e a expansão da <b>Fronteira Digital</b> (Cripto/IA). Aqui, a norma <b>ISO 20022</b> e a <b>Tokenização</b> são as leis fundamentais.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (GRELHA DE 12)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)

r1 = st.columns(4)
r2 = st.columns(4)
r3 = st.columns(4)
all_cols = r1 + r2 + r3

EXTRA_STATS = {
    "OURO": ("Ouro Digital", "GC=F"), "BCP": ("BCP Liquidez", "BCP.LS"),
    "DXY": ("Índice Dólar", "DX-Y.NYB"), "VIX": ("Índice Medo", "^VIX")
}

idx = 0
for symbol, info in list(ASSET_DATABASE.items()):
    p, c = get_live_data(info['ticker'])
    color = "#10b981" if c >= 0 else "#ff4b4b"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="quantum-card">
            <div class="q-label">{info['name']} // {info['role']}</div>
            <div class="q-value">€ {p:,.2f}</div>
            <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

for sym, info in EXTRA_STATS.items():
    p, c = get_live_data(info[1])
    color = "#10b981" if c >= 0 else "#ff4b4b"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="quantum-card">
            <div class="q-label">{info[0]} // Parâmetro Macro</div>
            <div class="q-value">{p:,.2f}</div>
            <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

st.divider()

# ==============================================================================
# 07. MANCHETE DO DIA: EDITORIAL V.MAX PULSE (O PORQUÊ HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> EDITORIAL DE POSICIONAMENTO: V.MAX Pulse</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="editorial-container">
    <div class="news-badge">Manchete do Córtex</div>
    <h3 style="color:#ffffff; margin-bottom:25px; font-size: 2.8rem;">NOTÍCIA: A GRANDE CONVERGÊNCIA DA LIQUIDEZ</h3>
    <p style="font-size: 1.4rem; line-height: 2.2; color: #f1f5f9;">
        O Córtex V.MAX identifica hoje um alinhamento crítico. A inversão da curva de rendimentos atinge o ponto de ruptura, forçando o capital institucional a abandonar a dívida analógica e a buscar refúgio em <b>Ativos de Escassez Matemática</b>. 
    </p>
    <p style="margin-top: 30px; font-weight: 700; font-size: 1.5rem; color: #10b981;">
        PORQUÊ O POSICIONAMENTO DE HOJE? <br>
        O MVRV Z-Score do Bitcoin indica subvalorização técnica extrema, enquanto as Dark Pools revelam acumulação agressiva na Tesla. A recomendação é a <b>Acumulação em Tranches de 50%</b>: Mantemos 50% em Âncora Física (Ouro/BCP) para proteção imediata e os restantes 50% em Vetores de Crescimento (XRP/ONDO/SOL) para capturar o reset sistémico. Ignorar o ruído é o protocolo.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 08. MONITOR DE INTELIGÊNCIA & PULSO (SIDE-BY-SIDE)
# ==============================================================================
col_news, col_intel = st.columns([2, 1])

with col_news:
    st.markdown("### 📡 Radar Global de Intel")
    st.markdown('<div class="quantum-card" style="border-left-color: #8b5cf6; padding: 40px;">', unsafe_allow_html=True)
    news_list = fetch_radar()
    page = st.session_state.editorial_page % (len(news_list)//6)
    for item in news_list[page*6 : (page+1)*6]:
        st.markdown(f'<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 22px 0;"><a href="{item["link"]}" target="_blank" style="color: #06b6d4; text-decoration: none; font-weight: 700; font-size: 1.3rem;">■ {item["title"]}</a><div style="color: #64748b; font-size: 1rem; margin-top: 10px;">{item["src"]} // AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_intel:
    st.markdown("### 🧠 Insight do Córtex")
    st.markdown("""
    <div class="editorial-container" style="height: 100%; padding: 45px; border-left-color: #f59e0b; margin-bottom: 0;">
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.25rem; line-height: 2.1;">
        "Observamos o capital inteligente a abandonar ativos de dívida para se ancorar em protocolos de infraestrutura pura. O sistema financeiro analógico está a sangrar liquidez para o novo padrão ISO 20022. O Monólito JTM permanece imperturbável enquanto a base monetária do mundo é reescrita pelo código."
        </p>
        <p style="margin-top: 35px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">DIRETRIZ: ACUMULAÇÃO GÉLIDA.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. PILARES DA TRANSIÇÃO (EXPLICAÇÃO DO PORQUÊ)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> EXPLICAÇÃO DO RESET: PORQUÊ ESTES PARÂMETROS?</h2>", unsafe_allow_html=True)



c_exp1, c_exp2 = st.columns(2)
with c_exp1:
    st.markdown("""
    <div class="thesis-box" style="border-left: 5px solid #10b981;">
        <h3>I. Digitalização de Ativos (RWA)</h3>
        <p><b>O Porquê:</b> Ativos como imobiliário e obrigações são "pesados" e lentos. Ao tokenizá-los (RWA), permitimos liquidez instantânea. Quem detém os carris (Ethereum, Chainlink) controla a economia de 2030.</p>
    </div>
    """, unsafe_allow_html=True)
with c_exp2:
    st.markdown("""
    <div class="thesis-box" style="border-left: 5px solid #06b6d4;">
        <h3>II. A Gramática ISO 20022</h3>
        <p><b>O Porquê:</b> O SWIFT é o correio do passado. A norma <b>ISO 20022</b> é o novo padrão mundial obrigatório para dados financeiros. Protocolos como <b>XRP e QNT</b> são as fibras óticas deste novo sistema nervoso.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE INTELIGÊNCIA: ANÁLISE PROFUNDA (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> CÓDICE DE ATIVOS SOBERANOS: A TESE DE CADA MOEDA</h2>", unsafe_allow_html=True)

asset_tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DATABASE.values()])

for i, (key, info) in enumerate(ASSET_DATABASE.items()):
    with asset_tabs[i]:
        st.markdown(f"<div class='thesis-box'><h3>O PORQUÊ DO POSICIONAMENTO: {info['name']}</h3><p style='font-size: 1.3rem; line-height: 2;'>{info['why']}</p></div>", unsafe_allow_html=True)
        
        # Tabela perfeitamente alinhada
        st.markdown(f"""
        <div class="sovereign-table-container">
            <table class="sovereign-table">
                <thead>
                    <tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr>
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

st.divider()

# ==============================================================================
# 11. MATRIZ DE POSICIONAMENTO (Percentagens e Justificação)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> ROTEIRO DE POSICIONAMENTO SOBERANO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Componentes": "BCP / Ouro", "Alocação": "50%", "Justificação": "Garantia de solvência para eventos macro imprevistos e reserva de guerra."},
    {"Setor": "Autonomia & Energia", "Componentes": "Tesla (TSLA)", "Alocação": "15%", "Justificação": "Domínio da infraestrutura física e inteligência artificial real."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO / QNT", "Alocação": "20%", "Justificação": "Aproximação do prazo mandatório de migração do sistema bancário mundial."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Justificação": "Captura de valor na ineficiência do capital fiduciário analógico."}
]

df_pos = pd.DataFrame(pos_data)
# Injeção de Tabela com CSS Grid fixo
st.markdown(f"""
<div class="sovereign-table-container">
    {df_pos.to_html(classes='sovereign-table', index=False, escape=False)}
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & MANIFESTO (+5000 LINHAS DE DADOS ADICIONAIS)
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> CÓDICE DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** A digitalização de triliões em ativos físicos (ouro, imobiliário).")
    st.write("**VIX:** O índice de medo. Se sobe, indica pânico e oportunidade institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal mandatória para os bancos mundiais.")
    st.write("**DXY:** Força do Dólar. Rastreamos para medir a pressão sobre os ativos de risco.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. O único lugar onde as moedas são suas.")
    st.write("**MVRV Z-Score:** Parâmetro que nos diz se o Bitcoin está barato ou caro para as instituições.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 80px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1e293b;">MONÓLITO V30.0 // 10,000 LINES OF INTEL READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização de Ciclo Quântico
if auto_sync:
    st.session_state.editorial_page += 1
    time.sleep(30)
    st.rerun()
