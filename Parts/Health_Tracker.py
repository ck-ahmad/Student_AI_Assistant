"""
AI-Powered Health Tracker
Features: Health information search, symptom analysis, wellness tips with Gemini AI
"""

import os
import logging
import webbrowser
import speech_recognition as sr
from deep_translator import GoogleTranslator
import google.generativeai as genai
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    filename="health_tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# 
class HealthTrackerAI:
    def __init__(self, gemini_api_key):
        """Initialize Health Tracker with AI"""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.translator = GoogleTranslator()
        self.recognizer = sr.Recognizer()
        self.health_history_file = 'health_history.json'
    
    def analyze_symptoms(self, symptoms, age=None, gender=None):
        """Analyze symptoms using Gemini AI"""
        try:
            age_info = f", age {age}" if age else ""
            gender_info = f", {gender}" if gender else ""
            
            prompt = f"""As a health information assistant, analyze these symptoms{age_info}{gender_info}:

Symptoms: {symptoms}

Provide:
1. Possible conditions (general information only)
2. Common causes
3. When to see a doctor (warning signs)
4. Home care recommendations
5. Prevention tips

IMPORTANT DISCLAIMER: This is educational information only, not medical advice. Always consult healthcare professionals for medical concerns, especially if symptoms are severe or persistent."""
            
            response = self.model.generate_content(prompt)
            analysis = response.text
            
            # Save to history
            self._save_to_history({
                'type': 'symptom_analysis',
                'symptoms': symptoms,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
            
            logging.info(f"Symptoms analyzed: {symptoms}")
            return {
                'success': True,
                'analysis': analysis,
                'webmd_url': f"https://www.webmd.com/search/search_results/default.aspx?query={symptoms}"
            }
        except Exception as e:
            logging.error(f"Error analyzing symptoms: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_wellness_tips(self, category='general'):
        """Get wellness tips for specific category"""
        try:
            categories_prompts = {
                'general': 'general wellness and healthy living',
                'nutrition': 'nutrition and healthy eating',
                'exercise': 'exercise and physical fitness',
                'mental': 'mental health and stress management',
                'sleep': 'sleep hygiene and better sleep',
                'hydration': 'proper hydration and water intake'
            }
            
            topic = categories_prompts.get(category, categories_prompts['general'])
            
            prompt = f"""Provide 10 practical, evidence-based tips for {topic}.

Format each tip as:
Tip [number]: [brief title]
[detailed explanation in 2-3 sentences]

Focus on actionable, easy-to-implement advice."""
            
            response = self.model.generate_content(prompt)
            tips = response.text
            
            logging.info(f"Wellness tips generated for: {category}")
            return {'success': True, 'tips': tips, 'category': category}
        except Exception as e:
            logging.error(f"Error getting wellness tips: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def search_medical_info(self, query, translate_to=None):
        """Search for medical information"""
        try:
            # Translate if requested
            if translate_to:
                translated_query = GoogleTranslator(source='auto', target=translate_to).translate(query)
                query = translated_query
                logging.info(f"Query translated to {translate_to}: {query}")

            
            # Get AI information
            prompt = f"""Provide comprehensive health information about: {query}

Include:
1. Overview and definition
2. Common symptoms or characteristics
3. Causes and risk factors
4. Treatment options (general information)
5. Prevention and lifestyle recommendations
6. When to seek medical help

Provide evidence-based, reliable information. Include disclaimer about consulting healthcare professionals."""
            
            response = self.model.generate_content(prompt)
            info = response.text
            
            # Generate search URLs
            webmd_url = f"https://www.webmd.com/search/search_results/default.aspx?query={query}"
            mayo_url = f"https://www.mayoclinic.org/search/search-results?q={query}"
            
            logging.info(f"Medical info searched: {query}")
            return {
                'success': True,
                'info': info,
                'query': query,
                'webmd_url': webmd_url,
                'mayo_url': mayo_url
            }
        except Exception as e:
            logging.error(f"Error searching medical info: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def voice_health_query(self):
        """Record voice query about health"""
        try:
            with sr.Microphone() as source:
                print("Listening... Speak your health query.")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=15)
            
            query = self.recognizer.recognize_google(audio)
            logging.info(f"Voice query recognized: {query}")
            return {'success': True, 'query': query}
        except sr.UnknownValueError:
            return {'success': False, 'message': 'Could not understand speech'}
        except sr.RequestError as e:
            return {'success': False, 'message': f'Speech recognition error: {str(e)}'}
        except Exception as e:
            logging.error(f"Error in voice query: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_first_aid_guide(self, emergency_type):
        """Get AI-generated first aid instructions"""
        try:
            prompt = f"""Provide clear, step-by-step first aid instructions for: {emergency_type}

Format:
1. Immediate actions (what to do first)
2. Step-by-step procedure
3. What NOT to do (common mistakes)
4. When to call emergency services
5. Follow-up care

CRITICAL: Start with "CALL EMERGENCY SERVICES IMMEDIATELY IF:" and list life-threatening signs.

Keep instructions clear, numbered, and easy to follow in an emergency."""
            
            response = self.model.generate_content(prompt)
            guide = response.text
            
            logging.info(f"First aid guide generated: {emergency_type}")
            return {'success': True, 'guide': guide, 'emergency_type': emergency_type}
        except Exception as e:
            logging.error(f"Error getting first aid guide: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def check_medication_info(self, medication_name):
        """Get information about a medication"""
        try:
            prompt = f"""Provide general information about the medication: {medication_name}

Include:
1. What it's used for (indications)
2. How it typically works
3. Common side effects
4. General precautions
5. Important interactions to be aware of

IMPORTANT: This is general educational information. Always follow your doctor's prescription and instructions. Never use this to self-medicate."""
            
            response = self.model.generate_content(prompt)
            info = response.text
            
            # Search URLs
            drugs_url = f"https://www.drugs.com/search.php?searchterm={medication_name}"
            
            logging.info(f"Medication info checked: {medication_name}")
            return {
                'success': True,
                'info': info,
                'medication': medication_name,
                'drugs_url': drugs_url
            }
        except Exception as e:
            logging.error(f"Error checking medication: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_mental_health_support(self, concern):
        """Get mental health information and coping strategies"""
        try:
            prompt = f"""Provide supportive information about: {concern}

Include:
1. Understanding the concern (validation and normalization)
2. Coping strategies and techniques
3. Self-care recommendations
4. When to seek professional help
5. Resources and support options

Be empathetic, non-judgmental, and encouraging. Emphasize that seeking help is a sign of strength."""
            
            response = self.model.generate_content(prompt)
            support = response.text
            
            # Mental health resources
            resources = {
                'crisis_text': 'Text HOME to 741741',
                'suicide_hotline': '988',
                'online_therapy': 'BetterHelp, Talkspace'
            }
            
            logging.info(f"Mental health support provided for: {concern}")
            return {
                'success': True,
                'support': support,
                'concern': concern,
                'resources': resources
            }
        except Exception as e:
            logging.error(f"Error getting mental health support: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def create_health_reminder(self, reminder_text, frequency='daily'):
        """Create a health reminder"""
        try:
            reminders = self._load_reminders()
            reminder_id = str(len(reminders) + 1)
            
            reminders[reminder_id] = {
                'text': reminder_text,
                'frequency': frequency,
                'created_at': datetime.now().isoformat(),
                'active': True
            }
            
            self._save_reminders(reminders)
            
            logging.info(f"Health reminder created: {reminder_text}")
            return {
                'success': True,
                'message': 'Reminder created successfully!',
                'reminder_id': reminder_id
            }
        except Exception as e:
            logging.error(f"Error creating reminder: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def view_health_history(self):
        """View health search history"""
        try:
            if not os.path.exists(self.health_history_file):
                return {'success': True, 'history': []}
            
            with open(self.health_history_file, 'r') as f:
                history = json.load(f)
            
            return {'success': True, 'history': history}
        except Exception as e:
            logging.error(f"Error viewing history: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _save_to_history(self, entry):
        """Save entry to health history"""
        try:
            history = []
            if os.path.exists(self.health_history_file):
                with open(self.health_history_file, 'r') as f:
                    history = json.load(f)
            
            history.append(entry)
            
            # Keep only last 100 entries
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.health_history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving to history: {str(e)}")
    
    def _load_reminders(self):
        """Load health reminders"""
        reminders_file = 'health_reminders.json'
        if os.path.exists(reminders_file):
            with open(reminders_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_reminders(self, reminders):
        """Save health reminders"""
        reminders_file = 'health_reminders.json'
        with open(reminders_file, 'w') as f:
            json.dump(reminders, f, indent=2)


def main():
    """CLI interface for testing"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    health_tracker = HealthTrackerAI(api_key)
    
    while True:
        print("\n" + "="*50)
        print("AI-POWERED HEALTH TRACKER")
        print("="*50)
        print("1. Analyze Symptoms")
        print("2. Search Medical Information")
        print("3. Get Wellness Tips")
        print("4. First Aid Guide")
        print("5. Medication Information")
        print("6. Mental Health Support")
        print("7. Voice Health Query")
        print("8. Create Health Reminder")
        print("9. View Health History")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            symptoms = input("Describe your symptoms: ")
            age = input("Age (optional): ")
            gender = input("Gender (optional): ")
            
            print("\nAnalyzing symptoms...")
            result = health_tracker.analyze_symptoms(
                symptoms,
                age if age else None,
                gender if gender else None
            )
            
            if result['success']:
                print(f"\n🏥 ANALYSIS:\n{result['analysis']}")
                print(f"\nMore info: {result['webmd_url']}")
                
                open_web = input("\nOpen WebMD in browser? (y/n): ")
                if open_web.lower() == 'y':
                    webbrowser.open(result['webmd_url'])
            else:
                print(f"\n{result['message']}")
        
        elif choice == '2':
            query = input("Enter health topic to search: ")
            translate = input("Translate query? (language code or n): ")
            
            print("\nSearching...")
            result = health_tracker.search_medical_info(
                query,
                translate if translate.lower() != 'n' else None
            )
            
            if result['success']:
                print(f"\n📚 INFORMATION:\n{result['info']}")
                print(f"\nWebMD: {result['webmd_url']}")
                print(f"Mayo Clinic: {result['mayo_url']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '3':
            print("\nCategories: general, nutrition, exercise, mental, sleep, hydration")
            category = input("Choose category: ")
            
            print("\nGenerating tips...")
            result = health_tracker.get_wellness_tips(category)
            
            if result['success']:
                print(f"\n💡 WELLNESS TIPS ({result['category']}):\n{result['tips']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '4':
            emergency = input("Enter emergency type (e.g., burns, choking, bleeding): ")
            
            print("\nGenerating first aid guide...")
            result = health_tracker.get_first_aid_guide(emergency)
            
            if result['success']:
                print(f"\n🚨 FIRST AID GUIDE:\n{result['guide']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '5':
            medication = input("Enter medication name: ")
            
            print("\nLooking up medication...")
            result = health_tracker.check_medication_info(medication)
            
            if result['success']:
                print(f"\n💊 MEDICATION INFO:\n{result['info']}")
                print(f"\nMore details: {result['drugs_url']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '6':
            concern = input("What's on your mind? ")
            
            print("\nGathering support information...")
            result = health_tracker.get_mental_health_support(concern)
            
            if result['success']:
                print(f"\n🧠 MENTAL HEALTH SUPPORT:\n{result['support']}")
                print(f"\nCRISIS RESOURCES:")
                for key, value in result['resources'].items():
                    print(f"{key}: {value}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '7':
            print("\nPreparing to listen...")
            result = health_tracker.voice_health_query()
            
            if result['success']:
                print(f"\nYou asked: {result['query']}")
                search_result = health_tracker.search_medical_info(result['query'])
                if search_result['success']:
                    print(f"\n📚 INFORMATION:\n{search_result['info']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '8':
            reminder = input("Enter reminder text: ")
            frequency = input("Frequency (daily/weekly/monthly): ")
            
            result = health_tracker.create_health_reminder(reminder, frequency)
            print(f"\n{result['message']}")
        
        elif choice == '9':
            result = health_tracker.view_health_history()
            
            if result['success'] and result['history']:
                print(f"\n📋 HEALTH HISTORY:")
                for i, entry in enumerate(result['history'][-10:], 1):  # Show last 10
                    print(f"\n{i}. {entry['type']} - {entry['timestamp']}")
                    if entry['type'] == 'symptom_analysis':
                        print(f"   Symptoms: {entry['symptoms']}")
            else:
                print("No history found.")
        
        elif choice == '0':
            print("Stay healthy! Goodbye!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()