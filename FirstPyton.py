from newsapi import NewsApiClient

# Replace with your API key
API_KEY = 'dd605ff3b87d4b9ba1eb27bf35ba0d20'

# Initialize client
newsapi = NewsApiClient(api_key=API_KEY)

# Fetch top headlines
def fetch_top_headlines(query='india', language='en', page_size=10):
    try:
        top_headlines = newsapi.get_everything(q=query,
                                               language=language,
                                               sort_by='publishedAt',
                                               page_size=page_size)
        articles = top_headlines['articles']
        for i, article in enumerate(articles, start=1):
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Published At: {article['publishedAt']}")
            print(f"   URL: {article['url']}\n")
    except Exception as e:
        print("Error fetching news:", e)

# Example usage
fetch_top_headlines(query='stock market', language='en')