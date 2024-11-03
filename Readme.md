# Stock Market Alert

This Python script monitors Tesla's stock price and sends an SMS notification with relevant news articles when significant price changes occur.

## Features

- Fetches daily stock data for Tesla (TSLA) from Alpha Vantage.
- Monitors the stock price for significant changes (greater than 5%).
- Retrieves the latest news articles about Tesla from the News API.
- Sends SMS notifications via Twilio when price changes exceed the threshold.

## Prerequisites

- Python 3.x
- A Twilio account and phone number
- An Alpha Vantage API key
- A News API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
