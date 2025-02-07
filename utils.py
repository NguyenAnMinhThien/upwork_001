import time
import hehe
import os
import pandas
import aiohttp
import asyncio
from bs4 import BeautifulSoup

member_urls = list()

def get_table(table):
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        rows.append([el.text.strip("\n").strip("\t") for el in row.find_all('td')])
    return rows


dftemps = pandas.DataFrame()

def extract_page(data):
    global dftemps
    dftemp = pandas.DataFrame()
    try:
        soup = BeautifulSoup(data, features="html.parser")
        tables = soup.find_all('table')
        part1 = get_table(tables[7])
        inputs = tables[9].find_all("input")
        dftemp = pandas.DataFrame(
            {"Award Type": [part1[0][1]],
             "Prepared Date": [part1[0][4]],
             "Prepared User": [part1[0][7]],
             "Award Status": [part1[2][1]],
             "Last Modified Date": [part1[2][4]],
             "Last Modified User": [part1[2][7]],
             "Close Status": [part1[4][1]],
             "Close Status Date": [part1[4][4]],
             "Close By": [part1[4][7]],
             "Approved Date": [part1[6][4]],
             "Approved By": [part1[6][7]],

             })
        dftemps = pandas.concat([dftemp, dftemps], ignore_index=False)
        # flatten = list()
            # for subdata in rows:
            #     flatten = flatten + subdata
            #
            # create the dic from flatten data
            # dftemp = pandas.DataFrame(
            #     {"Legal Business Name": [flatten[flatten.index("Legal Business Name:") + 1]], "Referenced IDV": [flatten[flatten.index("Referenced IDV:") + 1]], "Unique Entity ID": [flatten[flatten.index("Unique Entity ID:") + 1]], "Action Obligation": [flatten[flatten.index("Action Obligation:") + 1]]})
    except Exception as e:
        print(e)
        pass
    finally:
        return dftemps

haha = hehe.data
mydata = extract_page(haha)
mydata.to_csv("haha.csv")

async def fetch_url(url):
    global member_urls
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                # this is the part will be change
                extract_page(data)
                #
            else:
                print(f"Error fetching {url}: {response.status}")

async def main(urls):
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    await asyncio.gather(*tasks)

def fetch_and_parse(urls):
    asyncio.run(main(urls))


def get_file_name(start,stop):
    filename = f"output-{start*30}-{stop*30}.csv"
    if os.name == "nt":
        # window
        filepath = os.getcwd() + "\\output\\" + filename
    else:
        # other
        filepath = os.getcwd() + "/output/" + filename
    return filename,filepath

