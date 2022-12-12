import os
import pandas as pd
from src.utils.constants import KLINES_COL_KEYS


def write_csv_to_db(db, path):

    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        if ".csv" in f:
            df = pd.read_csv(f, names=KLINES_COL_KEYS, header=None)
            df.drop(['Ignore'], inplace=True, axis=1)
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'i'}, inplace=True)
            df_dict = df.to_dict('records')
            db.insert_many(df_dict)
            print("Inserted collection")
