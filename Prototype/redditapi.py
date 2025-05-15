from psaw import PushshiftAPI
from datetime import datetime, timedelta
import praw
from tqdm import tqdm

REDDIT_CLIENT_ID = "pEXEG4B218Rr4bKrPPZpuQ"
REDDIT_CLIENT_SECRET = "0o6MJaOdAnjPhECWKz_rZdXJ3lWflw"
REDDIT_USER_AGENT = "EchoSentiment"

'''
def scrape_reddit_posts(search_term, posts_per_day, days=10, subreddit="all"):
    # PRAW for content retrieval
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    api = PushshiftAPI()

    posts = []
    now = datetime.utcnow()

    for i in tqdm(range(days), desc="Fetching Reddit posts by day"):
        end_time = int((now - timedelta(days=i)).timestamp())
        start_time = int((now - timedelta(days=i+1)).timestamp())

        gen = api.search_submissions(
            q=search_term,
            after=start_time,
            before=end_time,
            subreddit=subreddit,
            sort_type="score",
            sort="desc",
            limit=posts_per_day,
            filter=["id"]
        )

        for submission in tqdm(gen, desc=f"Day {i + 1}/{days}", leave=False):
            try:
                praw_post = reddit.submission(id=submission.id)
                combined_text = f"{praw_post.title} {praw_post.selftext}".strip()
                timestamp = datetime.utcfromtimestamp(praw_post.created_utc).isoformat()
                posts.append({
                    "timestamp": timestamp,
                    "text": combined_text
                })
            except Exception as e:
                continue  # skip any posts that error out

    return posts

'''

def scrape_reddit_posts(company_name, limit=50, subreddit="all"):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    posts = []
    search_results = reddit.subreddit(subreddit).search(company_name, limit=limit)

    for post in tqdm(search_results, total=limit, desc="Fetching Reddit posts"):
        combined_text = f"{post.title} {post.selftext}".strip()
        timestamp = datetime.utcfromtimestamp(post.created_utc).isoformat()
        posts.append({
            "text": combined_text,
            "timestamp": timestamp
        })
    return posts
