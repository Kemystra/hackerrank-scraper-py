import requests
from requests.utils import cookiejar_from_dict
import os
import time
import random
import json
from dataclasses import dataclass

# Constants
TOKEN_NAME = "remember_hacker_token"
ACCEPTED_STATUS = "Accepted"
WRONG_ANSWER_STATUS = "Wrong Answer"


@dataclass
class Context:
    session: requests.Session
    contest_name: str


def scrape(args):
    session = requests.session()

    if args.option_file:
        f = open(args.option_file, 'r')
        option_json = json.loads(f.read())
        f.close()

        args.contest_name = option_json['contest_name']
        args.token = option_json['token']
        args.challenge_ids = option_json['challenge_id']
        args.usernames = option_json['usernames']
        args.output_folder = option_json['output_folder']
        args.delay = option_json['delay']

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
    submission_ids = get_submission_ids(context, args.challenge_ids, args.is_accepted_only, args.usernames)
    total_submissions = len(submission_ids)
    print(f"Scraped a total of {total_submissions} submission IDs.")

    for i in range(total_submissions):
        progress_percent = ((i + 1) / total_submissions) * 100
        print(f"{progress_percent:.4f}% - ", end='')
        fetch_submissions_with_retries(context, submission_ids[i], args.delay, args.output_folder)


def get_submission_ids(context, challenge_id_array, is_accepted_only, username_array):
    ids = []

    for challenge_id in challenge_id_array:
        url = f'https://www.hackerrank.com/rest/contests/{context.contest_name}/judge_submissions/?offset=0&limit=1000000&challenge_id={challenge_id}'
        response = req_api(context.session, url)

        submissions = response['models']
        for j in submissions:
            if is_accepted_only and j['status'] != ACCEPTED_STATUS:
                continue
            if username_array and j['hacker_username'] not in username_array:
                continue
            ids.append(j['id'])

        time.sleep(1)

    return ids


def fetch_submissions_with_retries(context, sub_id, delay, output_folder):
    # Retry each submission, in case of HTTP code 429: Too many requests
    while True:
        try:
            scrape_submissions(context, sub_id, output_folder)
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                continue
            else:
                raise err
        # Jitter to try confusing the rate limiter
        time.sleep(delay + random.random())
        break


def scrape_submissions(context, sub_id, output_folder):
    url = f"https://www.hackerrank.com/rest/contests/{context.contest_name}/submissions/{sub_id}"
    data = req_api(context.session, url)['model']

    # Rename the challenge name to a safe folder name
    folder_name = data['name'].lower().replace(' ', '_')
    os.makedirs(f"./{output_folder}/{folder_name}/", exist_ok=True)

    username = data['hacker_username']
    time_str = time.strftime("%H-%M-%S", time.localtime(int(data['created_at_epoch'])))

    if not output_folder:
        submission_filename = f"./{folder_name}/{username}_{time_str}.txt"
    else:
        submission_filename = f"./{output_folder}/{folder_name}/{username}_{time_str}.txt"

    print(f"Fetched {username}'s submission")
    with open(submission_filename, 'w') as f:
        f.write(data['code'])


def req_api(session: requests.Session, url: str) -> dict:
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data
