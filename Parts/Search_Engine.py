"""
AI-Powered Smart Search Engine
Features: Web search, file search, to-do list, study timer with Gemini AI
"""

import os
import webbrowser
import logging
import json
import time
from datetime import datetime
import speech_recognition as sr
from deep_translator import GoogleTranslator
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    filename="search_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SearchEngineAI:
    def __init__(self, gemini_api_key):
        """Initialize Search Engine with AI"""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.translator = GoogleTranslator()
        self.recognizer = sr.Recognizer()
        self.todo_file = 'todo_list.json'
    
    def smart_search_suggestions(self, query):
        """Get AI-powered search suggestions"""
        try:
            prompt = f"""For the search query: "{query}"

Provide:
1. 3 refined search suggestions to get better results
2. Key topics related to this query
3. Recommended search filters or keywords
4. Alternative search terms

Format as bullet points, be concise."""
            
            response = self.model.generate_content(prompt)
            suggestions = response.text
            
            logging.info(f"Search suggestions generated for: {query}")
            return {
                'success': True,
                'suggestions': suggestions,
                'google_url': f"https://www.google.com/search?q={query}",
                'scholar_url': f"https://scholar.google.com/scholar?q={query}",
                'youtube_url': f"https://www.youtube.com/results?search_query={query}"
            }
        except Exception as e:
            logging.error(f"Error getting suggestions: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def web_search(self, query, search_engine='google', feature='search', translate_to=None):
        """Perform web search with multiple engines and features"""
        try:
            # Translate query if requested
            if translate_to:
               translated_query = GoogleTranslator(source='auto', target=translate_to).translate(query)
               query = translated_query
               logging.info(f"Query translated to {translate_to}: {query}")

            
            # Build URL based on engine and feature
            if search_engine == 'google':
                urls = {
                    'search': f"https://www.google.com/search?q={query}",
                    'maps': f"https://www.google.com/maps/search/{query}",
                    'images': f"https://www.google.com/search?tbm=isch&q={query}",
                    'videos': f"https://www.youtube.com/results?search_query={query}",
                    'scholar': f"https://scholar.google.com/scholar?q={query}"
                }
            elif search_engine == 'bing':
                urls = {
                    'search': f"https://www.bing.com/search?q={query}",
                    'maps': f"https://www.bing.com/maps?q={query}",
                    'images': f"https://www.bing.com/images/search?q={query}",
                    'videos': f"https://www.bing.com/videos/search?q={query}"
                }
            else:
                return {'success': False, 'message': 'Invalid search engine'}
            
            url = urls.get(feature, urls['search'])
            
            logging.info(f"Web search: {query} on {search_engine}/{feature}")
            return {
                'success': True,
                'url': url,
                'query': query,
                'engine': search_engine,
                'feature': feature
            }
        except Exception as e:
            logging.error(f"Error in web search: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def search_files(self, query, root_dir=None):
        """Search for files on local system"""
        try:
            if not root_dir:
                root_dir = os.path.expanduser("~")
            
            matched_files = []
            query_lower = query.lower()
            
            # Search in common directories for students
            search_dirs = [
                os.path.join(root_dir, 'Documents'),
                os.path.join(root_dir, 'Downloads'),
                os.path.join(root_dir, 'Desktop'),
                os.getcwd()
            ]
            
            for search_dir in search_dirs:
                if not os.path.exists(search_dir):
                    continue
                
                try:
                    for root, dirs, files in os.walk(search_dir):
                        # Limit depth to avoid long searches
                        if root.count(os.sep) - search_dir.count(os.sep) > 3:
                            continue
                        
                        for file in files:
                            if query_lower in file.lower():
                                matched_files.append({
                                    'name': file,
                                    'path': os.path.join(root, file),
                                    'size': os.path.getsize(os.path.join(root, file)),
                                    'modified': datetime.fromtimestamp(
                                        os.path.getmtime(os.path.join(root, file))
                                    ).isoformat()
                                })
                        
                        if len(matched_files) >= 50:  # Limit results
                            break
                except PermissionError:
                    continue
            
            logging.info(f"File search: {query} - found {len(matched_files)} files")
            return {
                'success': True,
                'files': matched_files,
                'count': len(matched_files)
            }
        except Exception as e:
            logging.error(f"Error searching files: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def voice_search(self):
        """Perform voice-based search"""
        try:
            with sr.Microphone() as source:
                print("Listening... Speak your search query.")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=10)
            
            query = self.recognizer.recognize_google(audio)
            logging.info(f"Voice search recognized: {query}")
            return {'success': True, 'query': query}
        except sr.UnknownValueError:
            return {'success': False, 'message': 'Could not understand speech'}
        except sr.RequestError as e:
            return {'success': False, 'message': f'Speech recognition error: {str(e)}'}
        except Exception as e:
            logging.error(f"Error in voice search: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def manage_todo(self, action, task=None, task_id=None):
        """Manage to-do list"""
        try:
            todos = self._load_todos()
            
            if action == 'add':
                todo_id = str(len(todos) + 1)
                todos[todo_id] = {
                    'task': task,
                    'created_at': datetime.now().isoformat(),
                    'completed': False
                }
                self._save_todos(todos)
                logging.info(f"Task added: {task}")
                return {'success': True, 'message': 'Task added successfully', 'task_id': todo_id}
            
            elif action == 'list':
                task_list = [
                    {'id': tid, **tdata}
                    for tid, tdata in todos.items()
                ]
                return {'success': True, 'tasks': task_list}
            
            elif action == 'complete':
                if task_id in todos:
                    todos[task_id]['completed'] = True
                    todos[task_id]['completed_at'] = datetime.now().isoformat()
                    self._save_todos(todos)
                    logging.info(f"Task completed: {task_id}")
                    return {'success': True, 'message': 'Task marked as complete'}
                else:
                    return {'success': False, 'message': 'Task not found'}
            
            elif action == 'delete':
                if task_id in todos:
                    del todos[task_id]
                    self._save_todos(todos)
                    logging.info(f"Task deleted: {task_id}")
                    return {'success': True, 'message': 'Task deleted successfully'}
                else:
                    return {'success': False, 'message': 'Task not found'}
            
            else:
                return {'success': False, 'message': 'Invalid action'}
        except Exception as e:
            logging.error(f"Error managing todo: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_ai_task_suggestions(self, current_tasks):
        """Get AI suggestions for task prioritization"""
        try:
            tasks_text = '\n'.join([f"- {t['task']}" for t in current_tasks if not t.get('completed')])
            
            prompt = f"""Here are a student's current tasks:

{tasks_text}

Provide:
1. Prioritization recommendation (which tasks to do first)
2. Time estimates for each task
3. Suggested schedule for today
4. Tips for productivity

Be practical and encouraging."""
            
            response = self.model.generate_content(prompt)
            suggestions = response.text
            
            return {'success': True, 'suggestions': suggestions}
        except Exception as e:
            logging.error(f"Error getting task suggestions: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def study_timer(self, work_minutes=25, break_minutes=5, sessions=1):
        """Pomodoro study timer"""
        try:
            results = []
            
            for session in range(sessions):
                print(f"\n📚 Study Session {session + 1}/{sessions}")
                print(f"Starting {work_minutes} minute study session...")
                
                start_time = time.time()
                # In real implementation, this would be async or use threading
                # For demo, we just record the intent
                
                results.append({
                    'session': session + 1,
                    'work_minutes': work_minutes,
                    'break_minutes': break_minutes,
                    'start_time': datetime.now().isoformat()
                })
                
                logging.info(f"Study timer: Session {session + 1} started")
            
            return {
                'success': True,
                'message': f'{sessions} session(s) timer set',
                'sessions': results
            }
        except Exception as e:
            logging.error(f"Error with study timer: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_study_music_recommendations(self):
        """Get AI-recommended study music"""
        try:
            prompt = """Recommend 10 types of study music or playlists that help with concentration.

For each, provide:
- Music type/genre
- When it's best used
- YouTube search term

Focus on scientifically-backed options for focus and productivity."""
            
            response = self.model.generate_content(prompt)
            recommendations = response.text
            
            return {'success': True, 'recommendations': recommendations}
        except Exception as e:
            logging.error(f"Error getting music recommendations: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _load_todos(self):
        """Load to-do list from file"""
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_todos(self, todos):
        """Save to-do list to file"""
        with open(self.todo_file, 'w') as f:
            json.dump(todos, f, indent=2)


def main():
    """CLI interface for testing"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    search_engine = SearchEngineAI(api_key)
    
    while True:
        print("\n" + "="*50)
        print("AI-POWERED SMART SEARCH")
        print("="*50)
        print("1. Web Search (with AI suggestions)")
        print("2. Voice Search")
        print("3. Search Local Files")
        print("4. Manage To-Do List")
        print("5. Get Task Prioritization (AI)")
        print("6. Study Timer (Pomodoro)")
        print("7. Get Study Music Recommendations")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            query = input("Enter search query: ")
            
            # Get AI suggestions first
            print("\n🤖 Getting AI suggestions...")
            suggestions = search_engine.smart_search_suggestions(query)
            
            if suggestions['success']:
                print(f"\n💡 AI SUGGESTIONS:\n{suggestions['suggestions']}")
            
            engine = input("\nSearch engine (google/bing): ") or 'google'
            feature = input("Feature (search/maps/images/videos/scholar): ") or 'search'
            translate = input("Translate query? (language code or n): ")
            
            result = search_engine.web_search(
                query, engine, feature,
                translate if translate.lower() != 'n' else None
            )
            
            if result['success']:
                print(f"\n🔗 Opening: {result['url']}")
                webbrowser.open(result['url'])
            else:
                print(f"\n{result['message']}")
        
        elif choice == '2':
            print("\nPreparing to listen...")
            result = search_engine.voice_search()
            
            if result['success']:
                print(f"\n🎤 You said: {result['query']}")
                
                # Get suggestions
                suggestions = search_engine.smart_search_suggestions(result['query'])
                if suggestions['success']:
                    print(f"\n💡 AI SUGGESTIONS:\n{suggestions['suggestions']}")
                
                search_now = input("\nSearch now? (y/n): ")
                if search_now.lower() == 'y':
                    search_result = search_engine.web_search(result['query'])
                    if search_result['success']:
                        webbrowser.open(search_result['url'])
            else:
                print(f"\n{result['message']}")
        
        elif choice == '3':
            query = input("Enter filename to search: ")
            root_dir = input("Search directory (press Enter for home): ")
            
            print(f"\n🔍 Searching for '{query}'...")
            result = search_engine.search_files(
                query,
                root_dir if root_dir else None
            )
            
            if result['success']:
                if result['files']:
                    print(f"\n📁 Found {result['count']} file(s):\n")
                    for i, file in enumerate(result['files'][:20], 1):  # Show first 20
                        size_kb = file['size'] / 1024
                        print(f"{i}. {file['name']}")
                        print(f"   Path: {file['path']}")
                        print(f"   Size: {size_kb:.1f} KB")
                        print()
                    
                    if result['count'] > 20:
                        print(f"... and {result['count'] - 20} more files")
                    
                    open_file = input("Open a file? Enter number (or n): ")
                    if open_file.lower() != 'n':
                        try:
                            file_idx = int(open_file) - 1
                            if 0 <= file_idx < len(result['files']):
                                os.startfile(result['files'][file_idx]['path'])
                                print("Opening file...")
                        except:
                            print("Invalid selection")
                else:
                    print("No files found.")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '4':
            print("\n📝 TO-DO LIST MANAGER")
            print("1. View tasks")
            print("2. Add task")
            print("3. Complete task")
            print("4. Delete task")
            
            todo_choice = input("Choose action: ")
            
            if todo_choice == '1':
                result = search_engine.manage_todo('list')
                if result['success']:
                    tasks = result['tasks']
                    if tasks:
                        print("\n📋 Your Tasks:")
                        for task in tasks:
                            status = "✅" if task.get('completed') else "⏳"
                            print(f"{status} {task['id']}. {task['task']}")
                    else:
                        print("No tasks yet.")
                else:
                    print(f"\n{result['message']}")
            
            elif todo_choice == '2':
                task = input("Enter task: ")
                result = search_engine.manage_todo('add', task=task)
                print(f"\n{result['message']}")
            
            elif todo_choice == '3':
                search_engine.manage_todo('list')
                task_id = input("Enter task ID to complete: ")
                result = search_engine.manage_todo('complete', task_id=task_id)
                print(f"\n{result['message']}")
            
            elif todo_choice == '4':
                search_engine.manage_todo('list')
                task_id = input("Enter task ID to delete: ")
                result = search_engine.manage_todo('delete', task_id=task_id)
                print(f"\n{result['message']}")
        
        elif choice == '5':
            result = search_engine.manage_todo('list')
            if result['success'] and result['tasks']:
                print("\n🤖 Getting AI task prioritization...")
                ai_result = search_engine.get_ai_task_suggestions(result['tasks'])
                
                if ai_result['success']:
                    print(f"\n💡 AI RECOMMENDATIONS:\n{ai_result['suggestions']}")
                else:
                    print(f"\n{ai_result['message']}")
            else:
                print("No tasks to prioritize. Add some tasks first!")
        
        elif choice == '6':
            print("\n⏱️ POMODORO STUDY TIMER")
            work_min = int(input("Work minutes (default 25): ") or 25)
            break_min = int(input("Break minutes (default 5): ") or 5)
            sessions = int(input("Number of sessions (default 1): ") or 1)
            
            result = search_engine.study_timer(work_min, break_min, sessions)
            
            if result['success']:
                print(f"\n✅ {result['message']}")
                print("\nTimer sessions configured:")
                for session in result['sessions']:
                    print(f"Session {session['session']}: {session['work_minutes']}min work + {session['break_minutes']}min break")
                print("\n💡 TIP: Use a dedicated timer app or phone timer for accurate timing.")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '7':
            print("\n🎵 Getting study music recommendations...")
            result = search_engine.get_study_music_recommendations()
            
            if result['success']:
                print(f"\n🎧 STUDY MUSIC RECOMMENDATIONS:\n{result['recommendations']}")
                
                search_music = input("\nSearch for music on YouTube? (y/n): ")
                if search_music.lower() == 'y':
                    music_query = input("Enter search term: ")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={music_query}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '0':
            print("Happy searching! Goodbye!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()