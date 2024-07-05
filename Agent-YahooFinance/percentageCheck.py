from typing import List, Optional
from typing import ClassVar
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf
from datetime import timedelta,datetime

# Tool Functions
def get_price_change_percent(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    #Convert the format before sending it to the API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    # historical data from yahoo finance
    history_data = ticker.history(start=start_date_str, end=end_date_str)
    # Get closing prices
    old_price =history_data.iloc[0]['Close']
    new_price = history_data.iloc[-1]['Close']

    #calculate the price change percentage
    price_change = (new_price - old_price) / old_price * 100
    return round(price_change, 2)

def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    #Convert the format before sending it to the API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    # historical data from yahoo finance
    history_data = ticker.history(start=start_date_str, end=end_date_str)
    # Get closing prices
    old_price =history_data.iloc[0]['Close']
    new_price = history_data.iloc[-1]['Close']

    #calculate the price change percentage
    price_change = (new_price - old_price) / old_price * 100
    return round(price_change, 2)

def get_best_performing_stock(stocks, days_ago):
    best_stock = None
    best_performance = float('-inf')

    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if performance is None  or performance > best_performance:
                best_performance = performance
                best_stock = stock
        except Exception as e:
            print(f"Error processing {stock}: {e}")
    return best_stock, best_performance


class StockChangePercentageCheckInput(BaseModel):
    """
    Input class for StockChangePercentageCheck
    """
    stock_ticker: str = Field(..., description="Stock ticker symbol")
    days_ago: int = Field(..., description="Number of days to look back for price change")

class StockPercentageChangeTool(BaseTool):
    """
    Tool for checking the percentage change in stock price over a given number of days.
    """
    name = "get_price_change_percent"
    description = "Check the percentage change in stock price over a given number of days"
    args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput

    def _run(self, stock_ticker: str, days_ago: int) -> str:
        """
        Check the percentage change in stock price for the given ticker and number of days ago.
        """
        price_change_response = get_price_change_percent(stock_ticker, days_ago)
        return price_change_response

    async def _async_run(self, stock_ticker: List[str], days_ago: int) -> str:
        """
        Async version of _run
        """
        raise NotImplementedError("tool does not support async")