#!/usr/bin/env python3

from dotenv import load_dotenv
from src.lib.db import client
import torch
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()


model = torch.load('model.pt')


# DATA
coll = client(database='train')['data']
DOCS_LIMIT = 100000


data = []

for doc in coll.find({}).limit(DOCS_LIMIT):
    df = pd.DataFrame(doc, index=range(len(doc.keys())))
    data.append(df)


# FORMAT DATA
test_data = pd.concat(data)
test_data.drop(['target', '_id', 'target'], axis=1, inplace=True)
test_data = test_data.to_numpy()
test_data = torch.from_numpy(test_data)
test_data = test_data.to(torch.float32)
test_data = torch.nn.functional.normalize(test_data)

test_data = torch.where(torch.isnan(
    test_data), torch.zeros_like(test_data), test_data)

pred_tensor = model(test_data)
pred_df = pd.DataFrame(pred_tensor.detach().numpy())

pred_df.hist()
plt.show()
