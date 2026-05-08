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
📖 Interpretation:

- Histogram shows the distribution of student GPA.
- The KDE curve helps identify the overall trend.
- If the graph peaks around high GPA values, most students perform well.
- If the distribution is skewed left/right, it indicates imbalance in academic performance.
""")
