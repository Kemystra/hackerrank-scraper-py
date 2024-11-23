import requests
from requests.utils import cookiejar_from_dict
import os
import sys
import time
import random

# Constants

CONTEST_NAME = "codenection-2023-preliminary-round-open-category"
TOKEN_NAME = "remember_hacker_token"

SUBMISSION_API = "https://www.hackerrank.com/rest/contests/"+CONTEST_NAME+"/submissions/"

# Pass token as argument
token_value = sys.argv[1]
challenge_id = sys.argv[2]

DELAY = 5  # seconds
mx_retries = 3


def main():
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
    submission_ids = get_submission_ids(CONTEST_NAME, challenge_id, session)
    print(f"Scraped a total of {len(submission_ids)} submission IDs.")

    for i in submission_ids:
        while True:
            try:
                scrape_submissions(i, session)
            except Exception:
                continue
            time.sleep(DELAY + random.random())
            break


def get_submission_ids(CONTEST_NAME, challenge_id, session):
    ids = []

    url = f'https://www.hackerrank.com/rest/contests/{CONTEST_NAME}/judge_submissions/?offset=0&limit=1000000&challenge_id={challenge_id}'
    response = req_api(session, url)

    submissions = response['models']
    for j in submissions:
        if j['status_code'] == 2:
            ids.append(j['id'])

    time.sleep(1)

    return ids


def scrape_submissions(id, session):
    data = req_api(session, SUBMISSION_API + str(id))['model']

    # Rename the challenge name to a safe folder name
    folder_name = data['name'].lower().replace(' ', '_')
    os.makedirs(f"./{folder_name}/", exist_ok=True)

    username = data['hacker_username']

    print(f"Fetched {username}'s submission")
    with open(f"./{folder_name}/{username}.txt", 'w') as f:
        f.write(data['code'])


def req_api(session: requests.Session, url: str) -> dict:
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data


if __name__ == "__main__":
    main()
