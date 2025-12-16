from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from googleapiclient.discovery import build
import instaloader
import re

app = Flask(__name__)

# --- ⚠️ PASTE YOUR REAL API KEY HERE ⚠️ ---
YOUTUBE_API_KEY = 'AIzaSyCtWvlzPJlWLNW2Sad0UKG24mURZsQuPV8' 
# ------------------------------------------

def get_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1: return "Positive", score
    if score < -0.1: return "Negative", score
    return "Neutral", score

def get_youtube_comments(url):
    try:
        video_id = None
        if "v=" in url: video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be" in url: video_id = url.split("/")[-1]
        
        if not video_id: return None

        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50, # Get 50 comments
            textFormat="plainText"
        ).execute()

        analyzed_comments = []
        for item in response['items']:
            raw_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            label, score = get_sentiment(raw_comment)
            analyzed_comments.append({
                'text': raw_comment,
                'sentiment': label,
                'score': round(score, 2)
            })
        
        return analyzed_comments
    except Exception as e:
        print(f"YouTube Error: {e}")
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    
    results = []
    
    if "youtube.com" in url or "youtu.be" in url:
        results = get_youtube_comments(url)
    else:
        # Placeholder for other sites (simplified for now)
        return jsonify({'error': 'Currently supports YouTube links only for individual analysis.'}), 400

    if not results:
        return jsonify({'error': 'No comments found. Check API Key or URL.'}), 400

    return jsonify({'comments': results})

if __name__ == '__main__':
    app.run(debug=True)