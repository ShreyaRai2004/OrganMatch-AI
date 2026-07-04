# data/add_donors.py
# Adds 500 donors to your existing donors.csv

import pandas as pd
import random

print("🔄 Adding 500 donors to your data/donors.csv...")

blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
organs = ['Kidney', 'Liver', 'Heart', 'Lung', 'Pancreas', 'Cornea']
hla_list = ['A1,B8,DR3', 'A2,B7,DR2', 'A3,B7,DR4', 'A1,B8,DR17',
            'A2,B44,DR4', 'A3,B35,DR1', 'A24,B7,DR15', 'A1,B57,DR7']
cities = ['Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad', 
          'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
first_names = ['Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Pranav',
               'Dhruv', 'Krishna', 'Shaurya', 'Aadhya', 'Ananya', 'Diya',
               'Ishita', 'Myra', 'Priya', 'Riya', 'Sara', 'Tanvi']
last_names = ['Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Reddy',
              'Gupta', 'Joshi', 'Nair', 'Rao', 'Desai', 'Mehta']
hospitals = ['AIIMS Delhi', 'Apollo Hospitals', 'Fortis Hospital', 
             'Manipal Hospital', 'Narayana Health', 'KIMS Hospital']

def create_donors(count=500):
    donors = []
    for i in range(1, count + 1):
        donor = {
            'id': f'D{6000+i:04d}',
            'name': f'{random.choice(first_names)} {random.choice(last_names)}',
            'blood_group': random.choice(blood_types),
            'organ_type': random.choice(organs),
            'hla_score': round(random.uniform(0.3, 1.0), 2),
            'bmi': round(random.uniform(18.5, 35.0), 1),
            'rh_factor': random.choice(['Positive', 'Negative']),
            'age': random.randint(18, 65),
            'gender': random.choice(['Male', 'Female']),
            'city': random.choice(cities),
            'hospital': random.choice(hospitals),
            'contact': f'+91-{random.randint(7000000000, 9999999999)}',
            'weight_kg': round(random.uniform(45, 100), 1),
            'urgency_level': random.randint(1, 5),
            'wait_time_days': random.randint(0, 730),
            'medical_score': round(random.uniform(0.5, 1.0), 2)
        }
        donors.append(donor)
    return pd.DataFrame(donors)

# Read existing
existing = pd.read_csv('data/donors.csv')
print(f"✅ Existing donors: {len(existing)}")

# Generate new
new_donors = create_donors(500)

# Combine
final = pd.concat([existing, new_donors], ignore_index=True)

# Save
final.to_csv('data/donors.csv', index=False)

print(f"\n✅ Total donors now: {len(final)}")

print("\n📊 ORGAN DISTRIBUTION:")
print(final['organ_type'].value_counts())

print("\n📊 BLOOD TYPE DISTRIBUTION:")
print(final['blood_group'].value_counts())

# Check Lung + B-
lung_bminus = final[(final['organ_type'] == 'Lung') & (final['blood_group'] == 'B-')]
print(f"\n🔍 Lung + B- donors: {len(lung_bminus)}")
if len(lung_bminus) > 0:
    print(lung_bminus[['id', 'name', 'blood_group', 'organ_type', 'city']].head())
else:
    print("⚠️ Still no Lung + B- donors. Run again or increase count.")

print("\n✅ DONE! Now run: python backend/app.py")