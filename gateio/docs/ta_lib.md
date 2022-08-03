# Table of Contents

* [helpers](#helpers)
  * [sma](#helpers.sma)
  * [is\_support](#helpers.is_support)
  * [is\_resistance](#helpers.is_resistance)
  * [is\_far\_from\_level](#helpers.is_far_from_level)
* [indicators](#indicators)
  * [tenkan\_sen](#indicators.tenkan_sen)
  * [kinjun\_sen](#indicators.kinjun_sen)
  * [senkou\_span\_a](#indicators.senkou_span_a)
  * [senkou\_span\_b](#indicators.senkou_span_b)
  * [chikou\_span](#indicators.chikou_span)
  * [bollinger\_bands](#indicators.bollinger_bands)
  * [stoch\_rsi](#indicators.stoch_rsi)
  * [fractal\_detection](#indicators.fractal_detection)
  * [window\_detection](#indicators.window_detection)
* [\_\_init\_\_](#__init__)

<a id="helpers"></a>

# helpers

Implementation of different precursors of technical indicators

This scripts contains a variety of different technical analysis
functions used in the implementation of other technical indicators.

This file can be imported as a module and contains the following functions:

    * sma - Simple Moving Average
    * is_support - Support Detection
    * is_resistance - Resistance Detection
    * is_far_from_level - Decide if a support or resistance is far from the price

<a id="helpers.sma"></a>

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

<a id="helpers.is_support"></a>

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

<a id="helpers.is_resistance"></a>

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

<a id="helpers.is_far_from_level"></a>

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

<a id="indicators"></a>

# indicators

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

<a id="indicators.tenkan_sen"></a>

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

<a id="indicators.kinjun_sen"></a>

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

<a id="indicators.senkou_span_a"></a>

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

<a id="indicators.senkou_span_b"></a>

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

<a id="indicators.chikou_span"></a>

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

<a id="indicators.bollinger_bands"></a>

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

<a id="indicators.stoch_rsi"></a>

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

<a id="indicators.fractal_detection"></a>

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

<a id="indicators.window_detection"></a>

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

<a id="__init__"></a>

# \_\_init\_\_

