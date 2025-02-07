import sys
import concurrent.futures
import asyncio
import get_view
import utils
import os
import driver
import datetime
import multiprocessing


if __name__ == '__main__':
    # total_result, member_urls = driver.get_member_urls()
    start = 0
    stop = 10
    hehe = (datetime.datetime.now())
    member_urls = get_view.scrape_view_link(range(0,3))
    filename, filepath = utils.get_file_name(start,stop)
    utils.fetch_and_parse(urls=member_urls)
    utils.dftemps.to_csv(filepath)
    haha = (datetime.datetime.now()) - hehe
    print(f"Time taken: {haha} - Output file at: {filepath}")


