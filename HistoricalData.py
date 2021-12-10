from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    # def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
    #     print("Tick Price. Ticker id: ", reqId, " tickType: ", TickTypeEnum.to_str(tickType), " Price:", price, end=' ')
    #
    # def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
    #     print("Tick Size. Ticker id: ", reqId, " tickType: ", TickTypeEnum.to_str(tickType), " Size:", size)


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "USD"

    # app.reqMarketDataType(4)  # delayed - frozen data if live is not available
    # app.reqMktData(1, contract, "", False, False, [])
    app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])
    app.run()


if __name__ == "__main__":
    main()
