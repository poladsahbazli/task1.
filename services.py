from config import (
    EXCELLENT_THRESHOLD, GOOD_THRESHOLD, AVERAGE_THRESHOLD, PASS_THRESHOLD,
    GRADE_EXCELLENT, GRADE_GOOD, GRADE_AVERAGE, GRADE_PASS, GRADE_FAIL
)

def calculate_grade(score):
    """Bala əsasən hərf qiymətini hesablayır."""
    if score >= EXCELLENT_THRESHOLD:
        return GRADE_EXCELLENT
    elif score >= GOOD_THRESHOLD:
        return GRADE_GOOD
    elif score >= AVERAGE_THRESHOLD:
        return GRADE_AVERAGE
    elif score >= PASS_THRESHOLD:
        return GRADE_PASS
    else:
        return GRADE_FAIL

def calculate_statistics(students_data):
    """Tələbə nəticələri üzrə ümumi statistikaları hesablayır."""
    if not students_data:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "highest_score": 0,
            "lowest_score": 0
        }
    
    scores = [student["Score"] for student in students_data]
    
    total_students = len(scores)
    average_score = round(sum(scores) / total_students, 1)
    highest_score = max(scores)
    lowest_score = min(scores)
    
    return {
        "total_students": total_students,
        "average_score": average_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score
    }