import json
from openai import OpenAI
from prompt_utils.openai_utils import openai_function_call
from yahoo_fin import stock_info as si
import yfinance as yf
import datetime
from bs4 import BeautifulSoup
import requests

# Fetch stock data from Yahoo Finance


def get_historical_stock_data(ticker_symbol):
    # Calculate the date 5 days ago from today
    five_days_ago = datetime.datetime.now() - datetime.timedelta(days=5)

    # Get historical market data
    historical_prices = si.get_data(ticker_symbol, start_date=five_days_ago)

    # Display the last 5 days' prices
    return historical_prices.tail(5)


def get_stock_news(topic):
    # Google Search URL
    url = f"https://www.google.com/search?q={topic}+news"

    # Set headers to mimic a browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send the request
    response = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("div", class_="kCrYT")

    news = []
    for n in soup.find_all("div", class_="kCrYT"):
        news.append(n.text)
    for n in soup.find_all("div", "IJl0Z"):
        news.append(n.text)

    # if len(news)>6:
    #     news=news[:4]
    # else:
    #     news=news

    news_string = ""
    for i, n in enumerate(news):
        news_string += f"{i}. {n}\n"
    top5_news = "Recent News:\n\n" + news_string

    return top5_news


def get_detail_statement(ticker_symbol):
    # Fetch data
    company = yf.Ticker(ticker_symbol)

    # Get income statement, balance sheet, and cash flow statement
    income_statement = company.financials
    balance_sheet = company.balance_sheet
    cash_flow_statement = company.cashflow

    detail_statement = f""" Here is the details of statement for ticker {ticker_symbol}: 

    Income Statement for {ticker_symbol} : 
    {income_statement}

    Balance Sheet for {ticker_symbol} : 
    {balance_sheet}

    Cash flow statement for {ticker_symbol} : 
    {cash_flow_statement}

    """
    return detail_statement


def buy_order(ticker):
    print(f"A buy order has been submitted for {ticker}")


def sell_order(ticker):
    print(f"A sell order has been submitted for {ticker}")
