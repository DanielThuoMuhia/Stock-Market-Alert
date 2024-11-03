import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

STOCK_NAME = "TSLA" # Tesla stock name
COMPANY_NAME = "Tesla Inc" # Tesla company name

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
news_api_key = os.getenv("NEWS_API_KEY")
stock_api_key = os.getenv("STOCK_API_KEY")
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
my_number = os.getenv("MY_NUMBER")



# stock market parameters
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

# News parameters
NEWS_PARAMS = {
    "apiKey": news_api_key,
    "q": COMPANY_NAME
}

# Fetch stock data
response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Get the latest two closing prices
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])
day_before_yesterday_price = float(data_list[1]['4. close'])

# Calculate the difference and percentage change
difference = yesterday_closing_price - day_before_yesterday_price

up_down = None
if difference > 0 :
    up_down = "⬆️"
else :
    up_down = "⬇️"
diff_percent = round((abs(difference) / yesterday_closing_price) * 100, 2)

# Fetch news if the price change exceeds 5%
if diff_percent > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMS)
    news_response.raise_for_status()
    news_articles = news_response.json()["articles"][:3]

    # Format articles for SMS
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in news_articles
    ]

    # Send each article as a separate SMS via Twilio
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= twilio_number,
            to= my_number
        )
        print(f"Message sent: {message.sid}")