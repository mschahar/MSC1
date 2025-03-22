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
    "LG TV LM56": "https://www.lg.com/in/tv-soundbars/smart-tvs/32lm563bptc/buy/",
    "1st 185L 5S": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201ascu/buy/",
    "2nd 185L 5S": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abeu/buy/",
    "3rd 185L 5S": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201aseu/buy/",
    "4th 185L 5S": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abcu/buy/",
    "1st 185L 4s": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d199obey/buy/",
    "2nd 185L 4s": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d199osey/buy/",
    "3rd 185L 4s": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201ascy/buy/",
    "4th 185L 4s": "https://www.lg.com/in/refrigerators/single-door-refrigerators/gl-d201abcy/buy/",
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

        # 🔹 Enter Pincode
        try:
            pincode_box = driver.find_element(By.ID, "product-pincode-01")  # Update if different
            pincode_box.clear()
            pincode_box.send_keys(PINCODE)
            pincode_box.send_keys(Keys.RETURN)  # Press Enter
            time.sleep(7)  # Wait longer for stock status to update
        except:
            print(f"⚠️ {product_name}: Pincode input box not found! Skipping this step.")

        # 🔹 Check for "Delivery Unavailable" or "Out of Stock"
        try:
            unavailable_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sorry ! Delivery is unavailable to your postcode')]")
            out_of_stock_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sorry ! currently we are out of stock')]")
            
            if unavailable_element or out_of_stock_element:
                message = f"❌ {product_name} is **OUT OF STOCK** or **Delivery Unavailable**."
                send_telegram_message(message)
                return  # Stop further processing for this product
        except:
            pass  # No error message, proceed to stock check

        # 🔹 Get Stock Status from JavaScript
        stock_status = driver.execute_script("return ga4_dataset?.product?.stock_status;")
        print(f"🔍 {product_name} - JavaScript Stock Status: {stock_status}")  # Debugging

        # 🔹 Check if product is available
        if stock_status and "in" in stock_status.lower():
            message = f"✅ {product_name} is **AVAILABLE**!\nBuy here: {product_url}"
        else:
            message = f"⚠️ {product_name} stock status could not be determined."

        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Error checking {product_name}: {e}")

# 🔹 Function to Send Telegram Notification to Multiple Chat IDs
def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"📩 Telegram message sent to {chat_id}: {message}")
        else:
            print(f"⚠️ Failed to send message to {chat_id}: {response.json()}")

# 🔹 Run the check for all products
for name, url in PRODUCTS.items():
    check_availability(name, url)

driver.quit()  # Close the browser session
