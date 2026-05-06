# 🏢 Team Task Manager - Full-Stack Web App

What it does: A full-stack team collaboration platform that enables efficient project and task management with real-time analytics.

Key Features:

Admin Dashboard: Visual analytics, task stats, pie charts
Project Management: Create, list, and track projects
Task Assignment: Assign tasks to team members with status tracking
Role-Based Access: Admin (full control) vs Member (view/update tasks)
Secure Authentication: JWT tokens + bcrypt password hashing
Who it's for:

Team Leads/Managers - Track progress, assign work, monitor productivity
Development Teams - Receive tasks, update status, view projects
Small-Medium Businesses - Simple, zero-config project management
Freelance Teams - Client project tracking without complex setup


## Acknowledgements


**Built with ❤️ using the Python ecosystem:**

### 🛠️ Core Technologies
- **FastAPI** - Lightning-fast API framework ([fastapi.tiangolo.com](https://fastapi.tiangolo.com))
- **Streamlit** - Python-first web apps ([streamlit.io](https://streamlit.io))
- **SQLAlchemy** - Database ORM powerhouse ([sqlalchemy.org](https://sqlalchemy.org))
- **Plotly** - Interactive charts & visualizations ([plotly.com/python](https://plotly.com/python))
- **JWT + bcrypt** - Secure authentication (python-jose, passlib)

### 📚 Learning Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Plotly Python Examples](https://plotly.com/python/)

### 🎨 Design Inspiration
- [Streamlit Component Templates](https://streamlit.io/components)
- [FastAPI Swagger UI](https://fastapi.tiangolo.com/tutorial/)
- Modern dashboard patterns (Trello, Jira)

###  Special Thanks
- **FastAPI Discord Community** - Quick debugging support
- **Streamlit Forum** - Layout & styling tips
- **Stack Overflow** - Edge case solutions
- **My teammates** - Testing & valuable feedback


### ⚖️ License
MIT License © 2026 [Rahul]
## API Reference

#Base URL:
`https://team-task-manager-production-cc44.up.railway.app`

#API Docs:
'https://team-task-api-production.up.railway.app/docs'(Swagger UI)

 #Authentication:
All endpoints (except auth) require JWT token:
Authorization: Bearer <your_token>
Authentication Endpoints:
Register New User :POST /auth/register
Body:
{
  "email": "user@team.com",
  "username": "user1", 
  "password": "securepass123",
  "role": "admin"  // or "member"
}
Response (200):
{
  "id": 1,
  "email": "admin2@gmail.com",
  "username": "Rahul2",
  "role": "admin"
}
User Login :POST /auth/login
Body:
{
  "email": "admin2@gmail.com",
  "password": "123123123"
}
Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin2@gmail.com",
    "username": "Rahul2",
    "role": "admin"
  }
}
 Projects Endpoints (Admin Only):
 -Create Project : POST /projects
 -Headers: Authorization: Bearer <token>
 -Body:
  {
  "name": "Website Redesign",
  "description": "Complete UI/UX overhaul"
  }
  -Response (201):
   {
  "id": 1,
  "name": "Website Redesign",
  "description": "Complete UI/UX overhaul",
  "owner_id": 1,
  "created_at": "2026-05-04T10:00:00"
   }
   -List All Projects:GET /projects
Tasks Endpoints (Admin Only):
-Create Task : POST /tasks
-Headers: Authorization: Bearer <token>
-Body:
  {
  "title": "Design homepage",
  "description": "Modern responsive design",
  "status": "pending",
  "project_id": 1,
  "assignee_id": 2,
  "due_date": "2026-05-10"
   }
-Response (201):
  {
  "id": 1,
  "title": "Design homepage",
  "status": "pending",
  "project_id": 1,
  "assignee_id": 2
   }
-List All Tasks:GET /tasks
-Headers: Authorization: Bearer <token>
-Response (200):
  [
  {
    "id": 1,
    "title": "Design homepage",
    "status": "pending",
    "due_date": "2026-05-10"
  }
  ]
-Update Task Status:PUT /tasks/{task_id}
-Headers: Authorization: Bearer <token>
-Body:
  {
  "status": "in-progress"
  }

## Appendix

### 🗄️ Database Schema

#### Users Table
sql:

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Projects Table:

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

Tasks Table:

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    project_id INTEGER,
    assignee_id INTEGER,
    due_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (assignee_id) REFERENCES users(id)
);

Configuration:

SECRET_KEY=your-super-secret-key-here-min32chars
DATABASE_URL=sqlite:///./task_manager.db

Custom Settings:

API_PORT=8000
STREAMLIT_PORT=8501
JWT_EXPIRE_MINUTES=30

 Testing Commands:

 # Reset database (fresh users)
python fix_user.py

# Check tables
python -c "import sqlite3; print(sqlite3.connect('task_manager.db').execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"

# View users
python -c "import sqlite3; [print(r) for r in sqlite3.connect('task_manager.db').execute('SELECT * FROM users')]"

Testing Commands:
# Reset database (fresh users)
python fix_user.py

# Check tables
python -c "import sqlite3; print(sqlite3.connect('task_manager.db').execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"

# View users
python -c "import sqlite3; [print(r) for r in sqlite3.connect('task_manager.db').execute('SELECT * FROM users')]"

Common Issues & Solutions:
Issue

Solution

Invalid credentials

python fix_user.py

Not authenticated

Add Authorization: Bearer <token> header

403 Forbidden

Login as admin (admin1@gmail.com)

No such table

python -c "from database import init_db; init_db()"

Token missing

Check st.session_state.token in login


## Authors

Primary Credits 
Lead Developer : Rahul 

Full-stack implementation :(FastAPI + Streamlit)
Authentication system :(JWT + bcrypt)
Dashboard analytics :+ Plotly charts
Deployment : automation


## Badges

## 🏅 Badges

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-brightgreen)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-blue)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

![Logo]
1. Task Logo: https://img.icons8.com/color/96/000000/tasks.png
2. Team Logo: https://img.icons8.com/fluency/96/team.png
3. Dashboard: https://img.icons8.com/fluency/96/analytics.png

## 🚀 About Me
 Hello My name is Rahul.I'm a full stack developer...


## Lessons Learned

## 📚 Lessons Learned

### 🎯 Key Takeaways

1. **FastAPI + Streamlit = Dream Team**
   - Full-stack Python = Zero context switching
   - Live reload workflow = 10x faster iteration
   - **Learned:** Modern Python web dev is SIMPLE

2. **JWT Auth Complexity**
   - **Challenge:** Token storage + headers everywhere
   - **Solution:** `st.session_state.token` + global headers
   - **Takeaway:** Central auth helper next time

3. **SQLite Transaction Gotchas**
   - **Challenge:** `VACUUM` inside transactions
   - **Solution:** `conn.commit()` before cleanup
   - **Takeaway:** Always commit before schema ops

4. **Streamlit Session State Magic**
   - **Challenge:** Login state persistence
   - **Solution:** `st.session_state` + `st.rerun()`
   - **Takeaway:** Reactive UI = State management solved

5. **API Schema Mismatches**
   - **Challenge:** `username` vs `email` confusion
   - **Solution:** Swagger docs + exact testing
   - **Takeaway:** Never assume field names

 Best Practices Discovered:
✅ Always test API endpoints manually first
✅ Store tokens in session_state immediately
✅ Add comprehensive error messages (response.text)
✅ Use st.stop() for auth guards
✅ Schema validation = 90% bugs prevented
✅ Hot reload = Catch issues instantly


## Running Tests

### 🔍 Unit Tests (Backend)
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run API tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

Test Coverage :

pip install pytest-cov
pytest tests/ --cov=api --cov-report=html
open htmlcov/index.html  # View coverage report

Test Structure :
tests/
├── test_api.py          # FastAPI endpoints
├── test_auth.py         # Login/register
├── test_db.py          # Database operations
├── test_models.py      # SQLAlchemy models
├── integration/
│   └── test_full_flow.py
└── fixtures/
    └── test_data.py

