import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Phân tích sinh viên TLU", layout="wide")

st.title("📊 Phân tích kết quả học tập sinh viên TLU")
st.write("Ứng dụng phục vụ bài tập lớn môn Lập trình khoa học dữ liệu")

# ======================
# LOAD DATA
# ======================
try:
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()
except:
    st.error("❌ Không tìm thấy file data.csv")
    st.stop()

# ======================
# CLEAN & STANDARDIZE DATA
# ======================

# 1. Xóa khoảng trắng tên cột
df.columns = df.columns.str.strip()

# 2. Xóa cột "Dấu thời gian" nếu tồn tại
if "Dấu thời gian" in df.columns:
    df = df.drop(columns=["Dấu thời gian"])

# 3. Đổi tên cột
df = df.rename(columns={
    "Bạn đang học năm mấy?": "NamHoc",
    "Một học kỳ bạn thường học bao nhiêu tín chỉ?": "TinChi",
    "Một kì bạn thường học bao nhiêu tín chỉ?": "TinChi",  # phòng trường hợp khác dấu
    "Bạn cảm thấy khối lượng học tập của mình:": "KhoiLuong",
    "GPA học kỳ gần nhất của bạn khoảng:": "GPA",
    "GPA học kì gần nhất của bạn khoảng:": "GPA",
    "Bạn đã từng học lại môn nào chưa?": "HocLai",
    "Khi học nhiều môn cùng lúc, kết quả của bạn:": "AnhHuong",
    "Trung bình mỗi ngày bạn dành bao nhiêu thời gian tự học?": "TuHoc",
    "Bạn đánh giá mức độ khó của học kỳ vừa rồi:": "DoKho"
})

# ======================
# MAPPING
# ======================

mapping_year = {
    "Năm 1": 1,
    "Năm 2": 2,
    "Năm 3": 3,
    "Năm 4": 4
}

mapping_credit = {
    "Dưới 14": 13,
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

# 4. Áp dụng mapping (ghi đè luôn cột)
df["NamHoc"] = df["NamHoc"].map(mapping_year)
df["TinChi"] = df["TinChi"].map(mapping_credit)
df["KhoiLuong"] = df["KhoiLuong"].map(mapping_khoiluong)

# 5. Xóa dữ liệu lỗi
df = df.dropna()

# 6. Hiển thị
st.subheader("📂 Dữ liệu sau khi làm sạch")
st.dataframe(df)


# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
