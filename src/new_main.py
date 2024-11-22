from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from requests.utils import cookiejar_from_dict
import os
import time

# Constants

contest_name = "CONTEST_NAME"
challenge_id = "CHALLENGE_SLUG"
token_name = "remember_hacker_token"
token_value = "TOKEN_VALUE"
delay = 5  # seconds
mx_retries = 3


def get_submission_ids(contest_name, challenge_id):
    session = requests.session()
    cookies = dict({
        token_name: token_value
    })
    cookies = cookiejar_from_dict(cookies)
    session.cookies.update(cookies)

    url = f'https://www.hackerrank.com/rest/contests/{contest_name}/judge_submissions/?offset=0&limit=1&challenge_id={challenge_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    response = session.get(
        url,
        headers=headers
    )

    total = response.json()['total']
    ids = []

    url = f'https://www.hackerrank.com/rest/contests/{contest_name}/judge_submissions/?offset=0&limit=1000000&challenge_id={challenge_id}'
    response = session.get(
        url,
        headers=headers
    )

    submissions = response.json()['models']
    for j in submissions:
        if j['status_code'] == 2:
            ids.append(j['id'])

    time.sleep(1)

    return ids


def scrape_submissions(id, driver):
    url = f'https://www.hackerrank.com/contests/{contest_name}/challenges/{challenge_id}/submissions/code/{id}'
    driver.get(url)
    retry = 1

    while (retry <= mx_retries):
        time.sleep(delay)
        try:
            username = driver.find_element(By.CSS_SELECTOR, '.alert-info .bold').text

            challenge_name = driver.find_element(By.CSS_SELECTOR, '.hr_tour-challenge-name').text
            challenge_name = [i.lower() for i in challenge_name if i.isalpha() or i == ' ']
            challenge_name = ''.join(challenge_name).replace(' ', '_')

            lines = driver.find_elements(By.CSS_SELECTOR, '.CodeMirror-line')

            codes = []
            for line in lines:
                codes.append(line.text)

            os.makedirs(f'./{challenge_name}/', exist_ok=True)
            with open(f'./{challenge_name}/{username}.txt', 'w') as f:
                f.write('\n'.join(codes))
            break
        except Exception as e:
            print(f'Attempt #{retry}: Error occured at page {url}')

        retry += 1


if __name__ == "__main__":
    submission_ids = get_submission_ids(contest_name, challenge_id)
    print(f"Scraped a total of {len(submission_ids)} submission IDs.")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get('https://www.hackerrank.com/')
    cookie = {
        'name': token_name,
        'value': token_value,
        'domain': 'hackerrank.com',
        'path': '/',
    }

    driver.add_cookie(cookie)

    driver.refresh()

    for i in submission_ids:
        scrape_submissions(i, driver)

    driver.quit()
