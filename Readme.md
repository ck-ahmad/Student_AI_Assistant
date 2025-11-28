# 🎓 Student AI Assistant

<img width="952" height="446" alt="image" src="https://github.com/user-attachments/assets/a362f336-5d11-4bbb-9c91-c7191599be25" />

> **Your Complete Academic Companion Powered by Google Gemini 2.5 Pro**

A comprehensive AI-powered web application designed specifically for students, featuring smart notes, file management, health tracking, quiz generation, and intelligent search capabilities.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Pro-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![YouTube Video](https://img.shields.io/badge/Demo-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/G5eEwg4ChUo?si=MJOkSHZ7AfssjGlC)


---

## 👥 Development Team

### **Safia Liaqat & Ume Habiba**  - Frontend Developer (Under process as Safia will enhance fronet end by React)
- 🎨 **Responsible for**: Complete Frontend Architecture & UI/UX Design
- ⚛️ **Tech Stack**: React.js, Modern CSS, Responsive Design
- 💡 **Key Contributions**:
  - Designed beautiful, intuitive user interfaces
  - Built interactive React components for all features
  - Implemented responsive design for mobile/desktop
  - Created smooth animations and user interactions
  - Developed real-time AI response displays
- 💼 GitHub: [@Um e Habiba](https://github.com/UmeHabiba2416)
- 🔗 LinkedIn: [Um e Habiba](https://www.linkedin.com/in/um-e-habiba-031b6a301/)
- 💼 GitHub: [@safialiaqat](https://github.com/Safia-Liaqat)
- 🔗 LinkedIn: [Safia Liaqat](https://www.linkedin.com/in/safia-liaqat-7a8082200)

### **Ahmad** - Backend Developer (Python/Flask)
- ⚙️ **Responsible for**: Complete Backend Architecture & AI Integration
- 🐍 **Tech Stack**: Python, Flask, Google Gemini AI, RESTful APIs
- 💡 **Key Contributions**:
  - Built robust Flask REST API backend
  - Integrated Google Gemini 2.5 Pro AI model
  - Developed all AI-powered features (Notes, Quiz, Health, Search)
  - Implemented file upload and cloud storage system
  - Created database architecture and data management
  - Set up authentication and security features
- 📧 Email: ahmadleo498@gmail.com
- 💼 GitHub: [@ckahmad](https://github.com/ck-ahmad)
- 🔗 LinkedIn: [Ahmad](https://linkedin.com/in/ahmad0763)

---

## ✨ Features

### 📝 Smart Notes Manager
- **AI-Enhanced Notes**: Automatically improve grammar, formatting, and clarity
- **Smart Summarization**: Generate concise summaries of all your notes
- **Interactive Q&A**: Ask questions about your notes and get AI-powered answers
- **Flashcard Generation**: Auto-create study flashcards from your content
- **Voice Notes**: Record and transcribe voice notes (optional)
- **Search & Filter**: Quickly find specific notes by keywords
- **Real-time Updates**: Instant UI feedback with React

### 📚 Drive Manager
- **File Upload**: Upload files to cloud storage (Cloudinary) or local storage
- **External Links**: Add Google Drive, Dropbox, or any web links
- **Smart Organization**: Organize by semester, degree, and subject
- **Search Functionality**: Find files across all your materials
- **AI Study Plans**: Generate personalized study schedules
- **Quick Access**: Predefined links to common course materials
- **Drag & Drop**: Modern file upload interface

### 🏥 Health Tracker
- **Symptom Analysis**: Get AI-powered health information (educational only)
- **Medical Information**: Search for reliable health resources
- **Wellness Tips**: Get tips for nutrition, exercise, mental health, and more
- **First Aid Guides**: Quick access to emergency procedures
- **Medication Info**: Learn about common medications
- **Mental Health Support**: Resources and coping strategies
- **Interactive Forms**: Clean, user-friendly health input

### 🎯 Quiz Generator
- **Smart Quiz Generation**: Create quizzes from your notes or any topic
- **Multiple Question Types**: MCQ, True/False, and Short Answer questions
- **Difficulty Levels**: Easy, Medium, and Hard options
- **Instant AI Feedback**: Get personalized explanations for each answer
- **Performance Tracking**: View your quiz history and progress
- **Study Recommendations**: Get AI suggestions based on your performance
- **Interactive Quiz UI**: Smooth, engaging quiz-taking experience

### 🔍 Smart Search Engine
- **AI Search Suggestions**: Get optimized search queries
- **Multi-Engine Support**: Google, Bing, Scholar, YouTube
- **Local File Search**: Find files on your computer
- **To-Do List Manager**: Organize tasks with AI prioritization
- **Pomodoro Timer**: Built-in study timer
- **Study Music Recommendations**: AI-curated focus playlists
- **Real-time Search**: Fast, responsive search interface

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              Developed by: Safia Liaqat                  │
├─────────────────────────────────────────────────────────┤
│  • React Components      • State Management             │
│  • Responsive UI         • API Integration              │
│  • Modern CSS            • Real-time Updates            │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ REST API Calls
                     │
┌────────────────────▼────────────────────────────────────┐
│                Backend (Flask + Python)                  │
│                Developed by: Ahmad                       │
├─────────────────────────────────────────────────────────┤
│  • Flask REST API        • AI Integration               │
│  • Gemini 2.5 pro        • Data Processing              │
│  • File Management       • Authentication               │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    ┌──────────┐          ┌──────────┐
    │ Gemini   │          │Cloudinary│
    │ 2.5 pro  │          │  Storage │
    │   API    │          │   API    │
    └──────────┘          └──────────┘
```

---

## 🛠️ Tech Stack

### Frontend (Safia Liaqat)
- **Framework**: React.js 18+
- **Styling**: Modern CSS3, Flexbox, Grid
- **State Management**: React Hooks (useState, useEffect)
- **HTTP Client**: Fetch API / Axios
- **UI Features**: 
  - Responsive Design
  - Smooth Animations
  - Loading States
  - Error Handling
  - Real-time Updates

### Backend (Ahmad)
- **Framework**: Flask 3.0+
- **Language**: Python 3.8+
- **AI Model**: Google Gemini 2.5 pro
- **Translation**: Deep Translator
- **Storage**: Cloudinary (cloud) + Local filesystem
- **API Design**: RESTful architecture
- **Authentication**: Flask sessions
- **Logging**: Comprehensive error tracking

### AI & NLP
- **google-generativeai**: Gemini 2.5 pro integration
- **deep-translator**: Multi-language translation
- **speech-recognition**: Voice input support

### Cloud Services
- **Cloudinary**: Cloud file storage
- **Google AI**: Gemini API

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- pip (Python package manager)
- Git
- Google account (for Gemini API key)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ck-ahmad/student-ai-assistant.git
cd student-ai-assistant
```

### Step 2: Backend Setup (Ahmad's Part)

#### Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Frontend Setup (Safia's Part)

```bash
# Navigate to frontend directory (if separate)
cd frontend

# Install React dependencies
npm install

# Or if using single-page setup
# Frontend is already integrated in templates/
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Cloudinary (for cloud file storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

### Step 5: Run the Application

#### Start Backend Server (Ahmad's Part)
```bash
# Make sure virtual environment is activated & can work without it
python app.py
```

Backend will run on: **http://localhost:5000**

#### Start Frontend (Safia's Part)
```bash
# If using separate React dev server
npm start

# Or access directly through Flask
# Frontend is served through Flask templates
```

The application will be available at: **http://localhost:5000**

---

## 🔑 Configuration

### Getting API Keys

#### 1. Google Gemini API Key (Required - 100% Free)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add to `.env`

**Free Tier Limits:**
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ 1 million tokens per minute
- ✅ No credit card required!

#### 2. Cloudinary (Optional - Free Tier)

1. Sign up: https://cloudinary.com/users/register/free
2. Go to Dashboard
3. Copy Cloud Name, API Key, and API Secret
4. Add to `.env`

**Free Tier Includes:**
- ✅ 25 GB storage
- ✅ 25 GB bandwidth/month
- ✅ No credit card required

**Note:** If you skip Cloudinary, the app will use local storage automatically.

---

## 📖 Usage

### Basic Workflow

#### 1. Create and Manage Notes

```bash
1. Navigate to /notes
2. Enter a topic name
3. Write your note
4. Check "Enhance with AI" for automatic improvements
5. Click "Add Note"
```

**Frontend (React)**: Beautiful form with real-time validation  
**Backend (Flask)**: AI processing with Gemini 2.5 Pro

#### 2. Upload Study Materials

```bash
1. Navigate to /drive
2. Choose "Upload File" or "Add Link"
3. Select semester, degree, and subject
4. Upload or paste link
5. Add optional description
```

**Frontend (React)**: Drag-and-drop file upload interface  
**Backend (Flask)**: File processing and cloud storage integration

#### 3. Generate and Take Quizzes

```bash
1. Navigate to /quiz
2. Enter topic name
3. Choose question count and difficulty
4. Generate quiz
5. Take quiz and get instant feedback
```

**Frontend (React)**: Interactive quiz UI with smooth transitions  
**Backend (Flask)**: AI quiz generation and evaluation

---

## 📁 Project Structure

```
student-ai-assistant/
│
├── Backend (Ahmad's Work)/
│   ├── app.py                      # Main Flask application
│   ├── notes_ai.py                 # Notes AI with Gemini 1.5 Flash
│   ├── drive_manager_ai.py         # File management with AI
│   ├── health_tracker_ai.py        # Health information with AI
│   ├── quiz_generator_ai.py        # Quiz generation with AI
│   ├── search_engine_ai.py         # Smart search with AI
│   └── requirements.txt            # Python dependencies
│
├── Frontend (Safia's Work)/
│   ├── templates/                  # HTML templates with React
│   │   ├── index.html             # Landing page
│   │   ├── notes.html             # Notes interface
│   │   ├── drive.html             # Drive manager
│   │   ├── health.html            # Health tracker
│   │   ├── quiz.html              # Quiz generator
│   │   └── search.html            # Search engine
│   │
│   ├── static/                     # Frontend assets
│   │   ├── css/                   # Stylesheets
│   │   ├── js/                    # React components
│   │   └── images/                # Images and icons
│   │
│   └── components/                 # React components (if separate)
│
├── Data Storage/
│   ├── uploads/                    # Temporary file uploads
│   ├── drive_files/               # Local file storage
│   ├── notes/                     # Notes text files
│   └── *.json                     # Database files
│
├── Configuration/
│   ├── .env                       # Environment variables
│   ├── .env.example              # Environment template
│   ├── .gitignore                # Git ignore file
│   └── requirements.txt          # Python dependencies
│
└── Documentation/
    ├── README.md                 # This file
    └── LICENSE                   # MIT License
```

---

## 🔌 API Documentation (Backend - Ahmad)

### Base URL
```
http://localhost:5000/api
```

### Notes API

#### Create Note
```http
POST /api/notes/create
Content-Type: application/json

{
    "topic": "Python Programming",
    "note": "Functions are reusable blocks of code",
    "use_ai": true
}

Response:
{
    "success": true,
    "message": "Note added successfully! (AI Enhanced)",
    "enhanced_note": "Improved note text..."
}
```

#### View Notes
```http
POST /api/notes/view
Content-Type: application/json

{
    "topic": "Python Programming"
}

Response:
{
    "success": true,
    "notes": [
        {"id": 1, "text": "Note content..."},
        {"id": 2, "text": "Another note..."}
    ]
}
```

#### Summarize Notes
```http
POST /api/notes/summarize
Content-Type: application/json

{
    "topic": "Python Programming"
}

Response:
{
    "success": true,
    "summary": "AI-generated summary..."
}
```

### Quiz API

#### Generate Quiz
```http
POST /api/quiz/generate-from-topic
Content-Type: application/json

{
    "topic": "Machine Learning",
    "num_questions": 10,
    "difficulty": "medium",
    "quiz_type": "mixed"
}

Response:
{
    "success": true,
    "questions": [...]
}
```

#### Evaluate Quiz
```http
POST /api/quiz/evaluate
Content-Type: application/json

{
    "topic": "Machine Learning",
    "questions": [...],
    "answers": [...]
}

Response:
{
    "success": true,
    "score": 8,
    "total": 10,
    "percentage": 80.0,
    "results": [...],
    "overall_feedback": "Great job! ..."
}
```

---

## ⚛️ Frontend Components (React - Safia)

### Component Structure

```javascript
// Example: Notes Component
import React, { useState, useEffect } from 'react';

const NotesManager = () => {
    const [topic, setTopic] = useState('');
    const [note, setNote] = useState('');
    const [useAI, setUseAI] = useState(true);
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(false);

    const createNote = async () => {
        setLoading(true);
        const response = await fetch('/api/notes/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic, note, use_ai: useAI})
        });
        const data = await response.json();
        setLoading(false);
        // Update UI with response
    };

    return (
        // Beautiful React JSX UI
    );
};
```

### Key Frontend Features

- **Responsive Design**: Works on all devices
- **Real-time Validation**: Instant form feedback
- **Loading States**: Smooth user experience
- **Error Handling**: User-friendly error messages
- **Animations**: Smooth transitions and effects
- **Accessibility**: ARIA labels and keyboard navigation

---

## 🐍 Backend Modules (Python - Ahmad)

### Module Architecture

```python
# Example: Notes AI Module
class NotesAI:
    def __init__(self, gemini_api_key):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def create_note(self, topic, note_text, use_ai=False):
        if use_ai:
            note_text = self.enhance_note_with_ai(topic, note_text)
        # Save note logic
        return {'success': True, 'message': 'Note created'}
    
    def enhance_note_with_ai(self, topic, note_text):
        # Gemini AI processing
        response = self.model.generate_content(prompt)
        return response.text
```

### Key Backend Features

- **RESTful API Design**: Clean, consistent endpoints
- **AI Integration**: Gemini 2.5 Pro for  responses
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Track all operations and errors
- **Security**: Input validation and sanitization
- **Scalability**: Modular architecture for easy expansion

---

## 🤝 Contributing

We welcome contributions! Here's how our team worked:

### Development Workflow

**Safia's Workflow (Frontend)**:
1. Design UI mockups
2. Build React components
3. Integrate with backend APIs
4. Test user interactions
5. Optimize performance

**Ahmad's Workflow (Backend)**:
1. Design API endpoints
2. Implement AI features
3. Handle data processing
4. Test API responses
5. Deploy backend services

### How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes (frontend or backend)
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

---

## 🐛 Troubleshooting

### Backend Issues (Ahmad's Domain)

### 🧩 "API key not valid"
```
Solution:
1. Check .env file has the correct key
2. Verify key starts with "AIza..."
3. Ensure there are no spaces or quotes around the key
4. Restart app.py after adding or updating the key
```

### 🤖 "Gemini Model not found"
```
Solution:
Switched to model 2.5 pro
```

### 🌐 "Translator not working"
Issue:
The default translator API failed during runtime.
```
Solution:
1. Switched to Deep Translator for reliable multilingual support.
2. Installed using:
   pip install deep-translator
3. Updated import references in the translation module.
```

### ☁️ "Cloud Pipeline Crashing"
Issue:
The pipeline crashed during multiple parallel AI calls.
```
Solution:
1. Added async handling and error recovery in the Flask backend.
2. Implemented retry logic for unstable API requests.
3. Optimized concurrent request limits to prevent overload.
```

### Frontend Issues (Safia's Domain)

#### "Cannot connect to backend"
```bash
Solution:
1. Ensure backend is running (python app.py)
2. Check Flask is on http://localhost:5000
3. Verify CORS settings if using separate React server
```

#### "React components not loading"
```bash
Solution:
1. Clear browser cache
2. Check console for JavaScript errors
3. Verify all imports are correct
```

---

## 📊 Performance

### Speed Metrics

<img width="428" height="167" alt="image" src="https://github.com/user-attachments/assets/9dd74439-d966-45e2-a70e-c6cbf0089777" />


**Combined Performance: Frontend + Backend working seamlessly!**

---

## 🎓 Team Contributions Summary

### Safia Liaqat - Frontend Excellence
✅ Complete React UI/UX implementation  
✅ Responsive design for all devices  
✅ Interactive components and animations  
✅ API integration and state management  
✅ User experience optimization  

### Ahmad - Backend Mastery
✅ Complete Flask REST API  
✅ Gemini 2.5 Pro AI integration  
✅ All 5 AI-powered modules  
✅ File upload and cloud storage  
✅ Database and security implementation  

**Together**: A powerful, full-stack AI application! 🚀

---

## 🔒 Security

### Best Practices Implemented

**Backend Security (Ahmad)**:
- ✅ Input validation and sanitization
- ✅ Secure file upload handling
- ✅ API rate limiting
- ✅ Environment variable protection
- ✅ SQL injection prevention

**Frontend Security (Safia)**:
- ✅ XSS prevention
- ✅ CSRF token implementation
- ✅ Secure API calls
- ✅ Input validation on client side
- ✅ Secure state management

---

## 🌟 Acknowledgments

- **Safia Liaqat**: For creating an beautiful, intuitive frontend
- **Ahmad**: For building a robust, AI-powered backend
- **Google Gemini AI**: For providing free AI API
- **Cloudinary**: For free cloud storage
- **React & Flask Communities**: For excellent documentation
- **Open Source Contributors**: For inspiration and tools

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](Lisence.md) file for details.

---
## 🐛  PROBLEMS & FIXES LOG  ✅

The Problems I faced wile developing this project are in [Problems](Problem.md) file with how I solved them.

---

## 📞 Contact

### Project Maintainers

**Safia Liaqat** - Frontend Developer
- 💼 GitHub: [@safialiaqat](https://github.com/Safia-Liaqat)
- 🔗 LinkedIn: [Safia Liaqat](https://www.linkedin.com/in/safia-liaqat-7a8082200)
- 🎯 Expertise: React, UI/UX Design, Frontend Architecture

**Ahmad** - Backend Developer
- 📧 Email: ahmadleo498@gmail.com
- 💼 GitHub: [@ahmad](https://github.com/ck-ahmad)
- 🔗 LinkedIn: [Ahmad](https://linkedin.com/in/ahmad0763)
- 🎯 Expertise: Python, Flask, AI Integration, Backend Architecture

### Project Links
- 🌐 **Project Repository**: https://github.com/ck-ahmad/Student_AI_Assistant
- 📜 **Report Problem**: ahmadleo498@gmail.com

---

## 🎯 Roadmap

### Version 3.0 (Future Enhancements)

**Frontend (Safia's Planned Features)**:
- [ ] Progressive Web App (PWA) support
- [ ] Dark mode theme
- [ ] Advanced animations and transitions
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration UI

**Backend (Ahmad's Planned Features)**:
- [ ] User authentication system
- [ ] Advanced AI features
- [ ] Integration with more APIs
- [ ] Database optimization
- [ ] Microservices architecture

---

## 💖 Support the Project

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📖 Improving documentation
- 🤝 Contributing code (frontend or backend!)

---

<div align="center">

**Made with ❤️ by Safia Liaqat (Frontend - React) & Ahmad (Backend - Flask/AI)**

**Frontend: ⚛️ React.js | Backend: 🐍 Flask + 🤖 Gemini 2.5 Pro**

**A Perfect Full-Stack Collaboration** 🎓

[⬆ Back to Top](#-student-ai-assistant)

</div>
