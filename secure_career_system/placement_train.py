import os
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Features used by the placement prediction model.
PLACEMENT_FEATURES = ['cgpa', 'num_skills', 'num_projects', 'num_internships', 'assessment_score']


def generate_placement_data(n=1000):
    """Generate synthetic placement data with richer features.

    Returns feature matrix X and label array y.
    Features: CGPA (0-10 normalised to 0-1), num_skills, num_projects,
    num_internships and assessment_score (all normalised to 0-1).
    """
    rng = np.random.RandomState(42)
    cgpa = rng.uniform(4.0, 10.0, size=n) / 10.0
    num_skills = rng.randint(0, 11, size=n) / 10.0
    num_projects = rng.randint(0, 6, size=n) / 5.0
    num_internships = rng.randint(0, 4, size=n) / 3.0
    assessment_score = rng.uniform(0.3, 1.0, size=n)

    # Placement probability is a weighted combination
    prob = (0.30 * cgpa + 0.20 * num_skills + 0.15 * num_projects
            + 0.20 * num_internships + 0.15 * assessment_score)
    noise = rng.normal(0, 0.05, size=n)
    y = ((prob + noise) > 0.45).astype(int)

    X = np.column_stack([cgpa, num_skills, num_projects, num_internships, assessment_score])
    return X, y


def train(path=None):
    """Train the placement prediction model and save artefacts."""
    X, y = generate_placement_data()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LogisticRegression(solver='liblinear')
    model.fit(X_train_s, y_train)

    acc = accuracy_score(y_test, model.predict(X_test_s))
    print(f'Placement model accuracy: {acc:.2f}')

    base = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(base, 'placement_model.pkl'))
    joblib.dump(scaler, os.path.join(base, 'placement_scaler.pkl'))
    print('Saved placement_model.pkl and placement_scaler.pkl')
    return model, scaler


if __name__ == '__main__':
    train()
