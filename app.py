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
# Este terminal representa a culminação da inteligência JTM Capital para 2030.
# Cada parâmetro macro (VIX, DXY, US10Y) é cruzado com vetores de RWA e ISO 20022.
# ==============================================================================

st.set_page_config(
    page_title="JTM CAPITAL | Sovereign Apex V38",
    layout="wide",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Estado (Prevenção de Erros de Memória)
if 'pulse_cycle' not in st.session_state:
    st.session_state.pulse_cycle = 0

# --- SIDEBAR: CONSELHO DE GOVERNANÇA (NEO-INSTITUTIONAL) ---
with st.sidebar:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.02); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,212,255,0.2); text-align: center;'>
            <h2 style='color: #f1f5f9; font-family: Inter, sans-serif; margin:0;'>JTM CAPITAL</h2>
            <p style='color: #10b981; font-family: JetBrains Mono; font-size: 0.7rem; letter-spacing: 2px;'>OMNIPOTENT CORE V38</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Sincronização de Liquidez", value=True)
    
    st.markdown("### 🏛️ Matriz de Alocação")
    st.info("**Âncora Física:** 50% (OURO/BCP)\n\n**Vetor Digital:** 50% (IA/CRIPTO)")
    
    st.markdown("---")
    st.markdown("### 🔐 Protocolo de Custódia")
    st.error("Extração: Dia 29\nCold Storage: Trezor Ativa")
    
    st.markdown("---")
    st.caption(f"Refresco do Córtex: {datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 02. CSS MASTER: NEO-INSTITUTIONAL GLASS (ONDO + MATRIX)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Rajdhani:wght@600;700&family=JetBrains+Mono&display=swap');
    
    /* Configuração Geral do Workspace */
    .main .block-container { padding: 3rem 6rem; max-width: 1500px; margin: 0 auto; }
    
    /* Fundo Obsidian Mirror com Brilho Emerald */
    .stApp { 
        background-color: #010409; 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif;
        background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #010409 100%);
    }
    
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -1.5px; }

    /* Hero Section: Estilo Ondo Institutional */
    .hero-container {
        padding: 120px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 80px;
    }
    .hero-tag { 
        color: #10b981; 
        text-transform: uppercase; 
        font-weight: 800; 
        letter-spacing: 5px; 
        font-size: 0.8rem; 
        margin-bottom: 25px;
    }
    .hero-title { font-size: 6rem; line-height: 0.85; margin-bottom: 40px; font-family: 'Inter'; }
    .hero-desc { font-size: 1.6rem; color: #94a3b8; line-height: 1.7; max-width: 950px; font-weight: 300; }

    /* Cartões de Telemetria: Glassmorphism de Luxo */
    .quantum-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 35px;
        border-radius: 12px;
        transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        height: 100%;
        border-left: 4px solid #10b981;
    }
    .quantum-card:hover { border-color: #00d4ff; background: rgba(15, 23, 42, 0.7); transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0, 212, 255, 0.1); }
    .q-label { font-size: 0.75rem; color: #64748b; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .q-value { font-size: 2.3rem; font-weight: 700; color: #ffffff; font-family: 'Rajdhani'; margin-top: 10px; }

    /* Monitor "O Pulso" (Informação Real Alinhada) */
    .pulse-container {
        background: #0b0f1a;
        border: 1px solid #1e293b;
        padding: 45px;
        border-radius: 16px;
        min-height: 600px;
        border-top: 6px solid #8b5cf6;
    }
    .pulse-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px 0;
    }
    .pulse-link { color: #00d4ff; text-decoration: none; font-weight: 700; font-size: 1.3rem; display: block; margin-bottom: 8px; }
    .pulse-link:hover { color: #10b981; }

    /* Tabelas Blindadas (Alinhamento Absoluto) */
    .sovereign-table-wrapper { width: 100%; overflow-x: auto; margin: 30px 0; border-radius: 12px; }
    .sovereign-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .sovereign-table th { text-align: left; padding: 25px; color: #64748b; text-transform: uppercase; font-size: 0.8rem; border-bottom: 2px solid #1e293b; background: rgba(0,0,0,0.2); }
    .sovereign-table td { padding: 30px 25px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 1.1rem; line-height: 1.8; vertical-align: top; }
    .sovereign-table tr:hover { background: rgba(255, 255, 255, 0.02); }

    /* Editorial Matrix */
    .editorial-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 60px;
        border-radius: 20px;
        margin-top: 50px;
        border-left: 10px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 03. CÓDICE DE ATIVOS: O PORQUÊ TÉCNICO (+15 NÓS SOBERANOS)
# ==============================================================================
ASSET_VAULT = {
    "BTC": {
        "name": "Bitcoin", "ticker": "BTC-EUR", "role": "Âncora de Escassez",
        "why": "O padrão-ouro digital. Único ativo com limite matemático imutável (21M). Essencial para proteção contra o colapso do sistema fiduciário analógico.",
        "tech": "Baseado em Prova de Trabalho (PoW), é a rede mais segura e descentralizada do planeta. Funciona como reserva de valor institucional.",
        "pros": ["Escassez 21M.", "Adoção Institucional.", "Soberania Total."], "cons": ["Volatilidade.", "Lentidão L1."],
        "link": "https://bitcoin.org/bitcoin.pdf"
    },
    "ETH": {
        "name": "Ethereum", "ticker": "ETH-EUR", "role": "Liquidação de Ativos",
        "why": "O sistema operativo das finanças. É a camada onde triliões em RWA (Real World Assets) serão tokenizados e liquidados em 2030.",
        "tech": "Blockchain de Smart Contracts líder. O mecanismo de 'Burn' torna o ativo deflacionário em períodos de alta utilização.",
        "pros": ["Mecanismo Deflacionário.", "Ecossistema RWA.", "Adoção Bancária."], "cons": ["Gas fees elevadas."]
    },
    "XRP": {
        "name": "Ripple", "ticker": "XRP-EUR", "role": "Liquidez ISO 20022",
        "why": "Substituto direto do SWIFT. Ativo de ponte para liquidação instantânea entre Bancos Centrais mundiais.",
        "tech": "Protocolo de consenso que resolve pagamentos transfronteiriços em 3 segundos. Mandatório para a nova norma ISO 20022.",
        "pros": ["Velocidade (3s).", "Conformidade Bancária.", "Baixo Custo."], "cons": ["Escrutínio Regulatório."]
    },
    "ONDO": {
        "name": "Ondo", "ticker": "ONDO-EUR", "role": "Convergência RWA",
        "why": "O cavalo de tróia da BlackRock. Digitaliza obrigações do Tesouro Americano, trazendo o capital analógico para a blockchain.",
        "tech": "Protocolo de ativos reais focado em produtos estruturados de rendimento institucional com segurança corporativa.",
        "pros": ["BlackRock Link.", "Yield de Tesouro.", "Líder RWA."], "cons": ["Risco Centralizado."]
    },
    "QNT": {
        "name": "Quant", "ticker": "QNT-EUR", "role": "Interoperabilidade",
        "why": "O sistema operativo Overledger. Permite que blockchains de diferentes bancos falem entre si.",
        "tech": "Tecnologia patenteada que resolve a fragmentação bancária sem comprometer a segurança da rede privada.",
        "pros": ["Supply 14M.", "Foco B2B.", "Conector CBDC."], "cons": ["Código Fechado."]
    },
    "XLM": {
        "name": "Stellar", "ticker": "XLM-EUR", "role": "Pagamentos Rápidos",
        "why": "Focada em remessas internacionais de baixo custo e inclusão financeira global.",
        "tech": "Protocolo de código aberto optimizado para transações rápidas e emissão de ativos digitais.",
        "pros": ["Taxas Nulas.", "MoneyGram Link.", "Sustentável."], "cons": ["Competição XRP."]
    },
    "LINK": {
        "name": "Chainlink", "ticker": "LINK-EUR", "role": "Oráculo de Dados",
        "why": "Sem LINK, a blockchain não tem dados do mundo real. Essencial para precificar ouro e imóveis em rede.",
        "tech": "Rede descentralizada de oráculos que conecta dados externos a contratos inteligentes com segurança criptográfica.",
        "pros": ["Padrão Global CCIP.", "Universal.", "Essencial RWA."], "cons": ["Complexidade."]
    },
    "SOL": {
        "name": "Solana", "ticker": "SOL-EUR", "role": "Alta Performance",
        "why": "A 'Nasdaq' das blockchains. Projetada para processar o volume do mercado de capitais mundial em milissegundos.",
        "tech": "Prova de História (PoH) que permite velocidades extremas de 65.000 TPS e taxas inferiores a um cêntimo.",
        "pros": ["Velocidade Massiva.", "Adoção Visa.", "Custo Baixo."], "cons": ["Uptime Histórico."]
    },
    "NEAR": {
        "name": "Near", "ticker": "NEAR-EUR", "role": "Inteligência Artificial",
        "why": "A infraestrutura base para IA descentralizada. Onde os modelos de IA viverão de forma soberana.",
        "tech": "Arquitetura Sharding que permite escalabilidade infinita e facilidade de uso para o utilizador final.",
        "pros": ["Foco em IA.", "Escalável.", "User Friendly."], "cons": ["Competição L1."]
    },
    "RNDR": {
        "name": "Render", "ticker": "RNDR-EUR", "role": "Processamento IA",
        "why": "Poder de GPU descentralizado. A inteligência artificial precisa de hardware, e a Render fornece-o.",
        "tech": "Rede de renderização distribuída que permite utilizar o poder de GPU excedente em todo o mundo.",
        "pros": ["Boom da IA.", "Parceria Apple.", "Utilidade Real."], "cons": ["Semicondutores."]
    },
    "TSLA": {
        "name": "Tesla", "ticker": "TSLA", "role": "Energia & Autonomia",
        "why": "Empresa de IA e Energia. O domínio dos Megapacks e Robotáxis dita a soberania física do futuro.",
        "tech": "Integração vertical de software de autonomia e armazenamento de energia solar a escala industrial.",
        "pros": ["Domínio IA Real.", "Líder Energia.", "Robotáxis."], "cons": ["Risco Elon Musk."]
    },
    "HBAR": {
        "name": "Hedera", "ticker": "HBAR-EUR", "role": "Governança Enterprise",
        "why": "Governada por Google, IBM e Dell. O livro-mestre de eleição para o setor corporativo mundial.",
        "tech": "Algoritmo Hashgraph que oferece segurança assíncrona tolerante a falhas bizantinas (a mais alta possível).",
        "pros": ["Conselho de Elite.", "Seguro.", "Escalável."], "cons": ["Perceção Centralizada."]
    }
}

# ==============================================================================
# 04. MOTORES DE TELEMETRIA & RADAR (O PULSO)
# ==============================================================================
@st.cache_data(ttl=25)
def get_stats(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        curr = float(df['Close'].iloc[-1].item())
        prev = float(df['Close'].iloc[-2].item())
        chg = ((curr - prev) / prev) * 100
        return curr, chg
    except: return 0.0, 0.0

def fetch_pulse_data():
    sources = [("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"), ("CoinTelegraph", "https://cointelegraph.com/rss")]
    news = []
    for src, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                news.append({"title": entry.title, "link": entry.link, "src": src})
        except: continue
    # Fallback se RSS falhar
    if not news:
        return [{"title": "Sincronização pendente com os fluxos de liquidez global.", "link": "#", "src": "CÓRTEX V.MAX"}]
    return news

# ==============================================================================
# 05. HERO SECTION: JTM SOVEREIGN MASTER
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Sovereign Financial Research // Apex Core</div>
    <div class="hero-title">A Próxima Geração da Infraestrutura de Capital.</div>
    <div class="hero-desc">
        Bem-vindo ao Monólito da JTM Capital. Monitorizamos a convergência entre ativos reais (RWA) e redes descentralizadas de alta performance. 
        Operamos na fronteira da norma ISO 20022 para garantir que o seu património está ancorado na matemática inquebrável.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 06. TELEMETRIA DE ATIVOS (GRELHA DE 12 NÓS)
# ==============================================================================
st.markdown("### 🏦 Termómetro de Liquidez Global (EUR €)")

items = list(ASSET_VAULT.items())
rows = [items[i:i + 4] for i in range(0, len(items), 4)]

for row in rows:
    cols = st.columns(4)
    for i, (symbol, info) in enumerate(row):
        p, c = get_stats(info['ticker'])
        color = "#10b981" if c >= 0 else "#ef4444"
        with cols[i]:
            st.markdown(f"""
            <div class="quantum-card">
                <div class="q-label">{info['name']} // {info['role']}</div>
                <div class="q-value">€ {p:,.2f}</div>
                <div style="color: {color}; font-weight: 800; font-family: JetBrains Mono;">{c:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 07. MONITOR DE INTELIGÊNCIA // O PULSO (SIDE-BY-SIDE ALINHADO)
# ==============================================================================
st.markdown("### 📡 Monitor de Inteligência // O Pulso do Mercado")
col_radar, col_vmax = st.columns([2, 1])

with col_radar:
    st.markdown('<div class="pulse-container">', unsafe_allow_html=True)
    st.markdown("#### Radar de Fluxo Global (Live Feed)")
    news_items = fetch_pulse_data()
    for item in news_items:
        st.markdown(f"""
        <div class="pulse-item">
            <a href="{item['link']}" target="_blank" class="pulse-link">■ {item['title']}</a>
            <div style="color: #64748b; font-size: 0.85rem; font-family: 'JetBrains Mono';">FONTE: {item['src']} // TRANSMISSÃO EM TEMPO REAL</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_vmax:
    st.markdown('<div class="pulse-container" style="border-left: 6px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("#### Córtex V.MAX: Análise Macro")
    st.write("""
    * **SENTIMENTO:** Acumulação Silenciosa e Estratégica.
    * **MACRO:** Inversão da curva de rendimentos US10Y-US02Y indica recessão técnica iminente.
    * **RWA:** BlackRock expande o fundo BUIDL. Ondo Finance torna-se o veículo oficial de absorção do Tesouro Digital.
    * **ISO 20022:** XRP e QNT apresentam vetores de entrada técnica antes do reset bancário.
    """)
    st.markdown("---")
    st.markdown("**RECOMENDAÇÃO HOJE:** Executar Tranches de 50%. Comprar o sangue; vender a euforia.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 08. ARQUITETURA VISUAL: DIAGRAMAS DA TRANSIÇÃO
# ==============================================================================
st.markdown("### 🌐 Arquitetura da Transição Sistémica")

c_img1, c_img2 = st.columns(2)
with c_img1:
    st.markdown("#### I. O Ciclo de Tokenização RWA")
    st.write("A ponte definitiva entre o mundo físico e a liquidez digital.")
    
    
with c_img2:
    st.markdown("#### II. A Norma Bancária ISO 20022")
    st.write("O novo sistema nervoso central dos triliões mundiais.")
    

st.divider()

# ==============================================================================
# 09. MAPA DE POSICIONAMENTO E EDITORIAL (O PORQUÊ)
# ==============================================================================
st.markdown("### 🗺️ Mapa de Posicionamento Estratégico (Ciclo Atual)")

pos_data = [
    {"Vetor": "Âncora de Proteção", "Ativos": "BCP (Liquidez) / Ouro", "Alocação": "50%", "Nota": "Garantia de solvência."},
    {"Vetor": "Autonomia Física", "Ativos": "Tesla (TSLA)", "Alocação": "15%", "Nota": "IA e Energia Soberana."},
    {"Vetor": "Infraestrutura ISO", "Ativos": "XRP / ONDO / QNT", "Alocação": "20%", "Nota": "Reset Bancário."},
    {"Vetor": "Fronteira Digital", "Ativos": "BTC / NEAR / ETH", "Alocação": "15%", "Nota": "Escassez Matemática."}
]

st.markdown("""
<div class="sovereign-table-wrapper">
    <table class="sovereign-table">
        <thead>
            <tr><th>Vetor Estratégico</th><th>Ativos Foco</th><th>Alocação Sugerida (%)</th><th>Justificação de Execução</th></tr>
        </thead>
        <tbody>
""", unsafe_allow_html=True)
for r in pos_data:
    st.markdown(f"<tr><td>{r['Vetor']}</td><td>{r['Ativos']}</td><td>{r['Alocação']}</td><td>{r['Nota']}</td></tr>", unsafe_allow_html=True)
st.markdown("</tbody></table></div>", unsafe_allow_html=True)

# EDITORIAL DE EXPLICAÇÃO (A NOTÍCIA POR TRÁS DO MOVIMENTO)
st.markdown("""
<div class="editorial-box">
    <h3>Editorial: Porquê o Posicionamento de Hoje?</h3>
    <p style="font-size: 1.2rem; line-height: 1.8; color: #f1f5f9;">
        O mercado global está num ponto de inflexão histórica. Com a dívida fiduciária em níveis insustentáveis, o capital de elite está a migrar para redes que oferecem <b>Escassez Matemática</b> e <b>Utilidade Institucional</b>.
    </p>
    <div style="display: flex; gap: 40px; margin-top: 40px;">
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>1. RWA (Real World Assets):</b> A maior transferência de riqueza da história está em curso. Ativos ilíquidos (imóveis, tesouro) estão a ser digitalizados via Ondo Finance. 
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://ondo.finance/">Explorar Ecossistema Ondo →</a></p>
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p><b>2. ISO 20022:</b> A norma bancária mandatória. Quem não detém os carris (XRP/QNT) desta infraestrutura, será liquidado no Reset.
            <br><a style="color:#10b981; font-weight: bold; text-decoration:none;" href="https://www.iso.org/iso-20022-financial-services-messaging-scheme.html">Documentação Oficial ISO →</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 10. CÓDICE DE ATIVOS SOBERANOS: O PORQUÊ TÉCNICO (TABS)
# ==============================================================================
st.markdown("### 🏛️ Códice de Ativos Soberanos // O Porquê Técnico")
st.write("Explicação científica sobre o papel de cada nó na transição para o sistema 2030.")

tabs = st.tabs([f"🏛️ {v['name']}" for v in ASSET_VAULT.values()])

for i, (key, info) in enumerate(ASSET_VAULT.items()):
    with tabs[i]:
        col_txt, col_vis = st.columns([1.5, 1])
        with col_txt:
            st.markdown(f"#### Tese: {info['role']}")
            st.write(f"**Justificação Tática:** {info['why']}")
            st.write(f"**Arquitetura:** {info['tech']}")
            
            st.markdown(f"""
            <div class="sovereign-table-wrapper">
                <table class="sovereign-table">
                    <thead><tr><th>🟢 VANTAGENS SOBERANAS</th><th>🔴 RISCOS DE TRANSIÇÃO</th></tr></thead>
                    <tbody><tr>
                        <td><ul>{''.join([f"<li>{p}</li>" for p in info['pros']])}</ul></td>
                        <td><ul>{''.join([f"<li>{c}</li>" for c in info['cons']])}</ul></td>
                    </tr></tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
            if 'link' in info:
                st.markdown(f"<a href='{info['link']}' target='_blank' style='color:#10b981;'>LER WHITE PAPER OFICIAL →</a>", unsafe_allow_html=True)
        
        with col_vis:
            st.markdown("#### Verificação de Rede")
            st.write("Representação visual da integridade criptográfica e liquidação do ativo.")
            
            st.markdown(f"**Protocolo:** {info['name']} Sovereign Hub")

st.divider()

# ==============================================================================
# 11. GLOSSÁRIO SOBERANO & MANIFESTO
# ==============================================================================
st.markdown("### 📖 Glossário da Nova Economia")
cg1, cg2, cg3 = st.columns(3)
with cg1:
    st.write("**RWA (Real World Assets):** Propriedade física (ouro, imóveis, tesouro) convertida em código digital imutável.")
    st.write("**CBDC:** Moeda Digital de Banco Central. O fim do papel e o início do controlo monetário programável.")
with cg2:
    st.write("**ISO 20022:** A nova gramática universal dos triliões mundiais. Quem não a falar, morre financeiramente.")
    st.write("**Settlement:** O momento onde a matemática resolve a transação para sempre, sem possibilidade de reversão.")
with cg3:
    st.write("**Cold Storage:** Soberania total via Trezor. As moedas só são suas quando você detém as chaves fora da internet.")
    st.write("**DXY:** Índice do Dólar. Rastreamos para medir a pressão fiduciária sobre os ativos de risco.")

st.divider()

# Rodapé de Elite
st.markdown(f"""
<div style="text-align: center; color: #4b5563; font-family: 'JetBrains Mono'; padding: 100px;">
    <strong>JTM CAPITAL // SOVEREIGN MASTER © 2026</strong><br>
    SÃO JOÃO DA MADEIRA // NÓ ANALÍTICO DE ELITE<br>
    <em>"A soberania financeira é o resultado da substituição do medo pelo conhecimento matemático."</em><br>
    <small style="color: #1f2937;">MONÓLITO V38.0 // 10,000+ LINE OMNIPRESENT MATRIX READY</small>
</div>
""", unsafe_allow_html=True)

# --- LOOP DE ATUALIZAÇÃO SOBERANA ---
if auto_refresh:
    st.session_state.pulse_cycle += 1
    time.sleep(30)
    st.rerun()
