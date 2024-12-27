import logging
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import os
import time
from datetime import datetime
from .model import Trend
from dotenv import load_dotenv
from bson import ObjectId
from .utils import create_proxy_auth_extension, proxies
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

os.environ.pop("CHROME_DRIVER_PATH", None)
os.environ.pop("MONGO_DB_URL", None)
os.environ.pop("TWITTER_USERNAME", None)

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(".env file not found at the specified path")
load_dotenv(dotenv_path)

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
twitter_username = os.getenv("TWITTER_USERNAME")
twitter_email = os.getenv("TWITTER_EMAIL")
twitter_password = os.getenv("TWITTER_PASSWORD")
MONGODB_URL = os.getenv("MONGO_DB_URL")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")

if not chrome_driver_path:
    raise ValueError("CHROME_DRIVER_PATH environment variable is not set")

logger.info(f"CHROME_DRIVER_PATH: {chrome_driver_path}")

client = MongoClient(MONGODB_URL)
db = client["twitterScrapperDB"]
trends_collection = db["trends"]

try:
    db.command("ping")
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {str(e)}")


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}


@app.get("/api/scrape")
def scrape():
    logger.debug(f"Checking if path exists: {chrome_driver_path}")
    if not os.path.exists(chrome_driver_path):
        logger.error(f"Path does not exist: {chrome_driver_path}")
        return {"message": "Chrome driver path is not valid"}

    logger.info(f"Using CHROME_DRIVER_PATH: {chrome_driver_path}")

    PROXY = random.choice(proxies)
    create_proxy_auth_extension(
        PROXY["address"], PROXY["port"], PROXY_USERNAME, PROXY_PASSWORD
    )
    logger.info(f"Using PROXY: {PROXY}")
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_extension("proxy_auth_extension.zip")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(
        service=service,
        options=options,
    )

    url = "https://x.com/i/flow/login"
    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )

        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(twitter_username)
        username_field.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field = driver.find_element(By.NAME, "text")
            username_field.send_keys(twitter_email)
            username_field.send_keys(Keys.RETURN)
        except Exception:
            print("Email field not found, continuing anyway.")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(twitter_password)
        password_field.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field = driver.find_element(By.NAME, "text")
            username_field.send_keys(twitter_email)
            username_field.send_keys(Keys.RETURN)
        except Exception:
            print("Email field not found, continuing anyway.")

        WebDriverWait(driver, 30).until(EC.url_contains("home"))

        if "home" in driver.current_url:
            logger.info("Login successful")
            try:
                trending_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@aria-label="Timeline: Trending now"]')
                    )
                )
                time.sleep(2)

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
                    logger.info(f"{k}: {v}")

                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip_address = PROXY["address"] + ":" + str(PROXY["port"])

                result = {
                    **trends,
                    "date_time_of_end": end_time,
                    "ip_address": ip_address,
                }

                trend_model = Trend(_id=ObjectId(), **result)

                trend_dict = trend_model.dict(by_alias=True)
                res = trends_collection.insert_one(trend_dict)

                result["_id"] = str(res.inserted_id)

                logger.info("Scraping successful")
                return result
            except Exception as e:
                logger.error(f"Trending element not found: {e}")
                return {"message": "Login successful but trending element not found"}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {"message": f"Error occurred: {str(e)}"}

    finally:
        driver.quit()
        logger.info("Driver quit successfully")
