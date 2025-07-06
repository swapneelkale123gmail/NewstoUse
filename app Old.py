# app.py
import streamlit as st
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob
import spacy
import os

# Load SpaCy model once
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Stock News Sentiment Analyzer", layout="wide")
st.title("📈 Stock News Sentiment Analyzer (CSV-Driven)")

# 1. API key input
api_key = st.text_input("🔑 Enter your NewsAPI Key", type="password")

# 2. Upload stock CSV
uploaded_file = st.file_uploader("📄 Upload CSV with columns: 'Symbol', 'Company Name'", type=["csv"])

# 3. Keywords input
keywords = st.text_input("🧵 Enter Keywords to search (comma-separated)", value="stocks, finance, economy, earnings")

# 4. Run button
if api_key and uploaded_file and keywords and st.button("🚀 Run News Analysis"):

    # ✅ Load stock list
    try:
        stock_df = pd.read_csv(uploaded_file)
        stock_watchlist = dict(zip(stock_df['Symbol'], stock_df['Company Name']))
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    # ✅ Initialize NewsAPI
    try:
        newsapi = NewsApiClient(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize NewsAPI: {e}")
        st.stop()

    # ✅ Function: Fetch news
def fetch_news(query_keywords, pages=5):
    query = " OR ".join(query_keywords)
    all_articles = []
    
    for page in range(1, pages + 1):
        try:
            response = newsapi.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                page_size=100,  # max allowed per call
                page=page
            )
            articles = response.get('articles', [])
            if not articles:
                break
            all_articles.extend(articles)
        except Exception as e:
            st.warning(f"Error on page {page}: {e}")
            break

    return all_articles



    # ✅ Function: Extract organizations using SpaCy
    def extract_entities(text):
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ == 'ORG']

    # ✅ Function: Match stocks based on NLP
    def match_stock(entities):
        matched = []
        for symbol, company in stock_watchlist.items():
            company_lower = company.lower()
            for entity in entities:
                if company_lower in entity.lower() or entity.lower() in company_lower:
                    matched.append((symbol, company))
        return matched

    # ✅ Fallback: Raw text scan if NLP fails
    def fallback_match(text):
        matched = []
        text_lower = text.lower()
        for symbol, company in stock_watchlist.items():
            if company.lower() in text_lower:
                matched.append((symbol, company))
        return matched

    # ✅ Sentiment function
    def analyze_sentiment(text):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"

    # ✅ Start processing
    articles = fetch_news([kw.strip() for kw in keywords.split(",")])
    results = []

    with st.spinner(f"🔍 Analyzing {len(articles)} news articles..."):
        for article in articles:
            title = article.get('title', '')
            desc = article.get('description', '')
            url = article.get('url', '')
            content = f"{title}. {desc}"

            entities = extract_entities(content)
            matched = match_stock(entities)
            if not matched:
                matched = fallback_match(content)

            sentiment = analyze_sentiment(content)

            if matched:
                for symbol, name in matched:
                    results.append([symbol, name, title, sentiment, url])
            else:
                results.append(["", "", title, sentiment, url])

    if results:
        df_result = pd.DataFrame(results, columns=["Stock Symbol", "Company Name", "News Title", "Sentiment", "URL"])
        st.success(f"✅ Processed {len(results)} articles.")
        st.dataframe(df_result, use_container_width=True)

        # ✅ Download button
        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results as CSV", csv, file_name="stock_news_sentiment.csv", mime="text/csv")
    else:
        st.warning("⚠️ No matching articles found.")
