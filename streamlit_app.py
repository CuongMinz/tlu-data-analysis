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
# CLEAN & STANDARDIZE DATA
# ======================

# 1. Xóa khoảng trắng trong tên cột
df.columns = df.columns.str.strip()

# 2. Đổi tên cột cho dễ dùng
df = df.rename(columns={
    "Bạn đang học năm mấy?": "NamHoc_text",
    "Một học kỳ bạn thường học bao nhiêu tín chỉ?": "TinChi_text",
    "Bạn cảm thấy khối lượng học tập của mình:": "KhoiLuong_text"
})

# 3. Mapping dữ liệu
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
    "20–22": 21
}

mapping_khoiluong = {
    "Nhẹ": 1,
    "Vừa phải": 2,
    "Hơi nặng": 3,
    "Rất nặng": 4
}

# 4. Áp dụng mapping
df["NamHoc"] = df["NamHoc_text"].map(mapping_year)
df["TinChi"] = df["TinChi_text"].map(mapping_credit)
df["KhoiLuong"] = df["KhoiLuong_text"].map(mapping_khoiluong)

# 5. Xóa dữ liệu lỗi (nếu có)
df = df.dropna()

# 6. Hiển thị dữ liệu sau khi clean
st.subheader("📊 Dữ liệu sau khi chuẩn hóa")
st.dataframe(df)
