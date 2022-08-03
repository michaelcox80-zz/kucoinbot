"""Implementation of different trading strategies based on ta

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
    
"""

import pandas as pd
import sys
import os
sys.path.append(os.path.abspath('../ta_lib'))
from ta_lib import indicators, helpers


def ichimoku_breakout(df: pd.DataFrame, breakouts: list, timeframe: str, exchange: str) -> list:
    """
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
    """
    
    data = df.copy()    # copy dataframe to avoid changing original dataframe in the caller
    data = pd.concat([data, pd.DataFrame(indicators.tenkan_sen(data), columns=['tenkan_sen'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.kinjun_sen(data), columns=['kinjun_sen'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.senkou_span_a(data.tenkan_sen, data.kinjun_sen), columns=['senkou_span_a'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.senkou_span_b(data), columns=['senkou_span_b'])], axis=1)

    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            tenkan_sen = symbol_data.iloc[-1].tenkan_sen
            kinjun_sen = symbol_data.iloc[-1].kinjun_sen
            tenkan_sen_2 = symbol_data.iloc[-2].tenkan_sen
            kinjun_sen_2 = symbol_data.iloc[-2].kinjun_sen
            chikou_span = symbol_data.iloc[-30].close
            chikou_span_2 = symbol_data.iloc[-31].close
            senkou_span_a = symbol_data.iloc[-1].senkou_span_a
            senkou_span_b = symbol_data.iloc[-1].senkou_span_b
            senkou_span_a_2 = symbol_data.iloc[-2].senkou_span_a
            senkou_span_b_2 = symbol_data.iloc[-2].senkou_span_b

            if close > senkou_span_a > senkou_span_b and \
                    tenkan_sen > kinjun_sen and \
                    close > chikou_span:
                        
                if tenkan_sen_2 <= kinjun_sen_2:
                    breakouts.append({'symbol': symbol, 'type': 'ICH', 'timeframe': timeframe, 'exc': exchange})
                elif close_2 <= max(senkou_span_a_2, senkou_span_b_2):
                    breakouts.append({'symbol': symbol, 'type': 'ICH', 'timeframe': timeframe, 'exc': exchange})
                elif chikou_span_2 >= close_2:
                    breakouts.append({'symbol': symbol, 'type': 'ICH', 'timeframe': timeframe, 'exc': exchange})
                    
    return breakouts


def bb_rsi_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
    """
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
    """

    data = df.copy()    # copy dataframe to avoid changing original dataframe in the caller
    data = pd.concat([data, pd.DataFrame(indicators.bollinger_bands(data))], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.stoch_rsi(data))], axis=1)

    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
        
        if not symbol_data.empty:
            # The number after the '_' is the number of periods when there is
            # more than two of the same data, when there is only two is the data
            # and a _2 for the previous data
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_4 = symbol_data.iloc[-4].close
            close_5 = symbol_data.iloc[-5].close
            open_5 = symbol_data.iloc[-5].open      # Open prices are used to calculate two straight lines
            open_25 = symbol_data.iloc[-25].open    # from a far point and a near point, and check that in
            open_6 = symbol_data.iloc[-6].open      # the near point the slope is greater than the far point
            open_26 = symbol_data.iloc[-26].open    # thus signaling a rising tendency
            stoch_rsi_K = symbol_data.iloc[-4].stoch_rsi_k
            stoch_rsi_K_2 = symbol_data.iloc[-5].stoch_rsi_k
            stoch_rsi_D = symbol_data.iloc[-4].stoch_rsi_d
            stoch_rsi_D_2 = symbol_data.iloc[-5].stoch_rsi_d
            dev = 1.5
            bb_middle = symbol_data.iloc[-4].bb_middle
            bb_middle_2 = symbol_data.iloc[-5].bb_middle
            bb_std = symbol_data.iloc[-4].bb_std
            bb_std_2 = symbol_data.iloc[-5].bb_std
            
            
            if (stoch_rsi_K <= 5 or stoch_rsi_D <= 5) and \
                bb_middle - dev * bb_std >= close_4 and \
                (close - open_25) / 25 < (close - open_5) / 5 and \
                (close - open_5) / 5 > 0:
            
                # 1st Type of Breakout: stoch_rsi previously above 5
                if stoch_rsi_K_2 > 5 and stoch_rsi_D_2 > 5:
                    breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                # 2nd Type of Breakout: Price previously below the range for BB
                elif bb_middle_2 - dev * bb_std_2 < close_5:
                    breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                # 3rd Type of Breakout: Slope changing on the last five periods
                elif (close_2 - open_26) / 25 >= (close_2 - open_6) / 5 or \
                    (close_2 - open_6) / 5 <= 0:
                    breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                
    return breakouts


def ma_vol_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
    """
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
    """

    data = df.copy()    # copy dataframe to avoid changing original dataframe in the caller
    data = pd.concat([data, pd.DataFrame(helpers.sma(data.close, 25), columns=['sma_25'])], axis=1)
    #data = pd.concat([data, pd.DataFrame(helpers.sma(data.volume, 25), columns=['smav_25'])], axis=1)

    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            volume = symbol_data.iloc[-1].volume
            volume_2 = symbol_data.iloc[-2].volume
            sma = symbol_data.iloc[-1].sma_25
            sma_2 = symbol_data.iloc[-2].sma_25
            smav = symbol_data.iloc[-1].smav_25
            smav_2 = symbol_data.iloc[-2].smav_25
            
            if close > sma #and \
               #volume > smav:
            
                #if volume_2 < smav_2:
                #    breakouts.append({'symbol': symbol, 'type': 'MA_25', 'timeframe': '4h', 'exc': exchange})
                if close_2 < sma_2:
                    breakouts.append({'symbol': symbol, 'type': 'MA_25', 'timeframe': '1h', 'exc': exchange})
    
    return breakouts


def sr_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
    """
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
    """
    
    def has_breakout(levels, previous, last):
        for _, level in levels:
            cond1 = previous.open < level
            cond2 = last.open > level and last.low > level
        return cond1 and cond2

    data = df.copy()

    method_01 = []
    method_02 = []
    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
        
        if not symbol_data.empty:
            levels_01 = indicators.fractal_detection(symbol_data)
            if (has_breakout(levels_01[-5:], symbol_data.iloc[-2], symbol_data.iloc[-1])):
                method_01.append(symbol)
                
            levels_02 = indicators.window_detection(symbol_data)
            if (has_breakout(levels_02[-5:], symbol_data.iloc[-2], symbol_data.iloc[-1])):
                method_02.append(symbol)
                
    signals = list(dict.fromkeys(method_01 + method_02))
    
    for symbol in signals:
        breakouts.append({'symbol': symbol, 'type': 'S&R', 'timeframe': '4h', 'exc': exchange})
    
    return breakouts