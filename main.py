import tkinter as tk
from tkinter import messagebox
import database
import utils
import student_ui
import teacher_ui
import admin_ui

class MPACCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MPACC - Multi Purpose Application for Campus Convenience")
        self.root.geometry("900x600")
        self.root.configure(bg='#ffffff')
        
        database.init_database()
        
        self.current_user = None
        self.current_frame = None
        
        self.show_login()
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login(self):
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#ffffff')
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(self.current_frame, text="MPACC", font=("Arial", 32, "bold"), 
                              bg='#ffffff', fg='#1e3a8a')
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(self.current_frame, 
                                 text="Multi Purpose Application for Campus Convenience", 
                                 font=("Arial", 12), bg='#ffffff', fg='#64748b')
        subtitle_label.pack(pady=5)
        
        login_frame = tk.Frame(self.current_frame, bg='#f8fafc', bd=2, relief=tk.RIDGE)
        login_frame.pack(pady=40, padx=200)
        
        tk.Label(login_frame, text="Login", font=("Arial", 20, "bold"), 
                bg='#f8fafc', fg='#1e3a8a').pack(pady=20)
        
        tk.Label(login_frame, text="Username:", font=("Arial", 12), 
                bg='#f8fafc').pack(pady=5)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", font=("Arial", 12), 
                bg='#f8fafc').pack(pady=5)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), 
                                       width=30, show='*')
        self.password_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Role:", font=("Arial", 12), 
                bg='#f8fafc').pack(pady=5)
        
        self.role_var = tk.StringVar(value='student')
        
        role_frame = tk.Frame(login_frame, bg='#f8fafc')
        role_frame.pack(pady=5)
        
        tk.Radiobutton(role_frame, text="Student", variable=self.role_var, 
                      value='student', font=("Arial", 11), bg='#f8fafc').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(role_frame, text="Teacher", variable=self.role_var, 
                      value='teacher', font=("Arial", 11), bg='#f8fafc').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(role_frame, text="Admin", variable=self.role_var, 
                      value='admin', font=("Arial", 11), bg='#f8fafc').pack(side=tk.LEFT, padx=10)
        
        login_btn = tk.Button(login_frame, text="Login", font=("Arial", 12, "bold"), 
                            bg='#1e3a8a', fg='white', width=20, 
                            command=self.handle_login)
        login_btn.pack(pady=20)
        
        info_label = tk.Label(self.current_frame, 
                             text="Demo Credentials:\nAdmin: admin1/adminpass | Teacher: teacher1/teachpass | Student: student1/studpass", 
                             font=("Arial", 9), bg='#ffffff', fg='#94a3b8')
        info_label.pack(pady=10)
    
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        expected_role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        user = utils.authenticate_user(username, password)
        
        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return
        
        if user['role'] != expected_role:
            messagebox.showerror("Error", f"This user is not a {expected_role}")
            return
        
        self.current_user = user
        
        if user['role'] == 'student':
            self.show_student_dashboard()
        elif user['role'] == 'teacher':
            self.show_teacher_dashboard()
        elif user['role'] == 'admin':
            self.show_admin_dashboard()
    
    def show_student_dashboard(self):
        self.clear_frame()
        student_info = utils.get_student_info(self.current_user['user_id'])
        if student_info:
            self.current_frame = student_ui.StudentDashboard(self.root, student_info, self.logout)
    
    def show_teacher_dashboard(self):
        self.clear_frame()
        teacher_info = utils.get_teacher_info(self.current_user['user_id'])
        if teacher_info:
            self.current_frame = teacher_ui.TeacherDashboard(self.root, teacher_info, self.logout)
    
    def show_admin_dashboard(self):
        self.clear_frame()
        self.current_frame = admin_ui.AdminDashboard(self.root, self.logout)
    
    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == '__main__':
    root = tk.Tk()
    app = MPACCApp(root)
    root.mainloop()
