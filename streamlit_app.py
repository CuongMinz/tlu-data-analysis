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

# Mapping
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

# Apply mapping (an toàn hơn với .get)
df["NamHoc"] = df["Bạn đang học năm mấy?"].map(mapping_year)
df["TinChi"] = df["Một học kỳ bạn thường học bao nhiêu tín chỉ?"].map(mapping_credit)
df["KhoiLuong"] = df["Bạn cảm thấy khối lượng học tập của mình:"].map(mapping_khoiluong)

# Drop NA
df = df.dropna()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Bộ lọc")

selected_year = st.sidebar.multiselect(
    "Chọn năm học",
    options=sorted(df["NamHoc"].unique()),
    default=sorted(df["NamHoc"].unique())
)

df_filtered = df[df["NamHoc"].isin(selected_year)]

# ======================
# KPI
# ======================
st.subheader("📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric("👨‍🎓 Số SV", len(df_filtered))
col2.metric("📚 Tín chỉ TB", round(df_filtered["TinChi"].mean(), 2))
col3.metric("⚖️ Khối lượng TB", round(df_filtered["KhoiLuong"].mean(), 2))

# ======================
# HIỂN THỊ DATA
# ======================
st.subheader("📂 Dữ liệu sau khi chuẩn hóa")
st.dataframe(df_filtered)

# ======================
# TRỰC QUAN HÓA
# ======================
st.subheader("📈 Trực quan hóa dữ liệu")

col1, col2 = st.columns(2)

# 1. Bar chart
with col1:
    st.write("### Số sinh viên theo năm học")
    fig1, ax1 = plt.subplots()
    df_filtered["NamHoc"].value_counts().sort_index().plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Năm học")
    ax1.set_ylabel("Số lượng")
    st.pyplot(fig1)

# 2. Histogram
with col2:
    st.write("### Phân bố số tín chỉ")
    fig2, ax2 = plt.subplots()
    sns.histplot(df_filtered["TinChi"], bins=5, kde=True, ax=ax2)
    st.pyplot(fig2)

col3, col4 = st.columns(2)

# 3. Boxplot
with col3:
    st.write("### Boxplot khối lượng học tập")
    fig3, ax3 = plt.subplots()
    sns.boxplot(x=df_filtered["KhoiLuong"], ax=ax3)
    st.pyplot(fig3)

# 4. Pie chart
with col4:
    st.write("### Tỉ lệ khối lượng học tập")
    khoiluong_counts = df_filtered["Bạn cảm thấy khối lượng học tập của mình:"].value_counts()
    fig4, ax4 = plt.subplots()
    khoiluong_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax4)
    st.pyplot(fig4)

# ======================
# 5. Bar chart cuối
# ======================
st.write("### 📊 Tín chỉ trung bình theo năm học")

avg_credit = df_filtered.groupby("NamHoc")["TinChi"].mean()

fig5, ax5 = plt.subplots()
avg_credit.plot(kind="bar", ax=ax5)
ax5.set_ylabel("Tín chỉ trung bình")
st.pyplot(fig5)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
