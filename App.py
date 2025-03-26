import streamlit as st
import pandas as pd

# -----------------------------
# 1. CARREGAR OS DADOS
# -----------------------------
@st.cache_data

def load_data():
    df = pd.read_csv("Est_GRE_Mun_EscolaV5.csv", sep=';')

    # Corrigir colunas duplicadas e espaços
    def deduplicate_columns(columns):
    seen = {}
    new_cols = []
    for col in columns:
        col = col.strip()
        if col in seen:
            seen[col] += 1
            col = f"{col}_{seen[col]}"
        else:
            seen[col] = 0
        new_cols.append(col)
    return new_cols

df.columns = deduplicate_columns(df.columns)


    # Garantir que as colunas de índice sejam numéricas e arredondadas
    index_cols = df.columns[-18:]
    df[index_cols] = df[index_cols].apply(pd.to_numeric, errors='coerce').round(2)

    return df, index_cols

df, index_cols = load_data()

# -----------------------------
# 2. PÁGINA DINÂMICA
# -----------------------------
st.set_page_config(page_title="Painel da Educação", layout="wide")
view = st.sidebar.selectbox("Navegação", ["Visão Estadual"] + sorted(df['Regional'].unique()) + sorted(df['Município'].unique()))

# -----------------------------
# 3. VISÃO ESTADUAL
# -----------------------------
if view == "Visão Estadual":
    st.title("🌟 Painel de Indicadores da Educação - Estado")

    st.subheader("Médias Gerais do Estado")
    state_means = df[index_cols].mean().round(2)
    st.dataframe(state_means.to_frame("Média Estadual"))

    st.subheader("Regionais")
    regionais_df = df.groupby("Regional")[index_cols].mean().round(2).sort_index()

    for regional in regionais_df.index:
        st.markdown(f"### [{regional}](?view={regional})")
        st.dataframe(regionais_df.loc[[regional]])
        st.markdown("---")

# -----------------------------
# 4. VISÃO REGIONAL
# -----------------------------
elif view in df['Regional'].unique():
    st.title(f"🏢 Regional: {view}")

    municipios_df = df[df['Regional'] == view].groupby("Município")[index_cols].mean().round(2).sort_index()

    for municipio in municipios_df.index:
        st.markdown(f"### [{municipio}](?view={municipio})")
        st.dataframe(municipios_df.loc[[municipio]])
        st.markdown("---")

# -----------------------------
# 5. VISÃO MUNICÍPIO
# -----------------------------
elif view in df['Município'].unique():
    st.title(f"🏙️ Município: {view}")

    escolas_df = df[df['Município'] == view][['Escola'] + list(index_cols)].sort_values(by='Escola')
    st.dataframe(escolas_df)

else:
    st.warning("Seleção inválida.")
