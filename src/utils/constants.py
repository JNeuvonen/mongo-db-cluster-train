
ROWS_FOR_24h = 288
ROWS_FOR_1h = 12


KLINES_COLNAMES = ['Kline open time', 'Open', 'High', 'Low', 'Close', 'Vol', 'Kline Close time',
                   'Quote asset volume', 'Number of trades', 'Taker buy base asset vol', 'Taker buy quote asset vol', 'Ignore']
KLINES_COL_KEYS = ['k', 'o', 'h', 'l', 'c',
                   'v', 'K', 'q', 'n', 't', 'T', 'Ignore']


# Map readable key to as short key as possible to save storage space on server

KEY_TO_COLNAME = {
    'k': "Kline open time",
    'o': "Open",
    "h": "High",
    "l": "Low",
    "c": "Close",
    "v": "Vol",
    "K": "Kline Close time",
    "q": "Quote asset volume",
    "n": "Number of trades",
    "t": "Taker buy base asset vol",
    "T": "Taker buy quote asset vol",
    "Ignore": "Ignore"
}


# Map readable key to as short key as possible to save storage space on server
COLNAME_TO_KEY = {
    'Kline open time': 'k',
    'Open': "o",
    "High": "h",
    "Low": "l",
    "Close": "c",
    "Vol": "v",
    "Kline closet time": "K",
    "Quote asset volume": "q",
    "Number of trades": "n",
    "Taker buy base asset vol": "t",
    "Taker buy quote asset vol": "T",
    "Ignore": "Ignore"
}


def format_win_len(win_length):
    if win_length == ROWS_FOR_24h * 7:
        return '168h'

    if win_length == ROWS_FOR_24h:
        return '24h'

    if win_length == ROWS_FOR_1h:
        return '1h'


def get_key_with_suffix(key, suffix):
    return COLNAME_TO_KEY[key] + "_" + suffix
