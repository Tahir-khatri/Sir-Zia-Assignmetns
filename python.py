import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Theme selector
theme = st.sidebar.radio("Choose Theme", ["Dark", "Light"])

# Custom CSS with dynamic theming
theme_css = """
<style>
.stApp {background-color: %s; color: %s !important;}
.stButton button, .stDownloadButton button {background-color: %s !important; color: white;}
.stSelectbox, .stMultiSelect, .stSidebar {background-color: %s; color: %s;}
.stDataFrame, div[data-testid="stMarkdownContainer"], .element-container, [data-testid="stAppViewContainer"] > * {color: %s !important;}
</style>
""" % (
    "black" if theme == "Dark" else "white",
    "white" if theme == "Dark" else "black",
    "#ff4b4b" if theme == "Dark" else "#4CAF50",
    "#262730" if theme == "Dark" else "#f0f0f0",
    "white" if theme == "Dark" else "black",
    "white" if theme == "Dark" else "black"
)

st.markdown(theme_css, unsafe_allow_html=True)

# Title and description
st.title("DataSweeper Sterling Integrator By Muhammad Tahir")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = file.name.split(".")[-1].lower()
        if file_ext == "csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File data
        st.write(f"🔍 Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed successfully!")
            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    df.fillna(df.mean(numeric_only=True), inplace=True)
                    st.write("✅ Missing values filled successfully!")

        # Select columns
        st.subheader("🎯 Select Columns to Keep")
        selected_columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.rsplit(".", 1)[0] + (".csv" if conversion_type == "CSV" else ".xlsx")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False)

            buffer.seek(0)
            st.download_button(f"Download {file.name} as {conversion_type}", data=buffer, file_name=file_name, mime=mime_type)

st.success("🎉 All files processed successfully!")
