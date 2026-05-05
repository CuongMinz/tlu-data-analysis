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
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset"):
    st.rerun()

year_filter = st.sidebar.multiselect(
    "Năm học",
    sorted(df["NamHoc"].unique()),
    default=sorted(df["NamHoc"].unique())
)

credit_options = ["Dưới 14","14–16","17–19","20–22","Trên 22"]
credit_filter = st.sidebar.multiselect("Tín chỉ", credit_options, default=credit_options)

gpa_options = ["Dưới 2.0","2.0 – 2.49","2.5 – 3.19","3.2 – 3.59","Trên 3.6"]
gpa_filter = st.sidebar.multiselect("GPA", gpa_options, default=gpa_options)

khoiluong_filter = st.sidebar.multiselect(
    "Khối lượng",
    df["KhoiLuong"].unique(),
    default=df["KhoiLuong"].unique()
)

df_filtered = df[
    (df["NamHoc"].isin(year_filter)) &
    (df["TinChi"].isin(credit_filter)) &
    (df["GPA"].isin(gpa_filter)) &
    (df["KhoiLuong"].isin(khoiluong_filter))
]

# ======================
# KPI
# ======================
st.subheader("📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric("👨‍🎓 Số SV", len(df_filtered))
col2.metric("📊 GPA phổ biến", df_filtered["GPA"].mode()[0])
col3.metric("⏱️ Tự học phổ biến", df_filtered["TuHoc"].mode()[0])

# ======================
# DATA
# ======================
with st.expander("📂 Xem dữ liệu"):
    st.dataframe(df_filtered)

# ======================
# GPA + PIE
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Phân bố GPA")
    fig1, ax1 = plt.subplots()
    sns.countplot(
        x=df_filtered["GPA"],
        order=gpa_options,
        ax=ax1
    )
    for p in ax1.patches:
        ax1.annotate(int(p.get_height()),
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom')
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("📊 Phân bố tín chỉ")
    fig2, ax2 = plt.subplots()
    df_filtered["TinChi"].value_counts().reindex(credit_options).plot(
        kind="pie", autopct="%1.1f%%", ax=ax2
    )
    ax2.set_ylabel("")
    st.pyplot(fig2)

# ======================
# NĂM HỌC → TÍN CHỈ
# ======================
st.markdown("---")
st.subheader("📊 Năm học → Tín chỉ")

cross_tab = pd.crosstab(df_filtered["NamHoc"], df_filtered["TinChi"])
cross_tab = cross_tab.reindex(index=[1,2,3,4], columns=credit_options, fill_value=0)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig3, ax3 = plt.subplots(figsize=(8,5))
cross_tab_percent.plot(kind="bar", stacked=True, ax=ax3)

ax3.set_xticklabels(["Năm 1","Năm 2","Năm 3","Năm 4"], rotation=0)
ax3.set_ylabel("Tỷ lệ")
ax3.legend(title="Tín chỉ", bbox_to_anchor=(1.05,1))

st.pyplot(fig3)

# ======================
# TÍN CHỈ → KHỐI LƯỢNG
# ======================
st.subheader("📊 Tín chỉ → Khối lượng")

cross_tab = pd.crosstab(df_filtered["TinChi"], df_filtered["KhoiLuong"])
cross_tab = cross_tab.reindex(index=credit_options,
                             columns=["Nhẹ","Vừa phải","Hơi nặng","Rất nặng"],
                             fill_value=0)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig4, ax4 = plt.subplots(figsize=(8,5))
cross_tab_percent.plot(kind="bar", stacked=True, ax=ax4)

ax4.set_ylabel("Tỷ lệ")
ax4.legend(title="Khối lượng", bbox_to_anchor=(1.05,1))

st.pyplot(fig4)

# ======================
# TỰ HỌC → GPA
# ======================
st.subheader("📊 Tự học → GPA")

tuhoc_order = ["Dưới 1 giờ","1–2 giờ","2–4 giờ","Trên 4 giờ"]
gpa_order = ["Dưới 2.0","2.0 – 2.49","2.5 – 3.19","3.2 – 3.59"]

cross_tab = pd.crosstab(df_filtered["TuHoc"], df_filtered["GPA"])
cross_tab = cross_tab.reindex(index=tuhoc_order, columns=gpa_order, fill_value=0)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig5, ax5 = plt.subplots(figsize=(8,5))
cross_tab_percent.plot(kind="bar", stacked=True, ax=ax5)

ax5.set_ylabel("Tỷ lệ")
ax5.legend(title="GPA", bbox_to_anchor=(1.05,1))

st.pyplot(fig5)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("<center>👨‍💻 Sinh viên thực hiện: <b>Tên của bạn</b></center>", unsafe_allow_html=True)
