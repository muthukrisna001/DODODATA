# 💻 IT & AI Hub 🤖

A comprehensive Django web application that serves as your one-stop destination for both historical IT/AI facts and the latest technology news. Features a beautiful vintage terminal-themed UI with dual-mode functionality.

## ✨ Features

### 🎯 **Dual-Mode Interface**
- **📚 Historical Facts Mode**: Curated IT/AI historical facts and computing milestones
- **📰 Latest News Mode**: Current technology and AI industry updates

### 🎨 **Beautiful UI**
- **Vintage terminal aesthetic** with modern glassmorphism effects
- **Responsive design** that works on all devices
- **Smooth animations** and loading states
- **Centered content layout** for optimal readability

### 📚 **Historical Facts (25+ Facts)**
- **Programming Languages**: Python, Java, JavaScript, C, Rust, Go, TypeScript
- **Computer Scientists**: Alan Turing, Ada Lovelace, Steve Jobs, Tim Berners-Lee
- **AI Technologies**: ChatGPT, Neural Networks, Machine Learning, Computer Vision
- **Software Companies**: Microsoft, Apple, Google, Meta, AWS
- **Computing Milestones**: First Bug, First Website, First Email, Computer Mouse

### 📰 **Latest Tech News (10+ Articles)**
- **OpenAI Updates**: GPT-4 Turbo, new model releases
- **Open Source AI**: DeepSeek, Meta Llama 3 developments
- **Programming Languages**: Python 3.12, JavaScript ES2024, Rust 1.75
- **Developer Tools**: GitHub Copilot, TypeScript 5.3 improvements
- **Industry Trends**: Latest developments from major tech companies

### 🔧 **Smart Features**
- **Unique content system**: No duplicate news articles until all are shown
- **Smart Wikipedia linking**: Automatic relevant links for historical facts
- **External article linking**: Direct links to original news sources
- **Session-based variety**: Different facts each time with no immediate repetition
- **Error handling**: Graceful fallbacks and user-friendly error messages

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- **Internet connection** for fetching images and external content

### 📥 Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/DODODATA.git

# Navigate to the project directory
cd DODODATA
```

### 🐍 Step 2: Set Up Python Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 📦 Step 3: Install Dependencies

```bash
# Install required packages
pip install django==5.2.6
pip install djangorestframework
pip install requests
pip install python-dotenv
```

**Or install from requirements.txt (if available):**
```bash
pip install -r requirements.txt
```

### ⚙️ Step 4: Database Setup

```bash
# Apply database migrations
python manage.py migrate
```

### 🏃‍♂️ Step 5: Run the Development Server

```bash
# Start the Django development server
python manage.py runserver
```

You should see output like:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 25, 2024 - 15:30:45
Django version 5.2.6, using settings 'extinct_facts_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 🌐 Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

**That's it! 🎉 The application should now be running successfully.**

## 🔧 Configuration

### No API Keys Required!
**The app works completely out of the box!**

- **Historical Facts**: Curated content, no external APIs needed
- **News Content**: Sample tech news, no API keys required
- **Images**: Free Wikimedia Commons integration
- **All features work immediately** without any setup or registration!

### Optional: Environment Variables
Create a `.env` file in the root directory if you want to customize settings:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📖 How to Use

### 🎮 **Interface Overview**
The application features two main modes accessible via toggle buttons:

### 📚 **Historical Facts Mode**
1. **Click "📚 Historical Facts"** to enter facts mode
2. **Click the button** to generate a random IT/AI historical fact
3. **Read the content** with detailed descriptions and context
4. **Click "🔗 Learn More"** to visit the relevant Wikipedia page
5. **Click again** for a different fact (no immediate repeats!)

### 📰 **Latest News Mode**
1. **Click "📰 Latest News"** to switch to news mode
2. **Click the button** to get the latest tech industry updates
3. **Read current developments** in AI, programming languages, and tech companies
4. **Click "🔗 Read Full Article"** to visit the original source
5. **Get unique articles** - no duplicates until you've seen all 10 news items!

### 💡 **Pro Tips**
- **Switch modes anytime** using the toggle buttons at the top
- **All content is curated** for IT professionals and tech enthusiasts
- **Links are contextual** - Wikipedia for facts, original sources for news
- **Responsive design** works great on mobile, tablet, and desktop

## 📁 Project Structure

```
DODODATA/
├── extinct_facts/                 # Main Django application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py                   # Main page view and API endpoints
│   ├── openai_service.py          # Core service with fact generation logic
│   ├── wikidata_service.py        # Wikidata API integration and fallback facts
│   ├── urls.py                    # URL routing for the app
│   ├── templates/
│   │   └── extinct_facts/
│   │       └── index.html         # Main frontend UI with dual-mode interface
│   └── migrations/                # Database migration files
├── extinct_facts_project/         # Django project configuration
│   ├── __init__.py
│   ├── settings.py                # Django settings and configuration
│   ├── urls.py                    # Main URL routing
│   └── wsgi.py                    # WSGI configuration for deployment
├── manage.py                      # Django management script
├── README.md                      # This file
├── .env                          # Environment variables (optional)
└── requirements.txt              # Python dependencies (if available)
```

## 🔌 API Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Main application page | HTML page with dual-mode interface |
| `POST` | `/api/get-extinct-fact/` | Get random IT/AI historical fact | JSON with title, description, and image |

### Example API Response:
```json
{
  "title": "🧠 C Programming Language",
  "description": "C was developed by Dennis Ritchie at Bell Labs between 1969 and 1973. It's considered the foundation of modern programming languages...",
  "image_suggestion": "C programming language vintage computer terminal"
}
```

## ⚙️ How It Works

### **Historical Facts Mode:**
1. **Curated Content**: 25+ hand-crafted facts about IT/AI history
2. **Smart Selection**: Session-based tracking prevents immediate repetition
3. **Wikipedia Integration**: Automatic linking to relevant Wikipedia articles
4. **Image Support**: Wikimedia Commons integration for historical images

### **Latest News Mode:**
1. **Curated News Pool**: 10+ current tech industry updates
2. **Unique Article System**: Tracks shown articles to prevent duplicates
3. **External Linking**: Direct links to original news sources
4. **Auto-Reset**: Refreshes pool when all articles have been shown

## 🛠️ Troubleshooting

### Common Issues and Solutions:

#### **🚫 Server Won't Start**
```bash
# Check if port 8000 is in use
netstat -an | findstr :8000

# Use a different port if needed
python manage.py runserver 8080
```

#### **❌ No Facts Showing**
- Check your internet connection for image loading
- Verify Django server is running without errors
- Check browser console for JavaScript errors

#### **🔧 Database Issues**
```bash
# Reset database if needed
python manage.py flush
python manage.py migrate
```

#### **📦 Dependency Issues**
```bash
# Reinstall dependencies
pip uninstall django djangorestframework requests python-dotenv
pip install django==5.2.6 djangorestframework requests python-dotenv
```

#### **🌐 Browser Issues**
- Clear browser cache and cookies
- Try a different browser
- Disable browser extensions that might interfere

### **Getting Help**
- Check the Django development server console for error messages
- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies are installed: `pip list`

## 🎯 Development Notes

- **Framework**: Django 5.2.6 with Django REST Framework
- **Frontend**: Vanilla JavaScript with modern CSS (no external frameworks)
- **Styling**: Custom CSS with glassmorphism effects and animations
- **APIs**: Free services only - no API keys required
- **Database**: SQLite (default Django database)
- **Deployment Ready**: WSGI configuration included for production deployment

## 🌟 Features for Developers

- **Clean Code Structure**: Well-organized Django app with separation of concerns
- **Responsive Design**: Mobile-first CSS with modern techniques
- **Error Handling**: Comprehensive error handling and user feedback
- **Extensible**: Easy to add new fact categories or news sources
- **No External Dependencies**: Works completely offline for core functionality
