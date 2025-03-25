"""
FreeBitco.in Bot - Automates the "ROLL" button to earn free Bitcoin (BTC).
WARNING: Using this bot violates FreeBitco.in's Terms of Service and may result in a ban.
Use at your own risk, preferably with a test account.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import os

# Get credentials from environment variables (set in GitHub Secrets)
email = os.getenv("FREEBITCO_EMAIL")
password = os.getenv("FREEBITCO_PASSWORD")
proxy = os.getenv("PROXY")  # Optional: Format: http://username:password@host:port

if not email or not password:
    print("Error: FREEBITCO_EMAIL or FREEBITCO_PASSWORD not set in environment variables.")
    exit()

# Configure Chrome Options for GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
if proxy:
    chrome_options.add_argument(f'--proxy-server={proxy}')

# Initialize WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("WebDriver started successfully!")
except Exception as e:
    print(f"Failed to start WebDriver: {e}")
    exit()

# Function to automate FreeBitco.in ROLL
def auto_roll_freebitco():
    print("Starting FreeBitco.in bot...")
    try:
        driver.get("https://freebitco.in")
        print("Loaded FreeBitco.in page successfully")
    except Exception as e:
        print(f"Failed to load FreeBitco.in page: {e}")
        return

    # Log in to FreeBitco.in
    try:
        driver.find_element(By.ID, "login_form_email").send_keys(email)
        driver.find_element(By.ID, "login_form_password").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(5)
        print("Logged in successfully!")
    except Exception as e:
        print(f"Login failed: {e}")
        return

    # Click ROLL button 4 times (4 hours)
    for _ in range(4):
        try:
            roll_button = driver.find_element(By.ID, "free_play_form_button")
            roll_button.click()
            print(f"ROLL clicked successfully for {email} - {time.ctime()}")
            wait_time = 3600 + random.randint(10, 120)  # Wait 1 hour + random delay
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error during ROLL: {e}")
            time.sleep(60)

# Run the bot
if __name__ == "__main__":
    auto_roll_freebitco()
    driver.quit()