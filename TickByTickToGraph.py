import mplfinance as mpf
import pandas as pd

df = pd.read_csv("E:\\Datos\\Escritorio\\Osma\\tuckson.csv", sep=';')

df["MidPoint"] = (df.Ask + df.Bid) / 2
df["MidVolume"] = (df.AskVolume + df.BidVolume) / 2

header = ["Date", "Open", "High", "Low", "Close", "Volume"]
dfBars = pd.DataFrame(columns=header)

tick_size = 232
first = 0
last = tick_size
lenth = len(df.index)
i = 0
while True:
    if (first > lenth - 1):
        break
    if (last > lenth - 1):
        dfAux = df.tail(first)
    else:
        dfAux = df.loc[first:last]
    print(dfAux)

    data = str(dfAux.iloc[0][0])
    data = data[0:19]
    open = dfAux.iloc[0].MidPoint
    high = dfAux["MidPoint"].max()
    low = dfAux["MidPoint"].min()
    close = dfAux[-1:]["MidPoint"].values[0]
    volume = -1

    dfBar = pd.DataFrame([[data, open, high, low, close, volume]], columns=header, index=[i])

    dfBars = pd.concat([dfBars, dfBar])
    print(dfBars)
    print("???????????????????????????????????????????????????????????????????")

    first = last + 1
    last = first + 232
    i += 1

dfBars.to_csv('Tick.csv', index=False)
dfBars.index = pd.DatetimeIndex(dfBars['Date'])

print(dfBars.iloc[-1:].High)
mpf.plot(dfBars, type='candle', style='charles', title='S&P500', ylabel='Price')
