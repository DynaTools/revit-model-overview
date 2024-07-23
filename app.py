import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_lottie import st_lottie
import requests

# Configure Streamlit page
st.set_page_config(page_title="REVIT DASHBOARD", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    st.title("REVIT SCHEDULE DASHBOARD")
    st.write("Developed by Paulo Augusto Giavoni")
    st.write("[LinkedIn](https://www.linkedin.com/in/paulogiavoni/)")

    # Load Lottie animation
    lottie_url = "https://lottie.host/72e89b38-f43c-455a-8122-6f90f22e0430/CSODKEqCIe.json"
    lottie_animation = load_lottieurl(lottie_url)

    # Column layout for Speckle model iframe and Lottie animation
    col1, col2 = st.columns([2, 1])

    with col1:
        # Add Speckle model view window
        st.components.v1.iframe("https://app.speckle.systems/projects/95b44decbf/models/28b9a034de#embed=%7B%22isEnabled%22%3Atrue%2C%22isTransparent%22%3Atrue%7D", width=1000, height=400)

    with col2:
        # Display Lottie animation
        st_lottie(lottie_animation, height=400, width=300)

    # List files in uploads folder
    upload_folder = 'uploads'
    files = [f for f in os.listdir(upload_folder) if f.endswith('.xlsx') or f.endswith('.xls')]

    if not files:
        st.write("No Excel files found in the uploads folder.")
        return

    # Allow user to select a file
    selected_file = st.selectbox("Select an Excel file", files)

    if selected_file:
        file_path = os.path.join(upload_folder, selected_file)

        try:
            # Try to read the Excel file content
            df = pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return

        # Show a preview of the selected file content
        st.write("Preview of the selected file:")
        st.dataframe(df, height=400)  # Set fixed height to allow scrolling

        # Add filters in the sidebar
        st.sidebar.header("Filter data:")
        st.sidebar.markdown("---")  # Add a dividing line for clarity
        filter_options = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_values = df[col].unique()
                selected_values = st.sidebar.multiselect(f"Select {col}", options=unique_values, default=unique_values)
                df = df[df[col].isin(selected_values)]
                filter_options[col] = selected_values

        # Chart fields and type selection
        st.sidebar.header("Chart Settings")
        st.sidebar.markdown("---")  # Add a dividing line for clarity
        chart_type = st.sidebar.selectbox("Chart type", ["Bar", "Pie"])
        x_axis = st.sidebar.selectbox("Select column for X-axis", df.columns)
        y_axis = st.sidebar.selectbox("Select column for Y-axis", df.columns)

        # Create chart based on user selection
        if chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{chart_type} of {y_axis} by {x_axis}", color=x_axis, color_discrete_sequence=px.colors.qualitative.Plotly)
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"{chart_type} of {y_axis} by {x_axis}", color_discrete_sequence=px.colors.qualitative.Plotly)

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
