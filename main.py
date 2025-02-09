import glob
import pandas as pd
import get_view
import utils
import os
import datetime
import multiprocessing
import argparse


# usage python main.py -con yes -pages 300   -proxy yes  // This is used for scrape with proxy servers list.
# usage python main.py  -pages 30 -start 0 -end 2 -proxy no  //This is used for scrape with a range of pages only.

def latest_file():
    if os.name == "nt":
        # window
        filepath = os.getcwd() + "\\output\\" + "*.csv"
    else:
        # other
        filepath = os.getcwd() + "/output/" + "*.csv"
    list_of_files = glob.glob(filepath)  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    if os.name == "nt":
        return latest_file.split("\\")[-1]
    else:
        return latest_file.split("/")[-1]
def welcome():
    print("How many pages each csv contain ?")
    x = int(input("x = "))
    return x


def devide_part(start, stop):
    start_time = (datetime.datetime.now())
    member_urls = get_view.scrape_view_link(range(start, stop))
    filename, filepath = utils.get_file_name(start, stop)
    utils.fetch_and_parse(urls=member_urls)

    # Clear error list before run again
    while (utils.error_urls != []):
        error_urls_again = utils.error_urls.copy()
        utils.fetch_and_parse(urls=error_urls_again)

    # Save result
    utils.dftemps.to_csv(filepath)
    end = (datetime.datetime.now()) - start_time
    print(f"Time taken: {end} - Output file at: {filepath}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Web scraping")
    parser.add_argument("-con", help="Continue the job or not", required=False)
    parser.add_argument("-pages", help="Total pages each CSV file.", required=True)
    parser.add_argument("-start", help="Start of range", required=False)
    parser.add_argument("-end", help="End of range", required=False)
    parser.add_argument("-proxy", help="Use the local or proxy servers", required=True)
    args = parser.parse_args()

    number_pages = int(args.pages)
    con = args.con
    if args.start != "None":
        start = int(args.start)
    if args.end != "None":
        end = int(args.end)
    utils.proxy_apply = args.proxy

    # Define the start and end in a range if we decide to run with proxy and scrape all data.
    if args.start == "None" and args.end == "None":
        if con.lower() == "yes":
            latest_file = latest_file()
            start = round(int(latest_file.split("-")[2].strip(".csv"))/number_pages)
            end = round(10000000/number_pages)
        else:
            start = 0
            end = round(10000000/number_pages)

    #     The number of pages each file should contain.
    for i in range(start, end+1 ):
        devide_part(round(number_pages/30)*i, round(number_pages/30)*(i+1))
        get_view.member_urls.clear()
        utils.dftemps = pd.DataFrame()
