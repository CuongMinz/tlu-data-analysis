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

# Apply
df["NamHoc"] = df["NamHoc"].map(mapping_year)
df["TinChi"] = df["TinChi"].map(mapping_credit)

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
    options=sorted(df["TinChi"].unique()),
    default=sorted(df["TinChi"].unique())
)

# GPA (TEXT)
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
# BIỂU ĐỒ NHẬN XÉT 1
# ======================
st.subheader("📊 Mối quan hệ giữa GPA và thời gian tự học")

fig, ax = plt.subplots()

cross_tab.plot(kind="bar", ax=ax)

ax.set_xlabel("Thời gian tự học")
ax.set_ylabel("Số sinh viên")
ax.set_title("Ảnh hưởng của tự học đến kết quả học tập")

st.pyplot(fig)


# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("👨‍💻 Sinh viên thực hiện: **[Tên của bạn]**")
