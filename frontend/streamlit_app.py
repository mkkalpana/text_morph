# Professional AI Text Analysis System
import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

# Configure page
st.set_page_config(
    page_title="AI Text Summarization",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Session state initialization
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None

# Utility Functions
def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength on frontend"""
    import re
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if len(password) > 128:
        return False, "Password must be no more than 128 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter (A-Z)"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter (a-z)"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit (0-9)"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False, "Password must contain at least one special character (!@#$%^&*() etc.)"
    return True, "Password is strong"

def show_password_feedback(password: str):
    """Show password strength feedback"""
    if not password:
        return

    is_strong, message = validate_password_strength(password)

    if is_strong:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

# API Functions
class APIClient:
    
    @staticmethod
    def make_request(method: str, endpoint: str, data=None, files=None, token=None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        try:
            url = f"{API_BASE_URL}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                if files:
                    response = requests.post(url, files=files, headers=headers)
                else:
                    response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            
            return response.json() if response.status_code in [200, 201] else {
                "success": False, 
                "error": response.json().get("error", "Request failed")
            }
        
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    @staticmethod
    def register(name: str, email: str, password: str, language: str = "English"):
        return APIClient.make_request("POST", "/auth/register", {
            "name": name, "email": email, "password": password, "language_preference": language
        })
    
    @staticmethod
    def login(email: str, password: str):
        return APIClient.make_request("POST", "/auth/login", {
            "email": email, "password": password
        })
    
    @staticmethod
    def update_profile(name: str, language: str, token: str):
        return APIClient.make_request("PUT", "/users/profile", {
            "name": name, "language_preference": language
        }, token=token)
    
    @staticmethod
    def change_password(current_password: str, new_password: str, token: str):
        return APIClient.make_request("POST", "/auth/change-password", {
            "current_password": current_password, "new_password": new_password
        }, token=token)
    
    @staticmethod
    def analyze_file(file_bytes: bytes, filename: str, token: str):
        files = {"file": (filename, file_bytes)}
        return APIClient.make_request("POST", "/analysis/file", files=files, token=token)
    
    @staticmethod
    def analyze_text(text: str, token: str):
        return APIClient.make_request("POST", "/analysis/text", {"text": text}, token=token)

# CSS Styling
def load_css():
    st.markdown("""
    <style>
    body {
        background-color: white;  /* White background */
    }
    .main-header {
        background: #007bff;  /* Blue background */
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-size: 28px;  /* Increased font size */
    }
    .centered-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;  /* Light border */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    button {
        background-color: #007bff;  /* Blue button color */
        color: white;  /* White text */
        border: none;  /* No border */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding */
        cursor: pointer;  /* Pointer cursor on hover */
    }
    button:hover {
        background-color: #0056b3;  /* Darker blue on hover */
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
    }
    .upload-area {
        border: 2px dashed #007bff;  /* Blue border */
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f0f8ff;  /* Light blue background */
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    init_session_state()
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 AI Text Summarization</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab-based navigation
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            show_login_page()
        with tab2:
            show_register_page()
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👤 Profile", "🚪 Logout"])
        
        with tab1:
            show_dashboard_page()
        with tab2:
            show_profile_page()
        with tab3:
            show_logout_page()

def show_login_page():
    st.markdown("## 🔑 Login")
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password")
            
            if st.form_submit_button("🔑 Login", type="primary", use_container_width=True):
                if email and password:
                    result = APIClient.login(email, password)
                    
                    if result.get("success"):
                        st.session_state.authenticated = True
                        st.session_state.user_data = result["data"]["user"]
                        st.session_state.access_token = result["data"]["access_token"]
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {result.get('error')}")
                else:
                    st.error("⚠️ Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_register_page():
    st.markdown("## 📝 Create Account")

    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        name = st.text_input("👤 Full Name", placeholder="")
        email = st.text_input("📧 Email Address", placeholder="")
        password = st.text_input(
            "🔒 Password",
            type="password",
            help="Must be 8-128 chars with uppercase, lowercase, digit, and special character"
        )
        show_password_feedback(password)
        language = st.selectbox("🌍 Preferred Language", ["English", "Hindi", "Spanish", "French", "German"])

        if st.button("🚀 Create Account", type="primary", use_container_width=True):
            if not name or not email or not password:
                st.error("⚠️ Please fill in all fields")
            else:
                is_strong, message = validate_password_strength(password)
                if not is_strong:
                    st.error(f"❌ {message}")
                else:
                    result = APIClient.register(name, email, password, language)

                    if result.get("success"):
                        st.session_state.authenticated = True
                        st.session_state.user_data = result["data"]["user"]
                        st.session_state.access_token = result["data"]["access_token"]
                        st.success("✅ Account created successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Registration failed: {result.get('error')}")

        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard_page():
    st.markdown("## 📊 Text Summarization Dashboard")
    
    # Analysis methods
    tab1, tab2 = st.tabs(["📄 File Upload", "📝 Text Input"])
    
    with tab1:
        st.markdown("### Upload Document for Analysis")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx'],
            help="Supported formats: TXT, PDF, DOCX (Max 10MB)"
        )
        
        if uploaded_file:
            if st.button("🔍 Analyze File", type="primary", use_container_width=True):
                with st.spinner("Processing file..."):
                    file_bytes = uploaded_file.read()
                    result = APIClient.analyze_file(
                        file_bytes, uploaded_file.name, st.session_state.access_token
                    )
                    
                    if result.get("success"):
                        display_analysis_results(result["analysis"], uploaded_file.name)
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error')}")
    
    with tab2:
        st.markdown("### Enter Text for Analysis")
        
        user_text = st.text_area(
            "Text to analyze:",
            height=200,
            placeholder="Enter or paste your text here..."
        )
        
        if user_text and len(user_text.strip()) >= 10:
            if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
                with st.spinner("Analyzing text..."):
                    result = APIClient.analyze_text(user_text, st.session_state.access_token)
                    
                    if result.get("success"):
                        display_analysis_results(result["analysis"], "Text Input")
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error')}")
        elif user_text:
            st.warning("⚠️ Text must be at least 10 characters long")

def show_profile_page():
    st.markdown("## 👤 Profile Management")
    
    user_data = st.session_state.user_data
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Profile Update
        st.markdown("### ✏️ Update Profile Information")

        new_name = st.text_input("Full Name", value=user_data.get("name", ""))
        languages = ["English", "Hindi", "Spanish", "French", "German"]
        current_lang = user_data.get("language_preference", "English")
        lang_index = languages.index(current_lang) if current_lang in languages else 0
        new_language = st.selectbox("Preferred Language", languages, index=lang_index)

        if st.button("💾 Update Profile", type="primary", use_container_width=True):
            result = APIClient.update_profile(
                new_name, new_language, st.session_state.access_token
            )

            if result.get("success"):
                st.session_state.user_data = result["data"]
                st.success("✅ Profile updated successfully!")
                st.rerun()
            else:
                st.error(f"❌ Update failed: {result.get('error')}")

        # Password Change
        st.markdown("### 🔐 Change Password")

        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input(
            "New Password",
            type="password",
            help="Must be 8-128 chars with uppercase, lowercase, digit, and special character"
        )
        show_password_feedback(new_password)
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("🔄 Change Password", type="secondary", use_container_width=True):
            if not current_password or not new_password or not confirm_password:
                st.error("⚠️ Please fill in all password fields")
            elif new_password != confirm_password:
                st.error("❌ New passwords do not match")
            else:
                is_strong, message = validate_password_strength(new_password)
                if not is_strong:
                    st.error(f"❌ {message}")
                else:
                    result = APIClient.change_password(
                        current_password, new_password, st.session_state.access_token
                    )

                    if result.get("success"):
                        st.success("✅ Password changed successfully!")
                    else:
                        st.error(f"❌ Password change failed: {result.get('error')}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_logout_page():
    st.markdown("## 🚪 Logout")
    
    with st.container():
        st.markdown('<div class="centered-container">', unsafe_allow_html=True)
        
        st.warning("Are you sure you want to logout?")
        
        if st.button("✅ Confirm Logout", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.access_token = None
            st.success("Logged out successfully!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_analysis_results(analysis: Dict[str, Any], source_name: str):
    st.markdown("### 📊 Analysis Results")
    
    # Main metrics - Focus on Flesch-Kincaid, Gunning Fog, and SMOG Index
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎓 Flesch-Kincaid", f"{analysis['flesch_kincaid_grade']}")
    with col2:
        st.metric("🧠 Gunning Fog", f"{analysis['gunning_fog_index']}")
    with col3:
        st.metric("📚 SMOG Index", f"{analysis['smog_index']}")
    
    # Complexity visualization
    complexity_level = analysis['complexity_level']
    
    # Create complexity chart
    complexity_data = pd.DataFrame({
        'Level': ['Beginner', 'Intermediate', 'Advanced'],
        'Score': [
            100 if complexity_level == 'Beginner' else 30,
            100 if complexity_level == 'Intermediate' else 30,
            100 if complexity_level == 'Advanced' else 30
        ],
        'Color': ["#2a5b36", "#a48a3b", "#94353e"]
    })
    
    fig = go.Figure(data=[
        go.Bar(
            x=complexity_data['Level'],
            y=complexity_data['Score'],
            marker_color=complexity_data['Color'],
            text=complexity_data['Level'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Text Complexity Level",
        xaxis_title="Complexity Level",
        yaxis_title="Score",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed stats
    with st.expander("📈 Detailed Statistics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Word Count**: {analysis['word_count']}")
            st.write(f"**Sentence Count**: {analysis['sentence_count']}")
            st.write(f"**Average Sentence Length**: {analysis['avg_sentence_length']}")
            st.write(f"**Gunning Fog Index**: {analysis['gunning_fog_index']}")
        
        with col2:
            st.write(f"**Complexity Level**: {complexity_level}")
            st.write(f"**Grade Level**: {analysis['grade_level_interpretation']}")
            st.write(f"**SMOG Index**: {analysis['smog_index']}")
    
    # Final message
    st.success(f"✅ Analysis Complete: This text is classified as **{complexity_level}** complexity level.")

if __name__ == "__main__":
    main()
