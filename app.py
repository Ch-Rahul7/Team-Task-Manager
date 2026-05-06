import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ── Config ─────────────────────────────────────────────────────────────────
# API_BASE must point to your BACKEND service, not the frontend.
# Set API_BASE env var in Railway frontend service → Variables tab.
API_BASE = os.getenv("API_BASE", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Team Task Manager", layout="wide")

# ── Session state defaults (prevents KeyError on refresh) ──────────────────
for key, default in [
    ("logged_in", False),
    ("role", "member"),
    ("username", ""),
    ("email", ""),
    ("token", ""),
    ("show_signup", False),
    ("email_signin", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helpers ─────────────────────────────────────────────────────────────────
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_get(path):
    try:
        r = requests.get(f"{API_BASE}{path}", headers=auth_headers(), timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot reach backend at {API_BASE}")
        return None

def api_post(path, data, use_auth=True):
    try:
        headers = auth_headers() if use_auth else {}
        r = requests.post(f"{API_BASE}{path}", json=data, headers=headers, timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot reach backend at {API_BASE}")
        return None


# ── Login / Signup ───────────────────────────────────────────────────────────
def login():
    st.markdown("""
    <style>
    .form-title { text-align:center; color:#2c3e50; font-size:2.2rem; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h2 class="form-title">🏢 Team Task Manager</h2>', unsafe_allow_html=True)

        # ── SIGN IN ──────────────────────────────────────────────────────────
        if not st.session_state.show_signup:
            st.markdown('<p style="text-align:center;color:#64748b;">Welcome back! Please sign in to continue.</p>', unsafe_allow_html=True)

            email    = st.text_input("Email",    placeholder="admin@example.com",
                                     value=st.session_state.email_signin, key="email_signin_input")
            password = st.text_input("Password", placeholder="•••••••",
                                     type="password", key="password_signin")

            if st.button("🔐 Sign In", key="btn_signin", type="primary", use_container_width=True):
                if not email or not password:
                    st.error("❌ Please enter email and password.")
                else:
                    resp = api_post("/auth/login", {"email": email, "password": password}, use_auth=False)
                    if resp is not None:
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.logged_in  = True
                            st.session_state.token      = data["access_token"]
                            st.session_state.username   = data["user"]["username"]
                            st.session_state.role       = data["user"]["role"]
                            st.session_state.email      = data["user"]["email"]
                            st.session_state.email_signin = email
                            st.success(f"✅ Welcome {st.session_state.username}!")
                            st.rerun()
                        else:
                            try:
                                detail = resp.json().get("detail", resp.text)
                            except Exception:
                                detail = resp.text
                            st.error(f"❌ {detail}")

            st.markdown("---")
            if st.button("➕ Don't have an account? Create Account",
                         key="toggle_to_signup", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()

            with st.expander("🔑 Quick Demo Accounts"):
                st.markdown("""
**Admin:** `admin@example.com` / `admin123`  
**Member:** `member@example.com` / `member123`
""")

        # ── SIGN UP ──────────────────────────────────────────────────────────
        else:
            st.markdown('<p style="text-align:center;color:#64748b;">Create your Team Task Manager account</p>', unsafe_allow_html=True)

            name  = st.text_input("Full Name", placeholder="John Doe",        key="su_name")
            col_a, col_b = st.columns(2)
            with col_a:
                email  = st.text_input("Email",  placeholder="john@company.com", key="su_email")
            with col_b:
                mobile = st.text_input("Mobile", placeholder="+91 9999999999",   key="su_mobile")

            col_c, col_d = st.columns(2)
            with col_c:
                job_id   = st.text_input("Job ID", placeholder="EMP001",         key="su_jobid")
            with col_d:
                role_sel = st.selectbox("Role", ["member", "admin"],              key="su_role")

            password = st.text_input("Password",         placeholder="••••••••",
                                     type="password", key="su_pw")
            confirm  = st.text_input("Confirm Password", placeholder="••••••••",
                                     type="password", key="su_cpw")

            if st.button("✅ Create Account", key="btn_signup",
                         type="primary", use_container_width=True):
                if not all([name, email, password, confirm]):
                    st.error("❌ Please fill all required fields.")
                elif password != confirm:
                    st.error("❌ Passwords do not match!")
                else:
                    # ✅ Actually call the API — this was the bug before
                    resp = api_post("/auth/register", {
                        "username": name,
                        "email":    email,
                        "password": password,
                        "role":     role_sel,
                    }, use_auth=False)
                    if resp is not None:
                        if resp.status_code == 200:
                            st.success("✅ Account created! Please sign in.")
                            st.balloons()
                            st.session_state.show_signup  = False
                            st.session_state.email_signin = email
                            st.rerun()
                        else:
                            try:
                                detail = resp.json().get("detail", resp.text)
                            except Exception:
                                detail = resp.text
                            st.error(f"❌ {detail}")

            st.markdown("---")
            if st.button("👤 Already have an account? Sign In",
                         key="toggle_to_signin", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()


# ── Dashboard ────────────────────────────────────────────────────────────────
def dashboard():
    st.header("📊 Dashboard")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("📈 Tasks")
        resp = api_get("/tasks")
        if resp and resp.status_code == 200:
            tasks = resp.json()
            df = pd.DataFrame(tasks) if tasks else pd.DataFrame()

            c1, c2, c3, c4 = st.columns(4)
            total     = len(df)
            pending   = len(df[df["status"] == "pending"])    if not df.empty else 0
            progress  = len(df[df["status"] == "in-progress"])if not df.empty else 0
            completed = len(df[df["status"] == "completed"])  if not df.empty else 0

            c1.metric("Total",       total)
            c2.metric("Pending",     pending)
            c3.metric("In Progress", progress)
            c4.metric("Completed",   completed)

            if total > 0:
                fig = px.pie(
                    values=[pending, progress, completed],
                    names=["Pending", "In Progress", "Completed"],
                    title="Task Status"
                )
                st.plotly_chart(fig, use_container_width=True)
                cols = [c for c in ["title", "status", "due_date"] if c in df.columns]
                st.subheader("Recent Tasks")
                st.dataframe(df[cols].tail(5), use_container_width=True)
            else:
                st.info("📭 No tasks yet.")
        elif resp:
            st.error(f"Failed to load tasks ({resp.status_code}): {resp.text}")

    with right_col:
        st.subheader("📁 Projects")
        resp = api_get("/projects")
        if resp and resp.status_code == 200:
            projects = resp.json()
            df_proj = pd.DataFrame(projects) if projects else pd.DataFrame()
            st.metric("Total Projects", len(df_proj))
            if not df_proj.empty:
                cols = [c for c in ["id", "name", "description"] if c in df_proj.columns]
                st.dataframe(df_proj[cols], use_container_width=True, height=400)
            else:
                st.info("📭 No projects yet.")
        elif resp:
            st.error(f"Failed to load projects ({resp.status_code}): {resp.text}")


# ── Projects ──────────────────────────────────────────────────────────────────
def projects():
    st.header("📁 Projects")

    with st.form("create_project"):
        name = st.text_input("Project Name")
        desc = st.text_area("Description")
        submitted = st.form_submit_button("➕ Create Project")

    if submitted:
        if not name:
            st.error("❌ Project name is required.")
        else:
            resp = api_post("/projects", {"name": name, "description": desc})
            if resp is not None:
                if resp.status_code in (200, 201):
                    st.success("✅ Project created!")
                    st.rerun()
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"❌ {detail}")

    st.divider()
    st.subheader("All Projects")
    resp = api_get("/projects")
    if resp and resp.status_code == 200:
        data = resp.json()
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("📭 No projects yet.")
    elif resp:
        st.error(f"Failed ({resp.status_code}): {resp.text}")


# ── Tasks ─────────────────────────────────────────────────────────────────────
def tasks():
    st.header("✅ Tasks")

    with st.form("create_task"):
        title  = st.text_input("Task Title")
        desc   = st.text_area("Description")
        status = st.selectbox("Status", ["pending", "in-progress", "completed"])
        due    = st.date_input("Due Date", value=date.today())
        col1, col2 = st.columns(2)
        with col1:
            project_id  = st.number_input("Project ID (0 = none)",  min_value=0, value=0, step=1)
        with col2:
            assignee_id = st.number_input("Assignee ID (0 = none)", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("➕ Add Task")

    if submitted:
        if not title:
            st.error("❌ Task title is required.")
        else:
            payload = {
                "title":       title,
                "description": desc,
                "status":      status,
                "due_date":    due.isoformat(),
            }
            if project_id  > 0: payload["project_id"]  = int(project_id)
            if assignee_id > 0: payload["assignee_id"] = int(assignee_id)

            resp = api_post("/tasks", payload)
            if resp is not None:
                if resp.status_code in (200, 201):
                    st.success("✅ Task created!")
                    st.rerun()
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"❌ {detail}")

    st.divider()
    st.subheader("All Tasks")
    resp = api_get("/tasks")
    if resp and resp.status_code == 200:
        data = resp.json()
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("📭 No tasks yet.")
    elif resp:
        st.error(f"Failed ({resp.status_code}): {resp.text}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    st.sidebar.title("🏢 Team Task Manager")

    if not st.session_state.logged_in:
        login()
        return

    st.sidebar.success(f"👋 {st.session_state.username} ({st.session_state.role})")
    st.sidebar.markdown("---")

    page = st.sidebar.selectbox("Navigate", ["📊 Dashboard", "📁 Projects", "✅ Tasks"])

    if st.sidebar.button("🔓 Logout"):
        for key in ["logged_in", "token", "username", "role", "email"]:
            st.session_state[key] = False if key == "logged_in" else ""
        st.rerun()

    if page == "📊 Dashboard":
        dashboard()
    elif page == "📁 Projects":
        if st.session_state.role == "admin":
            projects()
        else:
            st.warning("👤 Only admins can manage projects.")
    elif page == "✅ Tasks":
        if st.session_state.role == "admin":
            tasks()
        else:
            # Members can view their tasks
            st.header("✅ My Tasks")
            resp = api_get("/tasks")
            if resp and resp.status_code == 200:
                data = resp.json()
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.info("📭 No tasks assigned yet.")
            elif resp:
                st.error(f"Failed ({resp.status_code}): {resp.text}")


if __name__ == "__main__":
    main()
