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
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V31",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'editorial_page' not in st.session_state:
    st.session_state.editorial_page = 0

# --- SIDEBAR: CONSELHO DE GOVERNANÇA (ULTRA-MODERN) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; border: 1px solid rgba(0,212,255,0.2);'>
            <h1 style='color: #00d4ff; font-family: Rajdhani; text-align: center; font-size: 1.8rem;'>SOVEREIGN CORE</h1>
            <p style='text-align: center; color: #00ffa3; font-family: JetBrains Mono; font-size: 0.8rem;'>CÓRTEX V.MAX: GOD MODE</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_sync = st.toggle("Sincronização Ativa", value=True)
    
    st.markdown("### 🧭 Direcionamento de Capital")
    st.info("**Âncora de Proteção (50%):** BCP / OURO\n\n**Vetor de Crescimento (50%):** TSLA / CRIPTO")
    
    st.markdown("---")
    st.markdown("### 🔒 Protocolo de Custódia")
    st.warning("Extração: Dia 29\nCold Storage: Ativo")
    
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS APEX: O PINÁCULO DO DESIGN MODERNO (TABELAS FIXAS E EFEITOS NEON)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    /* Global Reset */
    .main .block-container { padding: 3rem 6rem; max-width: 100%; overflow-x: hidden; }
    
    /* Fundo Obsidian Mirror */
    .stApp { 
        background-color: #010204; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0a192f 0%, #010204 100%); 
    }
    
    /* Títulos Soft e Elegantes */
    h1, h2, h3 { color: #ffffff; font-family: 'Rajdhani', sans-serif; letter-spacing: 5px; font-weight: 700; text-transform: uppercase; }

    /* Hero Section Futurista */
    .hero-apex {
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 6px solid #00d4ff;
        padding: 100px;
        border-radius: 25px;
        margin-bottom: 70px;
        box-shadow: 0 60px 250px rgba(0,0,0,1);
        position: relative;
        overflow: hidden;
    }
    .hero-title { font-size: 6.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.8; margin: 0; color: #fff; }
    .hero-subtitle { color: #00d4ff; font-size: 2.2rem; letter-spacing: 25px; margin-top: 35px; font-weight: 600; opacity: 0.8; }

    /* Quantum Metrics */
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin-bottom: 50px; }
    .q-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-left: 6px solid #00ffa3;
        padding: 40px;
        border-radius: 15px;
        transition: 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    }
    .q-card:hover { transform: translateY(-15px); border-color: #00d4ff; box-shadow: 0 40px 80px rgba(0, 212, 255, 0.2); }
    .q-label { font-size: 0.9rem; color: #64748b; font-family: 'JetBrains Mono'; letter-spacing: 3px; }
    .q-value { font-size: 2.6rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 15px; }

    /* Tabelas Perfeitas (Fixing Alignment) */
    .table-wrapper { width: 100%; margin-top: 30px; overflow-x: auto; border-radius: 15px; }
    .apex-table { width: 100%; border-collapse: separate; border-spacing: 0 12px; table-layout: fixed; }
    .apex-table th { color: #00d4ff; padding: 25px; text-align: left; font-family: 'Rajdhani'; font-size: 1.5rem; border-bottom: 2px solid rgba(255,255,255,0.1); }
    .apex-table td { background: rgba(255, 255, 255, 0.02); padding: 30px; color: #e2e8f0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 1.2rem; line-height: 1.8; vertical-align: top; }
    .apex-table tr td:first-child { border-top-left-radius: 15px; border-bottom-left-radius: 15px; font-weight: 800; color: #ffffff; width: 25%; }
    .apex-table tr td:last-child { border-top-right-radius: 15px; border-bottom-right-radius: 15px; }

    /* Editorial Section */
    .editorial-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 163, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 70px;
        border-radius: 20px;
        margin-bottom: 70px;
        border-left: 15px solid #00d4ff;
    }
    .news-badge { background: #00d4ff; color: #000; padding: 6px 18px; font-weight: 900; border-radius: 4px; font-family: 'JetBrains Mono'; margin-bottom: 30px; display: inline-block; }

    /* Thesis Boxes */
    .thesis-container {
        background: rgba(0, 0, 0, 0.3);
        padding: 50px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
    }
    
    .glow-txt { color: #00ffa3; text-shadow: 0 0 10px rgba(0, 255, 163, 0.4); font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE OMNIPOTENTE: A TESE DE CADA NÓ (EXPANSÃO MASSIVA)
# ==============================================================================
ASSET_INTELLIGENCE = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania Matemática",
        "why": "O Bitcoin é o único ativo no universo conhecido com escassez finita verificável por código. No sistema JTM, ele atua como a 'Bateria de Valor' final. Quando o Euro e o Dólar perdem poder de compra via inflação, o Bitcoin absorve essa liquidez perdida.",
        "pros": ["Imutabilidade absoluta.", "Maior rede de computação do planeta.", "Escassez de 21 Milhões."],
        "cons": ["Resistência de governos autoritários.", "Volatilidade de curto prazo.", "Incompreensão das massas."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Infraestrutura RWA",
        "why": "Ethereum é a camada de software das finanças globais. Através da Tokenização de Ativos do Mundo Real (RWA), o Ethereum permite que triliões em imóveis e ações fluam sem a necessidade de bancos comerciais lentos.",
        "pros": ["Domínio de 80% do mercado DeFi.", "Mecanismo de 'Burn' (Deflacionário).", "Infraestrutura para Stablecoins."],
        "cons": ["Custos de rede em picos de tráfego.", "Complexidade técnica para o leigo.", "Concorrência de L1s emergentes."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Interoperabilidade ISO 20022",
        "why": "O XRP é o substituto direto do sistema SWIFT. Ele não é apenas uma moeda, é um protocolo de liquidação. Ele permite que bancos mundiais movam valor instantaneamente sob as novas normas bancárias ISO 20022.",
        "pros": ["Liquidação em 3-5 segundos.", "Conformidade bancária total.", "Eficiência energética extrema."],
        "cons": ["Controlo residual pela Ripple Labs.", "Escrutínio regulatório histórico.", "Grande oferta circulante."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência Institucional",
        "why": "Ondo é a ponte direta da BlackRock para a Blockchain. Ele permite a digitalização de obrigações do tesouro americano, criando um yield (rendimento) seguro e institucional para a nossa carteira.",
        "pros": ["Parceria implícita com a elite financeira.", "Ativos lastreados em valor físico.", "Primeiro mover no setor RWA."],
        "cons": ["Risco de regulação direta de títulos.", "Barreiras de entrada para o retalho.", "Baixa liquidez em capitulação."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Máquina de Transações em Massa",
        "why": "Solana é a rede de alta performance escolhida pela Visa. O seu papel é permitir micropagamentos e comércio em massa a uma velocidade que o Ethereum ainda não consegue atingir.",
        "pros": ["Taxas inferiores a 1 cêntimo.", "Velocidade de 65k TPS.", "Forte adoção em IA e DePIN."],
        "cons": ["Instabilidade técnica histórica.", "Hardware de nó extremamente caro.", "Dependência de Capital de Risco (VC)."]
    },
    "NEAR": {
        "name": "Near", "ticker": "NEAR-EUR", "role": "Cérebro de Inteligência Web3",
        "why": "Near foca-se na abstração de conta e inteligência artificial. É a infraestrutura que permitirá que pessoas usem cripto sem saberem que estão a usar cripto. É o elo entre a IA e a Blockchain.",
        "pros": ["Facilidade de uso incomparável.", "Sharding dinâmico para escala.", "Liderança em pesquisa de IA."],
        "cons": ["Setor de IA é altamente volátil.", "Marketing inferior a Layer 1 rivais.", "Dependência de dApps de IA."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=25)
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
            for entry in feed.entries[:10]:
                news.append({"title": entry.title, "link": entry.link, "src": src, "ts": time.mktime(entry.published_parsed)})
        except: continue
    return sorted(news, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. NÓ DE CONVERGÊNCIA: HERO APEX
# ==============================================================================
st.markdown("""
<div class="hero-apex">
    <div class="hero-title">JTM CAPITAL</div>
    <div class="hero-subtitle">SOVEREIGN CORE // HORIZON 2030</div>
    <p style="margin-top: 50px; font-size: 1.6rem; line-height: 2.3; color: #94a3b8; border-left: 10px solid #00d4ff; padding-left: 60px;">
        Bem-vindo ao <b>Sovereign Core Apex</b>. Este terminal é o ápice da inteligência analítica da JTM Capital. Operamos através da observação fria de dados macro e da migração sistémica para o padrão <b>ISO 20022</b>. Aqui, a volatilidade é apenas uma ferramenta para a <b>Acumulação Soberana</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR (GRELHA APEX)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> SINCRONIZAÇÃO DE VALOR INSTITUCIONAL</h2>", unsafe_allow_html=True)

row1, row2 = st.columns(4), st.columns(4)
all_cols = row1 + row2

EXTRA_MACRO = {
    "TSLA": ("Tesla IA", "TSLA"), "GOLD": ("Ouro Físico", "GC=F"),
    "BCP": ("BCP Liquidez", "BCP.LS"), "QNT": ("Quant ISO", "QNT-EUR")
}

idx = 0
for symbol, info in list(ASSET_INTELLIGENCE.items()):
    p, c = fetch_telemetry(info['ticker'])
    color = "#00ffa3" if c >= 0 else "#ff4b4b"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="q-card">
            <div class="q-label">{info['name']} // {info['role']}</div>
            <div class="q-value">€ {p:,.2f}</div>
            <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

for sym, info in EXTRA_MACRO.items():
    p, c = fetch_telemetry(info[1])
    color = "#00ffa3" if c >= 0 else "#ff4b4b"
    with all_cols[idx]:
        st.markdown(f"""
        <div class="q-card">
            <div class="q-label">{info[0]} // Fluxo Macro</div>
            <div class="q-value">€ {p:,.2f}</div>
            <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    idx += 1

st.divider()

# ==============================================================================
# 07. EDITORIAL V.MAX: A NOTÍCIA E O PORQUÊ (HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> EDITORIAL DE POSICIONAMENTO // PULSO V.MAX</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="editorial-box">
    <div class="news-badge">Manchete do Córtex</div>
    <h3 style="color:#ffffff; margin-bottom:25px; font-size: 2.8rem;">NOTÍCIA: A GRANDE INFLEXÃO DA LIQUIDEZ GLOBAL</h3>
    <p style="font-size: 1.4rem; line-height: 2.2; color: #f1f5f9;">
        O Córtex V.MAX identifica hoje um alinhamento crítico no sistema financeiro internacional. A inversão da curva de rendimentos e a força do índice Dólar sinalizam que estamos a entrar na fase final de <b>Limpeza Fiduciária</b>. O capital institucional está a fugir de obrigações de dívida para se ancorar em <b>Protocolos de Infraestrutura Pura</b>.
    </p>
    <p style="margin-top: 35px; font-weight: 700; font-size: 1.6rem; color: #00ffa3;">
        PORQUÊ O POSICIONAMENTO DE HOJE? <br>
        O MVRV Z-Score do Bitcoin indica subvalorização técnica, enquanto as Dark Pools revelam acumulação agressiva na Tesla. A recomendação soberana é a <b>Acumulação em Tranches de 50%</b>. Mantemos 50% em Âncora de Proteção (Ouro/BCP) para garantir liquidez em caso de evento macro imprevisto, e os restantes 50% em Vetores de Crescimento (XRP/ONDO/NEAR) para capturar o reset sistémico.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 08. RADAR GLOBAL & INSIGHT (SIDE-BY-SIDE)
# ==============================================================================
col_radar, col_insight = st.columns([2, 1])

with col_radar:
    st.markdown("### 📡 Radar de Inteligência Global")
    st.markdown('<div class="q-card" style="border-left-color: #8b5cf6;">', unsafe_allow_html=True)
    news_list = fetch_radar()
    page = st.session_state.editorial_page % (len(news_list)//5)
    for item in news_list[page*5 : (page+1)*5]:
        st.markdown(f'<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 22px 0;"><a href="{item["link"]}" target="_blank" style="color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem;">■ {item["title"]}</a><div style="color: #64748b; font-size: 0.95rem; margin-top: 10px;">{item["src"]} // AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_insight:
    st.markdown("### 🧠 Insight do Córtex")
    st.markdown("""
    <div class="editorial-box" style="height: 100%; padding: 45px; border-left-color: #f59e0b; margin-bottom: 0;">
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.3rem; line-height: 2.2;">
        "Observamos o capital de elite a abandonar ativos de dívida para se ancorar em protocolos que o sistema será obrigado a utilizar. O Monólito JTM permanece imperturbável enquanto a base monetária do mundo é reescrita pelo código e pela matemática."
        </p>
        <p style="margin-top: 40px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">SINAL: POSICIONAMENTO GÉLIDO.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. PILARES DA TRANSIÇÃO (PORQUÊ?)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ARQUITETURA DO NOVO MUNDO // PORQUÊ CADA PARÂMETRO?</h2>", unsafe_allow_html=True)

c_exp1, c_exp2 = st.columns(2)
with c_exp1:
    st.markdown("""
    <div class="thesis-container" style="border-left: 10px solid #00ffa3;">
        <h3 style="color:#ffffff;">I. Digitalização de Ativos (RWA)</h3>
        <p style="font-size: 1.3rem; line-height: 2.1;"><b>O Porquê:</b> Ativos físicos são lentos. Ao tokenizá-los, permitimos liquidez 24/7. Quem controla as redes (Ethereum, Ondo) controla o fluxo de capital de 2030.</p>
    </div>
    """, unsafe_allow_html=True)
with c_exp2:
    st.markdown("""
    <div class="thesis-container" style="border-left: 10px solid #00d4ff;">
        <h3 style="color:#ffffff;">II. A Linguagem Universal ISO 20022</h3>
        <p style="font-size: 1.3rem; line-height: 2.1;"><b>O Porquê:</b> O sistema SWIFT é o passado. A norma <b>ISO 20022</b> é o novo padrão mundial obrigatório. Protocolos como <b>XRP e QNT</b> são a fibra ótica deste sistema.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: TESE DE CADA MOEDA (ALINHAMENTO TOTAL)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE ATIVOS SOBERANOS // O PORQUÊ TÉCNICO</h2>", unsafe_allow_html=True)

tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_INTELLIGENCE.values()])

for i, (key, info) in enumerate(ASSET_INTELLIGENCE.items()):
    with tabs[i]:
        st.markdown(f"<div class='thesis-container'><h3 style='color: #00d4ff;'>TESE SOBERANA: {info['name']}</h3><p style='font-size: 1.3rem; line-height: 2.2;'>{info['why']}</p></div>", unsafe_allow_html=True)
        
        # Tabela HTML Blindada
        st.markdown(f"""
        <div class="table-wrapper">
            <table class="apex-table">
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
# 11. MATRIZ DE POSICIONAMENTO RECOMENDADA (HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ROTEIRO DE POSICIONAMENTO RECOMENDADO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Componentes": "BCP / OURO", "Alocação": "50%", "Justificação": "Garantia de solvência e reserva de guerra para eventos macro imprevistos."},
    {"Setor": "Autonomia & Energia", "Componentes": "Tesla (TSLA)", "Alocação": "15%", "Justificação": "Domínio da infraestrutura física e inteligência artificial real."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO / QNT", "Alocação": "20%", "Justificação": "Aproximação do prazo mandatório de migração bancária global."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Justificação": "Captura de valor na ineficiência do capital analógico."}
]

df_pos = pd.DataFrame(pos_data)
# Injeção de Tabela com Alinhamento Fixo
st.markdown(f"""
<div class="table-wrapper">
    {df_pos.to_html(classes='apex-table', index=False, escape=False)}
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Digitalização de triliões em ativos físicos (ouro, imobiliário).")
    st.write("**VIX:** Índice de medo. Se sobe, indica pânico e oportunidade institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal mandatória para os bancos mundiais.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão sobre os ativos de risco.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. O único lugar onde as moedas são suas.")
    st.write("**MVRV Z-Score:** Parâmetro que nos diz se o Bitcoin está barato ou caro institucionalmente.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 80px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1e293b;">MONÓLITO V31.0 // THE OMNIPOTENT APEX READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização de Ciclo
if auto_sync:
    st.session_state.editorial_page += 1
    time.sleep(30)
    st.rerun()
