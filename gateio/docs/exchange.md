# Table of Contents

* [exchange](#exchange)
  * [get\_all\_symbols](#exchange.get_all_symbols)
  * [get\_all\_candles](#exchange.get_all_candles)
* [helpers](#helpers)
  * [get\_candles\_for\_symbol](#helpers.get_candles_for_symbol)
* [\_\_init\_\_](#__init__)

<a id="exchange"></a>

# exchange

Implementation of functions to retrieve data from Kucoin API

This script and its child (helpers.py) contains three functions to retrieve data from the Kucoin API.

This file can be imported as a module and contains the following functions:

    * get_all_symbols - Creates and returns the list of tradable USDT pairs on Kucoin spot
    * get_candles_for_symbol - Gets all candles for the given symbol and timeframe, putting them in a df
    * get_all_candles - Gets all candles for the given symbols and timeframe, putting them in a df

<a id="exchange.get_all_symbols"></a>

#### get\_all\_symbols

```python
def get_all_symbols() -> list
```

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

<a id="exchange.get_all_candles"></a>

#### get\_all\_candles

```python
def get_all_candles(symbols: list, timeframe: str) -> pd.DataFrame
```

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

<a id="helpers"></a>

# helpers

<a id="helpers.get_candles_for_symbol"></a>

#### get\_candles\_for\_symbol

```python
def get_candles_for_symbol(symbol: str, timeframe: str) -> list
```

Downloads a block of 150 candles for the given symbol and timeframe

Parameters
----------
symbol : str
    The symbol to download the candles for
timeframe : str
    The timeframe to download the candles for

Raises
------
APICallError - If the API call fails

Returns
-------
    list : A list of candles in dic format

<a id="__init__"></a>

# \_\_init\_\_

