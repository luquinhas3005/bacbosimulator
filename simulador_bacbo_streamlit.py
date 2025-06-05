
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")
st.title("🎲 Simulador Interativo de Bac Bo")

# Número de rodadas
rounds = st.slider("Número de rodadas a simular", min_value=10, max_value=300, value=50, step=10)

# Simulação
results = []
for _ in range(rounds):
    player = random.randint(1, 6) + random.randint(1, 6)
    banker = random.randint(1, 6) + random.randint(1, 6)
    if player > banker:
        result = "Player"
    elif banker > player:
        result = "Banker"
    else:
        result = "Tie"
    results.append(result)

df = pd.DataFrame({
    "Round": range(1, rounds + 1),
    "Result": results
})

color_map = {"Player": "blue", "Banker": "red", "Tie": "green"}

# Bead Road
bead_df = df.copy()
bead_df["Row"] = bead_df.index // 6
bead_df["Col"] = bead_df.index % 6

fig_bead, ax_bead = plt.subplots(figsize=(12, 5))
for _, row in bead_df.iterrows():
    ax_bead.add_patch(plt.Circle((row["Row"], 5 - row["Col"]), 0.4, color=color_map[row["Result"]]))
    ax_bead.text(row["Row"], 5 - row["Col"], row["Result"][0], ha='center', va='center', color='white', fontsize=8)

ax_bead.set_xlim(-1, bead_df["Row"].max() + 1)
ax_bead.set_ylim(-1, 6)
ax_bead.set_aspect('equal')
ax_bead.axis('off')
ax_bead.set_title("Bead Road (Estilo Baccarat)", fontsize=14)
st.pyplot(fig_bead)

# Big Road
big_road_df = []
current_result = None
col = 0
row = 0

for result in results:
    if result != current_result:
        current_result = result
        col += 1
        row = 0
    else:
        if row < 5:
            row += 1
        else:
            col += 1
            row = 0
    big_road_df.append((col, row, result))

fig_big, ax_big = plt.subplots(figsize=(12, 5))
for col, row, result in big_road_df:
    ax_big.add_patch(plt.Circle((col, 5 - row), 0.4, color=color_map[result]))
    ax_big.text(col, 5 - row, result[0], ha='center', va='center', color='white', fontsize=8)

ax_big.set_xlim(-1, col + 2)
ax_big.set_ylim(-1, 6)
ax_big.set_aspect('equal')
ax_big.axis('off')
ax_big.set_title("Big Road (Estilo Baccarat)", fontsize=14)
st.pyplot(fig_big)

# Derivados
def generate_derived_road(base_data, offset):
    derived_data = []
    for i in range(offset, len(base_data)):
        col_i, row_i, result_i = base_data[i]
        prev_col, prev_row, prev_result = base_data[i - offset]
        color = "blue" if result_i == prev_result else "red"
        derived_data.append((i - offset, color))
    return derived_data

def draw_derived_road(data, title):
    fig, ax = plt.subplots(figsize=(10, 2))
    for idx, (col, color) in enumerate(data):
        ax.add_patch(plt.Circle((col, 0), 0.4, color=color))
    ax.set_xlim(-1, len(data) + 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12)
    return fig

big_eye_data = generate_derived_road(big_road_df, offset=1)
small_road_data = generate_derived_road(big_road_df, offset=2)
cockroach_data = generate_derived_road(big_road_df, offset=3)

fig_big_eye = draw_derived_road(big_eye_data, "Big Eye Boy (Simplificado)")
fig_small = draw_derived_road(small_road_data, "Small Road (Simplificado)")
fig_cockroach = draw_derived_road(cockroach_data, "Cockroach Pig (Simplificado)")

st.pyplot(fig_big_eye)
st.pyplot(fig_small)
st.pyplot(fig_cockroach)

# Estatísticas
st.markdown("### 📊 Estatísticas")
win_counts = df['Result'].value_counts(normalize=True) * 100
st.write(win_counts.rename(lambda x: f"{x} (%)").round(2))

# Upload CSV
st.markdown("### ☁️ Importar CSV de resultados reais")
uploaded_file = st.file_uploader("Carregue um arquivo CSV com uma coluna 'Result' (Player, Banker, Tie):", type=["csv"])
if uploaded_file:
    imported_df = pd.read_csv(uploaded_file)
    if 'Result' in imported_df.columns:
        st.success("Arquivo carregado com sucesso!")
        st.write(imported_df.head())
        st.markdown("Você pode usar esses dados para seus próprios roadmaps!")
    else:
        st.error("O CSV precisa conter uma coluna chamada 'Result'.")

# Exportar
st.markdown("### 📤 Exportar Resultados")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar CSV com Resultados", data=csv, file_name="bacbo_resultados.csv", mime="text/csv")

# Rerun
if st.button("🔁 Simular Novamente"):
    st.experimental_rerun()
