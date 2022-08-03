from datetime import timedelta, datetime as dt
import requests as rq

# CONSTANTS
BASE_URL="https://api.gateio.ws/api/v4"
SYMBOLS_EP="/spot/currency_pairs"
MARKET_EP="/spot/candlesticks"


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
        timeframe = '1d'
    elif timeframe == '1hour':
        qty: int = 1
        timeframe = '1h'
    elif timeframe == '4hour':
        qty: int = 4
        timeframe = '4h'
        
    start_at = int((dt.now() - timedelta(hours=qty) * 160).timestamp())
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    params: dict = {'currency_pair': symbol, 'from': str(start_at), 'interval': timeframe}
    response: dict = rq.get(BASE_URL + MARKET_EP, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("APICallError: {}".format(response.status_code))