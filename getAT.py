#!usr/bin/env python3
#getAT.py
#Program that pulls ~600 stock tickers over $2000 million market cap, checks industry buy/sell analysis and groups by consensus ratio (%)


from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region
import yfinance as yf
import pandas as pd

import os
import json
from datetime import datetime
from collections import defaultdict


def all_tickers(letter: str) -> list:
    # tickers from NYSE and NASDAQ only
    all_tickers = gt.get_tickers(AMEX=False)
    
    # not setting max will get stocks with $2000 million market cap and up.
    filtered_tickers = gt.get_tickers_filtered(mktcap_min=2000)

    combined = []
    for i in all_tickers:
        if i in filtered_tickers and str(i).startswith(str(letter)):       #<-- and str(i).startswith("A")
            combined.append(i)    
    return combined


def stock_ratio(tickers:list) -> dict:

    Dict = {'forty_plus' : {},
            'thirty_five' : {},
            'thirty' : {},
            'twenty_five' : {},
            'twenty' : {},
            'rest' : {},
            'failed' : {}
            }
    
    for i in tickers:
        try:
            ticker = yf.Ticker(str(i))
            df = pd.DataFrame(ticker.recommendations)
            count = pd.DataFrame(df["To Grade"].value_counts())
            buy_ratio = (count[count.index.str.startswith("Buy")])
            sum_ratio = count["To Grade"].sum()
            count_ratio = (buy_ratio/sum_ratio)*100
            
            percent_ratio = round(count_ratio.iloc[0]["To Grade"], 2)
            if percent_ratio >= 40:
                Dict['forty_plus'][str(i)] = percent_ratio
            elif percent_ratio < 40 and percent_ratio >= 35:
                Dict['thirty_five'][str(i)] = percent_ratio
            elif percent_ratio < 35 and percent_ratio >= 30:
                Dict['thirty'][str(i)] = percent_ratio
            elif percent_ratio < 30 and percent_ratio >= 25:
                Dict['twenty_five'][str(i)] = percent_ratio
            elif percent_ratio < 25 and percent_ratio >= 20:
                Dict['twenty'][str(i)] = percent_ratio
            elif percent_ratio < 20:
                Dict['rest'][str(i)] = percent_ratio
                
        except:
            Dict['failed'][str(i)] = 0
            
            
    return Dict

if __name__ == "__main__":
    
    stocks = {}
    merged_dict = defaultdict(dict)
    merged_dict.update(stocks)
    
    Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']    
    for letter in Alphabet:
        tickers = all_tickers(str(letter))
        Dict = stock_ratio(tickers)
        print("Letter: " + str(letter))
        print(Dict)
        #print("/n")
        
        for key, nested_dict in Dict.items():
            merged_dict[key].update(nested_dict)
    
    #Make File Name + Directory
    current_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    #cwd = os.getcwd()
    python_path = "/Users/derek/Documents/Python"
    path = python_path + "/getAT/"
    name = current_time + "_getAT.txt"
    final = path + name
    
    json_stocks = json.dumps(merged_dict, indent=4)
    with open(final, "a") as f:                         #current_time + "_getAT.txt"
        f.write(json_stocks)
    





'''
#TEST CASE
stock = {}
test_ticker = yf.Ticker("AMZN")
df = pd.DataFrame(test_ticker.recommendations)
count = pd.DataFrame(df["To Grade"].value_counts())
buy_ratio = (count[count.index.str.startswith("Buy")])
sum_ratio = count["To Grade"].sum()
count_ratio = (buy_ratio/sum_ratio)*100
#count_ratio
stock["AMZN"] = round(count_ratio.iloc[0]["To Grade"], 2)
stock
'''