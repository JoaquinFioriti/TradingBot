from ibapi.client import EClient
from ibapi.common import TickerId, TickAttrib
from ibapi.contract import Contract
from ibapi.ticktype import TickType, TickTypeEnum
from ibapi.wrapper import EWrapper
import pandas as pd
import time


class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        headers = ["Date", "Open", "High", "Low", "Close"]
        self.data = pd.DataFrame(columns=headers)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        # Creating new Row as a serie
        new_row = {
            'Date': bar.date,
            'Open': bar.open,
            'High': bar.high,
            'Low': bar.low,
            'Close': bar.close
        }
        self.data = self.data.append(new_row, ignore_index=True)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(self.data)
        self.data.to_csv("Holis.csv", index=False)
        self.disconnect()

    # def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
    #     print("Tick Price. Ticker id: ", reqId, " tickType: ", TickTypeEnum.to_str(tickType), " Price:", price, end=' ')
    #
    # def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
    #     print("Tick Size. Ticker id: ", reqId, " tickType: ", TickTypeEnum.to_str(tickType), " Size:", size)

    # def tickSnapshotEnd(self, reqId: int):
    #     super().tickSnapshotEnd(reqId)
    #     print("TickSnapshotEnd. TickerId:", reqId)


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    time.sleep(1)
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "USD"

    # app.reqMarketDataType(1)  # delayed - frozen data if live is not available
    # app.reqMktData(1, contract, "233", False, False, [])
    # app.reqMktData(1002, contract, "", True, False, [])
    app.reqHistoricalData(1, contract, "", "2 D", "1 min", "MIDPOINT", 0, 1, False, [])
    app.run()


if __name__ == "__main__":
    main()
