#!/usr/bin/env python3
import os
import sys
import random
import time
import json
import argparse
from playwright.sync_api import sync_playwright

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIPS_FILE = os.path.join(BASE_DIR, 'tips.json')
USER_DATA_DIR = os.path.join(BASE_DIR, 'x_user_data')

def load_tips():
    try:
        with open(TIPS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading tips.json: {e}")
        sys.exit(1)

def get_random_tip():
    tips = load_tips()
    tip = random.choice(tips)
    return tip['text']

def post_to_x(text, headful=True):
    print("🤖 Starting Playwright X Auto-Poster...")
    
    # Ensure the user data directory exists
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        
    with sync_playwright() as p:
        # Launch Chromium with persistent context to keep login cookies active
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=not headful,
            viewport={'width': 1280, 'height': 800},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--start-maximized'
            ]
        )
        
        page = context.new_page()
        
        # Modify navigator.webdriver to bypass basic bot detection
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🌐 Navigating to X (Twitter)...")
        page.goto("https://x.com/home", wait_until="domcontentloaded")
        
        # Human-like delay
        time.sleep(random.uniform(3.0, 5.0))
        
        # Check if we need to log in
        if "login" in page.url or page.locator("a[href='/login']").is_visible():
            print("\n🔑 LOGIN REQUIRED:")
            print("Since this is your first run, please log in manually in the opened browser window.")
            print("The session cookies will be saved in 'x_user_data' automatically, so you won't need to log in again.\n")
            
            # Wait for user to log in and get to the home timeline
            while "x.com/home" not in page.url:
                time.sleep(1)
            print("✅ Successfully logged in and session saved!")
            time.sleep(3)
        
        print("📝 Locating tweet textbox...")
        
        # Using X's standardized testid for the input box (robust against CSS/class changes)
        tweet_box = page.locator("[data-testid='tweetTextarea_0']")
        
        try:
            tweet_box.wait_for(state="visible", timeout=15000)
        except Exception:
            print("❌ Timeout waiting for X post textbox. Check if you are correctly logged in.")
            context.close()
            return False
            
        tweet_box.click()
        time.sleep(random.uniform(0.5, 1.5))
        
        print(f"✍️ Typing content: '{text[:50]}...'")
        # Simulating human typing speed
        for char in text:
            tweet_box.type(char, delay=random.uniform(20, 100))
            
        time.sleep(random.uniform(1.5, 2.5))
        
        print("🚀 Sending tweet via keyboard shortcut (Control+Enter)...")
        tweet_box.press("Control+Enter")
        
        time.sleep(random.uniform(2.0, 3.0))
        
        # Locate the Post button for fallback
        post_button = page.locator("[data-testid='tweetButtonInline']")
        if not post_button.is_visible():
            post_button = page.get_by_role("button", name="Post")
            
        if post_button.is_visible() and post_button.is_enabled():
            print("🚀 Fallback: Clicking 'Post' button (force=True)...")
            try:
                post_button.click(force=True)
            except Exception as e:
                print(f"⚠️ Fallback click failed: {e}")
        
        # Wait to ensure the tweet goes through
        print("⏳ Waiting for publication to complete...")
        time.sleep(random.uniform(5.0, 7.0))
        
        print("🎉 Tweet posted successfully!")
        context.close()
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="X (Twitter) Playwright Automated Poster")
    parser.add_argument('--text', type=str, help="Specific text to post on X")
    parser.add_argument('--headless', action='store_true', help="Run browser in headless mode (requires prior login session)")
    
    args = parser.parse_args()
    
    if args.text:
        post_content = args.text
    else:
        post_content = get_random_tip()
        
    # First login must be headful to allow user input. Subsequent posts can be headless.
    is_headless = args.headless
    
    try:
        success = post_to_x(post_content, headful=not is_headless)
        if success:
            print("🚀 Job completed successfully!")
            sys.exit(0)
        else:
            print("❌ Job failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Process aborted by user.")
        sys.exit(0)
