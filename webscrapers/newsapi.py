# news_fetcher.py
import requests

def fetch_news_articles(api_key, query="News Corp Australia", max_articles=50):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={api_key}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Failed to fetch articles:", response.text)
        return []

    articles = response.json().get("articles", [])
    return [
        f"{article['title']}. {article.get('description', '')}"
        for article in articles
    ]
