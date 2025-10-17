MPACC — Multi-Purpose Application for Campus Convenience
===============================================

What this project is
--------------------
MPACC is a small desktop application (built with Python and a simple database) made to help college students, teachers, and administrators do common tasks in one place. It provides separate screens for three types of users:

- Students: View events, submit complaints, and see scores.
- Teachers: View classes, update student scores.
- Admins: Manage timetable, holidays, students, and complaints.

The app uses a simple local database (SQLite) and a graphical interface so you can run it on your computer without complex setup.

Who this README is for
----------------------
This README is written so anyone can understand and run the project — no deep technical background is required. It explains what the project does, how to start it on a Windows PC, and what each file is for.

Quick demo (run locally)
------------------------
1. Make sure you have Python 3.10 or newer installed. (You can download Python from python.org.)
2. Open PowerShell and go to the project folder:

   cd "C:\Users\welcome\Desktop\CampusUtility"

3. (Optional but recommended) Create a virtual environment and activate it:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

4. Install the required packages (used by some parts of the project):

   pip install -r backend\requirements.txt

5. Run the app (desktop GUI):

   python main.py

6. Use the demo login credentials shown on the login screen to enter each role:

   - Admin:  username = admin1    password = adminpass
   - Teacher: username = teacher1  password = teachpass
   - Student: username = student1  password = studpass

What to expect when the app opens
---------------------------------
You will see a login screen where you choose a role (Student/Teacher/Admin), and enter username and password. After login you will see a screen (dashboard) tailored to that role. There is a Logout button on the left sidebar and also a visible Logout button at the top-right of every dashboard.

Important files (plain language)
--------------------------------
- main.py — The program you run. It shows the login screen, remembers who is logged in, and switches to the right dashboard.
- database.py — Sets up the local database (SQLite). It creates tables and sample data if needed.
- utils.py — Helper functions used across the app (for example: checking your username/password, calculating CGPA).
- student_ui.py — The student screen (what students see and can do).
- teacher_ui.py — The teacher screen (what teachers see and can do).
- admin_ui.py — The administrator screen (manage timetable, holidays, complaints).
- mpacc.db — The local SQLite database file used to store data. This file is usually kept locally and is ignored by the project when publishing (so your personal data stays on your machine).

Notes about the code (non-technical)
-----------------------------------
- The app uses simple building blocks: windows, panels, buttons, and lists. When you click a button the program runs some code that changes what is shown or updates the database.
- The logout button simply tells the main program: "forget the current user and show the login screen again." This is already implemented and the new top-right button does the same thing as the sidebar Logout.
- If you see an error when starting the app, check that Python is installed and that the `mpacc.db` file is present in the project folder.

If you want to change the demo logins
------------------------------------
The login credentials are checked in `utils.py` using the `users` table in the local database. You can open `mpacc.db` with a SQLite browser (many free tools are available) and view or change the usernames and passwords.

Want help? Next steps I can do for you
-------------------------------------
- Add a packaged executable so the app can be run by double-clicking (Windows .exe).
- Remove temporary or history files from the Git history.
- Add a simple installer or a step-by-step video walkthrough.

If you want any of those, tell me which and I'll implement them.

Thank you — enjoy MPACC!
