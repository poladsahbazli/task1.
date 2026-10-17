import streamlit as st
import pandas as pd
from database import add_student, get_all_students
from services import calculate_grade, calculate_statistics

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

# --- SİDEBAR: Tələbə Əlavə Etmə Paneli ---
st.sidebar.header("Add New Student")

with st.sidebar.form("student_form", clear_on_submit=True):
    student_name = st.text_input("Student Name")
    student_score = st.number_input("Score", min_value=0, max_value=100, step=1)
    submit_button = st.form_submit_button("Add Student")
    
    if submit_button:
        if not student_name or student_name.strip() == "":
            st.sidebar.error("Zəhmət olmasa tələbənin adını daxil edin!")
        else:
            is_success = add_student(student_name.strip(), student_score)
            if is_success:
                st.sidebar.success(f"'{student_name}' uğurla əlavə olundu!")
                # Keşi təmizləyirik ki, yeni tələbə dərhal siyahıya düşsün
                st.cache_data.clear()
            else:
                st.sidebar.error("Baza ilə əlaqə zamanı xəta baş verdi.")

# --- MƏLUMATLARI KEŞLƏMƏK (Sürət üçün) ---
@st.cache_data(ttl=5) # Hər 5 saniyədən bir və ya keş təmizlənəndə yenilənir
def load_students():
    raw_data = get_all_students()
    if raw_data:
        processed_data = []
        for student in raw_data:
            processed_data.append({
                "Name": student["Name"],
                "Score": student["Score"],
                "Grade": calculate_grade(student["Score"])
            })
        return pd.DataFrame(processed_data)
    return pd.DataFrame(columns=["Name", "Score", "Grade"])

df = load_students()

# --- ƏSAS HİSSƏ: Axtarış Sətri ---
search_query = st.text_input("🔍 Search Student (by name)")

# Böyük və kiçik hərf fərqi qoymadan anlıq axtarış filteri
if search_query and not df.empty:
    filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Statistikaları hesablayırıq
students_data_for_stats = filtered_df.to_dict(orient="records")
stats = calculate_statistics(students_data_for_stats)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", stats["total_students"])
col2.metric("Average Score", stats["average_score"])
col3.metric("Highest Score", stats["highest_score"])
col4.metric("Lowest Score", stats["lowest_score"])

st.markdown("---")

# --- TƏLƏBƏLƏRİN CƏDVƏLİ ---
st.subheader("Student List & Grades")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("Heç bir tələbə tapılmadı.")