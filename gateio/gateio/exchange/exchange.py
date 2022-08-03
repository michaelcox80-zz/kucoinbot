"""Implementation of functions to retrieve data from Kucoin API

This script and its child (helpers.py) contains three functions to retrieve data from the Kucoin API.

This file can be imported as a module and contains the following functions:

    * get_all_symbols - Creates and returns the list of tradable USDT pairs on Kucoin spot
    * get_candles_for_symbol - Gets all candles for the given symbol and timeframe, putting them in a df
    * get_all_candles - Gets all candles for the given symbols and timeframe, putting them in a df
    
"""

import requests as rq
import time
import pandas as pd
import threading
from exchange.helpers import get_candles_for_symbol

# Constants
BASE_URL="https://api.gateio.ws/api/v4"
SYMBOLS_EP="/spot/currency_pairs"
MARKET_EP="/spot/candlesticks"


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

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response: dict = rq.get(BASE_URL + SYMBOLS_EP, headers=headers)
    
    if response.status_code == 200:
        margin_values: tuple = ("3S", "3L", "5S", "5L", "10S", "10L")
        symbols: list = [symbol['id'] for symbol in response.json()
                   if symbol['id'].endswith('USDT')
                   and not (symbol['id'].split("_")[0].endswith(margin_values))]
        
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
    
    def multiple_downloads(symbols: list, data_list: list, data_lock: threading.Lock):
        """Python decorator to download data in parallel

        Parameters
        ----------
            symbols : list
                List of symbols to download data of (smaller group of 10)
            data_list : list
                List to append the data to (used for multithreading memory
                using Python's object by reference)
            data_lock : threading.Lock
                Lock to prevent multiple accesses to memory
        """
        columns: list = ['time', 'volume', 'close', 'high', 'low', 'open']
        for symbol in symbols:
            while True:
                try:
                    candles: list = get_candles_for_symbol(symbol, timeframe)
                    if isinstance(candles, list):
                        break
                    else:
                        continue
                except BaseException as e:
                    print(e)
                    time.sleep(10)
                    continue
            
            if len(candles) >= 150:
                new_data: pd.DataFrame = pd.DataFrame(candles, columns=columns)
                new_data['symbol'] = symbol
                with data_lock:
                    data_list.append(new_data)
                    
            else:
                if symbol in symbols:
                    with data_lock:
                        symbols.remove(symbol)
                    
    types: dict = {'time': 'int64', 'volume': 'float64', 'close': 'float64', 
                    'high': 'float64', 'low': 'float64', 'open': 'float64', 
                    'symbol': 'str'}
    data_lock = threading.Lock()
    data: pd.DataFrame = pd.DataFrame()
    data_list = []

    # Multithreading module
    threads = []
    for i in grouper(10, symbols):
        threads.append(
            threading.Thread(target=multiple_downloads, args=(i, data_list, data_lock))
        )
        threads[-1].start()
    for t in threads:
        t.join()
        
    data = pd.concat(data_list, ignore_index=True)
    data = data.astype(types)
    data['timeframe'] = timeframe
    return data
    