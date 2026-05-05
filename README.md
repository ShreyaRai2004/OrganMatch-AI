# OrganMatch AI - KNN Based Organ Donor Matching System

## Project Overview
OrganMatch AI is a machine learning web application that matches organ donors with recipients using the K-Nearest Neighbors (KNN) algorithm. The system analyzes 8 medical parameters including blood group compatibility, HLA scoring, age similarity, geographic proximity, weight compatibility, urgency level, wait time, and medical score to achieve 90.2% matching accuracy.

## Tech Stack
- Backend: Python, Flask, Scikit-learn, Pandas, NumPy, Joblib
- Frontend: HTML5, CSS3, JavaScript
- ML Algorithms: KNN (Primary), RandomForest, DecisionTree, SVM
- Model Tuning: GridSearchCV

## Dataset Statistics
- 600 Registered Donors
- 500 Waiting Recipients
- 50,000+ Match Samples
- 80/20 Train-Test Split

## Model Performance
- KNN: 90.2% Accuracy (Primary Model)
- RandomForest: 89.8% Accuracy
- DecisionTree: 89.5% Accuracy
- SVM: 89.1% Accuracy

## Features
- Find compatible donors using KNN algorithm
- Request donor contact through hospital coordinator
- Track request status (Pending/Contacted/Accepted)
- Real-time matching with response time display
- Donor registry with filter options
- ML model comparison dashboard

## Installation and Setup

### Prerequisites
Python 3.9 or higher installed on your system

### Step 1: Clone or Download
Download the project files to your computer

### Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### Step 3: Install Dependencies
pip install flask flask-cors scikit-learn pandas numpy faker joblib

### Step 4: Generate Dataset
python data/generate_dataset.py

### Step 5: Train Machine Learning Models
python backend/model.py

### Step 6: Run Backend Server
python backend/app.py

### Step 7: Open Frontend
Double-click frontend/index.html or open in browser

## How It Works
1. Recipient enters medical details (organ needed, blood group, age, city, urgency)
2. KNN algorithm analyzes 8 medical parameters
3. System finds top 10 most compatible donors
4. Hospital coordinator is notified to contact donor
5. Request status can be tracked in "My Requests" tab

## Results and Achievements
- Achieved 90.2% matching accuracy using KNN algorithm
- Optimal hyperparameters found via GridSearchCV (k=9, Manhattan distance)
- Real-time matching response time under 200 milliseconds
- Successfully deployed as full-stack web application

