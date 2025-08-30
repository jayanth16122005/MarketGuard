import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import joblib
import re

def generate_training_data():
    """Generate mock training data for demonstration"""
    n_samples = 1000
    
    data = {
        'text': [],
        'length': [],
        'has_guaranteed': [],
        'has_free': [],
        'has_risk_free': [],
        'has_double': [],
        'has_quick': [],
        'urgency_score': [],
        'number_count': [],
        'percentage_count': [],
        'money_count': [],
        'sentiment': [],
        'is_fraud': []
    }
    
    # Fraudulent examples
    fraudulent_texts = [
        "Guaranteed returns of 20% monthly with no risk!",
        "Double your money in just 30 days with our secret strategy",
        "Risk-free investment opportunity with 100% success rate",
        "Act now to get in on this pre-IPO opportunity",
        "Limited time offer: get 5% daily returns",
        "Government approved investment with guaranteed profits",
        "Secret method that brokers don't want you to know",
        "Make fast money with our exclusive trading algorithm",
        "Special discount for first-time investors",
        "No one wants you to know about this opportunity"
    ]
    
    # Legitimate examples
    legitimate_texts = [
        "Diversified portfolio with historical average returns of 7% annually",
        "Consider investing in index funds for long-term growth",
        "Review the company's financial statements before investing",
        "All investments carry some degree of risk",
        "Consult with a registered financial advisor before making decisions",
        "Past performance is not indicative of future results",
        "The value of investments may go down as well as up",
        "Consider your risk tolerance before investing",
        "This is not a guarantee of future performance",
        "Investments should be made based on personal research"
    ]
    
    for i in range(n_samples):
        if i % 5 == 0:  # 20% fraudulent
            text = np.random.choice(fraudulent_texts)
            is_fraud = 1
        else:
            text = np.random.choice(legitimate_texts)
            is_fraud = 0
            
        data['text'].append(text)
        data['length'].append(len(text))
        data['has_guaranteed'].append(1 if 'guaranteed' in text.lower() else 0)
        data['has_free'].append(1 if 'free' in text.lower() else 0)
        data['has_risk_free'].append(1 if 'risk-free' in text.lower() else 0)
        data['has_double'].append(1 if 'double' in text.lower() else 0)
        data['has_quick'].append(1 if 'quick' in text.lower() else 0)
        data['urgency_score'].append(len(re.findall(r'now|immediately|today|quick|fast|limited', text.lower())))
        data['number_count'].append(len(re.findall(r'\d+', text)))
        data['percentage_count'].append(len(re.findall(r'\d+%', text)))
        data['money_count'].append(len(re.findall(r'\$|₹|€|£|rs|inr|usd', text.lower())))
        data['sentiment'].append(1 if any(word in text.lower() for word in ['profit', 'gain', 'success', 'win', 'growth']) else 0)
        data['is_fraud'].append(is_fraud)
    
    return pd.DataFrame(data)

def train_model():
    print("Generating training data...")
    df = generate_training_data()
    
    # Save the training dataset for reference
    df.to_csv('train_dataset.csv', index=False)
    print("Training data saved to train_dataset.csv")
    
    # Features and target
    X = df.drop(['text', 'is_fraud'], axis=1)
    y = df['is_fraud']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Training accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    # Save the model
    joblib.dump(model, '../backend/model.joblib')
    print("Model saved to backend/model.joblib")

if __name__ == '__main__':
    train_model()