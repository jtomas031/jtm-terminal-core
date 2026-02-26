import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO DO NÚCLEO E BLINDAGEM VISUAL
# ==========================================
st.set_page_config(page_title="JTM CAPITAL | COMANDO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; }
    .terminal-header { border-bottom: 2px solid #00FF41; padding-bottom: 10px; margin-bottom: 30px; }
    .title-main { color: #00FF41; font-family: 'Courier New', monospace; font-size: 42px; font-weight: 900; letter-spacing: 4px; margin: 0; }
    .title-sub { color: #555555; font-family: 'Courier New', monospace; font-size: 16px; letter-spacing: 2px; text-transform: uppercase; margin-top: -10px;}
    .hud-box { background-color: #070707; border: 1px solid #1A1A1A; border-left: 4px solid #00FF41; padding: 20px; border-radius: 2px; }
    .hud-warning { border-left: 4px solid #FF0000; }
    h2, h3, h4 { color: #FFFFFF; font-family: 'Courier New', monospace; text-transform: uppercase; }
    p, li { color: #B0B0B0; font-family: 'Arial'; font-size: 15px; }
    .highlight { color: #00FF41; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="terminal-header"><p class="title-main">JTM CAPITAL RESEARCH</p><p class="title-sub">Terminal de Operações Institucionais // Nível 5</p></div>', unsafe_allow_html=True)

# ==========================================
# 2. MOTOR DE TELEMETRIA (CACHED PARA PERFORMANCE)
# ==========================================
@st.cache_data(ttl=900) # Atualiza dados a cada 15 minutos para evitar bloqueios da API
def get_institutional_data(tickers):
    data = {}
    for t in tickers:
        try:
            df = yf.download(t, period="5d", interval="1h", progress=False)
            if not df.empty:
                current = df['Close'].iloc[-1].item() if not pd.isna(df['Close'].iloc[-1].item()) else 0
                first = df['Close'].iloc[0].item() if not pd.isna(df['Close'].iloc[0].item()) else 1
                change = ((current - first) / first) * 100
                data[t] = {"price": current, "change": change, "df": df}
            else:
                data[t] = {"price": 0.0, "change": 0.0, "df": None}
        except:
            data[t] = {"price": 0.0, "change": 0.0, "df": None}
    return data

# Mapeamento de Alvos
target_map = {
    "BTC-USD": "BTC (ESCUDO)",
    "ETH-USD": "ETH (AUTOESTRADA)",
    "LINK-USD": "LINK (ORÁCULO)",
    "QNT-USD": "QNT (INTEROP)",
    "XRP-USD": "XRP (ISO 20022)"
}

market_data = get_institutional_data(list(target_map.keys()))

st.subheader("📡 RADAR DE LIQUIDEZ (SWIFT & RWA)")
cols = st.columns(len(target_map))
for i, (ticker, label) in enumerate(target_map.items()):
    val = market_data[ticker]["price"]
    perc = market_data[ticker]["change"]
    cols[i].metric(label=label, value=f"${val:,.2f}", delta=f"{perc:.2f}%")

st.divider()

# ==========================================
# 3. DIRETRIZES DE GUERRA E EXECUÇÃO
# ==========================================
col_strat, col_chart = st.columns([1.2, 2])

with col_strat:
    st.markdown('<div class="hud-box">', unsafe_allow_html=True)
    st.subheader("⚙️ PROTOCOLO DE EXECUÇÃO")
    st.write("""
    A transição institucional exige disciplina matemática. As emoções, o medo e a ganância são falhas de sistema que devem ser suprimidas. O plano opera com precisão balística.
    
    <span class="highlight">ALOCAÇÃO TÁTICA MENSAL: 360€</span>
    
    * **Janela de Ataque:** Execução implacável perto do dia 29 de cada mês. Sem hesitação face a quedas de mercado (DCA).
    * **A Base (300€):** O núcleo intocável. Capital direcionado para a autoestrada principal (Ethereum) e para o escudo monetário (Bitcoin). 
    * **Pelotão Sniper (60€):** Forças especiais. Risco calculado implantado em Chainlink, Quant, Ripple ou infraestrutura DePIN.
    * **Protocolo de Extração:** Todo o capital adquirido tem como destino final obrigatório a hardware wallet Trezor. Qualquer retenção prolongada em exchanges é uma violação de segurança.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="hud-box hud-warning" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.subheader("⚠️ ALERTA DO SISTEMA")
    st.write("A soberania financeira absoluta até 2030 depende da manutenção do plano. Tentativas de alterar o fluxo de capital sem justificação institucional (BlackRock/SWIFT) serão bloqueadas.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    st.subheader("📊 VETOR DE PREÇO INSTITUCIONAL (BTC)")
    btc_df = market_data["BTC-USD"]["df"]
    if btc_df is not None:
        fig = go.Figure(data=[go.Candlestick(
            x=btc_df.index, open=btc_df['Open'], high=btc_df['High'], 
            low=btc_df['Low'], close=btc_df['Close'],
            increasing_line_color='#00FF41', decreasing_line_color='#FF0000'
        )])
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0), xaxis_rangeslider_visible=False, height=420
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("FALHA NA EXTRAÇÃO DE DADOS. ROTA DE SINAL COMPROMETIDA.")

st.divider()
st.caption("SISTEMA CORTEX JTM // INFRAESTRUTURA DESCENTRALIZADA // 2026")
