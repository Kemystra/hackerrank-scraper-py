import requests
from requests.utils import cookiejar_from_dict
import os
import sys
import time

# Constants

CONTEST_NAME = "codenection-2024-test"
CHALLENGE_ID = "cn24-test2"
TOKEN_NAME = "remember_hacker_token"

SUBMISSION_API = "https://www.hackerrank.com/rest/contests/codenection-2024-test/submissions/"
ACCEPTED_SUBMISSION_STATUS = "Accepted"

# Pass token as argument
token_value = sys.argv[1]

delay = 5  # seconds
mx_retries = 3


def get_submission_ids(CONTEST_NAME, CHALLENGE_ID, session):
    url = f'https://www.hackerrank.com/rest/contests/{CONTEST_NAME}/judge_submissions/?offset=0&limit=1&CHALLENGE_ID={CHALLENGE_ID}'

    response = session.get(url)

    ids = []

    url = f'https://www.hackerrank.com/rest/contests/{CONTEST_NAME}/judge_submissions/?offset=0&limit=1000000&CHALLENGE_ID={CHALLENGE_ID}'
    response = req_api(session, url)

    submissions = response['models']
    for j in submissions:
        if j['status_code'] == 2:
            ids.append(j['id'])

    time.sleep(1)

    return ids


def scrape_submissions(id, session):
    data = req_api(session, SUBMISSION_API + id)['models']

    if data['status'] != ACCEPTED_SUBMISSION_STATUS:
        return

    # Rename the challenge name to a safe folder name
    folder_name = data['name'].lowercase().replace(' ', '_')
    os.makedirs(f"./{folder_name}/", exist_ok=True)

    username = data['hacker_username']
    with open(f"./{folder_name}/{username}.txt", 'w') as f:
        f.write(data['code'])


def req_api(session: requests.Session, url: str) -> dict:
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data


if __name__ == "__main__":
    session = requests.session()

    cookies = dict({
        TOKEN_NAME: token_value
    })

    cookies = cookiejar_from_dict(cookies)
    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    session.headers.update(headers)
    submission_ids = get_submission_ids(CONTEST_NAME, CHALLENGE_ID, session)
    print(f"Scraped a total of {len(submission_ids)} submission IDs.")

    print(submission_ids)

    for i in submission_ids:
        scrape_submissions(i, session)
