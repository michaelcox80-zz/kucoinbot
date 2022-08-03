# Table of Contents

* [helpers](#helpers)
  * [hour\_rounder](#helpers.hour_rounder)
* [runner](#runner)
  * [find\_breakouts](#runner.find_breakouts)
  * [main](#runner.main)
* [\_\_init\_\_](#__init__)
* [exchange](#exchange)
* [exchange.exchange](#exchange.exchange)
  * [get\_all\_symbols](#exchange.exchange.get_all_symbols)
  * [get\_all\_candles](#exchange.exchange.get_all_candles)
* [exchange.helpers](#exchange.helpers)
  * [get\_candles\_for\_symbol](#exchange.helpers.get_candles_for_symbol)
* [strategies](#strategies)
* [strategies.strategies](#strategies.strategies)
  * [ichimoku\_breakout](#strategies.strategies.ichimoku_breakout)
  * [bb\_rsi\_breakout](#strategies.strategies.bb_rsi_breakout)
  * [ma\_vol\_breakout](#strategies.strategies.ma_vol_breakout)
  * [sr\_breakout](#strategies.strategies.sr_breakout)
* [ta\_lib](#ta_lib)
* [ta\_lib.helpers](#ta_lib.helpers)
  * [sma](#ta_lib.helpers.sma)
  * [is\_support](#ta_lib.helpers.is_support)
  * [is\_resistance](#ta_lib.helpers.is_resistance)
  * [is\_far\_from\_level](#ta_lib.helpers.is_far_from_level)
* [ta\_lib.indicators](#ta_lib.indicators)
  * [tenkan\_sen](#ta_lib.indicators.tenkan_sen)
  * [kinjun\_sen](#ta_lib.indicators.kinjun_sen)
  * [senkou\_span\_a](#ta_lib.indicators.senkou_span_a)
  * [senkou\_span\_b](#ta_lib.indicators.senkou_span_b)
  * [chikou\_span](#ta_lib.indicators.chikou_span)
  * [bollinger\_bands](#ta_lib.indicators.bollinger_bands)
  * [stoch\_rsi](#ta_lib.indicators.stoch_rsi)
  * [fractal\_detection](#ta_lib.indicators.fractal_detection)
  * [window\_detection](#ta_lib.indicators.window_detection)

<a id="helpers"></a>

# helpers

<a id="helpers.hour_rounder"></a>

#### hour\_rounder

```python
def hour_rounder(t)
```

Round the time to the nearest hour

Parameters
----------
t : datetime
    The time to be rounded

Returns
-------
datetime
    The rounded time

<a id="runner"></a>

# runner

<a id="runner.find_breakouts"></a>

#### find\_breakouts

```python
def find_breakouts()
```

Function which composes the whole program to find breakouts

Returns
-------
None

<a id="runner.main"></a>

#### main

```python
def main()
```

Main function of the program which mainly controls
timeflow and execution

Argv : list
    List of arguments passed to the program (false, true, -h, --help)

<a id="__init__"></a>

# \_\_init\_\_

<a id="exchange"></a>

# exchange

<a id="exchange.exchange"></a>

# exchange.exchange

Implementation of functions to retrieve data from Kucoin API

This script and its child (helpers.py) contains three functions to retrieve data from the Kucoin API.

This file can be imported as a module and contains the following functions:

    * get_all_symbols - Creates and returns the list of tradable USDT pairs on Kucoin spot
    * get_candles_for_symbol - Gets all candles for the given symbol and timeframe, putting them in a df
    * get_all_candles - Gets all candles for the given symbols and timeframe, putting them in a df

<a id="exchange.exchange.get_all_symbols"></a>

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

<a id="exchange.exchange.get_all_candles"></a>

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

<a id="exchange.helpers"></a>

# exchange.helpers

<a id="exchange.helpers.get_candles_for_symbol"></a>

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

<a id="strategies"></a>

# strategies

<a id="strategies.strategies"></a>

# strategies.strategies

Implementation of different trading strategies based on ta

This scripts contains a variety of different trading strategies
used to find price breakouts on cryptocurrencies

This file can be imported as a module and contains the following functions:

    * ichimoku_breakout : Calculates the Ichimoku breakout indicator for the 
        given dataframe and returns signals
    * ma_vol_breakout : Calculates the Moving Average and Volume breakout 
        indicator for the given dataframe and returns signals
    * sr_breakout : Calculates support and resistance levels in two different 
        ways and returns signals given out by both methods
    * bollinger_breakout : Calculates the Bollinger breakout indicator for 
        the given dataframe and returns signals

<a id="strategies.strategies.ichimoku_breakout"></a>

#### ichimoku\_breakout

```python
def ichimoku_breakout(df: pd.DataFrame, breakouts: list, timeframe: str,
                      exchange: str) -> list
```

Calculates the Ichimoku breakout indicator for the given dataframe and
returns signals

Parameters
----------
df : pd.DataFrame
    Dataframe with OHLCV data
breakouts : list
    List with breakouts
timeframe : str
    Timeframe of the data being used
exchange : str
    Name of the exchange

Returns
-------
breakouts : list
    List with signals

<a id="strategies.strategies.bb_rsi_breakout"></a>

#### bb\_rsi\_breakout

```python
def bb_rsi_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list
```

Calculates the Bollinger Bands and RSI breakout indicator for the given
dataframe and returns signals

Parameters
----------
df : pd.DataFrame
    Dataframe with OHLCV data
breakouts : list
    List with breakouts

Returns
-------
breakouts : list
    List with signals

<a id="strategies.strategies.ma_vol_breakout"></a>

#### ma\_vol\_breakout

```python
def ma_vol_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list
```

Calculates the Moving Average and Volume breakout indicator for the given
dataframe and returns signals

Parameters
----------
df : pd.DataFrame
    Dataframe with OHLCV data
breakouts : list
    List with breakouts
exchange : str
    Exchange the alerts are on

Returns
-------
breakouts : list
    List with signals

<a id="strategies.strategies.sr_breakout"></a>

#### sr\_breakout

```python
def sr_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list
```

Calculates support and resistance levels in two different ways
and returns signals given out by both methods

Parameters
----------
df : pd.DataFrame
    Dataframe with OHLCV data
breakouts : list
    List with breakouts
exchange : str
    Exchange the alerts are on

Returns
-------
breakouts : list
    List with signals

<a id="ta_lib"></a>

# ta\_lib

<a id="ta_lib.helpers"></a>

# ta\_lib.helpers

Implementation of different precursors of technical indicators

This scripts contains a variety of different technical analysis
functions used in the implementation of other technical indicators.

This file can be imported as a module and contains the following functions:

    * sma - Simple Moving Average
    * is_support - Support Detection
    * is_resistance - Resistance Detection
    * is_far_from_level - Decide if a support or resistance is far from the price

<a id="ta_lib.helpers.sma"></a>

#### sma

```python
def sma(data, period) -> pd.Series
```

Simple Moving Average

Parameters
----------
data : pd.Series
    Data the user wants to calculate the SMA on
period : int
    Number of periods to calculate the SMA on

Returns
-------
pd.Series
    SMA of the data on a given period

<a id="ta_lib.helpers.is_support"></a>

#### is\_support

```python
def is_support(data: pd.Series, i: int) -> bool
```

Support Detection

Parameters
----------
data : pd.Series
    Low column of the data
i : int
    Index of the data

Returns
-------
pd.Series
    If the given price is a support level

<a id="ta_lib.helpers.is_resistance"></a>

#### is\_resistance

```python
def is_resistance(data: pd.Series, i: int) -> bool
```

Resistance Detection

Parameters
----------
data : pd.Series
    High column of the data
i : int
    Index of the data

Returns
-------
pd.Series
    If the given price is a resistance level

<a id="ta_lib.helpers.is_far_from_level"></a>

#### is\_far\_from\_level

```python
def is_far_from_level(value: float, levels: list, data_high: pd.Series,
                      data_low: pd.Series) -> bool
```

Decide if a support or resistance is far from the price

Parameters
----------
value : float
    The current price
levels : list
    The list of support or resistance levels
data_high : pd.Series
    High column of the data
data_low : pd.Series
    Low column of the data

Returns
-------
bool
    True if the support or resistance is far from the levels

<a id="ta_lib.indicators"></a>

# ta\_lib.indicators

Implementation of different technical analysis indicators

This scripts contains a variety of different technical analysis
indicators used in the implementation of different trading strategies.

This file can be imported as a module and contains the following functions:

    * tenkan_sen - Conversion line of the ichimoku strategy
    * kinjun_sen - Base line of the ichimoku strategy
    * senkou_span_a - Leading span A of the ichimoku strategy
    * senkou_span_b - Leading span B of the ichimoku strategy
    * chikou_span - Lagging span of the ichimoku strategy
    * bollinger_bands - Bollinger Bands on a std_dev of 2
    * stoch_rsi - Stochastic RSI (Relative Strength Index)
    * fractal_detection - Detection of S&R using fractals
    * window_detection - Detection of S&R using windows

<a id="ta_lib.indicators.tenkan_sen"></a>

#### tenkan\_sen

```python
def tenkan_sen(data: pd.DataFrame, period: int = 20) -> pd.Series
```

Tenkan-sen (Conversion Line)

Parameters
----------
data_high : pd.Series
    Series of high prices
data_low : pd.Series
    Series of low prices
period : int
    Number of periods to calculate the Tenkan-sen on

Returns
-------
pd.Series
    Tenkan-sen of the data on a given period

<a id="ta_lib.indicators.kinjun_sen"></a>

#### kinjun\_sen

```python
def kinjun_sen(data: pd.DataFrame, period: int = 60) -> pd.Series
```

Kinjun-sen (Base Line)

Parameters
----------
data_high : pd.Series
    Series of high prices
data_low : pd.Series
    Series of low prices
period : int
    Number of periods to calculate the Kinjun-sen on

Returns
-------
pd.Series
    Kinjun-sen of the data on a given period

<a id="ta_lib.indicators.senkou_span_a"></a>

#### senkou\_span\_a

```python
def senkou_span_a(tenkan_sen: pd.Series,
                  kinjun_sen: pd.Series,
                  period: int = 30) -> pd.Series
```

Senkou Span A (Leading Span A)

Parameters
----------
tenkan_sen : pd.Series
    Tenkan-sen of the data the user wants to calculate the Senkou Span A on
kinjun_sen : pd.Series
    Kinjun-sen of the data the user wants to calculate the Senkou Span A on
period : int
    Number of periods to calculate the Senkou Span A on

Returns
-------
pd.Series
    Senkou Span A of the data on a given period

<a id="ta_lib.indicators.senkou_span_b"></a>

#### senkou\_span\_b

```python
def senkou_span_b(data: pd.DataFrame, period: int = 120) -> pd.Series
```

Senkou Span B (Leading Span B)

Parameters
----------
data : pd.DataFrame
    Dataframe containing the data the user wants to calculate the Senkou Span B on
period : int
    Number of periods to calculate the Senkou Span B on

Returns
-------
pd.Series
    Senkou Span B of the data on a given period

<a id="ta_lib.indicators.chikou_span"></a>

#### chikou\_span

```python
def chikou_span(data: pd.Series, period: int = 30) -> pd.Series
```

Chikou Span (Lagging Span)

Parameters
----------
data : pd.Series
    Close price of the data the user wants to calculate the Chikou Span on
period : int
    Number of periods to calculate the Chikou Span on

Returns
-------
pd.Series
    Chikou Span of the data on a given period

<a id="ta_lib.indicators.bollinger_bands"></a>

#### bollinger\_bands

```python
def bollinger_bands(data: pd.DataFrame,
                    period: int = 20,
                    dev: int = 2) -> pd.Series
```

Bollinger Bands

Parameters
----------
data : pd.Series
    Price close of the data the user wants to calculate the Bollinger Bands on
period : int
    Number of periods to calculate the Bollinger Bands on
dev : int
    Standard deviation of the Bollinger Bands

Returns
-------
pd.Series
    Bollinger Upper Band of the data on a given period
pd.Series
    Bollinger Lower Band of the data on a given period

<a id="ta_lib.indicators.stoch_rsi"></a>

#### stoch\_rsi

```python
def stoch_rsi(data: pd.DataFrame,
              period: int = 14,
              k_period: int = 3,
              d_period: int = 3) -> pd.Series
```

Stochastic RSI

Parameters
----------
data : pd.DataFrame
    The data of the stock including the close price
period : int
    Number of periods to calculate the Stochastic RSI on
k_period : int
    Number of periods to calculate the Stochastic RSI K on
d_period : int
    Number of periods to calculate the Stochastic RSI D on

Returns
-------
pd.Series
    Stochastic RSI of the data on a given period
pd.Series
    Stochastic RSI K of the data on a given period
pd.Series
    Stochastic RSI D of the data on a given period

<a id="ta_lib.indicators.fractal_detection"></a>

#### fractal\_detection

```python
def fractal_detection(data: pd.DataFrame) -> list
```

Search for support and resistance levels using fractal analysis

Parameters
----------
data : pd.DataFrame
    Dataframe containing the data the user wants to search levels on

Returns
-------
list of tuples (int, float)
    List of tuples containing the index and value of the support and resistance levels

<a id="ta_lib.indicators.window_detection"></a>

#### window\_detection

```python
def window_detection(data: pd.DataFrame) -> list
```

Search for support and resistance levels using window shifting

Parameters
----------
data : pd.DataFrame
    Dataframe containing the data the user wants to search levels on

Returns
-------
list of tuples (int, float)
    List of tuples containing the index and value of the support and resistance levels

