from flask import Flask, render_template, request, send_file
import requests
import re
import nltk
import csv
from collections import Counter
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------- NLTK SETUP ----------
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

# ---------- TEXT CLEANING ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    return [w for w in words if w not in stopwords.words("english")]

# ---------- FETCH NEWS ----------
def fetch_news(brand):
    API_KEY = "856a4f4b98a3e6cb1ff8d5569aa8b7da"   
    url = f"https://gnews.io/api/v4/search?q={brand}&lang=en&max=15&token={API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [
        a["title"] + " " + a["description"]
        for a in articles if a.get("description")
    ]

# ---------- SENTIMENT ----------
def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

# ---------- BRAND HEALTH ----------
def calculate_brand_health(results):
    total = sum(results.values())
    if total == 0:
        return 50
    pos = results["Positive"] / total
    neg = results["Negative"] / total
    raw = (pos - neg) * 100
    return max(0, min(100, int((raw + 100) / 2)))

# ---------- RISK ----------
def determine_risk(results):
    total = sum(results.values())
    if total == 0:
        return "Unknown"
    neg_ratio = results["Negative"] / total
    if neg_ratio > 0.4:
        return "High Risk"
    elif neg_ratio > 0.2:
        return "Moderate Risk"
    else:
        return "Low Risk"

# ---------- CONFIDENCE ----------
def calculate_confidence(article_count):
    if article_count >= 15:
        return "High"
    elif article_count >= 8:
        return "Medium"
    else:
        return "Low"

# ---------- AI INSIGHT ----------
def generate_insight(brand, health, risk):
    if health >= 75:
        tone = "strong and positive"
    elif health >= 55:
        tone = "stable but mixed"
    else:
        tone = "weak and concerning"

    return (
        f"{brand} currently shows a {tone} brand perception. "
        f"The brand health score is {health}/100, indicating a {risk.lower()} "
        f"level of reputational exposure."
    )

# ---------- EXECUTIVE SUMMARY ----------
def generate_executive_summary(brand, health, risk, confidence, article_count):
    return (
        f"This analysis of {brand} is based on {article_count} recent news articles "
        f"with a {confidence.lower()} confidence level. The brand has a health score "
        f"of {health}/100 and is categorized under {risk.lower()}."
    )

# ---------- RECOMMENDATION ENGINE ----------
def generate_recommendation(health, risk):
    if risk == "High Risk":
        return "Immediate reputation management and public communication is recommended."
    elif risk == "Moderate Risk":
        return "Brand monitoring and targeted improvement strategies are advised."
    else:
        return "Maintain current brand strategy and continue monitoring sentiment."

# ---------- KEY TOPICS ----------
def extract_key_topics(words):
    counter = Counter(words)
    return [w for w, _ in counter.most_common(6)]

# ---------- MAIN ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def index():
    all_results = []
    ranking = []

    if request.method == "POST":
        brands = request.form["brand"].split(",")

        with open("brand_results.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for brand in brands:
                brand = brand.strip()
                results = {"Positive": 0, "Negative": 0, "Neutral": 0}
                trend = []
                all_words = []

                articles = fetch_news(brand)
                article_count = len(articles)
                confidence = calculate_confidence(article_count)

                for article in articles:
                    words = clean_text(article)
                    sentiment, score = analyze_sentiment(" ".join(words))
                    results[sentiment] += 1
                    trend.append(score)
                    all_words.extend(words)

                health = calculate_brand_health(results)
                risk = determine_risk(results)
                insight = generate_insight(brand, health, risk)
                executive_summary = generate_executive_summary(
                    brand, health, risk, confidence, article_count
                )
                recommendation = generate_recommendation(health, risk)
                topics = extract_key_topics(all_words)

                writer.writerow([
                    brand,
                    results["Positive"],
                    results["Negative"],
                    results["Neutral"],
                    health,
                    risk
                ])

                all_results.append({
                    "brand": brand,
                    "health": health,
                    "risk": risk,
                    "confidence": confidence,
                    "article_count": article_count,
                    "executive_summary": executive_summary,
                    "insight": insight,
                    "recommendation": recommendation,
                    "topics": topics,
                    "trend": trend,
                    "trend_labels": list(range(len(trend))),
                    "results": results
                })

                ranking.append((brand, health))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return render_template("index.html", all_results=all_results, ranking=ranking)

# ---------- CSV DOWNLOAD ----------
@app.route("/download")
def download_csv():
    return send_file("brand_results.csv", as_attachment=True)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
