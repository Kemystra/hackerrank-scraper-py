import requests
from requests.utils import cookiejar_from_dict
import os
import sys
import time

# Constants

contest_name = "codenection-2024-test"
challenge_id = "cn24-test2"
token_name = "remember_hacker_token"

# Pass token as argument
token_value = sys.argv[1]
delay = 5  # seconds
mx_retries = 3


def get_submission_ids(contest_name, challenge_id, session):
    url = f'https://www.hackerrank.com/rest/contests/{contest_name}/judge_submissions/?offset=0&limit=1&challenge_id={challenge_id}'

    response = session.get(url)

    ids = []

    url = f'https://www.hackerrank.com/rest/contests/{contest_name}/judge_submissions/?offset=0&limit=1000000&challenge_id={challenge_id}'
    response = session.get(url)

    submissions = response.json()['models']
    for j in submissions:
        if j['status_code'] == 2:
            ids.append(j['id'])

    time.sleep(1)

    return ids


def scrape_submissions(id, session):
    pass


if __name__ == "__main__":
    session = requests.session()

    cookies = dict({
        token_name: token_value
    })

    cookies = cookiejar_from_dict(cookies)
    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    session.headers.update(headers)
    submission_ids = get_submission_ids(contest_name, challenge_id, session)
    print(f"Scraped a total of {len(submission_ids)} submission IDs.")

    print(submission_ids)

    for i in submission_ids:
        scrape_submissions(i, session)
