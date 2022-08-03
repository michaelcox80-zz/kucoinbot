"""Implementation of different precursors of technical indicators

This scripts contains a variety of different technical analysis
functions used in the implementation of other technical indicators.

This file can be imported as a module and contains the following functions:

    * sma - Simple Moving Average
    * is_support - Support Detection
    * is_resistance - Resistance Detection
    * is_far_from_level - Decide if a support or resistance is far from the price
    
"""

import pandas as pd


def sma(data, period) -> pd.Series:
    """
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
    """

    return data.rolling(window=period).mean()


def is_support(data: pd.Series, i: int) -> bool:
    """
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
    """
    
    cond1 = data.iloc[i] < data.iloc[i-1]
    cond2 = data.iloc[i] < data.iloc[i+1]
    cond3 = data.iloc[i+1] < data.iloc[i+2]
    cond4 = data.iloc[i-1] < data.iloc[i-2]
    
    return (cond1 and cond2 and cond3 and cond4)


def is_resistance(data: pd.Series, i: int) -> bool:
    """
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
    """
    
    cond1 = data.iloc[i] > data.iloc[i-1]
    cond2 = data.iloc[i] > data.iloc[i+1]
    cond3 = data.iloc[i+1] > data.iloc[i+2]
    cond4 = data.iloc[i-1] > data.iloc[i-2]
    
    return (cond1 and cond2 and cond3 and cond4)


def is_far_from_level(value: float, levels: list, data_high: pd.Series, data_low: pd.Series) -> bool:
    """
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
    """
    
    average = (data_high - data_low).mean()
    
    return len([abs(value - l) < average for l in levels]) == 0
