import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import requests
import pandas as pd
from datetime import datetime
from datetime import date, datetime, timedelta


# --- SIDEBAR CODE
def get_allsymbols():
    url = "https://caddd-index2.vercel.app/top.json?t=" + str(60*60*8)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)
    json_object = response.json()
    json_object1 = []
    for char in json_object:
        json_object1.append(char['symbol'])
    return json_object1

def get_symbol_log(symbol):
    url = "https://caddd-index2.vercel.app/symbol_log_data?t="+symbol
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)
    json_object = response.json()
    return json_object

def get_klink(symbol):
    url = "https://caddd-index2.vercel.app/cklines?symbol="+symbol
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    json_object = response.json()
    Open_time = []
    Open = []
    High = []
    Low = []
    Close = []
    for char in json_object["data"]:
        Open_time.append(char[0])
        Open.append(char[2])
        High.append(char[4])
        Low.append(char[5])
        Close.append(char[3])

    data = {'Open_time': Open_time,
        'Open' : Open,
        'High' : High,
        'Low' : Low,
        'Close' : Close}
    df1 = pd.DataFrame(data)
    return df1

options = get_allsymbols()
ticker = st.sidebar.selectbox('Select', options)

# --- MAIN PAGE
st.header('MAIN')
df = get_klink(ticker)
log = get_symbol_log(ticker)

fig = go.Figure(data=[go.Candlestick(x=df['Open_time'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.update_layout(
                title=ticker + " ticker",
                yaxis_title= ' Price', width=1200, height=700)

for char in log:
    if float(char['priceChangeM5']) > 2 or float(char['priceChangeM5']) < -2:
        print(char)
        fig.add_annotation(x=char['t_now']*1000, y=char['price'],
            text=char['priceChangeM5'],
            showarrow=True,
            arrowhead=7)

st.plotly_chart(fig)
