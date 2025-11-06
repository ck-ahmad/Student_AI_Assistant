"""
Complete Flask Application - Student AI Assistant
Main application file with all routes and integrations
"""

from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_cors import CORS
import os
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets
from dotenv import load_dotenv
from pathlib import Path


# Import custom modules
from Parts.Notes_AI import NotesAI
from Parts.Drive_Manager import DriveManagerAI
from Parts.Health_Tracker import HealthTrackerAI
from Parts.Quiz_Generator import QuizGeneratorAI
from Parts.Search_Engine import SearchEngineAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

load_dotenv()



# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure directories exist
for directory in ['uploads', 'notes', 'drive_files', 'static/css', 'static/js', 'templates']:
    os.makedirs(directory, exist_ok=True)

# Load API keys from environment
#GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'Your Key')



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

print("🔑 GEMINI_API_KEY:", GEMINI_API_KEY)
# Cloudinary config for file uploads
# CLOUDINARY_CONFIG = {
#     'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
#     'api_key': os.getenv('CLOUDINARY_API_KEY', ''),
#     'api_secret': os.getenv('CLOUDINARY_API_SECRET', '')
# }

CLOUDINARY_CONFIG = {
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', 'Your Name'),
    'api_key': os.getenv('CLOUDINARY_API_KEY', 'Your API Key'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET', 'Your Secrete Key')
}
# Initialize AI modules
try:
    notes_ai = NotesAI(GEMINI_API_KEY)
    drive_manager = DriveManagerAI(GEMINI_API_KEY, CLOUDINARY_CONFIG)
    health_tracker = HealthTrackerAI(GEMINI_API_KEY)
    quiz_generator = QuizGeneratorAI(GEMINI_API_KEY)
    search_engine = SearchEngineAI(GEMINI_API_KEY)
    print("✅ All AI modules initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: AI modules initialization error: {e}")
    print("⚠️ App will run but AI features may not work")

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# ==================== NOTES ROUTES ====================

@app.route('/notes')
def notes_page():
    """Notes management page"""
    return render_template('notes.html')

@app.route('/api/notes/create', methods=['POST'])
def create_note():
    try:
        data = request.json
        result = notes_ai.create_note(
            data.get('topic'),
            data.get('note'),
            data.get('use_ai', False)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/view', methods=['POST'])
def view_notes():
    try:
        data = request.json
        result = notes_ai.view_notes(data.get('topic'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/delete', methods=['POST'])
def delete_note():
    try:
        data = request.json
        result = notes_ai.delete_note(data.get('topic'), data.get('note_id'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/edit', methods=['POST'])
def edit_note():
    try:
        data = request.json
        result = notes_ai.edit_note(
            data.get('topic'),
            data.get('note_id'),
            data.get('new_text'),
            data.get('use_ai', False)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/search', methods=['POST'])
def search_notes():
    try:
        data = request.json
        result = notes_ai.search_notes(data.get('topic'), data.get('keyword'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/summarize', methods=['POST'])
def summarize_notes():
    try:
        data = request.json
        result = notes_ai.summarize_notes(data.get('topic'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/ask-ai', methods=['POST'])
def ask_ai_notes():
    try:
        data = request.json
        result = notes_ai.ask_ai_about_notes(data.get('topic'), data.get('question'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/notes/flashcards', methods=['POST'])
def generate_flashcards():
    try:
        data = request.json
        result = notes_ai.generate_flashcards(data.get('topic'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== DRIVE MANAGER ROUTES ====================

@app.route('/drive')
def drive_page():
    """Drive manager page"""
    return render_template('drive.html')

@app.route('/api/drive/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        semester = request.form.get('semester')
        degree = request.form.get('degree')
        subject = request.form.get('subject')
        description = request.form.get('description', '')
        use_cloud = request.form.get('use_cloud', 'false').lower() == 'true'
        
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        result = drive_manager.upload_file(
            temp_path, semester, degree, subject, description, use_cloud
        )
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify(result)
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/drive/add-link', methods=['POST'])
def add_link():
    try:
        data = request.json
        result = drive_manager.add_link(
            data.get('link'),
            data.get('semester'),
            data.get('degree'),
            data.get('subject'),
            data.get('filename', ''),
            data.get('description', '')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/drive/list', methods=['POST'])
def list_files():
    try:
        data = request.json
        result = drive_manager.list_files(
            data.get('semester'),
            data.get('degree'),
            data.get('subject')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/drive/delete', methods=['POST'])
def delete_file():
    try:
        data = request.json
        result = drive_manager.delete_file(data.get('file_id'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/drive/predefined', methods=['POST'])
def get_predefined_link():
    try:
        data = request.json
        result = drive_manager.get_predefined_link(data.get('semester'), data.get('subject'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== HEALTH TRACKER ROUTES ====================

@app.route('/health')
def health_page():
    """Health tracker page"""
    return render_template('health.html')

@app.route('/api/health/analyze', methods=['POST'])
def analyze_symptoms():
    try:
        data = request.json
        result = health_tracker.analyze_symptoms(
            data.get('symptoms'),
            data.get('age'),
            data.get('gender')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/health/search', methods=['POST'])
def search_health_info():
    try:
        data = request.json
        result = health_tracker.search_medical_info(
            data.get('query'),
            data.get('translate_to')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/health/wellness', methods=['POST'])
def get_wellness_tips():
    try:
        data = request.json
        result = health_tracker.get_wellness_tips(data.get('category', 'general'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== QUIZ ROUTES ====================

@app.route('/quiz')
def quiz_page():
    """Quiz generator page"""
    return render_template('quiz.html')

@app.route('/api/quiz/generate-from-notes', methods=['POST'])
def generate_quiz_notes():
    try:
        data = request.json
        result = quiz_generator.generate_quiz_from_notes(
            data.get('topic'),
            data.get('num_questions', 5),
            data.get('difficulty', 'medium'),
            data.get('quiz_type', 'mixed')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/quiz/generate-from-topic', methods=['POST'])
def generate_quiz_topic():
    try:
        data = request.json
        result = quiz_generator.generate_quiz_from_topic(
            data.get('topic'),
            data.get('num_questions', 5),
            data.get('difficulty', 'medium'),
            data.get('quiz_type', 'mixed')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/quiz/evaluate', methods=['POST'])
def evaluate_quiz():
    try:
        data = request.json
        result = quiz_generator.evaluate_quiz(
            data.get('questions'),
            data.get('answers')
        )
        
        if result['success']:
            quiz_generator.save_quiz_report(
                data.get('topic', 'Unknown'),
                result['score'],
                result['total'],
                result['percentage'],
                result['results']
            )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== SEARCH ENGINE ROUTES ====================

@app.route('/search')
def search_page():
    """Search engine page"""
    return render_template('search.html')

@app.route('/api/search/suggestions', methods=['POST'])
def search_suggestions():
    try:
        data = request.json
        result = search_engine.smart_search_suggestions(data.get('query'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/search/web', methods=['POST'])
def web_search():
    try:
        data = request.json
        result = search_engine.web_search(
            data.get('query'),
            data.get('engine', 'google'),
            data.get('feature', 'search'),
            data.get('translate_to')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/todo/manage', methods=['POST'])
def manage_todo():
    try:
        data = request.json
        result = search_engine.manage_todo(
            data.get('action'),
            data.get('task'),
            data.get('task_id')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎓 STUDENT AI ASSISTANT - Starting Server")
    print("="*60)
    print(f"✅ Flask App: Running")
    print(f"{'✅' if GEMINI_API_KEY != 'your-gemini-api-key-here' else '⚠️'} Gemini AI: {'Configured' if GEMINI_API_KEY != 'your-gemini-api-key-here' else 'NOT CONFIGURED - Add to .env'}")
    print(f"{'✅' if CLOUDINARY_CONFIG['cloud_name'] else '⚠️'} Cloudinary: {'Configured' if CLOUDINARY_CONFIG['cloud_name'] else 'NOT CONFIGURED (Optional)'}")
    print(f"\n🌐 Access the app at: http://localhost:5000")
    print(f"📱 Or from network: http://0.0.0.0:5000")
    print("="*60 + "\n")
    

    app.run(debug=True, host='0.0.0.0', port=5000)
