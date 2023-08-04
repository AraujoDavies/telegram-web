from splinter import Browser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from dotenv import load_dotenv

load_dotenv('config.env')

service = Service(ChromeDriverManager(version='114.0.5735.90').install())

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--log-level=3')
# chrome_options.add_argument(f"user-data-dir=C:\\projetos\\telegram-selenium\\profile-tele")

def meu_browser():
    # return Browser(driver_name='remote',browser='Chrome', command_executor='http://192.168.15.250:4444', options=chrome_options)
    # driver local
    return Browser('chrome', options=chrome_options, service=service)
