import requests
from requests.utils import cookiejar_from_dict
import os
import time
import random
from dataclasses import dataclass

# Constants
TOKEN_NAME = "remember_hacker_token"


@dataclass
class Context:
    session: requests.Session
    contest_name: str
    delay: float


def scrape(args):
    session = requests.session()

    cookies = dict({
        TOKEN_NAME: args.token
    })

    cookies = cookiejar_from_dict(cookies)
    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    session.headers.update(headers)

    context = Context(session, args.contest_name, args.delay)
    submission_ids = get_submission_ids(context, args.challenge_id)
    total_submissions = len(submission_ids)
    print(f"Scraped a total of {total_submissions} submission IDs.")

    for i in range(total_submissions):
        progress_percent = (i / total_submissions) * 100
        print(f"{progress_percent:.4f}% - ", end='')
        fetch_submissions_with_retries(context, submission_ids[i])


def get_submission_ids(context, challenge_id):
    ids = []

    url = f'https://www.hackerrank.com/rest/contests/{context.contest_name}/judge_submissions/?offset=0&limit=1000000&challenge_id={challenge_id}'
    response = req_api(context.session, url)

    submissions = response['models']
    for j in submissions:
        if j['status_code'] == 2:
            ids.append(j['id'])

    time.sleep(1)

    return ids


def fetch_submissions_with_retries(context, sub_id):
    # Retry each submission, in case of HTTP code 429: Too many requests
    while True:
        try:
            scrape_submissions(context, sub_id)
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                continue
            else:
                raise err
        # Jitter to try confusing the rate limiter
        time.sleep(context.delay + random.random())
        break


def scrape_submissions(context, sub_id):
    url = f"https://www.hackerrank.com/rest/contests/{context.contest_name}/submissions/{sub_id}"
    data = req_api(context.session, url)['model']

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
