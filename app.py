import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_lottie import st_lottie
import requests

# Configurar a página do Streamlit
st.set_page_config(page_title="REVIT DASHBOARD", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    st.title("REVIT SCHEDULE DASHBOARD")
    st.write("Desenvolvido por Paulo Augusto Giavoni")
    st.write("[LinkedIn](https://www.linkedin.com/in/paulogiavoni/)")

    # Carregar a animação Lottie
    lottie_url = "https://lottie.host/72e89b38-f43c-455a-8122-6f90f22e0430/CSODKEqCIe.json"
    lottie_animation = load_lottieurl(lottie_url)

    # Layout de colunas para o iframe do modelo e a animação Lottie
    col1, col2 = st.columns([2, 1])

    with col1:
        # Adicionar a janela de visualização do modelo Speckle
        st.components.v1.iframe("https://app.speckle.systems/projects/95b44decbf/models/28b9a034de#embed=%7B%22isEnabled%22%3Atrue%2C%22isTransparent%22%3Atrue%2C%22hideControls%22%3Atrue%2C%22hideSelectionInfo%22%3Atrue%7D", width=1000, height=400)

    with col2:
        # Exibir a animação Lottie
        st_lottie(lottie_animation, height=400, width=300)

    # Listar os arquivos na pasta uploads
    upload_folder = 'uploads'
    files = [f for f in os.listdir(upload_folder) if f.endswith('.xlsx') or f.endswith('.xls')]

    if not files:
        st.write("Nenhum arquivo Excel encontrado na pasta uploads.")
        return

    # Permitir que o usuário selecione um arquivo
    selected_file = st.selectbox("Selecione um arquivo Excel", files)

    if selected_file:
        file_path = os.path.join(upload_folder, selected_file)

        try:
            # Tentar ler o conteúdo do arquivo Excel
            df = pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo Excel: {e}")
            return

        # Mostrar uma pré-visualização do conteúdo do arquivo
        st.write("Pré-visualização do arquivo selecionado:")
        st.dataframe(df, height=400)  # Definir altura fixa para permitir rolagem

        # Adicionar filtros na barra lateral
        st.sidebar.header("Filtrar dados:")
        st.sidebar.markdown("---")  # Adicionar uma linha divisória para clareza
        filter_options = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_values = df[col].unique()
                selected_values = st.sidebar.multiselect(f"Selecionar {col}", options=unique_values, default=unique_values)
                df = df[df[col].isin(selected_values)]
                filter_options[col] = selected_values

        # Seleção dos campos e tipo de gráfico
        st.sidebar.header("Configurações do Gráfico")
        st.sidebar.markdown("---")  # Adicionar uma linha divisória para clareza
        chart_type = st.sidebar.selectbox("Tipo de gráfico", ["Barra", "Pizza"])
        x_axis = st.sidebar.selectbox("Selecione a coluna para o eixo X", df.columns)
        y_axis = st.sidebar.selectbox("Selecione a coluna para o eixo Y", df.columns)

        # Criar o gráfico baseado na seleção do usuário
        if chart_type == "Barra":
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{chart_type} de {y_axis} por {x_axis}", color_discrete_sequence=px.colors.qualitative.Plotly)
        elif chart_type == "Pizza":
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"{chart_type} de {y_axis} por {x_axis}", color_discrete_sequence=px.colors.qualitative.Plotly)

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
