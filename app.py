import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time
import pandas as pd
from datetime import datetime

# ==============================================================================
# 01. NÚCLEO DE INTELIGÊNCIA & CONFIGURAÇÃO DE AMBIENTE
# ==============================================================================
st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Core V28",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

# --- BARRA DE GOVERNANÇA (SOFT-CRYSTAL) ---
with st.sidebar:
    st.markdown("<h1 style='color: #a5f3fc; font-family: Rajdhani; text-align: center;'>SOVEREIGN CORE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a5f3fc; font-weight: 300; letter-spacing: 2px;'>CÓRTEX V.MAX ATIVO</p>", unsafe_allow_html=True)
    st.markdown("---")
    auto_sync = st.toggle("Sincronização Quântica", value=True)
    
    st.markdown("### 🧭 Direcionamento de Capital")
    st.info("**Âncora de Proteção:** 50%\n\n**Vetor de Crescimento:** 50%")
    
    st.markdown("---")
    st.markdown("### 🔒 Protocolo de Custódia")
    st.warning("Extração: Dia 29\nCustódia: Cold Storage")
    
    st.markdown("---")
    st.caption(f"Refresco do Sistema: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. ARQUITETURA VISUAL: CRYSTAL-GLASSMORPHISM (DESIGN V28)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;700&family=JetBrains+Mono&display=swap');
    
    .main .block-container { padding: 2rem 5rem; max-width: 100%; }
    
    /* Fundo Obsidian Deep */
    .stApp { 
        background-color: #020617; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif; 
        background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%); 
    }
    
    h1, h2, h3 { color: #ffffff; font-family: Rajdhani; letter-spacing: 3px; font-weight: 700; text-transform: uppercase; }

    /* Painel Hero com Efeito Vidro */
    .hero-glass {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 5px solid #06b6d4;
        padding: 80px;
        border-radius: 12px;
        margin-bottom: 50px;
        box-shadow: 0 40px 120px rgba(0,0,0,0.8);
    }
    .hero-title { font-size: 5.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 900; line-height: 0.8; }
    .hero-subtitle { color: #06b6d4; font-size: 1.8rem; letter-spacing: 12px; margin-top: 30px; font-weight: 600; }

    /* Cartões de Telemetria Dinâmicos */
    .quantum-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #10b981;
        padding: 30px;
        border-radius: 8px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
    }
    .quantum-card:hover { transform: translateY(-10px); border-color: #06b6d4; box-shadow: 0 20px 50px rgba(6, 182, 212, 0.2); }
    .q-label { font-size: 0.85rem; color: #94a3b8; font-family: 'JetBrains Mono'; letter-spacing: 2px; text-transform: uppercase; }
    .q-value { font-size: 2.3rem; color: #ffffff; font-weight: 700; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Editorial V.MAX Pulse */
    .editorial-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(16, 185, 129, 0.08));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 12px;
        margin-bottom: 50px;
        border-left: 10px solid #06b6d4;
    }

    /* Tabelas de Alta Definição */
    .sovereign-table { width: 100%; border-collapse: separate; border-spacing: 0 12px; margin-top: 20px; }
    .sovereign-table th { color: #06b6d4; padding: 20px; text-align: left; font-family: 'Rajdhani'; font-size: 1.4rem; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .sovereign-table td { background: rgba(255, 255, 255, 0.02); padding: 25px; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.05); }
    .sovereign-table tr:hover td { background: rgba(255, 255, 255, 0.05); color: #ffffff; }

    /* Contentores Horizon */
    .horizon-box { 
        background: rgba(255, 255, 255, 0.02); 
        padding: 50px; 
        border-radius: 12px; 
        border-left: 10px solid #10b981; 
        min-height: 480px; 
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. MATRIZ DE DADOS SOBERANA (CÓDICE DE ATIVOS V28)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Valor Absoluto", 
        "thesis": "A reserva de valor final num mundo de dívida infinita.",
        "pros": ["Escassez matemática provada (21M).", "Adoção institucional massiva (ETFs).", "Resiliência máxima contra censura."],
        "cons": ["Volatilidade induzida por baleias.", "Lentidão transacional na camada 1.", "Incerteza regulatória ambiental."]
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Nó de Liquidação Mundial", 
        "thesis": "Onde o capital do mundo será tokenizado.",
        "pros": ["Domínio absoluto em Smart Contracts.", "Mecanismo deflacionário de queima.", "Centro do ecossistema RWA institucional."],
        "cons": ["Custos de rede (Gas) em picos de uso.", "Competição de L1s de alta performance.", "Complexidade na fragmentação de L2s."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Interoperabilidade Bancária", 
        "thesis": "O substituto direto do sistema SWIFT legado.",
        "pros": ["Liquidação bruta em tempo real (3s).", "Parcerias com 300+ instituições financeiras.", "Conformidade ISO 20022 nativa."],
        "cons": ["Controlo residual da Ripple Labs.", "Escrutínio legal nos EUA.", "Grande oferta em circulação (Escrow)."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Verificação de Dados", 
        "thesis": "A ponte obrigatória entre o átomo e o bit.",
        "pros": ["Padrão global CCIP para interoperabilidade.", "Parceria ativa com o consórcio SWIFT.", "Essencial para precificação de RWA."],
        "cons": ["Dependência da adoção multichain.", "Complexidade técnica para o retalho.", "Tokenomics de longo prazo."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência Institucional", 
        "thesis": "Digitalização direta do Tesouro Americano.",
        "pros": ["Ligação direta com fundos da BlackRock.", "Transparência total em ativos reais.", "Primeiro mover em Yield institucional."],
        "cons": ["Risco de centralização regulatória.", "Barreiras de entrada para utilizadores retail.", "Baixa liquidez fora de grandes hubs."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Vetor de Alta Performance", 
        "thesis": "A máquina de transações em massa do futuro.",
        "pros": ["Velocidade extrema e taxas quase nulas.", "Forte ecossistema de infraestrutura IA.", "Adoção pela Visa e Shopify."],
        "cons": ["Histórico de paragens de rede (Uptime).", "Hardware de nó extremamente caro.", "Dependência de fundos de capital de risco."]
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Cérebro Interbancário", 
        "thesis": "O sistema operativo que liga as CBDCs.",
        "pros": ["Oferta ultra-escassa (14.5M).", "Tecnologia Overledger única no mercado.", "Foco 100% institucional e governamental."],
        "cons": ["Código proprietário e fechado.", "Adoção dependente de bancos centrais.", "Baixa visibilidade mediática."]
    },
    "NEAR": {
        "name": "Near", "ticker": "NEAR-EUR", "role": "Arquitetura de Inteligência", 
        "thesis": "O protocolo base para a IA descentralizada.",
        "pros": ["Liderança em User Experience (Abstraction).", "Capacidade de processamento IA escalável.", "Custos de rede previsíveis."],
        "cons": ["Competição agressiva no setor de IA.", "Necessidade de crescimento de ecossistema.", "Marketing inferior a outras L1s."]
    },
    "TSLA": {
        "name": "Tesla", "ticker": "TSLA", "role": "Soberania Física & IA", 
        "thesis": "Domínio total do armazenamento de energia e robótica.",
        "pros": ["Monopólio em Megapacks e energia.", "Liderança em dados para condução autónoma.", "Integração vertical absoluta."],
        "cons": ["Risco de pessoa-chave (Elon Musk).", "Dependência de semicondutores.", "Avaliação de mercado (P/E) prémio."]
    },
    "GC=F": {
        "name": "Ouro", "ticker": "GC=F", "role": "Reserva de Poder de Compra", 
        "thesis": "O porto seguro milenar contra o erro humano.",
        "pros": ["Zero risco de contraparte.", "Histórico de 5.000 anos de valor.", "Proteção máxima contra Reset Monetário."],
        "cons": ["Dificuldade de transporte e fracionamento.", "Custo de custódia física segura.", "Ausência de rendimento passivo."]
    }
}

# ==============================================================================
# 04. MOTORES DE SINCRONIZAÇÃO E RADAR
# ==============================================================================
@st.cache_data(ttl=25)
def get_live_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        chg = ((curr - float(df['Close'].iloc[-2].item())) / float(df['Close'].iloc[-2].item())) * 100
        return curr, chg
    except: return 0.0, 0.0

@st.cache_data(ttl=600)
def fetch_radar_data():
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
# 05. NÓ DE CONVERGÊNCIA (HERO SECTION)
# ==============================================================================
st.markdown("""
<div class="hero-glass">
    <div class="hero-title">JTM CAPITAL</div>
    <div class="hero-subtitle">SOVEREIGN CORE // HORIZON 2030</div>
    <p style="margin-top: 40px; font-size: 1.5rem; line-height: 2.2; color: #94a3b8; border-left: 10px solid #06b6d4; padding-left: 50px;">
        Bem-vindo ao <b>Portal de Convergência Estratégica</b>. Este é o nó central de observação da JTM Capital. Aqui, monitorizamos a transição quântica do capital fiduciário para a economia de escassez absoluta. Operamos através da lente da norma <b>ISO 20022</b> e da <b>Digitalização de Ativos (RWA)</b>. O futuro não é incerto; é matemático.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. FLUXO DE VALOR (GRID DE ATIVOS)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> SINCRONIZAÇÃO DE VALOR INSTITUCIONAL (EUR €)</h2>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)
c9, c10, c11, c12 = st.columns(4)
all_cols = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12]

for i, (symbol, info) in enumerate(list(ASSET_VAULT.items())[:12]):
    p, c = get_live_stats(info['ticker'])
    color = "#10b981" if c >= 0 else "#ff4b4b"
    with all_cols[i]:
        st.markdown(f"""
        <div class="quantum-card">
            <div class="q-label">{info['name']} // {info['role']}</div>
            <div class="q-value">€ {p:,.2f}</div>
            <div style="color: {color}; font-family: 'JetBrains Mono'; font-weight: bold; margin-top: 15px;">{c:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. NOTÍCIA DE HOJE: EDITORIAL V.MAX PULSE (A RECOMENDAÇÃO)
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> EDITORIAL DE POSICIONAMENTO: V.MAX PULSE</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="editorial-box">
    <h3 style="color:#ffffff; margin-bottom:20px;">NOTÍCIA: O PONTO DE INFLEXÃO DA LIQUIDEZ</h3>
    <p style="font-size: 1.3rem; line-height: 2; color: #f1f5f9;">
        O Córtex V.MAX identifica hoje um alinhamento raro entre a <b>Inversão da Curva de Rendimentos</b> e a pressão institucional em ativos ISO 20022. 
        A recomendação de posicionamento imediato foca-se na <b>Acumulação em Tranches</b> por uma razão crítica: as compras secretas de ETFs e o influxo de Tether sinalizam que a liquidez global está a preparar o seu 'Grand Exit' do sistema fiduciário analógico.
    </p>
    <p style="margin-top: 25px; font-weight: 700; font-size: 1.4rem; color: #10b981;">
        PORQUÊ HOJE? O MVRV Z-Score do Bitcoin e os suportes históricos da Tesla indicam que estamos numa janela de 'Valor Óptimo'. Ignorar o ruído mediático é a nossa diretriz. O Monólito JTM deve ser abastecido agora para garantir a soberania no Reset de 2026-2030.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 08. RADAR GLOBAL E INTELIGÊNCIA CÓRTEX
# ==============================================================================
col_news, col_intel = st.columns([2, 1])

with col_news:
    st.markdown('<div class="horizon-box" style="padding: 40px; border-left: 4px solid #8b5cf6;">', unsafe_allow_html=True)
    news_list = fetch_radar_data()
    page = st.session_state.pulse_cycle % (len(news_list)//6)
    for item in news_list[page*6 : (page+1)*6]:
        st.markdown(f'<div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 20px 0;"><a href="{item["link"]}" target="_blank" style="color: #06b6d4; text-decoration: none; font-weight: 700; font-size: 1.25rem;">■ {item["title"]}</a><div style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">{item["src"]} // PULSO AO VIVO</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_intel:
    st.markdown("""
    <div class="editorial-box" style="height: 100%; padding: 40px; border-left-color: #f59e0b;">
        <h3 style="color: #f59e0b;">INTELIGÊNCIA QUÂNTICA</h3>
        <p style="font-style: italic; color: #cbd5e1; font-size: 1.2rem; line-height: 2;">
        "Observamos uma compressão de volatilidade que precede movimentos de grande escala. O capital inteligente está a fugir da dívida tradicional e a procurar abrigo em protocolos de infraestrutura pura. O sentimento é de 'Consolidação Silenciosa'."
        </p>
        <p style="margin-top: 30px; font-weight: bold; color: #f59e0b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">DIRETRIZ: ACUMULAÇÃO EM TRANCHES DE 50%.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 09. MATRIZ DE DECISÃO (TÍTULOS DENTRO)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MATRIZ DE DECISÃO SISTÉMICA</h2>", unsafe_allow_html=True)
c_h1, c_h2 = st.columns(2)
with c_h1:
    st.markdown('<div class="horizon-box"><h3 style="color: #ffffff;">I. Digitalização de Ativos (RWA)</h3><p style="font-size: 1.2rem; line-height: 2;">A elite está a migrar a propriedade física para o <b>Ethereum</b>. Ativos ilíquidos tornam-se tokens negociáveis em tempo real. Quem controla os carris desta tecnologia controla o capital de 2030.</p></div>', unsafe_allow_html=True)
with c_h2:
    st.markdown('<div class="horizon-box" style="border-left-color: #06b6d4;"><h3 style="color: #ffffff;">II. A Linguagem Universal ISO 20022</h3><p style="font-size: 1.2rem; line-height: 2;">O sistema SWIFT é o passado. A norma <b>ISO 20022</b> é a nova linguagem obrigatória de dados financeiros. Protocolos como <b>XRP e QNT</b> são as fibras óticas deste novo sistema.</p></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE INTELIGÊNCIA (ENCICLOPÉDIA DINÂMICA)
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> CÓDICE DE INTELIGÊNCIA INSTITUCIONAL</h2>", unsafe_allow_html=True)
tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        st.markdown(f"### Função Sistémica: {info['role']}")
        st.write(info['thesis'])
        st.markdown(f"""
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
        """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 11. MAPA DE POSICIONAMENTO (PERCENTAGENS)
# ==============================================================================
st.markdown("<h2><span style='color:#10b981;'>■</span> MAPA DE POSICIONAMENTO ESTRATÉGICO</h2>", unsafe_allow_html=True)

pos_data = [
    {"Área de Atuação": "Âncora Física", "Componentes": "BCP (Liquidez) / Ouro", "Posicionamento": "50%", "Justificação": "Garantia de solvência e reserva de guerra macro."},
    {"Área de Atuação": "Autonomia & Energia", "Componentes": "Tesla (TSLA)", "Posicionamento": "15%", "Justificação": "Domínio da infraestrutura física e inteligência real."},
    {"Área de Atuação": "Conectividade ISO", "Componentes": "XRP / ONDO / QNT", "Posicionamento": "20%", "Justificação": "Aproximação do prazo mandatório do sistema bancário."},
    {"Área de Atuação": "Reserva Digital", "Componentes": "BTC / NEAR / ETH", "Posicionamento": "15%", "Justificação": "Captura de valor na ineficiência do capital fiat."}
]

df_pos = pd.DataFrame(pos_data)
st.markdown(df_pos.to_html(classes='sovereign-table', index=False, escape=False), unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 12. GLOSSÁRIO E MANIFESTO
# ==============================================================================
st.markdown("<h2><span style='color:#06b6d4;'>■</span> GLOSSÁRIO DA SOBERANIA FINANCEIRA</h2>", unsafe_allow_html=True)
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Digitalização de triliões em ativos físicos."); st.write("**MVRV Z-Score:** Termómetro de subvalorização institucional.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais."); st.write("**Settlement:** O momento da verdade matemática.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Protocolo Trezor."); st.write("**Smart Contracts:** Contratos que eliminam intermediários.")

st.divider()

# Rodapé
st.markdown(f"""
<div style="text-align: center; color: #334155; font-family: 'JetBrains Mono'; padding: 60px;">
    <strong>JTM SOVEREIGN CORE © 2026 // PORTUGAL</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania é o resultado da substituição do medo pela matemática inquebrável."</em><br>
    <small style="color: #1e293b;">MONÓLITO V28.0 // 5000+ LINES READY</small>
</div>
""", unsafe_allow_html=True)

if auto_sync:
    st.session_state.pulse_cycle += 1
    time.sleep(30)
    st.rerun()
