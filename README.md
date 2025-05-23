# 📰 News Summarization & Sentiment Analysis (Hindi TTS)

This project fetches news articles about a given company, summarizes them, analyzes their sentiment, translates the summaries to Hindi, and generates Hindi audio using Google Text-to-Speech.

## ✨ Features

- 🔍 Fetch news from **NewsAPI** based on a company name
- 🧠 Summarize and perform **sentiment analysis** (Positive/Negative/Neutral)
- 🌐 Translate summaries from **English to Hindi**
- 🔊 Convert Hindi text summaries to **audio (mp3)**
- 📊 Generate **comparative analysis** of article sentiment
- 🖥️ **Streamlit UI** and **Flask API** for interaction

---

## 🏗️ Project Structure

```bash
news-sentiment-analysis/
│
├── api.py               # Flask backend for processing and analysis
├── app.py               # Streamlit frontend interface
├── utils.py             # Helper functions (summarization, sentiment, TTS, etc.)
├── requirements.txt     # List of dependencies
├── .gitignore           # Files to ignore in Git
└── README.md            # This file


🚀 Getting Started
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/news-sentiment-analysis.git
cd news-sentiment-analysis
2. Create & activate virtual environment
bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Add your NewsAPI key
Replace the NEWSAPI_KEY value in api.py:

python
Copy
Edit
NEWSAPI_KEY = "your_actual_newsapi_key"
🧪 How to Run
Run Flask API
bash
Copy
Edit
python api.py
Run Streamlit App
In a new terminal:

bash
Copy
Edit
streamlit run app.py
🧠 Tech Stack
Python

Flask – REST API

Streamlit – Web UI

Googletrans – Translation to Hindi

gTTS – Text-to-speech in Hindi

TextBlob – Sentiment analysis

NewsAPI – News article source

🔐 Disclaimer
Do not commit your real API keys. Use .env or config management if you deploy this publicly.
