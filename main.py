#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'limin'

from datetime import date
from tqsdk import TqApi, TqAuth, TqBacktest, TargetPosTask
from tqsdk.ta import MA

import datetime

'''
画图示例: 在主图中画指标线
注意: 画图示例中用到的数据不含有实际意义，请根据自己的实际策略情况进行修改
'''

api = TqApi(web_gui="http://127.0.0.1:9876", backtest=TqBacktest(start_dt=date(2018, 5, 1), end_dt=date(2018, 10, 1)), auth=TqAuth("18616770111", "yu079124"))

ticks = api.get_tick_serial("DCE.m1901")
# 获得 ni2011 10秒K线的引用
klines = api.get_kline_serial("DCE.m1901", 10)
print(datetime.datetime.fromtimestamp(klines.iloc[-1]["datetime"] / 1e9))

while True:
    api.wait_update()
    # 判断整个tick序列是否有变化
    if api.is_changing(ticks):
        # ticks.iloc[-1]返回序列中最后一个tick
        print("tick变化", ticks.iloc[-1])
    # 判断最后一根K线的时间是否有变化，如果发生变化则表示新产生了一根K线
    if api.is_changing(klines.iloc[-1], "datetime"):
        # datetime: 自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数
        print("新K线", datetime.datetime.fromtimestamp(klines.iloc[-1]["datetime"] / 1e9))
    # 判断最后一根K线的收盘价是否有变化
    if api.is_changing(klines.iloc[-1], "close"):
        # klines.close返回收盘价序列
        print("K线变化", datetime.datetime.fromtimestamp(klines.iloc[-1]["datetime"] / 1e9), klines.close.iloc[-1])

# 画一次指标线
ma = MA(klines, 30)  # 使用 tqsdk 自带指标函数计算均线
klines["ma_MAIN"] = ma.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线

# 由于需要在浏览器中查看绘图结果，因此程序不能退出
while True:
    api.wait_update()
