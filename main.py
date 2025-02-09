import glob
import pandas as pd
import get_view
import utils
import os
import datetime
import multiprocessing
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
    latest_file = latest_file()
    number_pages = welcome()
    continue_or_not = input("Continue? (y/n): ")
    if continue_or_not.lower() == "y":
        start = round(int(latest_file.split("-")[2].strip(".csv"))/round(number_pages/30))
    else:
        start = 0
    for i in range(start, 330000 ):
        devide_part(round(number_pages/30)*i, round(number_pages/30)*(i+1))
        get_view.member_urls.clear()
        utils.dftemps = pd.DataFrame()
