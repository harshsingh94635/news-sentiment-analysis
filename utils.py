# utils.py
import requests
from textblob import TextBlob
from gtts import gTTS
import os
from googletrans import Translator

# Initialize the translator once
translator = Translator()

def fetch_news_from_newsapi(company, api_key, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "apiKey": api_key,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "relevancy"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") != "ok":
        raise Exception(data.get("message", "Error fetching news from NewsAPI"))
    articles = []
    for article in data.get("articles", []):
        content = article["content"] if article["content"] else "No content available."
        articles.append({
            "title": article["title"],
            "url": article["url"],
            "content": content
        })
    return articles

def summarize_article(text, max_sentences=2):
    if not text or text == "No content available.":
        return "No summary available."
    sentences = text.split('. ')
    summary = '. '.join(sentences[:max_sentences])
    return summary

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def comparative_analysis(articles):
    distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for art in articles:
        distribution[art["sentiment"]] += 1
    coverage_diff = []
    if len(articles) > 1:
        coverage_diff.append({
            "Comparison": f"{articles[0]['title']} is {articles[0]['sentiment']}, while {articles[1]['title']} is {articles[1]['sentiment']}.",
            "Impact": "Shows variance in coverage."
        })
    return {
        "Sentiment Distribution": distribution,
        "Coverage Differences": coverage_diff
    }

def generate_final_analysis_text(articles, company):
    total = len(articles)
    if total == 0:
        return f"No articles found for {company}."
    pos = sum(1 for a in articles if a["sentiment"] == "Positive")
    neg = sum(1 for a in articles if a["sentiment"] == "Negative")
    neu = sum(1 for a in articles if a["sentiment"] == "Neutral")
    text = (
        f"{company} ke baare mein humne {total} news articles paye. "
        f"Positive articles ki sankhya hai {pos}, "
        f"Negative articles ki sankhya hai {neg}, "
        f"aur Neutral articles ki sankhya hai {neu}."
    )
    return text

def text_to_speech_hindi(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    return filename

def text_to_speech_hindi_for_article(text, article_index):
    filename = f"article_{article_index}_summary.mp3"
    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    return filename

def translate_to_hindi(english_text):
    """
    Translates the provided English text to Hindi using googletrans.
    """
    if not english_text or english_text == "No summary available.":
        return english_text
    try:
        translation = translator.translate(english_text, src='en', dest='hi')
        return translation.text
    except Exception:
        # If translation fails, return the original text as fallback.
        return english_text
