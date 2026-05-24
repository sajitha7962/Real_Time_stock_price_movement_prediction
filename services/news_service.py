import requests

from config import Config

API_KEY = Config.NEWS_API_KEY

def get_news(stock):
    try:
        url = f"https://newsapi.org/v2/everything?q={stock}&apiKey={API_KEY}&pageSize=5"

        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        headlines = [article["title"] for article in articles if article.get("title")]

        print("NEWS HEADLINES:", headlines)

        return headlines

    except Exception as e:
        print("NEWS ERROR:", e)
        return []