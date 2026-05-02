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

# ======================
# CLEAN DATA
# ======================

# Mapping
mapping_year = {
    "Năm 1": 1,
    "Năm 2": 2,
    "Năm 3": 3,
    "Năm 4": 4
}

mapping_credit = {
    "Dưới 14": 12,
    "14–16": 15,
    "17–19": 18,
    "20–22": 21,
    "Trên 22": 23
}

mapping_khoiluong = {
    "Nhẹ": 1,
    "Vừa phải": 2,
    "Hơi nặng": 3,
    "Rất nặng": 4
}

# Apply
df["NamHoc"] = df["Bạn đang học năm mấy?"].map(mapping_year)
df["TinChi"] = df["Một học kỳ bạn thường học bao nhiêu tín chỉ?"].map(mapping_credit)
df["KhoiLuong"] = df["Bạn cảm thấy khối lượng học tập của mình:"].map(mapping_khoiluong)

st.subheader("📊 Dữ liệu sau khi chuẩn hóa")
st.dataframe(df)
