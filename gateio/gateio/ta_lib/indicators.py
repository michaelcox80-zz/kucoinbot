"""Implementation of different technical analysis indicators

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
    
"""

import pandas as pd
import numpy as np
from ta_lib.helpers import *


def tenkan_sen(data: pd.DataFrame, period: int =20) -> pd.Series:
    """
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
    """
    
    period_high = data['high'].rolling(window=period).max()
    period_low = data['low'].rolling(window=period).min()
    tenkan_sen = (period_high + period_low) / 2
    return tenkan_sen


def kinjun_sen(data: pd.DataFrame, period: int =60) -> pd.Series:
    """
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
    """
    
    period_high = data['high'].rolling(window=period).max()
    period_low = data['low'].rolling(window=period).min()
    kinjun_sen = (period_high + period_low) / 2
    return kinjun_sen


def senkou_span_a(tenkan_sen: pd.Series, kinjun_sen: pd.Series, period: int =30) -> pd.Series:
    """
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
    """
    
    return ((tenkan_sen + kinjun_sen) / 2).shift(period)


def senkou_span_b(data: pd.DataFrame, period: int =120) -> pd.Series:
    """
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
    """
    
    period_high = data['high'].rolling(window=period).max()
    period_low = data['low'].rolling(window=period).min()
    senkou_span_b = (period_high + period_low) / 2
    
    return senkou_span_b.shift(30)


def chikou_span(data: pd.Series, period: int =30) -> pd.Series:
    """
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
    """
    
    return data.shift(-30)


def bollinger_bands(data: pd.DataFrame, period: int =20, dev: int =2) -> pd.Series:
    """
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
    """
    
    sma_period = pd.Series()
    sma_period: pd.Series = sma(data['close'], period)
    std_dev: pd.Series = data['close'].rolling(window=period).std()
    
    return {'bb_middle': sma_period, 'bb_std': std_dev}


def stoch_rsi(data: pd.DataFrame, period: int =14, k_period: int =3, d_period: int =3) -> pd.Series:
    """
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
    """
    
    # Calculate RSI
    close = data['close']
    delta = close.diff().dropna()
    ups = delta * 0
    downs = ups.copy()
    ups[delta > 0] = delta[delta > 0]
    downs[delta < 0] = -delta[delta < 0]

    ups[ups.index[period - 1]] = np.mean(ups[:period])
    ups = ups.drop(ups.index[:(period - 1)])
    downs[downs.index[period - 1]] = np.mean(downs[:period])
    downs = downs.drop(downs.index[:(period - 1)])
    
    rs = ups.ewm(com=period - 1,
                 min_periods=0,
                 adjust=False,
                 ignore_na=False).mean() / \
         downs.ewm(com=period - 1,
                 min_periods=0,
                 adjust=False,
                 ignore_na=False).mean()
    rsi = 100 - 100 / (1 + rs)

    # Calculate stoch_rsi
    stoch_rsi = pd.to_numeric((rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min()), errors='coerce')
    stoch_rsi_k = pd.to_numeric(stoch_rsi.rolling(window=k_period).mean() * 100, errors='coerce')
    stoch_rsi_d = pd.to_numeric(stoch_rsi_k.rolling(window=d_period).mean() * 100, errors='coerce')

    return {'stoch_rsi': stoch_rsi, 'stoch_rsi_k': stoch_rsi_k, 'stoch_rsi_d': stoch_rsi_d}


def fractal_detection(data: pd.DataFrame) -> list:
    """
    Search for support and resistance levels using fractal analysis

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data the user wants to search levels on

    Returns
    -------
    list of tuples (int, float)
        List of tuples containing the index and value of the support and resistance levels
    """
    levels = []
    data_low = data.low
    data_high = data.high
    
    for i in range(2, data_high.shape[0]-2):
        if is_support(data_low, i):
            l = data_low.iloc[i]
            if is_far_from_level(l, levels, data_high, data_low):
                levels.append((i, l))
                
        elif is_resistance(data_high, i):
            l = data_high.iloc[i]
            if is_far_from_level(l, levels, data_high, data_low):
                levels.append((i, l))
                
    return levels


def window_detection(data: pd.DataFrame) -> list:
    """
    Search for support and resistance levels using window shifting

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data the user wants to search levels on

    Returns
    -------
    list of tuples (int, float)
        List of tuples containing the index and value of the support and resistance levels
    """
    
    levels = []
    max_list = []
    min_list = []
    data_high = data.high
    data_low = data.low
    
    for i in range(5, len(data_high)-5):
        high_range = data_high.iloc[i-5:i+4]
        current_max = high_range.max()
        if current_max not in max_list:
            max_list = []
        max_list.append(current_max)
        if len(max_list) == 5 and is_far_from_level(current_max, levels, data_high, data_low):
            levels.append((high_range.idxmax(), current_max))

        low_range = data_low.iloc[i-5:i+5]
        current_min = low_range.min()
        if current_min not in min_list:
            min_list = []
        min_list.append(current_min)
        if len(min_list) == 5 and is_far_from_level(current_min, levels, data_high, data_low):
            levels.append((low_range.idxmin(), current_min))
            
    return levels
