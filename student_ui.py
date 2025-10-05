import tkinter as tk
from tkinter import ttk
import utils
from datetime import datetime

class StudentDashboard(tk.Frame):
    def __init__(self, parent, student_info, logout_callback):
        super().__init__(parent, bg='#ffffff')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.student_info = student_info
        self.logout_callback = logout_callback
        
        self.sidebar = tk.Frame(self, bg='#1e3a8a', width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.content = tk.Frame(self, bg='#ffffff')
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        self.show_home()
    
    def create_sidebar(self):
        tk.Label(self.sidebar, text="MPACC", font=("Arial", 18, "bold"), 
                bg='#1e3a8a', fg='white').pack(pady=20)
        
        tk.Label(self.sidebar, text=self.student_info['name'], 
                font=("Arial", 12), bg='#1e3a8a', fg='white').pack(pady=5)
        tk.Label(self.sidebar, text=f"ID: {self.student_info['student_id']}", 
                font=("Arial", 10), bg='#1e3a8a', fg='#cbd5e1').pack(pady=2)
        tk.Label(self.sidebar, text=f"Dept: {self.student_info['dept']}", 
                font=("Arial", 10), bg='#1e3a8a', fg='#cbd5e1').pack(pady=2)
        
        tk.Frame(self.sidebar, height=2, bg='#3b82f6').pack(fill=tk.X, pady=20)
        
        btn_home = tk.Button(self.sidebar, text="Home", font=("Arial", 11), 
                           bg='#1e3a8a', fg='white', bd=0, 
                           command=self.show_home, cursor='hand2', anchor='w', padx=20)
        btn_home.pack(fill=tk.X, pady=5)
        
        btn_cgpa = tk.Button(self.sidebar, text="CGPA & Scores", font=("Arial", 11), 
                           bg='#1e3a8a', fg='white', bd=0, 
                           command=self.show_cgpa, cursor='hand2', anchor='w', padx=20)
        btn_cgpa.pack(fill=tk.X, pady=5)
        
        tk.Frame(self.sidebar, height=1, bg='#3b82f6').pack(fill=tk.X, pady=200)
        
        btn_logout = tk.Button(self.sidebar, text="Logout", font=("Arial", 11), 
                             bg='#dc2626', fg='white', bd=0, 
                             command=self.logout_callback, cursor='hand2')
        btn_logout.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_content()
        
        tk.Label(self.content, text="Dashboard", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        events = utils.get_upcoming_events(self.student_info['student_id'])
        
        calendar_frame = tk.Frame(self.content, bg='#f8fafc', bd=2, relief=tk.RIDGE)
        calendar_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(calendar_frame, text="Upcoming Events & Holidays", 
                font=("Arial", 16, "bold"), bg='#f8fafc', fg='#1e3a8a').pack(pady=15)
        
        if events:
            for event in events:
                event_frame = tk.Frame(calendar_frame, bg='#ffffff', bd=1, relief=tk.SOLID)
                event_frame.pack(pady=5, padx=20, fill=tk.X)
                
                date_obj = datetime.strptime(event['date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%b %d, %Y')
                
                tk.Label(event_frame, text=formatted_date, 
                        font=("Arial", 11, "bold"), bg='#ffffff', fg='#3b82f6').pack(side=tk.LEFT, padx=10, pady=8)
                tk.Label(event_frame, text=event['description'], 
                        font=("Arial", 11), bg='#ffffff').pack(side=tk.LEFT, padx=10, pady=8)
                tk.Label(event_frame, text=event['type'], 
                        font=("Arial", 9), bg='#dbeafe', fg='#1e3a8a').pack(side=tk.RIGHT, padx=10, pady=8)
        else:
            tk.Label(calendar_frame, text="No upcoming events", 
                    font=("Arial", 12), bg='#f8fafc', fg='#64748b').pack(pady=20)
    
    def show_cgpa(self):
        self.clear_content()
        
        tk.Label(self.content, text="CGPA & Scores", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        cgpa = utils.calculate_cgpa(self.student_info['student_id'])
        
        cgpa_frame = tk.Frame(self.content, bg='#1e3a8a', bd=2, relief=tk.RIDGE)
        cgpa_frame.pack(pady=10, padx=30, fill=tk.X)
        
        tk.Label(cgpa_frame, text="Current CGPA", font=("Arial", 14), 
                bg='#1e3a8a', fg='white').pack(pady=10)
        tk.Label(cgpa_frame, text=f"{cgpa}", font=("Arial", 36, "bold"), 
                bg='#1e3a8a', fg='#3b82f6').pack(pady=10)
        tk.Label(cgpa_frame, text="(Anna University Formula: CGPA = Σ(grade_point × credit) / Σ(credits))", 
                font=("Arial", 9), bg='#1e3a8a', fg='#cbd5e1').pack(pady=5, padx=10)
        
        scores_frame = tk.Frame(self.content, bg='#ffffff')
        scores_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(scores_frame, text="Detailed Scores", font=("Arial", 16, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=10)
        
        tree_frame = tk.Frame(scores_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('Subject', 'Type', 'Score', 'Max Score', 'Percentage'), 
                           show='headings', height=10)
        
        tree.heading('Subject', text='Subject')
        tree.heading('Type', text='Type')
        tree.heading('Score', text='Score')
        tree.heading('Max Score', text='Max Score')
        tree.heading('Percentage', text='Percentage')
        
        tree.column('Subject', width=200)
        tree.column('Type', width=100)
        tree.column('Score', width=80)
        tree.column('Max Score', width=100)
        tree.column('Percentage', width=100)
        
        scores = utils.get_student_scores(self.student_info['student_id'])
        
        for score in scores:
            subject, score_val, max_score, score_type = score
            percentage = (score_val / max_score * 100) if max_score > 0 else 0
            tree.insert('', tk.END, values=(subject, score_type, score_val, max_score, f"{percentage:.1f}%"))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
