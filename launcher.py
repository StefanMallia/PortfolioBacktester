from PortfolioClass import Portfolio
from datetime import date
import matplotlib.pyplot as plt

portfolio = Portfolio(10000,date(2010,1,1))
portfolio.addSecurity('AAPL', 'USD', date(2010,1,2), 5, date(2016,1,15))
portfolio.addSecurity('MSFT', 'USD', date(2010,1,2), 5, date(2016,1,15))
print(portfolio.tabulation)
plt.plot(portfolio.tabulation.sum(axis=1))
plt.show()
