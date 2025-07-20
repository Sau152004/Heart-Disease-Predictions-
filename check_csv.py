"""
CSV Diagnostic Script
This script helps diagnose issues with the heart disease CSV file
"""

import pandas as pd
import os

def check_file_exists(filepath):
    """Check if the CSV file exists"""
    print(f"🔍 Checking file: {filepath}")
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ File exists! Size: {size} bytes")
        return True
    else:
        print(f"❌ File not found: {filepath}")
        return False

def examine_csv_raw(filepath):
    """Examine the raw CSV content"""
    print(f"\n📄 Examining raw file content...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_lines = [f.readline().strip() for _ in range(5)]
        
        print("First 5 lines of the file:")
        for i, line in enumerate(first_lines, 1):
            print(f"Line {i}: {line[:100]}...")  # Show first 100 chars
            
        return first_lines
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        try:
            # Try different encoding
            with open(filepath, 'r', encoding='latin-1') as f:
                first_lines = [f.readline().strip() for _ in range(5)]
            
            print("✅ File readable with latin-1 encoding")
            print("First 5 lines:")
            for i, line in enumerate(first_lines, 1):
                print(f"Line {i}: {line[:100]}...")
                
            return first_lines
        except Exception as e2:
            print(f"❌ Error with latin-1 encoding too: {e2}")
            return None

def try_loading_csv(filepath):
    """Try different ways to load the CSV"""
    print(f"\n🔄 Trying different CSV loading methods...")
    
    methods = [
        ("Default pandas", {}),
        ("With header=0", {"header": 0}),
        ("Without header", {"header": None}),
        ("With semicolon separator", {"sep": ";"}),
        ("With tab separator", {"sep": "\t"}),
        ("With latin-1 encoding", {"encoding": "latin-1"}),
        ("Skip bad lines", {"on_bad_lines": "skip"})
    ]
    
    for method_name, kwargs in methods:
        try:
            print(f"\n📊 Trying: {method_name}")
            df = pd.read_csv(filepath, **kwargs)
            print(f"✅ Success! Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            
            if len(df) > 0:
                print(f"First row: {df.iloc[0].to_dict()}")
                return df, method_name, kwargs
            else:
                print("⚠️ DataFrame is empty")
                
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}...")
    
    return None, None, None

def check_expected_columns(df):
    """Check if the DataFrame has expected columns"""
    expected_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    print(f"\n🎯 Checking for expected columns...")
    print(f"Expected: {expected_columns}")
    print(f"Found: {list(df.columns)}")
    
    missing = [col for col in expected_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in expected_columns]
    
    if missing:
        print(f"❌ Missing columns: {missing}")
    if extra:
        print(f"ℹ️ Extra columns: {extra}")
    
    if not missing:
        print("✅ All expected columns found!")
        return True
    else:
        # Check for alternative column names
        print("\n🔍 Looking for alternative column names...")
        
        alternatives = {
            'target': ['num', 'heart_disease', 'diagnosis', 'class', 'output', 'result'],
            'sex': ['gender'],
            'cp': ['chest_pain', 'chest_pain_type'],
            'trestbps': ['resting_bp', 'rest_bp', 'rbp'],
            'chol': ['cholesterol'],
            'fbs': ['fasting_bs', 'fasting_blood_sugar'],
            'restecg': ['rest_ecg', 'resting_ecg'],
            'thalach': ['max_hr', 'max_heart_rate'],
            'exang': ['exercise_angina'],
            'oldpeak': ['st_depression'],
            'ca': ['vessels', 'num_vessels'],
            'thal': ['thalassemia']
        }
        
        found_alternatives = {}
        for expected, alts in alternatives.items():
            for alt in alts:
                if alt in df.columns:
                    found_alternatives[expected] = alt
                    print(f"✅ Found '{alt}' for '{expected}'")
                    break
        
        return found_alternatives

def main():
    """Main diagnostic function"""
    print("🫀 Heart Disease CSV Diagnostic Tool")
    print("=" * 50)
    
    # Ask for file path
    filepath = input("Enter the path to your CSV file (or press Enter for 'heart.csv'): ").strip()
    if not filepath:
        filepath = 'heart.csv'
    
    # Check if file exists
    if not check_file_exists(filepath):
        print("\n💡 Suggestions:")
        print("1. Make sure the CSV file is in the same directory as this script")
        print("2. Check if the filename is correct (case-sensitive)")
        print("3. Try using the full path to the file")
        
        # List files in current directory
        print(f"\n📁 Files in current directory:")
        for file in os.listdir('.'):
            if file.endswith('.csv'):
                print(f"  📄 {file}")
        return
    
    # Examine raw content
    raw_content = examine_csv_raw(filepath)
    if not raw_content:
        return
    
    # Try loading CSV
    df, method, kwargs = try_loading_csv(filepath)
    if df is None:
        print("\n❌ Could not load CSV file with any method")
        print("\n💡 Suggestions:")
        print("1. Check if the file is a valid CSV")
        print("2. Try opening the file in Excel or a text editor")
        print("3. Make sure the file is not corrupted")
        return
    
    print(f"\n✅ Successfully loaded CSV using: {method}")
    print(f"DataFrame shape: {df.shape}")
    
    # Check columns
    result = check_expected_columns(df)
    
    if df.shape[0] > 0:
        print(f"\n📊 Data sample:")
        print(df.head())
        print(f"\n📈 Data types:")
        print(df.dtypes)
        
        # Generate corrected loading code
        print(f"\n🔧 Use this code to load your CSV correctly:")
        print(f"df = pd.read_csv('{filepath}'", end="")
        if kwargs:
            for key, value in kwargs.items():
                if isinstance(value, str):
                    print(f", {key}='{value}'", end="")
                else:
                    print(f", {key}={value}", end="")
        print(")")
        
        if isinstance(result, dict):  # Alternative column names found
            print(f"\n🔄 Column mapping needed:")
            for expected, found in result.items():
                print(f"df = df.rename(columns={{'{found}': '{expected}'}})")

if __name__ == "__main__":
    main()