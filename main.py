import argparse
import src.scraper as scraper


def main():
    parser = argparse.ArgumentParser()

    normal_options_group = parser.add_argument_group('Normal Options', 'CLI-based options')

    # Required arguments
    normal_options_group.add_argument('-t', '--token', type=str, help='Token for authentication')
    normal_options_group.add_argument('-cn', '--contest_name', type=str, help='Contest name')
    normal_options_group.add_argument('-cid', '--challenge_ids', type=str, help='Challenge ID, can be a list of comma-separated values', dest='challenge_ids')

    # Optional argument
    normal_options_group.add_argument('-d', '--delay', type=float,
                                      help='Delay between requests, in seconds. Default is 5 seconds', default=5)
    normal_options_group.add_argument('--accepted-only', action='store_true', default=False, dest='is_accepted_only',
                                      help='Only scrape accepted submissions. Default to false')
    normal_options_group.add_argument('-u', '--usernames', type=str, default='', dest='usernames', help='Accept comma-separated usernames, and only scrape submissions from that. If omitted, will scrape all submissions by default')
    normal_options_group.add_argument('-o', '--output-folder', type=str, default='', dest='output_folder', help='Output folder')

    # Using option file
    parser.add_argument('-f', '--option-file', type=str, default='', dest='option_file', help='Option file')

    args = parser.parse_args()
    scraper.scrape(args)


if __name__ == "__main__":
    main()
