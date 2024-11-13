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
SUBMISSIONS_LIST_ENDPOINT = "https://www.hackerrank.com/rest/contests/" + CONTEST_SLUG + "/judge_submissions/?offset=0&limit=1000000"
SUBMISSION_DATA_ENDPOINT = "https://www.hackerrank.com/rest/contests/" + CONTEST_SLUG + "/submissions/"
ACCEPTED_SUBMISSION_STATUS = "Accepted"


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

    submission_list = req_api(s, SUBMISSIONS_LIST_ENDPOINT)["models"]
    challenge_names_map = {}
    result = []
    for submission in submission_list:
        if submission["status"] != ACCEPTED_SUBMISSION_STATUS:
            continue

        challenge_info = submission["challenge"]
        challenge_names_map[challenge_info["slug"]] = challenge_info["name"]

        print(submission["id"])
        code = req_api(s, SUBMISSION_DATA_ENDPOINT + str(submission["id"]))["model"]["code"]

        entry = Submission(
            submission_id=submission["id"],
            username=submission["hacker_username"],
            challenge_slug=challenge_info["slug"],
            lang=submission["language"],
            code=code
        )

        result.append(entry)

        time.sleep(5)

    print(len(result))


def req_api(session: requests.Session, url: str) -> dict:
    resp = session.get(url)
    resp.raise_for_status()
    data = json.loads(resp.text)
    return data


def process_cookie(raw_cookies):
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
