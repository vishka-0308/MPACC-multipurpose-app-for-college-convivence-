import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TeacherDashboard(tk.Frame):
    def __init__(self, parent, teacher_info, logout_callback):
        super().__init__(parent, bg='#ffffff')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.teacher_info = teacher_info
        self.logout_callback = logout_callback
        self.selected_class = None
        self.selected_student = None
        # Top header / top-right logout
        self.topbar = tk.Frame(self, bg='#ffffff', height=50)
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.topbar, text="Teacher Dashboard", font=("Arial", 14, "bold"),
                 bg='#ffffff', fg='#1e3a8a').pack(side=tk.LEFT, padx=20, pady=10)
        btn_logout_top = tk.Button(self.topbar, text="Logout", font=("Arial", 10),
                                   bg='#dc2626', fg='white', bd=0,
                                   command=self.logout_callback, cursor='hand2')
        btn_logout_top.pack(side=tk.RIGHT, padx=10, pady=8)

        self.sidebar = tk.Frame(self, bg='#1e3a8a', width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content = tk.Frame(self, bg='#ffffff')
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        self.show_classes()
    
    def create_sidebar(self):
        tk.Label(self.sidebar, text="MPACC", font=("Arial", 18, "bold"), 
                bg='#1e3a8a', fg='white').pack(pady=20)
        
        tk.Label(self.sidebar, text=self.teacher_info['name'], 
                font=("Arial", 12), bg='#1e3a8a', fg='white').pack(pady=5)
        tk.Label(self.sidebar, text="Teacher", 
                font=("Arial", 10), bg='#1e3a8a', fg='#cbd5e1').pack(pady=2)
        
        tk.Frame(self.sidebar, height=2, bg='#3b82f6').pack(fill=tk.X, pady=20)
        
        btn_classes = tk.Button(self.sidebar, text="My Classes", font=("Arial", 11), 
                              bg='#1e3a8a', fg='white', bd=0, 
                              command=self.show_classes, cursor='hand2', anchor='w', padx=20)
        btn_classes.pack(fill=tk.X, pady=5)
        
        tk.Frame(self.sidebar, height=1, bg='#3b82f6').pack(fill=tk.X, pady=300)
        
        btn_logout = tk.Button(self.sidebar, text="Logout", font=("Arial", 11), 
                             bg='#dc2626', fg='white', bd=0, 
                             command=self.logout_callback, cursor='hand2')
        btn_logout.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_classes(self):
        self.clear_content()
        self.selected_class = None
        self.selected_student = None
        
        tk.Label(self.content, text="My Classes", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT class_id, subject_name, credits 
            FROM classes 
            WHERE teacher_id = ?
        ''', (self.teacher_info['teacher_id'],))
        classes = cursor.fetchall()
        conn.close()
        
        classes_frame = tk.Frame(self.content, bg='#ffffff')
        classes_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        for class_data in classes:
            class_id, subject_name, credits = class_data
            
            class_card = tk.Frame(classes_frame, bg='#f8fafc', bd=2, relief=tk.RIDGE)
            class_card.pack(pady=10, fill=tk.X)
            
            tk.Label(class_card, text=subject_name, font=("Arial", 14, "bold"), 
                    bg='#f8fafc', fg='#1e3a8a').pack(side=tk.LEFT, padx=20, pady=15)
            tk.Label(class_card, text=f"Credits: {credits}", font=("Arial", 11), 
                    bg='#f8fafc', fg='#64748b').pack(side=tk.LEFT, padx=10)
            
            btn_view = tk.Button(class_card, text="View Students", font=("Arial", 10), 
                               bg='#3b82f6', fg='white', 
                               command=lambda cid=class_id, cname=subject_name: self.show_students(cid, cname))
            btn_view.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def show_students(self, class_id, class_name):
        self.clear_content()
        self.selected_class = class_id
        
        tk.Button(self.content, text="← Back to Classes", font=("Arial", 11), 
                 bg='#64748b', fg='white', bd=0, 
                 command=self.show_classes).pack(pady=10, anchor='w', padx=30)
        
        tk.Label(self.content, text=f"{class_name} - Students", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=10, anchor='w', padx=30)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT s.student_id, s.name, s.dept
            FROM students s
            JOIN (
                SELECT student_id FROM assignments WHERE class_id = ?
                UNION
                SELECT student_id FROM tests WHERE class_id = ?
            ) enrolled ON s.student_id = enrolled.student_id
        ''', (class_id, class_id))
        students = cursor.fetchall()
        conn.close()
        
        students_frame = tk.Frame(self.content, bg='#ffffff')
        students_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        for student in students:
            student_id, name, dept = student
            
            student_card = tk.Frame(students_frame, bg='#f8fafc', bd=2, relief=tk.RIDGE)
            student_card.pack(pady=5, fill=tk.X)
            
            tk.Label(student_card, text=name, font=("Arial", 12, "bold"), 
                    bg='#f8fafc', fg='#1e3a8a').pack(side=tk.LEFT, padx=20, pady=10)
            tk.Label(student_card, text=f"Dept: {dept}", font=("Arial", 10), 
                    bg='#f8fafc', fg='#64748b').pack(side=tk.LEFT, padx=10)
            
            btn_scores = tk.Button(student_card, text="Update Scores", font=("Arial", 10), 
                                 bg='#3b82f6', fg='white', 
                                 command=lambda sid=student_id, sname=name: self.update_scores(sid, sname))
            btn_scores.pack(side=tk.RIGHT, padx=20, pady=5)
    
    def update_scores(self, student_id, student_name):
        self.selected_student = student_id
        
        update_window = tk.Toplevel(self.content)
        update_window.title(f"Update Scores - {student_name}")
        update_window.geometry("500x400")
        update_window.configure(bg='#ffffff')
        
        tk.Label(update_window, text=f"Update Scores for {student_name}", 
                font=("Arial", 16, "bold"), bg='#ffffff', fg='#1e3a8a').pack(pady=20)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, score, max_score FROM assignments WHERE student_id = ? AND class_id = ?', 
                      (student_id, self.selected_class))
        assignment = cursor.fetchone()
        
        cursor.execute('SELECT id, score, max_score FROM tests WHERE student_id = ? AND class_id = ?', 
                      (student_id, self.selected_class))
        test = cursor.fetchone()
        
        conn.close()
        
        form_frame = tk.Frame(update_window, bg='#f8fafc', bd=2, relief=tk.RIDGE)
        form_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Assignment Score", font=("Arial", 12), 
                bg='#f8fafc').pack(pady=10)
        assignment_entry = tk.Entry(form_frame, font=("Arial", 12))
        assignment_entry.pack(pady=5)
        if assignment:
            assignment_entry.insert(0, str(assignment[1]))
        
        tk.Label(form_frame, text="Test Score", font=("Arial", 12), 
                bg='#f8fafc').pack(pady=10)
        test_entry = tk.Entry(form_frame, font=("Arial", 12))
        test_entry.pack(pady=5)
        if test:
            test_entry.insert(0, str(test[1]))
        
        def save_scores():
            try:
                assignment_score = float(assignment_entry.get())
                test_score = float(test_entry.get())
                
                conn = sqlite3.connect('mpacc.db')
                cursor = conn.cursor()
                
                if assignment:
                    cursor.execute('UPDATE assignments SET score = ? WHERE id = ?', 
                                 (assignment_score, assignment[0]))
                
                if test:
                    cursor.execute('UPDATE tests SET score = ? WHERE id = ?', 
                                 (test_score, test[0]))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Scores updated successfully!")
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric scores")
        
        btn_save = tk.Button(form_frame, text="Save Scores", font=("Arial", 12, "bold"), 
                           bg='#1e3a8a', fg='white', command=save_scores)
        btn_save.pack(pady=20)
