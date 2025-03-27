import praw

REDDIT_CLIENT_ID = "pEXEG4B218Rr4bKrPPZpuQ"
REDDIT_CLIENT_SECRET = "0o6MJaOdAnjPhECWKz_rZdXJ3lWflw"
REDDIT_USER_AGENT = "EchoSentiment"

def scrape_reddit_posts(company_name, limit=50, subreddit="all"):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    posts = []
    for post in reddit.subreddit(subreddit).search(company_name, limit=limit):
        combined_text = f"{post.title} {post.selftext}".strip()
        posts.append(combined_text)
    
    return posts
