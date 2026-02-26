import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import time

# --- 1. CONFIGURAÇÃO DE COMANDO TÁTICO ---
st.set_page_config(page_title="JTM CAPITAL | Research", layout="wide", page_icon="⚡")

# Motor de Atualização Autônoma (60 Segundos)
st.sidebar.markdown("### ⚙️ CONTROLO DE SISTEMA")
auto_update = st.sidebar.toggle("ATIVAR RADAR AUTÔNOMO (60s)", value=True)
st.sidebar.caption("Se ativado, o terminal atualiza preços e notícias a cada minuto, monitorizando o fluxo institucional em tempo real.")

# CSS Corporativo Premium (Cores Vibrantes & Fundo Profundo)
st.markdown("""
<style>
    .stApp { background-color: #040914; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #ffffff; font-weight: 800; letter-spacing: -0.5px; }
    
    /* Gradiente na Hero Section */
    .hero-section { background: linear-gradient(90deg, #0f172a
