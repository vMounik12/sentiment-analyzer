from flask import Flask, request, render_template
from textblob import TextBlob
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "local_s3_bucket/sentiment_data.csv"

# Ensure the local_s3_bucket directory exists
os.makedirs("local_s3_bucket", exist_ok=True)

# Create CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "date", "month", "feedback", "sentiment", "score"])

def analyze_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    return sentiment, score

def save_to_csv(feedback, sentiment, score):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date = now.date().isoformat()
    month = now.strftime("%Y-%m")
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, date, month, feedback, sentiment, score])

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    score = None

    if request.method == "POST":
        feedback = request.form["feedback"]
        sentiment, score = analyze_sentiment(feedback)
        save_to_csv(feedback, sentiment, score)

    return render_template("index.html", sentiment=sentiment, score=score)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
