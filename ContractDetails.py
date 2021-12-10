from threading import Timer

from ibapi.client import EClient
from ibapi.contract import ContractDetails, Contract
from ibapi.wrapper import EWrapper


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId: int):
        self.start()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails, "\n")

    def contractDetailsEnd(self, reqId: int):
        print("\ncontractDetails End\n")

    def start(self):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "202201"  # January 2022

        self.reqContractDetails(1, contract)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    app = TestApp()
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7497, 9)
    Timer(3, app.stop).start()  # Creating a new Thread, starting it, and 3 sec after it will stop.
    app.run()


if __name__ == "__main__":
    main()
