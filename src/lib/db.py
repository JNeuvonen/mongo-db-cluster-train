from pymongo import MongoClient
import os


def client(database):
    CONN_STRING = os.environ.get(
        'DB_CONN_STRING')

    if CONN_STRING == None:
        print("Invalid env")
        return None

    client = MongoClient(CONN_STRING, ssl=True,
                         tlsAllowInvalidCertificates=True)

    db = client[database]

    return db
