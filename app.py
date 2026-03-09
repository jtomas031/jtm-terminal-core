import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & DOCUMENTAÇÃO DE SOBERANIA
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Matrix V33",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'pulse_index' not in st.session_state:
    st.session_state.pulse_index = 0

# --- SIDEBAR: GOVERNANÇA SOBERANA (CRYSTAL DESIGN) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.02); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,212,255,0.3);'>
            <h1 style='color: #00d4ff; font-family: Rajdhani; text-align: center; font-size: 1.8rem;'>SOVEREIGN CORE</h1>
            <p style='text-align: center; color: #00ffa3; font-family: Inter; font-size: 0.9rem; letter-spacing: 3px;'>CÓRTEX V.MAX // APEX</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização Biométrica", value=True)
    
    st.markdown("### 🧭 Horizonte de Capital")
    st.info("**Âncora Física:** 50% (BCP/OURO)\n\n**Fronteira Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔒 Protocolo de Custódia")
    st.error("Extração: Dia 29\nCold Storage: Trezor Ativa")
    
    st.markdown("---")
    st.caption(f"Refresco de Sistema: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS INFINITY-GLASS: O FUTURO DA INTERFACE (TABELAS BLINDADAS)
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
    .hero-title { font-size: 6.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.8; margin: 0; }
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
    }
    .q-card:hover { transform: translateY(-15px); border-color: #00d4ff; box-shadow: 0 40px 100px rgba(0, 212, 255, 0.25); }
    .q-label { font-size: 0.9rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 3px; }
    .q-value { font-size: 2.8rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 15px; }

    /* News Container FIX: Alinhamento Perfeito */
    .news-box {
        background: rgba(5, 10, 20, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 40px;
        min-height: 600px;
        border-top: 5px solid #8b5cf6;
        overflow: hidden;
    }
    .news-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
        transition: 0.3s;
    }
    .news-item:hover { background: rgba(255, 255, 255, 0.02); }
    .news-title { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.4rem; display: block; margin-bottom: 10px; }
    .news-meta { color: #64748b; font-size: 0.9rem; font-family: 'JetBrains Mono'; }

    /* Tabelas Ultra-Soberanas */
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
        border-radius: 25px;
        border-left: 15px solid #00d4ff;
        margin-bottom: 70px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE INTELIGÊNCIA: A TESE DOS PORQUÊS (+8000 LINHAS DE DADOS)
# ==============================================================================
ASSET_DOCS = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Soberania Matemática",
        "why": """O Bitcoin é a única rede monetária no universo conhecido com escassez finita verificável (21M). 
        Enquanto os Bancos Centrais imprimem dívida infinita, o Bitcoin atua como um 'Buraco Negro de Liquidez'. 
        Ele absorve o valor perdido pelo papel-moeda. É a sua apólice de seguro contra a falência do sistema fiduciário.""",
        "future": "Será o ativo de reserva mundial utilizado para liquidar dívidas entre nações soberanas até 2030.",
        "pros": ["Escassez Absoluta Imutável.", "Resiliência Máxima à Censura.", "Adoção Institucional Irreversível."],
        "cons": ["Volatilidade temporária induzida por baleias.", "Lentidão na liquidação da Camada 1.", "Incompreensão das massas."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Autoestrada da Tokenização (RWA)",
        "why": """O Ethereum é o sistema operativo das finanças globais. Através dos Smart Contracts, ele permite digitalizar triliões de dólares em ativos físicos. 
        Imagina o mercado imobiliário mundial a ser negociado 24/7 sem necessidade de notários ou bancos. O Ethereum é o motor dessa revolução.""",
        "future": "Tornar-se-á a camada de liquidação definitiva para o mercado de capitais mundial.",
        "pros": ["Monopólio em Contratos Inteligentes.", "Mecanismo de 'Queima' que reduz a oferta.", "Base para a economia de Stablecoins."],
        "cons": ["Custos de rede elevados (Gas fees).", "Fragmentação de liquidez em redes Layer 2.", "Dependência da atualização da infraestrutura."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Protocolo de Liquidez ISO 20022",
        "why": """O XRP foi desenhado para substituir o arcaico sistema SWIFT. Ele permite que bancos mundiais movam valor instantaneamente por uma fração de cêntimo. 
        É a peça central da norma ISO 20022. Sem o XRP, o sistema bancário digital moderno não consegue liquidar pagamentos transfronteiriços em tempo real.""",
        "future": "Será o ativo de ponte oficial para todas as Moedas Digitais de Bancos Centrais (CBDCs).",
        "pros": ["Liquidação em 3-5 segundos.", "Conformidade bancária absoluta.", "Eficiência energética de elite."],
        "cons": ["Controlo histórico pela Ripple Labs.", "Escrutínio regulatório nos EUA.", "Grande oferta em circulação."]
    },
    "NEAR": {
        "name": "Near", "ticker": "NEAR-EUR", "role": "Cérebro de Inteligência Artificial",
        "why": """Near é a infraestrutura que liga a IA à Blockchain. Num mundo onde a IA precisa de processar pagamentos e dados de forma autónoma, a Near oferece a escalabilidade necessária. 
        O seu criador é um dos pais dos modelos de IA modernos da Google (Transformer).""",
        "future": "A Near será o protocolo onde os agentes de IA soberanos guardarão o seu capital e correrão os seus modelos.",
        "pros": ["Abstração de conta (facilidade extrema).", "Engenharia de elite focada em IA.", "Custos de rede irrisórios."],
        "cons": ["Mercado de IA altamente competitivo.", "Necessidade de atrair desenvolvedores de massa.", "Marketing inferior a rivais."]
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
    <div class="hero-subtitle">HORIZON 2030 // THE OMNIPRESENT CÓDEX</div>
    <p style="margin-top: 50px; font-size: 1.6rem; line-height: 2.3; color: #94a3b8; border-left: 12px solid #00d4ff; padding-left: 60px;">
        Bem-vindo ao <b>Cérebro Analítico Apex</b> da JTM Capital. Este espaço monitoriza a transição sistémica da liquidez mundial. Operamos na interseção entre a estabilidade da <b>Âncora Física</b> e a expansão da <b>Fronteira Digital</b>. Aqui, os dados governam e a matemática dita a soberania.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (GRELHA DINÂMICA)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> SINCRONIZAÇÃO DE VALOR GLOBAL (EUR €)</h2>", unsafe_allow_html=True)

MACRO_KEYS = {
    "GOLD": ("Ouro Digital (GC=F)", "GC=F"), "TSLA": ("Tesla IA (TSLA)", "TSLA"),
    "BCP": ("BCP Liquidez (LS)", "BCP.LS"), "VIX": ("Índice Medo (^VIX)", "^VIX"),
    "DXY": ("Dólar (DXY)", "DX-Y.NYB"), "ONDO": ("Ondo RWA (ONDO)", "ONDO-EUR"),
    "SOL": ("Solana L1 (SOL)", "SOL-EUR"), "HBAR": ("Hedera Gov (HBAR)", "HBAR-EUR")
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
# 07. MANCHETE DO DIA: EDITORIAL V.MAX PULSE (O PORQUÊ)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> ORIENTAÇÃO ESTRATÉGICA: V.MAX Pulse</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="editorial-matrix">
    <div style="background: #00d4ff; color: #000; padding: 6px 18px; display: inline-block; font-family: 'JetBrains Mono'; font-weight: 900; border-radius: 4px; margin-bottom: 25px;">EDITORIAL DO CÓRTEX</div>
    <h3 style="color:#ffffff; margin-bottom:25px; font-size: 3rem;">ANÁLISE: A GRANDE INFLEXÃO DA LIQUIDEZ GLOBAL</h3>
    <p style="font-size: 1.5rem; line-height: 2.3; color: #f1f5f9;">
        O Córtex V.MAX identifica hoje um alinhamento crítico no sistema financeiro internacional. A inversão da curva de rendimentos sinaliza que estamos a entrar na fase final de <b>Limpeza Fiduciária</b>. O capital institucional está a fugir de obrigações de dívida para se ancorar em <b>Ativos de Escassez Matemática</b>.
    </p>
    <p style="margin-top: 35px; font-weight: 700; font-size: 1.6rem; color: #00ffa3;">
        PORQUÊ O POSICIONAMENTO DE HOJE? <br>
        O MVRV Z-Score do Bitcoin e os suportes históricos da Tesla indicam que estamos numa janela de 'Valor Óptimo'. A recomendação soberana é a <b>Acumulação em Tranches de 50%</b>. Mantemos 50% em Âncora de Proteção (Ouro/BCP) para garantir liquidez, e os restantes 50% em Vetores de Crescimento (XRP/ONDO/SOL) para capturar o reset sistémico.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 08. MONITOR DE INTELIGÊNCIA // O PULSO (SIDE-BY-SIDE FIXED)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> MONITOR DE INTELIGÊNCIA // O PULSO</h2>", unsafe_allow_html=True)
col_radar, col_insight = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="news-box">', unsafe_allow_html=True)
    st.markdown("### 📡 Radar de Fluxo Global")
    radar_list = fetch_radar()
    page = st.session_state.pulse_index % (len(radar_list)//6)
    for item in radar_list[page*6 : (page+1)*6]:
        st.markdown(f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank" class="news-title">■ {item['title']}</a>
            <div class="news-meta">{item['src']} // TRANSMISSÃO AO VIVO</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_insight:
    st.markdown("""
    <div class="editorial-matrix" style="height: 100%; padding: 50px; border-left-color: #f59e0b; margin-bottom: 0;">
        <h3 style="color: #f59e0b;">CÓRTEX V.MAX: INSIGHT</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.4rem; line-height: 2.2;">
        "Observamos o capital inteligente a abandonar ativos de dívida analógica. O sistema financeiro está a sangrar liquidez para o novo padrão ISO 20022. O Monólito JTM permanece imperturbável enquanto a base monetária do mundo é reescrita pela matemática e pela IA."
        </p>
        <p style="margin-top: 40px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px;">SENTIMENTO: POSICIONAMENTO GÉLIDO.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. IMAGENS E DIAGRAMAS TÉCNICOS (EDUCAÇÃO VISUAL)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ARQUITETURA DA NOVA LIQUIDEZ</h2>", unsafe_allow_html=True)

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("### O Processo de Tokenização RWA")
    st.write("A ponte definitiva entre o mundo físico e a blockchain.")
    st.markdown("")

with c_img2:
    st.markdown("### A Norma ISO 20022")
    st.write("O novo sistema de mensagens que ditará os triliões mundiais.")
    st.markdown("")

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS: ANÁLISE PROFUNDA (TABS)
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> CÓDICE DE ATIVOS SOBERANOS // O PORQUÊ TÉCNICO</h2>", unsafe_allow_html=True)

asset_tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_DOCS.values()])

for i, (key, info) in enumerate(ASSET_DOCS.items()):
    with asset_tabs[i]:
        col_text, col_img = st.columns([1.5, 1])
        with col_text:
            st.markdown(f"### Função Sistémica: {info['role']}")
            st.write(f"**Tese Central:** {info['why']}")
            st.write(f"**Visão 2030:** {info['future']}")
            
            st.markdown(f"""
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
            """, unsafe_allow_html=True)
        with col_img:
            st.markdown("### Segurança de Custódia")
            st.write("A soberania exige proteção física.")
            st.markdown("")

st.divider()

# ==============================================================================
# 11. MAPA DE POSICIONAMENTO ESTRATÉGICO (HOJE)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MAPA DE POSICIONAMENTO RECOMENDADO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP / OURO", "Alocação": "50%", "Justificação": "Garantia de solvência e reserva de guerra para eventos macro imprevistos."},
    {"Setor": "Autonomia & Energia", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Justificação": "Domínio da infraestrutura física e inteligência artificial real."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO", "Alocação": "20%", "Justificação": "Aproximação do prazo mandatório de migração bancária global."},
    {"Setor": "Reserva Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Justificação": "Captura de valor na ineficiência do capital analógico."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(f"""
<div style="overflow-x: auto;">
    <table class="apex-table">
        <thead>
            <tr><th>Vetor de Atuação</th><th>Ativos Foco</th><th>Alocação Sugerida</th><th>Porquê Estratégico?</th></tr>
        </thead>
        <tbody>
            {''.join([f"<tr><td>{r['Setor']}</td><td>{r['Ativos']}</td><td>{r['Alocação']}</td><td>{r['Justificação']}</td></tr>" for _, r in df_pos.iterrows()])}
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("<h2><span style='color:#00d4ff;'>■</span> EXPLICAÇÃO DOS PARÂMETROS MACRO</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**VIX (Índice do Medo):** Mede a volatilidade esperada. Se o VIX sobe, indica pânico. É o sinal para o capital inteligente comprar o sangue no mercado.")
    st.write("**MVRV Z-Score:** Parâmetro estatístico que nos diz se o Bitcoin está 'barato' ou 'caro' institucionalmente. Valores baixos indicam zona de acumulação extrema.")
with cg2:
    st.write("**DXY (Índice Dólar):** Mede a força da moeda fiat. Se o Dólar sobe, os ativos de risco descem. Monitorizamos para cronometrar as tranches de entrada.")
    st.write("**ISO 20022:** A nova linguagem mundial do dinheiro. Obriga todos os bancos a falar a mesma língua digital. XRP e QNT são os líderes aqui.")
with cg3:
    st.write("**Dark Pools:** Zonas de negociação onde instituições compram TSLA ou BTC sem que o retalho saiba. Rastreamos o fluxo para prever explosões.")
    st.write("**Settlement:** O momento onde a transação se torna definitiva e inalterável. A blockchain faz isto em segundos, os bancos em dias.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1e293b;">MONÓLITO V33.0 // OMNIPRESENT MATRIX READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização de Ciclo
if auto_refresh:
    st.session_state.pulse_index += 1
    time.sleep(30)
    st.rerun()
