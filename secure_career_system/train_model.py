import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib


# Feature columns used by the career recommendation model.
# Each corresponds to a self-assessed interest/skill score (1-5).
CAREER_FEATURES = [
    'programming', 'math_analysis', 'finance_interest', 'data_driven',
    'helping_people', 'science_research', 'problem_solving', 'structured_env',
    'communication', 'leadership',
]

# Career path labels
CAREER_LABELS = {0: 'Technology', 1: 'Finance', 2: 'Healthcare'}


def generate_synthetic(path='data.csv', n=1000):
    """Generate a synthetic career-recommendation dataset.

    Each row has 10 interest/skill features (1-5) and a target label
    (0=Technology, 1=Finance, 2=Healthcare).  Feature distributions are
    biased so that the resulting model learns meaningful patterns.
    """
    np.random.seed(42)
    rows = []
    for _ in range(n):
        label = np.random.choice([0, 1, 2], p=[0.4, 0.3, 0.3])
        if label == 0:
            row = [
                np.random.choice([4, 5]), np.random.choice([3, 4, 5]),
                np.random.choice([1, 2, 3]), np.random.choice([3, 4, 5]),
                np.random.choice([1, 2, 3]), np.random.choice([2, 3, 4]),
                np.random.choice([4, 5]), np.random.choice([2, 3, 4]),
                np.random.choice([2, 3, 4]), np.random.choice([1, 2, 3, 4]),
            ]
        elif label == 1:
            row = [
                np.random.choice([1, 2, 3]), np.random.choice([3, 4, 5]),
                np.random.choice([4, 5]), np.random.choice([4, 5]),
                np.random.choice([1, 2, 3]), np.random.choice([1, 2, 3]),
                np.random.choice([3, 4]), np.random.choice([4, 5]),
                np.random.choice([3, 4, 5]), np.random.choice([3, 4, 5]),
            ]
        else:
            row = [
                np.random.choice([1, 2]), np.random.choice([2, 3, 4]),
                np.random.choice([1, 2, 3]), np.random.choice([2, 3, 4]),
                np.random.choice([4, 5]), np.random.choice([4, 5]),
                np.random.choice([3, 4, 5]), np.random.choice([3, 4, 5]),
                np.random.choice([4, 5]), np.random.choice([3, 4, 5]),
            ]
        rows.append(row + [label])

    df = pd.DataFrame(rows, columns=CAREER_FEATURES + ['target'])
    df.to_csv(path, index=False)
    return path


def train(data_path='data.csv'):
    """Train the career-recommendation Random Forest model.

    Reads *data_path* (CSV with columns matching ``CAREER_FEATURES`` plus a
    ``target`` column), trains a Random Forest classifier and persists the
    model, scaler and feature list to disk.
    """
    if not os.path.exists(data_path):
        print('No data.csv found, generating synthetic dataset...')
        generate_synthetic(data_path)

    df = pd.read_csv(data_path)
    if 'target' not in df.columns:
        raise ValueError('data must contain a target column')

    X = df.drop(columns=['target']).values
    y = df['target'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f'Career model accuracy: {acc:.2f}')
    print(classification_report(y_test, y_pred, target_names=list(CAREER_LABELS.values())))

    # Save artifacts next to this file
    base = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(base, 'ai_model.pkl'))
    joblib.dump(scaler, os.path.join(base, 'encoder.pkl'))

    feature_names = list(df.drop(columns=['target']).columns)
    with open(os.path.join(base, 'features.json'), 'w') as f:
        json.dump(feature_names, f)

    print('Model trained and saved: ai_model.pkl, encoder.pkl, features.json')
    return model, scaler


if __name__ == '__main__':
    train()
