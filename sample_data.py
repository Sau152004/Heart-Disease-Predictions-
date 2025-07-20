"""
Generate sample heart disease data for testing
This creates a realistic sample dataset that matches the expected format
"""

import pandas as pd
import numpy as np

def generate_sample_data(n_samples=300):
    """Generate sample heart disease data"""
    
    np.random.seed(42)  # For reproducible results
    
    print(f"🔬 Generating {n_samples} sample records...")
    
    data = []
    
    for i in range(n_samples):
        # Generate realistic medical data
        age = np.random.randint(29, 80)
        sex = np.random.choice([0, 1])  # 0=female, 1=male
        cp = np.random.choice([0, 1, 2, 3])  # chest pain type
        
        # More realistic ranges based on medical standards
        trestbps = np.random.randint(94, 200)  # resting blood pressure
        chol = np.random.randint(126, 564)     # cholesterol
        fbs = np.random.choice([0, 1], p=[0.85, 0.15])  # fasting blood sugar
        restecg = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])  # resting ecg
        thalach = np.random.randint(71, 202)   # max heart rate
        exang = np.random.choice([0, 1])       # exercise induced angina
        oldpeak = round(np.random.uniform(0, 6.2), 1)  # ST depression
        slope = np.random.choice([0, 1, 2])    # slope of peak exercise ST
        ca = np.random.choice([0, 1, 2, 3])    # number of major vessels
        thal = np.random.choice([1, 2, 3])     # thalassemia
        
        # Generate target based on risk factors (simplified logic)
        risk_score = 0
        
        # Age factor
        if age > 55:
            risk_score += 1
        
        # Gender factor (males higher risk)
        if sex == 1:
            risk_score += 1
        
        # Blood pressure
        if trestbps > 140:
            risk_score += 1
        
        # Cholesterol
        if chol > 240:
            risk_score += 1
        
        # Exercise angina
        if exang == 1:
            risk_score += 2
        
        # ST depression
        if oldpeak > 2.0:
            risk_score += 1
        
        # Major vessels
        if ca > 0:
            risk_score += ca
        
        # Add some randomness
        risk_score += np.random.choice([-1, 0, 1])
        
        # Convert to binary target
        target = 1 if risk_score >= 4 else 0
        
        data.append([
            age, sex, cp, trestbps, chol, fbs, restecg, 
            thalach, exang, oldpeak, slope, ca, thal, target
        ])
    
    # Create DataFrame
    columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    print("✅ Sample data generated!")
    print(f"📊 Shape: {df.shape}")
    print(f"🎯 Target distribution:")
    print(df['target'].value_counts())
    
    return df

def save_sample_data(df, filename='sample_heart_data.csv'):
    """Save the sample data to CSV"""
    
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Sample data saved to: {filename}")
        
        # Display first few rows
        print(f"\n📄 First 5 rows of {filename}:")
        print(df.head())
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def main():
    """Main function"""
    print("🫀 Heart Disease Sample Data Generator")
    print("=" * 50)
    
    # Ask user for number of samples
    try:
        n = input("Enter number of samples to generate (default 300): ").strip()
        n_samples = int(n) if n else 300
    except ValueError:
        n_samples = 300
    
    # Generate data
    df = generate_sample_data(n_samples)
    
    # Save data
    filename = input("Enter filename (default 'sample_heart_data.csv'): ").strip()
    if not filename:
        filename = 'sample_heart_data.csv'
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    success = save_sample_data(df, filename)
    
    if success:
        print(f"\n🎉 Sample data ready!")
        print(f"\nNext steps:")
        print(f"1. Use this file for testing: python train_model.py")
        print(f"2. When prompted, enter: {filename}")
        print(f"3. Or rename it to 'heart.csv' for default use")
        
        # Show data statistics
        print(f"\n📈 Data Statistics:")
        print(f"Age range: {df['age'].min()}-{df['age'].max()}")
        print(f"Male/Female ratio: {df['sex'].value_counts().to_dict()}")
        print(f"Heart disease cases: {df['target'].sum()}/{len(df)} ({df['target'].mean()*100:.1f}%)")

if __name__ == "__main__":
    main()