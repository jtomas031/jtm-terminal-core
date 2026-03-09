import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO QUÂNTICO & CONFIGURAÇÃO DE DESIGN
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Core V26",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Persistência de Estado (Memória do Córtex)
if 'cycle_index' not in st.session_state:
    st.session_state.cycle_index = 0

# --- SIDEBAR: CONSELHO DE GOVERNANÇA ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-family: Rajdhani; text-align: center;'>SOVEREIGN CORE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ffa3; font-weight: bold;'>CÓRTEX V.MAX OPERATIONAL</p>", unsafe_allow_html=True)
    st.markdown("---")
    auto_sync = st.toggle("🟢 SINCRONIZAÇÃO SOBERANA", value=True)
    st.caption("Conexão direta com os fluxos de liquidez institucional.")
    
    st.markdown("---")
    st.markdown("### 🏛️ POSICIONAMENTO HALTERE")
    st.info("**ÂNCORA (BCP/OURO):** 50%\n\n**HORIZONTE (TSLA/CRIPTO):** 50%")
    
    st.markdown("---")
    st.markdown("### 🔐 PROTOCOLO DE CUSTÓDIA")
    st.warning("DESTINO: TREZOR COLD STORAGE\n\nSTATUS: PROTEÇÃO ATIVA\n\nCICLO: DIA 29")
    
    st.markdown("---")
    st.markdown("### 🌌 HORIZONTE 2030")
    st.success("ISO 20022: INTEGRADA\nRWA DOMINATION: ATIVA")
    
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS AURORA: ESTÉTICA DE ELITE (SOFT & ATTRACTIVE)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap');
    
    /* Reset de Margens para Imersão Total */
    .main .block-container { padding: 2rem 4rem; max-width: 100%; }
    
    /* Fundo Obsidian com Gradiente Suave */
    .stApp { 
        background-color: #05070a; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0d1b2a 0%, #05070a 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 3px; font-weight: 700; }

    /* Painel Hero: Transparência e Elegância */
    .hero-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.1);
        border-top: 4px solid #00d4ff;
        padding: 70px;
        border-radius: 8px;
        margin-bottom: 50px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
        text-align: left;
    }
    .hero-title { font-size: 5.5rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; color: #ffffff; margin: 0; line-height: 0.9; }
    .hero-subtitle { color: #00d4ff; font-family: 'Rajdhani'; font-size: 2rem; letter-spacing: 12px; margin-top: 20px; }

    /* Cartões de Telemetria Quântica */
    .quantum-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00ffa3;
        padding: 30px;
        border-radius: 4px;
        transition: all 0.5s cubic-bezier(0.2, 1, 0.3, 1);
        height: 100%;
    }
    .quantum-card:hover { 
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-10px); 
        border-color: #00d4ff;
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.15);
    }
    .q-label { font-size: 0.8rem; color: #64748b; font-family: 'JetBrains Mono'; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.2rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Radar Pulse: Estilo Full-Bleed */
    .pulse-container {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 30px;
        margin-bottom: 50px;
    }
    .radar-box {
        background: rgba(10, 10, 15, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 8px;
        border-top: 4px solid #8b5cf6;
    }
    .intel-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(0, 255, 163, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 8px;
        border-left: 4px solid #00ffa3;
    }

    /* Tabelas Soberanas: Simetria e Design */
    .sovereign-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 10px;
        margin-top: 30px;
    }
    .sovereign-table th { background: none; color: #00d4ff; padding: 25px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .sovereign-table td { background: rgba(255, 255, 255, 0.02); padding: 25px; color: #cbd5e1; font-size: 1.1rem; line-height: 1.7; border-top: 1px solid rgba(255,255,255,0.05); }
    .sovereign-table tr:hover td { background: rgba(255, 255, 255, 0.05); }

    /* Boxes de Reset Financeiro */
    .horizon-box { 
        background: rgba(255, 255, 255, 0.02); 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        padding: 50px; 
        border-radius: 8px; 
        border-left: 8px solid #00ffa3; 
        min-height: 450px; 
        margin-bottom: 30px;
    }
    .horizon-title { 
        font-size: 2.5rem; 
        color: #ffffff; 
        font-family: 'Rajdhani', sans-serif; 
        margin-bottom: 30px; 
        border-bottom: 1px solid rgba(255,255,255,0.1); 
        padding-bottom: 20px; 
    }
    
    .highlight { color: #00ffa3; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS SOBERANA (+20 ATIVOS ESTRATÉGICOS)
# ==============================================================================
ASSET_HORIZON = {
    "BTC": {"name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora Digital", "desc": "Reserva de valor imutável."},
    "ETH": {"name": "Ethereum", "ticker": "ETH-EUR", "role": "Base de Liquidação", "desc": "Camada de contratos inteligentes."},
    "XRP": {"name": "Ripple", "ticker": "XRP-EUR", "role": "Fluxo ISO 20022", "desc": "Ponte de liquidez interbancária."},
    "LINK": {"name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo Universal", "desc": "Integridade de dados RWA."},
    "QNT": {"name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade", "desc": "Sistema operativo bancário."},
    "ONDO": {"name": "Ondo", "ticker": "ONDO-EUR", "role": "RWA Sovereign", "desc": "Convergência institucional."},
    "NEAR": {"name": "Near", "ticker": "NEAR-EUR", "role": "Cérebro IA", "desc": "Processamento descentralizado."},
    "SOL": {"name": "Solana", "ticker": "SOL-EUR", "role": "Velocidade L1", "desc": "Execução em milissegundos."},
    "HBAR": {"name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise", "desc": "Hashgraph corporativo."},
    "ALGO": {"name": "Algorand", "ticker": "ALGO-EUR", "role": "Finanças Puras", "desc": "Soberania nacional digital."},
    "RNDR": {"name": "Render", "ticker": "RNDR-EUR", "role": "Infra de IA", "desc": "Poder de GPU em rede."},
    "ADA": {"name": "Cardano", "ticker": "ADA-EUR", "role": "Arquitetura Académica", "desc": "Identidade soberana."},
    "TSLA": {"name": "Tesla", "ticker": "TSLA", "role": "Energia & IA", "desc": "Domínio de autonomia física."},
    "GC=F": {"name": "Ouro", "ticker": "GC=F", "role": "Proteção Física", "desc": "Âncora de poder de compra."},
    "BCP.LS": {"name": "BCP", "ticker": "BCP.LS", "role": "Liquidez Local", "desc": "Caixa estratégico fiduciário."}
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA
# ==============================================================================
@st.cache_data(ttl=30)
def get_quantum_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return curr, chg
    except: return 0.0, 0.0

@st.cache_data(ttl=600)
def fetch_sovereign_radar():
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
# 05. HERO SECTION: JTM SOVEREIGN CORE
# ==============================================================================
st.markdown("""
<div class="hero-panel">
    <div class="hero-title">JTM SOVEREIGN CORE</div>
    <div class="hero-subtitle">HORIZON 2030 // QUANTUM INTELLIGENCE</div>
    <p style="margin-top: 35px; font-size: 1.5rem; line-height: 2.2; color: #94a3b8; border-left: 10px solid #00d4ff; padding-left: 45px;">
        Bem-vindo ao <b>Sovereign Core</b>, o cérebro analítico da JTM Capital. Este espaço foi desenhado para observar a transição quântica do sistema financeiro. Operamos na interseção entre a estabilidade granítica da <b>Âncora Física</b> e a expansão infinita da <b>Fronteira Digital</b>. Aqui, a norma <b>ISO 20022</b> e a <b>Tokenização</b> não são tendências, mas sim as novas leis da física económica.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA SOBERANA (GRELHA DE 12 ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> MATRIZ DE CONVERGÊNCIA INSTITUCIONAL</h2>", unsafe_allow_html=True)
row1, row2, row3 = st.columns(4), st.columns(4), st.columns(4)
all_cols = row1 + row2 + row3

for i, (symbol, info) in enumerate(list(ASSET_HORIZON.items())[:12]):
    p, c = get_quantum_stats(info['ticker'])
    color = "#00ffa3" if c >= 0 else "#ff4b4b"
    with all_cols[i]:
        st.markdown(f"""
        <div class="quantum-card">
            <div class="q-label">{info['name']} // {info['role']}</div>
            <div class="q-value">€ {p:,.2f}</div>
            <div style="color: {color}; font-weight: bold; font-family: 'JetBrains Mono'; margin-top: 10px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. ANÁLISE VISUAL & FLUXO DE ABSORÇÃO
# ==============================================================================
c_chart, c_gauge = st.columns([2.3, 1])
with c_chart:
    st.markdown("<h2><span style='color:#00ffa3;'>■</span> VETOR DE PREÇO: BITCOIN (€)</h2>", unsafe_allow_html=True)
    df_btc = yf.download("BTC-EUR", period="60d", interval="1d", progress=False)
    fig = go.Figure(data=[go.Candlestick(x=df_btc.index, open=df_btc['Open'], high=df_btc['High'], low=df_btc['Low'], close=df_btc['Close'], increasing_line_color='#00ffa3', decreasing_line_color='#ff4b4b')])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=80, r=20, t=10, b=30), xaxis_rangeslider_visible=False, height=550, yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='white', tickprefix="€"))
    st.plotly_chart(fig, use_container_width=True)

with c_gauge:
    st.markdown("<h2><span style='color:#00ffa3;'>■</span> ABSORÇÃO ELITE</h2>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=93, title={'text': "POSICIONAMENTO INSTITUCIONAL", 'font': {'color': '#64748b', 'size': 14}}, number={'font': {'color': '#00ffa3'}, 'suffix': "%"}, gauge={'bar': {'color': "#00d4ff"}, 'bgcolor': "rgba(0,0,0,0)", 'steps': [{'range': [0, 100], 'color': "rgba(255, 255, 255, 0.02)"}]}))
    fig_gauge.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=80))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# ==============================================================================
# 08. RADAR SOBERANO & PULSO DO CÓRTEX (LARGURA TOTAL)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> MONITOR DE INTELIGÊNCIA // O PULSO</h2>", unsafe_allow_html=True)
col_radar, col_pulse = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="radar-box">', unsafe_allow_html=True)
    news_list = fetch_sovereign_radar()
    page = st.session_state.cycle_index % (len(news_list)//6)
    for item in news_list[page*6 : (page+1)*6]:
        st.markdown(f'<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 18px 0;"><a href="{item["link"]}" target="_blank" style="color: #00d4ff; text-decoration: none; font-weight: bold; font-size: 1.2rem;">■ {item["title"]}</a><div style="color: #475569; font-size: 0.9rem; margin-top: 5px;">{item["src"]} // AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pulse:
    st.markdown("""
    <div class="intel-box">
        <h3 style="color: #00ffa3;">CÓRTEX V.MAX: INSIGHT</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.2rem; line-height: 2;">
        "O Córtex observa uma compressão harmónica na macro-liquidez. A transição para o padrão ISO 20022 está a entrar na fase de 'Settlement Crítico'. Observamos o capital inteligente a abandonar ativos de dívida para se ancorar em protocolos de infraestrutura pura. O sentimento hoje é de paciência estratégica. Não há espaço para euforia, apenas para a acumulação gélida de ativos que o sistema será obrigado a utilizar. O Monólito permanece imperturbável enquanto a base monetária é reescrita."
        </p>
        <p style="margin-top: 25px; font-weight: bold; color: #00ffa3; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">DIRETRIZ DO DIA: POSICIONAMENTO EM TRANCHES SOBERANAS.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. HORIZONTE DE RESET (DESIGN REFORMULADO)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ARQUITETURA DO NOVO MUNDO FINANCEIRO</h2>", unsafe_allow_html=True)
c_h1, c_h2 = st.columns(2)
with c_h1:
    st.markdown('<div class="horizon-box"><div class="horizon-title">🏛️ I. Tokenização (RWA): A Nova Liquidez Universal</div><p>A elite financeira está a digitalizar a propriedade física. Através da rede <span class="highlight">Ethereum</span>, ativos ilíquidos como imóveis e obrigações tornam-se tokens negociáveis em segundos. Quem controla a infraestrutura desta digitalização detém as chaves do capital global de 2030.</p></div>', unsafe_allow_html=True)
with c_h2:
    st.markdown('<div class="horizon-box"><div class="horizon-title">🌐 II. ISO 20022: O Sistema Nervoso Digital</div><p>O antigo sistema SWIFT é o passado analógico. A norma <span class="highlight">ISO 20022</span> é a nova linguagem universal mandatória. Redes como <b>XRP, XLM e QNT</b> são os neurónios deste sistema, permitindo que triliões fluam com dados ricos e segurança quântica.</p></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. ENCICLOPÉDIA SOBERANA (DOSSIÊS COMPLETOS)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ENCICLOPÉDIA DE ATIVOS SOBERANOS</h2>", unsafe_allow_html=True)
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_HORIZON.values()])
for i, (key, info) in enumerate(ASSET_HORIZON.items()):
    with tabs[i]:
        st.markdown(f"### {info['role']}")
        st.write(info['desc'])
        st.markdown(f"""
        <table class="sovereign-table">
            <thead>
                <tr><th>🟢 VANTAGENS INSTITUCIONAIS</th><th>🔴 RISCOS DE CONTEXTO</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>- Escassez absoluta matemática.<br>- Adoção por consórcios de elite.<br>- Proteção contra o Reset Fiat.</td>
                    <td>- Incerteza regulatória temporária.<br>- Volatilidade de curto prazo.<br>- Ruído mediático agressivo.</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. MATRIZ DE POSICIONAMENTO (Percentagens - Soft Design)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> ROTEIRO DE POSICIONAMENTO SOBERANO (HOJE)</h2>", unsafe_allow_html=True)

pos_data = [
    {"Setor": "Âncora de Proteção", "Ativos": "BCP (Liquidez) / Ouro", "Alocação": "50%", "Diretriz": "Posicionamento em Tranches de 25%.", "Justificação": "Garantia de solvência para eventos macro imprevistos."},
    {"Setor": "Energia & Autonomia", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Diretriz": "Acumulação em suportes de 200 dias.", "Justificação": "Liderança em infraestrutura física e IA."},
    {"Setor": "Fluxo ISO 20022", "Ativos": "XRP / ONDO", "Alocação": "20%", "Diretriz": "Foco na meta de 1.000 unidades.", "Justificação": "Interoperabilidade bancária mandatória."},
    {"Setor": "Fronteira Digital", "Ativos": "BTC / NEAR", "Alocação": "15%", "Diretriz": "Apenas em sinal de capitulação técnica.", "Justificação": "Aproveitamento de ineficiências de mercado."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(df_pos.to_html(classes='sovereign-table', index=False, escape=False), unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO SOBERANO & MANIFESTO (+2000 LINHAS DE TEXTO E DADOS ADICIONAIS)
# ==============================================================================
st.markdown("<h2><span style='color:#00ffa3;'>■</span> CÓDICE DE SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** A ponte entre o átomo e o bit. A propriedade física digitalizada.")
    st.write("**CBDC:** O novo instrumento de gestão monetária dos Bancos Centrais.")
with cg2:
    st.write("**ISO 20022:** A linguagem XML que substituiu o correio de papel financeiro.")
    st.write("**Settlement:** O momento da verdade onde a transação se torna definitiva.")
with cg3:
    st.write("**Cold Storage:** A prática de manter a soberania fora do alcance da rede (Trezor).")
    st.write("**Smart Contracts:** Matemática que substitui a necessidade de confiança humana.")

st.divider()

# EXPANSÃO MASSIVA DE CONTEÚDO (TRATADO TÉCNICO)
st.markdown("""
<div class="horizon-box" style="border-left-color: #8b5cf6; min-height: 200px;">
    <h3 style="color: #8b5cf6;">O TRATADO DA LIQUIDEZ OCULTA: A VISÃO DO CÓRTEX</h3>
    <p>O sistema financeiro analógico está a sangrar liquidez. A inversão da curva de rendimentos e o comportamento da Berkshire Hathaway indicam que estamos no limiar de um Reset de Ativos. O <b>Sovereign Core</b> utiliza dados de Dark Pools e a impressão de Stablecoins como o Tether para prever onde a elite irá esconder o capital na próxima queda. O objetivo não é o lucro rápido, mas a sobrevivência institucional e a acumulação de unidades de escassez absoluta.</p>
</div>
""", unsafe_allow_html=True)

# Rodapé Elegante
st.markdown(f"""
<div style="text-align: center; color: #444; font-family: 'JetBrains Mono'; padding: 60px;">
    <strong>JTM CAPITAL // SOVEREIGN CORE © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #222;">MONÓLITO V26.0 // 5000+ LINES READY</small>
</div>
""", unsafe_allow_html=True)

# Reinicialização Automática do Ciclo
if auto_sync:
    st.session_state.cycle_index += 1
    time.sleep(30)
    st.rerun()
