"""
AI-Powered Drive Manager with File Upload and Link Management
Features: Upload files, add links, organize by semester/degree/subject, cloud storage
"""

import os
import json
import logging
from datetime import datetime
from urllib.parse import urlparse
import webbrowser
import google.generativeai as genai
import cloudinary
import cloudinary.uploader
import cloudinary.api
import re

# Configure logging
logging.basicConfig(
    filename="drive_manager.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DriveManagerAI:
    def __init__(self, gemini_api_key, cloudinary_config=None):
        """Initialize Drive Manager with AI and cloud storage"""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configure Cloudinary
        if cloudinary_config and all(cloudinary_config.values()):
            cloudinary.config(**cloudinary_config)
            self.cloudinary_enabled = True
        else:
            self.cloudinary_enabled = False
        
        self.database_file = 'drive_database.json'
        self.local_storage = 'drive_files'
        os.makedirs(self.local_storage, exist_ok=True)
        
        # Predefined Google Drive links
        self.predefined_links = self._load_predefined_links()
    
    def _load_predefined_links(self):
        """Load predefined course material links"""
        return {
            1: {
                'pf': 'https://drive.google.com/drive/folders/1WFbB33MDYV9ooz92zr1_bffhEb8Pye1_',
                'ict': 'https://drive.google.com/drive/folders/1yPk8VZbbB731S27JjBArGthtsJ89CiRS'
            },
            2: {
                'oop': 'https://drive.google.com/drive/folders/1hgH7wC7H6if9s-95wpKbHiTfVpWOfdBw'
            },
            3: {
                'dsa': 'https://drive.google.com/drive/folders/1deuPO-sxgbUugS4eAxzm3JTabK_95Qzj',
                'coal': 'https://drive.google.com/drive/folders/1ctNd4IFdayaaM1yQgV90z9lqgAJKjr3s',
                'ds': 'https://drive.google.com/drive/folders/1XPMNyqYL6QFVDlDgTiepx9HkiqcNtTRx'
            },
            4: {
                'db': 'https://drive.google.com/drive/folders/13zs9uv5t0L33gaxPRPEx4aDqhJpkWPFn',
                'os': 'https://drive.google.com/drive/folders/1XU_aEyVGhvWx5VFB8erMym_BICPbiy31'
            }
        }
    
    def _load_database(self):
        """Load file database"""
        if os.path.exists(self.database_file):
            try:
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logging.error("Database file corrupted, creating new one")
                return {}
        return {}
    
    def _save_database(self, data):
        """Save file database"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving database: {str(e)}")
            raise
    
    def upload_file(self, file_path, semester, degree, subject, description='', use_cloud=True):
        """Upload file to cloud or local storage"""
        try:
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                return {'success': False, 'message': 'File not found'}
            
            filename = os.path.basename(file_path)
            db = self._load_database()
            file_id = str(len(db) + 1)

            # Sanitize names to make them Cloudinary-safe
            # Remove all special characters and spaces, replace with underscore
            safe_semester = re.sub(r'[^a-zA-Z0-9]', '_', str(semester))
            safe_degree = re.sub(r'[^a-zA-Z0-9]', '_', degree)
            safe_subject = re.sub(r'[^a-zA-Z0-9]', '_', subject)
            safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', os.path.splitext(filename)[0])
            
            # Remove consecutive underscores and trim
            safe_semester = re.sub(r'_+', '_', safe_semester).strip('_')
            safe_degree = re.sub(r'_+', '_', safe_degree).strip('_')
            safe_subject = re.sub(r'_+', '_', safe_subject).strip('_')
            safe_filename = re.sub(r'_+', '_', safe_filename).strip('_')
            
            folder_path = f"student_ai/{safe_semester}/{safe_degree}/{safe_subject}"
            
            logging.info(f"Attempting upload: {filename}, Folder: {folder_path}, Public ID: {safe_filename}")

            if use_cloud and self.cloudinary_enabled:
                # Upload to Cloudinary
                logging.info(f"Uploading to Cloudinary: {folder_path}/{safe_filename}")
                upload_result = cloudinary.uploader.upload(
                    file_path,
                    resource_type="auto",
                    folder=folder_path,
                    public_id=safe_filename,
                    overwrite=True,
                    use_filename=False
                )

                file_url = upload_result['secure_url']
                file_size = upload_result.get('bytes', 0)
                file_type = upload_result.get('format', 'unknown')
                logging.info(f"Cloudinary upload successful: {file_url}")

            else:
                # Store locally
                logging.info(f"Storing locally for {degree}/{subject}")
                local_folder = os.path.join(
                    self.local_storage,
                    str(semester),
                    degree,
                    subject
                )
                os.makedirs(local_folder, exist_ok=True)
                local_path = os.path.join(local_folder, filename)

                import shutil
                shutil.copy2(file_path, local_path)

                file_url = local_path
                file_size = os.path.getsize(local_path)
                file_type = os.path.splitext(filename)[1][1:] or 'unknown'
                logging.info(f"Local storage successful: {local_path}")

            # Save metadata
            db[file_id] = {
                'filename': filename,
                'url': file_url,
                'semester': int(semester),
                'degree': degree.upper(),
                'subject': subject.upper(),
                'description': description,
                'uploaded_at': datetime.now().isoformat(),
                'file_type': file_type,
                'size': file_size,
                'is_cloud': use_cloud and self.cloudinary_enabled,
                'is_external': False
            }
            self._save_database(db)

            logging.info(f"File uploaded: {filename} for {degree} {subject}")
            return {
                'success': True,
                'message': 'File uploaded successfully!',
                'file_id': file_id,
                'url': file_url
            }

        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def add_link(self, link, semester, degree, subject, filename='', description=''):
        """Add external link to database"""
        try:
            # Validate URL
            parsed = urlparse(link)
            if not parsed.scheme or not parsed.netloc:
                return {'success': False, 'message': 'Invalid URL'}
            
            if not filename:
                filename = f"{subject.upper()} - External Resource"
            
            db = self._load_database()
            file_id = str(len(db) + 1)
            
            db[file_id] = {
                'filename': filename,
                'url': link,
                'semester': int(semester),
                'degree': degree.upper(),
                'subject': subject.upper(),
                'description': description,
                'added_at': datetime.now().isoformat(),
                'file_type': 'link',
                'size': 0,
                'is_external': True,
                'is_cloud': False
            }
            self._save_database(db)
            
            logging.info(f"Link added: {link} for {degree} {subject}")
            return {
                'success': True,
                'message': 'Link added successfully!',
                'file_id': file_id
            }
        except Exception as e:
            logging.error(f"Error adding link: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def list_files(self, semester=None, degree=None, subject=None):
        """List files with optional filters"""
        try:
            db = self._load_database()
            filtered_files = []
            
            for file_id, file_data in db.items():
                matches = True
                if semester and int(file_data.get('semester', 0)) != int(semester):
                    matches = False
                if degree and file_data.get('degree', '').upper() != degree.upper():
                    matches = False
                if subject and file_data.get('subject', '').upper() != subject.upper():
                    matches = False
                
                if matches:
                    filtered_files.append({
                        'id': file_id,
                        **file_data
                    })
            
            return {'success': True, 'files': filtered_files}
        except Exception as e:
            logging.error(f"Error listing files: {str(e)}")
            return {'success': False, 'message': str(e), 'files': []}
    
    def delete_file(self, file_id):
        """Delete file from storage and database"""
        try:
            db = self._load_database()
            
            if file_id not in db:
                return {'success': False, 'message': 'File not found'}
            
            file_data = db[file_id]
            
            # Delete from cloud storage if applicable
            if file_data.get('is_cloud') and not file_data.get('is_external'):
                try:
                    # Extract public_id from URL
                    url_parts = file_data['url'].split('/')
                    public_id_with_ext = '/'.join(url_parts[url_parts.index('upload') + 2:])
                    public_id = os.path.splitext(public_id_with_ext)[0]
                    cloudinary.uploader.destroy(public_id, resource_type="raw")
                except Exception as e:
                    logging.warning(f"Could not delete from cloud: {str(e)}")
            
            # Delete local file if applicable
            elif not file_data.get('is_external'):
                try:
                    if os.path.exists(file_data['url']):
                        os.remove(file_data['url'])
                except Exception as e:
                    logging.warning(f"Could not delete local file: {str(e)}")
            
            # Remove from database
            del db[file_id]
            self._save_database(db)
            
            logging.info(f"File deleted: {file_id}")
            return {'success': True, 'message': 'File deleted successfully!'}
        except Exception as e:
            logging.error(f"Error deleting file: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_predefined_link(self, semester, subject):
        """Get predefined Google Drive link"""
        try:
            semester = int(semester)
            subject = subject.lower()
            
            if semester in self.predefined_links:
                if subject in self.predefined_links[semester]:
                    link = self.predefined_links[semester][subject]
                    return {'success': True, 'link': link}
            
            return {'success': False, 'message': 'No predefined link found'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_file_info(self, file_id):
        """Get file information"""
        try:
            db = self._load_database()
            
            if file_id not in db:
                return {'success': False, 'message': 'File not found'}
            
            file_data = db[file_id]
            return {
                'success': True,
                'file': {
                    'id': file_id,
                    **file_data
                }
            }
        except Exception as e:
            logging.error(f"Error getting file info: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_file_path(self, file_id):
        """Get local file path if file is stored locally"""
        try:
            db = self._load_database()
            
            if file_id not in db:
                return None
            
            file_data = db[file_id]
            
            # Only return path for local files
            if not file_data.get('is_cloud') and not file_data.get('is_external'):
                file_path = file_data['url']
                if os.path.exists(file_path):
                    return file_path
            
            return None
        except Exception as e:
            logging.error(f"Error getting file path: {str(e)}")
            return None
    
    def open_file(self, file_id):
        """Open file in default application or browser"""
        try:
            db = self._load_database()
            
            if file_id not in db:
                return {'success': False, 'message': 'File not found'}
            
            file_data = db[file_id]
            
            # Return URL for cloud files and external links (frontend will open in new tab)
            if file_data.get('is_cloud') or file_data.get('is_external'):
                return {
                    'success': True, 
                    'message': 'Opening file...',
                    'url': file_data['url'],
                    'is_external': True
                }
            else:
                # For local files, return file ID (frontend will request download)
                if os.path.exists(file_data['url']):
                    return {
                        'success': True,
                        'message': 'Opening file...',
                        'file_id': file_id,
                        'is_external': False
                    }
                else:
                    return {'success': False, 'message': 'Local file not found'}
            
        except Exception as e:
            logging.error(f"Error opening file: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def search_files(self, query):
        """Search files by filename or description"""
        try:
            db = self._load_database()
            results = []
            
            query = query.lower()
            for file_id, file_data in db.items():
                if (query in file_data.get('filename', '').lower() or
                    query in file_data.get('description', '').lower() or
                    query in file_data.get('subject', '').lower() or
                    query in file_data.get('degree', '').lower()):
                    results.append({
                        'id': file_id,
                        **file_data
                    })
            
            return {'success': True, 'files': results}
        except Exception as e:
            logging.error(f"Error searching files: {str(e)}")
            return {'success': False, 'message': str(e), 'files': []}
    
    def get_ai_study_plan(self, semester, degree, subjects):
        """Generate study plan using AI"""
        try:
            prompt = f"""Create a study plan for a {degree} student in semester {semester}.

Subjects: {', '.join(subjects)}

Provide:
1. Weekly study schedule
2. Topic prioritization for each subject
3. Study techniques for each subject type
4. Time management tips
5. Resource recommendations

Keep it practical and actionable."""
            
            response = self.model.generate_content(prompt)
            study_plan = response.text
            
            logging.info(f"Study plan generated for {degree} semester {semester}")
            return {'success': True, 'study_plan': study_plan}
        except Exception as e:
            logging.error(f"Error generating study plan: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def analyze_file_with_ai(self, file_id):
        """Analyze file content using AI (for text files)"""
        try:
            db = self._load_database()
            
            if file_id not in db:
                return {'success': False, 'message': 'File not found'}
            
            file_data = db[file_id]
            
            # Read file content (only for text files)
            if file_data.get('is_external'):
                return {'success': False, 'message': 'Cannot analyze external links'}
            
            if file_data.get('is_cloud'):
                return {'success': False, 'message': 'Cannot analyze cloud files directly. Download first.'}
            
            file_path = file_data['url']
            if not os.path.exists(file_path):
                return {'success': False, 'message': 'File not found locally'}
            
            # Read content based on file type
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                return {'success': False, 'message': 'Cannot read file (not a text file or encoding issue)'}
            except Exception as e:
                return {'success': False, 'message': f'Error reading file: {str(e)}'}
            
            # Limit content to avoid token limits
            content_preview = content[:3000] if len(content) > 3000 else content
            
            prompt = f"""Analyze this study material for {file_data['subject']}:

{content_preview}

Provide:
1. Main topics covered
2. Key concepts to focus on
3. Difficulty level assessment
4. Study recommendations
5. Related topics to explore"""
            
            response = self.model.generate_content(prompt)
            analysis = response.text
            
            logging.info(f"File analyzed: {file_id}")
            return {'success': True, 'analysis': analysis}
        except Exception as e:
            logging.error(f"Error analyzing file: {str(e)}")
            return {'success': False, 'message': str(e)}


def main():
    """CLI interface for testing"""
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    # Cloudinary config (optional)
    cloudinary_config = {
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
        'api_key': os.getenv('CLOUDINARY_API_KEY', ''),
        'api_secret': os.getenv('CLOUDINARY_API_SECRET', '')
    }
    
    drive_manager = DriveManagerAI(api_key, cloudinary_config)
    
    while True:
        print("\n" + "="*50)
        print("AI-POWERED DRIVE MANAGER")
        print("="*50)
        print("1. Upload File")
        print("2. Add External Link")
        print("3. List Files")
        print("4. Search Files")
        print("5. Open File")
        print("6. Delete File")
        print("7. Get Predefined Course Link")
        print("8. Generate Study Plan (AI)")
        print("9. Analyze File (AI)")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            file_path = input("Enter file path: ")
            semester = input("Enter semester (1-8): ")
            degree = input("Enter degree (CS/SE/AI/EE): ")
            subject = input("Enter subject code: ")
            description = input("Enter description: ")
            use_cloud = input("Upload to cloud? (y/n): ").lower() == 'y'
            
            result = drive_manager.upload_file(
                file_path, semester, degree, subject, description, use_cloud
            )
            print(f"\n{result['message']}")
            if result['success']:
                print(f"File URL: {result['url']}")
        
        elif choice == '2':
            link = input("Enter link URL: ")
            semester = input("Enter semester (1-8): ")
            degree = input("Enter degree (CS/SE/AI/EE): ")
            subject = input("Enter subject code: ")
            filename = input("Enter filename (optional): ")
            description = input("Enter description: ")
            
            result = drive_manager.add_link(
                link, semester, degree, subject, filename, description
            )
            print(f"\n{result['message']}")
        
        elif choice == '3':
            semester = input("Filter by semester (press Enter to skip): ")
            degree = input("Filter by degree (press Enter to skip): ")
            subject = input("Filter by subject (press Enter to skip): ")
            
            result = drive_manager.list_files(
                semester if semester else None,
                degree if degree else None,
                subject if subject else None
            )
            
            if result['success'] and result['files']:
                print(f"\nFound {len(result['files'])} file(s):")
                for file in result['files']:
                    print(f"\nID: {file['id']}")
                    print(f"Name: {file['filename']}")
                    print(f"Subject: {file['subject']}")
                    print(f"Type: {file['file_type']}")
                    print(f"URL: {file['url'][:50]}...")
            else:
                print("No files found.")
        
        elif choice == '4':
            query = input("Enter search query: ")
            result = drive_manager.search_files(query)
            
            if result['success'] and result['files']:
                print(f"\nFound {len(result['files'])} file(s):")
                for file in result['files']:
                    print(f"\nID: {file['id']}")
                    print(f"Name: {file['filename']}")
                    print(f"Subject: {file['subject']}")
            else:
                print("No files found.")
        
        elif choice == '5':
            file_id = input("Enter file ID to open: ")
            result = drive_manager.open_file(file_id)
            print(f"\n{result['message']}")
        
        elif choice == '6':
            file_id = input("Enter file ID to delete: ")
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == 'y':
                result = drive_manager.delete_file(file_id)
                print(f"\n{result['message']}")
        
        elif choice == '7':
            semester = input("Enter semester (1-4): ")
            subject = input("Enter subject code (e.g., pf, oop, dsa): ")
            result = drive_manager.get_predefined_link(semester, subject)
            
            if result['success']:
                print(f"\nLink: {result['link']}")
                open_it = input("Open in browser? (y/n): ")
                if open_it.lower() == 'y':
                    webbrowser.open(result['link'])
            else:
                print(f"\n{result['message']}")
        
        elif choice == '8':
            semester = input("Enter semester: ")
            degree = input("Enter degree: ")
            subjects = input("Enter subjects (comma-separated): ").split(',')
            subjects = [s.strip() for s in subjects]
            
            print("\nGenerating study plan...")
            result = drive_manager.get_ai_study_plan(semester, degree, subjects)
            
            if result['success']:
                print(f"\n📚 STUDY PLAN:\n{result['study_plan']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '9':
            file_id = input("Enter file ID to analyze: ")
            print("\nAnalyzing file...")
            result = drive_manager.analyze_file_with_ai(file_id)
            
            if result['success']:
                print(f"\n🔍 ANALYSIS:\n{result['analysis']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == '0':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
