from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import os
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the model
model = None

def load_model():
    """Load the trained model from file"""
    global model
    model_path = 'heart_disease_model.pkl'
    
    try:
        if os.path.exists(model_path):
            loaded_data = joblib.load(model_path)
            
            # Check if it's a dictionary with model inside
            if isinstance(loaded_data, dict) and 'model' in loaded_data:
                model = loaded_data['model']
                logger.info(f"Model extracted from dictionary structure")
            else:
                model = loaded_data
                logger.info(f"Model loaded directly")
            
            logger.info(f"Model loaded successfully from {model_path}")
            logger.info(f"Model type: {type(model)}")
            return True
        else:
            # Try simple model file
            simple_model_path = 'heart_disease_model_simple.pkl'
            if os.path.exists(simple_model_path):
                model = joblib.load(simple_model_path)
                logger.info(f"Model loaded from simple file: {simple_model_path}")
                return True
            else:
                logger.error(f"Model file not found: {model_path}")
                return False
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def validate_input(data):
    """Validate input data"""
    required_fields = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate data types and ranges
    try:
        # Age validation
        age = int(data['age'])
        if not (1 <= age <= 120):
            return False, "Age must be between 1 and 120"
        
        # Sex validation (0 or 1)
        sex = int(data['sex'])
        if sex not in [0, 1]:
            return False, "Sex must be 0 (female) or 1 (male)"
        
        # Chest pain type validation (0-3)
        cp = int(data['cp'])
        if cp not in [0, 1, 2, 3]:
            return False, "Chest pain type must be 0, 1, 2, or 3"
        
        # Resting blood pressure validation
        trestbps = int(data['trestbps'])
        if not (80 <= trestbps <= 200):
            return False, "Resting blood pressure must be between 80 and 200"
        
        # Cholesterol validation
        chol = int(data['chol'])
        if not (100 <= chol <= 600):
            return False, "Cholesterol must be between 100 and 600"
        
        # Fasting blood sugar validation (0 or 1)
        fbs = int(data['fbs'])
        if fbs not in [0, 1]:
            return False, "Fasting blood sugar must be 0 or 1"
        
        # Resting ECG validation (0-2)
        restecg = int(data['restecg'])
        if restecg not in [0, 1, 2]:
            return False, "Resting ECG must be 0, 1, or 2"
        
        # Maximum heart rate validation
        thalach = int(data['thalach'])
        if not (60 <= thalach <= 220):
            return False, "Maximum heart rate must be between 60 and 220"
        
        # Exercise induced angina validation (0 or 1)
        exang = int(data['exang'])
        if exang not in [0, 1]:
            return False, "Exercise induced angina must be 0 or 1"
        
        # ST depression validation
        oldpeak = float(data['oldpeak'])
        if not (0 <= oldpeak <= 10):
            return False, "ST depression must be between 0 and 10"
        
        # Slope validation (0-2)
        slope = int(data['slope'])
        if slope not in [0, 1, 2]:
            return False, "Slope must be 0, 1, or 2"
        
        # Number of vessels validation (0-3)
        ca = int(data['ca'])
        if ca not in [0, 1, 2, 3]:
            return False, "Number of vessels must be 0, 1, 2, or 3"
        
        # Thalassemia validation (1-3)
        thal = int(data['thal'])
        if thal not in [1, 2, 3]:
            return False, "Thalassemia must be 1, 2, or 3"
        
        return True, "Valid input"
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid data type: {str(e)}"

def prepare_features(data):
    """Prepare features for model prediction"""
    # Order of features (adjust based on your model's expected input)
    feature_order = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    features = []
    for feature in feature_order:
        if feature == 'oldpeak':
            features.append(float(data[feature]))
        else:
            features.append(int(data[feature]))
    
    return np.array(features).reshape(1, -1)

# Routes for serving HTML templates
@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return f"Error: Could not load index.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/contact.html')
@app.route('/contact')
def contact():
    """Serve the contact page"""
    try:
        return render_template('contact.html')
    except Exception as e:
        logger.error(f"Error serving contact.html: {e}")
        return f"Error: Could not load contact.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/about.html')
@app.route('/about')
def about():
    """Serve the about page"""
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Error serving about.html: {e}")
        return f"Error: Could not load about.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/faq.html')
@app.route('/faq')
def faq():
    """Serve the FAQ page"""
    try:
        return render_template('faq.html')
    except Exception as e:
        logger.error(f"Error serving faq.html: {e}")
        return f"Error: Could not load faq.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/terms.html')
@app.route('/terms')
def terms():
    """Serve the terms page"""
    try:
        return render_template('terms.html')
    except Exception as e:
        logger.error(f"Error serving terms.html: {e}")
        return f"Error: Could not load terms.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/privacy.html')
@app.route('/privacy')
def privacy():
    """Serve the privacy page"""
    try:
        return render_template('privacy.html')
    except Exception as e:
        logger.error(f"Error serving privacy.html: {e}")
        return f"Error: Could not load privacy.html. Make sure it's in the templates folder. Error: {str(e)}", 500

@app.route('/predict', methods=['POST'])
def predict():
    """Predict heart disease risk"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Please ensure heart_disease_model.pkl exists.'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input data
        is_valid, message = validate_input(data)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Prepare features for prediction
        features = prepare_features(data)
        
        # Make prediction
        try:
            prediction = model.predict(features)[0]
            logger.info(f"Raw prediction: {prediction}")
        except AttributeError as e:
            logger.error(f"Model prediction error: {e}")
            logger.error(f"Model type: {type(model)}")
            return jsonify({
                'error': 'Model prediction failed. Please retrain the model.',
                'details': 'Model object does not have predict method'
            }), 500
        
        # Get prediction probability if available
        prediction_proba = None
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features)[0]
                prediction_proba = float(max(proba))
                logger.info(f"Prediction probabilities: {proba}")
        except Exception as e:
            logger.warning(f"Could not get prediction probabilities: {e}")
            prediction_proba = None
        
        # Convert prediction to readable format
        risk_status = "Risk" if prediction == 1 else "No Risk"
        
        # Prepare response
        response = {
            'prediction': risk_status,
            'prediction_value': int(prediction),
            'confidence': prediction_proba,
            'status': 'success'
        }
        
        logger.info(f"Prediction made: {risk_status} (confidence: {prediction_proba})")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': 'An error occurred during prediction',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    
    # Check if templates exist
    template_files = ['index.html', 'contact.html', 'about.html', 'faq.html', 'terms.html', 'privacy.html']
    templates_status = {}
    
    for template in template_files:
        template_path = os.path.join('templates', template)
        templates_status[template] = os.path.exists(template_path)
    
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'templates_status': templates_status
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load the model on startup
    model_loaded = load_model()
    
    # Check if templates exist
    template_files = ['index.html', 'contact.html', 'about.html', 'faq.html', 'terms.html', 'privacy.html']
    missing_templates = []
    
    for template in template_files:
        template_path = os.path.join('templates', template)
        if not os.path.exists(template_path):
            missing_templates.append(template)
    
    print("\n" + "="*60)
    print("🚀 CardioPredict Flask Server Starting...")
    print("="*60)
    
    if not model_loaded:
        print("⚠️  WARNING: Model file 'heart_disease_model.pkl' not found!")
        print("   /predict endpoint will not work until model is available.")
    else:
        print("✅ Model loaded successfully!")
    
    if missing_templates:
        print(f"⚠️  WARNING: Missing template files: {', '.join(missing_templates)}")
        print("   Make sure all HTML files are in the templates/ folder.")
    else:
        print("✅ All template files found!")
    
    print(f"🌐 Access your website at: http://localhost:5000")
    print(f"🔍 Health check at: http://localhost:5000/health")
    print("="*60 + "\n")
    
    # Start the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)