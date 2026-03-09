import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & INICIALIZAÇÃO GLOBAL
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Matrix V36",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'pulse_index' not in st.session_state:
    st.session_state.pulse_index = 0

auto_refresh = True # Ativo por padrão para o loop final

# --- SIDEBAR: GOVERNANÇA SOBERANA (CYBER-ELITE) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(0, 212, 255, 0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,212,255,0.3);'>
            <h1 style='color: #00d4ff; font-family: Rajdhani; text-align: center; font-size: 1.8rem;'>SOVEREIGN CORE</h1>
            <p style='text-align: center; color: #00ffa3; font-family: Inter; font-size: 0.9rem; letter-spacing: 3px;'>CÓRTEX V.MAX // MASTER</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    sync_active = st.toggle("Sincronização Quântica", value=True)
    
    st.markdown("### 🧭 Horizonte 2030")
    st.info("**Âncora:** 50% (OURO/BCP)\n\n**Fronteira:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔒 Protocolo de Custódia")
    st.error("Extração: Dia 29\nCold Storage: Ativo")
    
    st.markdown("---")
    st.caption(f"Refresco do Sistema: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS INFINITY-GLASS V36 (ESTÉTICA FUTURISTA & TABELAS FIXAS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    /* Global Styling */
    .main .block-container { padding: 2rem 5rem; max-width: 100%; }
    .stApp { 
        background-color: #010204; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0a192f 0%, #010204 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: 'Rajdhani', sans-serif; letter-spacing: 5px; font-weight: 700; text-transform: uppercase; }

    /* Glassmorphism Hero Section */
    .hero-matrix {
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 6px solid #00d4ff;
        padding: 100px;
        border-radius: 30px;
        margin-bottom: 80px;
        box-shadow: 0 60px 200px rgba(0,0,0,1);
    }
    .hero-title { font-size: 6rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.8; margin: 0; }
    .hero-subtitle { color: #00d4ff; font-size: 2.2rem; letter-spacing: 25px; margin-top: 40px; font-weight: 600; }

    /* Quantum Metrics */
    .q-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 6px solid #00ffa3;
        padding: 40px;
        border-radius: 15px;
        transition: 0.6s cubic-bezier(0.19, 1, 0.22, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .q-card:hover { transform: translateY(-15px); border-color: #00d4ff; box-shadow: 0 40px 100px rgba(0, 212, 255, 0.25); }
    .q-label { font-size: 0.9rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 3px; text-transform: uppercase; }
    .q-value { font-size: 2.8rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 15px; }

    /* News Box Alinhada (The Pulse) */
    .news-monitor {
        background: rgba(5, 10, 20, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 50px;
        min-height: 600px;
        border-top: 5px solid #8b5cf6;
        overflow: hidden;
    }
    .news-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
    }
    .news-title { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.4rem; display: block; margin-bottom: 10px; }
    .news-title:hover { color: #00ffa3; }

    /* Tabelas Ultra-Soberanas (Blindadas) */
    .apex-table-container { width: 100%; overflow: hidden; margin-top: 30px; border-radius: 15px; }
    .apex-table { width: 100%; border-collapse: separate; border-spacing: 0 15px; table-layout: fixed; }
    .apex-table th { color: #00d4ff; padding: 25px; text-align: left; font-family: 'Rajdhani'; font-size: 1.6rem; border-bottom: 2px solid rgba(255,255,255,0.1); }
    .apex-table td { background: rgba(255, 255, 255, 0.02); padding: 30px; color: #e2e8f0; border-top: 1px solid rgba(255,255,255,0.05); font-size: 1.2rem; line-height: 1.8; vertical-align: top; }
    .apex-table tr td:first-child { border-top-left-radius: 15px; border-bottom-left-radius: 15px; font-weight: 800; color: #ffffff; width: 30%; }
    .apex-table tr td:last-child { border-top-right-radius: 15px; border-bottom-right-radius: 15px; }

    /* Editorial Box */
    .editorial-matrix {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 163, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 70px;
        border-radius: 30px;
        border-left: 15px solid #00d4ff;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE INTELIGÊNCIA: A TESE DOS PORQUÊS (+10,000 LINHAS DE DADOS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania",
        "why": "Ouro digital. Ativo de escassez matemática finita (21M). Essencial para proteção contra o colapso fiduciário e inflação.",
        "tech": "A maior rede descentralizada do mundo, utilizando prova de trabalho (PoW) para garantir imutabilidade absoluta.",
        "pros": ["Escassez 21M.", "Adoção Institucional.", "Resistência a Censura."],
        "cons": ["Volatilidade.", "Lentidão L1."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Camada de Liquidação",
        "why": "O sistema operativo das finanças. É onde os triliões em RWA (Real World Assets) serão tokenizados e liquidados.",
        "tech": "Blockchain de Smart Contracts líder. Transição para PoS reduziu consumo e aumentou a eficiência de queima de tokens.",
        "pros": ["Mecanismo Deflacionário.", "Ecossistema DeFi.", "Líder RWA."],
        "cons": ["Gas fees elevadas.", "Competição L1."],
        "link": "https://ethereum.org/en/whitepaper/"
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "O ativo de ponte para o novo sistema bancário. Substitui o SWIFT para liquidações internacionais instantâneas.",
        "tech": "Protocolo de consenso (RPCA) que permite transações em 3 segundos com custos quase nulos e conformidade ISO nativa.",
        "pros": ["Velocidade (3s).", "Parcerias Bancárias.", "Custos Nulos."],
        "cons": ["Ripple Labs Control.", "Regulação."],
        "link": "https://ripple.com/xrp/"
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "O elo direto entre a BlackRock e a Blockchain. Permite deter dívida do tesouro americano em formato digital.",
        "tech": "Protocolo de ativos reais focado em yield institucional e conformidade regulatória de alto nível.",
        "pros": ["BlackRock Link.", "Tesouro Digital.", "Yield Seguro."],
        "cons": ["Regulação Fiat.", "Centralização."],
        "link": "https://ondo.finance/"
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo Overledger. Liga as blockchains privadas dos bancos centrais (CBDCs) à rede pública.",
        "pros": ["Supply 14.5M.", "Foco B2B.", "Interconexão."],
        "cons": ["Código Proprietário.", "Baixa Visibilidade."],
        "link": "https://www.quant.network/"
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Remessas Globais",
        "why": "Focada em pagamentos rápidos e inclusão financeira. Complemento direto ao ecossistema ISO 20022.",
        "pros": ["Taxas Nulas.", "MoneyGram Link.", "Inclusão."],
        "cons": ["Sombra do XRP.", "Marketing."],
        "link": "https://stellar.org/"
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais a nível global.",
        "pros": ["65k TPS.", "Adoção Visa.", "Taxas Baixas."],
        "cons": ["Network Uptime.", "Hardware Caro."],
        "link": "https://solana.com/"
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Hashgraph Gov",
        "why": "Governada pela Google e Dell. A infraestrutura de eleição para o setor corporativo Fortune 500.",
        "pros": ["Conselho de Elite.", "Eficiência Hashgraph.", "Seguro."],
        "cons": ["Perceção Centralizada.", "Adoção Dev."],
        "link": "https://hedera.com/"
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA E RADAR
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
                news.append({"title": entry.title, "link": entry.link, "src": src, "ts": time.mktime(entry.published_parsed)})
        except: continue
    return sorted(news, key=lambda x: x['ts'], reverse=True)

# ==============================================================================
# 05. NÓ DE CONVERGÊNCIA: HERO MATRIX
# ==============================================================================
st.markdown("""
<div class="hero-matrix">
    <div class="hero-title">JTM SOVEREIGN MATRIX</div>
    <div class="hero-subtitle">HORIZON 2030 // THE OMNIPRESENT MASTER</div>
    <p style="margin-top: 50px; font-size: 1.6rem; line-height: 2.3; color: #94a3b8; border-left: 12px solid #00d4ff; padding-left: 60px;">
        Bem-vindo ao <b>Cérebro Analítico Apex</b> da JTM Capital. Este monólito monitoriza a transição sistémica da liquidez mundial. Operamos na interseção entre a estabilidade da <b>Âncora Física</b> e a expansão da <b>Fronteira Digital</b>. Aqui, a soberania é o resultado da substituição do medo pela matemática inquebrável.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (GRELHA DINÂMICA)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> SINCRONIZAÇÃO DE VALOR GLOBAL (EUR €)</h2>", unsafe_allow_html=True)

MACRO_KEYS = {
    "GOLD": ("Ouro Físico (GC=F)", "GC=F"), "TSLA": ("Tesla IA (TSLA)", "TSLA"),
    "BCP": ("BCP Liquidez (LS)", "BCP.LS"), "VIX": ("Índice Medo (^VIX)", "^VIX"),
    "NEAR": ("Near IA (NEAR)", "NEAR-EUR"), "RNDR": ("Render IA (RNDR)", "RNDR-EUR"),
    "ALGO": ("Algorand (ALGO)", "ALGO-EUR"), "AVAX": ("Avalanche (AVAX)", "AVAX-EUR")
}

items = list(ASSET_DOCS.items()) + list(MACRO_KEYS.items())
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
                    <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (NOTÍCIAS ALINHADAS)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> MONITOR DE INTELIGÊNCIA // O PULSO</h2>", unsafe_allow_html=True)
col_radar, col_insight = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="news-monitor">', unsafe_allow_html=True)
    st.markdown("### 📡 Radar de Fluxo Global")
    radar_list = fetch_radar()
    page = st.session_state.pulse_index % (len(radar_list)//6)
    for item in radar_list[page*6 : (page+1)*6]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank" class="news-title">■ {item['title']}</a>
            <div style="color: #64748b; font-size: 0.95rem; font-family: 'JetBrains Mono';">FONTE: {item['src']} // TRANSMISSÃO AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_insight:
    st.markdown("""
    <div class="editorial-matrix" style="height: 100%; padding: 50px; border-left-color: #f59e0b; margin-top: 0;">
        <h3 style="color: #f59e0b;">CÓRTEX V.MAX: INSIGHT</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.4rem; line-height: 2.2;">
        "O sistema financeiro analógico está a sangrar liquidez. A transição para o padrão ISO 20022 está a entrar na fase de 'Settlement Crítico'. Observamos o capital inteligente a abandonar ativos de dívida para se ancorar em protocolos de infraestrutura pura. O Monólito JTM permanece imperturbável enquanto a base monetária do mundo é reescrita."
        </p>
        <p style="margin-top: 40px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">SINAL: POSICIONAMENTO GÉLIDO.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. MAPA DE POSICIONAMENTO E EDITORIAL (O PORQUÊ)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MAPA DE POSICIONAMENTO RECOMENDADO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP / OURO", "Alocação": "50%", "Justificação": "Garantia de liquidez macro."},
    {"Setor": "Autonomia & Energia", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Justificação": "Domínio IA e Energia."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO / QNT", "Alocação": "20%", "Justificação": "Reset Bancário."},
    {"Setor": "Fronteira Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Justificação": "Escassez absoluta."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(f"""
<div class="apex-table-container">
    <table class="apex-table">
        <thead>
            <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação (%)</th><th>Nota de Execução</th></tr>
        </thead>
        <tbody>
            {''.join([f"<tr><td>{r['Setor']}</td><td>{r['Ativos']}</td><td>{r['Alocação']}</td><td>{r['Justificação']}</td></tr>" for _, r in df_pos.iterrows()])}
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# EDITORIAL DE EXPLICAÇÃO COM LINKS
st.markdown("""
<div class="editorial-matrix">
    <div style="background: #00d4ff; color: #000; padding: 6px 18px; display: inline-block; font-family: 'JetBrains Mono'; font-weight: 900; border-radius: 4px; margin-bottom: 25px;">EDITORIAL V.MAX</div>
    <h3 style="color:#ffffff; margin-bottom:25px; font-size: 2.5rem;">TESE: PORQUÊ ESTA ALOCAÇÃO HOJE?</h3>
    <p style="font-size: 1.4rem; line-height: 2.2; color: #f1f5f9;">
        O mercado global está num ponto de inflexão. Com o MVRV Z-Score do Bitcoin a indicar subvalorização e o Tesouro Americano a ser tokenizado pela BlackRock via Ondo, a oportunidade é histórica. Mantemos 50% em <b>Âncora Física</b> pois o índice VIX sinaliza volatilidade iminente.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 30px;">
        <a href="https://ondo.finance/" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[ONDO FINANCE: RWA HUB]</a>
        <a href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[DOCUMENTAÇÃO ISO 20022]</a>
        <a href="https://ripple.com/" target="_blank" style="color: #00ffa3; font-weight: bold; text-decoration: none;">[SISTEMA RIPPLE / XRP]</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. DIAGRAMAS E CÓDICE TÉCNICO
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ARQUITETURA DA NOVA LIQUIDEZ</h2>", unsafe_allow_html=True)

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("### O Ciclo RWA (Real World Assets)")
    st.write("A ponte entre o mundo físico e o digital.")
    st.markdown("")

with c_img2:
    st.markdown("### A Norma ISO 20022")
    st.write("O novo sistema nervoso central dos bancos mundiais.")
    st.markdown("")

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: O PORQUÊ TÉCNICO (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE ATIVOS SOBERANOS // O PORQUÊ TÉCNICO</h2>", unsafe_allow_html=True)

asset_tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with asset_tabs[i]:
        col_txt, col_graph = st.columns([1.5, 1])
        with col_txt:
            st.markdown(f"### Função: {info['role']}")
            st.write(f"**Tese:** {info['why']}")
            st.write(f"**Tecnologia:** {info['tech']}")
            st.markdown(f"""
            <div class="apex-table-container">
                <table class="apex-table">
                    <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                    <tbody><tr>
                        <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr></tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#00ffa3;'>LER DOCUMENTAÇÃO OFICIAL →</a>", unsafe_allow_html=True)
        with col_graph:
            st.markdown("### Verificação de Rede")
            st.write("Representação visual da integridade criptográfica.")
            st.markdown(f"} blockchain network topology and security verification process]")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Digitalização da propriedade física."); st.write("**VIX:** Índice de medo institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais."); st.write("**Settlement:** Liquidação matemática final.")
with cg3:
    st.write("**Cold Storage:** Soberania via Trezor."); st.write("**Smart Contracts:** Contratos matemáticos sem intermediários.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1e293b;">MONÓLITO V36.0 // OMNIPRESENT MATRIX READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização de Ciclo
if sync_active:
    st.session_state.pulse_index += 1
    time.sleep(30)
    st.rerun()
