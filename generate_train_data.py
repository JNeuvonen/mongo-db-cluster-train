#!/usr/bin/env python3
import pandas as pd
import datetime

from dotenv import load_dotenv
from src.lib.db import client
from src.utils.functions import add_sma_from_binance_kline
from src.utils.constants import ROWS_FOR_24h, COLNAME_TO_KEY


load_dotenv()


def generate_train_data():

    # UTIL
    BTC_COLL_KEY = "BTCUSDT-5m-klines"

    # DB
    db = client(database='crypto')
    train_data_db = client(database='train')['data']
    collections = db.list_collection_names()
    btc_data = pd.DataFrame(list(db[BTC_COLL_KEY].find({})))

    for item in collections:
        if item != BTC_COLL_KEY:
            collection_data = pd.DataFrame(list(db[item].find({})))

            final_df = pd.DataFrame()

            merged_df = pd.merge(
                collection_data, btc_data, on='k')

            merged_df.drop(['_id_x', '_id_y', 'i_y'], axis=1, inplace=True)

            add_sma_from_binance_kline(
                final_df, merged_df, ROWS_FOR_24h * 7)

            add_sma_from_binance_kline(
                final_df, merged_df, ROWS_FOR_24h)

            add_sma_from_binance_kline(
                final_df, merged_df, int(ROWS_FOR_24h / 24))

            df_dict = final_df.to_dict('records')
            train_data_db.insert_many(df_dict)


generate_train_data()
