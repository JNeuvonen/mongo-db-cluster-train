#!/usr/bin/env python3
from dotenv import load_dotenv
from src.lib.db import client
from src.utils.functions import generate_ts_to_index_lookup_table, get_data_from_btc_row
from src.utils.constants import ROWS_FOR_24h, COLNAME_TO_KEY
import pandas as pd

load_dotenv()


def generate_train_data():

    # UTIL
    BTC_COLL_KEY = "BTCUSDT-5m-klines"
    ROWS_FOR_WEEK = ROWS_FOR_24h * 7

    # DB
    db = client(database='crypto')
    collections = db.list_collection_names()
    btc_data = pd.DataFrame(list(db[BTC_COLL_KEY].find({})))

    # TS TO INDEX LOOKUP TABLE
    btc_ts_lookup_table = generate_ts_to_index_lookup_table(
        btc_data)

    for item in collections:
        if item != BTC_COLL_KEY:
            data = pd.DataFrame(list(db[item].find({})))

            for ind in data.index:

                if ind - ROWS_FOR_WEEK < 0:
                    continue

                ts = data.iloc[ind][COLNAME_TO_KEY["Kline open time"]]
                btc_row_index = btc_ts_lookup_table[ts]

                train_data_row = {}

                get_data_from_btc_row(
                    data=btc_data, train_data_row=train_data_row, btc_row_index=btc_row_index)

                print(train_data_row)


generate_train_data()
