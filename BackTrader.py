import backtrader as bt


class MyStrategy(bt.Strategy):
    def __init__(self):
        print("inicializando")
        self.data_ready = False

    def notify_data(self, data, status):
        print('Dat Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True

    def log_data(self):
        ohlcv = []  # open high low close volume
        ohlcv.append(str(self.data.datetime.datetime()))
        ohlcv.append(str(self.data.open[0]))
        ohlcv.append(str(self.data.high[0]))
        ohlcv.append(str(self.data.low[0]))
        ohlcv.append(str(self.data.close[0]))
        ohlcv.append(str(self.data.volume[0]))
        print(",".join(ohlcv))  # esto lo hace como si fuera csv

    def next(self):
        self.log_data()
        if not self.data_ready:
            return

        if not self.position:
            self.buy()
        elif self.position:
            self.sell()


def start():
    print("hola")
    cerebro = bt.Cerebro()

    ibstore = bt.stores.IBStore(port=7497)
    data = ibstore.getdata(dataname='EUR.JPY', sectype='CASH', exchange="IDEALPRO", timeframe=bt.TimeFrame.Seconds)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=15)
    cerebro.broker = ibstore.getbroker()

    cerebro.addstrategy(MyStrategy)
    cerebro.run()


start()
