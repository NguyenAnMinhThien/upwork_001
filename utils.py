import argparse
import time
import os
import pandas
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import random
import proxy_list
import proxyscrape

member_urls = list()
error_urls = list()
dftemps = pandas.DataFrame()
proxy_apply = ""


# 54.255.135.139
# 14.173.75.31

def rotate_proxy():
    if proxy_apply == "yes":
        proxy = proxy_list.proxy
    else:
        proxy = ['']
    return random.choice(proxy)


def get_table(table):
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        rows.append([el.text.strip("\n").strip("\t") for el in row.find_all('td')])
    return rows


def extract_page(data):
    global dftemps
    dftemp = pandas.DataFrame()
    try:
        soup = BeautifulSoup(data, features="html.parser")
        tables = soup.find_all('table')
        part1 = get_table(tables[7])
        inputs1 = tables[9].find_all("input")
        inputs2 = tables[17].find_all("input")
        inputs3 = tables[22].find_all("input")
        inputs4 = tables[29].find_all("input")
        inputs5 = tables[37].find_all("input")
        inputs6 = tables[4].find_all("input")
        inputs7 = tables[81].find_all("input")
        dftemp = pandas.DataFrame(
            {
                "Award Type": [part1[0][1]],
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

                # inputs1
                "Award ID": [
                    f' Agency-{inputs1[0].get("value")}, Procurement Identifier-{inputs1[2].get("value")}, Modification No-{inputs1[3].get("value")}, Trans No-{inputs1[4].get("value")}'],
                "Referenced IDV ID": [
                    f' Agency-{inputs1[5].get("value")}, Procurement Identifier-{inputs1[6].get("value")}, Modification No-{inputs1[8].get("value")}'],
                "Reason for Modification": [f' {inputs1[10].get("value")}'],
                "Solicitation": [f' {inputs1[12].get("value")}'],
                "Treasury Account Symbol": [
                    f' Agency Identifier-{inputs1[13].get("value")}, Main Account-{inputs1[14].get("value")}, Sub Account-{inputs1[15].get("value")}'],

                # inputs2 = table17
                "Date Signed": [f' {inputs2[0].get("value")}'],
                "Period of Performance Start Date": [f' {inputs2[1].get("value")}'],
                "Completion Date": [f' {inputs2[2].get("value")}'],
                "Est. Ultimate Completion Date": [f' {inputs2[3].get("value")}'],
                "Solicitation Date": [f' {inputs2[4].get("value")}'],
                "Action Obligation": [f' Current-{inputs2[6].get("value")}, Total-{inputs2[7].get("value")}'],
                "Base and Exercised Options Value": [
                    f' Current-{inputs2[9].get("value")}, Total-{inputs2[10].get("value")}'],
                "Base and All Options Value (Total Constract Value)": [
                    f' Current-{inputs2[12].get("value")}, Total-{inputs2[13].get("value")}'],
                "Fee Paid for User of IDV": [f' {inputs2[14].get("value")}'],

                # inputs3 = table22
                "Constracting Office Agency ID": [f' {inputs3[0].get("value")}'],
                "Constracting Office ID": [f' {inputs3[3].get("value")}'],
                "Funding Agency ID": [f' {inputs3[6].get("value")}'],
                "Funding Office ID": [f' {inputs3[9].get("value")}'],
                "Constracting Office Agency Name": [f' {inputs3[2].get("value")}'],
                "Constraction Office Name": [f' {inputs3[5].get("value")}'],
                "Funding Agency Name": [f' {inputs3[8].get("value")}'],
                "Funding Office Name": [f' {inputs3[11].get("value")}'],

                # inputs4 - table29
                "Unique Entity ID": [f' {inputs4[0].get("value")}'],
                "Legal Business Name": [f' {inputs4[2].get("value")}'],
                "DBAN": [f' {inputs4[3].get("value")}'],
                "CAGE code": [f' {inputs4[4].get("value")}'],
                "Street": [f' {inputs4[5].get("value")}'],
                "Street2": [f' {inputs4[6].get("value")}'],
                "City": [f' {inputs4[7].get("value")}'],
                "State": [f' {inputs4[8].get("value")}, Zip-{inputs4[9].get("value")}'],
                "Country": [f' {inputs4[10].get("value")}'],
                "Phone": [f' {inputs4[12].get("value")}'],
                "Fax No": [f' {inputs4[13].get("value")}'],
                "Congressional District": [f' {inputs4[14].get("value")}'],

                # inputs5 - table37
                "Organization Type": [f' {inputs5[0].get("value")}'],
                "State of Incorporation": [f' {inputs5[1].get("value")}'],
                "Country of Incorporation": [f' {inputs5[2].get("value")}'],

                # inputs7 - table 81
                "Number of Actions": [f' {inputs7[1].get("value")}'],

                # inputs6 - table4
                "Principal Place of Performance Code": [
                    f' State-{inputs6[242].get("value")}, Location-{inputs6[243].get("value")}, Country-{inputs6[244].get("value")}'],
                "Principal Place of Performance County Name": [f' {inputs6[246].get("value")}'],
                "Principal Place of Performance City Name": [f' {inputs6[247].get("value")}'],
                "Congressional District Place of Performance": [f' {inputs6[248].get("value")}'],
                "Place of Performance Zip Code(+4)": [f' {inputs6[249].get("value")}'],

                # inputs6 - table4 also
                "Product/Service Code": [f' {inputs6[252].get("value")}, Description-{inputs6[254].get("value")}'],
                "Principal NAICS Code": [f' {inputs6[255].get("value")}, Description-{inputs6[257].get("value")}'],
                "DOD Acquistion Program": [f'  {inputs6[258].get("value")}'],
                "Country of Product or Service Origin": [f' {inputs6[261].get("value")},{inputs6[263].get("value")}'],
                "Claimant Program Code": [f' {inputs6[265].get("value")}, Description-{inputs6[267].get("value")}'],

                # inputs6 - table4 also
                "IDV Type of Set Aside": [f' {inputs6[269].get("value")}'],
                "Type of Set Aside Source": [f' {inputs6[270].get("value")}'],
                "IDV number of Offers": [f' {inputs6[271].get("value")}'],
                "Number of Offers Source": [f' {inputs6[273].get("value")}'],
                # inputs6-table4 also
                "Price Evaluation Percent Difference": [f' {inputs6[275].get("value")}'],
            })
        dftemps = pandas.concat([dftemp, dftemps], ignore_index=False)
    except Exception as e:
        print("The request is interrupted.")
        pass
    finally:
        return dftemps


def record_interrupted_request(error_requests):
    pandas.DataFrame(error_requests).to_csv("interrupted_urls.csv", index=False, mode='a', header=False)
    error_requests.clear()


async def fetch_url(url):
    global member_urls
    try:
        async with aiohttp.ClientSession() as session:
            proxy_url = rotate_proxy()
            async with session.get(url, proxy=proxy_url) as response:
                if response.status == 200:
                    data = await response.text()
                    # this is the part will be change
                    loop = asyncio.get_event_loop()
                    if data.__len__() > 2000:
                        await loop.run_in_executor(None, extract_page, data)
                    else:
                        print(f"{url} failed")
                        error_urls.append(url)
                else:
                    print(f"Error fetching {url}: {response.status}")
    except Exception as e:
        print(e)
        error_urls.append(url)
        pass


async def main(urls):
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    await asyncio.gather(*tasks)


def fetch_and_parse(urls):
    error_urls.clear()
    asyncio.run(main(urls))


def get_file_name(start, stop):
    filename = f"output-{start * 30}-{stop * 30}.csv"
    if os.name == "nt":
        # window
        filepath = os.getcwd() + "\\output\\" + filename
    else:
        # other
        filepath = os.getcwd() + "/output/" + filename
    return filename, filepath
