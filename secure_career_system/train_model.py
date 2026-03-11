import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Assessment question mapping to career domains:
# q1, q2, q7, q12 → Technology indicators
# q3, q4, q8, q14 → Finance indicators
# q5, q6, q13     → Healthcare indicators
# q9, q10, q11, q15 → General aptitude
FEATURE_COLUMNS = [f'q{i}' for i in range(1, 16)]


def generate_synthetic(path='data.csv', n=1000):
    """Generate a synthetic career assessment dataset with 15 question features.

    Each row simulates a student's assessment responses (1-5 scale)
    with a target career label: 0=Technology, 1=Finance, 2=Healthcare.
    """
    rng = np.random.RandomState(42)
    records = []

    for _ in range(n):
        # Randomly pick a dominant career category
        career = rng.choice([0, 1, 2])

        # Base responses (neutral)
        responses = rng.randint(1, 4, size=15)

        if career == 0:  # Technology
            for idx in [0, 1, 6, 11]:  # q1, q2, q7, q12
                responses[idx] = rng.randint(4, 6)
        elif career == 1:  # Finance
            for idx in [2, 3, 7, 13]:  # q3, q4, q8, q14
                responses[idx] = rng.randint(4, 6)
        else:  # Healthcare
            for idx in [4, 5, 12]:  # q5, q6, q13
                responses[idx] = rng.randint(4, 6)

        # Clip to 1-5
        responses = np.clip(responses, 1, 5)
        row = list(responses) + [career]
        records.append(row)

    columns = FEATURE_COLUMNS + ['target']
    df = pd.DataFrame(records, columns=columns)
    df.to_csv(path, index=False)
    return path


def train(data_path='data.csv'):
    """Train a career prediction model from assessment response data.

    The model predicts career path (0=Technology, 1=Finance, 2=Healthcare)
    from 15 assessment question responses (1-5 scale each).
    """
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

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Model Accuracy: {accuracy:.2f}')

    # save artifacts
    joblib.dump(model, 'ai_model.pkl')
    joblib.dump(scaler, 'encoder.pkl')

    feature_names = list(df.drop(columns=['target']).columns)
    with open('features.json', 'w') as f:
        json.dump(feature_names, f)

    print('Model trained and saved: ai_model.pkl, encoder.pkl, features.json')
    return model, scaler


if __name__ == '__main__':
    train()
