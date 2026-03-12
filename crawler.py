#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import time
import random

BASE_URL = "https://www.carzone.ie/search?page={}"
START = 1
END = 200

OUTPUT_DIR = "cars_list_200_output"

PROXY_URL = os.environ.get("PROXY_URL")
USE_PROXY = PROXY_URL is not None

MAX_ATTEMPTS = 3

# le dossier de sortie crée ! 

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================
def get_chrome_options(user_agent=None):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
     # Proxy + user-agent
    if USE_PROXY:
     options.add_argument(f"--proxy-server={PROXY_URL}")

    options.add_argument(f"--user-agent={user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}")
       
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def setup_driver(attempt):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'
    ]
    ua = user_agents[(attempt - 1) % len(user_agents)]
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=get_chrome_options(ua))

   
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": driver.execute_script("return navigator.userAgent"),
        "platform": "Win32"
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    width = random.randint(1200, 1920)
    height = random.randint(800, 1080)
    driver.set_window_size(width, height)
    return driver

# ==================================
def recaptcha_detect(driver):
    html = driver.page_source.lower()
    title = driver.title.lower()
    keywords = ["captcha", "verify", "challenge", "are you human", "cloudflare", "turnstile", "cf-challenge", "recaptcha", "grecaptcha"]
    if any(k in html for k in keywords) or any(k in title for k in keywords):
        return True
    selectors = ["iframe[src*='recaptcha']", "iframe[src*='cloudflare']", "div#cf-browser-verification", "div.recaptcha-checkbox"]
    for sel in selectors:
        if driver.find_elements(By.CSS_SELECTOR, sel):
            return True
    return False

def attempt_recaptcha_bypass(driver, attempt):
    wait_time = 3 + attempt
    time.sleep(wait_time)
    if not recaptcha_detect(driver):
        return True
    url = driver.current_url
    if "?" in url:
        url += f"&_attempt={attempt}&_t={int(time.time())}"
    else:
        url += f"?_attempt={attempt}&_t={int(time.time())}"
    driver.get(url)
    time.sleep(4 + attempt)
    return not recaptcha_detect(driver)

# ==================================
def analyze_failure(html, title, driver=None):
    reasons = []
    if any(k in title or k in html for k in ["403", "Forbidden", "Access Denied"]):
        reasons.append("403 Forbidden")
    if any(k in title or k in html for k in ["404", "Not Found"]):
        reasons.append("404 Not Found")
    if any(k in title or k in html for k in ["500", "Internal Server Error"]):
        reasons.append("500 Server Error")
    if "blocked" in html.lower() or "Blocked" in title:
        reasons.append("Blocked by site")
    if len(html) < 5000:
        reasons.append(f"Content too short ({len(html)})")
    if driver and recaptcha_detect(driver):
        reasons.append("CAPTCHA not resolved")
    return " | ".join(reasons) if reasons else "Unknown"

# ==================================
def fetch_page(page_num):
    url = BASE_URL.format(page_num)

  
    file_name = f"{page_num:04d}__used_cars.html"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        driver = None
        try:
            driver = setup_driver(attempt)
            driver.set_page_load_timeout(30)
            driver.get(url)
            time.sleep(random.uniform(2,4))

            if recaptcha_detect(driver):
                print(f"⚠ CAPTCHA detected on page {page_num}, attempt {attempt}")
                if attempt_recaptcha_bypass(driver, attempt):
                    print(f" CAPTCHA bypassed on attempt {attempt}")
                else:
                    print(f" CAPTCHA not bypassed on attempt {attempt}")
                    continue

            html = driver.page_source
            if len(html) < 5000:
                print(f" Page content too short ({len(html)})")
                continue

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f" Page {page_num} saved successfully")
            return True

        except Exception as e:
            print(f" Error on page {page_num}, attempt {attempt}: {str(e)[:80]}")
            time.sleep(random.uniform(3,6))

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    print(f" FAILED after {MAX_ATTEMPTS} attempts: Page {page_num}")
    return False

# ================= MAIN =================
def main():
    total_success = 0
    for page in range(START, END + 1):
        if fetch_page(page):
            total_success += 1
        time.sleep(random.uniform(1,3))
    print("\n========== SUMMARY ==========")
    print(f"Pages total: {END-START+1}")
    print(f"Pages réussies: {total_success}")
    print(f"Pages échouées: {END-START+1 - total_success}")

if __name__ == "__main__":
    main()