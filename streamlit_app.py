import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG + STYLE
# ======================
st.set_page_config(page_title="TLU Data Analysis", layout="wide")

st.markdown("""
<style>
.main-title {
    font-size:32px;
    font-weight:bold;
    text-align:center;
    color:#2c3e50;
}
.sub-title {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Dashboard phân tích kết quả học tập SV TLU</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Môn: Lập trình khoa học dữ liệu</div>', unsafe_allow_html=True)

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
df.columns = df.columns.str.strip()

if "Dấu thời gian" in df.columns:
    df = df.drop(columns=["Dấu thời gian"])

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

mapping_year = {"Năm 1":1,"Năm 2":2,"Năm 3":3,"Năm 4":4}
df["NamHoc"] = df["NamHoc"].map(mapping_year)
df = df.dropna()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.title("⚙️ Bộ lọc")

if st.sidebar.button("🔄 Reset"):
    st.rerun()

year_filter = st.sidebar.multiselect(
    "Năm học",
    sorted(df["NamHoc"].unique()),
    default=sorted(df["NamHoc"].unique())
)

credit_options = ["Dưới 14","14–16","17–19","20–22","Trên 22"]
gpa_options = ["Dưới 2.0","2.0 – 2.49","2.5 – 3.19","3.2 – 3.59","Trên 3.6"]

credit_filter = st.sidebar.multiselect("Tín chỉ", credit_options, default=credit_options)
gpa_filter = st.sidebar.multiselect("GPA", gpa_options, default=gpa_options)
khoiluong_filter = st.sidebar.multiselect("Khối lượng", df["KhoiLuong"].unique(), default=df["KhoiLuong"].unique())

# ======================
# FILTER DATA
# ======================
df_filtered = df[
    (df["NamHoc"].isin(year_filter)) &
    (df["TinChi"].isin(credit_filter)) &
    (df["GPA"].isin(gpa_filter)) &
    (df["KhoiLuong"].isin(khoiluong_filter))
]

# ======================
# 🔥 DATA SOURCE DUY NHẤT (QUAN TRỌNG)
# ======================
if "session_df" not in st.session_state:
    st.session_state.session_df = df_filtered.copy()
else:
    st.session_state.session_df = df_filtered.copy()

# ======================
# CRUD MODULE
# ======================
st.subheader("🛠️ CRUD dữ liệu (toàn dashboard)")

df_work = st.session_state.session_df

# -------- CREATE --------
with st.form("add_form"):
    st.markdown("### ➕ Thêm dữ liệu")

    namhoc = st.selectbox("Năm học", [1,2,3,4])
    tinchi = st.selectbox("Tín chỉ", credit_options)
    gpa = st.selectbox("GPA", gpa_options)
    khoiluong = st.selectbox("Khối lượng", df["KhoiLuong"].unique())
    tuhoc = st.selectbox("Thời gian tự học", df["TuHoc"].unique())
    do_kho = st.selectbox("Độ khó", df["DoKho"].unique())

    submit = st.form_submit_button("➕ Thêm")

    if submit:
        new_row = pd.DataFrame([{
            "NamHoc": namhoc,
            "TinChi": tinchi,
            "GPA": gpa,
            "KhoiLuong": khoiluong,
            "TuHoc": tuhoc,
            "DoKho": do_kho
        }])

        st.session_state.session_df = pd.concat([df_work, new_row], ignore_index=True)
        st.success("✔ Đã thêm dữ liệu")

# -------- UPDATE --------
st.markdown("### ✏️ Chỉnh sửa dữ liệu")

edited_df = st.data_editor(
    st.session_state.session_df,
    num_rows="dynamic",
    use_container_width=True
)

st.session_state.session_df = edited_df

# -------- DELETE --------
st.markdown("### 🗑️ Xoá dữ liệu")

idx = st.number_input(
    "Index dòng cần xoá",
    min_value=0,
    max_value=max(len(st.session_state.session_df)-1, 0)
)

if st.button("🗑️ Xoá"):
    st.session_state.session_df = st.session_state.session_df.drop(idx).reset_index(drop=True)
    st.success("✔ Đã xoá")

# ======================
# DATA VIEW
# ======================
st.markdown("### 📂 Dữ liệu toàn hệ thống")
st.dataframe(st.session_state.session_df)

# ======================
# KPI (FIXED)
# ======================
st.subheader("📌 Tổng quan")

data = st.session_state.session_df

col1, col2, col3 = st.columns(3)
col1.metric("👨‍🎓 Số SV", len(data))
col2.metric("📊 GPA phổ biến", data["GPA"].mode()[0])
col3.metric("⏱️ Tự học phổ biến", data["TuHoc"].mode()[0])

# ======================
# CHARTS (USE SESSION DATA)
# ======================

# GPA
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Phân bố GPA")
    fig1, ax1 = plt.subplots()
    sns.countplot(x=data["GPA"], order=gpa_options, ax=ax1)
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("📊 Phân bố tín chỉ")
    fig2, ax2 = plt.subplots()
    data["TinChi"].value_counts().reindex(credit_options).plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

# ======================
# TABLE FILTERED DATA
# ======================
with st.expander("📂 Xem dữ liệu"):
    st.dataframe(data)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("<center>👨‍💻 Sinh viên thực hiện: <b>Tên của bạn</b></center>", unsafe_allow_html=True)
