"""
Model Fix Script
This script checks and fixes the model loading issue
"""

import joblib
import os

def check_and_fix_model():
    """Check the current model and fix if needed"""
    
    print("🔍 Checking heart disease model...")
    
    model_files = [
        'heart_disease_model.pkl',
        'heart_disease_model_simple.pkl'
    ]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"\n📄 Checking: {model_file}")
            
            try:
                loaded_data = joblib.load(model_file)
                print(f"✅ File loaded successfully")
                print(f"📊 Data type: {type(loaded_data)}")
                
                if isinstance(loaded_data, dict):
                    print(f"📋 Dictionary keys: {list(loaded_data.keys())}")
                    
                    if 'model' in loaded_data:
                        actual_model = loaded_data['model']
                        print(f"🤖 Model type: {type(actual_model)}")
                        
                        # Test if model has predict method
                        if hasattr(actual_model, 'predict'):
                            print(f"✅ Model has predict method")
                            
                            # Save the extracted model as the main model
                            joblib.dump(actual_model, 'heart_disease_model_fixed.pkl')
                            print(f"✅ Fixed model saved as: heart_disease_model_fixed.pkl")
                            
                            return actual_model
                        else:
                            print(f"❌ Model object doesn't have predict method")
                else:
                    # Direct model object
                    if hasattr(loaded_data, 'predict'):
                        print(f"✅ Direct model object with predict method")
                        return loaded_data
                    else:
                        print(f"❌ Object doesn't have predict method")
                        
            except Exception as e:
                print(f"❌ Error loading {model_file}: {e}")
    
    print(f"\n❌ No working model found")
    return None

def test_model_prediction(model):
    """Test the model with sample data"""
    
    print(f"\n🧪 Testing model prediction...")
    
    # Sample test data (matching the expected features)
    sample_data = [
        63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1
    ]
    
    try:
        import numpy as np
        features = np.array(sample_data).reshape(1, -1)
        
        # Test prediction
        prediction = model.predict(features)[0]
        print(f"✅ Prediction test successful: {prediction}")
        
        # Test probability if available
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features)[0]
            print(f"✅ Probability test successful: {proba}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False

def main():
    """Main function"""
    
    print("🫀 Heart Disease Model Fix")
    print("=" * 40)
    
    # Check and fix model
    model = check_and_fix_model()
    
    if model:
        # Test the model
        if test_model_prediction(model):
            print(f"\n🎉 Model is working correctly!")
            
            # Update the Flask app to use the fixed model
            print(f"\n🔧 To use the fixed model:")
            print(f"1. Stop the Flask server (Ctrl+C)")
            print(f"2. Rename or remove the old model file")
            print(f"3. Rename 'heart_disease_model_fixed.pkl' to 'heart_disease_model.pkl'")
            print(f"4. Restart the Flask server: python app.py")
            
        else:
            print(f"\n❌ Model test failed - you may need to retrain")
            print(f"💡 Try running: python train_model.py")
    else:
        print(f"\n❌ No working model found")
        print(f"💡 Please run: python train_model.py")

if __name__ == "__main__":
    main()
    