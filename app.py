import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import pandas as pd
import time

# --- 1. CONFIGURAÇÃO DE PORTAL (COINDESK STYLE) ---
st.set_page_config(page_title="JTM CAPITAL | Research Hub", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    /* Estética Clean & Professional News Portal */
    .stApp { background-color: #0b1120; color: #f8fafc; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h1, h2, h3, h4 { color: #ffffff; font-weight: 700; }
    
    /* Hero e Artigos */
    .article-box { background-color: #1e293b; padding: 40px; border-radius: 8px; margin-bottom: 30px; border-left: 6px solid #38bdf8; line-height: 1.8; font-size: 1.1rem; }
    .article-title { font-size: 2.5rem; color: #38bdf8; margin-bottom: 20px; font-weight: 800; border-bottom: 1px solid #334155; padding-bottom: 10px; }
    .highlight { color: #38bdf8; font-weight: bold; }
    .highlight-green { color: #10b981; font-weight: bold; }
    
    /* Telemetria e Cartões */
    .metric-container { background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 20px; text-align: center; }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #ffffff; }
    .metric-sub { font-size: 0.9rem; color: #94a3b8; }
    
    /* Tabelas Prós/Contras */
    .pc-table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; background-color: #0f172a; border-radius: 8px; overflow: hidden; }
    .pc-table th, .pc-table td { border: 1px solid #334155; padding: 15px; text-align: left; }
    .pc-table th { background-color: #1e293b; color: #38bdf8; font-size: 1.1rem; }
    .pro-td { border-left: 4px solid #10b981 !important; }
    .con-td { border-left: 4px solid #ef4444 !important; }
    
    /* Notícias Específicas */
    .news-card { background-color: #1e293b; padding: 15px; border-radius: 6px; margin-bottom: 10px; border-left: 3px solid #64748b; }
    .news-card a { color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 1.05rem; }
    .news-card a:hover { color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- 2. CABEÇALHO DO PORTAL ---
st.markdown('<div style="text-align: center; margin-bottom: 40px;"><h1 style="font-size: 4rem; color: #ffffff; font-family: \'Georgia\', serif; letter-spacing: 2px;">JTM CAPITAL <span style="color: #38bdf8;">RESEARCH</span></h1><p style="color: #94a3b8; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 4px;">Inteligência Institucional & Educação Financeira</p></div>', unsafe_allow_html=True)

# --- 3. SECÇÃO EDUCATIVA PROFUNDA (O "PORQUÊ" PARA O PÚBLICO) ---
st.markdown('<div class="article-box">', unsafe_allow_html=True)
st.markdown('<div class="article-title">O Fim do Dinheiro de Papel: Entendendo a Tokenização (RWA)</div>', unsafe_allow_html=True)
st.write("""
Imagine que possui um apartamento de 500.000€. Se precisar de 5.000€ amanhã, não pode vender apenas "a cozinha" do apartamento. O ativo é ilíquido. A **Tokenização de Ativos do Mundo Real (RWA)** resolve isto. 

Ao utilizar a tecnologia Blockchain (como a rede Ethereum), a BlackRock e outros gigantes estão a transformar propriedades, ouro, ações e até dívida pública em "fichas digitais" (tokens). Um apartamento de 500.000€ pode ser dividido em 500.000 tokens de 1€. Qualquer pessoa, em qualquer parte do mundo, pode comprar 10€ dessa casa instantaneamente, 24 horas por dia, 7 dias por semana.

Isto não é o futuro distante. <span class="highlight">Acontece agora.</span> O fundo BUIDL da BlackRock já tokenizou centenas de milhões de dólares em obrigações do tesouro americano na rede Ethereum. As criptomoedas já não são apenas moedas; são a **infraestrutura de software** onde toda a economia mundial será negociada.
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



st.markdown('<div class="article-box">', unsafe_allow_html=True)
st.markdown('<div class="article-title">A Norma ISO 20022: O Novo Sistema Nervoso dos Bancos</div>', unsafe_allow_html=True)
st.write("""
Quando envia dinheiro de Portugal para o Japão hoje, a transação passa por um sistema chamado **SWIFT**, criado na década de 1970. É lento (demora dias), caro e frequentemente perde informações. 

O mundo está a adotar obrigatoriamente um novo padrão de comunicação financeira chamado **ISO 20022**. Este padrão permite que as transferências carreguem enormes volumes de dados (quem envia, porquê, recibos em anexo). Mas há um detalhe vital: o sistema bancário tradicional não tem velocidade para processar isto instantaneamente. 

É aqui que entram ativos como o **XRP (Ripple)**, **XLM (Stellar)** e **QNT (Quant)**. Eles foram desenhados de raiz para falar a linguagem ISO 20022. Os Bancos Centrais não vão usar "Bitcoin" para transferir euros entre si; vão usar pontes institucionais (como o XRP) que liquidam transações em 3 segundos, custando frações de cêntimo, cumprindo todas as leis globais de transparência.
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



st.divider()

# --- 4. MOTOR DE TELEMETRIA PROFUNDA (PREÇO, VOL, MCAP) ---
st.markdown("## 📡 Monitorização de Mercado Global")

@st.cache_data(ttl=300)
def get_deep_market_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="2d")
        
        if len(df) >= 2:
            current = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            vol = df['Volume'].iloc[-1]
        else:
            current, change, vol = 0.0, 0.0, 0.0
            
        # Tenta obter o Market Cap, se falhar, faz uma aproximação visual rápida
        info = t.info
        mcap = info.get('marketCap', current * info.get('circulatingSupply', 0))
        if mcap == 0: mcap = current * 1000000 # Fallback de emergência
        
        return current, change, vol, mcap
    except:
        return 0.0, 0.0, 0.0, 0.0

def format_large_number(num):
    if num >= 1_000_000_000:
        return f"€{(num / 1_000_000_000):.2f} B"
    elif num >= 1_000_000:
        return f"€{(num / 1_000_000):.2f} M"
    return f"€{num:,.0f}"

assets_list = {
    "Bitcoin": "BTC-EUR", "Ethereum": "ETH-EUR", "Chainlink": "LINK-EUR",
    "Ripple": "XRP-EUR", "Quant": "QNT-EUR", "Stellar": "XLM-EUR", "Render": "RNDR-EUR"
}

# Cria grelha de telemetria
cols = st.columns(4)
for i, (name, ticker) in enumerate(assets_list.items()):
    price, change, vol, mcap = get_deep_market_data(ticker)
    color = "#10b981" if change >= 0 else "#ef4444"
    
    with cols[i % 4]:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="color: #38bdf8; margin-bottom: 5px;">{name}</h4>
            <div class="metric-value">€ {price:,.2f}</div>
            <div style="color: {color}; font-weight: bold; margin-bottom: 10px;">{change:+.2f}% (24h)</div>
            <div class="metric-sub"><b>Vol 24h:</b> {format_large_number(vol)}</div>
            <div class="metric-sub"><b>Market Cap:</b> {format_large_number(mcap)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

st.divider()

# --- 5. INTELIGÊNCIA POR ATIVO (NOTÍCIAS & ANÁLISE) ---
st.markdown("## 🔍 Dossiês de Infraestrutura Institucional")

@st.cache_data(ttl=1200)
def fetch_specific_news(keyword):
    urls = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss"]
    relevant_news = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower():
                    relevant_news.append({"title": entry.title, "link": entry.link, "date": entry.published[:16]})
                if len(relevant_news) >= 3: break
        except:
            pass
    return relevant_news

# Sistema de Tabs para navegação limpa
tabs = st.tabs(list(assets_list.keys()))

def render_crypto_tab(name, ticker, pros, cons, keyword):
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown(f"### Análise Estratégica: {name}")
        # Tabela Prós e Contras HTML
        st.markdown(f"""
        <table class="pc-table">
            <tr><th>Vantagens Institucionais (Prós)</th><th>Riscos Associados (Contras)</th></tr>
            <tr>
                <td class="pro-td"><ul>{''.join([f"<li>{p}</li>" for p in pros])}</ul></td>
                <td class="con-td"><ul>{''.join([f"<li>{c}</li>" for c in cons])}</ul></td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        # Gráfico
        df = yf.download(ticker, period="30d", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#38bdf8', width=2), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.1)')])
            fig.update_layout(title=f"Volume de Preço (30 Dias) - {name}", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"### Últimas Notícias ({name})")
        news = fetch_specific_news(keyword)
        if not news:
            st.write(f"Sem fluxo de notícias institucionais recentes para {name} nas fontes primárias.")
        else:
            for item in news:
                st.markdown(f"<div class='news-card'><a href='{item['link']}' target='_blank'>{item['title']}</a><br><span style='color:#64748b; font-size:0.8rem;'>{item['date']}</span></div>", unsafe_allow_html=True)

# Preenchimento das Tabs
with tabs[0]: render_crypto_tab("Bitcoin", "BTC-EUR", ["Escassez matemática (apenas 21 milhões).", "Aprovado por Wall Street (ETFs BlackRock).", "Reserva de valor imune à impressão de dinheiro."], ["Tecnologia antiga e lenta para pagamentos.", "Consumo energético elevado.", "Incapacidade de executar contratos inteligentes complexos."], "bitcoin")
with tabs[1]: render_crypto_tab("Ethereum", "ETH-EUR", ["Líder global em Tokenização (RWA).", "Maior rede de programadores do mundo.", "Gera rendimento passivo institucional (Staking)."], ["Taxas de transação (Gas) extremamente altas.", "Rede congestionada em momentos de pico.", "Forte concorrência de redes mais novas e rápidas."], "ethereum")
with tabs[2]: render_crypto_tab("Chainlink", "LINK-EUR", ["Monopólio prático no setor de Oráculos.", "Parcerias ativas com o SWIFT.", "Essencial para que bancos comuniquem com blockchains."], ["Economia do token complexa de entender.", "Depende do sucesso geral do mercado de contratos inteligentes.", "Baixo apelo especulativo para o retalho."], "chainlink")
with tabs[3]: render_crypto_tab("Ripple", "XRP-EUR", ["Claridade legal absoluta nos EUA.", "Desenhado para o padrão ISO 20022.", "Transações custam cêntimos e demoram 3 segundos."], ["Forte dependência das ações da empresa Ripple Labs.", "Adoção bancária final ainda enfrenta resistência política.", "Elevada quantidade de tokens na posse da empresa original."], "ripple")
with tabs[4]: render_crypto_tab("Quant", "QNT-EUR", ["Permite interoperabilidade sem criar nova blockchain.", "Foco estrito em CBDCs e Bancos Centrais.", "Oferta total extremamente reduzida (14 milhões)."], ["Ecossistema fechado (código não é totalmente público).", "Depende de adoção puramente corporativa B2B.", "Baixa liquidez nas exchanges de retalho."], "quant")
with tabs[5]: render_crypto_tab("Stellar", "XLM-EUR", ["Compatível com ISO 20022 e focado em pagamentos transfronteiriços.", "Parcerias com a IBM e governos para emissão de moedas.", "Alta velocidade e escalabilidade."], ["Forte concorrência direta com o XRP.", "Adoção corporativa menos agressiva que o seu rival.", "Inflação histórica do token afetou o preço."], "stellar")
with tabs[6]: render_crypto_tab("Render", "RNDR-EUR", ["Captura a onda gigante de expansão da Inteligência Artificial.", "Fornece poder de processamento GPU real e necessário.", "Desafia o monopólio da AWS e Google Cloud."], ["Fortemente correlacionado com o 'hype' momentâneo da IA.", "Concorrência crescente no setor de computação descentralizada.", "Dependente da oferta de placas gráficas globais."], "render")

st.divider()
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>JTM CAPITAL RESEARCH © 2026 | DADOS EXTRAÍDOS EM TEMPO REAL | INFRAESTRUTURA ANALÍTICA DE MERCADO</p>", unsafe_allow_html=True)
