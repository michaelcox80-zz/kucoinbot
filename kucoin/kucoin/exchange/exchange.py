"""Implementation of functions to retrieve data from Kucoin API

This scripts contains three functions to retrieve data from the Kucoin API.

This file can be imported as a module and contains the following functions:

    * get_all_symbols - Creates and returns the list of tradable USDT pairs on Kucoin spot
    * get_candles_for_symbol - Gets all candles for the given symbol and timeframe, putting them in a df
    * get_all_candles - Gets all candles for the given symbols and timeframe, putting them in a df
    
"""

import requests as rq
import time
import pandas as pd
import threading
from exchange.helpers import *


def get_all_symbols() -> list:
    """
    Creates and returns the list of tradable USDT pairs on Kucoin spot

    Parameters
    ----------
    None
    
    Returns
    -------
    list
        List of symbols

    Raises
    ------
    APICallError
        If the API call fails
    EmptyListError
        If the list of symbols is empty after the API call was succesful
    """

    params: dict = {'market': 'USDS'}
    response: dict = rq.get(BASEURL + SYMBOLS_EP, params=params)
    
    if response.status_code == 200:
        margin_values: tuple = ("3S", "3L", "5S", "5L", "10S", "10L")
        symbols: list = [response['symbol'] for response in response.json()['data']
                   if response['quoteCurrency'] == 'USDT'
                   and bool(response['enableTrading'])
                   and not (response['symbol'].split("-")[0].endswith(margin_values))]
        symbols.pop(symbols.index('USDC-USDT'))
        
        if symbols:
            return symbols
        else:
            raise Exception("EmptyListError: The list of symbols is empty")
        
    else:
        raise Exception("APICallError: {}".format(response.status_code))
    
    
def get_all_candles(symbols: list, timeframe: str) -> pd.DataFrame:
    """
    Gets all candles for the given symbols and timeframe, putting them in a df

    Parameters
    ----------
    symbols : list
        List of symbols to download data of
    timeframe : str
        The timeframe to download the candles for

    Returns
    -------
    pd.DataFrame : The dataframe with all candles
    """
    
    def grouper(interval: int, data: list) -> list:
        """
        Groups the data into blocks of the given interval

        Parameters
        ----------
        interval : int
            The interval to group the data into
        data : list
            The data to group

        Returns
        -------
        list
            The grouped data
        """
        return [data[i:i+interval] for i in range(0, len(data), interval)]
    
    columns: list = ['time', 'open', 'close', 'high', 'low', 'volume', 'turnover']
    data: pd.DataFrame = pd.DataFrame(columns=columns)
    
    def multiple_downloads(symbols: list, data_list: list, data_lock: threading.Lock):
        for symbol in symbols:
            while True:
                try:
                    candles: list = get_candles_for_symbol(symbol, timeframe)
                    if isinstance(candles, list):
                        break
                    else:
                        continue
                except BaseException:
                    time.sleep(10)
                    continue
            
            candles.reverse()
            
            if len(candles) >= 120:
                types: dict = {'time': 'int64', 'open': 'float64', 'close': 'float64', 
                            'high': 'float64', 'low': 'float64', 'volume': 'float64', 
                            'turnover': 'float64', 'symbol': 'str'}
                new_data: pd.DataFrame = pd.DataFrame(candles, columns=columns)
                new_data['symbol'] = symbol
                new_data = new_data.astype(types)
                
                with data_lock:
                    data_list.append(new_data)
                
            else:
                if symbol in symbols:
                    symbols.remove(symbol)
    
    data_list = []
    data_lock = threading.Lock()
    threads = []
    for i in grouper(10, symbols):
        threads.append(
            threading.Thread(target=multiple_downloads, args=(i, data_list, data_lock))
        )
        threads[-1].start()
    for t in threads:
        t.join()
    data = pd.concat(data_list)
    data['timeframe'] = timeframe
    return data
