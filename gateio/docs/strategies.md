# Table of Contents

* [strategies](#strategies)
  * [ichimoku\_breakout](#strategies.ichimoku_breakout)
  * [bb\_rsi\_breakout](#strategies.bb_rsi_breakout)
  * [ma\_vol\_breakout](#strategies.ma_vol_breakout)
  * [sr\_breakout](#strategies.sr_breakout)
* [\_\_init\_\_](#__init__)

<a id="strategies"></a>

# strategies

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

<a id="strategies.ichimoku_breakout"></a>

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

<a id="strategies.bb_rsi_breakout"></a>

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

<a id="strategies.ma_vol_breakout"></a>

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

<a id="strategies.sr_breakout"></a>

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

<a id="__init__"></a>

# \_\_init\_\_

