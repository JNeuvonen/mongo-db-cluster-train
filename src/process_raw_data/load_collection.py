import pandas as pd
import os
from dotenv import load_dotenv
from src.lib.db import client
load_dotenv()


def load_collection(database, collection_name):

    db = client(database, collection_name)

    data = pd.DataFrame(list(db.find({})))

    print(data)
