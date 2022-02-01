# Selenium imports here
import ast
import base64
import json
import os
import urllib.parse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
nhs_login_user = os.environ["NHS_LOGIN_USER"]
nhs_login_password_b64 = os.environ["NHS_LOGIN_PASSWORD_B64"]
nhs_login_password = base64.b64decode(nhs_login_password_b64).decode('utf-8')
nhs_login_otp_code = os.environ["NHS_LOGIN_OTP_CODE"]

# Chrome driver configuration
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--no-sandbox")

# initialize the Chrome driver
driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options
)

# hit identity-service on INT
params = {
    "response_type": "code",
    "client_id": client_id,
    "state": 123,
    "scope": "nhs-login",
    "redirect_uri": "https://nhsd-apim-testing-int.herokuapp.com/callback",
}
base_url = "https://int.api.service.nhs.uk/oauth2/authorize?"
url = base_url + urllib.parse.urlencode(params)
driver.get(url)

# wait for the username input element to be available
username = WebDriverWait(driver=driver, timeout=10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
)

# clear the username input element
username.clear()

# populate the username element
username.send_keys(nhs_login_user)

# submit user
WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
).click()

# click the 'continue' button again to accept stuff
WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
).click()

# wait for the password input element to be ready
password = WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
)

# clear the password input element
password.clear()

# populate the password element
password.send_keys(nhs_login_password)

# submit password
WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
).click()

# wait for the otp element to be ready
otp_code = WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='otp']"))
)

# clear the otp element
otp_code.clear()

# populate ods element
otp_code.send_keys(nhs_login_otp_code)

# submit otp
WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
).click()

# wait for callback url
callback_page = WebDriverWait(driver=driver, timeout=20).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/pre"))
)

# access callback url to get the code
current_url = driver.current_url

query = requests.utils.urlparse(current_url).query
params = dict(x.split("=") for x in query.split("&"))
code = params["code"]

url = "https://int.api.service.nhs.uk/oauth2/token"

# post code to identity service
data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "https://nhsd-apim-testing-int.herokuapp.com/callback",
    "client_id": client_id,
    "client_secret": client_secret,
}

response = requests.post(url, data=data)
response = json.dumps(response.json(), indent=2)
dictionary = ast.literal_eval(response)

print(dictionary["access_token"])
driver.close()
