import backtrader as bt


class St(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))

        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat())
        )
        txt.append('{:.5f}'.format(self.data.open[0]))
        txt.append('{:.5f}'.format(self.data.high[0]))
        txt.append('{:.5f}'.format(self.data.low[0]))
        txt.append('{:.5f}'.format(self.data.close[0]))
        txt.append('{:.5f}'.format(self.data.volume[0]))
        print(','.join(txt))

    def next(self):
        self.logdata()

    def notify_data(self, data, status, *args, **kwargs):
        print("^" * 5, "Data Status: ", data._getstatusname(status))


def run(args=None):
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=7496)
    data = store.getdata(dataname='EUR.USD-CASH-IDEALPRO', timeframe=bt.TimeFrame.Ticks, compression=1)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=1)
    cerebro.adddata(data)
    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == '__main__':
    run()
