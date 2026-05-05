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

mapping_gpa = {
    "Dưới 2.0": 1.8,
    "2.0 – 2.49": 2.25,
    "2.5 – 3.19": 2.85,
    "3.2 – 3.59": 3.4,
    "Trên 3.6": 3.8,
    "3.6+": 3.8
}

mapping_tuhoc = {
    "Dưới 1 giờ": 0.5,
    "1–2 giờ": 1.5,
    "2–4 giờ": 3,
    "Trên 4 giờ": 5
}

# ======================
# APPLY
# ======================

df["NamHoc"] = df["NamHoc"].map(mapping_year)
df["TinChi"] = df["TinChi"].map(mapping_credit)
df["KhoiLuong"] = df["KhoiLuong"].map(mapping_khoiluong)

df["GPA_num"] = df["GPA"].map(mapping_gpa)
df["TuHoc_num"] = df["TuHoc"].map(mapping_tuhoc)

# Xóa dữ liệu lỗi
df = df.dropna()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Bộ lọc")

year_filter = st.sidebar.multiselect(
    "Năm học",
    options=sorted(df["NamHoc"].unique()),
    default=sorted(df["NamHoc"].unique())
)

credit_filter = st.sidebar.multiselect(
    "Tín chỉ",
    options=sorted(df["TinChi"].unique()),
    default=sorted(df["TinChi"].unique())
)

gpa_filter = st.sidebar.slider(
    "GPA",
    float(df["GPA_num"].min()),
    float(df["GPA_num"].max()),
    (float(df["GPA_num"].min()), float(df["GPA_num"].max()))
)

study_filter = st.sidebar.slider(
    "Giờ tự học",
    float(df["TuHoc_num"].min()),
    float(df["TuHoc_num"].max()),
    (float(df["TuHoc_num"].min()), float(df["TuHoc_num"].max()))
)

# Apply filter
df_filtered = df[
    (df["NamHoc"].isin(year_filter)) &
    (df["TinChi"].isin(credit_filter)) &
    (df["GPA_num"].between(gpa_filter[0], gpa_filter[1])) &
    (df["TuHoc_num"].between(study_filter[0], study_filter[1]))
]

# ======================
# KPI
# ======================
st.subheader("📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric("👨‍🎓 Số SV", len(df_filtered))
col2.metric("📚 Tín chỉ TB", round(df_filtered["TinChi"].mean(), 2))
col3.metric("🎯 GPA TB", round(df_filtered["GPA_num"].mean(), 2))

# ======================
# HIỂN THỊ DATA
# ======================
st.subheader("📂 Dữ liệu sau khi làm sạch")
st.dataframe(df_filtered)


# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
