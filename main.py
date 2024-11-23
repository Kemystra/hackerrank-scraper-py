import argparse
import src.scraper as scraper


def main():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument('-t', '--token', type=str, required=True, help='Token input')
    parser.add_argument('-cn', '--contest_name', type=str, required=True, help='Contest name input')
    parser.add_argument('-cid', '--challenge_id', type=str, required=True, help='Challenge ID input')

    # Optional argument
    parser.add_argument('-d', '--delay', type=float, help='Delay input')

    args = parser.parse_args()
    scraper.scrape(args)


if __name__ == "__main__":
    main()
