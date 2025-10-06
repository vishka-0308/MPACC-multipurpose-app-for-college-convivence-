import tkinter as tk
from tkinter import ttk, messagebox
import utils
from datetime import datetime
import sqlite3

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
        
        btn_complaints = tk.Button(self.sidebar, text="Complaint Portal", font=("Arial", 11), 
                                  bg='#1e3a8a', fg='white', bd=0, 
                                  command=self.show_complaints, cursor='hand2', anchor='w', padx=20)
        btn_complaints.pack(fill=tk.X, pady=5)
        
        tk.Frame(self.sidebar, height=1, bg='#3b82f6').pack(fill=tk.X, pady=150)
        
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
    
    def show_complaints(self):
        self.clear_content()
        
        tk.Label(self.content, text="Complaint Portal", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        form_frame = tk.Frame(self.content, bg='#f8fafc', bd=2, relief=tk.RIDGE)
        form_frame.pack(pady=10, padx=30, fill=tk.X)
        
        tk.Label(form_frame, text="Submit New Complaint", font=("Arial", 16, "bold"), 
                bg='#f8fafc', fg='#1e3a8a').pack(pady=15)
        
        input_frame = tk.Frame(form_frame, bg='#f8fafc')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(input_frame, text="Name:", font=("Arial", 11), bg='#f8fafc').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        name_entry.grid(row=0, column=1, pady=5, padx=10)
        name_entry.insert(0, self.student_info['name'])
        name_entry.config(state='readonly')
        
        tk.Label(input_frame, text="Student ID:", font=("Arial", 11), bg='#f8fafc').grid(row=1, column=0, sticky='w', pady=5)
        id_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        id_entry.grid(row=1, column=1, pady=5, padx=10)
        id_entry.insert(0, str(self.student_info['student_id']))
        id_entry.config(state='readonly')
        
        tk.Label(input_frame, text="Complaint:", font=("Arial", 11), bg='#f8fafc').grid(row=2, column=0, sticky='nw', pady=5)
        complaint_text = tk.Text(input_frame, font=("Arial", 11), width=40, height=6)
        complaint_text.grid(row=2, column=1, pady=5, padx=10)
        
        def submit_complaint():
            complaint = complaint_text.get("1.0", tk.END).strip()
            if not complaint:
                messagebox.showerror("Error", "Please enter your complaint")
                return
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO complaints (student_id, name, complaint_text, status) VALUES (?, ?, ?, ?)",
                         (self.student_info['student_id'], self.student_info['name'], complaint, 'Pending'))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Complaint submitted successfully!")
            complaint_text.delete("1.0", tk.END)
            self.show_complaints()
        
        btn_submit = tk.Button(form_frame, text="Submit Complaint", font=("Arial", 12, "bold"), 
                             bg='#1e3a8a', fg='white', command=submit_complaint)
        btn_submit.pack(pady=15)
        
        complaints_frame = tk.Frame(self.content, bg='#ffffff')
        complaints_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(complaints_frame, text="My Complaints", font=("Arial", 16, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=10)
        
        tree_frame = tk.Frame(complaints_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Complaint', 'Status'), 
                           show='headings', height=10)
        
        tree.heading('ID', text='Complaint ID')
        tree.heading('Complaint', text='Complaint Text')
        tree.heading('Status', text='Status')
        
        tree.column('ID', width=100)
        tree.column('Complaint', width=400)
        tree.column('Status', width=100)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, complaint_text, status FROM complaints WHERE student_id = ? ORDER BY id DESC',
                      (self.student_info['student_id'],))
        complaints = cursor.fetchall()
        conn.close()
        
        for complaint in complaints:
            complaint_id, text, status = complaint
            tag = 'pending' if status == 'Pending' else 'resolved'
            tree.insert('', tk.END, values=(complaint_id, text, status), tags=(tag,))
        
        tree.tag_configure('pending', background='#fef3c7')
        tree.tag_configure('resolved', background='#d1fae5')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
