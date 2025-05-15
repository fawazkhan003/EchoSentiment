from redditapi import scrape_reddit_posts
from sentimentalg import analyze_sentiment
import csv
import os
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys


def main():
    search_term = input("Enter a search term: ").strip()
    limit = input("How many posts would you like to retrieve? (Default 100): ").strip()
    limit = int(limit) if limit.isdigit() else 100

    #posts_per_day = max(1, limit // 10)
    #posts = scrape_reddit_posts(search_term, posts_per_day=posts_per_day, days=10)
    posts = scrape_reddit_posts(search_term, limit=limit)

    os.makedirs("Data", exist_ok=True)

    filename = f"Data/reddit_posts_{search_term.replace(' ', '_')}.csv"

    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "text", "sentiment"])
        writer.writeheader()
        for post in tqdm(posts, desc="Analyzing Sentiment", unit="post"):
            sentiment = analyze_sentiment(post["text"])
            writer.writerow({
                "timestamp": post["timestamp"],
                "text": post["text"],
                "sentiment": sentiment
            })

    print(f"\n{len(posts)} posts saved to '{filename}' including sentiment.")
    return filename


def plot_sentiment_over_time(csv_path):
    df = pd.read_csv(csv_path)

    # Remove outlier dates
    df = filter_outliers(df, "timestamp")

    # Now convert timestamp to date and continue as before...
    df["date"] = pd.to_datetime(df["timestamp"])


    sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df["sentiment_score"] = df["sentiment"].map(sentiment_map)

    # Set date as index
    df.set_index("date", inplace=True)

    # Resample by week (W) and calculate mean sentiment
    weekly_sentiment = df["sentiment_score"].resample("W").mean()

    plt.figure(figsize=(10, 5))
    weekly_sentiment.plot(marker='o', linestyle='-')

    plt.title("Weekly Average Sentiment Over Time")
    plt.xlabel("Week")
    plt.ylabel("Average Sentiment Score")
    plt.grid(True)
    plt.tight_layout()

    graph_path = csv_path.replace(".csv", "_weekly_sentiment_graph.png")
    plt.savefig(graph_path)
    plt.show()

    print(f"Weekly sentiment graph saved to: {graph_path}")

    sys.exit(0)


'''
def plot_sentiment_over_time(csv_path):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Convert timestamp string to datetime object and extract the date
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date

    # Map sentiment to numeric values
    sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df["sentiment_score"] = df["sentiment"].map(sentiment_map)

    # Group by date and calculate average sentiment score
    daily_sentiment = df.groupby("date")["sentiment_score"].mean()

    # Plot the sentiment trend
    plt.figure(figsize=(10, 5))
    daily_sentiment.plot(kind="line", marker='o', linestyle='-')

    plt.title("Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.grid(True)
    plt.tight_layout()

    # Save to file
    graph_path = csv_path.replace(".csv", "_sentiment_graph.png")
    plt.savefig(graph_path)
    plt.show()

    print(f"Sentiment graph saved to: {graph_path}")
'''

def filter_outliers(df, date_column="timestamp"):
    # Convert to datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Get the interquartile range (IQR) for the dates
    q1 = df[date_column].quantile(0.25)
    q3 = df[date_column].quantile(0.75)
    iqr = q3 - q1

    # Define bounds to filter out outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Filter dataframe
    filtered_df = df[(df[date_column] >= lower_bound) & (df[date_column] <= upper_bound)]
    return filtered_df


if __name__ == "__main__":
    filename = main()
    plot_sentiment_over_time(filename)