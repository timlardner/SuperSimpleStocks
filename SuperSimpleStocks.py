
# coding: utf-8

# In[42]:

# All code in one .py file for easy reading
# All prices in pennies

import datetime

class Stock:
    # Optional argument of 'fixed dividend' to be passed if type is preferred
    def __init__(self,name,kind,par_value,last_divi,*args):
        self.symbol = name
        self.type = kind
        self.par_value = par_value
        self.last_divi = last_divi
        
        # Ensure that if type is preferred, our optional arugment is passed
        if self.type is 'Preferred':
            if len(args) is 1:
                self.fixed_divi = args[0]
            else:
                print('Unexpected combination of arguments')
    def DividendYield(self,market_value):
        if self.type is 'Common':
            return self.last_divi / market_value
        else:
            return self.fixed_divi * self.par_value / market_value
    def PERatio(self,market_value):
        try:
            PE =  market_value/self.last_divi
        except ZeroDivisionError:
            PE = float("inf")
        return PE
    
class StockManager:
    def __init__(self):
        self.symbols = []
    def add(self,stock):
        self.symbols.append(stock)
    def print_all(self):
        for symb in self.symbols:
            print(symb)
    def getStock(self,symbol):
        for symb in self.symbols:
            if symb.symbol is symbol:
                return symb
    def GeometricMean(self):
        # Using par value since we don't have a given market value for each stock
        n_stocks = len(self.symbols)
        accum = 1
        for stock in self.symbols:
            accum = accum * stock.par_value
        return accum**(1/n_stocks)
        
class Trade:
    def __init__(self,quantity,BS,price):
        self.timestamp = datetime.datetime.now()
        self.quantity = quantity
        self.BS = BS
        self.price = price
        
class TradeManager:
    def __init__(self):
        self.trades = []
    def addTrade(self,trade):
        self.trades.append(trade)
    def VolumeWeightedStockPrice(self,time_in_minutes):
        numerator = 0
        denominator = 0
        for trade in self.trades:
            current_time = datetime.datetime.now()
            to_use = current_time - datetime.timedelta(minutes=time_in_minutes)
            if trade.timestamp > to_use:
                numerator = numerator + trade.price*trade.quantity
                denominator = denominator + trade.quantity
        return numerator/denominator

Stocks = StockManager()
Stocks.add(Stock('TEA','Common',100,0))
Stocks.add(Stock('POP','Common',100,8))
Stocks.add(Stock('ALE','Common',60,23))
Stocks.add(Stock('GIN','Preferred',100,8,0.02))
Stocks.add(Stock('JOE','Common',250,13))

print('Dividend yield',Stocks.getStock('POP').DividendYield(100))
print('Dividend yield',Stocks.getStock('GIN').DividendYield(200))
print('PE Ratio:',Stocks.getStock('TEA').PERatio(200))

# Adding some random trades to keep track of
# All being timestamped with the current time
# This can easily be amended if we want to add trades either retrospectively or in the future
Trades = TradeManager()
Trades.addTrade(Trade(100,'Buy',100))
Trades.addTrade(Trade(50,'Sell',95))
Trades.addTrade(Trade(500,'Buy',130))
Trades.addTrade(Trade(200,'Sell',140))
Trades.addTrade(Trade(100,'Sell',120))

print('Volume Weighted Stock Price of trades:',Trades.VolumeWeightedStockPrice(15))
print('Geometric Mean of GBCE:',Stocks.GeometricMean())

