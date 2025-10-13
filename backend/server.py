from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    username: str
    password: str
    role: Literal["student", "teacher", "admin"]
    name: str
    email: str
    profile_pic: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: Optional[User] = None
    message: Optional[str] = None

class Student(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    department: str
    year: int
    semester: int
    email: str
    phone: str
    profile_pic: Optional[str] = None

class Grade(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    student_id: str
    student_name: str
    subject: str
    subject_code: str
    part_a_marks: int  # Out of 10 (5×2)
    part_b_marks: int  # Out of 40 (5×8)
    total_marks: int   # Out of 50
    grade: str
    semester: int
    year: int

class Attendance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    student_id: str
    student_name: str
    subject: str
    subject_code: str
    total_classes: int
    attended_classes: int
    percentage: float
    semester: int

class StudyMaterial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    subject: str
    subject_code: str
    description: str
    file_url: str
    uploaded_by: str
    uploaded_date: str
    semester: int
    department: str

class LibraryBook(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    author: str
    isbn: str
    category: str
    available: bool
    total_copies: int
    available_copies: int

class Event(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    description: str
    date: str
    time: str
    location: str
    event_type: Literal["academic", "cultural", "sports", "holiday"]
    registration_required: bool
    registered_users: List[str] = []

class Complaint(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    description: str
    complaint_type: Literal["public", "private"]
    status: Literal["pending", "resolved"]
    submitted_by: str
    submitted_by_name: str
    submitted_date: str
    assigned_to: Optional[str] = None
    votes: int = 0
    voted_by: List[str] = []
    response: Optional[str] = None
    resolved_date: Optional[str] = None

class Schedule(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    teacher_id: str
    teacher_name: str
    subject: str
    subject_code: str
    day: str
    time_slot: str
    room: str
    department: str
    year: int
    semester: int

class Notice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    content: str
    posted_by: str
    posted_date: str
    priority: Literal["low", "medium", "high"]
    target_audience: List[str]  # ["student", "teacher", "all"]

class AttendanceWaiver(BaseModel):
    student_id: str
    subject_code: str
    reason: str

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "College Campus API"}

# Authentication
@api_router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    user = await db.users.find_one(
        {"username": request.username, "password": request.password},
        {"_id": 0}
    )
    
    if user:
        return LoginResponse(success=True, user=User(**user))
    else:
        return LoginResponse(success=False, message="Invalid credentials")

# Users
@api_router.get("/users", response_model=List[User])
async def get_users():
    users = await db.users.find({}, {"_id": 0}).to_list(1000)
    return users

@api_router.post("/users", response_model=User)
async def create_user(user: User):
    await db.users.insert_one(user.model_dump())
    return user

@api_router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    await db.users.update_one({"id": user_id}, {"$set": user.model_dump()})
    return user

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    await db.users.delete_one({"id": user_id})
    return {"message": "User deleted"}

# Students
@api_router.get("/students", response_model=List[Student])
async def get_students():
    students = await db.students.find({}, {"_id": 0}).to_list(1000)
    return students

@api_router.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = await db.students.find_one({"id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Grades
@api_router.get("/grades/{student_id}", response_model=List[Grade])
async def get_grades(student_id: str):
    grades = await db.grades.find({"student_id": student_id}, {"_id": 0}).to_list(1000)
    return grades

@api_router.get("/grades", response_model=List[Grade])
async def get_all_grades():
    grades = await db.grades.find({}, {"_id": 0}).to_list(1000)
    return grades

@api_router.post("/grades", response_model=Grade)
async def create_grade(grade: Grade):
    await db.grades.insert_one(grade.model_dump())
    return grade

@api_router.put("/grades/{grade_id}", response_model=Grade)
async def update_grade(grade_id: str, grade: Grade):
    await db.grades.update_one({"id": grade_id}, {"$set": grade.model_dump()})
    return grade

# Attendance
@api_router.get("/attendance/{student_id}", response_model=List[Attendance])
async def get_attendance(student_id: str):
    attendance = await db.attendance.find({"student_id": student_id}, {"_id": 0}).to_list(1000)
    return attendance

@api_router.get("/attendance", response_model=List[Attendance])
async def get_all_attendance():
    attendance = await db.attendance.find({}, {"_id": 0}).to_list(1000)
    return attendance

@api_router.post("/attendance/waive", response_model=dict)
async def waive_attendance(waiver: AttendanceWaiver):
    # Update attendance for specific student and subject
    attendance_record = await db.attendance.find_one(
        {"student_id": waiver.student_id, "subject_code": waiver.subject_code}
    )
    
    if attendance_record:
        # Set attendance to 100%
        await db.attendance.update_one(
            {"student_id": waiver.student_id, "subject_code": waiver.subject_code},
            {"$set": {"attended_classes": attendance_record["total_classes"], "percentage": 100.0}}
        )
        return {"success": True, "message": "Attendance waived"}
    else:
        raise HTTPException(status_code=404, detail="Attendance record not found")

# Study Materials
@api_router.get("/materials", response_model=List[StudyMaterial])
async def get_materials():
    materials = await db.materials.find({}, {"_id": 0}).to_list(1000)
    return materials

@api_router.post("/materials", response_model=StudyMaterial)
async def create_material(material: StudyMaterial):
    await db.materials.insert_one(material.model_dump())
    return material

# Library
@api_router.get("/library", response_model=List[LibraryBook])
async def get_library_books():
    books = await db.library.find({}, {"_id": 0}).to_list(1000)
    return books

# Events
@api_router.get("/events", response_model=List[Event])
async def get_events():
    events = await db.events.find({}, {"_id": 0}).to_list(1000)
    return events

@api_router.post("/events", response_model=Event)
async def create_event(event: Event):
    await db.events.insert_one(event.model_dump())
    return event

@api_router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: str, event: Event):
    await db.events.update_one({"id": event_id}, {"$set": event.model_dump()})
    return event

@api_router.post("/events/{event_id}/register")
async def register_for_event(event_id: str, user_id: dict):
    uid = user_id.get("user_id")
    event = await db.events.find_one({"id": event_id})
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if uid not in event.get("registered_users", []):
        await db.events.update_one(
            {"id": event_id},
            {"$push": {"registered_users": uid}}
        )
    
    return {"success": True, "message": "Registered for event"}

# Complaints
@api_router.get("/complaints", response_model=List[Complaint])
async def get_complaints():
    complaints = await db.complaints.find({}, {"_id": 0}).to_list(1000)
    return complaints

@api_router.get("/complaints/{complaint_id}", response_model=Complaint)
async def get_complaint(complaint_id: str):
    complaint = await db.complaints.find_one({"id": complaint_id}, {"_id": 0})
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@api_router.post("/complaints", response_model=Complaint)
async def create_complaint(complaint: Complaint):
    await db.complaints.insert_one(complaint.model_dump())
    return complaint

@api_router.post("/complaints/{complaint_id}/vote")
async def vote_complaint(complaint_id: str, user_id: dict):
    uid = user_id.get("user_id")
    complaint = await db.complaints.find_one({"id": complaint_id})
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    voted_by = complaint.get("voted_by", [])
    
    if uid in voted_by:
        # Remove vote
        await db.complaints.update_one(
            {"id": complaint_id},
            {"$pull": {"voted_by": uid}, "$inc": {"votes": -1}}
        )
        return {"success": True, "message": "Vote removed", "action": "removed"}
    else:
        # Add vote
        await db.complaints.update_one(
            {"id": complaint_id},
            {"$push": {"voted_by": uid}, "$inc": {"votes": 1}}
        )
        return {"success": True, "message": "Vote added", "action": "added"}

@api_router.put("/complaints/{complaint_id}/resolve", response_model=Complaint)
async def resolve_complaint(complaint_id: str, response_data: dict):
    await db.complaints.update_one(
        {"id": complaint_id},
        {"$set": {
            "status": "resolved",
            "response": response_data.get("response"),
            "resolved_date": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    complaint = await db.complaints.find_one({"id": complaint_id}, {"_id": 0})
    return complaint

# Schedules
@api_router.get("/schedules", response_model=List[Schedule])
async def get_schedules():
    schedules = await db.schedules.find({}, {"_id": 0}).to_list(1000)
    return schedules

@api_router.get("/schedules/teacher/{teacher_id}", response_model=List[Schedule])
async def get_teacher_schedules(teacher_id: str):
    schedules = await db.schedules.find({"teacher_id": teacher_id}, {"_id": 0}).to_list(1000)
    return schedules

@api_router.post("/schedules", response_model=Schedule)
async def create_schedule(schedule: Schedule):
    await db.schedules.insert_one(schedule.model_dump())
    return schedule

@api_router.put("/schedules/{schedule_id}", response_model=Schedule)
async def update_schedule(schedule_id: str, schedule: Schedule):
    await db.schedules.update_one({"id": schedule_id}, {"$set": schedule.model_dump()})
    return schedule

# Notices
@api_router.get("/notices", response_model=List[Notice])
async def get_notices():
    notices = await db.notices.find({}, {"_id": 0}).to_list(1000)
    return notices

@api_router.post("/notices", response_model=Notice)
async def create_notice(notice: Notice):
    await db.notices.insert_one(notice.model_dump())
    return notice

@api_router.delete("/notices/{notice_id}")
async def delete_notice(notice_id: str):
    await db.notices.delete_one({"id": notice_id})
    return {"message": "Notice deleted"}

# Reset Demo Data
@api_router.post("/reset-demo-data")
async def reset_demo_data():
    # Clear all collections
    await db.users.delete_many({})
    await db.students.delete_many({})
    await db.grades.delete_many({})
    await db.attendance.delete_many({})
    await db.materials.delete_many({})
    await db.library.delete_many({})
    await db.events.delete_many({})
    await db.complaints.delete_many({})
    await db.schedules.delete_many({})
    await db.notices.delete_many({})
    
    # Insert demo users
    demo_users = [
        # Students
        {"id": "S123", "username": "ai", "password": "alicepw", "role": "student", "name": "Alice James", "email": "alice@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice"},
        {"id": "S124", "username": "bob", "password": "bobpw", "role": "student", "name": "Bob Wilson", "email": "bob@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Bob"},
        {"id": "S125", "username": "carol", "password": "carolpw", "role": "student", "name": "Carol Martinez", "email": "carol@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Carol"},
        {"id": "S126", "username": "david", "password": "davidpw", "role": "student", "name": "David Chen", "email": "david@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=David"},
        {"id": "S127", "username": "emma", "password": "emmapw", "role": "student", "name": "Emma Thompson", "email": "emma@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emma"},
        # Teachers
        {"id": "T202", "username": "ai", "password": "vkumarpw", "role": "teacher", "name": "Prof. V. Kumar", "email": "vkumar@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kumar"},
        {"id": "T203", "username": "sraja", "password": "srajapw", "role": "teacher", "name": "Dr. S. Rajamanickam", "email": "sraja@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Raja"},
        # Admin
        {"id": "A001", "username": "ai", "password": "srinipw", "role": "admin", "name": "V. Srinivasan", "email": "admin@college.edu", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Srini"},
    ]
    await db.users.insert_many(demo_users)
    
    # Insert demo students
    demo_students = [
        {"id": "S123", "name": "Alice James", "department": "Computer Science", "year": 3, "semester": 5, "email": "alice@college.edu", "phone": "+91 9876543210", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice"},
        {"id": "S124", "name": "Bob Wilson", "department": "Computer Science", "year": 3, "semester": 5, "email": "bob@college.edu", "phone": "+91 9876543211", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Bob"},
        {"id": "S125", "name": "Carol Martinez", "department": "Electronics", "year": 2, "semester": 4, "email": "carol@college.edu", "phone": "+91 9876543212", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Carol"},
        {"id": "S126", "name": "David Chen", "department": "Mechanical", "year": 4, "semester": 7, "email": "david@college.edu", "phone": "+91 9876543213", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=David"},
        {"id": "S127", "name": "Emma Thompson", "department": "Computer Science", "year": 3, "semester": 5, "email": "emma@college.edu", "phone": "+91 9876543214", "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emma"},
    ]
    await db.students.insert_many(demo_students)
    
    # Insert demo grades (Anna University format)
    demo_grades = [
        {"id": "G1", "student_id": "S123", "student_name": "Alice James", "subject": "Data Structures", "subject_code": "CS301", "part_a_marks": 8, "part_b_marks": 35, "total_marks": 43, "grade": "A", "semester": 5, "year": 3},
        {"id": "G2", "student_id": "S123", "student_name": "Alice James", "subject": "Database Management", "subject_code": "CS302", "part_a_marks": 9, "part_b_marks": 38, "total_marks": 47, "grade": "A+", "semester": 5, "year": 3},
        {"id": "G3", "student_id": "S123", "student_name": "Alice James", "subject": "Operating Systems", "subject_code": "CS303", "part_a_marks": 7, "part_b_marks": 32, "total_marks": 39, "grade": "B+", "semester": 5, "year": 3},
        {"id": "G4", "student_id": "S124", "student_name": "Bob Wilson", "subject": "Data Structures", "subject_code": "CS301", "part_a_marks": 6, "part_b_marks": 28, "total_marks": 34, "grade": "B", "semester": 5, "year": 3},
        {"id": "G5", "student_id": "S125", "student_name": "Carol Martinez", "subject": "Digital Electronics", "subject_code": "EC201", "part_a_marks": 9, "part_b_marks": 36, "total_marks": 45, "grade": "A", "semester": 4, "year": 2},
    ]
    await db.grades.insert_many(demo_grades)
    
    # Insert demo attendance
    demo_attendance = [
        {"id": "AT1", "student_id": "S123", "student_name": "Alice James", "subject": "Data Structures", "subject_code": "CS301", "total_classes": 45, "attended_classes": 42, "percentage": 93.33, "semester": 5},
        {"id": "AT2", "student_id": "S123", "student_name": "Alice James", "subject": "Database Management", "subject_code": "CS302", "total_classes": 40, "attended_classes": 38, "percentage": 95.0, "semester": 5},
        {"id": "AT3", "student_id": "S123", "student_name": "Alice James", "subject": "Operating Systems", "subject_code": "CS303", "total_classes": 42, "attended_classes": 35, "percentage": 83.33, "semester": 5},
        {"id": "AT4", "student_id": "S124", "student_name": "Bob Wilson", "subject": "Data Structures", "subject_code": "CS301", "total_classes": 45, "attended_classes": 30, "percentage": 66.67, "semester": 5},
    ]
    await db.attendance.insert_many(demo_attendance)
    
    # Insert demo study materials
    demo_materials = [
        {"id": "M1", "title": "Data Structures - Lecture Notes", "subject": "Data Structures", "subject_code": "CS301", "description": "Complete lecture notes covering trees, graphs, and sorting algorithms", "file_url": "#", "uploaded_by": "Prof. V. Kumar", "uploaded_date": "2025-01-15", "semester": 5, "department": "Computer Science"},
        {"id": "M2", "title": "DBMS Tutorial - SQL Queries", "subject": "Database Management", "subject_code": "CS302", "description": "Practice SQL queries and normalization exercises", "file_url": "#", "uploaded_by": "Prof. V. Kumar", "uploaded_date": "2025-01-18", "semester": 5, "department": "Computer Science"},
        {"id": "M3", "title": "OS Concepts - Process Scheduling", "subject": "Operating Systems", "subject_code": "CS303", "description": "Detailed notes on CPU scheduling algorithms", "file_url": "#", "uploaded_by": "Dr. S. Rajamanickam", "uploaded_date": "2025-01-20", "semester": 5, "department": "Computer Science"},
    ]
    await db.materials.insert_many(demo_materials)
    
    # Insert demo library books
    demo_library = [
        {"id": "L1", "title": "Introduction to Algorithms", "author": "Cormen, Leiserson, Rivest, Stein", "isbn": "978-0262033848", "category": "Computer Science", "available": True, "total_copies": 5, "available_copies": 3},
        {"id": "L2", "title": "Database System Concepts", "author": "Silberschatz, Korth, Sudarshan", "isbn": "978-0073523323", "category": "Computer Science", "available": True, "total_copies": 4, "available_copies": 2},
        {"id": "L3", "title": "Operating System Concepts", "author": "Silberschatz, Galvin, Gagne", "isbn": "978-1118063330", "category": "Computer Science", "available": True, "total_copies": 6, "available_copies": 4},
        {"id": "L4", "title": "Digital Design", "author": "Morris Mano", "isbn": "978-0134549897", "category": "Electronics", "available": False, "total_copies": 3, "available_copies": 0},
    ]
    await db.library.insert_many(demo_library)
    
    # Insert demo events
    demo_events = [
        {"id": "E1", "title": "Tech Symposium 2025", "description": "Annual technical symposium with paper presentations and workshops", "date": "2025-03-15", "time": "09:00 AM", "location": "Main Auditorium", "event_type": "academic", "registration_required": True, "registered_users": ["S123", "S124"]},
        {"id": "E2", "title": "Cultural Fest - Vibrance 2025", "description": "Three-day cultural festival with music, dance, and drama competitions", "date": "2025-04-10", "time": "10:00 AM", "location": "Open Air Theatre", "event_type": "cultural", "registration_required": True, "registered_users": []},
        {"id": "E3", "title": "Sports Day", "description": "Inter-department sports competitions", "date": "2025-02-28", "time": "08:00 AM", "location": "Sports Ground", "event_type": "sports", "registration_required": True, "registered_users": ["S125"]},
        {"id": "E4", "title": "Pongal Holiday", "description": "Tamil harvest festival", "date": "2025-01-15", "time": "All Day", "location": "Campus Closed", "event_type": "holiday", "registration_required": False, "registered_users": []},
        {"id": "E5", "title": "Independence Day", "description": "National holiday", "date": "2025-08-15", "time": "All Day", "location": "Campus Closed", "event_type": "holiday", "registration_required": False, "registered_users": []},
    ]
    await db.events.insert_many(demo_events)
    
    # Insert demo complaints
    demo_complaints = [
        {"id": "C1", "title": "WiFi connectivity issues in hostel", "description": "Frequent disconnections and slow internet speed in hostel blocks A and B", "complaint_type": "public", "status": "pending", "submitted_by": "S123", "submitted_by_name": "Alice James", "submitted_date": "2025-01-20", "votes": 12, "voted_by": ["S123", "S124", "S125"]},
        {"id": "C2", "title": "Library AC not working", "description": "Air conditioning in the library has been non-functional for 2 weeks", "complaint_type": "public", "status": "pending", "submitted_by": "S124", "submitted_by_name": "Bob Wilson", "submitted_date": "2025-01-18", "votes": 8, "voted_by": ["S124", "S126"]},
        {"id": "C3", "title": "Cafeteria food quality", "description": "Need improvement in food quality and variety in the main cafeteria", "complaint_type": "public", "status": "resolved", "submitted_by": "S125", "submitted_by_name": "Carol Martinez", "submitted_date": "2025-01-10", "votes": 25, "voted_by": ["S123", "S124", "S125", "S126", "S127"], "response": "We have hired a new catering service and updated the menu. Please provide feedback.", "resolved_date": "2025-01-25"},
        {"id": "C4", "title": "Grade discrepancy in CS302", "description": "My internal marks don't match what was announced. Need clarification.", "complaint_type": "private", "status": "pending", "submitted_by": "S124", "submitted_by_name": "Bob Wilson", "submitted_date": "2025-01-22", "votes": 0, "voted_by": []},
        {"id": "C5", "title": "Attendance record error", "description": "Attendance shows 60% but I have submitted medical certificates for all absences", "complaint_type": "private", "status": "resolved", "submitted_by": "S126", "submitted_by_name": "David Chen", "submitted_date": "2025-01-15", "votes": 0, "voted_by": [], "response": "Medical certificates verified. Attendance updated to 85%.", "resolved_date": "2025-01-23"},
    ]
    await db.complaints.insert_many(demo_complaints)
    
    # Insert demo schedules
    demo_schedules = [
        {"id": "SCH1", "teacher_id": "T202", "teacher_name": "Prof. V. Kumar", "subject": "Data Structures", "subject_code": "CS301", "day": "Monday", "time_slot": "09:00 AM - 10:00 AM", "room": "CS Lab 1", "department": "Computer Science", "year": 3, "semester": 5},
        {"id": "SCH2", "teacher_id": "T202", "teacher_name": "Prof. V. Kumar", "subject": "Database Management", "subject_code": "CS302", "day": "Tuesday", "time_slot": "10:00 AM - 11:00 AM", "room": "Room 301", "department": "Computer Science", "year": 3, "semester": 5},
        {"id": "SCH3", "teacher_id": "T202", "teacher_name": "Prof. V. Kumar", "subject": "Data Structures", "subject_code": "CS301", "day": "Wednesday", "time_slot": "02:00 PM - 03:00 PM", "room": "CS Lab 1", "department": "Computer Science", "year": 3, "semester": 5},
        {"id": "SCH4", "teacher_id": "T203", "teacher_name": "Dr. S. Rajamanickam", "subject": "Operating Systems", "subject_code": "CS303", "day": "Thursday", "time_slot": "11:00 AM - 12:00 PM", "room": "Room 302", "department": "Computer Science", "year": 3, "semester": 5},
    ]
    await db.schedules.insert_many(demo_schedules)
    
    # Insert demo notices
    demo_notices = [
        {"id": "N1", "title": "Semester Exam Schedule Released", "content": "The semester 5 examination schedule has been released. Check the academic calendar for details.", "posted_by": "Admin Office", "posted_date": "2025-01-20", "priority": "high", "target_audience": ["student", "teacher"]},
        {"id": "N2", "title": "Library Timings Extended", "content": "Library will be open till 10 PM during exam season (Feb 1 - Feb 28)", "posted_by": "Library", "posted_date": "2025-01-22", "priority": "medium", "target_audience": ["student"]},
        {"id": "N3", "title": "Faculty Meeting - Feb 5", "content": "All faculty members are requested to attend the meeting at 3 PM in Conference Hall", "posted_by": "Principal Office", "posted_date": "2025-01-25", "priority": "high", "target_audience": ["teacher"]},
    ]
    await db.notices.insert_many(demo_notices)
    
    return {"success": True, "message": "Demo data reset successfully"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()