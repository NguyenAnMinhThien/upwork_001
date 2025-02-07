import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup

member_urls = list()
async def fetch_url(url):
    global member_urls
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                soup = BeautifulSoup(data, features="html.parser")
                links = soup.find_all('a', title="View")
                member_urls.extend(["https://www.fpds.gov" + link.get('href').strip("javascript:getParentURL('").strip("')") for link in links])
            else:
                print(f"Error fetching {url}: {response.status}")

async def main(urls):
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    await asyncio.gather(*tasks)


def scrape_view_link(my_range):
    mylist = list()
    for i in my_range:
        mylist.append(i*30)
    urls = [
        f"https://www.fpds.gov/ezsearch/fpdsportal?indexName=awardfull&templateName=1.5.3&s=FPDS.GOV&q=SIGNED_DATE%3A%5B2020%2F06%2F21%2C2025%2F02%2F05%5D+OBLIGATED_AMOUNT%3A%5B1000%2C%29&x=11&y=13&start={number}"
        for number in mylist]
    asyncio.run(main(urls))
    return member_urls

