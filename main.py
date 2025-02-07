import sys
import concurrent.futures
import asyncio
import get_view
import utils
import os
import datetime
import multiprocessing

def devide_part(start,stop):
    start_time = (datetime.datetime.now())
    member_urls = get_view.scrape_view_link(range(start, stop))
    filename, filepath = utils.get_file_name(start, stop)
    utils.fetch_and_parse(urls=member_urls)
    utils.dftemps.to_csv(filepath)
    end = (datetime.datetime.now()) - start_time
    print(f"Time taken: {end} - Output file at: {filepath}")

if __name__ == '__main__':
    # total_result, member_urls = driver.get_member_urls()
    for i in range(0,3):
        devide_part(i,i+1)


