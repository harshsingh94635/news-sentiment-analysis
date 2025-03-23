# api.py
from flask import Flask, request, jsonify
from utils import (
    fetch_news_from_newsapi,
    summarize_article,
    analyze_sentiment,
    comparative_analysis,
    generate_final_analysis_text,
    text_to_speech_hindi,
    text_to_speech_hindi_for_article,
    translate_to_hindi
)

app = Flask(__name__)

NEWSAPI_KEY = "bf5d8ff575214d8f8e70888191b83d63"  # Replace with your actual NewsAPI key


@app.route('/')
def home():
    return "Welcome to the News Summarization & Sentiment Analysis API!"


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    company = data.get("company")
    if not company:
        return jsonify({"error": "No company provided"}), 400

    try:
        # 1. Fetch news articles
        articles = fetch_news_from_newsapi(company, api_key=NEWSAPI_KEY, page_size=10)

        # 2. Process each article: summarize, sentiment, translate summary, and TTS
        for i, art in enumerate(articles, start=1):
            summary_en = summarize_article(art["content"])  # English summary
            sentiment = analyze_sentiment(art["content"])

            # Translate the English summary to Hindi
            summary_hi = translate_to_hindi(summary_en)

            art["summary"] = summary_en  # Still store English summary if needed
            art["sentiment"] = sentiment

            # Convert the Hindi summary to speech (TTS)
            audio_file = text_to_speech_hindi_for_article(summary_hi, i)
            art["audio_file"] = audio_file

        # 3. Comparative analysis on the articles
        comp_analysis = comparative_analysis(articles)

        # 4. Generate final analysis text in English and then translate to Hindi
        final_text_en = generate_final_analysis_text(articles, company)
        final_text_hi = translate_to_hindi(final_text_en)

        # 5. Convert the final Hindi text to TTS
        final_audio_file = text_to_speech_hindi(final_text_hi, filename="final_summary.mp3")

        # Construct the final response JSON
        response_data = {
            "Company": company,
            "Articles": articles,
            "Comparative Analysis": comp_analysis,
            "Final Sentiment Analysis (English)": final_text_en,
            "Final Sentiment Analysis (Hindi)": final_text_hi,
            "Final Audio File": final_audio_file
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
