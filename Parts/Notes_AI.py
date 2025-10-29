"""
AI-Powered Notes Management System
Features: Create, view, edit, delete, search notes with Gemini AI enhancement
"""

import os
import logging
from datetime import datetime
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment

# Configure logging
logging.basicConfig(
    filename="notes_ai.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class NotesAI:
    def __init__(self, gemini_api_key):
        """Initialize with Gemini AI"""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.recognizer = sr.Recognizer()
        
    def create_note(self, topic, note_text, use_ai=False):
        """Create a new note with optional AI enhancement"""
        try:
            # Enhance note with Gemini AI if requested
            if use_ai and note_text:
                note_text = self.enhance_note_with_ai(topic, note_text)
            
            filename = topic.replace(" ", "_") + "_notes.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filename, "a", encoding='utf-8') as file:
                file.write(f"{timestamp} - {note_text}\n")
            
            logging.info(f"Note created for topic: {topic}")
            return {
                'success': True,
                'message': 'Note added successfully!' + (' (AI Enhanced)' if use_ai else ''),
                'timestamp': timestamp,
                'enhanced_note': note_text
            }
        except Exception as e:
            logging.error(f"Error creating note: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def enhance_note_with_ai(self, topic, note_text):
        """Enhance note using Gemini AI"""
        try:
            prompt = f"""Improve and organize this note for a student studying {topic}:

Note: {note_text}

Please:
1. Correct any grammar or spelling errors
2. Format it clearly with bullet points if appropriate
3. Add relevant key concepts if missing
4. Keep it concise and study-friendly
5. Preserve all important information

Return only the improved note without extra commentary."""
            
            response = self.model.generate_content(prompt)
            enhanced_text = response.text
            logging.info(f"Note enhanced with AI for topic: {topic}")
            return enhanced_text
        except Exception as e:
            logging.error(f"AI enhancement error: {str(e)}")
            return note_text  # Return original if AI fails
    
    def view_notes(self, topic):
        """View all notes for a topic"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': True, 'notes': []}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.readlines()
            
            notes_list = [
                {'id': idx, 'text': note.strip()} 
                for idx, note in enumerate(notes, 1)
            ]
            
            return {'success': True, 'notes': notes_list}
        except Exception as e:
            logging.error(f"Error viewing notes: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def delete_note(self, topic, note_id):
        """Delete a specific note"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.readlines()
            
            if 1 <= note_id <= len(notes):
                notes.pop(note_id - 1)
                with open(filename, "w", encoding='utf-8') as file:
                    file.writelines(notes)
                logging.info(f"Note {note_id} deleted from topic: {topic}")
                return {'success': True, 'message': 'Note deleted successfully!'}
            else:
                return {'success': False, 'message': 'Invalid note ID'}
        except Exception as e:
            logging.error(f"Error deleting note: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def edit_note(self, topic, note_id, new_text, use_ai=False):
        """Edit an existing note"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.readlines()
            
            if 1 <= note_id <= len(notes):
                if use_ai:
                    new_text = self.enhance_note_with_ai(topic, new_text)
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                notes[note_id - 1] = f"{timestamp} - {new_text}\n"
                
                with open(filename, "w", encoding='utf-8') as file:
                    file.writelines(notes)
                
                logging.info(f"Note {note_id} edited for topic: {topic}")
                return {
                    'success': True, 
                    'message': 'Note updated successfully!',
                    'enhanced_note': new_text
                }
            else:
                return {'success': False, 'message': 'Invalid note ID'}
        except Exception as e:
            logging.error(f"Error editing note: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def search_notes(self, topic, keyword):
        """Search notes by keyword"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': True, 'notes': []}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.readlines()
            
            found_notes = [
                {'id': idx, 'text': note.strip()}
                for idx, note in enumerate(notes, 1)
                if keyword.lower() in note.lower()
            ]
            
            return {'success': True, 'notes': found_notes}
        except Exception as e:
            logging.error(f"Error searching notes: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def summarize_notes(self, topic):
        """Summarize all notes for a topic using AI"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': False, 'message': 'No notes found for this topic'}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.read()
            
            if not notes.strip():
                return {'success': False, 'message': 'No notes to summarize'}
            
            prompt = f"""Summarize these study notes for {topic}:

{notes}

Create a comprehensive summary that includes:
1. Main topics covered
2. Key concepts and definitions
3. Important points to remember
4. Quick review points
5. Study tips based on the content

Format it in a clear, organized way that's easy to review before exams."""
            
            response = self.model.generate_content(prompt)
            summary = response.text
            
            logging.info(f"Notes summarized for topic: {topic}")
            return {'success': True, 'summary': summary}
        except Exception as e:
            logging.error(f"Error summarizing notes: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def ask_ai_about_notes(self, topic, question):
        """Ask AI questions about your notes"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': False, 'message': 'No notes found for this topic'}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.read()
            
            prompt = f"""Based on these study notes for {topic}:

{notes}

Question: {question}

Provide a clear, educational answer based on the notes. If the notes don't contain enough information, mention that and provide general knowledge about the topic."""
            
            response = self.model.generate_content(prompt)
            answer = response.text
            
            logging.info(f"AI answered question for topic: {topic}")
            return {'success': True, 'answer': answer}
        except Exception as e:
            logging.error(f"Error asking AI: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def generate_flashcards(self, topic):
        """Generate flashcards from notes using AI"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': False, 'message': 'No notes found for this topic'}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes = file.read()
            
            prompt = f"""Based on these notes for {topic}, create 10 flashcards:

{notes}

Format each flashcard as:
FRONT: [question or term]
BACK: [answer or definition]

Focus on key concepts, definitions, and important facts."""
            
            response = self.model.generate_content(prompt)
            flashcards_text = response.text
            
            # Parse flashcards
            flashcards = self._parse_flashcards(flashcards_text)
            
            logging.info(f"Flashcards generated for topic: {topic}")
            return {'success': True, 'flashcards': flashcards}
        except Exception as e:
            logging.error(f"Error generating flashcards: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _parse_flashcards(self, text):
        """Parse flashcards from AI response"""
        flashcards = []
        lines = text.split('\n')
        current_card = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('FRONT:'):
                if current_card:
                    flashcards.append(current_card)
                current_card = {'front': line[6:].strip()}
            elif line.startswith('BACK:'):
                current_card['back'] = line[5:].strip()
        
        if current_card:
            flashcards.append(current_card)
        
        return flashcards
    
    def record_voice_note(self, topic):
        """Record a voice note and transcribe it"""
        try:
            with sr.Microphone() as source:
                print("Listening... Speak your note.")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=30)
            
            # Transcribe audio
            note_text = self.recognizer.recognize_google(audio)
            print(f"Transcribed: {note_text}")
            
            # Save audio file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            audio_filename = f"{topic}_{timestamp}_voice_note.wav"
            
            with open(audio_filename, "wb") as audio_file:
                audio_file.write(audio.get_wav_data())
            
            # Convert to MP3
            sound = AudioSegment.from_wav(audio_filename)
            audio_mp3_filename = audio_filename.replace(".wav", ".mp3")
            sound.export(audio_mp3_filename, format="mp3")
            os.remove(audio_filename)
            
            # Save transcribed note
            result = self.create_note(
                topic, 
                f"{note_text} (Audio: {audio_mp3_filename})", 
                use_ai=True
            )
            
            logging.info(f"Voice note recorded for topic: {topic}")
            return result
        except sr.UnknownValueError:
            return {'success': False, 'message': 'Could not understand speech'}
        except sr.RequestError as e:
            return {'success': False, 'message': f'Speech recognition error: {str(e)}'}
        except Exception as e:
            logging.error(f"Error recording voice note: {str(e)}")
            return {'success': False, 'message': str(e)}


def main():
    """CLI interface for testing"""
    import sys
    
    # Get API key from environment or argument
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    notes_ai = NotesAI(api_key)
    
    while True:
        print("\n" + "="*50)
        print("AI-POWERED NOTES MANAGER")
        print("="*50)
        print("1. Create Note (with AI enhancement)")
        print("2. View Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Search Notes")
        print("6. Summarize Notes")
        print("7. Ask AI about Notes")
        print("8. Generate Flashcards")
        print("9. Record Voice Note")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            topic = input("Enter topic: ")
            note = input("Enter note: ")
            use_ai = input("Enhance with AI? (y/n): ").lower() == 'y'
            result = notes_ai.create_note(topic, note, use_ai)
            print(f"\n{result['message']}")
            if use_ai and result.get('enhanced_note'):
                print(f"Enhanced note: {result['enhanced_note']}")
        
        elif choice == '2':
            topic = input("Enter topic: ")
            result = notes_ai.view_notes(topic)
            if result['notes']:
                print(f"\nNotes for {topic}:")
                for note in result['notes']:
                    print(f"{note['id']}. {note['text']}")
            else:
                print("No notes found.")
        
        elif choice == '3':
            topic = input("Enter topic: ")
            notes_ai.view_notes(topic)
            note_id = int(input("Enter note ID to edit: "))
            new_text = input("Enter new text: ")
            use_ai = input("Enhance with AI? (y/n): ").lower() == 'y'
            result = notes_ai.edit_note(topic, note_id, new_text, use_ai)
            print(f"\n{result['message']}")
        
        elif choice == '4':
            topic = input("Enter topic: ")
            notes_ai.view_notes(topic)
            note_id = int(input("Enter note ID to delete: "))
            result = notes_ai.delete_note(topic, note_id)
            print(f"\n{result['message']}")
        
        elif choice == '5':
            topic = input("Enter topic: ")
            keyword = input("Enter keyword to search: ")
            result = notes_ai.search_notes(topic, keyword)
            if result['notes']:
                print(f"\nFound {len(result['notes'])} note(s):")
                for note in result['notes']:
                    print(f"{note['id']}. {note['text']}")
            else:
                print("No notes found.")
        
        elif choice == '6':
            topic = input("Enter topic: ")
            result = notes_ai.summarize_notes(topic)
            if result['success']:
                print(f"\n📋 SUMMARY:\n{result['summary']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '7':
            topic = input("Enter topic: ")
            question = input("Ask a question: ")
            result = notes_ai.ask_ai_about_notes(topic, question)
            if result['success']:
                print(f"\n🤖 AI Answer:\n{result['answer']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '8':
            topic = input("Enter topic: ")
            result = notes_ai.generate_flashcards(topic)
            if result['success']:
                print(f"\n📇 FLASHCARDS:")
                for i, card in enumerate(result['flashcards'], 1):
                    print(f"\nCard {i}:")
                    print(f"Front: {card['front']}")
                    print(f"Back: {card['back']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '9':
            topic = input("Enter topic: ")
            print("\nPreparing to record...")
            result = notes_ai.record_voice_note(topic)
            print(f"\n{result['message']}")
        
        elif choice == '0':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()