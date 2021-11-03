#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'limin'

from datetime import date
from tqsdk import TqApi, TqAuth, TqBacktest, TargetPosTask
from tqsdk.ta import MA

from tqsdk.tafunc import ma

import datetime

'''
画图示例: 在主图中画指标线
注意: 画图示例中用到的数据不含有实际意义，请根据自己的实际策略情况进行修改
'''

api = TqApi(web_gui="http://127.0.0.1:9876", backtest=TqBacktest(start_dt=date(2018, 5, 1), end_dt=date(2018, 10, 1)), auth=TqAuth("18616770111", "yu079124"))


SHORT = 30  # 短周期
LONG = 60  # 长周期
SYMBOL = "SHFE.bu1812"  # 合约代码

print("策略开始运行")

data_length = LONG + 2  # k线数据长度
# "duration_seconds=60"为一分钟线, 日线的duration_seconds参数为: 24*60*60
klines = api.get_kline_serial(SYMBOL, duration_seconds=60*10, data_length=data_length)
target_pos = TargetPosTask(api, SYMBOL)

while True:
    api.wait_update()

    if api.is_changing(klines.iloc[-1], "datetime"):  # 产生新k线:重新计算SMA
        short_avg = ma(klines["close"], SHORT)  # 短周期
        long_avg = ma(klines["close"], LONG)  # 长周期

        # 均线下穿，做空
        if long_avg.iloc[-2] < short_avg.iloc[-2] and long_avg.iloc[-1] > short_avg.iloc[-1]:
            target_pos.set_target_volume(-3)
            print("均线下穿，做空")

        # 均线上穿，做多
        if short_avg.iloc[-2] < long_avg.iloc[-2] and short_avg.iloc[-1] > long_avg.iloc[-1]:
            target_pos.set_target_volume(3)
            print("均线上穿，做多")
    # 画一次指标线

        short_avg = MA(klines, SHORT)  # 短周期
        long_avg = MA(klines, LONG)  # 长周期

        klines["ma_MAIN"] = long_avg.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
        klines["ma_MAIN2"] = short_avg.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
        klines["ma_MAIN2.color"] = 0xFF0000EE


