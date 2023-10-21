from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def generate_datetime_range(start_date:str, end_date:str) -> list:
    date_time_range = []
    current_date = start_date
    
    while current_date <= end_date:
        current_time = datetime(current_date.year, current_date.month, current_date.day, 0, 0)
        
        while current_time <= datetime(current_date.year, current_date.month, current_date.day, 23, 30):
            date_time_range.append(current_time.strftime("%Y-%m-%d-%H-%M"))
            current_time += timedelta(minutes=30)
        
        current_date += timedelta(days=1)
    
    return date_time_range
    # return by list. example : ["2023-09-16-14-00", ..]

def getData(date:str, _location:str) -> pd.DataFrame or None:
    date = date.split('-')
    url = f'https://rrf.seoul.go.kr/content/{_location}.do?pageIndex=1&srchCategory=&menuId=&subPage=&menuNm=&year={date[0]}&month={date[1]}&date={date[2]}&hour={date[3]}&minute={date[4]}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        table = soup.find('table', class_='list_table')

        if table:
            thead = table.find('thead')
            thead_rows = thead.find_all('tr')
        
            tbody = table.find('tbody')
            tbody_rows = tbody.find_all('tr')
            headers = [th.text for th in thead_rows[0].find_all('th')]
            data = []
            for row in tbody_rows:
                row_data = [td.text for td in row.find_all('td')]
                data.append(row_data)
            df = pd.DataFrame(data, columns=headers)
            return df
    return None

def getAVG(date:str, df:pd.DataFrame, daily_df:pd.DataFrame)->pd.DataFrame:
    """
    get data from `getData()`
    update daily_df to calculate daily avg rate
    """
    new_row = {"date" : date}
    for item, group_df in df.groupby("항목"):
        values = group_df[["1호기", "2호기", "3호기"]]
        values = values.replace(["없음", "시스템 점검 중",''], np.nan).astype(float)
        average = round(values.mean(axis=1).values[0], 2)
        
        new_row [item] = average
    daily_df = pd.concat([daily_df, pd.DataFrame([new_row])], ignore_index=True)

    return daily_df

def forDataframeFormatDate(date:str) -> str:
    year, month, day, _, _ = date.split('-')
    formatted_date = f"{year}-{month}-{day}"
    return formatted_date



col = ["date", "일산화탄소(CO)", "염화수소(HCl)", "황산화물(SO2)", "먼지(Dust)", "질소산화물(NOx)"]
dataframe = pd.DataFrame(columns=col)
daily_df = pd.DataFrame(columns=col)

start_date = datetime.now() - timedelta(days=90)
end_date = datetime.now() - timedelta(days=1)

result = generate_datetime_range(start_date, end_date)
i = 0

location = {'Gangnam-gu' :'bcreb226', 'Nowon-gu': 'bcrec237', 'Mapo-gu' : 'bcred246', 'Yangchun-gu' : 'bcree257'}     # location : link_value

for key, value in location.items():
    for _date in result:
        i += 1
        print(f'[{key} {_date}] Crawling..', end='\r')
        crawling_df = getData(date=_date, _location=value)
        
        if crawling_df is None:
            print(f'Error Occured! : {key}-{value}')
            continue
        daily_df = getAVG(_date, crawling_df, daily_df)
        
        if i % 48 == 0:     # every day
            averaged_values = daily_df.drop(columns=["date"]).mean(axis=0)
            averaged_values["date"] = forDataframeFormatDate(_date)
            print(f'[{forDataframeFormatDate(_date)}] avg value to dataframe..')
            dataframe = pd.concat([dataframe, pd.DataFrame([averaged_values])], ignore_index=True)
            daily_df = pd.DataFrame(columns=col)

    dataframe.to_csv(f'{key}_AirPollutionAVG.csv', encoding='utf-8')