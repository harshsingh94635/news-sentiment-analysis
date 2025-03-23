# app.py
import streamlit as st
import requests
import os

st.set_page_config(page_title="News Summarization & Sentiment Analysis (Hindi TTS)", layout="wide")

st.title("News Summarization & Sentiment Analysis (Hindi TTS)")
st.write(
    "Enter a company name, and we'll fetch articles, analyze sentiment, and generate Hindi audio for each summary.")

company_name = st.text_input("Company Name", "")

if st.button("Analyze News"):
    if not company_name.strip():
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Analyzing..."):
            try:
                url = "http://127.0.0.1:5000/analyze"
                response = requests.post(url, json={"company": company_name}, timeout=30)

                if response.status_code == 200:
                    data = response.json()

                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        st.subheader(f"News Analysis for {data.get('Company', 'N/A')}")
                        articles = data.get("Articles", [])

                        for idx, art in enumerate(articles, start=1):
                            st.markdown(f"### Article {idx}")
                            st.markdown(f"**Title:** {art['title']}")
                            st.markdown(f"**URL:** {art['url']}")
                            st.markdown(f"**Summary (English):** {art['summary']}")
                            st.markdown(f"**Sentiment:** {art['sentiment']}")

                            # Display Hindi TTS audio for the article's summary
                            audio_file = art.get("audio_file")
                            if audio_file and os.path.exists(audio_file):
                                st.markdown("**Summary Audio (Hindi):**")
                                audio_bytes = open(audio_file, 'rb').read()
                                st.audio(audio_bytes, format='audio/mp3')
                            else:
                                st.warning("No audio file for this article's summary.")
                            st.write("---")

                        st.subheader("Comparative Analysis")
                        st.json(data.get("Comparative Analysis", {}))

                        st.subheader("Final Sentiment Analysis")
                        st.write("**English:**", data.get("Final Sentiment Analysis (English)", ""))
                        st.write("**Hindi:**", data.get("Final Sentiment Analysis (Hindi)", ""))

                        # Display final summary Hindi TTS audio
                        final_audio = data.get("Final Audio File")
                        if final_audio and os.path.exists(final_audio):
                            st.subheader("Final Summary Audio (Hindi)")
                            audio_bytes = open(final_audio, 'rb').read()
                            st.audio(audio_bytes, format='audio/mp3')
                        else:
                            st.warning("Final audio file not found.")
                else:
                    st.error(f"Server error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")
