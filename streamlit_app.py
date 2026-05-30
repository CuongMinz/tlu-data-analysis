import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# CONFIG + STYLE
st.set_page_config(
    page_title="Student GPA Analysis",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    color: #1f2937;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: gray;
    font-size: 18px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #111827;
    margin-top: 30px;
    margin-bottom: 15px;
}

.metric-card {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">PHÂN TÍCH KẾT QUẢ HỌC TẬP CỦA SINH VIÊN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Lập trình khoa học dữ liệu</div>',
    unsafe_allow_html=True
)


# LOAD DATA
try:
    df_raw = pd.read_csv("data.csv")

except:
    st.error("❌ Không tìm thấy file data.csv")
    st.stop()


# CLEAN DATA
df = df_raw.copy()

df.columns = df.columns.str.strip()

if "Age" in df.columns:
    df = df.drop(columns=["Age"])

if "Ethnicity" in df.columns:
    df = df.drop(columns=["Ethnicity"])

if "ParentalEducation" in df.columns:
    df = df.drop(columns=["ParentalEducation"])

df = df.drop_duplicates()

df = df.dropna()


# CONVERT DATA TYPES
binary_cols = [
    "Gender",
    "Tutoring",
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]

for col in binary_cols:
    if col in df.columns:
        df[col] = df[col].astype(int)


# SIDEBAR FILTER
st.sidebar.title("⚙️ Lọc dữ liệu")

if st.sidebar.button("🔄 Reset"):
    st.rerun()

gender_filter = st.sidebar.multiselect(
    "Gender",
    [0, 1],
    default=[0, 1]
)

grade_filter = st.sidebar.multiselect(
    "Grade Class",
    sorted(df["GradeClass"].unique()),
    default=sorted(df["GradeClass"].unique())
)


# FILTER DATA
df_filtered = df[
    (df["Gender"].isin(gender_filter)) &
    (df["GradeClass"].isin(grade_filter))
]


# SESSION DATA
if "session_df" not in st.session_state:
    st.session_state.session_df = df_filtered.copy()
else:
    st.session_state.session_df = df_filtered.copy()


# CRUD MODULE
st.markdown(
    '<p class="section-title">🛠️ CRUD Management</p>',
    unsafe_allow_html=True
)

df_work = st.session_state.session_df


# CREATE DATA
with st.form("add_form"):

    st.markdown("### ➕ Thêm sinh viên mới")

    col1, col2 = st.columns(2)

    with col1:
        student_id = st.number_input(
            "Student ID",
            min_value=1000,
            step=1
        )

        gender = st.selectbox(
            "Gender",
            [0, 1],
            help="0 = Female, 1 = Male"
        )

        study_time = st.number_input(
            "Study Time Weekly",
            min_value=0.0,
            max_value=40.0,
            step=0.5
        )

        absences = st.number_input(
            "Absences",
            min_value=0,
            max_value=50,
            step=1
        )

        tutoring = st.selectbox(
            "Tutoring",
            [0, 1]
        )

    with col2:
        parental_support = st.slider(
            "Parental Support",
            min_value=0,
            max_value=4,
            step=1
        )

        extracurricular = st.selectbox(
            "Extracurricular",
            [0, 1]
        )

        sports = st.selectbox(
            "Sports",
            [0, 1]
        )

        music = st.selectbox(
            "Music",
            [0, 1]
        )

        volunteering = st.selectbox(
            "Volunteering",
            [0, 1]
        )

        gpa = st.number_input(
            "GPA",
            min_value=0.0,
            max_value=4.0,
            step=0.01
        )

        grade_class = st.selectbox(
            "Grade Class",
            [0, 1, 2, 3, 4]
        )
    submit = st.form_submit_button("➕ Thêm sinh viên")
    if submit:
        new_row = pd.DataFrame([{
            "StudentID": student_id,
            "Gender": gender,
            "StudyTimeWeekly": study_time,
            "Absences": absences,
            "Tutoring": tutoring,
            "ParentalSupport": parental_support,
            "Extracurricular": extracurricular,
            "Sports": sports,
            "Music": music,
            "Volunteering": volunteering,
            "GPA": gpa,
            "GradeClass": grade_class
        }])

        st.session_state.session_df = pd.concat(
            [df_work, new_row],
            ignore_index=True
        )

        st.success("✔ Thêm sinh viên thành công")


# UPDATE DATA
st.markdown("### ✏️ Chỉnh sửa dữ liệu")

edited_df = st.data_editor(
    st.session_state.session_df,
    num_rows="dynamic",
    use_container_width=True
)

st.session_state.session_df = edited_df


# DELETE DATA
st.markdown("### 🗑️ Xóa hàng")

idx = st.number_input(
    "Chọn hàng muốn xóa",
    min_value=0,
    max_value=max(len(st.session_state.session_df)-1, 0),
    step=1
)

if st.button("🗑️ Delete"):

    st.session_state.session_df = (
        st.session_state.session_df
        .drop(idx)
        .reset_index(drop=True)
    )

    st.success("✔ Xóa hàng thành công!")


# DATA VIEW
st.markdown(
    '<p class="section-title">📂 Bảng dữ liệu hiện tại</p>',
    unsafe_allow_html=True
)

st.dataframe(
    st.session_state.session_df,
    use_container_width=True
)


# SEARCH DATA
st.markdown(
    '<p class="section-title">🔍 Tìm kiếm dữ liệu</p>',
    unsafe_allow_html=True
)

keyword = st.text_input(
    "Tìm kiếm theo GPA, study time, absences, activities..."
)

search_df = st.session_state.session_df.copy()

if keyword:

    search_df = search_df[
        search_df.astype(str).apply(
            lambda row: row.str.contains(
                keyword,
                case=False
            ).any(),
            axis=1
        )
    ]

st.dataframe(
    search_df,
    use_container_width=True
)


# EXPORT DỮ LIỆU RA FILE CSV
st.markdown(
    '<p class="section-title">📤 Xuất dữ liệu</p>',
    unsafe_allow_html=True
)

csv_data = (
    st.session_state.session_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="student_gpa_analysis.csv",
    mime="text/csv"
)


# KPI
st.markdown(
    '<p class="section-title">📌 Tổng quan</p>',
    unsafe_allow_html=True
)

data = st.session_state.session_df

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🎓 Số sinh viên",
        len(data)
    )

with col2:
    st.metric(
        "📊 Điểm GPA trung bình",
        round(data["GPA"].mean(), 2)
    )

with col3:
    st.metric(
        "📚 Thời gian học trung bình",
        round(data["StudyTimeWeekly"].mean(), 2)
    )

with col4:
    st.metric(
        "❌ Số buổi nghỉ trung bình",
        round(data["Absences"].mean(), 2)
    )



# STEP 1 - TỔNG QUAN GPA
st.markdown("---")

st.header("Bước 1: Tổng quan phân bố GPA")

st.write("""
Biểu đồ Histogram giúp quan sát phân bố GPA của sinh viên.
Từ đó có thể đánh giá:
- GPA tập trung ở mức nào
- Dữ liệu có bị lệch hay không
- Sinh viên đạt GPA cao hay thấp chiếm đa số
""")


# HISTOGRAM GPA
fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    data=st.session_state.session_df,
    x="GPA",
    bins=15,
    kde=True,
    ax=ax
)

ax.set_title(
    "Phân bố GPA của sinh viên",
    fontsize=16,
    fontweight='bold'
)

ax.set_xlabel("GPA")
ax.set_ylabel("Số lượng sinh viên")

ax.grid(
    alpha=0.3,
    linestyle="--"
)
st.pyplot(fig)


# GPA SUMMARY
st.markdown("### 📌 Thống kê GPA")

gpa_data = st.session_state.session_df["GPA"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "GPA trung bình",
    round(gpa_data.mean(), 2)
)

col2.metric(
    "GPA cao nhất",
    round(gpa_data.max(), 2)
)

col3.metric(
    "GPA thấp nhất",
    round(gpa_data.min(), 2)
)

col4.metric(
    "GPA trung vị",
    round(gpa_data.median(), 2)
)


# INTERPRETATION
st.info("""
📖 Nhận xét:

• GPA của sinh viên phân bố chủ yếu trong khoảng từ 1.0 đến 3.0.

• Nhóm sinh viên đạt GPA trung bình và khá chiếm tỷ lệ lớn nhất trong dữ liệu.

• Chỉ có một số lượng nhỏ sinh viên đạt GPA quá thấp hoặc quá cao.

• Đường KDE cho thấy dữ liệu có phân bố tương đối cân đối,
không bị lệch mạnh về một phía.

• Điều này cho thấy phần lớn sinh viên có kết quả học tập ở mức ổn định.
""")


# STEP 2 - PHÂN LOẠI HỌC LỰC
st.markdown("---")

st.header("Bước 2: Phân loại học lực sinh viên")

st.write("""
Biểu đồ tròn giúp thể hiện tỷ lệ học lực của sinh viên trong tập dữ liệu.
Qua đó có thể đánh giá:
- Nhóm học lực nào chiếm đa số
- Mức độ phân hóa kết quả học tập
- Tỷ lệ sinh viên học tốt và học yếu
""")


# CREATE GRADE CATEGORY
grade_df = st.session_state.session_df.copy()

def classify_gpa(gpa):

    if gpa < 2.0:
        return "Yếu"

    elif gpa < 2.5:
        return "Trung bình"

    elif gpa < 3.2:
        return "Khá"

    else:
        return "Giỏi"

grade_df["HocLuc"] = grade_df["GPA"].apply(classify_gpa)


# COUNT DATA
grade_counts = (
    grade_df["HocLuc"]
    .value_counts()
    .reindex(["Yếu", "Trung bình", "Khá", "Giỏi"])
)


# PIE CHART
st.markdown("### 🥧 Tỷ lệ học lực sinh viên")

fig, ax = plt.subplots(figsize=(8,8))

# Tách từng phần để dễ quan sát hơn
explode = [0.03, 0.05, 0.08, 0.12]

colors = [
    "#e74c3c",  
    "#f39c12",   
    "#3498db",   
    "#2ecc71"    
]

ax.pie(
    grade_counts,
    labels=grade_counts.index,
    autopct='%.1f%%',
    explode=explode,
    shadow=True,
    startangle=90,
    colors=colors
)

ax.set_title(
    "Tỷ lệ học lực của sinh viên",
    fontsize=16,
    color="#2c3e50",
    fontweight="bold"
)

st.pyplot(fig)


# SUMMARY TABLE
st.markdown("### 📋 Bảng thống kê học lực")

summary_df = pd.DataFrame({
    "Học lực": grade_counts.index,
    "Số lượng sinh viên": grade_counts.values,
    "Tỷ lệ (%)": (
        grade_counts.values / grade_counts.sum() * 100
    ).round(1)
})

st.dataframe(
    summary_df,
    use_container_width=True
)


# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Yếu",
    int(grade_counts["Yếu"])
)

col2.metric(
    "Trung bình",
    int(grade_counts["Trung bình"])
)

col3.metric(
    "Khá",
    int(grade_counts["Khá"])
)

col4.metric(
    "Giỏi",
    int(grade_counts["Giỏi"])
)


# INTERPRETATION
st.info("""
📖 Nhận xét:

• Nhóm sinh viên có học lực Yếu chiếm tỷ lệ cao nhất,
cho thấy nhiều sinh viên vẫn gặp khó khăn trong học tập.

• Tỷ lệ sinh viên đạt mức Khá và Giỏi còn tương đối thấp,
phản ánh sự chênh lệch khá rõ về kết quả học tập giữa các nhóm.

• Nhóm học lực Trung bình và Yếu chiếm phần lớn dữ liệu,
cho thấy GPA của sinh viên hiện chủ yếu tập trung ở mức chưa cao.

• Kết quả này cho thấy cần tiếp tục phân tích các yếu tố như:
thời gian tự học, số buổi nghỉ học và hoạt động ngoại khóa
để tìm ra nguyên nhân ảnh hưởng đến GPA.

• Đây cũng là cơ sở để xây dựng các giải pháp hỗ trợ học tập
phù hợp cho từng nhóm sinh viên.
""")


# STEP 3 - PHÂN TÍCH THÓI QUEN HỌC TẬP
st.markdown("---")

st.header("Bước 3: Phân tích thói quen học tập")

st.write("""
Bước này phân tích thói quen học tập của sinh viên thông qua:
- Thời gian tự học mỗi tuần
- Số buổi nghỉ học
- Mức độ đầu tư cho việc học

Từ đó đánh giá ý thức học tập và sự khác biệt giữa các sinh viên.
""")


# DATA
data = st.session_state.session_df

# KPI

st.markdown("### 📌 Tổng quan thói quen học tập")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⏱️ Tự học trung bình",
    round(data["StudyTimeWeekly"].mean(), 2)
)

col2.metric(
    "📈 Tự học cao nhất",
    round(data["StudyTimeWeekly"].max(), 2)
)

col3.metric(
    "❌ Nghỉ học trung bình",
    round(data["Absences"].mean(), 2)
)

col4.metric(
    "🚫 Nghỉ học cao nhất",
    round(data["Absences"].max(), 2)
)


# SUMMARY TABLE
st.markdown("📋 Bảng thống kê")

summary_df = pd.DataFrame({

    "Chỉ số": [
        "Study Time Trung bình",
        "Study Time Cao nhất",
        "Study Time Thấp nhất",
        "Absences Trung bình",
        "Absences Cao nhất"
    ],

    "Giá trị": [
        round(data["StudyTimeWeekly"].mean(), 2),
        round(data["StudyTimeWeekly"].max(), 2),
        round(data["StudyTimeWeekly"].min(), 2),
        round(data["Absences"].mean(), 2),
        round(data["Absences"].max(), 2)
    ]
})

st.dataframe(
    summary_df,
    use_container_width=True
)


# TRANSITION
st.write("""
Để quan sát rõ hơn mức độ phân tán dữ liệu và phát hiện các giá trị bất thường,
biểu đồ Boxplot được sử dụng cho:
- Thời gian tự học
- Số buổi nghỉ học
""")


# BOXPLOT
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦Thời gian tự học")
    fig, ax = plt.subplots(figsize=(7,3))
    sns.boxplot(
        x=data["StudyTimeWeekly"],
        ax=ax
    )

    ax.set_title(
        "Phân bố thời gian tự học",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Study Time Weekly")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    st.pyplot(fig)

with col2:

    st.markdown("### 📦Số buổi nghỉ học")

    fig, ax = plt.subplots(figsize=(7,3))

    sns.boxplot(
        x=data["Absences"],
        ax=ax
    )

    ax.set_title(
        "Phân bố số buổi nghỉ học",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Absences")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    st.pyplot(fig)


# INTERPRETATION
st.info("""
📖 Nhận xét:

• Trung bình mỗi sinh viên dành khoảng 9.77 giờ tự học mỗi tuần,
cho thấy phần lớn sinh viên có đầu tư thời gian cho việc học ngoài giờ lên lớp.

• Tuy nhiên,
vẫn tồn tại những sinh viên gần như không tự học,
phản ánh sự khác biệt khá lớn về thói quen học tập.

• Một số sinh viên có thời gian tự học rất cao,
gần 20 giờ mỗi tuần,
cho thấy mức độ tập trung học tập vượt trội hơn mặt bằng chung.

• Số buổi nghỉ học trung bình ở mức khá cao,
điều này có thể ảnh hưởng tiêu cực đến kết quả học tập.

• Có sinh viên nghỉ học tới gần 30 buổi,
cho thấy tình trạng vắng học vẫn diễn ra khá nghiêm trọng ở một bộ phận sinh viên.

• Boxplot cho thấy dữ liệu có độ phân tán tương đối lớn,
đặc biệt xuất hiện một số giá trị ngoại lệ về thời gian học và số buổi nghỉ học.

• Nhìn chung,
dữ liệu phản ánh sự chênh lệch rõ rệt về ý thức học tập
và mức độ tham gia học tập giữa các sinh viên.
""")


# STEP 4 - THỜI GIAN TỰ HỌC VÀ GPA
st.markdown("---")

st.header("Bước 4: Mối quan hệ giữa thời gian tự học và GPA")

st.write("""
Bước này phân tích mối quan hệ giữa thời gian tự học và GPA của sinh viên.

Mục tiêu:
- Kiểm tra liệu sinh viên học nhiều hơn có đạt GPA cao hơn hay không
- Quan sát xu hướng thay đổi GPA theo thời gian học
- Đánh giá mức độ ảnh hưởng của thời gian tự học đến kết quả học tập
""")

data = st.session_state.session_df.copy()

st.markdown("### 📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "⏱️ Tự học trung bình",
    round(data["StudyTimeWeekly"].mean(), 2)
)

col2.metric(
    "📊 GPA trung bình",
    round(data["GPA"].mean(), 2)
)

col3.metric(
    "📈 Hệ số tương quan",
    round(
        data["StudyTimeWeekly"].corr(data["GPA"]),
        2
    )
)


# REGRESSION PLOT
st.markdown("### 📉 Biểu đồ hồi quy")

fig, ax = plt.subplots(figsize=(9,5))

sns.regplot(
    data=data,
    x="StudyTimeWeekly",
    y="GPA",
    scatter_kws={
        "alpha":0.5
    },
    line_kws={
        "color":"red"
    },
    ax=ax
)

ax.set_title(
    "Mối quan hệ giữa thời gian tự học và GPA",
    fontsize=16,
    fontweight='bold'
)

ax.set_xlabel("Study Time Weekly")
ax.set_ylabel("GPA")

ax.grid(
    alpha=0.3,
    linestyle="--"
)

st.pyplot(fig)

st.markdown("### 📊 GPA trung bình theo nhóm thời gian học")

bins = [0, 5, 10, 15, 20]

labels = [
    "0-5 giờ",
    "5-10 giờ",
    "10-15 giờ",
    "15-20 giờ"
]

data["StudyGroup"] = pd.cut(
    data["StudyTimeWeekly"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

group_avg = (
    data
    .groupby("StudyGroup")["GPA"]
    .mean()
    .round(2)
)

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    x=group_avg.index,
    y=group_avg.values,
    ax=ax
)

for i, v in enumerate(group_avg.values):

    ax.text(
        i,
        v + 0.03,
        str(v),
        ha='center',
        fontsize=10
    )

ax.set_title(
    "GPA trung bình theo nhóm thời gian học",
    fontsize=15,
    fontweight='bold'
)

ax.set_xlabel("Nhóm thời gian học")
ax.set_ylabel("GPA trung bình")

ax.grid(
    alpha=0.2,
    linestyle="--"
)

st.pyplot(fig)


# SUMMARY TABLE
st.markdown("### 📋 Bảng thống kê")

summary_df = pd.DataFrame({
    "Nhóm thời gian học": group_avg.index,
    "GPA trung bình": group_avg.values
})

st.dataframe(
    summary_df,
    use_container_width=True
)


# MINI HEATMAP
st.markdown("### 🔥 Heatmap tương quan")

corr_cols = [
    "GPA",
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport"
]

corr_matrix = data[corr_cols].corr()

fig, ax = plt.subplots(figsize=(6,4))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="Blues",
    fmt=".2f",
    ax=ax
)

ax.set_title(
    "Tương quan giữa các yếu tố học tập",
    fontsize=15,
    fontweight='bold'
)

st.pyplot(fig)


# INTERPRETATION
st.info("""
📖 Nhận xét:

• Regression Plot cho thấy GPA có xu hướng tăng khi thời gian tự học tăng.

• Đường hồi quy đi lên cho thấy tồn tại mối quan hệ tích cực giữa thời gian tự học và GPA.

• GPA trung bình tăng dần theo từng nhóm thời gian học,
cho thấy sinh viên học nhiều hơn thường đạt kết quả học tập tốt hơn.

• Nhóm học dưới 5 giờ mỗi tuần có GPA thấp nhất,
trong khi nhóm học từ 15–20 giờ đạt GPA cao nhất.

• Tuy nhiên,
mức tăng GPA giữa các nhóm không quá lớn,
cho thấy GPA còn chịu ảnh hưởng từ nhiều yếu tố khác ngoài thời gian học.

• Heatmap cho thấy số buổi nghỉ học có tương quan âm mạnh với GPA,
đồng nghĩa với việc nghỉ học nhiều thường làm kết quả học tập giảm.

• Trong khi đó,
Study Time và Parental Support có tương quan dương với GPA,
cho thấy việc duy trì học tập đều đặn và nhận được hỗ trợ phù hợp
có thể giúp cải thiện kết quả học tập.

• Nhìn chung,
thời gian tự học là yếu tố có tác động tích cực đến GPA,
nhưng sự chuyên cần vẫn là yếu tố ảnh hưởng mạnh nhất trong dữ liệu hiện tại.
""")


# STEP 5 - SỐ BUỔI NGHỈ HỌC VÀ GPA
st.markdown("---")

st.header("Bước 5: Mối quan hệ giữa số buổi nghỉ học và GPA")

st.write("""
Sau khi phân tích thời gian tự học,
bước tiếp theo tập trung vào ảnh hưởng của số buổi nghỉ học đến GPA.

Mục tiêu:
- Kiểm tra tác động của việc nghỉ học đến kết quả học tập
- Quan sát xu hướng thay đổi GPA khi số buổi nghỉ tăng
- Đánh giá mức độ ảnh hưởng của Absences đến GPA
""")

data = st.session_state.session_df.copy()

st.markdown("### 📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "📅 Nghỉ học trung bình",
    round(data["Absences"].mean(), 2)
)

col2.metric(
    "📊 GPA trung bình",
    round(data["GPA"].mean(), 2)
)

col3.metric(
    "📉 Hệ số tương quan",
    round(
        data["Absences"].corr(data["GPA"]),
        2
    )
)

col1, col2 = st.columns(2)

with col2:

    st.markdown("### 📈 Regression Plot")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.regplot(
        data=data,
        x="Absences",
        y="GPA",
        scatter_kws={
            "alpha":0.4
        },
        line_kws={
            "color":"red"
        },
        ax=ax
    )

    ax.set_title(
        "Xu hướng hồi quy giữa nghỉ học và GPA",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Số buổi nghỉ học")
    ax.set_ylabel("GPA")

    ax.grid(
        alpha=0.3,
        linestyle="--"
    )

    st.pyplot(fig)


# GROUP ANALYSIS
st.markdown("### 📊 GPA trung bình theo nhóm nghỉ học")

bins = [0, 5, 10, 20, 30]

labels = [
    "0-5 buổi",
    "6-10 buổi",
    "11-20 buổi",
    "21-30 buổi"
]

data["AbsenceGroup"] = pd.cut(
    data["Absences"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

absence_avg = (
    data
    .groupby("AbsenceGroup")["GPA"]
    .mean()
    .round(2)
)

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    x=absence_avg.index,
    y=absence_avg.values,
    ax=ax
)

for i, v in enumerate(absence_avg.values):

    ax.text(
        i,
        v + 0.03,
        str(v),
        ha='center',
        fontsize=10
    )

ax.set_title(
    "GPA trung bình theo nhóm nghỉ học",
    fontsize=15,
    fontweight='bold'
)

ax.set_xlabel("Nhóm nghỉ học")
ax.set_ylabel("GPA trung bình")

ax.grid(
    alpha=0.2,
    linestyle="--"
)

st.pyplot(fig)


# SUMMARY TABLE
st.markdown("### 📋 Bảng thống kê")

summary_df = pd.DataFrame({
    "Nhóm nghỉ học": absence_avg.index,
    "GPA trung bình": absence_avg.values
})

st.dataframe(
    summary_df,
    use_container_width=True
)


# INTERPRETATION
st.info("""
📖 Nhận xét:

• Scatter Plot cho thấy GPA có xu hướng giảm khi số buổi nghỉ học tăng lên.

• Đường hồi quy đi xuống thể hiện mối quan hệ âm giữa Absences và GPA.

• Sinh viên nghỉ học ít thường đạt GPA cao hơn đáng kể
so với nhóm nghỉ học nhiều.

• Hệ số tương quan âm mạnh cho thấy Absences là một trong những yếu tố ảnh hưởng lớn nhất đến kết quả học tập.

• GPA trung bình giảm dần theo từng nhóm nghỉ học,
đặc biệt nhóm nghỉ trên 20 buổi có kết quả học tập thấp hơn rõ rệt.

• Điều này cho thấy tính chuyên cần đóng vai trò rất quan trọng
trong việc duy trì kết quả học tập ổn định.

• Kết quả cũng phù hợp với Heatmap ở bước trước,
khi Absences là biến có tương quan âm mạnh nhất với GPA.

• Nhìn chung,
việc hạn chế nghỉ học có thể giúp cải thiện đáng kể kết quả học tập của sinh viên.
""")


# STEP 6 - HOẠT ĐỘNG NGOẠI KHÓA VÀ GPA
st.markdown("---")

st.header("Bước 6: Ảnh hưởng của hoạt động ngoại khóa đến GPA")

st.write("""
Ở bước này,
bài toán tập trung phân tích ảnh hưởng của các hoạt động ngoại khóa đến GPA của sinh viên.

Các hoạt động được xem xét gồm:
- Extracurricular
- Sports
- Music
- Volunteering

Mục tiêu:
- So sánh GPA giữa nhóm tham gia và không tham gia hoạt động
- Tìm hoạt động có ảnh hưởng tích cực nhất đến kết quả học tập
- Đánh giá vai trò của hoạt động ngoại khóa đối với sinh viên
""")

data = st.session_state.session_df.copy()

activities = [
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]


# CALCULATE GPA
activity_results = []

for activity in activities:

    no_activity = (
        data[data[activity] == 0]["GPA"]
        .mean()
    )

    participated = (
        data[data[activity] == 1]["GPA"]
        .mean()
    )

    diff = participated - no_activity

    activity_results.append([
        activity,
        round(no_activity, 2),
        round(participated, 2),
        round(diff, 2)
    ])

activity_df = pd.DataFrame(
    activity_results,
    columns=[
        "Hoạt động",
        "GPA không tham gia",
        "GPA tham gia",
        "Mức chênh lệch"
    ]
)


# KPI
st.markdown("### 📌 Tổng quan")

best_activity = activity_df.loc[
    activity_df["Mức chênh lệch"].idxmax()
]

positive_count = (
    activity_df["Mức chênh lệch"] > 0
).sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "🎯 Số hoạt động phân tích",
    len(activities)
)

col2.metric(
    "📈 Hoạt động tác động tích cực",
    positive_count
)

col3.metric(
    "🏆 Hoạt động nổi bật",
    best_activity["Hoạt động"]
)


# TABLE
st.markdown("### 📋 Bảng so sánh")

st.dataframe(
    activity_df,
    use_container_width=True
)


# GROUPED BAR CHART
st.markdown("### 📊 GPA trung bình theo hoạt động")

plot_df = activity_df.melt(
    id_vars="Hoạt động",
    value_vars=[
        "GPA không tham gia",
        "GPA tham gia"
    ],
    var_name="Nhóm",
    value_name="GPA"
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=plot_df,
    x="Hoạt động",
    y="GPA",
    hue="Nhóm",
    ax=ax
)

ax.set_title(
    "So sánh GPA theo hoạt động ngoại khóa",
    fontsize=18,
    fontweight='bold'
)

ax.set_xlabel("Hoạt động")
ax.set_ylabel("GPA trung bình")

ax.grid(
    alpha=0.2,
    linestyle="--"
)


for p in ax.patches:

    height = p.get_height()

    if height > 0.05:

        ax.annotate(
            f"{height:.2f}",
            (
                p.get_x() + p.get_width()/2,
                height
            ),
            ha='center',
            va='bottom',
            fontsize=9
        )

st.pyplot(fig)


# IMPACT CHART
st.markdown("### 📈 Mức cải thiện GPA theo hoạt động")

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=activity_df,
    x="Hoạt động",
    y="Mức chênh lệch",
    ax=ax
)

ax.set_title(
    "Mức ảnh hưởng của hoạt động ngoại khóa đến GPA",
    fontsize=16,
    fontweight='bold'
)

ax.set_xlabel("Hoạt động")
ax.set_ylabel("Mức chênh lệch GPA")

ax.axhline(
    0,
    color='black',
    linewidth=1
)

ax.grid(
    alpha=0.2,
    linestyle="--"
)

for p in ax.patches:

    height = p.get_height()

    if abs(height) > 0.01:

        ax.annotate(
            f"{height:.2f}",
            (
                p.get_x() + p.get_width()/2,
                height
            ),
            ha='center',
            va='bottom',
            fontsize=9
        )

st.pyplot(fig)


# BEST ACTIVITY
st.success(f"""
🏆 Hoạt động có ảnh hưởng tích cực nhất đến GPA là:
{best_activity['Hoạt động']}
với mức tăng GPA trung bình khoảng {best_activity['Mức chênh lệch']} điểm.
""")


# INTERPRETATION
st.info("""
📖 Nhận xét:

• Hầu hết các hoạt động ngoại khóa đều có ảnh hưởng tích cực đến GPA của sinh viên.

• Sinh viên tham gia hoạt động thường có GPA cao hơn
so với nhóm không tham gia.

• Trong các hoạt động được phân tích,
Extracurricular cho thấy mức cải thiện GPA rõ rệt nhất.

• Sports và Music cũng có tác động tích cực tương đối tốt đến kết quả học tập.

• Volunteering gần như không tạo ra sự khác biệt lớn về GPA.

• Điều này cho thấy sinh viên năng động,
biết cân bằng giữa học tập và hoạt động cá nhân
thường có kết quả học tập ổn định hơn.

• Tuy nhiên,
mức chênh lệch GPA giữa các nhóm không quá lớn,
cho thấy hoạt động ngoại khóa không phải yếu tố quyết định duy nhất đến thành tích học tập.

• Nhìn chung,
việc tham gia hoạt động ngoại khóa hợp lý
có thể hỗ trợ sinh viên phát triển kỹ năng mềm
và duy trì hiệu quả học tập tốt hơn.
""")


# STEP 7 - PHÂN TÍCH ẢNH HƯỞNG CỦA GIA ĐÌNH ĐẾN GPA
st.markdown(
    '<p class="section-title">Bước 7: Ảnh hưởng của hỗ trợ gia đình đến GPA</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này phân tích ảnh hưởng của mức độ hỗ trợ từ gia đình đến GPA của sinh viên.

Mục tiêu:
- So sánh GPA trung bình theo từng mức hỗ trợ từ phụ huynh
- Kiểm tra liệu sự quan tâm của gia đình có ảnh hưởng đến kết quả học tập hay không
- Quan sát xu hướng thay đổi GPA theo mức độ hỗ trợ
""")


# DATA
data = st.session_state.session_df.copy()

support_labels = {
    0: "Rất thấp",
    1: "Thấp",
    2: "Trung bình",
    3: "Cao",
    4: "Rất cao"
}

data["SupportLabel"] = (
    data["ParentalSupport"]
    .map(support_labels)
)


# TÍNH GPA TRUNG BÌNH
support_gpa = (
    data.groupby("SupportLabel")["GPA"]
    .mean()
    .reindex([
        "Rất thấp",
        "Thấp",
        "Trung bình",
        "Cao",
        "Rất cao"
    ])
    .reset_index()
)

support_gpa["GPA"] = (
    support_gpa["GPA"]
    .round(2)
)

st.markdown("### 📌 Tổng quan")

highest_support = support_gpa.loc[
    support_gpa["GPA"].idxmax()
]

lowest_support = support_gpa.loc[
    support_gpa["GPA"].idxmin()
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Nhóm GPA cao nhất",
    highest_support["SupportLabel"]
)

col2.metric(
    "GPA cao nhất",
    highest_support["GPA"]
)

col3.metric(
    "GPA thấp nhất",
    lowest_support["GPA"]
)


# BẢNG DỮ LIỆU
st.markdown("### 📋 GPA theo mức hỗ trợ gia đình")

st.dataframe(
    support_gpa,
    use_container_width=True
)

col1, col2 = st.columns(2)


# BAR CHART
with col1:

    st.markdown("### 📊 GPA trung bình theo mức hỗ trợ")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        data=support_gpa,
        x="SupportLabel",
        y="GPA",
        ax=ax
    )

    ax.set_title(
        "GPA trung bình theo mức hỗ trợ gia đình",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Mức hỗ trợ")
    ax.set_ylabel("GPA trung bình")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    for p in ax.patches:

        height = p.get_height()

        if height > 0.05:

            ax.annotate(
                f"{height:.2f}",
                (
                    p.get_x() + p.get_width()/2,
                    height
                ),
                ha='center',
                va='bottom',
                fontsize=8
            )

    st.pyplot(fig)


# LINE CHART
with col2:

    st.markdown("### 📈 Xu hướng GPA theo mức hỗ trợ")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.lineplot(
        data=support_gpa,
        x="SupportLabel",
        y="GPA",
        marker="o",
        linewidth=3,
        ax=ax
    )

    ax.set_title(
        "Xu hướng giữa hỗ trợ gia đình và GPA",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Mức hỗ trợ")
    ax.set_ylabel("GPA trung bình")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )
    
    for i, row in support_gpa.iterrows():
        ax.text(
            i,
            row["GPA"] + 0.02,
            f"{row['GPA']:.2f}",
            ha='center',
            fontsize=8
        )

    st.pyplot(fig)


# CORRELATION
correlation = round(
    data["ParentalSupport"]
    .corr(data["GPA"]),
    2
)

st.success(f"""
📌 Hệ số tương quan giữa Parental Support và GPA: {correlation}

Giá trị dương cho thấy khi mức hỗ trợ từ gia đình tăng,
GPA của sinh viên có xu hướng tăng theo.
""")


# NHẬN XÉT
st.info("""
📖 Nhận xét:

• GPA trung bình có xu hướng tăng khi mức độ hỗ trợ từ gia đình tăng lên.

• Nhóm sinh viên nhận được mức hỗ trợ “Rất cao” đạt GPA cao hơn đáng kể so với nhóm “Rất thấp”.

• Biểu đồ đường cho thấy xu hướng tăng tương đối ổn định giữa Parental Support và GPA.

• Điều này cho thấy sự quan tâm, động viên và hỗ trợ từ gia đình có tác động tích cực đến kết quả học tập của sinh viên.

• Tuy nhiên, hệ số tương quan không quá mạnh, cho thấy GPA vẫn còn chịu ảnh hưởng từ nhiều yếu tố khác như:
thời gian học tập, số buổi nghỉ học và ý thức cá nhân.

• Kết quả cho thấy môi trường gia đình đóng vai trò hỗ trợ quan trọng trong quá trình học tập,
đặc biệt trong việc duy trì động lực và tinh thần học tập của sinh viên.
""")


# STEP 8 — PHÂN TÍCH TƯƠNG QUAN
st.markdown(
    '<p class="section-title">Bước 8: Tương quan giữa các yếu tố học tập</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này nhằm phân tích mức độ tương quan giữa các yếu tố học tập
và GPA của sinh viên.

Giá trị tương quan:
- Gần 1  → tương quan dương mạnh
- Gần -1 → tương quan âm mạnh
- Gần 0  → tương quan yếu
""")

corr_df = data[[
    "GPA",
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport",
    "Tutoring",
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]]

# MA TRẬN TƯƠNG QUAN
corr_matrix = corr_df.corr()

# HEATMAP
st.markdown("### 🔥 Biểu đồ tương quan")

fig, ax = plt.subplots(figsize=(10,7))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="Blues",
    fmt=".2f",
    linewidths=0.5,
    ax=ax
)

ax.set_title(
    "Ma trận tương quan giữa các yếu tố học tập",
    fontsize=18,
    fontweight='bold'
)

st.pyplot(fig)


# TƯƠNG QUAN VỚI GPA
st.markdown("### 📊 Mức độ tương quan với GPA")

gpa_corr = (
    corr_matrix["GPA"]
    .drop("GPA")
    .sort_values(ascending=False)
)

corr_result = pd.DataFrame({
    "Yếu tố": gpa_corr.index,
    "Tương quan với GPA": gpa_corr.values.round(2)
})

st.dataframe(
    corr_result,
    use_container_width=True
)


# THỐNG KÊ YẾU TỐ MẠNH NHẤT
highest_positive = gpa_corr.idxmax()
highest_positive_value = gpa_corr.max()

highest_negative = gpa_corr.idxmin()
highest_negative_value = gpa_corr.min()

col1, col2 = st.columns(2)
with col1:
    st.metric(
        "📈 Yếu tố tích cực mạnh nhất",
        highest_positive,
        f"{highest_positive_value:.2f}"
    )

with col2:
    st.metric(
        "📉 Yếu tố tiêu cực mạnh nhất",
        highest_negative,
        f"{highest_negative_value:.2f}"
    )


# NHẬN XÉT
st.info(f"""
📖 Nhận xét:

• Yếu tố có tương quan dương mạnh nhất với GPA là
'{highest_positive}' với hệ số khoảng {highest_positive_value:.2f}.

• Điều này cho thấy khi '{highest_positive}' tăng,
GPA của sinh viên có xu hướng tăng theo.

• Yếu tố có tương quan âm mạnh nhất là
'{highest_negative}' với hệ số khoảng {highest_negative_value:.2f}.

• Điều này cho thấy khi '{highest_negative}' tăng,
GPA thường giảm xuống đáng kể.

• Heatmap cho thấy số buổi nghỉ học (Absences)
có ảnh hưởng tiêu cực rất mạnh tới kết quả học tập.

• Trong khi đó,
thời gian học tập và sự hỗ trợ từ gia đình
có xu hướng tác động tích cực đến GPA.

• Các hoạt động ngoại khóa như Sports, Music và Volunteering
có tương quan dương nhưng ở mức khá yếu,
cho thấy chúng chỉ hỗ trợ học tập ở mức vừa phải
thay vì quyết định trực tiếp GPA.

• Kết quả phân tích tương quan phù hợp với các bước trước,
khi StudyTimeWeekly giúp GPA tăng
còn Absences làm GPA giảm rõ rệt.
""")


# STEP 9 — SO SÁNH CÁC MÔ HÌNH HỌC MÁY
st.markdown(
    '<p class="section-title">Bước 9: So sánh các mô hình học máy</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này sử dụng nhiều mô hình học máy khác nhau
để dự đoán GPA của sinh viên.

Các mô hình được sử dụng:
- OLS Regression
- Decision Tree
- Logistic Regression

Mục tiêu:
- So sánh hiệu quả của các mô hình
- Đánh giá khả năng dự đoán GPA
- Chọn mô hình phù hợp nhất cho bài toán
""")


# IMPORT THƯ VIỆN
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    accuracy_score
)

X = data[[
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport",
    "Tutoring",
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]]

# GPA cho regression
y_reg = data["GPA"]

# GradeClass cho classification
y_clf = data["GradeClass"]

# CHIA DỮ LIỆU
split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train_reg = y_reg.iloc[:split_index]
y_test_reg = y_reg.iloc[split_index:]

y_train_clf = y_clf.iloc[:split_index]
y_test_clf = y_clf.iloc[split_index:]


# 1. OLS REGRESSION
X_train_ols = sm.add_constant(X_train)
X_test_ols = sm.add_constant(X_test)

ols_model = sm.OLS(
    y_train_reg,
    X_train_ols
).fit()

ols_pred = ols_model.predict(X_test_ols)

ols_r2 = r2_score(
    y_test_reg,
    ols_pred
)

ols_mae = mean_absolute_error(
    y_test_reg,
    ols_pred
)


# 2. DECISION TREE
tree_model = DecisionTreeRegressor(
    max_depth=5,
    random_state=42
)

tree_model.fit(
    X_train,
    y_train_reg
)

tree_pred = tree_model.predict(X_test)

tree_r2 = r2_score(
    y_test_reg,
    tree_pred
)

tree_mae = mean_absolute_error(
    y_test_reg,
    tree_pred
)


# 3. LOGISTIC REGRESSION
logistic_model = LogisticRegression(
    max_iter=1000
)

logistic_model.fit(
    X_train,
    y_train_clf
)

logistic_pred = logistic_model.predict(X_test)

logistic_acc = accuracy_score(
    y_test_clf,
    logistic_pred
)


# BẢNG SO SÁNH
st.markdown("### 📋 Bảng so sánh mô hình")

result_df = pd.DataFrame({

    "Mô hình": [
        "OLS Regression",
        "Decision Tree",
        "Logistic Regression"
    ],

    "R² Score": [
        round(ols_r2, 3),
        round(tree_r2, 3),
        "-"
    ],

    "MAE": [
        round(ols_mae, 3),
        round(tree_mae, 3),
        "-"
    ],

    "Accuracy": [
        "-",
        "-",
        round(logistic_acc, 3)
    ]

})

st.dataframe(
    result_df,
    use_container_width=True
)


# BIỂU ĐỒ SO SÁNH
st.markdown("### 📊 So sánh độ chính xác mô hình Regression")

regression_df = pd.DataFrame({

    "Model": [
        "OLS",
        "Decision Tree"
    ],

    "R²": [
        ols_r2,
        tree_r2
    ]

})

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=regression_df,
    x="Model",
    y="R²",
    ax=ax
)

ax.set_title(
    "So sánh R² giữa các mô hình",
    fontsize=16,
    fontweight='bold'
)

ax.set_ylim(0, 1)

ax.grid(
    alpha=0.2,
    linestyle="--"
)

# Hiển thị giá trị
for p in ax.patches:

    height = p.get_height()

    if height > 0:

        ax.annotate(
            f"{height:.2f}",
            (
                p.get_x() + p.get_width()/2,
                height
            ),
            ha='center',
            va='bottom',
            fontsize=9
        )

st.pyplot(fig)


# MÔ HÌNH TỐT NHẤT
best_regression = regression_df.loc[
    regression_df["R²"].idxmax()
]

st.success(f"""
🏆 Mô hình Regression tốt nhất:
{best_regression['Model']}
với R² Score = {best_regression['R²']:.3f}
""")

st.success(f"""
🏆 Logistic Regression Accuracy:
{logistic_acc:.3f}
""")


# NHẬN XÉT
st.info(f"""
📖 Nhận xét:

• Kết quả cho thấy mô hình OLS Regression đạt giá trị R² cao nhất,
cho thấy mô hình này phù hợp nhất để dự đoán GPA
trong bộ dữ liệu hiện tại.

• Decision Tree có khả năng xử lý các mối quan hệ phi tuyến,
tuy nhiên hiệu quả dự đoán chưa vượt qua OLS Regression.

• Logistic Regression được sử dụng để phân loại học lực sinh viên
và đạt độ chính xác tương đối tốt.

• Từ kết quả trên,
mô hình OLS sẽ được sử dụng để phân tích chi tiết
mức độ ảnh hưởng của từng yếu tố tới GPA.
""")


# PHÂN TÍCH CHI TIẾT OLS
st.markdown("### 📄 Phân tích chi tiết mô hình OLS")

X = data[[
    "StudyTimeWeekly",
    "Absences",
    "ParentalSupport",
    "Tutoring",
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]]

y = data["GPA"]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()


# MODEL SUMMARY
st.markdown("### 📋 OLS Regression Summary")
st.text(model.summary())
st.markdown("### 📊 Bảng hệ số hồi quy")

coef_df = pd.DataFrame({
    "Yếu tố": model.params.index,
    "Coefficient": model.params.values.round(4),
    "P-Value": model.pvalues.values.round(4)
})

st.dataframe(
    coef_df,
    use_container_width=True
)


st.markdown("### 📈 Mức độ ảnh hưởng của các yếu tố")

coef_plot = coef_df[coef_df["Yếu tố"] != "const"]

fig, ax = plt.subplots(figsize=(9,5))

sns.barplot(
    data=coef_plot,
    x="Coefficient",
    y="Yếu tố",
    ax=ax
)

ax.axvline(
    0,
    color='black',
    linestyle='--'
)

ax.set_title(
    "OLS Coefficients",
    fontsize=18,
    fontweight='bold'
)

st.pyplot(fig)


# MODEL PERFORMANCE
r2 = model.rsquared
adj_r2 = model.rsquared_adj

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📌 R² Score",
        round(r2, 3)
    )

with col2:

    st.metric(
        "📌 Adjusted R²",
        round(adj_r2, 3)
    )


# YẾU TỐ QUAN TRỌNG NHẤT
important_feature = (
    coef_plot.iloc[
        coef_plot["Coefficient"].abs().idxmax()
    ]
)


# NHẬN XÉT CHI TIẾT OLS
st.info(f"""
📖 Phân tích chi tiết mô hình OLS:

• Mô hình OLS cho thấy mức độ ảnh hưởng của từng yếu tố tới GPA của sinh viên.

• Giá trị R² = {r2:.3f} cho thấy mô hình có thể giải thích khoảng
{r2*100:.1f}% sự biến động của GPA.

• Yếu tố ảnh hưởng mạnh nhất là:
'{important_feature["Yếu tố"]}'
với hệ số hồi quy khoảng {important_feature["Coefficient"]:.2f}.

• Hệ số hồi quy dương cho thấy khi biến đó tăng,
GPA có xu hướng tăng theo.

• Ngược lại,
hệ số âm cho thấy biến đó tác động tiêu cực đến GPA.

• Absences thường có hệ số âm lớn,
cho thấy nghỉ học nhiều làm giảm kết quả học tập đáng kể.

• StudyTimeWeekly và ParentalSupport
có xu hướng tác động tích cực đến GPA,
cho thấy sự chuyên cần và môi trường hỗ trợ
đóng vai trò quan trọng trong học tập.

• Các hoạt động ngoại khóa như Sports, Music và Volunteering
có ảnh hưởng nhưng ở mức nhỏ hơn.

• Nhìn chung,
mô hình cho thấy GPA của sinh viên chịu ảnh hưởng mạnh bởi:
thời gian học tập, mức độ chuyên cần
và sự hỗ trợ từ gia đình.
""")


# STEP 10 — HỆ THỐNG GỢI Ý HỌC TẬP
st.markdown(
    '<p class="section-title">🎯 Bước 10: Hệ thống gợi ý học tập</p>',
    unsafe_allow_html=True
)

st.write("""
Dựa trên kết quả phân tích dữ liệu và mô hình học máy,
hệ thống sẽ đưa ra các gợi ý học tập phù hợp cho sinh viên.

Mục tiêu:
- Hỗ trợ sinh viên cải thiện GPA
- Đề xuất kế hoạch học tập phù hợp
- Giảm nguy cơ học lực yếu
- Hỗ trợ định hướng học tập hiệu quả hơn
""")

recommend_df = data.copy()


# HÀM GỢI Ý
def recommend(row):
    if row["GPA"] < 2.0:
        if row["Absences"] > 15:

            return (
                "⚠️ GPA thấp và nghỉ học nhiều. "
                "Cần giảm số buổi nghỉ học, tăng thời gian tự học "
                "và nên tham gia tutoring để cải thiện kết quả học tập."
            )
        elif row["StudyTimeWeekly"] < 8:
            return (
                "⚠️ GPA thấp do thời gian tự học chưa đủ. "
                "Nên tăng thời gian học mỗi tuần và xây dựng kế hoạch học tập ổn định."
            )
        else:
            return (
                "⚠️ GPA còn thấp. "
                "Nên tập trung củng cố kiến thức nền tảng "
                "và giảm áp lực học phần trong thời gian tới."
            )
    elif row["GPA"] < 3.0:
        return (
            "📘 Kết quả học tập ở mức trung bình. "
            "Cần duy trì học tập ổn định và hạn chế nghỉ học "
            "để cải thiện GPA."
        )
    elif row["GPA"] < 3.5:

        return (
            "✅ Kết quả học tập khá tốt. "
            "Có thể đăng ký thêm học phần phù hợp "
            "hoặc tham gia thêm hoạt động ngoại khóa."
        )
    else:
        return (
            "🏆 Thành tích học tập rất tốt. "
            "Có thể cân nhắc học nâng cao, phát triển kỹ năng chuyên môn "
            "hoặc tham gia các dự án thực tế."
        )


# ÁP DỤNG GỢI Ý
recommend_df["Recommendation"] = recommend_df.apply(
    recommend,
    axis=1
)


# PHÂN LOẠI NHÓM
def classify_recommendation(gpa):
    if gpa < 2.0:
        return "Cần hỗ trợ"
    elif gpa < 3.0:
        return "Trung bình"
    elif gpa < 3.5:
        return "Khá"
    else:
        return "Giỏi"

recommend_df["Category"] = recommend_df["GPA"].apply(
    classify_recommendation
)

st.markdown("### 📌 Tổng quan gợi ý học tập")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "⚠️ Cần hỗ trợ",
        len(recommend_df[recommend_df["GPA"] < 2.0])
    )

with col2:
    st.metric(
        "📘 Trung bình",
        len(
            recommend_df[
                (recommend_df["GPA"] >= 2.0) &
                (recommend_df["GPA"] < 3.0)
            ]
        )
    )

with col3:
    st.metric(
        "✅ Khá",
        len(
            recommend_df[
                (recommend_df["GPA"] >= 3.0) &
                (recommend_df["GPA"] < 3.5)
            ]
        )
    )

with col4:
    st.metric(
        "🏆 Giỏi",
        len(recommend_df[recommend_df["GPA"] >= 3.5])
    )

st.markdown("### 📋 Gợi ý học tập cho sinh viên")
show_cols = [
    "StudentID",
    "GPA",
    "StudyTimeWeekly",
    "Absences",
    "Recommendation"
]

st.dataframe(
    recommend_df[show_cols],
    use_container_width=True
)

st.markdown("### 📊 Phân bố nhóm sinh viên")

category_counts = (
    recommend_df["Category"]
    .value_counts()
)

explode = [0.08, 0.04, 0.04, 0.04]

fig, ax = plt.subplots(figsize=(7,7))

ax.pie(
    category_counts.values,
    labels=category_counts.index,
    autopct='%1.1f%%',
    explode=explode,
    shadow=True
)

ax.set_title(
    "Phân loại gợi ý học tập",
    fontsize=16,
    fontweight='bold'
)

st.pyplot(fig)


# NHẬN XÉT
st.info("""
📖 Nhận xét:

• Hệ thống gợi ý học tập được xây dựng dựa trên:
GPA, thời gian tự học và số buổi nghỉ học của sinh viên.

• Những sinh viên có GPA thấp thường đi kèm:
- thời gian học ít
- số buổi nghỉ học cao
- hiệu suất học tập chưa ổn định.

• Nhóm sinh viên có kết quả học tập tốt
thường duy trì thời gian học tập đều đặn
và nghỉ học ít hơn.

• Kết quả cho thấy việc tăng thời gian tự học
và giảm số buổi nghỉ học
có thể cải thiện đáng kể GPA của sinh viên.

• Hệ thống recommendation giúp sinh viên:
- xây dựng kế hoạch học tập phù hợp
- lựa chọn khối lượng học hợp lý
- cải thiện hiệu quả học tập trong tương lai.

• Đây là bước mở rộng mang tính ứng dụng thực tế,
giúp chuyển đổi kết quả phân tích dữ liệu
thành các gợi ý hỗ trợ học tập cụ thể cho sinh viên.
""")


# FOOTER
st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 20px;'>

<p style='color:gray; font-size:14px;'>
Môn học: Lập trình khoa học dữ liệu
</p>

<p style='color:gray; font-size:14px;'>
Trường Đại học Thăng Long
</p>

<p style='color:gray; font-size:14px;'>
Sinh viên thực hiện:
Nguyễn Minh Cường - Vũ Văn Toàn - Nguyễn Đức Kiên - Nguyễn Đình Chiến
</p>

</div>
""", unsafe_allow_html=True)
