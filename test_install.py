"""
Quick test script to verify all required packages are installed correctly
"""

def test_imports():
    """Test if all required packages can be imported"""
    
    packages = [
        ('flask', 'Flask web framework'),
        ('flask_cors', 'Flask CORS extension'),
        ('pandas', 'Data manipulation library'),
        ('numpy', 'Numerical computing library'),
        ('sklearn', 'Machine learning library'),
        ('joblib', 'Model serialization library'),
        ('matplotlib', 'Plotting library'),
        ('seaborn', 'Statistical visualization library')
    ]
    
    print("🔍 Testing package imports...")
    print("=" * 50)
    
    all_good = True
    
    for package, description in packages:
        try:
            if package == 'sklearn':
                import sklearn
                version = sklearn.__version__
            elif package == 'flask_cors':
                import flask_cors
                version = getattr(flask_cors, '__version__', 'Unknown')
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'Unknown')
            
            print(f"✅ {package:<15} v{version:<10} - {description}")
            
        except ImportError as e:
            print(f"❌ {package:<15} MISSING    - {description}")
            print(f"   Error: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {package:<15} ERROR      - {description}")
            print(f"   Error: {e}")
    
    print("=" * 50)
    
    if all_good:
        print("🎉 All packages installed successfully!")
        print("✅ You can now run: python train_model.py")
        return True
    else:
        print("❌ Some packages are missing. Please install them first.")
        print("💡 Try: pip install flask flask-cors scikit-learn pandas numpy joblib matplotlib seaborn")
        return False

def test_basic_functionality():
    """Test basic functionality of key packages"""
    
    try:
        print("\n🧪 Testing basic functionality...")
        
        # Test pandas
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        print("✅ Pandas: DataFrame creation works")
        
        # Test numpy
        import numpy as np
        arr = np.array([1, 2, 3])
        print("✅ NumPy: Array creation works")
        
        # Test sklearn
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10)
        print("✅ Scikit-learn: Model creation works")
        
        # Test flask
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask: App creation works")
        
        print("🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("🫀 Heart Disease Prediction - Installation Test")
    print("=" * 60)
    
    imports_ok = test_imports()
    
    if imports_ok:
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🚀 Everything looks good! You're ready to proceed.")
            print("\nNext steps:")
            print("1. Place your heart disease CSV file in this directory")
            print("2. Run: python train_model.py")
            print("3. Run: python app.py")
            print("4. Open browser to: http://localhost:5000")
        else:
            print("\n⚠️  Installation verification failed. Please reinstall packages.")
    else:
        print("\n❌ Please install missing packages before proceeding.")
        
    input("\nPress Enter to exit...")