import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_synthetic(path='data.csv', n=1000):
    # Create a deterministic synthetic dataset for local training/testing.
    np.random.seed(0)
    X = np.random.randint(0, 5, size=(n, 10)).astype(float)

    # Weighted score to derive a target class in {0,1,2}.
    weighted_sum = (
        2.0 * X[:, 0] + 2.0 * X[:, 1] +
        1.5 * X[:, 3] + 1.8 * X[:, 5] +
        1.2 * X[:, 7] + 1.0 * X[:, 9]
    )
    thresholds = np.quantile(weighted_sum, [0.33, 0.66])
    y = np.digitize(weighted_sum, thresholds)

    columns = [f'q{i}' for i in range(1, 11)]
    df = pd.DataFrame(X, columns=columns)
    df['target'] = y
    df.to_csv(path, index=False)
    return path


def train(data_path='data.csv'):
    if not os.path.exists(data_path):
        print(f'No {data_path} found, generating synthetic dataset...')
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
    print(f'Model Accuracy: {accuracy:.2f}')
    print(classification_report(y_test, y_pred))

    # save artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'ai_model.pkl')
    joblib.dump(scaler, 'encoder.pkl')

    feature_names = [f for f in df.drop(columns=['target']).columns]
    with open('features.json', 'w') as f:
        json.dump(feature_names, f)

    print('Model trained and saved: ai_model.pkl, encoder.pkl, features.json')
    return {
        'accuracy': float(accuracy),
        'model_path': 'ai_model.pkl',
        'encoder_path': 'encoder.pkl',
        'features_path': 'features.json',
    }


if __name__ == '__main__':
    train()
