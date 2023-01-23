import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1
tesla = yf.Ticker('TSLA')
tesla_share_price_data = tesla.history(period="max")
tesla_share_price_data.reset_index(inplace=True)
print(tesla_share_price_data.head())

# 2
url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
tesla_data = requests.get(url).text
soup = BeautifulSoup(tesla_data, "html5lib")

tables = soup.find_all('table')
for index, table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        table_index = index
Tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col:
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        Tesla_revenue = Tesla_revenue.append({"Date": Date, "Revenue": Revenue}, ignore_index=True)

Tesla_revenue = Tesla_revenue[Tesla_revenue['Revenue'] != ""]
print(Tesla_revenue.tail())

# 3
gamestop = yf.Ticker('GME')
gamestop_share_price_data = tesla.history(period="max")
gamestop_share_price_data.reset_index(inplace=True)
print(gamestop_share_price_data.head())

# 4
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
gamestop_data = requests.get(url).text
soup = BeautifulSoup(gamestop_data, "html5lib")

tables = soup.find_all('table')
for index, table in enumerate(tables):
    if "Gamestop Quarterly Revenue" in str(table):
        table_index = index
gamestop_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col:
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        gamestop_revenue = gamestop_revenue.append({"Date": Date, "Revenue": Revenue}, ignore_index=True)

gamestop_revenue = gamestop_revenue[gamestop_revenue['Revenue'] != ""]
print(gamestop_revenue.tail())


# Function to make stock and revenue dashboard
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    fig.add_trace(
        go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"),
                   name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True),
                             y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


# 5
make_graph(tesla_share_price_data, Tesla_revenue, 'Tesla')

# 6
make_graph(gamestop_share_price_data, gamestop_revenue, 'Gamestop')