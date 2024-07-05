

from typing import List
from pydantic import BaseModel,Field
from typing import Type
from typing import Optional
from percentageCheck import get_best_performing_stock
from langchain.tools import BaseTool

class StockBestPerformerInput(BaseModel):
    """
    Represents the input data for the StockBestPerformer operation.
    """
    stock_tickers: List[str] = Field(..., description="A list of stock or index tickers to analyze.")
    days_ago: int = Field(..., description="The number of days ago to look for the best performing stock.")

class StockBestPerformerTool(BaseTool):
    name = "get_best_performing"
    description = "Useful for when you need to find the best performing stock out of a list of stocks. You should input the stock tickers used on the yfinance API and the number of days ago to look for the best performing stock"
    args_schema: Optional[Type[BaseModel]] = StockBestPerformerInput

    def _run(self, stock_tickers: List[str], days_ago: int) -> str:
        """
        Check the percentage change in stock price for the given ticker and number of days ago.
        """
        price_change_response = get_best_performing_stock(stock_tickers, days_ago)
        return price_change_response

    async def _async_run(self, stock_tickers: List[str], days_ago: int) -> str:
        """
        Async version of _run
        """
        raise NotImplementedError("tool does not support async")