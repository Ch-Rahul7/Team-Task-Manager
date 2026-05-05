import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# Config
<<<<<<< HEAD
API_BASE = "https://team-task-manager-production-cc44.up.railway.app"
=======
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
>>>>>>> c53cdf0a2ba008d5bc54cc14da04b63385e43821
st.set_page_config(page_title="Team Task Manager", layout="wide")

# Simple Session-based Auth (No external library)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = "member"

def login():
    st.markdown("""
    <style>
    .main-container { max-width: 450px; margin: 3rem auto; padding: 1rem; }
    .login-card { 
        background: rgba(255,255,255,0.95); padding: 3rem 2.5rem; 
        border-radius: 25px; box-shadow: 0 30px 60px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.4);
    }
    .form-title { 
        text-align: center; color: #2c3e50; margin-bottom: 2rem; 
        font-size: 2.2rem; font-weight: 700;
    }
    .input-field {
        width: 100%; padding: 16px 20px; margin: 15px 0; 
        border: 2px solid #e1e8ed; border-radius: 15px; font-size: 16px;
        background: #f8fafc; transition: all 0.3s ease; box-sizing: border-box;
    }
    .input-field:focus {
        border-color: #4f46e5; background: white; 
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
    }
    .required::after { content: " *"; color: #ef4444; font-weight: bold; }
    .submit-btn {
        width: 100%; padding: 18px; margin: 25px 0 15px 0;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white; border: none; border-radius: 15px; font-size: 17px;
        font-weight: 600; cursor: pointer; transition: all 0.3s;
    }
    .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 20px 40px rgba(79, 70, 229, 0.3); }
    .toggle-btn {
        width: 100%; padding: 14px; margin: 20px 0;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white; border: none; border-radius: 12px; font-size: 16px;
        font-weight: 600; cursor: pointer; transition: all 0.3s;
    }
    .toggle-btn:hover { transform: translateY(-1px); box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3); }
    .demo-box {
        background: linear-gradient(135deg, #ec4899, #f43f5e); border-radius: 15px;
        padding: 20px; margin-top: 30px; color: white; text-align: center;
        box-shadow: 0 10px 30px rgba(236, 72, 153, 0.3);
    }
    .form-row { display: flex; gap: 15px; }
    .form-row .input-field { flex: 1; margin-bottom: 20px !important; }
    @media (max-width: 700px) { .form-row { flex-direction: column; } }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h2 class="form-title">🏢 Team Task Manager</h2>', unsafe_allow_html=True)
    
    # Initialize session state
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False
    if "email_signin" not in st.session_state:
        st.session_state.email_signin = ""
    
    # SIGN IN FORM (Default - Button at BOTTOM)
    if not st.session_state.show_signup:
        st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2.5rem;">Welcome back! Please sign in to continue.</p>', unsafe_allow_html=True)
        
        # Sign In Fields
        email = st.text_input("Email", placeholder="admin@example.com", value=st.session_state.email_signin, key="email_signin_input")
        password = st.text_input("Password", type="password", placeholder="•••••••", key="password_signin")
        
        # Sign In Button - BOTTOM
        if st.button("🔐 Sign In", key="btn_signin", type="primary"):
            try:
                response = requests.post(f"{API_BASE}/auth/login", json={
                    "email": email,     # API expects email!
                    "password": password
                })
                
                if response.status_code == 200:
                    user_data = response.json()
                    st.session_state.logged_in = True
                    st.session_state.username = user_data["user"]["username"]
                    st.session_state.role = user_data["user"]["role"]
                    st.session_state.email = email
                    st.session_state.email_signin = email
                    st.session_state.token = user_data["access_token"]
                    st.success(f"✅ Welcome {st.session_state.username}!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        # Toggle to Signup - Separate button
        st.markdown("---")
        if st.button("➕ Don't have an account? Create Account", key="toggle_to_signup"):
            st.session_state.show_signup = True
            st.rerun()
    
    # SIGN UP FORM
    else:
        st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2.5rem;">Create your Team Task Manager account</p>', unsafe_allow_html=True)
        
        # Signup fields
        name = st.text_input("Full Name", placeholder="John Doe", key="name")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", placeholder="john@company.com", key="email")
        with col2:
            mobile = st.text_input("Mobile No.", placeholder="+1 234 567 8900", key="mobile")
        
        col3, col4 = st.columns(2)
        with col3:
            job_id = st.text_input("Job ID", placeholder="EMP001", key="jobid")
        with col4:
            role_options = st.selectbox("Role", ["member", "admin"], key="role")
        
        password = st.text_input("Password", type="password", placeholder="••••••••", key="password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="confirmpw")
        
        # Sign Up Button - BOTTOM
        if st.button("✅ Create Account", key="btn_signup", type="primary"):
            if all([name, email, mobile, job_id, role_options, password, confirm_password]):
                if password == confirm_password:
                    st.session_state.logged_in = True
                    st.session_state.username = name
                    st.session_state.role = role_options
                    st.session_state.email = email
                    st.session_state.mobile = mobile
                    st.session_state.job_id = job_id
                    st.session_state.email_signin = email
                    st.success(f"✅ Welcome {name}! Account created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.error("❌ Please fill all fields marked with *")
        
        # Toggle back to Sign In
        st.markdown("---")
        if st.button("👤 Already have an account? Sign In", key="toggle_to_signin"):
            st.session_state.show_signup = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo accounts
    with st.expander("🔑 Quick Demo Accounts"):
        st.markdown("""
        **Admin:** `admin@example.com` / `admin123`  
        **Member:** `member@example.com` / `member123`
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def dashboard():
    st.header("📊 Dashboard")
    
    if not st.session_state.get("token"):
        st.error("🔐 Login required!")
        st.stop()
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # FULL HEIGHT 50/50 VERTICAL SPLIT
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("### 📈 Tasks ")
        # TASKS CONTENT
        tasks_resp = requests.get(f"{API_BASE}/tasks", headers=headers)
        if tasks_resp.status_code == 200:
            tasks = tasks_resp.json()
            df = pd.DataFrame(tasks) if tasks else pd.DataFrame()
            
            # Stats
            c1, c2, c3, c4 = st.columns(4)
            total = len(df)
            pending = len(df[df['status'] == 'pending']) if not df.empty else 0
            progress = len(df[df['status'] == 'in-progress']) if not df.empty else 0
            completed = len(df[df['status'] == 'completed']) if not df.empty else 0
            
            with c1: st.metric("Total", total)
            with c2: st.metric("Pending", pending)
            with c3: st.metric("In Progress", progress)
            with c4: st.metric("Completed", completed)
            
            # Chart + Table
            if total > 0:
                fig = px.pie(values=[pending, progress, completed], 
                           names=['Pending','Progress','Done'])
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Recent Tasks")
            st.dataframe(df[['title','status']].tail(5) if not df.empty else "No tasks", height=200)
        st.markdown("---")  # Spacer
    
    with right_col:
        st.markdown("### 📁 Projects ")
        # PROJECTS CONTENT
        proj_resp = requests.get(f"{API_BASE}/projects", headers=headers)
        if proj_resp.status_code == 200:
            projects = proj_resp.json()
            df_proj = pd.DataFrame(projects) if projects else pd.DataFrame()
            
            st.metric("Projects", len(df_proj))
            
            if not df_proj.empty:
                proj_display = df_proj[['id', 'name']].copy()
                proj_display.columns = ['#', 'Name']
                st.dataframe(proj_display, use_container_width=True, height=400)
            else:
                st.info("📭 Create projects first!")
        st.markdown("---")  # Spacer
def projects():
    st.header("📁 Projects")
    
    # 1. TOKEN CHECK
    if "token" not in st.session_state or not st.session_state.token:
        st.error("❌ No token! Login again.")
        st.stop()
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # 2. CREATE FORM
    with st.form("create_project"):
        name = st.text_input("Project Name")
        desc = st.text_area("Description")
        if st.form_submit_button("Create"):
            try:
                response = requests.post(f"{API_BASE}/projects",
                                       json={"name": name, "description": desc},
                                       headers=headers)
                st.write(f"Status: {response.status_code}")  # DEBUG
                st.write(f"Response: {response.text}")       # DEBUG
                if response.status_code in [200, 201]:
                    st.success("✅ Created!")
                    st.rerun()
                else:
                    st.error("❌ Failed!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # 3. LIST
    try:
        resp = requests.get(f"{API_BASE}/projects", headers=headers)
        if resp.status_code == 200:
            st.dataframe(pd.DataFrame(resp.json()))
    except:
        st.error("List failed")
def tasks():
    st.header("✅ Tasks")
    
    # TOKEN CHECK (same as projects)
    if not st.session_state.get("token"):
        st.error("🔐 Login required!")
        st.stop()
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Create Task
    with st.form("create_task"):
        title = st.text_input("Task Title")
        desc = st.text_area("Description")
        status = st.selectbox("Status", ["pending", "in-progress", "completed"])
        due_date = st.date_input("Due Date", value=date.today())
        
        col1, col2 = st.columns(2)
        with col1:
            project_id = st.number_input("Project ID", min_value=0, value=0)
        with col2:
            assignee_id = st.number_input("Assignee ID", min_value=0, value=0)
        
        if st.form_submit_button("Add Task"):
            try:
                task_data = {
                    "title": title,
                    "description": desc,
                    "status": status,
                    "due_date": due_date.isoformat()
                }
                if project_id > 0:
                    task_data["project_id"] = int(project_id)
                if assignee_id > 0:
                    task_data["assignee_id"] = int(assignee_id)
                    
                response = requests.post(f"{API_BASE}/tasks", 
                                       json=task_data,
                                       headers=headers)  # TOKEN!
                if response.status_code in [200, 201]:
                    st.success("✅ Task Created!")
                    st.rerun()
                else:
                    st.error(f"❌ {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # List Tasks
    try:
        response = requests.get(f"{API_BASE}/tasks", headers=headers)  # TOKEN!
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                st.dataframe(pd.DataFrame(tasks))
            else:
                st.info("📭 No tasks yet")
    except Exception as e:
        st.error(f"List error: {e}")
# Main App
def main():
    st.sidebar.title("🏢 Team Task Manager")
    
    if not st.session_state.logged_in:
        login()
    else:
        st.sidebar.success(f"👋 {st.session_state.username}")
        st.sidebar.markdown("---")
        
        page = st.sidebar.selectbox("Navigate", ["📊 Dashboard", "📁 Projects", "✅ Tasks"])
        
        if st.sidebar.button("🔓 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = "member"
            st.rerun()
        
        if page == "📊 Dashboard":
            dashboard()
        elif page == "📁 Projects":
            if st.session_state.role == "admin":
                projects()
            else:
                st.warning("👤 Members can't manage projects")
        elif page == "✅ Tasks":
            if st.session_state.role == "admin":
                tasks()
            else:
                st.warning("👤 Members can view tasks only")

if __name__ == "__main__":
    main()