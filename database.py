import pyodbc
from config import SERVER_NAME, DATABASE_NAME, DRIVER_NAME

def create_connection():
    """SQL Server bazası ilə əlaqə yaradır."""
    try:
        connection_string = (
            f"DRIVER={DRIVER_NAME};"
            f"SERVER={SERVER_NAME};"
            f"DATABASE={DATABASE_NAME};"
            f"Trusted_connection=yes;"
        )
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as error:
        print(f"Bağlantı xatası detalları: {error}")
        return None

def add_student(student_name, student_score):
    """Bazaya yeni tələbə əlavə edir."""
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Students (Name, Score) VALUES (?, ?)"
        cursor.execute(query, (student_name, student_score))
        connection.commit()
        return True
    except Exception as error:
        print(f"Tələbə əlavə olunarkən xəta: {error}")
        return False
    finally:
        connection.close()

def get_all_students():
    """Bazadakı bütün tələbələri çəkir."""
    connection = create_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Id, Name, Score FROM Students")
        rows = cursor.fetchall()
        
        students_list = []
        for row in rows:
            students_list.append({
                "Id": row.Id,
                "Name": row.Name,
                "Score": row.Score
            })
        return students_list
    except Exception as error:
        print(f"Məlumatları çəkərkən xəta: {error}")
        return []
    finally:
        connection.close()