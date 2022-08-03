from exchange.exchange import *
from strategies.strategies import *
from helpers import *
from telegram_send import send
import schedule
from datetime import datetime as dt
import time
import pandas as pd

def find_breakouts():
    """
    Function which composes the whole program to find breakouts
    
    Returns
    -------
    None
    """
    
    exchange = 'KUCOIN'
    breakouts = []
    
    symbols = get_all_symbols()

    data_4h = get_all_candles(symbols, '4hour')
    data_1h = get_all_candles(symbols, '1hour')
    data_1d = get_all_candles(symbols, '1day')
    data_4h = data_4h.reset_index(drop=True)  
    data_1h = data_1h.reset_index(drop=True)       # reset index because when downloading data, it is not in order
    data_1d = data_1d.reset_index(drop=True)

    #breakouts = ichimoku_breakout(data_4h, breakouts, '4h', exchange)
    breakouts = ichimoku_breakout(data_1d, breakouts, '1d', exchange)
    breakouts = sr_breakout(data_1h, breakouts, exchange)
    #breakouts = sr_breakout(data_1d, breakouts, exchange)
    #breakouts = catching_knives(data_1h, breakouts, exchange)
    breakouts = ma_inch(data_1h, breakouts, exchange)
    breakouts = bottom(data_1d, breakouts, exchange)
    breakouts = rounding_breakout(data_1d, breakouts, exchange)
    breakouts = ma_pumpers(data_1h, breakouts, exchange)
    
    for dic in breakouts:
        send(messages=["{} | {} | {} | {}".format(dic['exc'], dic['symbol'], dic['type'], dic['timeframe'])])
        time.sleep(0.1)
        
        
def main():
    """Main function of the program which mainly controls
    timeflow and execution

    Argv : list
        List of arguments passed to the program (false, true, -h, --help)
    """
    
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print('Usage: python3 main.py <repeat>')
            print('<repeat> can be true or false')
            exit()
        elif sys.argv[1] == 'true':
            schedule.every().hour.at(':00').do(find_breakouts)
            while True:
                if (hour_rounder(dt.now())).timestamp() % 14400 == 0:
                    schedule.run_pending()
                time.sleep(1)

        elif sys.argv[1] == 'false':
            find_breakouts()

        else:
            raise Exception('Invalid argument: should be either true or false')


if __name__ == '__main__':
    main()