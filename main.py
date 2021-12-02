import threading
import time

from ibapi.client import EClient
from ibapi.common import TickerId
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


# Class for Interactive Brokers Connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Listen for real time bars
    def realtimeBar(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        try:
            bot.onBarUpdate(reqId, time, open_, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)


class Bot:
    ib = None

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop,
                                     daemon=True)  # deamon = true means the main thread can stop all executes.
        ib_thread.start()
        time.sleep(1)
        # Get symbol info
        symbol = input("Enter the symbol you want to trade: ")
        # Creating our IB Contract OBject
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Request market data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

    # Listen to socket in separate thread
    def run_loop(self):
        self.ib.run()

    # Pass realtime bar data back to our bot object
    def onBarUpdate(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        print(close)


bot = Bot()
