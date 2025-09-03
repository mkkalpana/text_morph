
# 🚀 Text morph advanced summarisation using AI (INTERFACE, AUTHENTICATION AND READABILITY)


## 🔧 Technology Stack
- **Frontend**: Streamlit (Professional Dashboard)
- **Backend**: FastAPI (REST API with JWT)
- **Database**: MySQL (User & Analysis data)
- **File Processing**: PDF, DOCX, TXT support
- **Text Analysis**: NLTK + TextStat libraries

## ⚡ Quick Setup

### 1. **Database Setup**
```bash
# Login to MySQL
mysql -u root -p

# Run database setup to create database and tables
source database-schema.sql
```

### 2. **Backend Setup**
```bash
# Create backend directory structure
mkdir -p backend/app/{models,services,routers,utils}

# Copy all backend files to their locations
# Create empty __init__.py files in each folder

# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"

# Start FastAPI server
cd ..
python -m uvicorn backend.app.main:app --reload

uvicorn app.main:app --reload
```

### 3. **Frontend Setup** (New Terminal)
```bash
# Create frontend directory
mkdir frontend

# Copy frontend files
# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
cd frontend
pip install -r requirements.txt

# Start Streamlit app
streamlit run streamlit_app.py
```
streamlit run streamlit_app.py

## 🌐 Access Points
- **Frontend**: http://localhost:8501 (Dashboard)
- **Backend API**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs (Auto-generated)

## 🎯 Professional Features

### ✅ **File Upload & Processing**
- **Drag & Drop Interface** - Professional file upload
- **Multiple Formats** - TXT, PDF, DOCX support
- **File Validation** - Size and type checking
- **Text Extraction** - Smart content parsing

### ✅ **Advanced Authentication**
- **JWT Token System** - Secure session management
- **Password Validation** - Strong password requirements
- **Profile Management** - Update name, language, password
- **Database Updates** - All changes reflected in MySQL

### ✅ **Professional UI**
- **Clean Design** - No unnecessary popups
- **Intuitive Navigation** - Sidebar with clear sections
- **Visual Charts** - Plotly-powered analytics
- **Responsive Layout** - Works on all devices

### ✅ **Comprehensive Analysis**
- **Flesch Reading Ease** - 0-100 readability score
- **Grade Level Analysis** - Educational level required
- **SMOG Index** - Complexity measurement
- **Visual Classification** - Beginner/Intermediate/Advanced

## 📊 File Structure Details

### **Backend Files:**
- `backend-config.py` → `backend/app/config.py`
- `backend-database.py` → `backend/app/database.py`
- `backend-main.py` → `backend/app/main.py`
- `backend-models-user.py` → `backend/app/models/user.py`
- `backend-schemas.py` → `backend/app/schemas.py`
- `backend-services-auth.py` → `backend/app/services/auth.py`
- `backend-services-file.py` → `backend/app/services/file.py`
- `backend-utils-security.py` → `backend/app/utils/security.py`
- `backend-routers-auth.py` → `backend/app/routers/auth.py`
- `backend-routers-users.py` → `backend/app/routers/users.py`
- `backend-routers-analysis.py` → `backend/app/routers/analysis.py`

### **Frontend Files:**
- `frontend-streamlit-app.py` → `frontend/streamlit_app.py`

## 🔒 Security Features

- **bcrypt Password Hashing** - Industry standard
- **JWT Authentication** - Secure token system
- **Input Validation** - Pydantic schemas
- **File Upload Security** - Size and type validation
- **Database Protection** - SQLAlchemy ORM

## 🧪 Testing

### **Demo Account:**
- Email: `demo@example.com`
- Password: `DemoPass123!`

### **API Testing:**
```bash
# Test file upload
curl -X POST "http://localhost:8000/api/analysis/file" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample.txt"

# Test profile update
curl -X PUT "http://localhost:8000/api/users/profile" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "language_preference": "Hindi"}'
```

## 📈 Professional Enhancements

### **What's Different from Basic Version:**
1. **File Upload** - Drag & drop with PDF/DOCX support
2. **Professional UI** - Clean, no popups, better UX
3. **Database Updates** - All profile changes saved to MySQL
4. **Password Management** - Change password functionality
5. **Organized Code** - Proper separation of concerns
6. **Error Handling** - Comprehensive validation
7. **Security** - Enhanced JWT and file validation

## 🐛 Troubleshooting

**File Upload Issues:**
- Ensure file is under 10MB
- Supported formats: TXT, PDF, DOCX only

**Database Connection:**
- Check MySQL is running on port 3306
- Verify credentials in config.py

**Authentication Problems:**
- Clear browser cache/cookies
- Check token expiration (30 minutes)

