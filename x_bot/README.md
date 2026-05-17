# Insured618 X (Twitter) Auto-Posting Bot 🤖

This is a simple, lightweight Python bot designed to automate your Twitter marketing updates for your website and share high-quality financial & insurance tips.

## 📁 Directory Structure
* `bot.py`: The main script that handles posting to X using API v2.
* `tips.json`: A list of premium, pre-written Canadian insurance and tax-planning tips.
* `.env.example`: A template for secure API keys.
* `requirements.txt`: Python package dependencies.

---

## 🚀 Setup Instructions

### 1. Install Dependencies
Open your terminal, navigate to the `x_bot` directory, and run:
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
1. Register/Login to [X Developer Portal](https://developer.x.com/) with your Twitter account.
2. Sign up for the **Free Tier**.
3. Create a Project & App.
4. Ensure your App permissions are set to **Read and Write** in the User Authentication Settings (choose "Web App, Automated App or Bot").
5. Copy your 4 Keys.
6. Rename `.env.example` in this folder to `.env`:
   ```bash
   mv .env.example .env
   ```
7. Open `.env` and fill in your keys.

---

## ⚙️ How to Run the Bot

The bot has two primary functions:

### 1. Post a Random Tip 💡
Selects a random high-quality tip from `tips.json` and posts it to your account. Great for daily scheduled posts!
```bash
python bot.py --tip
```

### 2. Post a Website Update Alert 📢
Analyzes your latest git commit, identifies which service pages have been updated (e.g., Segregated Funds, Payout Annuities), formats a friendly announcement in Chinese, and posts it with a link to your home page.
```bash
python bot.py --update
```

---

## 🕒 Automating Your Posts (Bonus)
You can schedule these scripts to run automatically on your computer or server using **Cron** (Mac/Linux) or **Task Scheduler** (Windows).

For example, to post a tip every day at 9:00 AM on Mac, open `crontab -e` and add:
```text
0 9 * * * cd /Users/mac325/insured618_web/x_bot && python bot.py --tip
```
