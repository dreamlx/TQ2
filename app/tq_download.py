from datetime import datetime, date
from contextlib import closing
from tqsdk import TqApi, TqAuth, TqSim
from tqsdk.tools import DataDownloader

import os
import yaml
import sys

file_path= ''
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print('缺少配置文件')
    exit()
with open(file_path, 'r', encoding='utf-8') as fr:
    data = yaml.load(fr, yaml.FullLoader)
print(data)
# api = TqApi(auth=TqAuth("dreamlinx@gmail.com", "y6YnRu8TWWASK2J"))
api = TqApi(auth=TqAuth("18616770111", "yu079124"))
download_tasks = {}
# # 下载从 2018-01-01 到 2018-09-01 的 SR901 日线数据
# download_tasks["SR_daily"] = DataDownloader(api, symbol_list="CZCE.SR901", dur_sec=24*60*60,
#                     start_dt=date(2018, 1, 1), end_dt=date(2018, 9, 1), csv_file_name="SR901_daily.csv")

symbols = []
for item in list(data.keys()):
    code = '' 
    for item2 in data[item]:
        code = item + '.' + item2
        symbols.append(code)


print('需要下载的列表:')
print(symbols)

str = input("0 退出, 其他继续:    ")

if str == '0':
    api.close()
    exit()

print('继续...')


download_tasks = {}

for item in symbols:
    download_tasks[item] = DataDownloader(api, symbol_list=item, dur_sec=60,
                    start_dt=datetime(2016, 1, 1, 6, 0 ,0), end_dt=datetime(2021, 12, 1, 16, 0, 0), csv_file_name= "./data/%s.csv" %item)

with closing(api):
    while not all([v.is_finished() for v in download_tasks.values()]):
        api.wait_update()
        print("progress: ", { k:("%.2f%%" % v.get_progress()) for k,v in download_tasks.items() })