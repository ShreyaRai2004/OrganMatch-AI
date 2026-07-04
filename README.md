# OrganMatch-AI
## AI-Powered Organ Donor Matching System | 90.2% Accuracy

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made in India](https://img.shields.io/badge/Made%20in-India-blue.svg)](https://www.india.gov.in/)

---

## Overview

OrganMatch-AI is an intelligent web application that uses Machine Learning to match organ donors with recipients in real-time.

The system analyzes 5 critical medical parameters including Blood Type, Organ Type, HLA Typing, BMI, and Rh Factor.

Using the K-Nearest Neighbors (KNN) algorithm, it delivers the top-10 most compatible donors in under 1 second.

The model achieves 90.2% matching accuracy, significantly outperforming traditional manual matching methods.

Why this matters: Every day, people die waiting for organ transplants - not because organs aren't available, but because the matching process is slow and manual.

OrganMatch-AI solves this by automating the entire matching process, making it faster, more accurate, and potentially life-saving.

---

## How It Works

Input Parameters:

- Blood Type (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Organ Type (Kidney, Liver, Heart, Lung, Pancreas, Cornea)
- HLA Typing
- BMI
- Rh Factor (Positive/Negative)

Algorithm Details:

- Model: K-Nearest Neighbors (KNN)
- k-value: 7 (optimized)
- Accuracy: 90.2%
- Response Time: Less than 1 second

Performance Metrics:

- Accuracy: 90.2%
- Precision: 0.88
- Recall: 0.89
- F1-Score: 0.88

---

## Tech Stack

Frontend: HTML5, CSS3, JavaScript

Backend: Flask (Python)

Machine Learning: Scikit-learn (KNN)

Data Processing: Pandas, NumPy

Model Persistence: Joblib

API: Flask-CORS

---

## How to Use

Step 1: Enter patient details (Blood Type, Organ, Age, City, BMI, Rh Factor, HLA Typing)

Step 2: Click "Find Compatible Donors"

Step 3: System shows top-10 matching donors with match scores

Step 4: Donor hospital name and phone number is displayed

Step 5: Click "Contact Donor Hospital" to send a request

Step 6: View all your requests in the "My Requests" tab

---

## Dataset

- 1500+ Donors
- 500+ Recipients
- 6 Organs (Kidney, Liver, Heart, Lung, Pancreas, Cornea)
- 8 Blood Types
- 10 Indian Cities

---

## Key Features

- Matching in less than 1 second
- 90.2% matching accuracy
- Direct donor hospital phone number
- Complete request tracking
- KNN algorithm with 5 medical parameters

---

## Model Comparison

KNN: 90.2% Accuracy, 0.88 F1-Score

Random Forest: 87.5% Accuracy, 0.855 F1-Score

SVM: 84.3% Accuracy, 0.815 F1-Score

Decision Tree: 81.2% Accuracy, 0.785 F1-Score

---

## Quick Start

Step 1: pip install -r requirements.txt

Step 2: python backend/create_data.py

Step 3: python backend.py

Step 4: python app.py

Step 5: Open frontend/index.html in browser

---

## Contributor

Shreya S Rai



Made with Love for India
