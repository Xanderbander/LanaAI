from datetime import datetime
import backtrader as bt
from mystrategy import MyStrategy  # import your custom strategy class
from data import CustomData  # import your custom data feed

# define parameters
start_cash = 10000.0
commission_rate = 0.002
stop_loss_pct = 0.05
trailing_stop_loss_pct = 0.02

# create Cerebro instance
cerebro = bt.Cerebro(stdstats=False)

# add data feed to Cerebro
data = CustomData(dataname='my_data.csv')  # create instance of your data feed
cerebro.adddata(data)

# set broker parameters
cerebro.broker.setcash(start_cash)
cerebro.broker.setcommission(commission=commission_rate)

# add strategy to Cerebro
strats = cerebro.optstrategy(MyStrategy, stop_loss_pct=stop_loss_pct, trailing_stop_loss_pct=trailing_stop_loss_pct)[0]
cerebro.addstrategy(strats)

# run the backtest
cerebro.run()

# print final results
portvalue = cerebro.broker.getvalue()
pnl = portvalue - start_cash
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))
