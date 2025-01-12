import streamlit as st
import requests

# Set page configuration to use a wide layout
st.set_page_config(layout="wide", page_title="Stock Insights", page_icon="📈")

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

# Center content
st.markdown("""
    <style>
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
    </style>
    <div class="center-content">
""", unsafe_allow_html=True)

# Custom-styled title using a div
st.markdown("""
    <div style="background-color:#FFFFFF; padding:15px; border-radius:10px; text-align:Center; font-size:40px; font-family: Arial, sans-serif; font-weight:bold; color:#000000;">
        Simply enter a stock ticker to fetch detailed insights
    </div>
""", unsafe_allow_html=True)

# Input field for the stock ticker
ticker = st.text_input(
    label="Enter Stock Ticker",
    placeholder="e.g., AAPL, TSLA, MSFT",
    help="Enter a stock ticker symbol to fetch detailed insights."
)

# State management
if "ticker" not in st.session_state:
    st.session_state["ticker"] = None

# Function: Format large numbers into a readable format
def format_large_number(number_str):
    try:
        number = int(number_str)
        if number >= 1_000_000_000:  # Billions
            return f"{number / 1_000_000_000:.2f} Billion"
        elif number >= 1_000_000:  # Millions
            return f"{number / 1_000_000:.2f} Million"
        else:  # Less than a million
            return f"{number:,}"
    except ValueError:
        return "N/A"

# Function: Add percentage sign to Dividend Yield
def format_percentage(value):
    try:
        return f"{float(value) * 100:.2f}%"  # Convert to percentage and format
    except ValueError:
        return "N/A"

# Function: Add dollar sign to numeric values (for 52-week high/low)
def add_dollar_sign(value):
    try:
        return f"${float(value):,.2f}"
    except ValueError:
        return "N/A"

# Function: Fetch stock info
def get_stock_info(ticker):
    # Alpha Vantage API example (replace with your API key)
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=I0UIP5S724XG4FDT"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Symbol" in data:
            return {
                "Company Name": data.get("Name", "N/A"),
                "Full Name": data.get("Name", "N/A"),
                "Sector": data.get("Sector", "N/A"),
                "Industry": data.get("Industry", "N/A"),
                "Country": data.get("Country", "N/A"),
                "Description": data.get("Description", "N/A"),
                "Market Capitalization": format_large_number(data.get("MarketCapitalization", "N/A")),
                "Dividend Yield": format_percentage(data.get("DividendYield", "N/A")),
                "52-Week High": add_dollar_sign(data.get("52WeekHigh", "N/A")),
                "52-Week Low": add_dollar_sign(data.get("52WeekLow", "N/A")),
                "Financial Currency": data.get("Currency", "N/A"),
                "Exchange": data.get("Exchange", "N/A"),
            }
    return None

# Submit button to fetch data
if st.button("Enter"):
    if ticker:
        st.session_state["ticker"] = ticker.upper()
        stock_info = get_stock_info(ticker)
        if stock_info:
            st.session_state["stock_info"] = stock_info
            st.success(f"Stock information successfully fetched for {ticker.upper()}!")
        else:
            st.error("Invalid ticker or data unavailable!")
    else:
        st.error("Please enter a valid stock ticker.")

# Display stock information
if st.session_state.get("stock_info"):
    # Add custom CSS for the header
    st.markdown(f"""
    <style>
        .custom-header {{
            background-color: #FFFFFF;
            color: black;
            font-family: Arial, sans-serif;
            font-size: 28px; 
            font-weight: bold;
            padding: 10px; 
            text-align: center; 
            margin-top: 10px; 
            
        }}
    </style>
    <div class="custom-header">
        Essential Insights for {st.session_state['ticker']}
    </div>
""", unsafe_allow_html=True)

    info = st.session_state["stock_info"]

    # Display all fields
    st.markdown(f"**Company Name:** {info['Company Name']}")
    st.markdown(f"**Full Name:** {info['Full Name']}")
    st.markdown(f"**Sector:** {info['Sector']}")
    st.markdown(f"**Industry:** {info['Industry']}")
    st.markdown(f"**Country:** {info['Country']}")
    st.markdown(f"**Description:** {info['Description']}")
    st.markdown(f"**Market Capitalization:** {info['Market Capitalization']}")
    st.markdown(f"**Dividend Yield:** {info['Dividend Yield']}")  # Updated to percentage
    st.markdown(f"**52-Week High:** {info['52-Week High']}")
    st.markdown(f"**52-Week Low:** {info['52-Week Low']}")
    st.markdown(f"**Financial Currency:** {info['Financial Currency']}")
    st.markdown(f"**Exchange:** {info['Exchange']}")

    # Proceed button
    if st.button("Proceed to layer 3 for insight and prediction for analysis"):
        st.success(f"Proceeding to Layer 3 with ticker: {st.session_state['ticker']}")
    
# Button to redirect users to the home page
home_url = "https://icspcw2landingpage.streamlit.app/"

# Add a styled button for redirection
st.markdown(f"""
    <a href="{home_url}" target="_self">
        <button style="
            background-color: #007bff; 
            color: white; 
            padding: 10px 20px; 
            font-size: 16px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
        ">
            Back to Home
        </button>
    </a>
""", unsafe_allow_html=True)

# Close center-content div
st.markdown("</div>", unsafe_allow_html=True)

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
