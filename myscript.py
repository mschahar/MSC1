from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

# 🔹 Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7607310655:AAEBc_-jzx47VRBLWjqm2sceyInZ_d-z5lg"  # Replace with your bot token
CHAT_IDS = ["163447880", "826574622"]  # Add multiple chat IDs here

# 🔹 Products & Pincode
PRODUCTS = {
    "🌟 LG AC 5 Star 🌟": "https://www.lg.com/in/air-conditioners/split-air-conditioners/us-q19bnze/buy/",
    "🏆 1st 185L 5S 🏆": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201ascu/buy/",
    "🏆 2nd 185L 5S 🏆": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abeu/buy/",
    "🏆 3rd 185L 5S 🏆": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201aseu/buy/",
    "🏆 4th 185L 5S 🏆": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abcu/buy/",
    "🔥 1st 185L 4S 🔥": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d199obey/buy/",
    "🔥 2nd 185L 4S 🔥": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d199osey/buy/",
    "🔥 3rd 185L 4S 🔥": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201ascy/buy/",
    "🔥 4th 185L 4S 🔥": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abcy/buy/",
}
PINCODE = "305001"  # Change this to your desired pincode

# 🔹 Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening the browser
driver = webdriver.Chrome(options=options)

def check_availability(product_name, product_url):
    try:
        driver.get(product_url)
        time.sleep(5)  # Wait for page to load completely

        # 🔹 Enter Pincode and Confirm
        try:
            pincode_box = driver.find_element(By.ID, "product-pincode-01")
            pincode_box.clear()
            pincode_box.send_keys(PINCODE)
            pincode_box.send_keys(Keys.RETURN)
            time.sleep(7)  # Wait to update stock status
        except:
            print(f"⚠️ {product_name}: Pincode box not found! Skipping pincode check.")

        # 🔹 Check for "Delivery Unavailable" or "Out of Stock"
        try:
            unavailable_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sorry ! Delivery is unavailable to your postcode')]")
            out_of_stock_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sorry ! currently we are out of stock')]")

            if unavailable_element or out_of_stock_element:
                message = f"❌ *{product_name}* is _OUT OF STOCK_ or _Delivery Unavailable_.\n🚫 Check here: [Product Link]({product_url})"
                send_telegram_message(message)
                return  # Stop further checks for this product
        except:
            pass  # No error message, proceed to stock check

        # 🔹 Get Stock Status from JavaScript
        stock_status = driver.execute_script("return ga4_dataset?.product?.stock_status;")
        print(f"🔍 {product_name} - JavaScript Stock Status: {stock_status}")

        # 🔹 Final Stock Status Check
        if stock_status and "in" in stock_status.lower():
            message = f"✅ *{product_name}* is 🎉 _AVAILABLE_ 🎉\n🛒 [Buy Now]({product_url})"
        else:
            message = f"⚠️ *{product_name}* status is _UNKNOWN_ or _Error in fetching status_.\n🤔 [Check Here]({product_url})"

        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Error while checking {product_name}: {e}")

# 🔹 Function to Send Telegram Notification to Multiple Chat IDs
def
