from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from submissions import Submission

import requests
import time
import json

LOGIN_URL = "https://www.hackerrank.com/auth/login"
USERNAME = "programmer_cole1"
PASSWORD = "RugMargaritaClubhouse"

CONTEST_SLUG = "cn24-prelim-test"
CHALLENGE_LIST_ENDPOINT = "https://www.hackerrank.com/rest/contests/" + CONTEST_SLUG + "/challenges?offset=0&limit=1000000"
CHALLENGE_SUBMISSIONS_LIST_ENDPOINT = "https://www.hackerrank.com/rest/contests/" + CONTEST_SLUG + "/judge_submissions/?offset=0&limit=1000000&challenge_id="

raw_cookies = 'hackerrank_mixpanel_token=7866c454-fb22-44ef-8214-938d28d9bf8e; h_r=auth_dialog; h_l=in_app; h_v=_default; g_state={"i_p":1731488010421,"i_l":2}; hacker_editor_theme=light; user_theme=dark; hackerrankx_mixpanel_token=7866c454-fb22-44ef-8214-938d28d9bf8e; referrer=direct; metrics_user_identifier=19cf21c-0edc2bae99473f0620fda0c49b00e8b8b9a5170f; react_var=false__cnt4; react_var2=false__cnt4; _fcdscst=MTczMTUwMzE3Nzg0MQ==; show_cookie_banner=false; homepage_variant=https://www.hackerrank.com/; hrc_l_i=T; user_type=hacker; session_id=mm8vgpus-1731503199133'


def main():
    # Copying cookies from a logged-in browser console isn't enough
    # But fetching it directly from a Selenium session works
    # Why?????

    options = Options()
    # Don't wait for full page load
    options.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=options)

    cookies = login(driver)

    # Not sure why user agent is important here
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    s = requests.session()
    s.headers.update(headers)

    # Copying session credentials to requests for easier API calls
    for cookie in cookies:
        c = {cookie["name"]: cookie["value"]}
        s.cookies.update(c)

    challenge_data_list = req_api(s, CHALLENGE_LIST_ENDPOINT)["models"]

    all_submission = {}
    for challenge in challenge_data_list:
        challenge_submissions = get_submissions(slug)


def get_submissions(slug: str) -> list[Submission]:
    result = []


def req_api(session: requests.Session, url: str) -> dict:
    resp = session.get(url)
    resp.raise_for_status()
    print(resp.status_code)
    data = json.loads(resp.text)
    return data


def process_cookie(raw_cookie):
    cookies_key_value_pairs = [x for x in raw_cookies.split("; ")]
    cookies = []
    for raw_cookie_pair in cookies_key_value_pairs:
        pair = raw_cookie_pair.split('=')
        c = {pair[0]: pair[1]}
        cookies.append(c)


def login(driver):
    driver.get(LOGIN_URL)
    inputs = driver.find_elements(By.TAG_NAME, "input")

    username_input = inputs[0]
    password_input = inputs[1]

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    # Crude way to wait for login response
    time.sleep(3)

    return driver.get_cookies()


if __name__ == "__main__":
    main()
