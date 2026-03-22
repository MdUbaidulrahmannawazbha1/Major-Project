import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


def generate_synthetic(path='data.csv', n=1000):
    # create simple synthetic dataset
    np.random.seed(0)
    X = np.random.randint(0, 5, size=(n, 10))
    y = (X.sum(axis=1) > 20).astype(int)
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    df['target'] = y
    df.to_csv(path, index=False)
    return path


def train(data_path='data.csv'):
    if not os.path.exists(data_path):
        print('No data.csv found, generating synthetic dataset...')
        generate_synthetic(data_path)

    df = pd.read_csv(data_path)
    if 'target' not in df.columns:
        raise ValueError('data must contain a target column')

    X = df.drop(columns=['target']).values
    y = df['target'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # save artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'ai_model.pkl')
    joblib.dump(scaler, 'encoder.pkl')

    feature_names = [f for f in df.drop(columns=['target']).columns]
    with open('features.json', 'w') as f:
        json.dump(feature_names, f)

    print('Model trained and saved: ai_model.pkl, encoder.pkl, features.json')


if __name__ == '__main__':
    train()
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Sample data for training (replace with actual data)
X = np.array([
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 1, 0, 0, 1],
    [0, 0, 1, 1, 0],
    [1, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1],
])

# Labels for career paths (0: Tech, 1: Finance, 2: Healthcare)
y = np.array([0, 1, 0, 1, 0, 2, 1, 2])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')
print(f'Classification Report:\n{classification_report(y_test, y_pred)}')

# Save model
with open('ai_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print('Model saved as ai_model.pkl')

# Train and save encoder
encoder = LabelEncoder()
encoder.fit(['Tech', 'Finance', 'Healthcare'])

with open('encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)
print('Encoder saved as encoder.pkl')
