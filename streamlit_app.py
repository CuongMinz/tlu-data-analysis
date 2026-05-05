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
    df_raw = pd.read_csv("data.csv")
except:
    st.error("❌ Không tìm thấy file data.csv")
    st.stop()

# ======================
# CLEAN DATA
# ======================
df = df_raw.copy()

# 1. Xóa khoảng trắng
df.columns = df.columns.str.strip()

# 2. Xóa cột không cần
if "Dấu thời gian" in df.columns:
    df = df.drop(columns=["Dấu thời gian"])

# 3. Đổi tên cột
df = df.rename(columns={
    "Bạn đang học năm mấy?": "NamHoc",
    "Một học kỳ bạn thường học bao nhiêu tín chỉ?": "TinChi",
    "Một kì bạn thường học bao nhiêu tín chỉ?": "TinChi",
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
mapping_year = {"Năm 1":1,"Năm 2":2,"Năm 3":3,"Năm 4":4}
mapping_credit = {"Dưới 14":13,"14–16":15,"17–19":18,"20–22":21,"Trên 22":23}
mapping_gpa = {
    "Dưới 2.0":1.8,
    "2.0 – 2.49":2.25,
    "2.5 – 3.19":2.85,
    "3.2 – 3.59":3.4,
    "Trên 3.6":3.8
}

# Apply
df["NamHoc"] = df["NamHoc"].map(mapping_year)
df["TinChi"] = df["TinChi"].map(mapping_credit)
df["GPA_num"] = df["GPA"].map(mapping_gpa)

# Xóa NA
df = df.dropna()

# ======================
# HIỂN THỊ SAU CLEAN
# ======================
st.subheader("📊 Dữ liệu sau khi làm sạch")
st.dataframe(df)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Bộ lọc dữ liệu")

# Reset button
if st.sidebar.button("🔄 Reset bộ lọc"):
    st.experimental_rerun()

# Năm học
year_filter = st.sidebar.multiselect(
    "Năm học",
    options=sorted(df["NamHoc"].dropna().unique()),
    default=sorted(df["NamHoc"].dropna().unique())
)

# Tín chỉ
credit_filter = st.sidebar.multiselect(
    "Tín chỉ",
    options=sorted(df["TinChi"].dropna().unique()),
    default=sorted(df["TinChi"].dropna().unique())
)

# GPA
gpa_filter = st.sidebar.slider(
    "Khoảng GPA",
    float(df["GPA_num"].min()),
    float(df["GPA_num"].max()),
    (float(df["GPA_num"].min()), float(df["GPA_num"].max()))
)

# Tự học
study_filter = st.sidebar.slider(
    "Giờ tự học/ngày",
    float(df["TuHoc_num"].min()) if "TuHoc_num" in df.columns else 0,
    float(df["TuHoc_num"].max()) if "TuHoc_num" in df.columns else 5,
    (float(df["TuHoc_num"].min()), float(df["TuHoc_num"].max())) if "TuHoc_num" in df.columns else (0,5)
)

# Khối lượng (GIỮ TEXT)
khoiluong_filter = st.sidebar.multiselect(
    "Khối lượng học tập",
    options=df["KhoiLuong"].unique(),
    default=df["KhoiLuong"].unique()
)

# ======================
# APPLY FILTER
# ======================
df_filtered = df[
    (df["NamHoc"].isin(year_filter)) &
    (df["TinChi"].isin(credit_filter)) &
    (df["GPA_num"].between(gpa_filter[0], gpa_filter[1])) &
    (df["KhoiLuong"].isin(khoiluong_filter))
]

# Nếu có TuHoc_num thì lọc thêm
if "TuHoc_num" in df.columns:
    df_filtered = df_filtered[
        df_filtered["TuHoc_num"].between(study_filter[0], study_filter[1])
    ]


# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
