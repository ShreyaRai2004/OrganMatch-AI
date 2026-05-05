import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker('en_IN')
random.seed(42)
np.random.seed(42)

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
ORGANS = ['Kidney', 'Liver', 'Heart', 'Lung', 'Cornea', 'Pancreas']
CITIES = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad',
          'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']

COMPATIBILITY = {
    'A+':  ['A+', 'AB+'],
    'A-':  ['A+', 'A-', 'AB+', 'AB-'],
    'B+':  ['B+', 'AB+'],
    'B-':  ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'],
    'AB-': ['AB+', 'AB-'],
    'O+':  ['A+', 'B+', 'AB+', 'O+'],
    'O-':  ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
}

def blood_compatible(donor_bg, recipient_bg):
    return 1 if recipient_bg in COMPATIBILITY.get(donor_bg, []) else 0

def generate_record(record_id, role):
    return {
        'id':             record_id,
        'name':           fake.name(),
        'age':            random.randint(18, 65),
        'blood_group':    random.choice(BLOOD_GROUPS),
        'organ_type':     random.choice(ORGANS),
        'hla_score':      round(random.uniform(0.3, 1.0), 2),
        'city':           random.choice(CITIES),
        'urgency_level':  random.randint(1, 5),
        'wait_time_days': random.randint(1, 730),
        'weight_kg':      round(random.uniform(45, 100), 1),
        'medical_score':  round(random.uniform(0.5, 1.0), 2),
        'role':           role
    }

donors     = [generate_record(f'D{i:04d}', 'donor')     for i in range(1, 601)]
recipients = [generate_record(f'R{i:04d}', 'recipient') for i in range(1, 501)]

df_donors     = pd.DataFrame(donors)
df_recipients = pd.DataFrame(recipients)

matches = []
for _, rec in df_recipients.iterrows():
    compatible = df_donors[df_donors['organ_type'] == rec['organ_type']].copy()
    for _, don in compatible.iterrows():
        bc         = blood_compatible(don['blood_group'], rec['blood_group'])
        hla_diff   = abs(don['hla_score'] - rec['hla_score'])
        age_diff   = abs(don['age'] - rec['age'])
        city_match = 1 if don['city'] == rec['city'] else 0
        weight_diff= abs(don['weight_kg'] - rec['weight_kg'])
        
        # Raw compatibility score (0-100)
        raw_score = (bc * 35 + (1 - hla_diff) * 25 +
                     max(0, 1 - age_diff/50) * 15 + city_match * 10 +
                     max(0, 1 - weight_diff/60) * 10 +
                     rec['urgency_level'] / 5 * 5)
        
        # Add noise to make it realistic (target ~90% accuracy)
        noisy_score = raw_score + np.random.normal(0, 8)
        noisy_score = max(0, min(100, noisy_score))
        
        # Match label based on noisy score (threshold 55)
        is_match = 1 if (bc == 1 and noisy_score >= 55) else 0
        
        matches.append({
            'donor_id':            don['id'],
            'recipient_id':        rec['id'],
            'blood_compatible':    bc,
            'hla_diff':            round(hla_diff, 3),
            'age_diff':            age_diff,
            'city_match':          city_match,
            'weight_diff':         round(weight_diff, 1),
            'urgency_level':       rec['urgency_level'],
            'wait_time_days':      rec['wait_time_days'],
            'medical_score':       rec['medical_score'],
            'compatibility_score': round(noisy_score, 2),
            'match_label':         is_match
        })

df_matches = pd.DataFrame(matches)
pos  = df_matches[df_matches['match_label'] == 1]
neg  = df_matches[df_matches['match_label'] == 0]
neg  = neg.sample(min(len(pos)*2, len(neg)), random_state=42)
df_balanced = pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

df_donors.to_csv('data/donors.csv', index=False)
df_recipients.to_csv('data/recipients.csv', index=False)
df_balanced.to_csv('data/matches.csv', index=False)

accuracy = df_balanced['match_label'].mean() * 100
print(f"✅ Donors:      {len(df_donors)}")
print(f"✅ Recipients:  {len(df_recipients)}")
print(f"✅ Match pairs: {len(df_balanced)}")
print(f"✅ Match rate:  {accuracy:.1f}%")
print("Dataset saved successfully!")