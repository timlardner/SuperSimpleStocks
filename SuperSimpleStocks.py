
# coding: utf-8

# In[42]:

# All code in one .py file for easy reading
# All prices in pennies

import datetime
import unittest

class Stock:
    # Optional argument of 'fixed dividend' to be passed if type is preferred
    def __init__(self,name,par_value,last_divi):
        self.symbol = name
        self.par_value = par_value
        self.last_divi = last_divi
            
    def PERatio(self,market_value):
        try:
            PE =  market_value/self.last_divi
        except ZeroDivisionError:
            PE = float("inf")
        return PE

class Common(Stock):
    def __init__(self,name,par_value,last_divi):
        self.type = 'Common'
        super().__init__(name,par_value,last_divi)

    def DividendYield(self,market_value):
        return self.last_divi / market_value

class Preferred(Stock):
    def __init__(self,name,par_value,last_divi,fixed_divi):
        self.type = 'Preferred'
        self.fixed_divi = fixed_divi
        super().__init__(name,par_value,last_divi)
    def DividendYield(self,market_value):
        return self.fixed_divi * self.par_value / market_value
    
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
        # Using par value since we don't have a set market value for each stock
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

class TestStockClass(unittest.TestCase):
    def setUp(self):
        self.Stocks = StockManager()
        self.Stocks.add(Common('TEA',100,0))
        self.Stocks.add(Common('POP',100,8))
        self.Stocks.add(Common('ALE',60,23))
        self.Stocks.add(Preferred('GIN',100,8,0.02))
        self.Stocks.add(Common('JOE',250,13))
    def test_dividend_yield(self):
    	# All answers pre-calculated given values above
       self.assertEqual(self.Stocks.getStock('POP').DividendYield(100),0.08)
       self.assertEqual(self.Stocks.getStock('GIN').DividendYield(200),0.01)
    def test_PE_ratio(self):
        self.assertEqual(self.Stocks.getStock('GIN').PERatio(200),25)
    def test_geometric_mean(self):
        self.assertEqual(self.Stocks.GeometricMean(),108.44717711976989)

class TestTradesClass(unittest.TestCase):
    def setUp(self):
    # Adding some random trades to keep track of
	# All being timestamped with the current time
	# This can easily be amended if we want to add trades either retrospectively or in the future
       self.Trades = TradeManager()
       self.Trades.addTrade(Trade(100,'Buy',100))
       self.Trades.addTrade(Trade(50,'Sell',95))
       self.Trades.addTrade(Trade(500,'Buy',130))
       self.Trades.addTrade(Trade(200,'Sell',140))
       self.Trades.addTrade(Trade(100,'Sell',120))
    def test_volume_weighted_stock_price(self):
       minutes = 15
       # Answer pre-calculated given values above
       precalculated_answer = 126.05263157894737
       self.assertEqual(self.Trades.VolumeWeightedStockPrice(minutes),precalculated_answer)
    	

if __name__ == '__main__':
    unittest.main()
