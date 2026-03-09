import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & INICIALIZAÇÃO SOBERANA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Matrix V37",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de variáveis de estado para evitar NameError
if 'pulse_index' not in st.session_state:
    st.session_state.pulse_index = 0

# Variável de controlo global
sync_active = True 

# --- SIDEBAR: GOVERNANÇA (CYBER-ELITE) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(0, 212, 255, 0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.3); text-align: center;'>
            <h2 style='color: #00d4ff; font-family: Rajdhani; margin:0;'>SOVEREIGN CORE</h2>
            <p style='color: #00ffa3; font-family: Inter; font-size: 0.8rem; letter-spacing: 2px;'>V37.0 // APEX MASTER</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    sync_active = st.toggle("Sincronização Ativa", value=True)
    
    st.markdown("### 🧭 Alocação Estratégica")
    st.info("**Âncora (50%):** BCP / OURO\n\n**Fronteira (50%):** IA / CRIPTO")
    
    st.markdown("---")
    st.markdown("### 🔒 Custódia Tática")
    st.error("Extração: Dia 29\nStatus: Cold Storage")
    
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MATRIX V37: ESTÉTICA FUTURISTA & TABELAS BLINDADAS
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; }
    .stApp { 
        background-color: #010204; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0a192f 0%, #010204 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: 'Rajdhani', sans-serif; letter-spacing: 5px; font-weight: 700; text-transform: uppercase; }

    /* Glassmorphism Hero */
    .hero-matrix {
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 6px solid #00d4ff;
        padding: 80px;
        border-radius: 25px;
        margin-bottom: 60px;
        box-shadow: 0 60px 200px rgba(0,0,0,1);
    }
    .hero-title { font-size: 5.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.9; margin: 0; }
    .hero-subtitle { color: #00d4ff; font-size: 1.8rem; letter-spacing: 20px; margin-top: 30px; font-weight: 600; }

    /* Quantum Metrics Grid */
    .q-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 5px solid #00ffa3;
        padding: 35px;
        border-radius: 12px;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .q-card:hover { transform: translateY(-12px); border-color: #00d4ff; box-shadow: 0 30px 80px rgba(0, 212, 255, 0.2); }
    .q-label { font-size: 0.85rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 2px; }
    .q-value { font-size: 2.3rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* News Monitor - Alinhamento Perfeito */
    .news-box {
        background: rgba(5, 10, 20, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 40px;
        min-height: 550px;
        border-top: 5px solid #8b5cf6;
    }
    .news-item { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 22px 0; }
    .news-title { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem; display: block; margin-bottom: 8px; }

    /* Tabelas Blindadas */
    .apex-table { width: 100%; border-collapse: separate; border-spacing: 0 12px; table-layout: fixed; }
    .apex-table th { color: #00d4ff; padding: 20px; text-align: left; font-family: 'Rajdhani'; font-size: 1.5rem; border-bottom: 2px solid rgba(255,255,255,0.1); }
    .apex-table td { background: rgba(255, 255, 255, 0.02); padding: 25px; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.05); font-size: 1.1rem; line-height: 1.7; vertical-align: top; }
    .apex-table tr td:first-child { border-top-left-radius: 12px; border-bottom-left-radius: 12px; font-weight: 700; color: #fff; width: 30%; }
    .apex-table tr td:last-child { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }

    /* Editorial Box */
    .editorial-matrix {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 163, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 60px;
        border-radius: 25px;
        border-left: 12px solid #00d4ff;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE SOBERANO: PORQUÊ CADA NÓ? (DATA)
# ==============================================================================
ASSET_DATA = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania",
        "why": "Único ativo com escassez finita verificável. Proteção definitiva contra o colapso fiduciário.",
        "pros": ["Escassez 21M.", "Adoção Institucional."], "cons": ["Volatilidade.", "Lentidão L1."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação RWA",
        "why": "Onde os triliões em ativos reais (RWA) serão liquidados. O sistema operativo das finanças.",
        "pros": ["Líder Smart Contracts.", "Deflacionário."], "cons": ["Gas fees."],
        "link": "https://ethereum.org/"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "Substituto do SWIFT. Ativo de ponte mandatório para a nova norma bancária mundial.",
        "pros": ["Velocidade (3s).", "Parcerias Bancárias."], "cons": ["Regulação."],
        "link": "https://ripple.com/"
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência Institucional",
        "why": "Digitalização do Tesouro Americano. O elo direto entre a BlackRock e a Blockchain.",
        "pros": ["BlackRock Link.", "Yield Seguro."], "cons": ["Regulação Fiat."],
        "link": "https://ondo.finance/"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & RADAR
# ==============================================================================
@st.cache_data(ttl=25)
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
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    return news

# ==============================================================================
# 05. NÓ DE CONVERGÊNCIA: HERO MATRIX
# ==============================================================================
st.markdown("""
<div class="hero-matrix">
    <div class="hero-title">JTM SOVEREIGN MATRIX</div>
    <div class="hero-subtitle">HORIZON 2030 // THE APEX CÓDEX</div>
    <p style="margin-top: 40px; font-size: 1.5rem; line-height: 2.2; color: #94a3b8; border-left: 10px solid #00d4ff; padding-left: 50px;">
        Bem-vindo ao <b>Cérebro Analítico Apex</b>. Este monólito monitoriza a transição sistémica da liquidez mundial para o padrão 2030. Operamos na interseção entre a estabilidade da <b>Âncora Física</b> e a expansão da <b>Fronteira Digital</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR (GRELHA DINÂMICA)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> SINCRONIZAÇÃO DE VALOR GLOBAL (EUR €)</h2>", unsafe_allow_html=True)

MACRO_KEYS = {
    "GOLD": ("Ouro (GC=F)", "GC=F"), "TSLA": ("Tesla IA (TSLA)", "TSLA"),
    "BCP": ("BCP Liquidez", "BCP.LS"), "VIX": ("Índice Medo", "^VIX"),
    "DXY": ("Dólar (DXY)", "DX-Y.NYB"), "QNT": ("Quant (QNT)", "QNT-EUR"),
    "SOL": ("Solana (SOL)", "SOL-EUR"), "NEAR": ("Near IA (NEAR)", "NEAR-EUR")
}

items = list(ASSET_DATA.items()) + list(MACRO_KEYS.items())
cols_per_row = 4

for i in range(0, len(items), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        idx = i + j
        if idx < len(items):
            key, val = items[idx]
            name, ticker = (val['name'], val['ticker']) if isinstance(val, dict) else (val[0], val[1])
            p, c = get_live_data(ticker)
            color = "#00ffa3" if c >= 0 else "#ff4b4b"
            with cols[j]:
                st.markdown(f"""
                <div class="q-card">
                    <div class="q-label">{name}</div>
                    <div class="q-value">€ {p:,.2f}</div>
                    <div style="color: {color}; font-weight: bold; font-family: 'JetBrains Mono'; margin-top: 15px;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> MONITOR DE INTELIGÊNCIA // O PULSO</h2>", unsafe_allow_html=True)
col_radar, col_insight = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="news-box">', unsafe_allow_html=True)
    st.markdown("### 📡 Radar de Fluxo Global")
    radar_list = fetch_radar()
    page = st.session_state.pulse_index % (len(radar_list)//6) if radar_list else 0
    for item in radar_list[page*6 : (page+1)*6]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank" class="news-title">■ {item['title']}</a>
            <div style="color: #64748b; font-size: 0.9rem; font-family: 'JetBrains Mono';">FONTE: {item['src']} // AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_insight:
    st.markdown("""
    <div class="editorial-matrix" style="height: 100%; padding: 45px; border-left-color: #f59e0b; margin-top: 0;">
        <h3 style="color: #f59e0b;">CÓRTEX V.MAX: INSIGHT</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.3rem; line-height: 2.2;">
        "O capital institucional está a fugir de ativos de dívida analógica. O sistema está a sangrar liquidez para o novo padrão ISO 20022. O Monólito permanece imperturbável."
        </p>
        <p style="margin-top: 35px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">SENTIMENTO: POSICIONAMENTO GÉLIDO.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO E EDITORIAL
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MAPA DE POSICIONAMENTO RECOMENDADO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora Física", "Ativos": "BCP / OURO", "Alocação": "50%", "Nota": "Liquidez Macro."},
    {"Setor": "Autonomia IA", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Nota": "Domínio IA/Energia."},
    {"Setor": "Fluxo ISO", "Ativos": "XRP / ONDO", "Alocação": "20%", "Nota": "Reset Bancário."},
    {"Setor": "Digital Scarcity", "Ativos": "BTC / ETH / NEAR", "Alocação": "15%", "Nota": "Escassez Matemática."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(f"""
<div style="overflow-x: auto;">
    <table class="apex-table">
        <thead>
            <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Nota de Execução</th></tr>
        </thead>
        <tbody>
            {''.join([f"<tr><td>{r['Setor']}</td><td>{r['Ativos']}</td><td>{r['Alocação']}</td><td>{r['Nota']}</td></tr>" for _, r in df_pos.iterrows()])}
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="editorial-matrix">
    <h3 style="color:#ffffff; margin-bottom:20px;">TESE: PORQUÊ ESTA ALOCAÇÃO HOJE?</h3>
    <p style="font-size: 1.3rem; line-height: 2.2; color: #f1f5f9;">
        O MVRV Z-Score do Bitcoin indica subvalorização técnica, enquanto a BlackRock absorve liquidez do Tesouro via Ondo. Mantemos 50% em Âncora Física pois o VIX sinaliza volatilidade iminente.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 25px;">
        <a href="https://ondo.finance/" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[ONDO FINANCE]</a>
        <a href="https://ripple.com/" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[RIPPLE/XRP]</a>
        <a href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[ISO 20022]</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. DIAGRAMAS E CÓDICE TÉCNICO (IMAGENS CORRIGIDAS)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ARQUITETURA DA NOVA LIQUIDEZ</h2>", unsafe_allow_html=True)

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("### O Ciclo RWA (Real World Assets)")
    st.write("Digitalização da propriedade física em rede.")
    st.markdown("")



with c_img2:
    st.markdown("### A Norma ISO 20022")
    st.write("A nova linguagem mundial do dinheiro.")
    st.markdown("")



st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: O PORQUÊ TÉCNICO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE ATIVOS SOBERANOS // O PORQUÊ TÉCNICO</h2>", unsafe_allow_html=True)
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DATA.values()])

for i, (key, info) in enumerate(ASSET_DATA.items()):
    with tabs[i]:
        col_t, col_i = st.columns([1.5, 1])
        with col_t:
            st.markdown(f"### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.markdown(f"""
            <table class="apex-table">
                <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                <tbody><tr>
                    <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                    <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                </tr></tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#00ffa3;'>WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        with col_i:
            st.markdown("### Verificação de Rede")
            # FIX: SyntaxError resolvido aqui com f-string correta
            st.markdown(f"[{info['name']} blockchain network topology and security verification process]")



st.divider()

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1e293b;">MONÓLITO V37.0 // SYNTAX ERROR FIXED</small>
</div>
""", unsafe_allow_html=True)

if sync_active:
    st.session_state.pulse_index += 1
    time.sleep(30)
    st.rerun()
