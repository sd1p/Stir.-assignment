import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

twitter_username = os.getenv("TWITTER_USERNAME")
twitter_password = os.getenv("TWITTER_PASSWORD")

chrome_driver_path = "D:\\chromedriver-win64\\chromedriver.exe"


def generate_unique_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def scrape():
    print(f"Checking if path exists: {chrome_driver_path}")
    if not os.path.exists(chrome_driver_path):
        print(f"Path does not exist: {chrome_driver_path}")
        return {"message": "Chrome driver path is not valid"}

    print(f"Using CHROME_DRIVER_PATH: {chrome_driver_path}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://x.com/i/flow/login"
    try:
        print(f"Navigating to URL: {url}")
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )

        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(twitter_username)
        username_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(twitter_password)
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.url_contains("home"))

        if "home" in driver.current_url:
            print("Login successful")
            try:
                trending_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@aria-label="Timeline: Trending now"]')
                    )
                )
                time.sleep(1)

                trend_elements = trending_element.find_elements(
                    By.XPATH, "//div[@data-testid='trend']"
                )

                def get_second_element_or_first(trend_text):
                    trend_parts = trend_text.split("\n")
                    return trend_parts[1] if len(trend_parts) > 1 else trend_parts[0]

                trends = {
                    f"nameOfTrend{i+1}": get_second_element_or_first(trend.text)
                    for i, trend in enumerate(trend_elements)
                }

                for k, v in trends.items():
                    print(f"{k}: {v}")

                unique_id = generate_unique_id()
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip_address = "127.0.0.1"

                result = {
                    "unique_id": unique_id,
                    **trends,
                    "date_time_of_end": end_time,
                    "ip_address": ip_address,
                }

                print("Scraping successful")
                return result
            except Exception as e:
                print("Trending element not found:", e)
                return {"message": "Login successful but trending element not found"}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"message": f"Error occurred: {str(e)}"}

    finally:
        driver.quit()
        print("Driver quit successfully")


if __name__ == "__main__":
    result = scrape()
    print(result)
