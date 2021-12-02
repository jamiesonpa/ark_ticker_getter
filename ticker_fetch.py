import requests
import streamlit as st


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


st.title("ARK Fund Ticker Fetching Tool")
arkk = st.sidebar.checkbox(label="ARKK")
arkg = st.sidebar.checkbox(label="ARKG")
arkf = st.sidebar.checkbox(label="ARKF")
arkw = st.sidebar.checkbox(label="ARKW")
arkq = st.sidebar.checkbox(label="ARKQ")
arkx = st.sidebar.checkbox(label="ARKX")
prnt = st.sidebar.checkbox(label="PRNT")

analyze = st.sidebar.button(label = "FETCH TICKERS")

if analyze:
    if arkg:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv","ARKG")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)
    if arkk:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv","ARKK")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)

    if arkf:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv", "ARKF")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)

    if arkw:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv","ARKW")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)

    if arkx:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv","ARKX")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)

    if arkq:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv","ARKQ")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)

    if prnt:
        ticks = get_ark_tickers("https://ark-funds.com/wp-content/uploads/funds-etf-csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv","PRNT")
        ts = ""
        for tick in ticks:
            tick = tick.strip("\n")
            ts = ts + tick + "\n"
        st.write(ts)
