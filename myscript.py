from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# 🔹 Telegram Details
TELEGRAM_BOT_TOKEN = "7607310655:AAEBc_-jzx47VRBLWjqm2sceyInZ_d-z5lg"
CHAT_IDS = ["163447880", "826574622"]

PRODUCTS = {
    " LG 32 LR57 📺": "https://www.lg.com/in/tv-soundbars/smart-tvs/32lr570b6la/buy/",
    " LG WM Semi 7KG🗄️": "https://www.lg.com/in/laundry/semi-automatic-washing-machines/p7020ngaz/buy/",
}
PINCODE = "305001"

# 🔹 Setup Chrome with Stealth Arguments
options = webdriver.ChromeOptions()
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

def check_availability(product_name, product_url):
    try:
        driver.get(product_url)
        wait = WebDriverWait(driver, 25)

        # 1. Enter Pincode
        try:
            pincode_box = wait.until(EC.element_to_be_clickable((By.ID, "product-pincode-01")))
            pincode_box.click()
            pincode_box.clear()
            pincode_box.send_keys(PINCODE)
            pincode_box.send_keys(Keys.RETURN)
            
            # Wait for the UI to refresh after entering pincode
            time.sleep(7) 
        except Exception as e:
            print(f"⚠️ Pincode box issue: {e}")

        # 2. Check for "Out of Stock" or "Delivery Unavailable" via UI Text
        page_source = driver.page_source.lower()
        
        failure_indicators = [
            "currently we are out of stock",
            "delivery is unavailable to your postcode",
            "not deliverable",
            "sold out"
        ]

        is_actually_available = True
        found_msg = ""
        
        for msg in failure_indicators:
            if msg in page_source:
                print(f"❌ {product_name}: Found failure message: '{msg}'")
                is_actually_available = False
                found_msg = msg
                break

        # 3. Double check the "Buy Now" button
        if is_actually_available:
            try:
                buy_now_btn = driver.find_element(By.CSS_SELECTOR, ".buy-now, .add-to-cart")
                if "disabled" in buy_now_btn.get_attribute("class") or not buy_now_btn.is_enabled():
                    is_actually_available = False
            except:
                is_actually_available = False

        # 4. Final Verdict & Notification
        if is_actually_available:
            message = f"🎉 *{product_name}* is AVAILABLE for `{PINCODE}`!\n[Buy Now]({product_url})"
        else:
            message = f"ℹ️ *{product_name}* is currently Out of Stock for `{PINCODE}`."
            print(f"ℹ️ {product_name} is confirmed OUT of stock for {PINCODE}.")

        # Send the notification (This runs for both In Stock and Out of Stock now)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Error: {e}")

def send_telegram_message(message):
    for chat_id in CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
            r = requests.post(url, data=payload)
            if r.status_code != 200:
                print(f"⚠️ Telegram API Error: {r.text}")
        except Exception as e:
            print(f"⚠️ Failed to reach Telegram: {e}")

# Execution
for name, url in PRODUCTS.items():
    check_availability(name, url)

driver.quit()


