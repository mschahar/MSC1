from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

# 🔹 Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7607310655:AAEBc_-jzx47VRBLWjqm2sceyInZ_d-z5lg"  # Replace with your bot token
CHAT_ID = "163447880"  # Replace with your chat ID

# 🔹 Product URL & Pincode
PRODUCT_URL = "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201aseu/buy/"  # Change this
PINCODE = "305001"  # Change this to your desired pincode

# 🔹 Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening the browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def check_availability():
    try:
        driver.get(PRODUCT_URL)
        time.sleep(5)  # Wait for page to load completely

        # 🔹 Enter Pincode
        try:
            pincode_box = driver.find_element(By.ID, "product-pincode-01")  # Update if different
            pincode_box.clear()
            pincode_box.send_keys(PINCODE)
            pincode_box.send_keys(Keys.RETURN)  # Press Enter
            time.sleep(5)  # Wait for stock status to update
        except Exception as e:
            print("⚠️ Pincode input box not found! Skipping this step.")

        # 🔹 Get Page Source and Check for Out of Stock Message
        page_source = driver.page_source.lower()  # Convert to lowercase for consistency

        if "sorry ! currently we are out of stock" in page_source:
            print("❌ Product is OUT of stock.")
        else:
            print("✅ Product is IN STOCK! Sending notification...")
            send_telegram_message(f"✅ The product is now available! Buy here: {PRODUCT_URL}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        driver.quit()  # Close browser session

# 🔹 Function to Send Telegram Notification
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("📩 Telegram message sent successfully!")
    else:
        print(f"⚠️ Failed to send message: {response.json()}")

# 🔹 Run every 30 minutes
while True:
    check_availability()
    time.sleep(1800)  # 30 minutes delay
