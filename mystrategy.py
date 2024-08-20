from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt


class MyStrategy(bt.Strategy):
    
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.data_close = self.datas[0].close

        # Keep track of pending orders/placements
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=15)

    def next(self):
        # Log the closing price of the series from the reference
        self.log('Close: {:.2f}'.format(self.data_close[0]))

        # If there's a pending order, don't do anything
        if self.order:
            return

        # Check if we're in the market
        if not self.position:
            # If the closing price is above the moving average, buy
            if self.data_close[0] > self.sma[0]:
                self.log('Buy at {:.2f}'.format(self.data_close[0]))
                self.order = self.buy()
        else:
            # If the closing price is below the moving average, sell
            if self.data_close[0] < self.sma[0]:
                self.log('Sell at {:.2f}'.format(self.data_close[0]))
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: {:.2f}, Cost: {:.2f}, Comm: {:.2f}'.format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm
                    ))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    'SELL EXECUTED, Price: {:.2f}, Cost: {:.2f}, Comm: {:.2f}'.format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm
                    ))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {:.2f}, NET {:.2f}'.format(
            trade.pnl, trade.pnlcomm))
