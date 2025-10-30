"""
Setup Script for Student AI Assistant
Automates initial setup and configuration
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("  STUDENT AI ASSISTANT - SETUP SCRIPT")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    directories = [
        'uploads',
        'drive_files',
        'notes',
        'static/css',
        'static/js',
        'static/images',
        'templates',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\nSetting up environment variables...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping...")
        return
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
        print("\n⚠️  IMPORTANT: Edit .env file and add your API keys!")
        print("   Required: GEMINI_API_KEY")
        print("   Optional: CLOUDINARY credentials")
    else:
        print("❌ .env.example not found")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    print("This may take a few minutes...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("   Try manually: pip install -r requirements.txt")
        return False

def create_test_data():
    """Create sample data for testing"""
    print("\nCreating test data...")
    
    # Create a sample note
    sample_note = """# Welcome to Student AI Assistant!

This is a sample note to help you get started.

## Features:
- AI-powered note enhancement
- Smart summarization
- Quiz generation from notes
- And much more!

Try editing this note or create a new one!
"""
    
    with open('Sample_Topic_notes.txt', 'w', encoding='utf-8') as f:
        f.write(f"{os.popen('date').read().strip()} - {sample_note}\n")
    
    print("✅ Sample note created")

def verify_setup():
    """Verify the setup"""
    print("\nVerifying setup...")
    
    checks = {
        'requirements.txt': os.path.exists('requirements.txt'),
        'app.py': os.path.exists('app.py'),
        'notes_ai.py': os.path.exists('notes_ai.py'),
        'drive_manager_ai.py': os.path.exists('drive_manager_ai.py'),
        'health_tracker_ai.py': os.path.exists('health_tracker_ai.py'),
        'quiz_generator_ai.py': os.path.exists('quiz_generator_ai.py'),
        'search_engine_ai.py': os.path.exists('search_engine_ai.py'),
        '.env': os.path.exists('.env'),
        'uploads/': os.path.isdir('uploads'),
        'templates/': os.path.isdir('templates')
    }
    
    all_good = True
    for item, exists in checks.items():
        status = "✅" if exists else "❌"
        print(f"{status} {item}")
        if not exists:
            all_good = False
    
    return all_good

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "=" * 60)
    print("  SETUP COMPLETE!")
    print("=" * 60)
    print("\n📝 NEXT STEPS:")
    print("\n1. Get your Gemini API Key:")
    print("   → Visit: https://makersuite.google.com/app/apikey")
    print("   → Sign in with Google account")
    print("   → Click 'Create API Key'")
    print("   → Copy the key")
    
    print("\n2. Edit the .env file:")
    print("   → Open .env in a text editor")
    print("   → Replace 'your_gemini_api_key_here' with your actual key")
    print("   → Save the file")
    
    print("\n3. (Optional) Set up Cloudinary for file uploads:")
    print("   → Sign up at: https://cloudinary.com/")
    print("   → Get your credentials from dashboard")
    print("   → Add to .env file")
    
    print("\n4. Run the application:")
    print("   → Command: python app.py")
    print("   → Open browser: http://localhost:5000")
    
    print("\n5. Test individual modules (optional):")
    print("   → python notes_ai.py")
    print("   → python quiz_generator_ai.py")
    print("   → etc.")
    
    print("\n💡 TIPS:")
    print("   - Check README.md for detailed documentation")
    print("   - View logs in *.log files if errors occur")
    print("   - Use debug mode during development")
    
    print("\n🎓 Happy studying with AI!")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Create .env file
    create_env_file()
    
    # Step 4: Install dependencies
    print("\nDo you want to install dependencies now?")
    install = input("This will run: pip install -r requirements.txt (y/n): ")
    if install.lower() == 'y':
        if not install_dependencies():
            print("\n⚠️  Continue with manual dependency installation")
    else:
        print("⚠️  Remember to run: pip install -r requirements.txt")
    
    # Step 5: Create test data
    create_test_data()
    
    # Step 6: Verify setup
    if verify_setup():
        print("\n✅ All checks passed!")
    else:
        print("\n⚠️  Some files are missing. Please check.")
    
    # Step 7: Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        sys.exit(1)
