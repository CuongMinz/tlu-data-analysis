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
# 🔍 SEARCH DATA
# ======================
st.subheader("🔍 Tìm kiếm dữ liệu")

keyword = st.text_input("Nhập từ khóa (năm, GPA, tín chỉ, tự học...)")

search_df = st.session_state.session_df.copy()

if keyword:
    search_df = search_df[
        search_df.astype(str).apply(
            lambda row: row.str.contains(keyword, case=False).any(),
            axis=1
        )
    ]

st.dataframe(search_df)


# ======================
# 📤 EXPORT DATA
# ======================
st.subheader("📤 Xuất dữ liệu")

csv_data = st.session_state.session_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Tải file CSV",
    data=csv_data,
    file_name="tlu_dashboard_data.csv",
    mime="text/csv"
)


# ======================
# KPI 
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
# NĂM HỌC vs TÍN CHỈ 
# ======================
st.subheader("📊 Tỷ lệ đăng ký tín chỉ theo năm học")

cross_tab = pd.crosstab(data["NamHoc"], data["TinChi"])

year_order = [1, 2, 3, 4]
tinchi_order = ["Dưới 14", "14–16", "17–19", "20–22", "Trên 22"]

cross_tab = cross_tab.reindex(index=year_order, columns=tinchi_order, fill_value=0)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(8,5))

cross_tab_percent.plot(kind="bar", stacked=True, ax=ax)

ax.set_xlabel("Năm học")
ax.set_ylabel("Tỷ lệ (%)")
ax.set_title("Tỷ lệ số tín chỉ theo từng năm học")

ax.set_xticklabels(["Năm 1", "Năm 2", "Năm 3", "Năm 4"], rotation=0)
ax.legend(title="Tín chỉ", bbox_to_anchor=(1.05, 1), loc='upper left')

# hiển thị %
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
                fontsize=8
            )
            cumulative += value

st.pyplot(fig)


# ======================
# TÍN CHỈ vs KHỐI LƯỢNG (100% STACKED)
# ======================
st.subheader("📊 Tỷ lệ cảm nhận khối lượng theo số tín chỉ")

cross_tab = pd.crosstab(data["TinChi"], data["KhoiLuong"])

tinchi_order = ["Dưới 14", "14–16", "17–19", "20–22", "Trên 22"]
khoiluong_order = ["Nhẹ", "Vừa phải", "Hơi nặng", "Rất nặng"]

cross_tab = cross_tab.reindex(
    index=tinchi_order,
    columns=khoiluong_order,
    fill_value=0
)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(8,5))

cross_tab_percent.plot(kind="bar", stacked=True, ax=ax)

ax.set_xlabel("Số tín chỉ")
ax.set_ylabel("Tỷ lệ (%)")
ax.set_title("Ảnh hưởng của số tín chỉ đến khối lượng học tập")

plt.xticks(rotation=0)
ax.legend(title="Khối lượng", bbox_to_anchor=(1.05, 1), loc='upper left')

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
# TỰ HỌC vs GPA 
# ======================
st.subheader("📊 Ảnh hưởng của thời gian tự học đến GPA")

cross_tab = pd.crosstab(data["TuHoc"], data["GPA"])

tuhoc_order = ["Dưới 1 giờ", "1–2 giờ", "2–4 giờ", "Trên 4 giờ"]
gpa_order = ["Dưới 2.0", "2.0 – 2.49", "2.5 – 3.19", "3.2 – 3.59"]

cross_tab = cross_tab.reindex(index=tuhoc_order, columns=gpa_order, fill_value=0)

cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(8,5))

cross_tab_percent.plot(kind="bar", stacked=True, ax=ax)

ax.set_xlabel("Thời gian tự học")
ax.set_ylabel("Tỷ lệ (%)")
ax.set_title("Tỷ lệ GPA theo thời gian tự học")

plt.xticks(rotation=0)
ax.legend(title="GPA", bbox_to_anchor=(1.05, 1), loc='upper left')

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
                fontsize=8
            )
            cumulative += value

st.pyplot(fig)



# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("<center>👨‍💻 Sinh viên thực hiện: <b>Tên của bạn</b></center>", unsafe_allow_html=True)
