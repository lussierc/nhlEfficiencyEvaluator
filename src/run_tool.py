"""Runs the various components of the tool."""

import scraper, data_cleaner

def main():
    """Runs the project."""

    print("Welcome to the NHL Statistics Projection Tool:")
    input_dec = input("* Do you want to scrape data? Y/N: ")

    if input_dec.upper() == 'Y':
        scraper.run_scraper()
        data_cleaner.main()
    else:
        data_cleaner.main()
