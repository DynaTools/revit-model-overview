import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configurar a página do Streamlit
st.set_page_config(page_title="REVIT DASHBOARD", page_icon="bar_chart:", layout="wide")

def app():
    st.title("Hello, World!")
    st.write("Bem-vindo ao meu primeiro site com Streamlit!")

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
        st.dataframe(df, height=100)  # Definir altura fixa para permitir rolagem

        # Adicionar filtros na barra lateral
        st.sidebar.header("Filtrar dados:")
        filter_options = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_values = df[col].unique()
                selected_values = st.sidebar.multiselect(f"Selecionar {col}", options=unique_values, default=unique_values)
                df = df[df[col].isin(selected_values)]
                filter_options[col] = selected_values

        # Seleção dos campos e tipo de gráfico
        st.sidebar.header("Configurações do Gráfico")
        chart_type = st.sidebar.selectbox("Tipo de gráfico", ["Barra", "Pizza"])
        x_axis = st.sidebar.selectbox("Selecione a coluna para o eixo X", df.columns)
        y_axis = st.sidebar.selectbox("Selecione a coluna para o eixo Y", df.columns)
        color_column = 'Location'  # Usar a coluna 'Location' para diferenciar as cores automaticamente

        # Criar o gráfico baseado na seleção do usuário
        if chart_type == "Barra":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_column, title=f"{chart_type} de {y_axis} por {x_axis}", color_discrete_sequence=px.colors.qualitative.Plotly)
        elif chart_type == "Pizza":
            fig = px.pie(df, names=x_axis, values=y_axis, color=color_column, title=f"{chart_type} de {y_axis} por {x_axis}", color_discrete_sequence=px.colors.qualitative.Plotly)

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
