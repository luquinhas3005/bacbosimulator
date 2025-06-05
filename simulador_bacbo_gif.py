
import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Bac Bo", layout="centered")

st.title("🎲 Simulador Bac Bo - Versão com Animação")

# Inicialização da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para simular uma rodada
def simular_rodada():
    # Animação com GIF
    st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", caption="Rolando os dados...")
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
        resultado = "Player"
    elif banker_total > player_total:
        resultado = "Banker"
    else:
        resultado = "Tie"

    dados["Resultado"] = resultado
    st.session_state.historico.append(dados)

# Botão para rodar
if st.button("🎰 Rodar Dados"):
    simular_rodada()

# Mostrar resultados
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Player Total"] = df["Player 1"] + df["Player 2"]
    df["Banker Total"] = df["Banker 1"] + df["Banker 2"]

    st.subheader("📊 Histórico de Rodadas")
    st.dataframe(df[["Player 1", "Player 2", "Banker 1", "Banker 2", "Player Total", "Banker Total", "Resultado"]], use_container_width=True)

    # Contador por resultado
    contagem = df["Resultado"].value_counts()
    st.subheader("🔢 Contagem de Resultados")
    st.bar_chart(contagem)
else:
    st.info("Clique no botão acima para iniciar a simulação.")
