
import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Bac Bo Royale", layout="centered")

# 🎰 Título com estilo
st.markdown(
    "<h2 style='text-align: center; color: gold;'>🎰 Bac Bo Royale 🎰</h2>",
    unsafe_allow_html=True
)

# Fundo temático
st.markdown(
    "<div style='background-color: #111; padding: 20px; border-radius: 15px;'>",
    unsafe_allow_html=True
)

# Inicialização
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função de simulação com GIF
def simular_rodada():
    st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", caption="🎲 Dados rolando...")
    time.sleep(1.5)

    dados = {
        "Player 1": random.randint(1, 6),
        "Player 2": random.randint(1, 6),
        "Banker 1": random.randint(1, 6),
        "Banker 2": random.randint(1, 6),
    }
    player_total = dados["Player 1"] + dados["Player 2"]
    banker_total = dados["Banker 1"] + dados["Banker 2"]

    if player_total > banker_total:
        resultado = "🧍 Player"
    elif banker_total > player_total:
        resultado = "🏦 Banker"
    else:
        resultado = "⚖️ Tie"

    dados["Resultado"] = resultado
    st.session_state.historico.append(dados)

# Botão estilizado
st.markdown(
    "<div style='text-align: center; margin-top: 20px;'>",
    unsafe_allow_html=True
)
if st.button("🎰 Rodar Dados", use_container_width=True):
    simular_rodada()

# Mostrar histórico
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Player Total"] = df["Player 1"] + df["Player 2"]
    df["Banker Total"] = df["Banker 1"] + df["Banker 2"]

    st.markdown("<h4 style='color: gold;'>📊 Histórico de Rodadas</h4>", unsafe_allow_html=True)
    st.dataframe(df[["Player 1", "Player 2", "Banker 1", "Banker 2", "Player Total", "Banker Total", "Resultado"]], use_container_width=True)

    # Contagem
    contagem = df["Resultado"].value_counts()
    st.markdown("<h4 style='color: gold;'>📈 Contagem de Resultados</h4>", unsafe_allow_html=True)
    st.bar_chart(contagem)

else:
    st.info("Clique no botão acima para iniciar a simulação.")

# Fechar o fundo temático
st.markdown("</div>", unsafe_allow_html=True)
