from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
import yfinance as yf
from datetime import timedelta,datetime
from stockprice import get_stock_price, StockPriceCheckTool
from percentageCheck import get_best_performing_stock, StockPercentageChangeTool
from bestperformer import get_best_performing_stock, StockBestPerformerTool
from langchain.agents import initialize_agent, Tool, AgentType, create_react_agent
from dotenv import load_dotenv, find_dotenv


#Testing
symbol = 'AAPL'
price = get_stock_price(symbol)
print(f'The Stock Price for symbol {symbol} is {price}')

# Testing
stocks = ['AAPL', 'GOOG', 'MSFT', 'NFLX', 'TSLA']
days_ago = 90
best_stock, best_performance = get_best_performing_stock(stocks, days_ago)

print(f'The best performing stock over the last {days_ago} days is {best_stock} with a performance of {best_performance}%')

# load the environment details
load_dotenv()

# define the tools for AI Agent
tools = [StockPriceCheckTool(),StockPercentageChangeTool(),StockBestPerformerTool()]

llm = ChatOpenAI(temperature=0.0, verbose=True)

open_ai_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
   verbose=True
 )

'''
Uncomment this if not to use Streamlit and test
in terminal with python3


#
# Question 1:
q1 = "What is the stock price of AAPL today?"
response = open_ai_agent.invoke(q1)
print(q1)
print(f'Response 1: {response}')

# Question 2:
q2  = "Has Google's stock gone up over 3 months?"
response2 = open_ai_agent.invoke(q2)
print(q2)
print(f'Response: {response2}')

#Question 3:
q3 = "What is the best performing stock among AAPL, GOOG, MSFT, NFLX and TSLA over the last 90 days?"
response3 = open_ai_agent.invoke(q3)
print(q3)
print(f'Response: {response3}')


# Question 4: ( This is not listing correctly. Still returing the first best performer)
# q4 = "What is the second best performing Stock among AAPL, GOOG, MSFT, TSLA over 30 days?"
# response4 = open_ai_agent.invoke(q4)
# print(q4)
# print(f'Response: {response4}')
'''

# Use Streamlit to build a simple web app to interact with the AI agent
import streamlit as st
st.set_page_config(page_title="Stock Price Analysis", layout="wide")
st.title("Stock Price Analysis using Yahoo Finance")
user_question = st.text_input("Ask a question about your stocks: ")
if len(user_question) == 0:
    st.write("Please enter a question")
    st.stop()
response = open_ai_agent.invoke(user_question)
st.json(response)