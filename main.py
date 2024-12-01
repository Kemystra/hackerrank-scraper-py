import argparse
import src.scraper as scraper


def main():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument('-t', '--token', type=str, required=True, help='Token for authentication')
    parser.add_argument('-cn', '--contest_name', type=str, required=True, help='Contest name')
    parser.add_argument('-cid', '--challenge_id', type=str, required=True, help='Challenge ID, can be a list of comma-separated values')

    # Optional argument
    parser.add_argument('-d', '--delay', type=float, help='Delay between requests, in seconds. Default is 5 seconds', default=5)
    parser.add_argument('--accepted-only', action='store_true', default=False, dest='is_accepted_only',
                        help='Only scrape accepted submissions. Default to false')
    parser.add_argument('-u', '--username', type=str, default='', dest='usernames', help='Accept comma-separated usernames, and only scrape submissions from that. If omitted, will scrape all submissions by default')
    parser.add_argument('-o', '--output-folder', type=str, default='', dest='output_folder', help='Output folder')

    args = parser.parse_args()
    scraper.scrape(args)


if __name__ == "__main__":
    main()
