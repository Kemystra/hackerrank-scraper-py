# Hackerrank Contest Submissions Scraper
To scrape stuff

## Basic Usage
1. Download this repo
2. Go into this repo's folder
3. Run:
    ```py
    python main.py -t TOKEN -cn CONTEST_NAME -cid CHALLENGE_ID
    ```

## Advanced
An optional `-d,--delay` option can be given, with no. of seconds as input. This will set the delay between each submission's fetching requests. Note that setting this number too low may have unexpected consequences. By default, it is set to 5 seconds.
