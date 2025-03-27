import requests
import datetime
import os


BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    raise ValueError("Bearer Token is not set in environment variables!")

def create_headers():
    """Create headers for Twitter API request."""
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}


def search_tweets(query, max_results):
    """
    Search tweets based on a keyword.

    Parameters:
        query (str): Search term or hashtag.
        max_results (int): Number of tweets to retrieve (max 100 per request).

    Returns:
        list: JSON response containing tweet data.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": f"{query} lang:en",
        "max_results": max_results,
        "tweet.fields": "created_at,text,lang"
    }

    response = requests.get(url, headers=create_headers(), params=params)

    print(f"Remaining requests: {response.headers.get('x-rate-limit-remaining')}")
    reset_timestamp = int(response.headers.get('x-rate-limit-reset', 0))  # Default to 0 if key is missing
    reset_time = datetime.datetime.fromtimestamp(reset_timestamp)
    print(f"Rate limit reset time (epoch): {reset_time}")

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None


if __name__ == "__main__":
    while True:
        selection = input("Would you like to make a search? (y/n) ").lower()

        if selection == 'y':

            query = input("What term would you like to query for? ")
            if query:
                while True:
                    max_results = input("How many posts would you like to retrieve? ")
                    try:
                        max_results = int(max_results)
                        if max_results > 0:
                            break
                        else:
                            print("Please enter a positive integer.")
                    except ValueError:
                        print("Invalid input, please enter a valid integer.")

                if max_results:
                    print("Querying...")

                    tweets = search_tweets(query, max_results=max_results)
                    if tweets:
                        for tweet in tweets.get("data", []):
                            print(f"Tweet: {tweet['text']}\nTimestamp: {tweet['created_at']}\n")

        elif selection == 'n':
            print("Ok")
            break
        else:
            print("Not a valid input.")
