import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AdminDashboard(tk.Frame):
    def __init__(self, parent, logout_callback):
        super().__init__(parent, bg='#ffffff')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.logout_callback = logout_callback
        
        self.sidebar = tk.Frame(self, bg='#1e3a8a', width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.content = tk.Frame(self, bg='#ffffff')
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        self.show_timetable()
    
    def create_sidebar(self):
        tk.Label(self.sidebar, text="MPACC", font=("Arial", 18, "bold"), 
                bg='#1e3a8a', fg='white').pack(pady=20)
        
        tk.Label(self.sidebar, text="Administrator", 
                font=("Arial", 12), bg='#1e3a8a', fg='white').pack(pady=5)
        
        tk.Frame(self.sidebar, height=2, bg='#3b82f6').pack(fill=tk.X, pady=20)
        
        btn_timetable = tk.Button(self.sidebar, text="Manage Timetable", font=("Arial", 11), 
                                bg='#1e3a8a', fg='white', bd=0, 
                                command=self.show_timetable, cursor='hand2', anchor='w', padx=20)
        btn_timetable.pack(fill=tk.X, pady=5)
        
        btn_holidays = tk.Button(self.sidebar, text="Manage Holidays", font=("Arial", 11), 
                               bg='#1e3a8a', fg='white', bd=0, 
                               command=self.show_holidays, cursor='hand2', anchor='w', padx=20)
        btn_holidays.pack(fill=tk.X, pady=5)
        
        btn_accounts = tk.Button(self.sidebar, text="Manage Accounts", font=("Arial", 11), 
                               bg='#1e3a8a', fg='white', bd=0, 
                               command=self.show_accounts, cursor='hand2', anchor='w', padx=20)
        btn_accounts.pack(fill=tk.X, pady=5)
        
        btn_students = tk.Button(self.sidebar, text="View All Students", font=("Arial", 11), 
                               bg='#1e3a8a', fg='white', bd=0, 
                               command=self.show_students, cursor='hand2', anchor='w', padx=20)
        btn_students.pack(fill=tk.X, pady=5)
        
        btn_complaints = tk.Button(self.sidebar, text="Complaints Management", font=("Arial", 11), 
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
    
    def show_timetable(self):
        self.clear_content()
        
        tk.Label(self.content, text="Manage Timetable", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        btn_add = tk.Button(self.content, text="+ Add Schedule", font=("Arial", 11), 
                          bg='#3b82f6', fg='white', command=self.add_timetable_entry)
        btn_add.pack(pady=10, anchor='e', padx=30)
        
        tree_frame = tk.Frame(self.content, bg='#ffffff')
        tree_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Subject', 'Day', 'Time'), 
                           show='headings', height=15)
        
        tree.heading('ID', text='ID')
        tree.heading('Subject', text='Subject')
        tree.heading('Day', text='Day')
        tree.heading('Time', text='Time')
        
        tree.column('ID', width=50)
        tree.column('Subject', width=250)
        tree.column('Day', width=150)
        tree.column('Time', width=200)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, c.subject_name, t.day, t.time
            FROM timetable t
            JOIN classes c ON t.class_id = c.class_id
            ORDER BY t.day, t.time
        ''')
        entries = cursor.fetchall()
        conn.close()
        
        for entry in entries:
            tree.insert('', tk.END, values=entry)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_timetable_entry(self):
        add_window = tk.Toplevel(self.content)
        add_window.title("Add Timetable Entry")
        add_window.geometry("400x400")
        add_window.configure(bg='#ffffff')
        
        tk.Label(add_window, text="Add Timetable Entry", font=("Arial", 16, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20)
        
        form_frame = tk.Frame(add_window, bg='#f8fafc')
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Class:", font=("Arial", 11), bg='#f8fafc').pack(pady=5)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT class_id, subject_name FROM classes')
        classes = cursor.fetchall()
        conn.close()
        
        class_var = tk.StringVar()
        class_dropdown = ttk.Combobox(form_frame, textvariable=class_var, state='readonly')
        class_dropdown['values'] = [f"{c[0]}: {c[1]}" for c in classes]
        class_dropdown.pack(pady=5)
        
        tk.Label(form_frame, text="Day:", font=("Arial", 11), bg='#f8fafc').pack(pady=5)
        day_var = tk.StringVar()
        day_dropdown = ttk.Combobox(form_frame, textvariable=day_var, state='readonly')
        day_dropdown['values'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_dropdown.pack(pady=5)
        
        tk.Label(form_frame, text="Time:", font=("Arial", 11), bg='#f8fafc').pack(pady=5)
        time_entry = tk.Entry(form_frame, font=("Arial", 11))
        time_entry.pack(pady=5)
        time_entry.insert(0, "9:00 AM - 10:00 AM")
        
        def save_entry():
            if not class_var.get() or not day_var.get() or not time_entry.get():
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            class_id = int(class_var.get().split(':')[0])
            subject = class_var.get().split(': ')[1]
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO timetable (class_id, day, time, subject) VALUES (?, ?, ?, ?)',
                         (class_id, day_var.get(), time_entry.get(), subject))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Timetable entry added successfully!")
            add_window.destroy()
            self.show_timetable()
        
        btn_save = tk.Button(form_frame, text="Save", font=("Arial", 12, "bold"), 
                           bg='#1e3a8a', fg='white', command=save_entry)
        btn_save.pack(pady=20)
    
    def show_holidays(self):
        self.clear_content()
        
        tk.Label(self.content, text="Manage Holidays", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        btn_add = tk.Button(self.content, text="+ Add Holiday", font=("Arial", 11), 
                          bg='#3b82f6', fg='white', command=self.add_holiday)
        btn_add.pack(pady=10, anchor='e', padx=30)
        
        tree_frame = tk.Frame(self.content, bg='#ffffff')
        tree_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Date', 'Description'), 
                           show='headings', height=15)
        
        tree.heading('ID', text='ID')
        tree.heading('Date', text='Date')
        tree.heading('Description', text='Description')
        
        tree.column('ID', width=50)
        tree.column('Date', width=150)
        tree.column('Description', width=350)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, date, description FROM holidays ORDER BY date')
        holidays = cursor.fetchall()
        conn.close()
        
        for holiday in holidays:
            tree.insert('', tk.END, values=holiday)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_holiday(self):
        add_window = tk.Toplevel(self.content)
        add_window.title("Add Holiday")
        add_window.geometry("400x300")
        add_window.configure(bg='#ffffff')
        
        tk.Label(add_window, text="Add Holiday", font=("Arial", 16, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20)
        
        form_frame = tk.Frame(add_window, bg='#f8fafc')
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Arial", 11), bg='#f8fafc').pack(pady=5)
        date_entry = tk.Entry(form_frame, font=("Arial", 11))
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="Description:", font=("Arial", 11), bg='#f8fafc').pack(pady=5)
        desc_entry = tk.Entry(form_frame, font=("Arial", 11))
        desc_entry.pack(pady=5)
        
        def save_holiday():
            if not date_entry.get() or not desc_entry.get():
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO holidays (date, description) VALUES (?, ?)',
                         (date_entry.get(), desc_entry.get()))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Holiday added successfully!")
            add_window.destroy()
            self.show_holidays()
        
        btn_save = tk.Button(form_frame, text="Save", font=("Arial", 12, "bold"), 
                           bg='#1e3a8a', fg='white', command=save_holiday)
        btn_save.pack(pady=20)
    
    def show_accounts(self):
        self.clear_content()
        
        tk.Label(self.content, text="Manage Accounts", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        tk.Label(self.content, text="User account management coming soon...", 
                font=("Arial", 14), bg='#ffffff', fg='#64748b').pack(pady=40)
    
    def show_students(self):
        self.clear_content()
        
        tk.Label(self.content, text="View All Students", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        tree_frame = tk.Frame(self.content, bg='#ffffff')
        tree_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Department'), 
                           show='headings', height=15)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Department', text='Department')
        
        tree.column('ID', width=100)
        tree.column('Name', width=250)
        tree.column('Department', width=200)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT student_id, name, dept FROM students')
        students = cursor.fetchall()
        conn.close()
        
        for student in students:
            tree.insert('', tk.END, values=student)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_complaints(self):
        self.clear_content()
        
        tk.Label(self.content, text="Complaints Management", font=("Arial", 24, "bold"), 
                bg='#ffffff', fg='#1e3a8a').pack(pady=20, anchor='w', padx=30)
        
        tree_frame = tk.Frame(self.content, bg='#ffffff')
        tree_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Student Name', 'Student ID', 'Complaint', 'Status'), 
                           show='headings', height=15)
        
        tree.heading('ID', text='Complaint ID')
        tree.heading('Student Name', text='Student Name')
        tree.heading('Student ID', text='Student ID')
        tree.heading('Complaint', text='Complaint Text')
        tree.heading('Status', text='Status')
        
        tree.column('ID', width=80)
        tree.column('Student Name', width=150)
        tree.column('Student ID', width=100)
        tree.column('Complaint', width=300)
        tree.column('Status', width=100)
        
        conn = sqlite3.connect('mpacc.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, student_id, complaint_text, status FROM complaints ORDER BY id DESC')
        complaints = cursor.fetchall()
        conn.close()
        
        for complaint in complaints:
            complaint_id, name, student_id, text, status = complaint
            tag = 'pending' if status == 'Pending' else 'resolved'
            tree.insert('', tk.END, values=(complaint_id, name, student_id, text, status), tags=(tag,))
        
        tree.tag_configure('pending', background='#fef3c7')
        tree.tag_configure('resolved', background='#d1fae5')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        buttons_frame = tk.Frame(self.content, bg='#ffffff')
        buttons_frame.pack(pady=10, padx=30, fill=tk.X)
        
        def mark_pending():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a complaint")
                return
            
            complaint_id = tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE complaints SET status = ? WHERE id = ?', ('Pending', complaint_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Complaint marked as Pending")
            self.show_complaints()
        
        def mark_resolved():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a complaint")
                return
            
            complaint_id = tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE complaints SET status = ? WHERE id = ?', ('Resolved', complaint_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Complaint marked as Resolved")
            self.show_complaints()
        
        def delete_complaint():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a complaint")
                return
            
            complaint_id = tree.item(selected[0])['values'][0]
            
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this complaint?")
            if not confirm:
                return
            
            conn = sqlite3.connect('mpacc.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM complaints WHERE id = ?', (complaint_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Complaint deleted")
            self.show_complaints()
        
        btn_pending = tk.Button(buttons_frame, text="Mark as Pending", font=("Arial", 11), 
                              bg='#f59e0b', fg='white', command=mark_pending)
        btn_pending.pack(side=tk.LEFT, padx=5)
        
        btn_resolved = tk.Button(buttons_frame, text="Mark as Resolved", font=("Arial", 11), 
                               bg='#10b981', fg='white', command=mark_resolved)
        btn_resolved.pack(side=tk.LEFT, padx=5)
        
        btn_delete = tk.Button(buttons_frame, text="Delete Complaint", font=("Arial", 11), 
                             bg='#dc2626', fg='white', command=delete_complaint)
        btn_delete.pack(side=tk.LEFT, padx=5)
