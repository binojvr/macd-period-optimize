import pandas as pd
import pandas_ta as ta
import yfinance as yf
import mplfinance as mpf

df = yf.Ticker('AAPL').history(period="1d", interval="5m")

df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
df = df.rename(columns={'MACD_12_26_9': 'MACD'}).rename(columns={'MACDs_12_26_9': 'Signal'}).rename(columns={'MACDh_12_26_9': 'Histogram'})

macd_line  = [
   mpf.make_addplot(df['MACD'], panel=2, color='blue', width=0.7),
    mpf.make_addplot(df['Signal'], panel=2, color='lime', width=0.7, secondary_y = False),
    mpf.make_addplot(df['Histogram'], type='bar',width=0.7,panel=2, color='#6E6E6E', secondary_y = False)
]
setup = dict(type='candle', volume=True, datetime_format='%Y/%m/%d', figsize=(9,5), style=cs, xrotation=False, ylabel='', ylabel_lower='')
mpf.plot(df, **setup,scale_width_adjustment=dict(volume=0.6), addplot=macd_line)
