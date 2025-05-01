import requests

print("🚀 Running the latest version of the script...")

ACCESS_TOKEN = 'EACKMnZBcrkwQBO9GPAF4iLbwZBmWWIzntI9DjjdHGb2rnTXo26yZBZC7JuBnrf8oEPLzxPcxycscI58xfaQYAdCpJ9CyzDFdNP2PCAiASZBjtRV9gQzjGtFTZCeMmhNSusFEq9QZAl6hCPUW19dZA9cHuyhEZChL1OIHYpZA9EGMjFdhCOe7lQRipiPhWPpaI8KcsPhV1flW67kdViv4INcFNAxPJSkjGy'
PAGE_ID = '639786179217551'
SEARCH_TERM = input("Enter search term: ").strip()

def get_facebook_posts():
    print("🔍 Starting API query to Facebook...")

    url = f'https://graph.facebook.com/v22.0/{PAGE_ID}/posts'
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'message,created_time',
        'limit': 100
    }

    matching_posts = []
    total_posts_checked = 0

    while url:
        print(f"➡️  Requesting: {url}")
        response = requests.get(url, params=params).json()

        if 'data' not in response:
            print("❌ Error in response or no access:")
            print(response)
            break

        posts = response['data']
        print(f"📄 Retrieved {len(posts)} post(s) from this page of results.")
        total_posts_checked += len(posts)

        for post in posts:
            message = post.get('message', '')
            if SEARCH_TERM.lower() in message.lower():
                matching_posts.append({
                    'message': message,
                    'created_time': post['created_time']
                })

        # Pagination
        paging = response.get('paging', {})
        url = paging.get('next')
        params = {}  # Clear params after first request

    print(f"✅ Finished fetching posts. Total checked: {total_posts_checked}")
    return matching_posts

# Run the function
posts = get_facebook_posts()

# Output results
if posts:
    print(f"\n🔎 Found {len(posts)} matching post(s) containing '{SEARCH_TERM}':\n")
    for post in posts:
        print(f"🕓 {post['created_time']}\n✏️  {post['message']}\n")
else:
    print(f"\n⚠️ No posts found containing '{SEARCH_TERM}'.")