from pydantic import BaseModel, Field
import yfinance as yf
from langchain.tools import BaseTool
from typing import Optional, Type

# Tools
def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return round(todays_data['Close'][0])


# pydantic class for the Input to the tool
class StockPriceCheckInput(BaseModel):
    """
    Input for Stock price check tool
    """
    stock_name: str = Field(..., description="Ticker symbol of the stock or index")

class StockPriceCheckTool(BaseTool):
    name ="get_stock_price"
    description = "Useful for when you need to find out the price of stock. You should input the stock ticker used on the yfinance API"

    def _run(self, stock_name: str) -> str:
        print("Running tool...")
        """Search for documents"""
        return get_stock_price(stock_name)
    
    def _arun(self, stock_name: str) -> str:
        raise NotImplementedError("tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput

