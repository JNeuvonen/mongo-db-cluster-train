#!/usr/bin/env python3


import math
from src.utils.constants import COLNAME_TO_KEY, ROWS_FOR_24h, ROWS_FOR_1h
import time


def generate_ts_to_index_lookup_table(data):
    ret = {}
    key = COLNAME_TO_KEY['Kline open time']

    for i in data.index:
        row = data.iloc[i]
        ret[row[key]] = i

    return ret


def get_data_from_btc_row(data, train_data_row, btc_row_index):

    # sma time windows
    rows_for_week = ROWS_FOR_24h * 7
    rows_for_24h = ROWS_FOR_24h
    rows_for_1h = 12

    if btc_row_index - rows_for_week < 0:
        return None

    sma_week = get_btc_sma_values(data, btc_row_index, rows_for_week)
    sma_24h = get_btc_sma_values(data, btc_row_index, rows_for_24h)
    sma_1h = get_btc_sma_values(data, btc_row_index, rows_for_1h)

    insert_sma_dict_into_final_data_row(train_data_row, sma_week, '168h')
    insert_sma_dict_into_final_data_row(train_data_row, sma_24h, '24h')
    insert_sma_dict_into_final_data_row(train_data_row, sma_1h, '1h')


def get_btc_sma_values(data, end_index, target_rows):

    index = end_index - target_rows

    # variables
    sma_open = 0
    sma_vol = 0
    sma_num_trades = 0
    sma_tkr_buy_bse_vol = 0
    sma_tkr_buy_qte_vol = 0
    sma_high_low_diff = 0

    while index < end_index:
        row = data.iloc[index]

        # variables from data row
        (open_price, vol, num_of_trades, tkr_buy_bse_vol,
         tkr_buy_qte_vol, hi_low_diff) = get_values_from_btc_row(row)

        sma_open += open_price
        sma_vol += vol
        sma_num_trades += num_of_trades
        sma_tkr_buy_bse_vol += tkr_buy_bse_vol
        sma_tkr_buy_qte_vol += tkr_buy_qte_vol
        sma_high_low_diff += hi_low_diff

        index += 1

    latest_btc_tick = data.iloc[end_index]
    (open_price, vol, num_of_trades,
     tkr_buy_bse_vol, tkr_buy_qte_vol, hi_low_diff) = get_values_from_btc_row(latest_btc_tick)

    sma_open = sma_open / target_rows / open_price - 1
    sma_vol = sma_vol / target_rows / vol - 1
    sma_num_trades = sma_num_trades / target_rows / num_of_trades - 1
    sma_tkr_buy_bse_vol = sma_tkr_buy_bse_vol / target_rows / tkr_buy_bse_vol - 1
    sma_tkr_buy_qte_vol = sma_tkr_buy_qte_vol / target_rows / tkr_buy_qte_vol - 1
    sma_high_low_diff = sma_high_low_diff / target_rows / hi_low_diff - 1

    return {
        "open": sma_open,
        "vol": sma_vol,
        "num_trades": sma_num_trades,
        "tkr_buy_bse_vol": sma_tkr_buy_bse_vol,
        "tkr_buy_qte_vol": sma_tkr_buy_qte_vol,
        "hi_low_diff": sma_high_low_diff
    }


def insert_sma_dict_into_final_data_row(final_data_row, sma_dict, sma_window):

    for key in sma_dict:
        key_for_ret_dict = 'sma_' + key + '_' + sma_window
        final_data_row[key_for_ret_dict] = sma_dict[key]


def get_values_from_btc_row(data_row):

    bse_vol = data_row[COLNAME_TO_KEY['Vol']]
    qte_vol = data_row[COLNAME_TO_KEY['Quote asset volume']]
    high = data_row[COLNAME_TO_KEY['High']]
    low = data_row[COLNAME_TO_KEY['Low']]
    close = data_row[COLNAME_TO_KEY['Close']]

    return (data_row[COLNAME_TO_KEY['Open']],
            bse_vol,
            data_row[COLNAME_TO_KEY['Number of trades']],
            data_row[COLNAME_TO_KEY['Taker buy base asset vol']] / bse_vol,
            data_row[COLNAME_TO_KEY['Taker buy quote asset vol']] / qte_vol,
            (high - low) / close
            )
