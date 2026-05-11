import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# ======================
# CONFIG + STYLE
# ======================
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
    '<div class="main-title">📊 Student GPA Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Scientific Data Programming Project</div>',
    unsafe_allow_html=True
)

# ======================
# LOAD DATA
# ======================
try:
    df_raw = pd.read_csv("data.csv")

except:
    st.error("❌ Cannot find data.csv")
    st.stop()

# ======================
# CLEAN DATA
# ======================
df = df_raw.copy()

# Remove spaces in column names
df.columns = df.columns.str.strip()

# ======================
# DROP UNUSED COLUMNS
# ======================
if "Age" in df.columns:
    df = df.drop(columns=["Age"])

if "Ethnicity" in df.columns:
    df = df.drop(columns=["Ethnicity"])

if "ParentalEducation" in df.columns:
    df = df.drop(columns=["ParentalEducation"])

# ======================
# REMOVE DUPLICATES
# ======================
df = df.drop_duplicates()

# ======================
# REMOVE NULL VALUES
# ======================
df = df.dropna()

# ======================
# CONVERT DATA TYPES
# ======================
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

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.title("⚙️ Filters")

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

gender_filter = st.sidebar.multiselect(
    "Gender",
    [0, 1],
    default=[0, 1]
)

tutoring_filter = st.sidebar.multiselect(
    "Tutoring",
    [0, 1],
    default=[0, 1]
)

grade_filter = st.sidebar.multiselect(
    "Grade Class",
    sorted(df["GradeClass"].unique()),
    default=sorted(df["GradeClass"].unique())
)

# ======================
# FILTER DATA
# ======================
df_filtered = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Tutoring"].isin(tutoring_filter)) &
    (df["GradeClass"].isin(grade_filter))
]

# ======================
# SESSION DATA
# ======================
if "session_df" not in st.session_state:
    st.session_state.session_df = df_filtered.copy()
else:
    st.session_state.session_df = df_filtered.copy()

# ======================
# CRUD MODULE
# ======================
st.markdown(
    '<p class="section-title">🛠️ CRUD Management</p>',
    unsafe_allow_html=True
)

df_work = st.session_state.session_df

# ======================
# CREATE DATA
# ======================
with st.form("add_form"):

    st.markdown("### ➕ Add New Student")

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

    submit = st.form_submit_button("➕ Add Student")

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

        st.success("✔ Student added successfully")

# ======================
# UPDATE DATA
# ======================
st.markdown("### ✏️ Edit Dataset")

edited_df = st.data_editor(
    st.session_state.session_df,
    num_rows="dynamic",
    use_container_width=True
)

st.session_state.session_df = edited_df

# ======================
# DELETE DATA
# ======================
st.markdown("### 🗑️ Delete Row")

idx = st.number_input(
    "Enter row index to delete",
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

    st.success("✔ Row deleted successfully")

# ======================
# DATA VIEW
# ======================
st.markdown(
    '<p class="section-title">📂 Current Dataset</p>',
    unsafe_allow_html=True
)

st.dataframe(
    st.session_state.session_df,
    use_container_width=True
)

# ======================
# SEARCH DATA
# ======================
st.markdown(
    '<p class="section-title">🔍 Search Data</p>',
    unsafe_allow_html=True
)

keyword = st.text_input(
    "Search by GPA, study time, absences, activities..."
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

# ======================
# EXPORT DATA
# ======================
st.markdown(
    '<p class="section-title">📤 Export Dataset</p>',
    unsafe_allow_html=True
)

csv_data = (
    st.session_state.session_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="student_gpa_analysis.csv",
    mime="text/csv"
)

# ======================
# KPI
# ======================
st.markdown(
    '<p class="section-title">📌 Overview</p>',
    unsafe_allow_html=True
)

data = st.session_state.session_df

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🎓 Students",
        len(data)
    )

with col2:
    st.metric(
        "📊 Average GPA",
        round(data["GPA"].mean(), 2)
    )

with col3:
    st.metric(
        "📚 Avg Study Time",
        round(data["StudyTimeWeekly"].mean(), 2)
    )

with col4:
    st.metric(
        "❌ Avg Absences",
        round(data["Absences"].mean(), 2)
    )


# ======================
# STEP 1 - GPA OVERVIEW
# ======================

st.markdown(
    '<p class="section-title">📊 Step 1: GPA Distribution Overview</p>',
    unsafe_allow_html=True
)

st.write("""
Biểu đồ Histogram giúp quan sát phân bố GPA của sinh viên.
Từ đó có thể đánh giá:
- GPA tập trung ở mức nào
- Dữ liệu có lệch hay không
- Sinh viên đạt GPA cao hay thấp chiếm đa số
""")

# ======================
# HISTOGRAM GPA
# ======================

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    data=st.session_state.session_df,
    x="GPA",
    bins=15,
    kde=True,
    ax=ax
)

# Format
ax.set_title("Distribution of Student GPA", fontsize=16)
ax.set_xlabel("GPA")
ax.set_ylabel("Number of Students")

# Grid
ax.grid(
    alpha=0.3,
    linestyle="--"
)

st.pyplot(fig)

# ======================
# GPA SUMMARY
# ======================

st.markdown("### 📌 GPA Statistics")

gpa_data = st.session_state.session_df["GPA"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average GPA",
    round(gpa_data.mean(), 2)
)

col2.metric(
    "Highest GPA",
    round(gpa_data.max(), 2)
)

col3.metric(
    "Lowest GPA",
    round(gpa_data.min(), 2)
)

col4.metric(
    "Median GPA",
    round(gpa_data.median(), 2)
)

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

- GPA của sinh viên phân bố chủ yếu trong khoảng từ 1.0 đến 3.0.
- Số lượng sinh viên đạt GPA trung bình và khá chiếm tỷ lệ lớn nhất.
- Rất ít sinh viên có GPA quá thấp hoặc quá cao.
- Đường KDE cho thấy phân bố dữ liệu khá cân đối, không bị lệch mạnh về một phía.
- Điều này cho thấy phần lớn sinh viên có kết quả học tập ở mức ổn định.
""")


# ======================
# STEP 2 - GRADE CLASSIFICATION
# ======================

st.markdown(
    '<p class="section-title">🎓 Step 2: Academic Performance Classification</p>',
    unsafe_allow_html=True
)

st.write("""
Biểu đồ tròn giúp thể hiện tỷ lệ học lực của sinh viên trong tập dữ liệu.
Qua đó có thể đánh giá nhóm học lực nào chiếm đa số và mức độ phân hóa kết quả học tập.
""")

# ======================
# CREATE GRADE CATEGORY
# ======================

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

# ======================
# COUNT DATA
# ======================

grade_counts = (
    grade_df["HocLuc"]
    .value_counts()
    .reindex(["Yếu", "Trung bình", "Khá", "Giỏi"])
)

# ======================
# PIE CHART
# ======================

st.markdown("### 🥧 Tỷ lệ học lực sinh viên")

fig, ax = plt.subplots(figsize=(8,8))

# Tách từng phần nhẹ để đẹp hơn
explode = [0.03, 0.05, 0.08, 0.12]

colors = [
    "#e74c3c",   # đỏ
    "#f39c12",   # cam
    "#3498db",   # xanh dương
    "#2ecc71"    # xanh lá
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

# ======================
# SUMMARY TABLE
# ======================

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

# ======================
# KPI
# ======================

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

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

- Nhóm sinh viên có học lực Yếu chiếm tỷ lệ cao nhất với 53.3%, cho thấy phần lớn sinh viên trong tập dữ liệu đang gặp khó khăn trong học tập.
- Tỷ lệ sinh viên đạt mức Khá và Giỏi còn khá thấp, lần lượt là 20.7% và 8.8%.
- Điều này phản ánh sự chênh lệch rõ rệt về kết quả học tập giữa các nhóm sinh viên.
- Kết quả trên cho thấy cần phân tích sâu hơn các yếu tố như thời gian tự học, số buổi nghỉ học và hoạt động ngoại khóa để tìm ra nguyên nhân ảnh hưởng đến GPA.
""")


# ======================
# STEP 3 - STUDY HABITS
# ======================

st.markdown(
    '<p class="section-title">📚 Step 3: Study Habits Analysis</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này phân tích thói quen học tập của sinh viên thông qua:
- Thời gian tự học mỗi tuần
- Số buổi nghỉ học
- Mối quan hệ giữa học tập và nghỉ học

Từ đó đánh giá mức độ đầu tư học tập của sinh viên.
""")

# ======================
# DATA
# ======================

data = st.session_state.session_df

# ======================
# KPI
# ======================

st.markdown("### 📌 Tổng quan thói quen học tập")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⏱️ Study Time TB",
    round(data["StudyTimeWeekly"].mean(), 2)
)

col2.metric(
    "📈 Study Time Max",
    round(data["StudyTimeWeekly"].max(), 2)
)

col3.metric(
    "❌ Absences TB",
    round(data["Absences"].mean(), 2)
)

col4.metric(
    "🚫 Absences Max",
    round(data["Absences"].max(), 2)
)

# ======================
# SUMMARY TABLE
# ======================

st.markdown("### 📋 Bảng thống kê")

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

# ======================
# BOXPLOT
# ======================

col1, col2 = st.columns(2)

# -------- STUDY TIME --------
with col1:

    st.markdown("### 📦 Boxplot thời gian tự học")

    fig, ax = plt.subplots(figsize=(7,3))

    sns.boxplot(
        x=data["StudyTimeWeekly"],
        ax=ax
    )

    ax.set_title("Boxplot of Weekly Study Time")
    ax.set_xlabel("Study Time Weekly")

    st.pyplot(fig)

# -------- ABSENCES --------
with col2:

    st.markdown("### 📦 Boxplot số buổi nghỉ học")

    fig, ax = plt.subplots(figsize=(7,3))

    sns.boxplot(
        x=data["Absences"],
        ax=ax
    )

    ax.set_title("Boxplot of Student Absences")
    ax.set_xlabel("Absences")

    st.pyplot(fig)


# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

- Trung bình mỗi sinh viên dành khoảng 9.77 giờ tự học mỗi tuần, cho thấy phần lớn sinh viên có đầu tư thời gian cho việc học ngoài giờ lên lớp.
- Tuy nhiên, vẫn tồn tại những sinh viên gần như không tự học (0 giờ), phản ánh sự khác biệt lớn về thói quen học tập.
- Một số sinh viên có thời gian tự học rất cao, lên tới gần 20 giờ mỗi tuần, cho thấy mức độ tập trung học tập cao hơn đáng kể so với mặt bằng chung.
- Số buổi nghỉ học trung bình là 14.54 buổi, tương đối cao và có thể ảnh hưởng tiêu cực đến kết quả học tập.
- Có sinh viên nghỉ học tới 29 buổi, cho thấy tình trạng vắng học diễn ra khá nghiêm trọng ở một bộ phận sinh viên.
- Nhìn chung, dữ liệu cho thấy sự chênh lệch rõ rệt về ý thức học tập và mức độ tham gia học tập giữa các sinh viên.
""")

# ======================
# STEP 4 - STUDY TIME → GPA
# ======================

st.markdown(
    '<p class="section-title">📈 Step 4: Study Time and GPA</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này phân tích mối quan hệ giữa thời gian tự học và GPA của sinh viên.

Mục tiêu:
- Kiểm tra liệu sinh viên học nhiều hơn có đạt GPA cao hơn hay không
- Quan sát xu hướng thay đổi GPA theo thời gian học
- Đánh giá mức độ ảnh hưởng của thời gian tự học đến kết quả học tập
""")

# ======================
# DATA
# ======================

data = st.session_state.session_df.copy()

# ======================
# KPI
# ======================

st.markdown("### 📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "⏱️ Study Time TB",
    round(data["StudyTimeWeekly"].mean(), 2)
)

col2.metric(
    "📊 GPA TB",
    round(data["GPA"].mean(), 2)
)

col3.metric(
    "📈 Correlation",
    round(
        data["StudyTimeWeekly"].corr(data["GPA"]),
        2
    )
)

# ======================
# REGRESSION PLOT
# ======================

st.markdown("### 📉 Regression Plot")

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
    "Relationship Between Study Time and GPA",
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

# ======================
# GPA BY STUDY GROUP
# ======================

st.markdown("### 📊 Average GPA by Study Time Group")

# Chia nhóm thời gian học
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

# Hiển thị số trên cột
for i, v in enumerate(group_avg.values):

    ax.text(
        i,
        v + 0.03,
        str(v),
        ha='center',
        fontsize=10
    )

ax.set_title(
    "Average GPA by Study Time Group",
    fontsize=15,
    fontweight='bold'
)

ax.set_xlabel("Study Time Group")
ax.set_ylabel("Average GPA")

ax.grid(
    alpha=0.2,
    linestyle="--"
)

st.pyplot(fig)

# ======================
# SUMMARY TABLE
# ======================

st.markdown("### 📋 Summary Table")

summary_df = pd.DataFrame({
    "Study Time Group": group_avg.index,
    "Average GPA": group_avg.values
})

st.dataframe(
    summary_df,
    use_container_width=True
)

# ======================
# MINI HEATMAP
# ======================

st.markdown("### 🔥 Mini Correlation Heatmap")

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
    "Correlation Between Study Factors",
    fontsize=15,
    fontweight='bold'
)

st.pyplot(fig)

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

• Regression plot cho thấy GPA có xu hướng tăng khi thời gian tự học tăng.

• Đường hồi quy đi lên cho thấy tồn tại mối quan hệ tích cực giữa Study Time và GPA.

• GPA trung bình tăng dần theo từng nhóm thời gian học.
    
• Nhóm học dưới 5 giờ mỗi tuần có GPA thấp nhất, trong khi nhóm học nhiều nhất đạt GPA cao nhất.

• Điều này cho thấy thời gian tự học có ảnh hưởng tích cực đến kết quả học tập.

• Tuy nhiên, mức tăng GPA giữa các nhóm không quá lớn, cho thấy GPA còn chịu ảnh hưởng từ nhiều yếu tố khác.

• Heatmap cho thấy số buổi nghỉ học (Absences) có tương quan âm rất mạnh với GPA (-0.92).

• Trong khi đó, Study Time và Parental Support chỉ có tương quan dương nhẹ với GPA.

• Kết quả cho thấy việc duy trì thời gian tự học hợp lý và hạn chế nghỉ học là hai yếu tố quan trọng giúp cải thiện kết quả học tập của sinh viên.
""")

# ======================
# STEP 5 - ABSENCES → GPA
# ======================

st.markdown(
    '<p class="section-title">📉 Step 5: Absences and GPA</p>',
    unsafe_allow_html=True
)

st.write("""
Sau khi phân tích thời gian tự học, bước tiếp theo tập trung vào ảnh hưởng của số buổi nghỉ học đến GPA.

Mục tiêu:
- Kiểm tra tác động của việc nghỉ học đến kết quả học tập
- Quan sát xu hướng thay đổi GPA khi số buổi nghỉ tăng
- Đánh giá mức độ ảnh hưởng của Absences đến GPA
""")

# ======================
# DATA
# ======================

data = st.session_state.session_df.copy()

# ======================
# KPI
# ======================

st.markdown("### 📌 Tổng quan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "📅 Absences TB",
    round(data["Absences"].mean(), 2)
)

col2.metric(
    "📊 GPA TB",
    round(data["GPA"].mean(), 2)
)

col3.metric(
    "📉 Correlation",
    round(
        data["Absences"].corr(data["GPA"]),
        2
    )
)

# ======================
# SCATTER + REGRESSION
# ======================

col1, col2 = st.columns(2)

# ----------------------
# SCATTER PLOT
# ----------------------
with col1:

    st.markdown("### 📉 Scatter Plot: Absences vs GPA")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.scatterplot(
        data=data,
        x="Absences",
        y="GPA",
        alpha=0.6,
        ax=ax
    )

    ax.set_title(
        "Absences vs GPA",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Number of Absences")
    ax.set_ylabel("GPA")

    ax.grid(
        alpha=0.3,
        linestyle="--"
    )

    st.pyplot(fig)

# ----------------------
# REGRESSION PLOT
# ----------------------
with col2:

    st.markdown("### 📈 Regression Trend")

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
        "Regression Between Absences and GPA",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Absences")
    ax.set_ylabel("GPA")

    ax.grid(
        alpha=0.3,
        linestyle="--"
    )

    st.pyplot(fig)

# ======================
# GROUP ANALYSIS
# ======================

st.markdown("### 📊 GPA theo nhóm số buổi nghỉ")

# Chia nhóm nghỉ học
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

# Hiển thị số GPA
for i, v in enumerate(absence_avg.values):

    ax.text(
        i,
        v + 0.03,
        str(v),
        ha='center',
        fontsize=10
    )

ax.set_title(
    "Average GPA by Absence Group",
    fontsize=15,
    fontweight='bold'
)

ax.set_xlabel("Absence Group")
ax.set_ylabel("Average GPA")

ax.grid(
    alpha=0.2,
    linestyle="--"
)

st.pyplot(fig)

# ======================
# SUMMARY TABLE
# ======================

st.markdown("### 📋 Summary Table")

summary_df = pd.DataFrame({
    "Absence Group": absence_avg.index,
    "Average GPA": absence_avg.values
})

st.dataframe(
    summary_df,
    use_container_width=True
)

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

• Scatter plot cho thấy GPA có xu hướng giảm khi số buổi nghỉ học tăng lên.

• Đường hồi quy đi xuống thể hiện mối quan hệ âm giữa Absences và GPA.

• Sinh viên nghỉ học ít thường đạt GPA cao hơn so với nhóm nghỉ học nhiều.

• Correlation âm mạnh cho thấy Absences là một trong những yếu tố ảnh hưởng lớn đến kết quả học tập.

• GPA trung bình giảm dần theo từng nhóm nghỉ học:

    - Nhóm nghỉ ít buổi có GPA cao hơn rõ rệt
    
    - Nhóm nghỉ nhiều buổi thường có GPA thấp hơn

• Điều này cho thấy tính chuyên cần đóng vai trò rất quan trọng trong việc duy trì kết quả học tập ổn định.

• Kết quả cũng phù hợp với Heatmap ở bước trước khi Absences có tương quan âm mạnh nhất với GPA.
""")


# ======================
# STEP 6 - ACTIVITIES → GPA
# ======================

st.markdown(
    '<p class="section-title">🎯 Step 6: Activities and GPA</p>',
    unsafe_allow_html=True
)

st.write("""
Ở bước này, bài toán tập trung phân tích ảnh hưởng của các hoạt động ngoại khóa đến GPA của sinh viên.

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

# ======================
# DATA
# ======================

data = st.session_state.session_df.copy()

activities = [
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering"
]

# ======================
# CALCULATE GPA
# ======================

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
        "Activity",
        "No Activity GPA",
        "Participated GPA",
        "Difference"
    ]
)

# ======================
# KPI
# ======================

st.markdown("### 📌 Tổng quan")

best_activity = activity_df.loc[
    activity_df["Difference"].idxmax()
]

positive_count = (
    activity_df["Difference"] > 0
).sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "🎯 Activities Analyzed",
    len(activities)
)

col2.metric(
    "📈 Positive Activities",
    positive_count
)

col3.metric(
    "🏆 Best Activity",
    best_activity["Activity"]
)

# ======================
# TABLE
# ======================

st.markdown("### 📋 Comparison Table")

st.dataframe(
    activity_df,
    use_container_width=True
)

# ======================
# GROUPED BAR CHART
# ======================

st.markdown("### 📊 Average GPA by Student Activities")

plot_df = activity_df.melt(
    id_vars="Activity",
    value_vars=[
        "No Activity GPA",
        "Participated GPA"
    ],
    var_name="Group",
    value_name="GPA"
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=plot_df,
    x="Activity",
    y="GPA",
    hue="Group",
    ax=ax
)

ax.set_title(
    "Average GPA by Student Activities",
    fontsize=18,
    fontweight='bold'
)

ax.set_xlabel("Activities")
ax.set_ylabel("Average GPA")

ax.grid(
    alpha=0.2,
    linestyle="--"
)

# Hiển thị giá trị trên cột
for p in ax.patches:

    height = p.get_height()

    # Tránh hiện 0.00 dư
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

# ======================
# IMPACT CHART
# ======================

st.markdown("### 📈 GPA Improvement by Activities")

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    data=activity_df,
    x="Activity",
    y="Difference",
    ax=ax
)

ax.set_title(
    "Impact of Activities on GPA",
    fontsize=16,
    fontweight='bold'
)

ax.set_xlabel("Activities")
ax.set_ylabel("GPA Difference")

ax.axhline(
    0,
    color='black',
    linewidth=1
)

ax.grid(
    alpha=0.2,
    linestyle="--"
)

# Hiển thị giá trị
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

# ======================
# BEST ACTIVITY
# ======================

st.success(f"""
🏆 Hoạt động có ảnh hưởng tích cực nhất đến GPA là:
**{best_activity['Activity']}**
với mức tăng GPA trung bình khoảng **{best_activity['Difference']}** điểm.
""")

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

• Hầu hết các hoạt động ngoại khóa đều có ảnh hưởng tích cực đến GPA của sinh viên.

• Sinh viên tham gia hoạt động thường có GPA cao hơn nhóm không tham gia.

• Trong các hoạt động được phân tích, Extracurricular cho thấy mức cải thiện GPA rõ rệt nhất.

• Sports và Music cũng có tác động tích cực tương đối tốt đến kết quả học tập.

• Volunteering gần như không tạo ra sự khác biệt lớn về GPA.

• Điều này cho thấy sinh viên có xu hướng năng động, biết cân bằng giữa học tập và hoạt động cá nhân thường đạt kết quả học tập ổn định hơn.

• Tuy nhiên, mức chênh lệch GPA giữa các nhóm không quá lớn, nên hoạt động ngoại khóa không phải yếu tố quyết định duy nhất đến thành tích học tập.
""")


# ======================
# STEP 7 - PARENTAL SUPPORT → GPA
# ======================

st.markdown(
    '<p class="section-title">👨‍👩‍👧 Step 7: Parental Support and GPA</p>',
    unsafe_allow_html=True
)

st.write("""
Bước này phân tích ảnh hưởng của mức độ hỗ trợ từ gia đình đến GPA của sinh viên.

Mục tiêu:
- So sánh GPA trung bình theo từng mức hỗ trợ của phụ huynh
- Kiểm tra liệu sự quan tâm từ gia đình có ảnh hưởng đến kết quả học tập hay không
- Tìm xu hướng giữa Parental Support và GPA
""")

# ======================
# DATA
# ======================

data = st.session_state.session_df.copy()

# ======================
# MAP LABEL
# ======================

support_labels = {
    0: "Very Low",
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Very High"
}

data["SupportLabel"] = (
    data["ParentalSupport"]
    .map(support_labels)
)

# ======================
# CALCULATE GPA
# ======================

support_gpa = (
    data.groupby("SupportLabel")["GPA"]
    .mean()
    .reindex([
        "Very Low",
        "Low",
        "Medium",
        "High",
        "Very High"
    ])
    .reset_index()
)

support_gpa["GPA"] = (
    support_gpa["GPA"]
    .round(2)
)

# ======================
# KPI
# ======================

st.markdown("### 📌 Overview")

highest_support = support_gpa.loc[
    support_gpa["GPA"].idxmax()
]

lowest_support = support_gpa.loc[
    support_gpa["GPA"].idxmin()
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Highest GPA Group",
    highest_support["SupportLabel"]
)

col2.metric(
    "Highest GPA",
    highest_support["GPA"]
)

col3.metric(
    "Lowest GPA",
    lowest_support["GPA"]
)

# ======================
# TABLE
# ======================

st.markdown("### 📋 GPA by Parental Support")

st.dataframe(
    support_gpa,
    use_container_width=True
)

# ======================
# VẼ BIỂU ĐỒ
# ======================
col1, col2 = st.columns(2)

# ----------------------
# BAR CHART
# ----------------------
with col1:

    st.markdown("### 📊 Average GPA by Parental Support")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        data=support_gpa,
        x="SupportLabel",
        y="GPA",
        ax=ax
    )

    ax.set_title(
        "Average GPA by Parental Support",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Support Level")
    ax.set_ylabel("Average GPA")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    # Hiển thị giá trị
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

# ----------------------
# LINE CHART
# ----------------------
with col2:

    st.markdown("### 📈 GPA Trend by Support Level")

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
        "Trend Between Support and GPA",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel("Support Level")
    ax.set_ylabel("Average GPA")

    ax.grid(
        alpha=0.2,
        linestyle="--"
    )

    # Hiển thị giá trị
    for i, row in support_gpa.iterrows():

        ax.text(
            i,
            row["GPA"] + 0.02,
            f"{row['GPA']:.2f}",
            ha='center',
            fontsize=8
        )

    st.pyplot(fig)

# ======================
# CORRELATION
# ======================

correlation = round(
    data["ParentalSupport"]
    .corr(data["GPA"]),
    2
)

st.success(f"""
📌 Correlation between Parental Support and GPA: {correlation}

Giá trị dương cho thấy khi mức hỗ trợ từ gia đình tăng,
GPA của sinh viên có xu hướng tăng theo.
""")

# ======================
# INTERPRETATION
# ======================

st.info("""
📖 Nhận xét:

• GPA trung bình tăng dần theo mức độ hỗ trợ từ gia đình.

• Sinh viên có mức hỗ trợ “Very High” đạt GPA trung bình khoảng 2.19,
cao hơn rõ rệt so với nhóm “Very Low” chỉ khoảng 1.54.

• Biểu đồ đường cho thấy xu hướng tăng khá đều giữa Parental Support và GPA,
chứng tỏ sự hỗ trợ từ gia đình có ảnh hưởng tích cực đến kết quả học tập.

• Hệ số tương quan khoảng 0.19 cho thấy mối quan hệ dương nhưng không quá mạnh.
Điều này nghĩa là hỗ trợ từ gia đình có tác động nhất định,
tuy nhiên GPA vẫn còn phụ thuộc vào nhiều yếu tố khác như:
thời gian học, ý thức cá nhân, hoạt động ngoại khóa và mức độ chuyên cần.

• Khoảng cách GPA giữa các nhóm khá rõ ràng,
đặc biệt từ mức “Medium” trở lên,
cho thấy sinh viên nhận được sự quan tâm và động viên nhiều hơn
thường có động lực học tập tốt hơn.

• Kết quả cho thấy môi trường gia đình đóng vai trò hỗ trợ quan trọng
trong việc cải thiện kết quả học tập của sinh viên,
dù không phải yếu tố quyết định duy nhất.
""")


# =========================================================
# STEP 8 — CORRELATION ANALYSIS
# =========================================================

st.markdown("---")

st.header("🔥 Step 8: Correlation Between Study Factors")

st.write("""
Bước này nhằm phân tích mức độ tương quan giữa các yếu tố học tập
và GPA của sinh viên.

Giá trị tương quan:
- Gần 1  → tương quan dương mạnh
- Gần -1 → tương quan âm mạnh
- Gần 0  → tương quan yếu
""")

# =========================================================
# SELECT NUMERIC COLUMNS
# =========================================================

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

# =========================================================
# CORRELATION MATRIX
# =========================================================

corr_matrix = corr_df.corr()

# =========================================================
# HEATMAP
# =========================================================

st.subheader("📊 Correlation Heatmap")

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
    "Correlation Between Study Factors",
    fontsize=18,
    fontweight='bold'
)

st.pyplot(fig)

# =========================================================
# TOP FACTORS
# =========================================================

st.subheader("📌 Correlation With GPA")

gpa_corr = (
    corr_matrix["GPA"]
    .drop("GPA")
    .sort_values(ascending=False)
)

corr_result = pd.DataFrame({
    "Factor": gpa_corr.index,
    "Correlation With GPA": gpa_corr.values.round(2)
})

st.dataframe(
    corr_result,
    use_container_width=True
)

# =========================================================
# STRONGEST FACTORS
# =========================================================

highest_positive = gpa_corr.idxmax()
highest_positive_value = gpa_corr.max()

highest_negative = gpa_corr.idxmin()
highest_negative_value = gpa_corr.min()

# =========================================================
# KPI
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📈 Strongest Positive Factor",
        highest_positive,
        f"{highest_positive_value:.2f}"
    )

with col2:

    st.metric(
        "📉 Strongest Negative Factor",
        highest_negative,
        f"{highest_negative_value:.2f}"
    )

# =========================================================
# INTERPRETATION
# =========================================================

st.success(f"""
📖 Nhận xét:

• Yếu tố có tương quan dương mạnh nhất với GPA là
'{highest_positive}' với hệ số khoảng {highest_positive_value:.2f}.

• Điều này cho thấy khi '{highest_positive}' tăng,
GPA của sinh viên có xu hướng tăng theo.

• Yếu tố có tương quan âm mạnh nhất là
'{highest_negative}' với hệ số khoảng {highest_negative_value:.2f}.

• Điều này cho thấy khi '{highest_negative}' tăng,
GPA thường giảm xuống đáng kể.

• Heatmap cho thấy Absences có ảnh hưởng tiêu cực mạnh tới kết quả học tập,
trong khi thời gian học và sự hỗ trợ từ gia đình
có xu hướng tác động tích cực hơn.

• Một số hoạt động ngoại khóa như Sports, Music hoặc Volunteering
có tương quan dương nhưng ở mức yếu,
cho thấy các hoạt động này hỗ trợ học tập ở mức vừa phải.
""")


# =========================================================
# STEP 9 — OLS REGRESSION ANALYSIS
# =========================================================

st.markdown("---")

st.header("🔥 Step 9: OLS Regression Analysis")

st.write("""
Bước cuối cùng sử dụng mô hình hồi quy tuyến tính OLS
(Ordinary Least Squares)
để đánh giá mức độ ảnh hưởng của các yếu tố học tập đến GPA.

Mục tiêu:
- Xác định yếu tố ảnh hưởng mạnh nhất
- Đánh giá chiều hướng tác động (+ / -)
- Phân tích khả năng dự đoán GPA
""")

# =========================================================
# SELECT FEATURES
# =========================================================

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

# =========================================================
# ADD CONSTANT
# =========================================================

X = sm.add_constant(X)

# =========================================================
# BUILD MODEL
# =========================================================

model = sm.OLS(y, X).fit()

# =========================================================
# MODEL SUMMARY
# =========================================================

st.subheader("📄 OLS Regression Summary")

st.text(model.summary())

# =========================================================
# COEFFICIENT TABLE
# =========================================================

st.subheader("📊 Regression Coefficients")

coef_df = pd.DataFrame({
    "Feature": model.params.index,
    "Coefficient": model.params.values.round(4),
    "P-Value": model.pvalues.values.round(4)
})

st.dataframe(
    coef_df,
    use_container_width=True
)

# =========================================================
# VISUALIZE COEFFICIENTS
# =========================================================

st.subheader("📈 Feature Impact on GPA")

coef_plot = coef_df[coef_df["Feature"] != "const"]

fig, ax = plt.subplots(figsize=(9,5))

sns.barplot(
    data=coef_plot,
    x="Coefficient",
    y="Feature",
    ax=ax
)

ax.axvline(0, color='black', linestyle='--')

ax.set_title(
    "OLS Coefficients",
    fontsize=18,
    fontweight='bold'
)

st.pyplot(fig)

# =========================================================
# MODEL PERFORMANCE
# =========================================================

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

# =========================================================
# MOST IMPORTANT FACTORS
# =========================================================

important_feature = (
    coef_plot.iloc[
        coef_plot["Coefficient"].abs().idxmax()
    ]
)

# =========================================================
# INTERPRETATION
# =========================================================

st.info(f"""
📖 Nhận xét:

• Mô hình OLS cho thấy mức độ ảnh hưởng của từng yếu tố tới GPA.

• R² = {r2:.3f} cho thấy mô hình giải thích được khoảng
{r2*100:.1f}% sự biến động của GPA.

• Yếu tố ảnh hưởng mạnh nhất là
'{important_feature["Feature"]}'
với hệ số khoảng {important_feature["Coefficient"]:.2f}.

• Hệ số dương cho thấy yếu tố đó làm GPA tăng,
trong khi hệ số âm cho thấy GPA có xu hướng giảm.

• Absences thường có hệ số âm khá lớn,
cho thấy nghỉ học nhiều ảnh hưởng tiêu cực rõ rệt tới kết quả học tập.

• StudyTimeWeekly và ParentalSupport
thường có tác động tích cực tới GPA.

• Một số hoạt động ngoại khóa có tác động nhỏ,
cho thấy chúng hỗ trợ học tập ở mức vừa phải
thay vì quyết định trực tiếp GPA.

• Nhìn chung,
mô hình cho thấy sự chuyên cần và thời gian học tập
là những yếu tố quan trọng nhất ảnh hưởng đến kết quả học tập của sinh viên.
""")
