from datetime import datetime
from decimal import Decimal

from ibapi.client import EClient
from ibapi.common import TickAttribLast, TickAttribBidAsk
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: Decimal, askSize: Decimal, tickAttribBidAsk: TickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        print("BidAsk. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
              "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:",
              tickAttribBidAsk.askPastHigh)

    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        super().tickByTickMidPoint(reqId, time, midPoint)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "MidPoint:", midPoint)

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: Decimal, tickAtrribLast: TickAttribLast, exchange: str,
                          specialConditions: str):

        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAtrribLast,
                                  exchange, specialConditions)
        if tickType == 1:
            print("Last.", end='')
        else:
            print("AllLast.", end='')
        print(" ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "Price:", price, "Size:", size, "Exch:", exchange,
              "Spec Cond:", specialConditions, "PastLimit:", tickAtrribLast.pastLimit, "Unreported:",
              tickAtrribLast.unreported)


class ContractMaker:

    @staticmethod
    def createContract(symbol: str, secType: str, exchange: str, currency: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.exchange = exchange
        contract.currency = currency
        return contract


class Main:
    # Connecting to the TWS API
    app = TestApp()
    app.connect("127.0.0.1", 7496, 0)

    # Creating a contract
    contract = ContractMaker.createContract("EUR", "CASH", "IDEALPRO",
                                            "USD")  # Using this active (forex) beacuse of we do not have the main subscription

    app.reqTickByTickData(19004, contract, "MidPoint", 0, False)
    app.run()


if __name__ == "__main__":
    Main()
