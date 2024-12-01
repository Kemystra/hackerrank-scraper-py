# Hackerrank Contest Submissions Scraper
To scrape stuff

## Basic Usage
1. Download this repo
2. Go into this repo's folder
3. Run:
    ```py
    python main.py -t TOKEN -cn CONTEST_NAME -cid CHALLENGE_ID -u USERNAMES -o OUTPUT_FOLDER
    ```
    TOKEN can be a token string or txt file containing the token.
    CHALLENGE_ID can be a comma-separated value. Same with USERNAMES.

4. OR if you want to, you can just specify an option file.
```sh
python main.py -f OPTION_FILE

```

The basic format of the option file is:
```json
{
    "token": "TOKEN",
    "contest_name": "CONTEST_NAME",
    "challenge_ids": [],
    "usernames": [],
    "output_folder": "OUTPUT_FOLDER",
    "delay": 3,
    "is_accepted_only": false
}
```

## Advanced
- An optional `-d,--delay` option can be given, with no. of seconds as input. This will set the delay between each submission's fetching requests. Note that setting this number too low may have unexpected consequences. By default, it is set to 5 seconds.

- Without the option `-u,--username`, the program will fetch submissions from ALL username.

- Without the option `-cid,--challenge-id`, s
