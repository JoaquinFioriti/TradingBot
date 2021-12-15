from datetime import datetime
from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator)
import backtrader as bt


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.data_ready = False
        self.ema1 = bt.indicators.ExponentialMovingAverage(self.data, period=21)
        self.ema2 = bt.indicators.ExponentialMovingAverage(self.data, period=53)
        self.macd = bt.indicators.MACD(self.data, period_me1=13, period_me2=21, period_signal=11)
        self.macdCross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.order = None
        self.counter = 0

    def notify_data(self, data, status):
        print('Dat Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True

    def notify_trade(self, trade):
        print("Trade done: ", trade)

    # def log_data(self):
    #
    # # ohlcv = []  # open high low close volume
    # # ohlcv.append(str(self.data.datetime.datetime()))
    # # ohlcv.append(str(self.data.open[0]))
    # # ohlcv.append(str(self.data.high[0]))
    # # ohlcv.append(str(self.data.low[0]))
    # # ohlcv.append(str(self.data.close[0]))
    # # ohlcv.append(str(self.data.volume[0]))
    # # print(",".join(ohlcv))  # esto lo hace como si fuera csv

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def next(self):
        # self.log_data()

        # # Already in an order excecution
        # if self.order:
        #     return

        if not self.position:
            if self.macdCross[0] == 1:
                self.counter += 1
                print("Buy done, at ", self.data.open[0], self.counter)
                self.buy()

        elif self.position:
            if self.macdCross[0] == -1:
                print("Sell done, at ", self.data.open[0])
                self.sell()
    # if not self.data_ready:
    #     return
    #
    # if not self.position:
    #     print("COMPRANDO")
    #     self.buy()
    # elif self.position:
    #     print("VENDIENDO")
    #     self.sell()


def start():
    cerebro = bt.Cerebro()

    # ibstore = bt.stores.IBStore(port=7497)
    # data = ibstore.getdata(dataname='EUR.JPY', sectype='CASH', exchange="IDEALPRO", timeframe=bt.TimeFrame.Seconds)
    # data = ibstore.getdata(dataname='USD.JPY', sectype='CASH', exchange="IDEALPRO", timeframe=bt.TimeFrame.Seconds)

    data = bt.feeds.GenericCSVData(
        dataname='Tick.csv',
        fromdate=datetime(2021, 12, 8),
        todate=datetime(2021, 12, 9),
        nullvalue=0.0,

        dtformat=('%d.%m.%Y %H:%M:%S'),
        timeframe=bt.TimeFrame.Seconds,
        compression=1,

        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1

    )

    cerebro.addobserver(
        bt.observers.BuySell,
        barplot=True,
        bardist=0.001)  # buy / sell arrows
    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy)
    cerebro.run()
    cerebro.plot(style='candlestick')


start()
