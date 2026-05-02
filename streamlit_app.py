import streamlit as st
import pandas as pd

st.set_page_config(page_title="Phân tích sinh viên TLU", layout="centered")

st.title("📊 Phân tích kết quả học tập sinh viên TLU")

st.write("Ứng dụng phục vụ bài tập lớn môn Lập trình khoa học dữ liệu")

# ======================
# LOAD DATA
# ======================
try:
    df = pd.read_csv("data.csv")
    
    st.subheader("📂 Dữ liệu khảo sát")
    st.dataframe(df)

except:
    st.error("❌ Không tìm thấy file data.csv")
