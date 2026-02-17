from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# 🔹 Telegram Details (Keep your tokens)
TELEGRAM_BOT_TOKEN = "7607310655:AAEBc_-jzx47VRBLWjqm2sceyInZ_d-z5lg"
CHAT_IDS = ["163447880", "826574622"]

PRODUCTS = {
    " LG 32 LR57 📺": "https://www.lg.com/in/tv-soundbars/smart-tvs/32lr570b6la/buy/",
}
PINCODE = "305001"

# 🔹 Setup Chrome with Stealth Arguments
options = webdriver.ChromeOptions()
options.add_argument("--headless=new") # Faster, modern headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
# Hides the "Automation" flag
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

def check_availability(product_name, product_url):
    try:
        driver.get(product_url)
        wait = WebDriverWait(driver, 20) # Wait up to 20 seconds

        # 🔹 Enter Pincode
        try:
            # Wait for pincode box to be clickable
            pincode_box = wait.until(EC.element_to_be_clickable((By.ID, "product-pincode-01")))
            pincode_box.click() # Click first to focus
            pincode_box.clear()
            pincode_box.send_keys(PINCODE)
            pincode_box.send_keys(Keys.RETURN)
            
            # Wait for the price or stock status to refresh after pincode
            time.sleep(5) 
        except Exception as e:
            print(f"⚠️ {product_name}: Pincode Error: {e}")

        # 🔹 JavaScript Check (LG's internal data layer)
        # We wrap this in a try-block because ga4_dataset might not load immediately
        try:
            stock_status = driver.execute_script("return ga4_dataset?.product?.stock_status;")
            print(f"🔍 {product_name} Status: {stock_status}")
        except:
            stock_status = "unknown"

        # 🔹 Logic Check
        if stock_status and "in" in stock_status.lower():
            message = f"🎉 *{product_name}* is IN STOCK for `{PINCODE}`!\n[Buy Now]({product_url})"
            send_telegram_message(message)
        elif "out" in str(stock_status).lower():
            print(f"❌ {product_name} is Out of Stock.")
        else:
            # Fallback: Check for visual "Out of Stock" text
            body_text = driver.find_element(By.TAG_NAME, "body").text
            if "out of stock" in body_text.lower():
                print(f"❌ {product_name} confirmed Out of Stock via text.")
            else:
                send_telegram_message(f"❓ Status Unclear for {product_name}. Check link: {product_url}")

    except Exception as e:
        print(f"⚠️ Error checking {product_name}: {e}")

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)

# Execution
for name, url in PRODUCTS.items():
    check_availability(name, url)

driver.quit()
