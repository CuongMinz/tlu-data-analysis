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

# Apply
df["NamHoc"] = df["NamHoc"].map(mapping_year)

# Xóa NA
df = df.dropna()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Bộ lọc dữ liệu")

if st.sidebar.button("🔄 Reset bộ lọc"):
    st.rerun()

# Năm học
year_filter = st.sidebar.multiselect(
    "Năm học",
    options=sorted(df["NamHoc"].unique()),
    default=sorted(df["NamHoc"].unique())
)

# Tín chỉ
credit_filter = st.sidebar.multiselect(
    "Tín chỉ",
    options=[
        "Dưới 14",
        "14–16",
        "17–19",
        "20–22",
        "Trên 22"
    ],
    default=[
        "Dưới 14",
        "14–16",
        "17–19",
        "20–22",
        "Trên 22"
    ]
)

# GPA 
gpa_filter = st.sidebar.multiselect(
    "Mức GPA",
    options=[
        "Dưới 2.0",
        "2.0 – 2.49",
        "2.5 – 3.19",
        "3.2 – 3.59",
        "Trên 3.6"
    ],
    default=[
        "Dưới 2.0",
        "2.0 – 2.49",
        "2.5 – 3.19",
        "3.2 – 3.59",
        "Trên 3.6"
    ]
)

# Khối lượng
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
    (df["GPA"].isin(gpa_filter)) &
    (df["KhoiLuong"].isin(khoiluong_filter))
]

# ======================
# HIỂN THỊ
# ======================
st.subheader("📊 Dữ liệu sau khi lọc")
st.write(f"🔍 Số sinh viên: {len(df_filtered)}")
st.dataframe(df_filtered)


# ======================
# BIỂU ĐỒ PHÂN BỐ GPA
# ======================
st.subheader("📊 Phân bố điểm GPA học kỳ")

fig, ax = plt.subplots()

sns.countplot(
    x=df_filtered["GPA"],
    order=[
        "Dưới 2.0",
        "2.0 – 2.49",
        "2.5 – 3.19",
        "3.2 – 3.59",
        "Trên 3.6"
    ],
    ax=ax
)

ax.set_xlabel("Mức GPA")
ax.set_ylabel("Số sinh viên")

# Hiển thị số trên cột
for p in ax.patches:
    ax.annotate(
        str(int(p.get_height())),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='bottom'
    )

st.pyplot(fig)


# ======================
# NĂM HỌC VÀ TÍN CHỈ
# ======================
st.subheader("📊 Tỷ lệ tín chỉ theo năm học")

# Tính %
cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig2, ax2 = plt.subplots(figsize=(8,5))

cross_tab_percent.plot(
    kind="bar",
    stacked=True,
    ax=ax2
)

# Format
ax2.set_xlabel("Năm học")
ax2.set_ylabel("Tỷ lệ (%)")
ax2.set_title("Tỷ lệ đăng ký tín chỉ theo năm học")

ax2.set_xticklabels(["Năm 1", "Năm 2", "Năm 3", "Năm 4"], rotation=0)
ax2.legend(title="Tín chỉ", bbox_to_anchor=(1.05, 1), loc='upper left')

# Hiển thị %
for i in range(len(cross_tab_percent)):
    cumulative = 0
    for j in range(len(cross_tab_percent.columns)):
        value = cross_tab_percent.iloc[i, j]
        if value > 0:
            ax2.text(
                i,
                cumulative + value/2,
                f"{value*100:.0f}%",
                ha='center',
                va='center',
                fontsize=8
            )
            cumulative += value

st.pyplot(fig2)


# ======================
# PIE CHART TÍN CHỈ
# ======================
st.subheader("📊 Phân bố số tín chỉ")

# Đếm số lượng
tinchi_counts = df_filtered["TinChi"].value_counts()

# Sắp xếp đúng thứ tự
tinchi_counts = tinchi_counts.reindex(
    ["Dưới 14", "14–16", "17–19", "20–22"]
).fillna(0)

# Vẽ biểu đồ
fig, ax = plt.subplots()

ax.pie(
    tinchi_counts,
    labels=tinchi_counts.index,
    autopct='%1.1f%%',
    startangle=90
)

ax.set_title("Tỷ lệ số tín chỉ sinh viên đăng ký")

st.pyplot(fig)


# ======================
# TÍN CHỈ vs KHỐI LƯỢNG (%)
# ======================
st.subheader("📊 Tỷ lệ cảm nhận khối lượng theo số tín chỉ")

# Tạo bảng chéo
cross_tab = pd.crosstab(df_filtered["TinChi"], df_filtered["KhoiLuong"])

# Chuẩn hóa thứ tự
tinchi_order = ["Dưới 14", "14–16", "17–19", "20–22", "Trên 22"]
khoiluong_order = ["Nhẹ", "Vừa phải", "Hơi nặng", "Rất nặng"]

cross_tab = cross_tab.reindex(
    index=tinchi_order,
    columns=khoiluong_order,
    fill_value=0
)

# Chuyển sang %
cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(8,5))

cross_tab_percent.plot(
    kind="bar",
    stacked=True,
    ax=ax
)

# Format
ax.set_xlabel("Số tín chỉ")
ax.set_ylabel("Tỷ lệ (%)")
ax.set_title("Ảnh hưởng của số tín chỉ đến cảm nhận khối lượng học tập")

plt.xticks(rotation=0)
ax.legend(title="Khối lượng", bbox_to_anchor=(1.05, 1), loc='upper left')

# Hiển thị % trên cột
for i in range(len(cross_tab_percent)):
    cumulative = 0
    for j in range(len(cross_tab_percent.columns)):
        value = cross_tab_percent.iloc[i, j]
        if value > 0:
            ax.text(
                i,
                cumulative + value/2,
                f"{value*100:.0f}%",
                ha='center',
                va='center',
                fontsize=8,
                color='black'
            )
            cumulative += value

st.pyplot(fig)

# ======================
# CROSSTAB GPA vs TỰ HỌC
# ======================
st.subheader("📊 Phân bố GPA theo thời gian tự học")


# Tạo bảng chéo
cross_tab = pd.crosstab(df_filtered["GPA"], df_filtered["TuHoc"])

# Sắp xếp lại thứ tự cột
cross_tab = cross_tab.reindex(
    columns=["Dưới 1 giờ", "1–2 giờ", "2–4 giờ", "Trên 4 giờ"]
)

# Vẽ biểu đồ
fig, ax = plt.subplots()

cross_tab.plot(kind='bar', ax=ax)

ax.set_title("Phân bố GPA theo thời gian tự học")
ax.set_xlabel("Mức GPA")
ax.set_ylabel("Số sinh viên")

plt.xticks(rotation=45)

st.pyplot(fig)


# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
