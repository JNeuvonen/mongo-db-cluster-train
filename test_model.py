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
DOCS_LIMIT = 10000


data = []

for doc in coll.find({}).limit(DOCS_LIMIT):
    df = pd.DataFrame(doc, index=range(len(doc.keys())))
    data.append(df)

# FORMAT DATA
test_data = pd.concat(data)
target_data = test_data['target']
test_data.drop(['target', '_id', 'target'], axis=1, inplace=True)
test_data = test_data.to_numpy()
test_data = torch.from_numpy(test_data)
test_data = test_data.to(torch.float32)
test_data = torch.nn.functional.normalize(test_data)

test_data = torch.where(torch.isnan(
    test_data), torch.zeros_like(test_data), test_data)

balance = 10000
index = 0
ticks_invested = 0
short_bets = 0
long_bets = 0
chart_of_balance = [balance]

for item in test_data:
    pred = model(item)
    pred = pred.detach().numpy()[0] + 1
    target = target_data.iloc[index] + 1

    if pred > 1.05 and ticks_invested >= 30:
        balance = balance * target
        ticks_invested = 0
        long_bets += 1
        chart_of_balance.append(balance)

    index += 1
    ticks_invested += 1

plt.plot(chart_of_balance)
plt.show()
