# AI Brand Perception Dashboard

##  Overview
The AI Brand Perception Dashboard is a real-time web-based system that analyzes brand reputation using news data. It uses Natural Language Processing (NLP) techniques to classify sentiment and generate insights such as brand health score and reputation risk.


##  Objectives
- Analyze real-time brand-related news data
- Perform sentiment analysis (Positive, Negative, Neutral)
- Calculate Brand Health Score (0–100)
- Detect Reputation Risk Level
- Provide interactive visual insights


##  Features
- Real-time news fetching using GNews API
- Sentiment analysis using VADER
- Brand Health Score calculation
- Risk classification (Low / Moderate / High)
- Sentiment trend visualization
- Topic extraction (Top keywords)
- Multi-brand comparison
- CSV report download


## 🧠 Technologies Used
- Python
- Flask
- NLTK
- VADER Sentiment Analysis
- Chart.js
- HTML & CSS


## 📊 How It Works
1. User enters brand names
2. System fetches news articles using API
3. Text is cleaned and preprocessed
4. Sentiment analysis is performed
5. Health score and risk level are calculated
6. Results are displayed on dashboard


## ▶️ How to Run the Project

### Step 1: Install dependencies
bash
pip install -r requirements.txt

Step 2: Run the application
python app.py

Step 3: Open in browser
http://127.0.0.1:5000

Sample Input
Apple, Tesla, Microsoft


