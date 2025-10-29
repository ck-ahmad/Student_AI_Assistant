"""
AI-Powered Quiz Generator
Features: Generate quizzes from notes, multiple formats, instant feedback with Gemini AI
"""

import os
import json
import logging
import csv
from datetime import datetime
import google.generativeai as genai
import difflib

# Configure logging
logging.basicConfig(
    filename="quiz_generator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class QuizGeneratorAI:
    def __init__(self, gemini_api_key):
        """Initialize Quiz Generator with AI"""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.notes_dir = "notes"
        self.report_file = "quiz_reports.csv"
        os.makedirs(self.notes_dir, exist_ok=True)
    
    def generate_quiz_from_notes(self, topic, num_questions=5, difficulty='medium', quiz_type='mixed'):
        """Generate quiz from existing notes using AI"""
        try:
            filename = topic.replace(" ", "_") + "_notes.txt"
            
            if not os.path.exists(filename):
                return {'success': False, 'message': 'No notes found for this topic'}
            
            with open(filename, "r", encoding='utf-8') as file:
                notes_content = file.read()
            
            if not notes_content.strip():
                return {'success': False, 'message': 'Notes are empty'}
            
            # Generate quiz based on type
            if quiz_type == 'mcq':
                quiz_format = "multiple choice questions with 4 options each"
            elif quiz_type == 'tf':
                quiz_format = "true/false questions"
            elif quiz_type == 'short':
                quiz_format = "short answer questions"
            else:  # mixed
                quiz_format = "a mix of multiple choice, true/false, and short answer questions"
            
            prompt = f"""Based on these study notes for {topic}, generate {num_questions} {difficulty} difficulty {quiz_format}:

{notes_content}

For each question, format as:
TYPE: [MCQ/TF/SHORT]
Q: [question text]
A: [correct answer]
OPTIONS: [for MCQ: option1, option2, option3, option4]
EXPLANATION: [brief explanation of the answer]

Requirements:
- Test understanding, not just memorization
- Difficulty level: {difficulty}
- Cover different parts of the notes
- Clear, unambiguous questions
- For MCQ, make distractors plausible"""
            
            response = self.model.generate_content(prompt)
            quiz_text = response.text
            
            # Parse quiz
            questions = self._parse_quiz_response(quiz_text)
            
            if not questions:
                return {'success': False, 'message': 'Failed to generate quiz'}
            
            logging.info(f"Quiz generated for {topic}: {len(questions)} questions")
            return {
                'success': True,
                'questions': questions,
                'topic': topic,
                'difficulty': difficulty,
                'type': quiz_type
            }
        except Exception as e:
            logging.error(f"Error generating quiz: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def generate_quiz_from_topic(self, topic, num_questions=5, difficulty='medium', quiz_type='mixed'):
        """Generate quiz on a topic without notes using AI"""
        try:
            if quiz_type == 'mcq':
                quiz_format = "multiple choice questions with 4 options each"
            elif quiz_type == 'tf':
                quiz_format = "true/false questions"
            elif quiz_type == 'short':
                quiz_format = "short answer questions"
            else:  # mixed
                quiz_format = "a mix of multiple choice, true/false, and short answer questions"
            
            prompt = f"""Generate {num_questions} {difficulty} difficulty {quiz_format} about {topic}.

For each question, format as:
TYPE: [MCQ/TF/SHORT]
Q: [question text]
A: [correct answer]
OPTIONS: [for MCQ: option1, option2, option3, option4]
EXPLANATION: [brief explanation of the answer]

Requirements:
- Cover key concepts in {topic}
- Test understanding and application
- Difficulty level: {difficulty}
- Clear, educational questions
- For MCQ, make distractors plausible but clearly wrong"""
            
            response = self.model.generate_content(prompt)
            quiz_text = response.text
            
            # Parse quiz
            questions = self._parse_quiz_response(quiz_text)
            
            if not questions:
                return {'success': False, 'message': 'Failed to generate quiz'}
            
            logging.info(f"Quiz generated for {topic}: {len(questions)} questions")
            return {
                'success': True,
                'questions': questions,
                'topic': topic,
                'difficulty': difficulty,
                'type': quiz_type
            }
        except Exception as e:
            logging.error(f"Error generating quiz: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _parse_quiz_response(self, quiz_text):
        """Parse AI-generated quiz into structured format"""
        questions = []
        lines = quiz_text.split('\n')
        current_q = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TYPE:'):
                if current_q and 'question' in current_q:
                    questions.append(current_q)
                current_q = {'type': line[5:].strip()}
            elif line.startswith('Q:'):
                current_q['question'] = line[2:].strip()
            elif line.startswith('A:'):
                current_q['answer'] = line[2:].strip()
            elif line.startswith('OPTIONS:'):
                options = line[8:].strip().split(',')
                current_q['options'] = [opt.strip() for opt in options]
            elif line.startswith('EXPLANATION:'):
                current_q['explanation'] = line[12:].strip()
        
        if current_q and 'question' in current_q:
            questions.append(current_q)
        
        return questions
    
    def evaluate_answer(self, question, user_answer, get_feedback=True):
        """Evaluate a single answer with AI feedback"""
        try:
            correct_answer = question.get('answer', '')
            q_type = question.get('type', 'SHORT')
            
            # Check if answer is correct
            if q_type == 'TF':
                is_correct = user_answer.lower().strip() in ['true', 't'] and correct_answer.lower().strip() in ['true', 't'] or \
                            user_answer.lower().strip() in ['false', 'f'] and correct_answer.lower().strip() in ['false', 'f']
            elif q_type == 'MCQ':
                is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            else:  # SHORT
                # Use similarity for short answers
                similarity = difflib.SequenceMatcher(None, 
                                                    user_answer.lower().strip(), 
                                                    correct_answer.lower().strip()).ratio()
                is_correct = similarity > 0.7
            
            # Get AI feedback if requested
            if get_feedback:
                prompt = f"""Question: {question['question']}
Student's Answer: {user_answer}
Correct Answer: {correct_answer}
Question Type: {q_type}

Provide brief, encouraging feedback (2-3 sentences) that:
{'- Praises the correct answer and reinforces the concept' if is_correct else '- Explains why the answer is incorrect'}
{'- Explains the key concept' if not is_correct else '- Mentions a related concept or application'}
- Is supportive and educational"""
                
                response = self.model.generate_content(prompt)
                feedback = response.text
            else:
                feedback = question.get('explanation', 
                                       "Correct!" if is_correct else f"The correct answer is: {correct_answer}")
            
            return {
                'is_correct': is_correct,
                'feedback': feedback,
                'correct_answer': correct_answer
            }
        except Exception as e:
            logging.error(f"Error evaluating answer: {str(e)}")
            return {
                'is_correct': False,
                'feedback': 'Error evaluating answer',
                'correct_answer': question.get('answer', '')
            }
    
    def evaluate_quiz(self, questions, user_answers):
        """Evaluate entire quiz and provide detailed feedback"""
        try:
            score = 0
            total = len(questions)
            results = []
            
            for i, (question, user_answer) in enumerate(zip(questions, user_answers)):
                evaluation = self.evaluate_answer(question, user_answer, get_feedback=True)
                
                if evaluation['is_correct']:
                    score += 1
                
                results.append({
                    'question_num': i + 1,
                    'question': question['question'],
                    'type': question.get('type', 'SHORT'),
                    'user_answer': user_answer,
                    'correct_answer': evaluation['correct_answer'],
                    'is_correct': evaluation['is_correct'],
                    'feedback': evaluation['feedback']
                })
            
            percentage = (score / total * 100) if total > 0 else 0
            
            # Get overall performance feedback
            overall_feedback = self._get_overall_feedback(percentage, results)
            
            return {
                'success': True,
                'score': score,
                'total': total,
                'percentage': percentage,
                'results': results,
                'overall_feedback': overall_feedback
            }
        except Exception as e:
            logging.error(f"Error evaluating quiz: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _get_overall_feedback(self, percentage, results):
        """Generate overall performance feedback using AI"""
        try:
            wrong_topics = [r['question'] for r in results if not r['is_correct']]
            
            prompt = f"""A student scored {percentage:.1f}% on a quiz.

{'Areas needing improvement:' if wrong_topics else 'All questions answered correctly!'}
{chr(10).join(f'- {q}' for q in wrong_topics[:3]) if wrong_topics else ''}

Provide:
1. Brief performance assessment (1 sentence)
2. Specific study recommendations (2-3 points)
3. Encouragement and next steps (1 sentence)

Be supportive and constructive."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except:
            if percentage >= 90:
                return "Excellent work! Keep up the great study habits."
            elif percentage >= 70:
                return "Good job! Review the missed topics and you'll master them."
            elif percentage >= 50:
                return "You're making progress. Focus on understanding core concepts."
            else:
                return "Keep studying! Review your notes and try practice questions."
    
    def save_quiz_report(self, topic, score, total, percentage, results):
        """Save quiz results to CSV report"""
        try:
            file_exists = os.path.exists(self.report_file)
            
            with open(self.report_file, mode='a', newline='', encoding='utf-8') as file:
                fieldnames = ['timestamp', 'topic', 'score', 'total', 'percentage', 'details']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                # Create details summary
                details = f"{score}/{total} correct"
                
                writer.writerow({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'topic': topic,
                    'score': score,
                    'total': total,
                    'percentage': f"{percentage:.1f}%",
                    'details': details
                })
            
            logging.info(f"Quiz report saved: {topic} - {score}/{total}")
            return {'success': True, 'message': 'Report saved successfully'}
        except Exception as e:
            logging.error(f"Error saving report: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def view_quiz_history(self):
        """View quiz history from reports"""
        try:
            if not os.path.exists(self.report_file):
                return {'success': True, 'history': []}
            
            history = []
            with open(self.report_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                history = list(reader)
            
            return {'success': True, 'history': history}
        except Exception as e:
            logging.error(f"Error viewing history: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def generate_practice_questions(self, topic, weak_areas):
        """Generate additional practice questions for weak areas"""
        try:
            prompt = f"""Generate 5 practice questions for {topic}, focusing on these weak areas:

{', '.join(weak_areas)}

Format as:
Q: [question]
A: [answer]
HINT: [helpful hint]

Make questions progressively easier to build confidence."""
            
            response = self.model.generate_content(prompt)
            practice = response.text
            
            logging.info(f"Practice questions generated for {topic}")
            return {'success': True, 'practice': practice}
        except Exception as e:
            logging.error(f"Error generating practice questions: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_study_recommendations(self, quiz_results):
        """Get personalized study recommendations based on quiz performance"""
        try:
            incorrect = [r for r in quiz_results if not r['is_correct']]
            
            if not incorrect:
                return {
                    'success': True,
                    'recommendations': "Excellent! You've mastered this topic. Consider moving to advanced topics or helping others learn."
                }
            
            topics = [r['question'] for r in incorrect]
            
            prompt = f"""A student struggled with these questions:

{chr(10).join(f'- {q}' for q in topics)}

Provide:
1. Specific study strategies for these topics
2. Resources or methods to use
3. Practice recommendations
4. Timeline suggestion

Be practical and encouraging."""
            
            response = self.model.generate_content(prompt)
            recommendations = response.text
            
            return {'success': True, 'recommendations': recommendations}
        except Exception as e:
            logging.error(f"Error getting recommendations: {str(e)}")
            return {'success': False, 'message': str(e)}


def main():
    """CLI interface for testing"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    quiz_gen = QuizGeneratorAI(api_key)
    
    while True:
        print("\n" + "="*50)
        print("AI-POWERED QUIZ GENERATOR")
        print("="*50)
        print("1. Generate Quiz from Notes")
        print("2. Generate Quiz from Topic")
        print("3. Take Quiz")
        print("4. View Quiz History")
        print("5. Generate Practice Questions")
        print("6. Get Study Recommendations")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            topic = input("Enter topic (must have notes): ")
            num_q = int(input("Number of questions (default 5): ") or 5)
            difficulty = input("Difficulty (easy/medium/hard): ") or 'medium'
            quiz_type = input("Type (mcq/tf/short/mixed): ") or 'mixed'
            
            print("\nGenerating quiz...")
            result = quiz_gen.generate_quiz_from_notes(topic, num_q, difficulty, quiz_type)
            
            if result['success']:
                print(f"\n✅ Quiz generated: {len(result['questions'])} questions")
                
                # Save quiz for taking later
                with open('current_quiz.json', 'w') as f:
                    json.dump(result, f)
                print("Quiz saved! Use option 3 to take it.")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '2':
            topic = input("Enter topic: ")
            num_q = int(input("Number of questions (default 5): ") or 5)
            difficulty = input("Difficulty (easy/medium/hard): ") or 'medium'
            quiz_type = input("Type (mcq/tf/short/mixed): ") or 'mixed'
            
            print("\nGenerating quiz...")
            result = quiz_gen.generate_quiz_from_topic(topic, num_q, difficulty, quiz_type)
            
            if result['success']:
                print(f"\n✅ Quiz generated: {len(result['questions'])} questions")
                
                # Save quiz for taking later
                with open('current_quiz.json', 'w') as f:
                    json.dump(result, f)
                print("Quiz saved! Use option 3 to take it.")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '3':
            if not os.path.exists('current_quiz.json'):
                print("No quiz found! Generate one first.")
                continue
            
            with open('current_quiz.json', 'r') as f:
                quiz_data = json.load(f)
            
            questions = quiz_data['questions']
            user_answers = []
            
            print(f"\n📝 QUIZ: {quiz_data['topic']}")
            print(f"Difficulty: {quiz_data['difficulty']}")
            print(f"Questions: {len(questions)}\n")
            
            for i, q in enumerate(questions, 1):
                print(f"\nQ{i}. [{q.get('type', 'SHORT')}] {q['question']}")
                
                if q.get('options'):
                    for j, opt in enumerate(q['options'], 1):
                        print(f"   {j}. {opt}")
                
                answer = input("Your answer: ")
                user_answers.append(answer)
            
            print("\n📊 Evaluating your quiz...")
            result = quiz_gen.evaluate_quiz(questions, user_answers)
            
            if result['success']:
                print(f"\n{'='*50}")
                print(f"SCORE: {result['score']}/{result['total']} ({result['percentage']:.1f}%)")
                print(f"{'='*50}\n")
                
                for r in result['results']:
                    status = "✅" if r['is_correct'] else "❌"
                    print(f"{status} Q{r['question_num']}: {r['question']}")
                    print(f"   Your answer: {r['user_answer']}")
                    if not r['is_correct']:
                        print(f"   Correct answer: {r['correct_answer']}")
                    print(f"   Feedback: {r['feedback']}\n")
                
                print(f"📋 OVERALL FEEDBACK:\n{result['overall_feedback']}")
                
                # Save report
                quiz_gen.save_quiz_report(
                    quiz_data['topic'],
                    result['score'],
                    result['total'],
                    result['percentage'],
                    result['results']
                )
                
                # Offer study recommendations
                if result['percentage'] < 80:
                    print("\nWould you like study recommendations?")
                    if input("(y/n): ").lower() == 'y':
                        rec_result = quiz_gen.get_study_recommendations(result['results'])
                        if rec_result['success']:
                            print(f"\n💡 STUDY RECOMMENDATIONS:\n{rec_result['recommendations']}")
        
        elif choice == '4':
            result = quiz_gen.view_quiz_history()
            
            if result['success'] and result['history']:
                print(f"\n📊 QUIZ HISTORY:")
                for entry in result['history'][-10:]:  # Last 10
                    print(f"\n{entry['timestamp']} - {entry['topic']}")
                    print(f"Score: {entry['score']}/{entry['total']} ({entry['percentage']})")
            else:
                print("No quiz history found.")
        
        elif choice == '5':
            topic = input("Enter topic: ")
            weak_areas = input("Enter weak areas (comma-separated): ").split(',')
            weak_areas = [area.strip() for area in weak_areas]
            
            print("\nGenerating practice questions...")
            result = quiz_gen.generate_practice_questions(topic, weak_areas)
            
            if result['success']:
                print(f"\n📚 PRACTICE QUESTIONS:\n{result['practice']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '6':
            if not os.path.exists('current_quiz.json'):
                print("Take a quiz first to get recommendations!")
                continue
            
            print("\nThis requires quiz results. Take a quiz first (option 3).")
        
        elif choice == '0':
            print("Keep learning! Goodbye!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()