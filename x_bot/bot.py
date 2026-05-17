import os
import sys
import json
import random
import argparse
import subprocess
from pathlib import Path
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path)

# Retrieve X API Credentials
API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

def get_twitter_client():
    """Initializes and returns the Twitter/X API client."""
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("❌ Error: Missing Twitter API credentials in .env file!")
        print("Please check x_bot/.env and fill in your keys.")
        sys.exit(1)
    
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Twitter Client: {e}")
        sys.exit(1)

def post_tweet(text):
    """Utility to post a tweet using X API v2."""
    client = get_twitter_client()
    try:
        print(f"🚀 Attempting to tweet:\n\"{text}\"\n")
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        print(f"✅ Success! Tweet posted successfully. Tweet ID: {tweet_id}")
        return tweet_id
    except Exception as e:
        print(f"❌ Failed to post tweet: {e}")
        sys.exit(1)

def handle_tip():
    """Loads a random tip from tips.json and posts it."""
    tips_file = Path(__file__).resolve().parent / 'tips.json'
    if not tips_file.exists():
        print(f"❌ Error: {tips_file} not found!")
        sys.exit(1)
        
    with open(tips_file, 'r', encoding='utf-8') as f:
        tips = json.load(f)
        
    if not tips:
        print("❌ Error: No tips found in tips.json!")
        sys.exit(1)
        
    selected_tip = random.choice(tips)
    post_tweet(selected_tip['text'])

def get_recent_git_updates():
    """Finds recently modified .html files in the repository using Git."""
    try:
        # Check files modified in the latest commit
        result = subprocess.run(
            ["git", "log", "-1", "--name-only", "--pretty="],
            capture_output=True,
            text=True,
            check=True
        )
        files = [line.strip() for line in result.stdout.splitlines() if line.strip().endswith('.html')]
        return files
    except Exception as e:
        print(f"⚠️ Could not read git log: {e}")
        return []

def handle_update():
    """Detects modified files and tweets a site update notification."""
    updated_files = get_recent_git_updates()
    
    if not updated_files:
        print("ℹ️ No recent HTML updates detected in the last git commit.")
        print("Defaulting to a general site update announcement...")
        tweet_text = "📢 Insured618 网站已更新！我们为您量身定制的加拿大财富管理与保险策略平台已经上线最新版。欢迎访问主页免费预约评估：https://insured618.netlify.app/ #加拿大理财 #资产规划"
        post_tweet(tweet_text)
        return

    # Map file names to friendly Chinese names
    friendly_names = {
        "index.html": "首页及预约系统",
        "wealth.html": "财富与退休规划主页",
        "business.html": "企业主专区方案",
        "segregated-funds.html": "保本基金 (Segregated Funds) 全面解析",
        "payout-annuities.html": "给付年金 (Payout Annuities) 介绍",
        "term.html": "定期人寿保险",
        "par.html": "分红终身寿险",
        "ci.html": "重大疾病保险",
        "health.html": "健康与牙科保险",
        "about.html": "关于我们品牌故事"
    }

    # Filter out files we have custom names for or just use their raw name
    items = []
    for f in updated_files:
        filename = os.path.basename(f)
        if filename in friendly_names:
            items.append(friendly_names[filename])
        else:
            items.append(filename.replace(".html", " 页面"))

    items_str = "、".join(items[:3])  # Limit to max 3 items in tweet text
    tweet_text = f"📢 网站更新速递：我们的【{items_str}】已完成全新升级！量身定制保障，让您的财富更稳健。立即访问主页预约免费咨询：https://insured618.netlify.app/ #加拿大生活 #财务规划"
    post_tweet(tweet_text)

def main():
    parser = argparse.ArgumentParser(description="Insured618 X (Twitter) Auto Posting Bot")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tip", action="store_true", help="Post a random insurance/tax tip from tips.json")
    group.add_argument("--update", action="store_true", help="Check for recent website HTML updates and post about them")
    
    args = parser.parse_args()
    
    if args.tip:
        handle_tip()
    elif args.update:
        handle_update()

if __name__ == "__main__":
    main()
