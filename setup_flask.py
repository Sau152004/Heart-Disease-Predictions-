"""
Flask Project Setup Script
This script organizes files into the correct Flask structure
"""

import os
import shutil

def create_flask_structure():
    """Create the proper Flask directory structure"""
    
    print("🔧 Setting up Flask project structure...")
    
    # Create directories
    directories = ['templates', 'static']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}/")
        else:
            print(f"📁 Directory already exists: {directory}/")
    
    # File movements
    file_moves = [
        ('index.html', 'templates/index.html'),
        ('style.css', 'static/style.css'),
        ('script.js', 'static/script.js')
    ]
    
    for source, destination in file_moves:
        if os.path.exists(source):
            try:
                # Create destination directory if it doesn't exist
                dest_dir = os.path.dirname(destination)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                # Move file
                shutil.move(source, destination)
                print(f"✅ Moved: {source} → {destination}")
                
            except Exception as e:
                print(f"❌ Error moving {source}: {e}")
        else:
            print(f"⚠️  File not found: {source}")
    
    print("\n📁 Final project structure:")
    print_directory_tree()

def print_directory_tree():
    """Print the current directory structure"""
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
            
        items = []
        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            return
        
        for i, item in enumerate(items):
            if item.startswith('.'):
                continue
                
            item_path = os.path.join(directory, item)
            is_last = i == len(items) - 1
            
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item}")
            
            if os.path.isdir(item_path) and current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(item_path, next_prefix, max_depth, current_depth + 1)
    
    print("heart-disease-prediction/")
    print_tree(".", max_depth=2)

def update_html_references():
    """Update HTML file to reference static files correctly"""
    
    templates_index = 'templates/index.html'
    
    if os.path.exists(templates_index):
        print(f"\n🔄 Updating file references in {templates_index}...")
        
        try:
            with open(templates_index, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update CSS and JS references
            content = content.replace('href="style.css"', 'href="{{ url_for(\'static\', filename=\'style.css\') }}"')
            content = content.replace('src="script.js"', 'src="{{ url_for(\'static\', filename=\'script.js\') }}"')
            
            with open(templates_index, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated file references to use Flask static URL routing")
            
        except Exception as e:
            print(f"❌ Error updating HTML file: {e}")
    else:
        print(f"⚠️  Template file not found: {templates_index}")

def check_required_files():
    """Check if all required files exist"""
    
    print("\n🔍 Checking required files...")
    
    required_files = [
        ('templates/index.html', 'Main HTML template'),
        ('static/style.css', 'CSS styles'),
        ('static/script.js', 'JavaScript code'),
        ('app.py', 'Flask application'),
        ('heart_disease_model.pkl', 'Trained ML model')
    ]
    
    all_present = True
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path:<25} ({size:,} bytes) - {description}")
        else:
            print(f"❌ {file_path:<25} MISSING - {description}")
            all_present = False
    
    return all_present

def main():
    """Main setup function"""
    
    print("🫀 Heart Disease Prediction - Flask Setup")
    print("=" * 50)
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"📍 Current directory: {current_dir}")
    
    # Create Flask structure
    create_flask_structure()
    
    # Update HTML references
    update_html_references()
    
    # Check if everything is ready
    all_ready = check_required_files()
    
    print("\n" + "=" * 50)
    
    if all_ready:
        print("🎉 Setup completed successfully!")
        print("\n🚀 Next steps:")
        print("1. Stop the current Flask server (Ctrl+C)")
        print("2. Restart the server: python app.py")
        print("3. Open browser to: http://localhost:5000")
        print("4. Enjoy your heart disease prediction website! 🫀")
    else:
        print("⚠️  Setup incomplete - some files are missing")
        print("Please ensure all required files are present and try again")

if __name__ == "__main__":
    main()