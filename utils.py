import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_cgpa(student_id):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.credits, 
               AVG((a.score / a.max_score) * 100) as avg_assignment,
               AVG((t.score / t.max_score) * 100) as avg_test
        FROM classes c
        LEFT JOIN assignments a ON c.class_id = a.class_id AND a.student_id = ?
        LEFT JOIN tests t ON c.class_id = t.class_id AND t.student_id = ?
        WHERE a.student_id = ? OR t.student_id = ?
        GROUP BY c.class_id, c.credits
    ''', (student_id, student_id, student_id, student_id))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return 0.0
    
    total_grade_points = 0
    total_credits = 0
    
    for credits, avg_assignment, avg_test in results:
        avg_assignment = avg_assignment or 0
        avg_test = avg_test or 0
        
        overall_percentage = (avg_assignment * 0.3 + avg_test * 0.7)
        
        grade_point = percentage_to_grade_point(overall_percentage)
        
        total_grade_points += grade_point * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    cgpa = total_grade_points / total_credits
    return round(cgpa, 2)

def percentage_to_grade_point(percentage):
    if percentage >= 90:
        return 10
    elif percentage >= 80:
        return 9
    elif percentage >= 70:
        return 8
    elif percentage >= 60:
        return 7
    elif percentage >= 50:
        return 6
    elif percentage >= 40:
        return 5
    else:
        return 0

def get_student_scores(student_id):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.subject_name, a.score, a.max_score, 'Assignment' as type
        FROM assignments a
        JOIN classes c ON a.class_id = c.class_id
        WHERE a.student_id = ?
        UNION ALL
        SELECT c.subject_name, t.score, t.max_score, 'Test' as type
        FROM tests t
        JOIN classes c ON t.class_id = c.class_id
        WHERE t.student_id = ?
        ORDER BY subject_name
    ''', (student_id, student_id))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_upcoming_events(student_id):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT date, description FROM holidays
        WHERE date >= date('now')
        ORDER BY date
    ''')
    
    events = [{'type': 'Holiday', 'date': row[0], 'description': row[1]} 
              for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT due_date, description FROM assignments
        WHERE student_id = ? AND due_date >= date('now')
        ORDER BY due_date
    ''', (student_id,))
    
    events.extend([{'type': 'Assignment', 'date': row[0], 'description': row[1]} 
                   for row in cursor.fetchall()])
    
    cursor.execute('''
        SELECT exam_date, description FROM tests
        WHERE student_id = ? AND exam_date >= date('now')
        ORDER BY exam_date
    ''', (student_id,))
    
    events.extend([{'type': 'Exam', 'date': row[0], 'description': row[1]} 
                   for row in cursor.fetchall()])
    
    events.sort(key=lambda x: x['date'])
    
    conn.close()
    return events

def authenticate_user(username, password):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, role FROM users WHERE username = ? AND password = ?',
                   (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {'user_id': result[0], 'role': result[1]}
    return None

def get_student_info(user_id):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT student_id, name, dept FROM students WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {'student_id': result[0], 'name': result[1], 'dept': result[2]}
    return None

def get_teacher_info(user_id):
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT teacher_id, name FROM teachers WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {'teacher_id': result[0], 'name': result[1]}
    return None
