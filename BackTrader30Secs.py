from datetime import datetime

import backtrader as bt


class MyStrategy(bt.Strategy):
    params = (
        ('fast_ema', 5)
        ('slow_ema', 25)
        ('me1', 13)
        ('me2', 21)
        ('signal', 11)
    )

    def __init__(self):
        self.ema1 = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.fast_ema)
        self.ema2 = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.slow_ema)
        self.macd = bt.indicators.MACD(self.data, period_me1=self.params.me1, period_me2=self.params.me2,
                                       period_signal=self.params.signal)
        self.macdCross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.order = None
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')  # Comment this line when running optimization

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.5f, NET %.5f' %
                 (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.5f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.5f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders. It must to be None in order to take action
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades

            # If there is a crossOver in the MACD
            if self.macdCross > 0:
                self.log(f'BUY CREATE {self.dataclose[0]:5f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if self.macdCross < 0:
                self.log(f'CLOSE CREATE {self.dataclose[0]:5f}')
                self.order = self.sell()


class start:
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000)
    data = bt.feeds.GenericCSVData(
        dataname='holis.csv',
        fromdate=datetime(2021, 12, 12),
        todate=datetime(2021, 12, 16),
        nullvalue=0.0,
        separator=',',

        dtformat=('%Y%m%d  %H:%M:%S'),
        timeframe=bt.TimeFrame.Minutes,
        compression=1,

        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=-1,
        openinterest=-1

    )
    cerebro.adddata(data)
    ('fast_ema', 5)
    ('slow_ema', 25)
    ('me1', 13)
    ('me2', 21)
    ('signal', 11)
    cerebro.potstrategy(MyStrategy, fast_ema=range(1, 7), slow_ema=range(20, 30), )
    cerebro.addobserver(
        bt.observers.BuySell,
        barplot=True,
        bardist=0.001)  # buy / sell arrows
    print("Inicially we have :", cerebro.broker.get_value())

    cerebro.run()
    cerebro.plot(style="candelstick")
    print("At the end we have :", cerebro.broker.get_value())
