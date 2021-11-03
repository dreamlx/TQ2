
#%%
import pandas as pd
import matplotlib.pyplot as plt

def get_diff_report(frt_near, frt_forward):
    df_near = pd.read_csv("./data/%s.csv" % frt_near)
    df_forward = pd.read_csv("./data/%s.csv" % frt_forward)

    # df_near.set_index(pd.to_datetime('datetime'), inplace=True)
    # df_forward.set_index(pd.to_datetime('datetime'), inplace=True)

    df_near.drop(columns=['datetime_nano'], inplace=True)
    df_forward.drop(columns=['datetime_nano'],inplace=True)

    df_all = df_near.merge(df_forward)

    df_all['close_diff'] = df_all["%s.close" % frt_near] - df_all["%s.close" % frt_forward]

    df_all['datetime'] = pd.to_datetime(df_all['datetime'])
    df_all.set_index('datetime', inplace=True)

    return df_all
# %%
frt_1 = 'DCE.c2203'
frt_2 = 'DCE.c2207'
df = get_diff_report(frt_1, frt_2)

print(frt_1,frt_2)
df["close_diff"].plot()
# %%
import talib as ta
df4 = df["close_diff"].resample('20T').ohlc().dropna()
# %%
df4.dropna()

# %%
atr1 = ta.ATR(df4['high'],df4['low'],df4['close'], period=12)
# %%
atr1
# %%
atr1.plot()
# %%
