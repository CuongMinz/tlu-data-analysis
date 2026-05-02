import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
df["NamHoc"] = df["Bạn đang học năm mấy?"].map(mapping_year)
df["TinChi"] = df["Một học kỳ bạn thường học bao nhiêu tín chỉ?"].map(mapping_credit)
df["KhoiLuong"] = df["Bạn cảm thấy khối lượng học tập của mình:"].map(mapping_khoiluong)

# 5. Xóa dữ liệu lỗi (nếu có)
df = df.dropna()

# 6. Hiển thị dữ liệu sau khi clean
st.subheader("📊 Dữ liệu sau khi chuẩn hóa")
st.dataframe(df)

# ======================
# Trực quan hóa DL
# ======================

st.subheader("📈 Trực quan hóa dữ liệu")

# ======================
# 1. Bar chart: Số SV theo năm học
# ======================
st.write("### 📊 Số sinh viên theo năm học")

fig1, ax1 = plt.subplots()
df["NamHoc"].value_counts().sort_index().plot(kind="bar", ax=ax1)
ax1.set_xlabel("Năm học")
ax1.set_ylabel("Số lượng")
st.pyplot(fig1)


# ======================
# 2. Histogram: Phân bố tín chỉ
# ======================
st.write("### 📊 Phân bố số tín chỉ")

fig2, ax2 = plt.subplots()
sns.histplot(df["TinChi"], bins=5, kde=True, ax=ax2)
st.pyplot(fig2)


# ======================
# 3. Boxplot: Khối lượng học tập
# ======================
st.write("### 📊 Boxplot khối lượng học tập")

fig3, ax3 = plt.subplots()
sns.boxplot(x=df["KhoiLuong"], ax=ax3)
st.pyplot(fig3)


# ======================
# 4. Pie chart: Cảm nhận khối lượng
# ======================
st.write("### 📊 Tỉ lệ khối lượng học tập")

khoiluong_counts = df["KhoiLuong_text"].value_counts()

fig4, ax4 = plt.subplots()
khoiluong_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax4)
st.pyplot(fig4)


# ======================
# 5. Bar chart: Tín chỉ trung bình theo năm học
# ======================
st.write("### 📊 Tín chỉ trung bình theo năm học")

avg_credit = df.groupby("NamHoc")["TinChi"].mean()

fig5, ax5 = plt.subplots()
avg_credit.plot(kind="bar", ax=ax5)
ax5.set_ylabel("Tín chỉ trung bình")
st.pyplot(fig5)
