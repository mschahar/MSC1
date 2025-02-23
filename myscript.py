from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# 🔹 Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7607310655:AAEBc_-jzx47VRBLWjqm2sceyInZ_d-z5lg"  # Replace with your bot token
CHAT_ID = "163447880"  # Replace with your chat ID

# 🔹 Product URL & Pincode
PRODUCT_URL = "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d211hbcz/buy/"  # Change this
PINCODE = "305001"  # Change this to your desired pincode

# 🔹 Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening the browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

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

        # 🔹 Try fetching stock status via JavaScript
        stock_status = driver.execute_script("return ga4_dataset?.product?.stock_status;")
        print(f"🔍 Debug: JavaScript Stock Status - {stock_status}")  # Debugging

        # 🔹 Backup Method: Extract stock status from page text
        try:
            stock_text_element = driver.find_element(By.CLASS_NAME, "stock-status")  # Update if needed
            stock_text = stock_text_element.text.strip().lower()
            print(f"🔍 Debug: Stock Status from Page - {stock_text}")
        except:
            stock_text = None
            print("⚠️ Could not find stock status in page text.")

        # 🔹 Determine Final Stock Status
        final_status = (stock_status or stock_text or "").lower().strip()

        if final_status in ["out_of_stock", "oos", "out", "currently unavailable", "not available"]:
            print("❌ Product is out of stock. No notification sent.")
        elif final_status in ["in_stock", "available", "in", "add to cart", "buy now"]:
            send_telegram_message(f"✅ The product is now available! Buy here: {PRODUCT_URL}")
        else:
            print(f"⚠️ Unknown stock status: {final_status}. No notification sent.")

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

# 🔹 Run once
check_availability()
