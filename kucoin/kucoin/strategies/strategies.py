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

import math
import pandas as pd
import sys
import os
import collections
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
                    print(symbol, 'BB_RSI')
                    #breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                # 2nd Type of Breakout: Price previously below the range for BB
                elif bb_middle_2 - dev * bb_std_2 < close_5:
                    print(symbol, 'BB_RSI')
                    #breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                # 3rd Type of Breakout: Slope changing on the last five periods
                elif (close_2 - open_26) / 25 >= (close_2 - open_6) / 5 or \
                    (close_2 - open_6) / 5 <= 0:
                    print(symbol, 'BB_RSI')
                    #breakouts.append({'symbol': symbol, 'type': 'BB_RSI', 'timeframe': '4h', 'exc': exchange})
                
    return breakouts


def rounding_breakout(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
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
    #data = pd.concat([data, pd.DataFrame(helpers.sma(data.close, 25), columns=['sma_25'])], axis=1)
    #data = pd.concat([data, pd.DataFrame(helpers.sma(data.low, 25), columns=['low'])], axis=1)
    #data['pandas_SMA_25'] = df.iloc[:,1].rolling(window=25).mean()
    #data = pd.concat([data, pd.DataFrame(indicators.tenkan_sen(data), columns=['tenkan_sen'])], axis=1)
    #data = pd.concat([data, pd.DataFrame(indicators.kinjun_sen(data), columns=['kinjun_sen'])], axis=1)
    #print(data)

    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
        
        if not symbol_data.empty:
            (df.low).apply(lambda x: float(x))
            (df.volume).apply(lambda x: float(x))
            #(df.low).apply(lambda x: float(x))
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_3 = symbol_data.iloc[-3].close
            close_4 = symbol_data.iloc[-4].close
            low = symbol_data.iloc[-1].low
            low_2 = symbol_data.iloc[-2].low
            low_3 = symbol_data.iloc[-3].low
            low_4 = symbol_data.iloc[-4].low
            low_5 = symbol_data.iloc[-5].low
            low_10 = symbol_data.iloc[-10].low
            low_20 = symbol_data.iloc[-20].low
            vol = symbol_data.iloc[-1].volume
            vol_2 = symbol_data.iloc[-2].volume
            vol_3 = symbol_data.iloc[-3].volume
            vol_4 = symbol_data.iloc[-4].volume
            high = symbol_data.iloc[-1].high
            
            #(df.low).apply(lambda x: float(x))

            if close >= close_2 and close_2 >= close_3 and close_3 >= close_4 and low_20 > low and ((high - low_4) / low_4) * 100.0 < 8.0:    
                #print(symbol, low, low_2, low_3, low_4)
                a = low
            #try:
                #print((abs(low - low_4) / low_4) * 100.0, symbol)
                if abs((low - low_4) / low_4) * 100.0 < 7.0:
                    #if abs(vol_2 - vol_3) / vol_2 * 100.0 > -30.0 and abs(vol_3 - vol_4) / vol_4 * 100.0 > -30.0:
                    print(symbol, "rounding...", high, low_4, ((high - low_4) / low_4) * 100.0)
                    #breakouts.append({'symbol': symbol, 'type': 'TEST:::Rounding price1 DAY::::TEST', 'timeframe': '1D', 'exc': exchange})
            #except ZeroDivisionError:
                #return float('inf')
             #       print(symbol)
            #print(symbol, close, sma)
            #if low >= low_2: 
            #    print(symbol)
             #   print(symbol, smav, smav_2)
             #   print(symbol, close_2, close_2)
                #breakouts.append({'symbol': symbol, 'type': 'MA_25', 'timeframe': '1h', 'exc': exchange})
    
    return breakouts



def ma_inch(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
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
    data['pandas_SMA_25'] = df.iloc[:,1].rolling(window=25).mean()
    data = pd.concat([data, pd.DataFrame(indicators.tenkan_sen(data), columns=['tenkan_sen'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.kinjun_sen(data), columns=['kinjun_sen'])], axis=1)
    

    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
     
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_3 = symbol_data.iloc[-3].close
            close_4 = symbol_data.iloc[-4].close
            close_5 = symbol_data.iloc[-5].close
            close_6 = symbol_data.iloc[-6].close
            close_7 = symbol_data.iloc[-7].close
            close_8 = symbol_data.iloc[-8].close
            close_9 = symbol_data.iloc[-9].close
            close_10 = symbol_data.iloc[-10].close
            close_11 = symbol_data.iloc[-11].close
            close_12 = symbol_data.iloc[-12].close
            close_13 = symbol_data.iloc[-13].close
            close_14 = symbol_data.iloc[-14].close
            close_15 = symbol_data.iloc[-15].close
            close_16 = symbol_data.iloc[-16].close
            close_17 = symbol_data.iloc[-17].close
            close_18 = symbol_data.iloc[-18].close
            close_25 = symbol_data.iloc[-25].close
            sma = symbol_data.iloc[-1].pandas_SMA_25
            sma_2 = symbol_data.iloc[-2].sma_25
            smav = symbol_data.iloc[-1].volume
            smav_2 = symbol_data.iloc[-2].volume
            smav_3 = symbol_data.iloc[-3].volume
            smav_4 = symbol_data.iloc[-5].volume
            tenkan_sen = symbol_data.iloc[-1].tenkan_sen
            kinjun_sen = symbol_data.iloc[-1].kinjun_sen
            tenkan_sen_2 = symbol_data.iloc[-2].tenkan_sen
            kinjun_sen_2 = symbol_data.iloc[-2].kinjun_sen
            tenkan_sen_20 = symbol_data.iloc[-20].tenkan_sen
            kinjun_sen_20 = symbol_data.iloc[-20].kinjun_sen
            low = symbol_data.iloc[-1].low
            low_2 = symbol_data.iloc[-2].low
            low_3 = symbol_data.iloc[-3].low
            low_4 = symbol_data.iloc[-4].low
            low_5 = symbol_data.iloc[-5].low
            low_35 = symbol_data.iloc[-35].low
            low_60 = symbol_data.iloc[-60].low
            high = symbol_data.iloc[-1].high

            
            #print(symbol, close, sma)
            if low >= low_2 and close > sma and close_2 > sma and tenkan_sen > kinjun_sen:
            #if close >= close_2 and close > sma and close_2 > sma and close_3 > sma and close_4 > sma and close_10 <= close_25 and tenkan_sen > kinjun_sen and ((close - close_10) / close_10) * 100.0 < 3:
                #if ((close - close_2) / close_2) * 100.0 < 3 and ((close_2 - close_3) / close_3) * 100.0 < 3: #and ((close_3 - close_4) / close_4) * 100.0 < 3:
                    # and close_3 < sma: # and tenkan_sen > kinjun_sen and smav > smav_3: 
                    #if (low - low_4) / low_4) * 100.0 
                    #print(symbol, close, close_2, close_3, sma) wasl  low + low_35
                print(symbol, "ma inch", ((close - close_10) / close_10) * 100.0, ((close - close_10) / close_10))
                    #breakouts.append({'symbol': symbol, 'type': 'MA_25/BASE/CONV', 'timeframe': '1h', 'exc': exchange})
    
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
    #cond1 =''
    #cond2 =''
    data = df.copy()

    cond1 =''
    cond2 =''

    def has_breakout(levels, previous, last):
        for _, level in levels:
            nonlocal cond1 
            cond1 = previous.open < level
            nonlocal cond2 
            cond2 = last.open > level and last.low > level
        return cond1 and cond2

    

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
        print("breakouts", symbol)
        #breakouts.append({'symbol': symbol, 'type': 'S&R', 'timeframe': '4h', 'exc': exchange})
    
    return breakouts



def double(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
    
    data = df.copy()    # copy dataframe to avoid changing original dataframe in the caller
    data = pd.concat([data, pd.DataFrame(helpers.sma(data.close, 25), columns=['sma_25'])], axis=1)
    #data = pd.concat([data, pd.DataFrame(helpers.sma(data.volume, 25), columns=['smav_25'])], axis=1)
    data['pandas_SMA_25'] = df.iloc[:,1].rolling(window=25).mean()
    data = pd.concat([data, pd.DataFrame(indicators.tenkan_sen(data), columns=['tenkan_sen'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.kinjun_sen(data), columns=['kinjun_sen'])], axis=1)
    

    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
     
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_3 = symbol_data.iloc[-3].close
            sma = symbol_data.iloc[-1].pandas_SMA_25
            sma_2 = symbol_data.iloc[-2].sma_25
            smav = symbol_data.iloc[-1].volume
            smav_2 = symbol_data.iloc[-2].volume
            smav_3 = symbol_data.iloc[-3].volume
            smav_4 = symbol_data.iloc[-5].volume
            tenkan_sen = symbol_data.iloc[-1].tenkan_sen
            kinjun_sen = symbol_data.iloc[-1].kinjun_sen
            tenkan_sen_2 = symbol_data.iloc[-2].tenkan_sen
            kinjun_sen_2 = symbol_data.iloc[-2].kinjun_sen
            tenkan_sen_20 = symbol_data.iloc[-20].tenkan_sen
            kinjun_sen_20 = symbol_data.iloc[-20].kinjun_sen
            low = symbol_data.iloc[-1].low
            low_2 = symbol_data.iloc[-2].low
            low_3 = symbol_data.iloc[-3].low
            low_4 = symbol_data.iloc[-4].low
            low_5 = symbol_data.iloc[-5].low
            low_6 = symbol_data.iloc[-6].low
            low_7 = symbol_data.iloc[-7].low
            low_8  = symbol_data.iloc[-8].low
            low_9 = symbol_data.iloc[-9].low
            low_10 = symbol_data.iloc[-10].low
            low_11 = symbol_data.iloc[-11].low
            low_12 = symbol_data.iloc[-12].low
            low_13 = symbol_data.iloc[-13].low
            low_14 = symbol_data.iloc[-14].low
            low_15 = symbol_data.iloc[-15].low
            low_16 = symbol_data.iloc[-16].low
            low_17 = symbol_data.iloc[-17].low
            low_18 = symbol_data.iloc[-18].low
            #high = symbol_data.iloc[-1].high

            lows =[low, low_2, low_3, low_4, low_5, low_6, low_7, low_8,low_9, low_10,low_11, low_12, low_13, low_14, low_15, low_16, low_17, low_18]   
            bottom_low = min(lows)
            seen = set()
            duplicated = [t for t in lows if t in seen or seen.add(t)]
            bottom = min(seen)

            #for elem in lows:
            #    if lows.count(elem) > 1:
            #        print(symbol, bottom_low)
            #    return False

            #if duplicated == bottom or duplicated == low_2:
            #    print(symbol, duplicated, bottom_low)



            #if low in seen:
            #if low == bottom or low == bottom:
            #if bottom_low == bottom:
            #    if low == bottom_low or low == bottom: 
            #print ("double bottoms", symbol, bottom, bottom_low,low, low_2, low_3, low_4, low_5, low_6, low_7, low_8,low_9, low_10,low_11, low_12, low_13, low_14, low_15, low_16, low_17, low_18)
            
            #print(symbol, close, sma)
            #if low >= low_2 and close > sma and close_2 > sma and ((low - low_35) / low_35) * 100.0 < 2 and tenkan_sen > kinjun_sen:# and close_3 < sma: # and tenkan_sen > kinjun_sen and smav > smav_3: 
                #if (low - low_4) / low_4) * 100.0 
                #print(symbol, close, close_2, close_3, sma)
            #    print(symbol, "ma inch", ((low - low_35) / low_35) * 100.0)
                #breakouts.append({'symbol': symbol, 'type': 'MA_25/BASE/CONV', 'timeframe': '1h', 'exc': exchange})
    
    return breakouts

def bottom(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
    
    data = df.copy()    # copy dataframe to avoid changing original dataframe in the caller
    data = pd.concat([data, pd.DataFrame(helpers.sma(data.close, 25), columns=['sma_25'])], axis=1)
    #data = pd.concat([data, pd.DataFrame(helpers.sma(data.volume, 25), columns=['smav_25'])], axis=1)
    
    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
     
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_3 = symbol_data.iloc[-3].close
            close_4 = symbol_data.iloc[-4].close
            close_5 = symbol_data.iloc[-5].close
            close_6 = symbol_data.iloc[-6].close
            close_7 = symbol_data.iloc[-7].close
            close_8 = symbol_data.iloc[-8].close
            close_9 = symbol_data.iloc[-9].close
            low = symbol_data.iloc[-1].low
            low_2 = symbol_data.iloc[-2].low
            low_3 = symbol_data.iloc[-3].low
            low_4 = symbol_data.iloc[-4].low
            low_5 = symbol_data.iloc[-5].low
            low_6 = symbol_data.iloc[-6].low
            low_7 = symbol_data.iloc[-7].low
            low_8  = symbol_data.iloc[-8].low
            low_9 = symbol_data.iloc[-9].low
            low_10 = symbol_data.iloc[-10].low
            low_11 = symbol_data.iloc[-11].low
            low_12 = symbol_data.iloc[-12].low
            low_13 = symbol_data.iloc[-13].low
            low_14 = symbol_data.iloc[-14].low
            low_15 = symbol_data.iloc[-15].low
            low_16 = symbol_data.iloc[-16].low
            low_17 = symbol_data.iloc[-17].low
            low_18 = symbol_data.iloc[-18].low
            #high = symbol_data.iloc[-1].high

            #lows =[low, low_2, low_3, low_4, low_5, low_6, low_7, low_8,low_9, low_10,low_11, low_12, low_13, low_14, low_15, low_16, low_17, low_18]   
            #bottom_low = min(lows)
            #seen = set()
            #duplicated = [t for t in lows if t in seen or seen.add(t)]
            #bottom = min(seen)
            if low >= low_2 and low_2 >= low_3 and close_4 <= close_5 and close_5 <= close_6: #and low_4 <= low_5 and low_5 <= low_6:
                print(symbol, " daily bottom")
            #for elem in lows:
            #    if lows.count(elem) > 1:
            #        print(symbol, bottom_low)
            #    return False

            #if duplicated == bottom or duplicated == low_2:
            #    print(symbol, duplicated, bottom_low)



            #if low in seen:
            #if low == bottom or low == bottom:
            #if bottom_low == bottom:
            #    if low == bottom_low or low == bottom: 
            #print ("double bottoms", symbol, bottom, bottom_low,low, low_2, low_3, low_4, low_5, low_6, low_7, low_8,low_9, low_10,low_11, low_12, low_13, low_14, low_15, low_16, low_17, low_18)
            
            #print(symbol, close, sma)
            #if low >= low_2 and close > sma and close_2 > sma and ((low - low_35) / low_35) * 100.0 < 2 and tenkan_sen > kinjun_sen:# and close_3 < sma: # and tenkan_sen > kinjun_sen and smav > smav_3: 
                #if (low - low_4) / low_4) * 100.0 
                #print(symbol, close, close_2, close_3, sma)
            #    print(symbol, "ma inch", ((low - low_35) / low_35) * 100.0)
                #breakouts.append({'symbol': symbol, 'type': 'MA_25/BASE/CONV', 'timeframe': '1h', 'exc': exchange})
    
    return breakouts


def ma_pumpers(df: pd.DataFrame, breakouts: list, exchange: str) -> list:
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
    data['pandas_SMA_25'] = df.iloc[:,1].rolling(window=25).mean()
    data = pd.concat([data, pd.DataFrame(indicators.tenkan_sen(data), columns=['tenkan_sen'])], axis=1)
    data = pd.concat([data, pd.DataFrame(indicators.kinjun_sen(data), columns=['kinjun_sen'])], axis=1)
    

    
    for symbol in data.symbol.unique():
        symbol_data = data.loc[data['symbol'] == symbol]
     
        
        if not symbol_data.empty:
            close = symbol_data.iloc[-1].close
            close_2 = symbol_data.iloc[-2].close
            close_3 = symbol_data.iloc[-3].close
            close_4 = symbol_data.iloc[-4].close
            close_5 = symbol_data.iloc[-5].close
            close_6 = symbol_data.iloc[-6].close
            close_7 = symbol_data.iloc[-7].close
            close_8 = symbol_data.iloc[-8].close
            close_9 = symbol_data.iloc[-9].close
            close_10 = symbol_data.iloc[-10].close
            close_11 = symbol_data.iloc[-11].close
            close_12 = symbol_data.iloc[-12].close
            close_13 = symbol_data.iloc[-13].close
            close_14 = symbol_data.iloc[-14].close
            close_15 = symbol_data.iloc[-15].close
            close_16 = symbol_data.iloc[-16].close
            close_17 = symbol_data.iloc[-17].close
            close_18 = symbol_data.iloc[-18].close
            close_25 = symbol_data.iloc[-25].close
            sma = symbol_data.iloc[-1].pandas_SMA_25
            sma_2 = symbol_data.iloc[-2].sma_25
            smav = symbol_data.iloc[-1].volume
            smav_2 = symbol_data.iloc[-2].volume
            smav_3 = symbol_data.iloc[-3].volume
            smav_4 = symbol_data.iloc[-5].volume
            tenkan_sen = symbol_data.iloc[-1].tenkan_sen
            kinjun_sen = symbol_data.iloc[-1].kinjun_sen
            tenkan_sen_2 = symbol_data.iloc[-2].tenkan_sen
            kinjun_sen_2 = symbol_data.iloc[-2].kinjun_sen
            tenkan_sen_20 = symbol_data.iloc[-20].tenkan_sen
            kinjun_sen_20 = symbol_data.iloc[-20].kinjun_sen
            low = symbol_data.iloc[-1].low
            low_2 = symbol_data.iloc[-2].low
            low_3 = symbol_data.iloc[-3].low
            low_4 = symbol_data.iloc[-4].low
            low_5 = symbol_data.iloc[-5].low
            low_35 = symbol_data.iloc[-35].low
            low_60 = symbol_data.iloc[-60].low
            high = symbol_data.iloc[-1].high

            
            #print(symbol, close, sma)
            if close >= close_2 and close_2 > close_3 and close > sma and tenkan_sen > kinjun_sen:
            #if close >= close_2 and close > sma and close_2 > sma and close_3 > sma and close_4 > sma and close_10 <= close_25 and tenkan_sen > kinjun_sen and ((close - close_10) / close_10) * 100.0 < 3:
                #if ((close - close_2) / close_2) * 100.0 < 3 and ((close_2 - close_3) / close_3) * 100.0 < 3: #and ((close_3 - close_4) / close_4) * 100.0 < 3:
                    # and close_3 < sma: # and tenkan_sen > kinjun_sen and smav > smav_3: 
                    #if (low - low_4) / low_4) * 100.0 
                    #print(symbol, close, close_2, close_3, sma) wasl  low + low_35
                print(symbol, "pumper", ((close - close_10) / close_10) * 100.0, ((close - close_10) / close_10))
                    #breakouts.append({'symbol': symbol, 'type': 'MA_25/BASE/CONV', 'timeframe': '1h', 'exc': exchange})
    
    return breakouts
