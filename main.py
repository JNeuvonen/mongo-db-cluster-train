import os
from process_raw_data.raw_data_to_db import write_csv_to_db
from lib.db import client
from dotenv import load_dotenv


load_dotenv()


def main():

    db = client(database=os.environ.get('MONGO_DB'))

    write_csv_to_db(db['DOGEUSDT-5m-klines'], path='process_raw_data/data')


main()
