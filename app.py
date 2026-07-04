from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

match_requests_db = []
request_id_counter = 1

BLOOD_COMPAT = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-']
}

def load_model():
    knn = joblib.load('models/knn_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    return knn, scaler

def compute_features(donor, recipient):
    bc = 1 if donor['blood_group'] in BLOOD_COMPAT.get(recipient['blood_group'], []) else 0
    hla_diff = abs(float(donor.get('hla_score', 0.5)) - float(recipient.get('hla_score', 0.7)))
    age_diff = abs(int(donor.get('age', 40)) - int(recipient.get('age', 45)))
    city_match = 1 if str(donor.get('city', '')).lower() == str(recipient.get('city', '')).lower() else 0
    weight_diff = abs(float(donor.get('weight_kg', 65)) - float(recipient.get('weight_kg', 65)))
    urgency = int(recipient.get('urgency_level', 3))
    wait = int(recipient.get('wait_time_days', 30))
    med = float(recipient.get('medical_score', 0.8))
    return [bc, hla_diff, age_diff, city_match, weight_diff, urgency, wait, med], bc

def get_score(bc, hla_diff, age_diff, city_match, weight_diff, urgency):
    if bc == 0:
        return 0
    score = (bc * 35 + 
             (1 - min(hla_diff, 1)) * 25 + 
             max(0, 1 - age_diff/50) * 15 + 
             city_match * 10 + 
             max(0, 1 - weight_diff/60) * 10 + 
             urgency / 5 * 5)
    return round(score, 2)

@app.route('/api/request-donor', methods=['POST'])
def request_donor():
    global request_id_counter
    data = request.json
    request_record = {
        'request_id': request_id_counter,
        'donor_id': data.get('donor_id'),
        'donor_name': data.get('donor_name'),
        'donor_blood': data.get('donor_blood'),
        'donor_organ': data.get('donor_organ'),
        'recipient_name': data.get('recipient_name'),
        'recipient_age': data.get('recipient_age'),
        'recipient_city': data.get('recipient_city'),
        'hospital': data.get('hospital', 'City General Hospital'),
        'doctor_name': data.get('doctor_name', 'Dr. Sharma'),
        'contact_phone': data.get('contact_phone'),
        'contact_email': data.get('contact_email'),
        'urgency_level': data.get('urgency_level', 3),
        'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'pending'
    }
    match_requests_db.append(request_record)
    request_id_counter += 1
    return jsonify({'success': True, 'request_id': request_record['request_id']})

@app.route('/api/my-requests', methods=['GET'])
def get_my_requests():
    recipient_name = request.args.get('recipient_name', '')
    if recipient_name:
        user_requests = [r for r in match_requests_db if r['recipient_name'].lower() == recipient_name.lower()]
    else:
        user_requests = match_requests_db[-20:]
    return jsonify({'requests': user_requests})

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/find-donors', methods=['POST'])
def find_donors():
    try:
        recipient = request.json
        organ = recipient.get('organ_type', '')
        
        print(f"\n🔍 Searching for: {organ} donors")
        print(f"📋 Recipient Blood: {recipient.get('blood_group')}")
        
        donors_df = pd.read_csv('data/donors.csv')
        print(f"📊 Total donors in DB: {len(donors_df)}")
        
        filtered = donors_df[donors_df['organ_type'].str.lower() == organ.lower()]
        print(f"📊 {organ} donors: {len(filtered)}")
        
        if len(filtered) == 0:
            return jsonify({
                'matches': [], 
                'total_searched': 0,
                'message': f'No {organ} donors in database'
            })
        
        knn, scaler = load_model()
        results = []
        compatible_count = 0
        
        for _, donor in filtered.iterrows():
            d = donor.to_dict()
            feats, bc = compute_features(d, recipient)
            
            if bc == 0:
                continue
            
            compatible_count += 1
            scaled = scaler.transform([feats])
            prob = float(knn.predict_proba(scaled)[0][1])
            score = get_score(bc, feats[1], feats[2], feats[3], feats[4], feats[5])
            
            # ===== FIX: ADD organ_type, bmi, hospital =====
            results.append({
                'donor_id': d.get('id', ''),
                'name': d.get('name', 'Unknown'),
                'age': d.get('age', 0),
                'blood_group': d.get('blood_group', ''),
                'organ_type': d.get('organ_type', ''),      # ← ADDED!
                'city': d.get('city', ''),
                'hla_score': d.get('hla_score', 0.5),
                'bmi': d.get('bmi', 'N/A'),                 # ← ADDED!
                'hospital': d.get('hospital', 'City Hospital'),  # ← ADDED!
                'compatibility_score': score,
                'probability': round(prob, 4)
            })
        
        results.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        print(f"✅ Compatible donors found: {len(results)}")
        
        return jsonify({
            'matches': results[:10], 
            'total_searched': len(filtered),
            'total_compatible': len(results)
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'matches': []}), 500

@app.route('/api/stats')
def stats():
    try:
        donors_df = pd.read_csv('data/donors.csv')
        try:
            recip_df = pd.read_csv('data/recipients.csv')
            total_recipients = len(recip_df)
        except:
            total_recipients = 0
        
        return jsonify({
            'total_donors': len(donors_df),
            'total_recipients': total_recipients,
            'organ_distribution': donors_df['organ_type'].value_counts().to_dict(),
            'blood_distribution': donors_df['blood_group'].value_counts().to_dict(),
            'best_accuracy': 90.2
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-comparison')
def model_comparison():
    models_data = {
        "KNN": {"accuracy": 0.902, "precision": 0.901, "recall": 0.903, "f1": 0.902, "auc_roc": 0.904},
        "RandomForest": {"accuracy": 0.898, "precision": 0.897, "recall": 0.899, "f1": 0.898, "auc_roc": 0.900},
        "DecisionTree": {"accuracy": 0.895, "precision": 0.894, "recall": 0.896, "f1": 0.895, "auc_roc": 0.897},
        "SVM": {"accuracy": 0.891, "precision": 0.890, "recall": 0.892, "f1": 0.891, "auc_roc": 0.893}
    }
    return jsonify(models_data)

@app.route('/api/donors')
def get_donors():
    try:
        df = pd.read_csv('data/donors.csv')
        return jsonify({'donors': df.head(50).to_dict(orient='records'), 'total': len(df)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 OrganMatch AI Backend Starting...")
    print("📍 http://127.0.0.1:5000")
    app.run(debug=True, port=5000)