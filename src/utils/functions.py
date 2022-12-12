#!/usr/bin/env python3


import math
from src.utils.constants import COLNAME_TO_KEY, ROWS_FOR_24h, ROWS_FOR_1h
import datetime


def generate_ts_to_index_lookup_table(data):
    ret = {}
    key = COLNAME_TO_KEY['Kline open time']

    for i in data.index:
        row = data.iloc[i]
        ret[row[key]] = i

    return ret


def get_sma_values_for_row(data, train_data_row, curr_row_index, key_pre_fix):

    # sma time windows
    rows_for_week = ROWS_FOR_24h * 7
    rows_for_24h = ROWS_FOR_24h
    rows_for_1h = ROWS_FOR_1h

    if curr_row_index - rows_for_week < 0:
        return None

    sma_week = sma_values(data, curr_row_index, rows_for_week, key_pre_fix)
    sma_24h = sma_values(data, curr_row_index, rows_for_24h, key_pre_fix)
    sma_1h = sma_values(data, curr_row_index, rows_for_1h, key_pre_fix)

    insert_sma_dict_into_final_data_row(train_data_row, sma_week, '168h')
    insert_sma_dict_into_final_data_row(train_data_row, sma_24h, '24h')
    insert_sma_dict_into_final_data_row(train_data_row, sma_1h, '1h')


def sma_values(data, end_index, target_rows, key_pre_fix):

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

    sma_open = div_by_zero_guard(sma_open / target_rows, open_price, 1) - 1
    sma_vol = div_by_zero_guard(sma_vol / target_rows, vol, 1) - 1
    sma_num_trades = div_by_zero_guard(
        sma_num_trades / target_rows, num_of_trades, 1) - 1
    sma_tkr_buy_bse_vol = div_by_zero_guard(
        sma_tkr_buy_bse_vol / target_rows, tkr_buy_bse_vol, 1) - 1
    sma_tkr_buy_qte_vol = div_by_zero_guard(
        sma_tkr_buy_qte_vol / target_rows, tkr_buy_qte_vol, 1) - 1
    sma_high_low_diff = div_by_zero_guard(
        sma_high_low_diff / target_rows, hi_low_diff, 1) - 1

    return {
        key_pre_fix + "_" + "open": sma_open,
        key_pre_fix + "_" + "vol": sma_vol,
        key_pre_fix + "_" + "num_trades": sma_num_trades,
        key_pre_fix + "_" + "tkr_buy_bse_vol": sma_tkr_buy_bse_vol,
        key_pre_fix + "_" + "tkr_buy_qte_vol": sma_tkr_buy_qte_vol,
        key_pre_fix + "_" + "hi_low_diff": sma_high_low_diff
    }


def insert_sma_dict_into_final_data_row(final_data_row, sma_dict, sma_window):

    for key in sma_dict:
        key_for_ret_dict = 'sma_' + key + '_' + sma_window
        final_data_row[key_for_ret_dict] = sma_dict[key]


def get_values_from_btc_row(data_row):

    bse_vol = data_row[COLNAME_TO_KEY['Vol']]
    qte_vol = data_row[COLNAME_TO_KEY['Quote asset volume']]
    high = data_row[COLNAME_TO_KEY['High']] * 1000
    low = data_row[COLNAME_TO_KEY['Low']] * 1000
    close = data_row[COLNAME_TO_KEY['Close']] * 1000

    return (data_row[COLNAME_TO_KEY['Open']],
            bse_vol,
            data_row[COLNAME_TO_KEY['Number of trades']],
            div_by_zero_guard(
                data_row[COLNAME_TO_KEY['Taker buy base asset vol']], bse_vol, 0),
            div_by_zero_guard(
                data_row[COLNAME_TO_KEY['Taker buy quote asset vol']], qte_vol, 0),
            (high - low) / close
            )


def div_by_zero_guard(dividend, divisor, fallback_val):

    if divisor == 0:
        return fallback_val

    return dividend / divisor


def difference_in_milliseconds(date_start, date_end):
    return int((date_end-date_start).total_seconds() * 1000)
