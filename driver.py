import time
import os
import pandas
import utils
import concurrent.futures

global Total_results
def get_member_urls():
    number = 0
    members_url = list()
    Total_result =  6000
    result_per_page = 30
    count = 0
    # return a list of URLs
    while( count < (Total_result // result_per_page + 1)):
        number = number + 30
        get_urls = f"https://www.fpds.gov/ezsearch/fpdsportal?q=%20SIGNED_DATE%3A%5B2020/06/21%2C2025/02/05%5D%20%20OBLIGATED_AMOUNT%3A%5B1000%2C%29&s=FPDS.GOV&templateName=1.5.3&indexName=awardfull&x=19&y=13&start={number}"
        members_url.append(get_urls)
        count = count + 1
    return Total_result, members_url


# count = 1


def get_dataframe(members_url):
    # for member_url in members_url:
    #     get_data(member_url,Total_results)
    my_df = pandas.DataFrame()
    executor = concurrent.futures.ProcessPoolExecutor(20)
    futures = [executor.submit(get_data, member_url) for member_url in members_url]
    concurrent.futures.wait(futures)
    for future in futures:
        my_df = pandas.concat([future.result(), my_df])
    return my_df

def get_data(member_url):
    dftemps = pandas.DataFrame()
    dftemp = utils.extract_page(member_url)
    if not dftemp.empty:
        # dftemps = dftemps._append(dftemp, ignore_index= True)
        dftemps = pandas.concat([dftemp, dftemps])
    return dftemps

def sub_main(member_urls, filename, filepath):
    my_df = get_dataframe(member_urls)
    # Save file
    if os.name == "nt":
        # window
        my_df.to_csv(f".\\output\\{filename}")
    else:
        # other
        my_df.to_csv(f"./output/{filename}")
    print(f"The file has been saved at: \n{filepath}")

