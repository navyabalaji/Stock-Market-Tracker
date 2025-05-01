# STOCK MARKET TRACKER AND VISUALISER - Team 4

The **Stock Market Tracker and Visualiser** is a desktop application that allows users to:

- Track selected stocks
- Analyze historical trends
- Compare multiple stocks
- View real-time stock prices and market news
- Get trade recommendations based on historical data

It offers an intuitive GUI built using `customtkinter` and integrates APIs like Yahoo Finance and NewsAPI to fetch real-time stock and market data.

---

## Supported Platforms

- Windows
- macOS
- Linux

## How to Run

1. Clone or download the `StockMarket` folder.
2. Make sure you have Python 3.x installed.
3. Navigate to the `StockMarket` folder using the terminal:
   ```bash
   cd path/to/StockMarket
   ```
4. Run the application:
   - **Windows**:
   ```bash
   python app.py
    ```
   - **Mac/Linux**:
   ```bash
   python3 app.py
    ```

---

## Required Software and Tools

### 1. Python 3.x

Install it from the [official website](https://www.python.org/downloads/) and make sure to add Python to PATH during installation.

### 2. VS Code (Optional but Recommended)

Download from [here](https://code.visualstudio.com/). Add to PATH during installation.

### 3. pip

Usually comes with Python 3.4+. If not:

- **Windows**: `python get-pip.py`
- **Linux**: `sudo apt install python3-pip`
- **macOS**: `sudo easy_install pip` or `python3 -m ensurepip --upgrade`

---

## Python Libraries, APIs, and Databases Used

# Libraries and Modules

Ensure all libraries below are installed. If not, use:

```bash
pip install <library-name>
```

`customtkinter` – GUI creation

`pillow` – Image processing

`pandas` – Data manipulation & analysis

`matplotlib` – Visualization (line/candlestick plots)

`requests` – HTTP requests

`yfinance` – Fetching Yahoo Finance data


Additional built-in modules:

`subprocess` – Running system commands

`sys` – Interacting with Python runtime environment

`sqlite3` – Database management

`webbrowser` – Opening URLs in default browser

`threading` – Running parallel threads

`tkinter` – Messagebox dialogs


# APIs

`Yahoo Finance API` – For retrieving real-time and historical stock data

`News API` – For fetching financial market news

---

## Application Features

### 1. Login / Sign Up
- Main screen allows users to login or sign up.
- New user credentials are stored in a `users` SQLite database.

### 2. Dashboard
Displays:
- Latest stock market news
- Navigation buttons for all key features:
  - MyStocks
  - Add Stock
  - Delete Stock
  - Trade Guide (Invest/Sell)
  - Compare Stocks
  - Exit

### 3. MyStocks
- Displays stocks saved by the user.
- Click any stock to view:
  - Interactive candlestick chart
  - Latest price
  - Company details (sector, industry)

### 4. Add Stock
- User enters stock symbol, company name, and username.
- Added to the `stocks` database and visible in MyStocks.

### 5. Delete Stock
- User inputs stock symbol and username.
- Stock entry is removed from the database.

### 6. Trade Guide
#### Invest
- Enter stock symbol and company name.
- Based on 1-month historical data, get investment recommendation (safe, volatile, high growth, etc.)

#### Sell
- Enter symbol, company name, and date of purchase.
- Recommendation on whether to sell now or hold, based on current and past performance.

### 7. Compare Stocks
- Select two stocks from your MyStocks.
- Compare them over a selected time range (daily, weekly, monthly).

---

## Databases Used

- `users`: Stores login credentials
- `stocks`: Stores user's tracked stocks (username, symbol, company name)

---

## Project Structure

Each feature is modular and stored in separate Python files:

| File                 | Description                                      |
|----------------------|--------------------------------------------------|
| `app.py`             | Main file to run the application                 |
| `Stocks.py`          | Manages stock data and historical calculations   |
| `Datafetcher.py`     | Handles API calls and data formatting            |
| `ClientLogin.py`     | Login interface                                  |
| `ClientSignUp.py`    | Signup interface                                 |
| `Dashboard.py`       | User dashboard after login                       |
| `AddStock.py`        | Add stock to user's watchlist                    |
| `DeleteStock.py`     | Delete stock from user's watchlist               |
| `MyStocks.py`        | Display all saved stocks                         |
| `Visualiser.py`      | Plot candlestick charts                          |
| `StockGuide.py`      | Navigation for invest/sell features              |
| `Sell.py`, `Sell_backend.py` | Logic and UI for sell recommendation  |
| `Invest.py`, `Invest_backend.py` | Logic and UI for invest recommendation |
| `Comparison.py`      | Compare two stocks                               |

Text files in the project are used only for temporary data handling.

