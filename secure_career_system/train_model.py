import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [f'q{i}' for i in range(1, 16)]


def generate_synthetic(path='data.csv', n=1000):
    """Generate synthetic career-assessment data with 15 question features."""
    rng = np.random.RandomState(42)
    records = []

    for _ in range(n):
        career = int(rng.choice([0, 1, 2]))
        responses = rng.randint(1, 4, size=15)

        if career == 0:
            for idx in [0, 1, 6, 11]:
                responses[idx] = rng.randint(4, 6)
        elif career == 1:
            for idx in [2, 3, 7, 13]:
                responses[idx] = rng.randint(4, 6)
        else:
            for idx in [4, 5, 12]:
                responses[idx] = rng.randint(4, 6)

        responses = np.clip(responses, 1, 5)
        records.append(list(responses) + [career])

    df = pd.DataFrame(records, columns=FEATURE_COLUMNS + ['target'])
    df.to_csv(path, index=False)
    return path


def train(
    data_path='data.csv',
    model_path='ai_model.pkl',
    scaler_path='encoder.pkl',
    features_path='features.json',
):
    """Train and save the career prediction model artifacts."""
    if not os.path.exists(data_path):
        print('No data.csv found, generating synthetic dataset...')
        generate_synthetic(data_path)

    df = pd.read_csv(data_path)
    if 'target' not in df.columns:
        raise ValueError('data must contain a target column')

    X = df.drop(columns=['target'])
    y = df['target'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    with open(features_path, 'w', encoding='utf-8') as f:
        json.dump(list(X.columns), f)

    print(f'Model Accuracy: {accuracy:.2f}')
    print(f'Classification Report:\n{report}')
    print(f'Model trained and saved: {model_path}, {scaler_path}, {features_path}')

    return {
        'accuracy': float(accuracy),
        'features': list(X.columns),
    }


if __name__ == '__main__':
    train()
