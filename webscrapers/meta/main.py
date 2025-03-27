# ..........NOT FUNCTIONAL..........



import requests
import json
import os

# Replace with your actual User Access Token
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("Access Token is not set in environment variables!")

# Facebook Graph API URL
graph_url = 'https://graph.facebook.com/v22.0/me/feed'

# Define parameters for the request
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'message,created_time',  # Fields we want from the posts (message and timestamp)
    'limit': 10  # Limit the number of posts retrieved (optional)
}

# Send a GET request to the Graph API
response = requests.get(graph_url, params=params)
print(f"Response Status Code: {response.status_code}")
print(f"Response Content: {response.text}")  # This will show the entire raw response

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    posts = data.get('data', [])
    paging = data.get('paging', {})
    next_page_url = paging.get('next')

    # Optionally filter posts by a keyword
    keyword = "fitness"  # Replace with the keyword you're looking for
    filtered_posts = [post for post in posts if keyword.lower() in post.get('message', '').lower()]

    # Print the filtered posts
    for post in filtered_posts:
        print(f"Post: {post['message']}")
        print(f"Created Time: {post['created_time']}")
        print("=" * 50)
else:
    print(f"Error fetching posts: {response.status_code}, {response.text}")
