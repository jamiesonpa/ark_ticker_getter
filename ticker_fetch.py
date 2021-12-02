from PIL.Image import ROTATE_90
import requests
import pandas as pd
from streamlit.elements.arrow import _pandas_style_to_css
from yahoo_fin import stock_info as si 
from pandas_datareader import DataReader
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import math as maths

def get_news_data(tickers):
    base_link = "https://finviz.com/quote.ashx?t="
    links = []
    for ticker in tickers:
        links.append(base_link+ticker)

    return_vals = []
    for link in links:
        # print("\n")
        # print("getting news for " + link.split("=")[1])
        hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
        r = requests.get(link, headers = hdr)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = None
        try:
            table = soup.find_all("table",{"class": "fullview-news-outer"})
        except:
            pass
        try:
            if len(table) > 0:
                rows = table[0].find_all("tr")
                data = {}
                months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                most_recent_date = None
                most_recent_date_found = False
                second_most_recent_date = None
                second_most_recent_date_found = False
                for row in rows:
                    for month in months:
                        if row.text.find(month) != -1:
                            if most_recent_date_found == False:
                                most_recent_date = row.text.split(" ")[0]
                                # print("most recent : " + most_recent_date)
                                most_recent_date_found = True
                            else:
                                if second_most_recent_date_found == False:
                                    second_most_recent_date = row.text.split(" ")[0]
                                    # print("second most recent: " + second_most_recent_date)
                                    second_most_recent_date_found = True
                recent_news_list = []
                for row in rows:
                    if row != None:
                        if row.text.find(second_most_recent_date) != -1:
                            break
                        else:
                            if row.text.find("Motley Fool") == -1:
                                if row.text.find("TipRanks") == -1:
                                    if row.text.find("ACCESSWIRE") == -1:
                                        if row.text.find("Law Offices") == -1:
                                            if row.text.find("Business Daily") == -1:
                                                if row.text.find("INVESTOR ALERT") == -1:
                                                    subdiv1 = row.find("div")
                                                    subdiv2 = subdiv1.find("div")
                                                    suba = subdiv2.find("a")
                                                    link = suba["href"]
                                                    st.write(str(link))
                                                    recent_news_list.append((row.text.replace("\xa0\xa0"," "), str(link)))
                # st.write(((link.split("="))))
                for item in recent_news_list:
                    st.write("\t" + item[0] + "; " + item[1])
        except:
            pass

def get_ark_tickers(fund, name):
    #this is the link that downloads the csv of the current ARKG holdings
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
    ark_holdings_csv = fund
    ark_holdings = str(requests.get(ark_holdings_csv, headers=hdr).content).split(name)
    ark_holdings = ark_holdings[1:len(ark_holdings)-1]
    ark_tickers = []
    ark_names = []
    for line in ark_holdings:
        ticker = line.split(",")[2].replace('"',"")
        if ticker.find(" ") != -1:
            ticker = ticker.split(" ")[0]
        if ticker != "":
            ark_tickers.append(ticker)
            name = line.split(",")[1].replace('"',"")
            name = name.replace(" INC", "")
            name = name.replace(" CORP", "")
            name = name.replace("CLASS-A","")
            name = name.replace("C-A","")    
            name = name.replace("-A","")     
            name = name.replace(" - ADR","")
            name = name.replace(" -CLASS A","")  
            name = name.replace("-SP ADR","")  
            name = name.replace(" AG","")  
            name = name.replace(" - CLASS A","")
            name = name.replace("-CLASS A","")
            ark_names.append(name)


    tickers = ark_tickers
    return tickers


st.title("ARK Fund Tools")
arkk = st.sidebar.checkbox(label="ARKK")
arkg = st.sidebar.checkbox(label="ARKG")
arkf = st.sidebar.checkbox(label="ARKF")
arkw = st.sidebar.checkbox(label="ARKW")
arkq = st.sidebar.checkbox(label="ARKQ")
arkx = st.sidebar.checkbox(label="ARKX")
prnt = st.sidebar.checkbox(label="PRNT")

analyze = st.sidebar.button(label = "FETCH TICKERS")
news = st.sidebar.button(label = "FETCH HEADLINES")

if news:
    if arkg:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv","ARKG")
        get_news_data(ticks)

    if arkk:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv","ARKK")
        get_news_data(ticks)

    if arkf:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv", "ARKF")
        get_news_data(ticks)

    if arkw:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv","ARKW")
        get_news_data(ticks)

    if arkx:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv","ARKX")
        get_news_data(ticks)

    if arkq:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv","ARKQ")
        get_news_data(ticks)

    if prnt:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv","PRNT")
        get_news_data(ticks)


if analyze:
    if arkg:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv","ARKG")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)

    if arkk:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv","ARKK")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)

    if arkf:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv", "ARKF")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)

    if arkw:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv","ARKW")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)
    if arkx:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv","ARKX")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)

    if arkq:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv","ARKQ")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)

    if prnt:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv","PRNT")
        for tick in ticks:
            tick = tick.strip("\n")
            st.write(tick)
