#!/usr/bin/env python3
import pandas as pd
import datetime

from dotenv import load_dotenv
from src.lib.db import client
from src.utils.functions import generate_ts_to_index_lookup_table, get_sma_values_for_row, difference_in_milliseconds
from src.utils.constants import ROWS_FOR_24h, COLNAME_TO_KEY


load_dotenv()


def generate_train_data():

    # UTIL
    BTC_COLL_KEY = "BTCUSDT-5m-klines"
    ROWS_FOR_WEEK = ROWS_FOR_24h * 7

    # DB
    db = client(database='crypto')
    train_data_db = client(database='train')['data']
    collections = db.list_collection_names()
    btc_data = pd.DataFrame(list(db[BTC_COLL_KEY].find({})))

    # TS TO INDEX LOOKUP TABLE
    btc_ts_lookup_table = generate_ts_to_index_lookup_table(
        btc_data)

    inserted_batches = 0

    for item in collections:
        if item != BTC_COLL_KEY:
            collection_data = pd.DataFrame(list(db[item].find({})))
            batch = []

            for ind in collection_data.index:

                if ind - ROWS_FOR_WEEK < 0:
                    continue

                ts = collection_data.iloc[ind][COLNAME_TO_KEY["Kline open time"]]
                btc_row_index = btc_ts_lookup_table[ts]

                train_data_row = {}

                start = datetime.datetime.now()

                get_sma_values_for_row(
                    data=collection_data,
                    train_data_row=train_data_row,
                    curr_row_index=ind,
                    key_pre_fix='coin')

                end = datetime.datetime.now()

                print('get_sma_values_for_row: ' +
                      difference_in_milliseconds(start, end))

                get_sma_values_for_row(
                    data=btc_data,
                    train_data_row=train_data_row,
                    curr_row_index=btc_row_index,
                    key_pre_fix='btc')

                batch.append(train_data_row)

                if len(batch) == 100:

                    batched_data_df = pd.concat(batch, axis=0)
                    batched_data_df.reset_index(inplace=True)
                    batched_data_df.drop(['index'], inplace=True, axis=1)
                    batched_data_dict = batched_data_df.to_dict('records')
                    train_data_db.insert_many(batched_data_dict)

                    inserted_batches += 1
                    print(inserted_batches)
                    batch = []


generate_train_data()
