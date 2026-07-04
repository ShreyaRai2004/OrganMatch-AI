# backend/create_data.py
# Creates 1000 donors with ALL organs and ALL blood types for data/donors.csv

import pandas as pd
import random
import os

print("🔄 Creating 1000 donors with ALL organs and blood types...")

# ===== CREATE data/ folder if not exists =====
os.makedirs('data', exist_ok=True)

# ===== ALL BLOOD TYPES =====
blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# ===== ALL ORGANS =====
organs = ['Kidney', 'Liver', 'Heart', 'Lung', 'Pancreas', 'Cornea']

# ===== RH FACTORS =====
rh_factors = ['Positive', 'Negative']

# ===== HLA TYPES =====
hla_list = [
    'A1,B8,DR3', 'A2,B7,DR2', 'A3,B7,DR4', 'A1,B8,DR17',
    'A2,B44,DR4', 'A3,B35,DR1', 'A24,B7,DR15', 'A1,B57,DR7',
    'A2,B15,DR4', 'A3,B18,DR11', 'A11,B35,DR1', 'A24,B44,DR7'
]

# ===== CITIES (Only 10 from your donor list) =====
cities = [
    'Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 
    'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 
    'Jaipur', 'Lucknow'
]

# ===== INDIAN NAMES =====
first_names = ['Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Pranav',
               'Dhruv', 'Krishna', 'Shaurya', 'Aadhya', 'Ananya', 'Diya',
               'Ishita', 'Myra', 'Priya', 'Riya', 'Sara', 'Tanvi', 'Aanya']

last_names = ['Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Reddy',
              'Gupta', 'Joshi', 'Nair', 'Rao', 'Desai', 'Mehta', 'Khanna']

# ===== HOSPITALS =====
hospitals = [
    'AIIMS Delhi', 'Apollo Hospitals', 'Fortis Hospital', 
    'Manipal Hospital', 'Narayana Health', 'KIMS Hospital',
    'Medanta Hospital', 'Sir Ganga Ram Hospital', 'Kokilaben Hospital'
]

def create_donors(count=1000):
    """Create 1000 donors with ALL organs and ALL blood types"""
    donors = []
    
    for i in range(1, count + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        donor = {
            'id': f'D{i:04d}',                    # ✅ MATCHES app.py column name
            'name': f'{first} {last}',            # ✅ MATCHES app.py column name
            'blood_group': random.choice(blood_types),   # ✅ MATCHES app.py
            'organ_type': random.choice(organs),          # ✅ MATCHES app.py
            'hla_score': round(random.uniform(0.3, 1.0), 2),
            'bmi': round(random.uniform(18.5, 35.0), 1),
            'rh_factor': random.choice(rh_factors),
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

# ===== GENERATE 1000 DONORS =====
df = create_donors(1000)

# ===== SAVE TO data/donors.csv (WHERE app.py READS FROM!) =====
df.to_csv('data/donors.csv', index=False)

print(f"✅ Created {len(df)} donors in data/donors.csv!")

# ===== SHOW STATS =====
print("\n" + "="*50)
print("📊 ORGAN DISTRIBUTION")
print("="*50)
print(df['organ_type'].value_counts())

print("\n" + "="*50)
print("📊 BLOOD TYPE DISTRIBUTION")
print("="*50)
print(df['blood_group'].value_counts())

print("\n" + "="*50)
print("📊 CITY DISTRIBUTION")
print("="*50)
print(df['city'].value_counts())

print("\n" + "="*50)
print("📊 SAMPLE DONORS (First 10)")
print("="*50)
print(df[['id', 'name', 'blood_group', 'organ_type', 'city', 'hospital']].head(10))

print("\n✅ ALL DONE! Now run: python app.py")