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
from getpass import getpass
from flask import Flask
from threading import Thread

# Set up Flask for Keep Alive (to prevent Replit from stopping)
app = Flask(__name__)

@app.route('/')
def home():
    return "FreeBitco.in Bot is running!"

# Configure Chrome Options for Replit or local environment
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

# Initialize WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("WebDriver started successfully!")
except Exception as e:
    print(f"Failed to start WebDriver: {e}")
    exit()

# Function to automate FreeBitco.in ROLL
def auto_roll_freebitco(email, password):
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

    # Loop to click ROLL button every hour
    while True:
        try:
            roll_button = driver.find_element(By.ID, "free_play_form_button")
            roll_button.click()
            print(f"ROLL clicked successfully for {email} - {time.ctime()}")
            wait_time = 3600 + random.randint(10, 120)  # Wait 1 hour + random delay
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error during ROLL: {e}")
            time.sleep(60)  # Retry after 1 minute if error occurs

# Get user credentials securely
email = input("Enter your FreeBitco.in email: ")
password = getpass("Enter your password (hidden): ")

# Run the bot in a separate thread and start Flask
if __name__ == "__main__":
    Thread(target=auto_roll_freebitco, args=(email, password)).start()
    app.run(host='0.0.0.0', port=8080)

# Uncomment to close driver (not recommended for continuous running)
# driver.quit()