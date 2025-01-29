# Stock-Market-Tracker
This is a project created by my teammates and I to track and analyse the stock market trend using python

The Stock Market Tracker and Visualizer is an application that provides users with up-to-date stock information and historical performance insights for various companies. It enables users to track selected stocks, analyze historical trends, and compare multiple stocks over time. Users can easily monitor the stock market and visualize changes, helping them make informed decisions.

    Name:-                                        RollNo:-
    1) Hosdurga Rohan Vittal Kamath               BT2024238
    2) Katakamsetti Vishal Sriram                 BT2024036
    3) Muppana Jatin                              BT2024127
    4) Navya Balaji                               BT2024262
    5) Varshith M Gowda                           BT2024227

Operating systems supported are Windows, Mac and Linux
    1) To run it on Windows - 
       -> Open terminal and run the command - python <filename>.py
    2) To run it on Mac/Linux -
       -> Open terminal and run the command - python3 <filename>.py

To run the application the following softwares are required:

### 1. **PYTHON INSTALLATION**(obviously)
This project requires **Python 3.x**.

For Windows:
1. Visit the official [Python download page](https://www.python.org/downloads/).
2. Download the latest version of Python for Windows.
3. Run the installer, and **make sure to check the box that says "Add Python to PATH"**.
4. Click **Install Now**.

For macOS:
1. Visit the official [Python download page](https://www.python.org/downloads/).
2. Download the latest version of Python for macOS.
3. Open the `.pkg` installer and follow the on-screen instructions.

For Linux (Ubuntu):
1. Open the terminal and run the following commands:
   ```bash
   sudo apt update
   sudo apt install python3

### 2. **VISUAL STUDIO CODE (VS CODE) INSTALLATION**

VS Code is a free, open-source code editor that is widely used for Python development. Below are the installation steps for different operating systems.

For Windows:
1. Visit the official [VS Code download page](https://code.visualstudio.com/).
2. Click on the **"Download for Windows"** button to get the installer.
3. Run the installer and follow the installation prompts.
4. **Important**: During installation, make sure to check the box that says **"Add to PATH"** (this makes it easier to launch VS Code from the terminal).
5. Once the installation is complete, open **Visual Studio Code** from the Start menu.

For macOS:
1. Visit the official [VS Code download page](https://code.visualstudio.com/).
2. Click the **"Download for macOS"** button to download the `.zip` file.
3. Open the `.zip` file and drag **Visual Studio Code** to the **Applications** folder.
4. Open VS Code from the **Applications** folder or by searching via Spotlight.

For Linux (Ubuntu/Debian-based distributions):
1. Open the terminal and run the following commands to install VS Code:
   ```bash
   sudo apt update
   sudo apt install software-properties-common apt-transport-https curl
   curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
   sudo mv packages.microsoft.gpg /usr/share/keyrings
   sudo add-apt-repository "deb [signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main"
   sudo apt update
   sudo apt install code

### 3. ** INSTALLATION OF PIP **

pip (Python Installs Packages) is Python's package manager, used to install, manage, and uninstall Python libraries and dependencies. It simplifies the process of handling external libraries in your Python projects.

pip is generally by default installed along with modern versions of python(3.4 and newer)
However, to manually install it, the following command has to be run on terminal

1. For windows -  python get-pip.py
2. For Linux(Ubuntu/Debian-based distributions) - sudo apt update
                                                  sudo apt install python3-pip
3. For Mac - sudo easy_install pip
   If python3 is already installed, the following command can be run - python3 -m ensurepip --upgrade

### FEATURES OF THE APPLICATION
    1) Main page has a client login button which the user has to click to login and an exit button to close the application
    
    ![alt text](MyScreenshots/MainPage.png)


    2) The user is expected to login if he has already registered. Else, there is an option for signup
    as well, where the user can set his username and password. The username and password of every new user is stored in a database "users".
       ![alt text](MyScreenshots/ClientLogin.png)

    3) After logging in, users are redirected to a dashboard. The dashboard displays the latest top stories and news related to the stock market. At the top of the dashboard, there is a navigation bar featuring buttons for various functionalities. They are:-
        -> Mystocks
        -> Add stock
        -> Delete stock
        -> Your Trade Guide
        -> Compare Stocks
        -> Exit
        Functionality of each button is discussed below

    4) Functionalities:

         -> MyStocks:
            - Displays the symbols of all the stocks that the user has added as buttons
            - Clicking a button redirects the user to a window displaying an interactive candlestick plot of stock price versus date.The window also shows the current stock price and provides key company details, including its sector and industry.
            - There's a 'Back to MyStocks' button that directs the user back to MyStocks.

            ![alt text](MyScreenshots/MyStocks.png)
            ![alt text](MyScreenshots/CandleStick.png)
            ![alt text](MyScreenshots/BarGraph.png)
            ![alt text](MyScreenshots/OpeningPrice.png)
            ![alt text](MyScreenshots/ClosingPrice.png)
            ![alt text](MyScreenshots/HighLowRange.png)
            ![alt text](MyScreenshots/PlotTypeDropDown.png)
            ![alt text](MyScreenshots/PeriodDropdown.png)

        -> Add Stock:
            - User can enter a stock here, which he wants to add into his MyStocks List.
            - User has to enter his username, stock symbol, the company name and click add stock.
            - This adds the details entered into a database "stocks".
            - On the basis of username, the details of the stock are queried from the database(used in MyStocks and Comparison)
            - 'Back to dashboard' button directs the user back to the dashboard.

            ![alt text](MyScreenshots/AddStock.png)

        -> Delete Stock:
            - User needs to enter his username and stock symbol that he wants to delete.
            - Upon clicking on Delete Stock, on the basis of the username, stock symbol, the stock is deleted from the database
              The same is reflected in MyStocks.

            ![alt text](MyScreenshots/DeleteStock.png)

        -> Your Trade Guide:
            - Gives recommendation to users for selling or investing in stocks
            - There are 2 buttons - Invest, Sell
            - User needs to click on invest if he has plans on investing in any stock(neednot be the stocks that he has in MyStocks).
              A new window opens where the user needs to enter the symbol of the stock he plans to invest in and the company name.Upon
              enter, the following recommendations can be given:
                  -The stock has increased significantly, consider investing.
                  -The stock price is stable, making it a safer investment.
                  -The stock has had a significant peak, but be cautious.
                  -The stock is inconsistent, consider holding off on investment.
              These recommendations are given after analysing last one month of stock data. From the data, we extract the highest price, latest price, %change in price(previous day to present day) and the standard deviation(STD) of closing price over the month. The STD of the stock highlights the consistency of prices.
            - User needs to click on sell if he has plans on selling any of the shares he has.
              A new window opens where the user needs to enter the symbol, companyname and date on which he had bought the shares. Upon enter, the application suggests on whether to go ahead and sell the stock or not. It also suggests whether to sell at once or wait for some time to lock in more profits, depending upon the market performance.

              ![alt text](MyScreenshots/Sell.png)
              ![alt text](MyScreenshots/Sell_Rec.png.png)
              ![alt text](MyScreenshots/Invest.png)
              ![alt text](MyScreenshots/Invest_Rec.png)

        -> Compare Stocks:
            - Users can compare any two stocks from their "MyStocks" list. A dropdown menu allows them to select the symbols of the two stocks they wish to compare. They can also specify the time interval for the plot (from date to date) and choose the periodicity (daily, weekly, or monthly).
         
              ![alt text](MyScreenshots/Compare.png)
        -> Exit:
            - Directs the user back to the main page.

### PYTHON LIBRARIES, APIs, DATABASES USED

1) Libraries and Modules:

   Ensure that all these libraries and modules are installed. Otherwise run:  pip install <library/modulename> in terminal
   
   - customtkinter    : Building GUI
   - pillow           : Image processing
   - pandas           : Data manipulation, analysis
   - matplotlib       : Data Visualisation through plots(candle stick, line graphs)
   - subprocess       : For running system commands
   - sys              : For access to variables and methods that interact with Python runtime environment
   - sqlite3          : Database Management System
   - requests         : Making HTTP requests
   - webbrowser       : High-level interface to allow displaying web-based documents to the user in their default web browser
   - threading        : Run multiple threads (smaller units of a process) concurrently in a program
   - yfinance         : Retrieving data from Yahoo Finance API
   - tkinter          : Used just for the messagebox

2) APIs:
   
   - Yahoo Finance API   : Retriving stocks data
   - News API            : Extracting stock market news

3) Databases:
   
   - users  : Database that stores the user information (username and password)
   - stocks : Stores the stocks the user wants to track. Consists of username, stock symbol and company name

### ClASSES AND MODULES MADE

1) Stocks.py : Creates the Stocks class with symbol and company name and defines the following methods
               - get_historical_data :Extracting the historical data of the concerned stock. Returns a Pandas data frame with the data
               - get_latest_data     :Extracting the latest data of the concerned stock. Returns a dictionary with the data - namely
                                      symbol,latest price and latest date as key
               - calculate_price_change : Percentage change in the price is calculated. Returns the percentage change

2) Datafetcher.py : Creates Datafetcher class with symbol and stocks-ticker object from yfinance. Has the following methods
                    - get_historical_data: Extracts hitorical data from Yahoo Finance API
                    - format_historical_data: Formats the pandas dataframe
                    - get_latest_price: Extract current stock price
                    - get_stock_data: Extract details about the sector, industry etc.

3) ClientLogin.py , ClientSignUp.py : contains ClientLogin and ClientSignup classes respectively. Used to build the login and signup
                                      interfaces respectively

4) Dashboard.py : contains dashboard class. Used to build the dashboard for the application

5) AddStock.py : contains AddStock class. Used to add stocks to the database "stocks"

6) DeleteStock.py : contains DeleteStock class. Used to delete stocks previously saved

7) MyStocks.py : contains MyStocks class. Used to display all the stocks saved by a user

8) Visualiser.py : contains Visualise class. Displays candle stick plot for a stock chosen by the user in MyStocks.py

9) StockGuide.py: contains StockGuide class. Gives the user an option to choose whether he wants recommendations for selling or investing.

10) Sell.py and Sell_backend.py: Recommendations for selling stock entered by user

11) Invest.py and Invest_backend.py : Recommendation for investing in stock entered by user

12) Comparison.py: Comparing 2 stocks

NOTE - There are some text files as well, in the STOCK_MARKET folder. These have been used just to hold user data on a temporary basis.

### Work Done by Team Members

The following team members have contributed to the development of the project, with specific responsibilities outlined below:

1) Hosdurga Rohan Vittal Kamath (BT2024238):

   Worked on:
     - Stocks.py
     - Datafetcher.py
     - Visualiser.py
     - StockGuide.py
         - Sell.py
         - Sell_backend.py
         - Invest.py
         - Invest_backend.py

2) Katakamsetti Vishal Sriram (BT2024036):
   
   Worked on:
     - MyStocks.py 
     - Dashboard.py

3) Muppana Jatin (BT2024127):
   
   Worked on: 
     - Comparison.py

4) Navya Balaji (BT2024262):

   Worked on: 
     - AddStock.py
     - DeleteStock.py

5) Varshith M Gowda (BT2024227):

   Worked on:
     - MainPage.py
     - ClientLogin.py
     - ClientSignup.py
