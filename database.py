import sqlite3
import hashlib
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    conn = sqlite3.connect('mpacc.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dept TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            subject_name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            class_id INTEGER,
            score REAL,
            max_score REAL DEFAULT 100,
            due_date TEXT,
            description TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            class_id INTEGER,
            score REAL,
            max_score REAL DEFAULT 100,
            exam_date TEXT,
            description TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            day TEXT,
            time TEXT,
            subject TEXT,
            FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        populate_dummy_data(cursor)
    
    conn.commit()
    conn.close()

def populate_dummy_data(cursor):
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('admin1', hash_password('adminpass'), 'admin'))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('teacher1', hash_password('teachpass'), 'teacher'))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('student1', hash_password('studpass'), 'student'))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('student2', hash_password('studpass2'), 'student'))
    
    cursor.execute("INSERT INTO teachers (name, user_id) VALUES (?, ?)",
                   ('Dr. Rajesh Kumar', 2))
    
    cursor.execute("INSERT INTO students (name, dept, user_id) VALUES (?, ?, ?)",
                   ('Arun Prakash', 'CSE', 3))
    cursor.execute("INSERT INTO students (name, dept, user_id) VALUES (?, ?, ?)",
                   ('Priya Sharma', 'ECE', 4))
    
    cursor.execute("INSERT INTO classes (teacher_id, subject_name, credits) VALUES (?, ?, ?)",
                   (1, 'Data Structures', 4))
    cursor.execute("INSERT INTO classes (teacher_id, subject_name, credits) VALUES (?, ?, ?)",
                   (1, 'Database Management Systems', 3))
    cursor.execute("INSERT INTO classes (teacher_id, subject_name, credits) VALUES (?, ?, ?)",
                   (1, 'Operating Systems', 4))
    
    today = datetime.now()
    assignment1_due = (today + timedelta(days=5)).strftime('%Y-%m-%d')
    assignment2_due = (today + timedelta(days=10)).strftime('%Y-%m-%d')
    test1_date = (today + timedelta(days=12)).strftime('%Y-%m-%d')
    test2_date = (today + timedelta(days=18)).strftime('%Y-%m-%d')
    
    cursor.execute("INSERT INTO assignments (student_id, class_id, score, max_score, due_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, 1, 85, 100, assignment1_due, 'Binary Tree Implementation'))
    cursor.execute("INSERT INTO assignments (student_id, class_id, score, max_score, due_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, 2, 90, 100, assignment2_due, 'SQL Query Optimization'))
    cursor.execute("INSERT INTO assignments (student_id, class_id, score, max_score, due_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (2, 1, 78, 100, assignment1_due, 'Binary Tree Implementation'))
    
    cursor.execute("INSERT INTO tests (student_id, class_id, score, max_score, exam_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, 1, 88, 100, test1_date, 'Mid-Term Exam - Data Structures'))
    cursor.execute("INSERT INTO tests (student_id, class_id, score, max_score, exam_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, 2, 92, 100, test2_date, 'Mid-Term Exam - DBMS'))
    cursor.execute("INSERT INTO tests (student_id, class_id, score, max_score, exam_date, description) VALUES (?, ?, ?, ?, ?, ?)",
                   (2, 1, 82, 100, test1_date, 'Mid-Term Exam - Data Structures'))
    
    cursor.execute("INSERT INTO timetable (class_id, day, time, subject) VALUES (?, ?, ?, ?)",
                   (1, 'Monday', '9:00 AM - 10:00 AM', 'Data Structures'))
    cursor.execute("INSERT INTO timetable (class_id, day, time, subject) VALUES (?, ?, ?, ?)",
                   (2, 'Tuesday', '10:00 AM - 11:00 AM', 'Database Management Systems'))
    
    holiday1 = (today + timedelta(days=7)).strftime('%Y-%m-%d')
    holiday2 = (today + timedelta(days=15)).strftime('%Y-%m-%d')
    
    cursor.execute("INSERT INTO holidays (date, description) VALUES (?, ?)",
                   (holiday1, 'Diwali Festival'))
    cursor.execute("INSERT INTO holidays (date, description) VALUES (?, ?)",
                   (holiday2, 'Annual Day'))

if __name__ == '__main__':
    init_database()
    print("Database initialized with dummy data!")
