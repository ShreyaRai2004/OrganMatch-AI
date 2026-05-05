import pandas as pd
import numpy as np
import joblib
import json
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score)
import warnings
warnings.filterwarnings('ignore')

FEATURES = ['blood_compatible', 'hla_diff', 'age_diff', 'city_match',
            'weight_diff', 'urgency_level', 'wait_time_days', 'medical_score']

def train_models():
    df = pd.read_csv('data/matches.csv')
    X  = df[FEATURES]
    y  = df['match_label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    scaler       = StandardScaler()
    X_train_sc   = scaler.fit_transform(X_train)
    X_test_sc    = scaler.transform(X_test)

    # Find best K
    print("🔍 Tuning KNN...")
    param_grid = {'n_neighbors': range(3, 16, 2),
                  'metric': ['euclidean', 'manhattan']}
    knn_cv = GridSearchCV(KNeighborsClassifier(), param_grid,
                          cv=5, scoring='f1', n_jobs=-1)
    knn_cv.fit(X_train_sc, y_train)
    best_knn = knn_cv.best_estimator_
    print(f"   Best k={knn_cv.best_params_['n_neighbors']}, metric={knn_cv.best_params_['metric']}")

    models = {
        'KNN':          best_knn,
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'SVM':          SVC(probability=True, random_state=42),
        'DecisionTree': DecisionTreeClassifier(max_depth=8, random_state=42)
    }

    results = {}
    for name, model in models.items():
        print(f"🤖 Training {name}...")
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)
        y_prob = model.predict_proba(X_test_sc)[:, 1]
        results[name] = {
            'accuracy':  round(accuracy_score(y_test, y_pred),  4),
            'precision': round(precision_score(y_test, y_pred), 4),
            'recall':    round(recall_score(y_test, y_pred),    4),
            'f1':        round(f1_score(y_test, y_pred),        4),
            'auc_roc':   round(roc_auc_score(y_test, y_prob),   4)
        }
        print(f"   Accuracy={results[name]['accuracy']} | F1={results[name]['f1']}")

    joblib.dump(best_knn, 'models/knn_model.pkl')
    joblib.dump(scaler,   'models/scaler.pkl')
    joblib.dump(models,   'models/all_models.pkl')
    with open('models/results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n✅ All models saved!")
    return results

if __name__ == '__main__':
    results = train_models()
    print("\n===== FINAL RESULTS =====")
    for model, m in results.items():
        print(f"{model:15s} | Acc={m['accuracy']} | F1={m['f1']} | AUC={m['auc_roc']}")