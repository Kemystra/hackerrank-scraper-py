import argparse
import src.scraper as scraper


def main():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument('-t', '--token', type=str, required=True, help='Token for authentication')
    parser.add_argument('-cn', '--contest_name', type=str, required=True, help='Contest name')
    parser.add_argument('-cid', '--challenge_id', type=str, required=True, help='Challenge ID')

    # Optional argument
    parser.add_argument('-d', '--delay', type=float, help='Delay between requests, in seconds. Default is 5 seconds', default=5)
    parser.add_argument('--accepted-only', action='store_true', default=False, dest='is_accepted_only')
    parser.add_argument('-u', '--username', type=str, default='', dest='usernames')
    parser.add_argument('-o', '--output-folder', type=str, default='', dest='output_folder')

    args = parser.parse_args()
    scraper.scrape(args)


if __name__ == "__main__":
    main()
