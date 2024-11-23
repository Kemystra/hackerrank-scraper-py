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

    context = Context(session, args.contest_name)
    submission_ids = get_submission_ids(context, args.challenge_id)
    print(f"Scraped a total of {len(submission_ids)} submission IDs.")

    for i in submission_ids:
        while True:
            try:
                scrape_submissions(context, i)
            except Exception:
                continue
            time.sleep(args.delay + random.random())
            break


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


def scrape_submissions(context, id):
    url = f"https://www.hackerrank.com/rest/contests/{context.contest_name}/submissions/{id}"
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
