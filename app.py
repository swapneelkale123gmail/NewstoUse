import streamlit as st
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob
import spacy
from fuzzywuzzy import fuzz

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Stock News Analyzer", layout="centered")
st.title("📈 Stock News Sentiment Analyzer (CSV-Driven)")

# Input: NewsAPI Key
api_key = st.text_input("🔑 Enter your NewsAPI Key", type="password")
if not api_key:
    st.stop()

newsapi = NewsApiClient(api_key=api_key)

# Upload CSV file
st.markdown("📄 **Upload CSV with columns: 'Symbol', 'Company Name'**")
uploaded_file = st.file_uploader("Upload your stock watchlist CSV", type="csv")
if uploaded_file is None:
    st.stop()

# Load stock list
try:
    stock_df = pd.read_csv(uploaded_file)
    st.write("✅ CSV Loaded:", stock_df.head())
    stock_watchlist = dict(zip(stock_df['Symbol'], stock_df['Company Name']))
except Exception as e:
    st.error(f"❌ Error reading CSV: {e}")
    st.stop()

# Keyword input
keywords = st.text_input("📝 Enter news keywords (comma-separated)", value="stocks, finance, economy")

# Parameters
pages = st.slider("📄 Number of pages to fetch", min_value=1, max_value=10, value=2)
threshold = st.slider("🎯 Matching sensitivity (lower = looser)", min_value=60, max_value=100, value=80)

# Utilities
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON"]]

def match_stock(entities, stock_watchlist, threshold=90):
    matches = []
    for symbol, name in stock_watchlist.items():
        name_clean = name.lower().strip()
        for ent in entities:
            ent_clean = ent.lower().strip()
            if fuzz.ratio(name_clean, ent_clean) >= threshold:
                matches.append((symbol, name))
                break
    return matches

def fetch_news(query_keywords, pages=5):
    query = " OR ".join(query_keywords)
    all_articles = []
    for page in range(1, pages + 1):
        try:
            response = newsapi.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                page_size=100,
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

# Run Analysis
if st.button("🚀 Run News Analysis"):
    st.write("🕵️ Fetching news...")
    articles = fetch_news([kw.strip() for kw in keywords.split(",")], pages=pages)
    st.write(f"✅ Fetched {len(articles)} articles")

    results = []
    for article in articles:
        title = article.get('title') or ''
        desc = article.get('description') or ''
        url = article.get('url')
        content = f"{title}. {desc}"

        entities = extract_entities(content)
        st.write("🧠 Entities:", entities)

        matched_stocks = match_stock(entities, stock_watchlist, threshold=threshold)
        sentiment = analyze_sentiment(content)

        if matched_stocks:
            for symbol, name in matched_stocks:
                results.append({
                    "Stock Symbol": symbol,
                    "Company Name": name,
                    "News Title": title,
                    "Sentiment": sentiment,
                    "URL": url
                })

    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)
        csv = df_results.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results as CSV", data=csv, file_name="news_results.csv", mime="text/csv")
    else:
        st.warning("⚠️ No matching stocks found. Try lowering the threshold or checking your company names.")
