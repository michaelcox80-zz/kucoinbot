from datetime import timedelta, datetime as dt
import requests as rq

BASEURL="https://api.kucoin.com"
KEY="618558c5bc85c200065b6e50"

SYMBOLS_EP="/api/v1/symbols"
MARKET_EP="/api/v1/market/candles"


def get_candles_for_symbol(symbol: str, timeframe: str) -> list:
    """
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
    """
    
    if timeframe == '1day':
        qty: int = 24
    elif timeframe == '1hour':
        qty: int = 1
    elif timeframe == '4hour':
        qty: int = 4
        
    start_at = int((dt.now() - timedelta(hours=qty) * 160).timestamp())
    params: dict = {'symbol': symbol, 'startAt': start_at, 'type': timeframe}
    response: dict = rq.get(BASEURL + MARKET_EP, params=params)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception("APICallError: {}".format(response.status_code))