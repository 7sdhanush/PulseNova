import streamlit as st
import sqlite3
import hashlib
import re


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)


def is_valid_username(username):
    return username.replace("_", "").isalnum()


def authenticate_user(conn, cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Login"

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if st.session_state.logged_in:
        return

    st.markdown("""
    <div style="
    max-width:900px;
    margin:40px auto 25px auto;
    background:linear-gradient(135deg,#14B8A6,#3B82F6);
    padding:45px;
    border-radius:28px;
    text-align:center;
    color:white;
    box-shadow:0px 12px 35px rgba(0,0,0,0.18);
    ">

    <h1 style="font-size:48px;margin-bottom:8px;">❤️ PulseNova</h1>

    <h2 style="font-size:48px;margin-bottom:18px;font-weight:800;">
    🏥 Smart Healthcare Assistant
    </h2>

    <p style="font-size:20px;font-weight:500;">
    AI-Powered Personal Healthcare Companion
    </p>

    </div>
    """, unsafe_allow_html=True)

    left, col1, col2, right = st.columns([1, 2, 2, 1])

    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.auth_mode = "Login"

    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.auth_mode = "Signup"

    st.markdown("---")

    if st.session_state.auth_mode == "Signup":

        st.subheader("📝 Create Your Account")

        with st.form("signup_form"):

            name = st.text_input("Full Name")
            username = st.text_input("Username")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            signup_btn = st.form_submit_button("Create Account")

            if signup_btn:

                if not name or not username or not email or not password or not confirm_password:
                    st.warning("⚠️ Please fill all required fields.")

                elif len(name) < 3:
                    st.warning("⚠️ Name must contain at least 3 characters.")

                elif len(username) < 4:
                    st.warning("⚠️ Username must contain at least 4 characters.")

                elif not is_valid_username(username):
                    st.warning("⚠️ Username can contain only letters, numbers, and underscore.")

                elif not is_valid_email(email):
                    st.warning("⚠️ Please enter a valid email address.")

                elif len(password) < 6:
                    st.warning("⚠️ Password must contain at least 6 characters.")

                elif password != confirm_password:
                    st.warning("⚠️ Password and Confirm Password do not match.")

                else:
                    try:
                        hashed_password = hash_password(password)

                        cursor.execute(
                            """
                            INSERT INTO users
                            (name, username, email, password)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                name.strip(),
                                username.strip(),
                                email.strip(),
                                hashed_password
                            )
                        )

                        conn.commit()

                        st.success("✅ Account created successfully. Please login now.")

                        st.session_state.auth_mode = "Login"

                    except sqlite3.IntegrityError:
                        st.error("❌ Username or email already exists. Please use another one.")

    else:

        st.subheader("🔐 Login to Your Account")

        with st.form("login_form"):

            login_id = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")

            login_btn = st.form_submit_button("Login")

            if login_btn:

                if not login_id or not password:
                    st.warning("⚠️ Please enter username/email and password.")

                else:
                    hashed_password = hash_password(password)

                    cursor.execute(
                        """
                        SELECT name
                        FROM users
                        WHERE (username = ? OR email = ?)
                        AND password = ?
                        """,
                        (
                            login_id.strip(),
                            login_id.strip(),
                            hashed_password
                        )
                    )

                    user = cursor.fetchone()

                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user[0]

                        st.success("✅ Login successful.")

                        st.rerun()

                    else:
                        st.error("❌ Invalid username/email or password.")

    st.stop()


def logout_button():

    st.sidebar.info(
        f"👤 Welcome, {st.session_state.user_name}"
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.auth_mode = "Login"

        st.rerun()