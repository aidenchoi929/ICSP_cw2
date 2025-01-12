import yfinance as yf
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Set up the page configuration
st.set_page_config(page_title="FinSight AI", page_icon="🧊", layout="wide")

# Main banner
st.markdown("""
    <style>
        .main-banner {
            background-color: #FFFFFF;
            padding: 30px;
            text-align: center;
            border-radius: 30px;
            border: 5px dotted black;
            font-size: 20px;
            font-family: Arial, sans-serif;
            font-weight: bold;
            color: #000000;
        }
    </style>
    <div class="main-banner">
        This product is for informational purposes only and should not be considered financial advice. Please note that past performance is not indicative of future results. Investments carry inherent risks, including the potential loss of principal. Consult with a qualified financial advisor to assess your individual circumstances before making any investment decisions.
    </div>
""", unsafe_allow_html=True)

# Page title and subtitle centered
st.markdown("""
    <div style="text-align: center;">
    <br> 
        <div style="font-size: 50px; font-weight: bold; margin-bottom: 10px;">✨Welcome to FinSight AI!✨</div>
        <div style="font-size: 30px; font-weight: normal; margin-bottom: 10px;">❤️Predictions for your beloved assets with meaningful insights❤️</div>
    <br>    
    </div>
""", unsafe_allow_html=True)


# FX Rate API Integration
fx_api_key = "0e906beefcc6370c11f59308"
fx_api_url = f"https://v6.exchangerate-api.com/v6/{fx_api_key}/latest/SGD"

try:
    fx_response = requests.get(fx_api_url)
    fx_data = fx_response.json()
    usd_rate = fx_data['conversion_rates']['USD']
    cny_rate = fx_data['conversion_rates']['CNY']
    gbp_rate = fx_data['conversion_rates']['GBP']
    jpy_rate = fx_data['conversion_rates']['JPY']
    fx_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
except Exception as e:
    usd_rate = cny_rate = gbp_rate = jpy_rate = "Error fetching data"
    fx_timestamp = "Error fetching timestamp"

# FED Interest Rate API Integration
fed_api_key = "1dc3b41f131bcfbeeaf83889c0df4087"
fed_api_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={fed_api_key}&file_type=json"

try:
    fed_response = requests.get(fed_api_url)
    fed_data = fed_response.json()
    observations = fed_data['observations']
    fed_rate = observations[-1]['value']  # Latest interest rate
    prev_fed_rate = observations[-2]['value']  # Previous interest rate
    fed_change = float(fed_rate) - float(prev_fed_rate)  # Calculate change
    fed_change_display = f"{fed_change:+.2f}"  # Format change with sign
    fed_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
except Exception as e:
    fed_rate = fed_change_display = "Error fetching data"
    fed_timestamp = "Error fetching timestamp"

# Scraping FOMC Meeting Data
fomc_url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
try:
    fomc_response = requests.get(fomc_url)
    soup = BeautifulSoup(fomc_response.text, 'html.parser')

    # Find the next meeting date
    meeting_dates = soup.find_all('td', class_='fomc-meeting-date')
    next_meeting_date = meeting_dates[0].text.strip() if meeting_dates else "No upcoming meeting found"
except Exception as e:
    next_meeting_date = "Error fetching data"

fed_meeting = next_meeting_date

# Fetching Fear and Greed Index Data
fear_and_greed_api_url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
fear_and_greed_api_key = "6a733b2a-2c15-4036-8b0b-cdcf52a5955d"  # Your API Key
headers = {"X-CMC_PRO_API_KEY": fear_and_greed_api_key}

try:
    response = requests.get(fear_and_greed_api_url, headers=headers, params={"limit": 1})
    response_data = response.json()
    
    # Extract the latest Fear and Greed Index value and classification
    if response_data.get("data"):
        fear_and_greed_data = response_data["data"][0]
        fg_value = fear_and_greed_data["value"]  # Index value (e.g., 50)
        fg_classification = fear_and_greed_data["value_classification"]  # Classification (e.g., "Neutral")
        fg_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp of data fetch
    else:
        fg_value = "N/A"
        fg_classification = "N/A"
        fg_timestamp = "Error fetching timestamp"
except Exception as e:
    print(f"Error fetching Fear and Greed data: {e}")
    fg_value = "N/A"
    fg_classification = "N/A"
    fg_timestamp = "Error fetching timestamp"

# Layout setup
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(f"""
        <div style="
            text-align: center; 
            background-color: #FFFFFF; 
            padding: 20px; 
            border-radius: 15px; 
            border: 5px dotted black;
            width: 100%; 
            height: 280px; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            box-sizing: border-box;">
            <div style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">Today's FX rate</div>
            <p style="font-size: 24px; font-weight: bold; color:rgb(14, 14, 14);">1 SGD =</p>
            <p>{usd_rate} USD<br>
               {cny_rate} Chinese Yuan<br>
               {gbp_rate} Pound Sterling<br>
               {jpy_rate} Japanese Yen</p>
            <p style="font-size: 12px; color: #6c757d;">Last updated: {fx_timestamp}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="
            text-align: center; 
            background-color: #FFFFFF; 
            padding: 20px; 
            border-radius: 15px; 
            border: 5px dotted black;
            width: 100%; 
            height: 280px; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            box-sizing: border-box;">
            <div style="font-size: 20px; font-weight: bold; margin-top: 10px; margin-bottom: 10px;">Current FED Interest Rate</div>
            <p style="font-size: 32px; font-weight: bold;">{fed_rate}% <span style="color: red;">({fed_change_display}%)</span></p>
            <p style= "font-size: 20px; font-weight: bold;">Next FOMC meeting:<br>{next_meeting_date}</p>
            <p style="font-size: 12px; color: #6c757d; margin-top: 20px; ">Last updated: {fed_timestamp}</p>
        </div>
    """, unsafe_allow_html=True)

# Alpha Vantage API Key
alpha_vantage_api_key = "I0UIP5S724XG4FDT"

# Function to fetch market data
def fetch_market_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

# Function to get the latest close price
def get_latest_close(data):
    if "Time Series (5min)" in data:
        time_series = data["Time Series (5min)"]
        latest_timestamp = sorted(time_series.keys())[-1]
        latest_close = time_series[latest_timestamp]["4. close"]
        return round(float(latest_close), 2), latest_timestamp  # Rounded to two decimals
    return "Error", "N/A"

# Dropdown for market selection (only in col3)
markets = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ (QQQ)": "QQQ",
    "Dow Jones Industrial Average (DIA)": "DIA",
    "Russell 2000 (IWM)": "IWM",
    "FTSE 100 (ISF.L)": "ISF.L",
    "Nikkei 225 (EWJ)": "EWJ",
    "DAX (EWG)": "EWG",
    "Gold (GLD)": "GLD",
    "Oil (USO)": "USO",
}

with col3:
    # Dropdown inside the banner
    selected_market = st.selectbox(
        "Choose a Market",
        list(markets.keys()),
        key="market_dropdown",  # Key ensures state tracking
        label_visibility="visible"  # Make the label visible for clarity
    )
    # Fetch data for the selected market
    selected_symbol = markets[selected_market]
    market_data = fetch_market_data(selected_symbol, alpha_vantage_api_key)
    market_close, market_timestamp = get_latest_close(market_data) if market_data else ("Error", "N/A")

    # Market Performance Banner with Dropdown
    st.markdown(f"""
        <div style="
            text-align: center; 
            background-color: #FFFFFF; 
            padding: 10px; 
            border-radius: 15px; 
            border: 5px dotted black;
            width: 100%;
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            box-sizing: border-box;">
            <div style="font-size: 20px; font-weight: bold; color: #212121;  margin-top: 10px; margin-bottom: 10px;">
                Market Performance
                <div style="font-size: 18px; font-weight: bold; color: #212121;">{selected_market}</div>
                <div style="font-size: 32px; font-weight: bold; color: #17a2b8;">${market_close}</div>
                <p style="font-size: 12px; color: #6c757d; margin-top: 15px; margin-bottom: 0px;">Last updated: {market_timestamp}</p>
            </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style="
            text-align: center; 
            background-color: #FFFFFF; 
            padding: 20px; 
            border: 5px dotted black;
            border-radius: 15px; 
            width: 100%; 
            height: 280px; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            box-sizing: border-box;">
            <div style="font-size: 20px; font-weight: bold; color: #212121; margin-bottom: 10px;">Cryptocurrency market's Fear and Greed Index</div>
            <div style="
                background-color: #FFFFFF; 
                padding: 15px; 
                border-radius: 10px; 
                border: 1px solid #E0E0E0; 
                width: 90%; 
                margin: 0 auto;">
                <div style="font-size: 40px; font-weight: bold; color: {'green' if fg_classification == 'Neutral' else 'red'};">{fg_value}</div>
                <div style="font-size: 18px; color: #606060;">{fg_classification}</div>
            </div>
            <p style="font-size: 12px; margin-top: 18px; color:#6c757d;">Last updated: {fg_timestamp}</p>
        </div>
    """, unsafe_allow_html=True)


# Add blank space
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

col5, col6 = st.columns(2, gap="medium")

with col5:
    st.markdown("""
        <div style="
            background-color: #FFFFFF; 
            padding: 20px; 
            border-radius: 15px; 
            border: 5px dotted black; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 350px;">
            <div style="font-size: 50px; font-weight: bold; text-align: center; margin-bottom: 20px;">US Stocks 🇺🇸💰📈</div>
            <button class="button-89" onclick="window.location.href='https://icspcw2-n33r4exgrg7wi2qpidkey4.streamlit.app/'"
 role="button">Gain stock insights</button>
        </div>

        <style>
            .button-89 {
              --b: 3px;   /* border thickness */
              --s: .45em; /* size of the corner */
              --color:rgb(0, 0, 0);
              
              padding: calc(.5em + var(--s)) calc(.9em + var(--s));
              color: var(--color);
              --_p: var(--s);
              background:
                conic-gradient(from 90deg at var(--b) var(--b),#0000 90deg,var(--color) 0)
                var(--_p) var(--_p)/calc(100% - var(--b) - 2*var(--_p)) calc(100% - var(--b) - 2*var(--_p));
              transition: .3s linear, color 0s, background-color 0s;
              outline: var(--b) solid #0000;
              outline-offset: .6em;
              font-size: 25px;
              font-weight: bold;

              border: 0;

              user-select: none;
              -webkit-user-select: none;
              touch-action: manipulation;
            }

            .button-89:hover,
            .button-89:focus-visible {
              --_p: 0px;
              outline-color: var(--color);
              outline-offset: .05em;
            }

            .button-89:active {
              background: var(--color);
              color: #fff;
            }
        </style>
    """, unsafe_allow_html=True)


with col6:
    st.markdown("""
        <div style="
            background-color: #FFFFFF; 
            padding: 20px; 
            border-radius: 15px; 
            border: 5px dotted black; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 350px;">
            <div style="font-size: 50px; font-weight: bold; text-align: center; margin-bottom: 20px;">Cryptocurrency ₿🚀</div>
            <button class="button-89" onclick="window.location.href='crypto_page'" role="button">Gain crypto insights</button>
        </div>

        <style>
            .button-89 {
              --b: 3px;   /* border thickness */
              --s: .45em; /* size of the corner */
              --color:rgb(0, 0, 0);
              
              padding: calc(.5em + var(--s)) calc(.9em + var(--s));
              color: var(--color);
              --_p: var(--s);
              background:
                conic-gradient(from 90deg at var(--b) var(--b),#0000 90deg,var(--color) 0)
                var(--_p) var(--_p)/calc(100% - var(--b) - 2*var(--_p)) calc(100% - var(--b) - 2*var(--_p));
              transition: .3s linear, color 0s, background-color 0s;
              outline: var(--b) solid #0000;
              outline-offset: .6em;
              font-size: 25px;
              font-weight: bold;

              border: 0;

              user-select: none;
              -webkit-user-select: none;
              touch-action: manipulation;
            }

            .button-89:hover,
            .button-89:focus-visible {
              --_p: 0px;
              outline-color: var(--color);
              outline-offset: .05em;
            }

            .button-89:active {
              background: var(--color);
              color: #fff;
            }
        </style>
    """, unsafe_allow_html=True)


# Footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f8f9fa;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color:rgb(0, 0, 0);
        }
    </style>
    <div class="footer">
        All rights reserved by Aiden Choi for ICSP © 2025
    </div>
""", unsafe_allow_html=True)
