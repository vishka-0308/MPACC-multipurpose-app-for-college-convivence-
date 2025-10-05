# MPACC - Multi Purpose Application for Campus Convenience

## Overview

MPACC (Multi Purpose Application for Campus Convenience) is a desktop application built with Python that serves as a campus management system. The application provides role-based dashboards for three user types: students, teachers, and administrators. Students can view their schedules, grades, and CGPA; teachers can manage classes and student assessments; and administrators can manage timetables, holidays, and user accounts. The system uses a local SQLite database for data persistence and Tkinter for the graphical user interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **UI Framework**: Pure Tkinter-based desktop application with no external dependencies
- **Design Pattern**: Frame-based component architecture where each user role has a dedicated UI module
- **Layout Strategy**: Sidebar navigation with content area pattern - consistent across all dashboards with a left sidebar (200px) containing navigation and user info, and an expandable content area on the right
- **Styling Approach**: Inline styling with consistent color scheme (blue theme: #1e3a8a for primary, #3b82f6 for accents, #ffffff for backgrounds)
- **Component Organization**: Separate UI modules for each role (`student_ui.py`, `teacher_ui.py`, `admin_ui.py`) with shared utilities in `utils.py`

### Backend Architecture
- **Database Layer**: SQLite with direct SQL queries (no ORM)
- **Authentication**: SHA-256 password hashing for user credentials
- **Data Access Pattern**: Direct database connections per operation (no connection pooling or session management)
- **Business Logic**: Utility functions in `utils.py` for calculations (CGPA, grade conversions) and shared operations
- **Session Management**: In-memory session state stored in main application class, tracking current user and active frame

### Database Schema
- **users**: Stores login credentials and roles (student/teacher/admin)
- **students**: Student profiles linked to user accounts via foreign key
- **teachers**: Teacher profiles linked to user accounts via foreign key
- **classes**: Course information with teacher assignments
- **Relational Model**: Foreign key relationships between users and role-specific tables, with classes linked to teachers
- **Assessment Tables**: Separate tables for assignments and tests (referenced in code but schema not fully shown in provided files)
- **Grading System**: Anna University-style CGPA calculation with 30% assignment weight and 70% test weight

### Application Flow
- **Entry Point**: `main.py` initializes the database and displays login screen
- **Role-Based Routing**: After authentication, users are directed to role-specific dashboards based on user role field
- **Navigation Pattern**: Callback-based navigation with logout callbacks passed to child components
- **State Management**: Current user info and active frame tracked in main application class

### Key Architectural Decisions

**Decision: Tkinter for UI**
- Rationale: No external dependencies requirement, built-in Python library
- Pros: Zero setup, cross-platform, lightweight
- Cons: Limited modern UI capabilities, requires manual styling

**Decision: SQLite for Database**
- Rationale: Local persistence requirement, single-user desktop application
- Pros: No server setup, file-based, SQL support
- Cons: Limited concurrency, not suitable for multi-user scenarios

**Decision: Direct SQL Queries**
- Rationale: Simplicity and no external library constraints
- Pros: Full control over queries, no ORM overhead
- Cons: More verbose, potential SQL injection risks if not careful, no automatic schema migrations

**Decision: SHA-256 Password Hashing**
- Rationale: Built-in Python hashlib, adequate security for local application
- Pros: No external dependencies, deterministic hashing
- Cons: No salt (less secure), not suitable for production web applications

**Decision: Frame-Based Component Architecture**
- Rationale: Tkinter's widget system naturally supports frame composition
- Pros: Clear separation of concerns, reusable layouts
- Cons: Manual frame lifecycle management required

## External Dependencies

### Core Dependencies
- **Python Standard Library Only**: tkinter (GUI), sqlite3 (database), hashlib (password hashing), datetime (date/time operations)
- **No Third-Party Packages**: Application designed to run with Python 3 standard library only

### Database
- **SQLite**: Local file-based database (`mpacc.db`) stored in application directory
- **Schema Initialization**: Automatic table creation on first run via `database.init_database()`
- **No External Database Server**: Completely self-contained data storage

### Integration Points
- **No External APIs**: Fully offline application
- **No Cloud Services**: All data stored locally
- **No Authentication Providers**: Built-in user management system