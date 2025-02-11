import glob
import pandas as pd
import get_view
import utils
import os
import datetime
import multiprocessing
import argparse
from itertools import repeat


# usage python main.py -con yes -pages 300   -proxy yes  // This is used for scrape with proxy servers list.
# usage python main.py  -pages 30 -start 0 -end 2 -proxy no  //This is used for scrape with a range of pages only.

def latest_file(number_of_pages):
    if os.name == "nt":
        # window
        filepath = os.getcwd() + "\\output\\" + "*.csv"
    else:
        # other
        filepath = os.getcwd() + "/output/" + "*.csv"
    list_of_files = glob.glob(filepath)  # * means all if need specific format then *.csv
    if os.name == "nt":
        file_numbers = [int(file.split("\\")[-1].split("-")[1]) // number_of_pages for file in list_of_files]
        file_numbers.sort()
    else:
        file_numbers = [int(file.split('/')[-1].split("-")[1]) // number_of_pages for file in list_of_files]
        file_numbers.sort()
    for i in range(os.cpu_count()):
        count_down =file_numbers.__len__() -1 - i
        if file_numbers[count_down] == count_down:
            interrup_file = f"output-{count_down * number_of_pages}-{(count_down + 1) * number_of_pages}.csv"
            return interrup_file


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


def create_repeats(start, end):
    repeats = list()
    # each CPU will run the devide_part 2 times.
    for j in range(start // (2*os.cpu_count()), ((end + 1 - start) // (2 * os.cpu_count()))):
        repeats.append([i for i in range(j * (2 * os.cpu_count()), (j + 1) * (2 * os.cpu_count()))])

    final = (end + 1 - start) % (2 * os.cpu_count())
    if final > 0 and repeats != []:
        repeats.append([i for i in range(repeats[-1][-1] + 1, repeats[-1][-1] + final + 1)])
    elif final > 0 and repeats == []:
        repeats.append([i for i in range(0, final)])
    return repeats


def devide_part_multiprocessing(number_pages, i):
    devide_part(round(number_pages / 30) * i, round(number_pages / 30) * (i + 1))
    get_view.member_urls.clear()
    utils.dftemps = pd.DataFrame()


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
    if args.start != None:
        start = int(args.start)
    if args.end != None:
        end = int(args.end)
    utils.proxy_apply = args.proxy

    # Define the start and end in a range if we decide to run with proxy and scrape all data.
    if args.start == None and args.end == None:
        if con.lower() == "yes":
            latest_file = latest_file(number_pages)
            start = round(int(latest_file.split("-")[2].strip(".csv")) / number_pages)
            end = round(9889953 / number_pages) - 1
        #     From practical calculation, end - 1 for stop before running in forever
        else:
            start = 0
            end = round(9889953 / number_pages) - 1

    repeats = create_repeats(start, end)
    for my_repeat in repeats:
        with multiprocessing.Pool() as multiprocessing_pool:
            multiprocessing_pool.starmap(devide_part_multiprocessing, zip(repeat(number_pages), my_repeat))
