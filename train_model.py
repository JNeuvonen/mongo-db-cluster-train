#!/usr/bin/env python3

from dotenv import load_dotenv
from src.lib.db import client
from src.net.main import NeuralNet

import pandas as pd
import math
import torch

load_dotenv()


def train_model():

    # DATA
    coll = client(database='train')['data']
    DOCS_LIMIT = 100000

    # MODEL PARAMETERS
    NUM_INPUTS = 0
    NUM_OUTPUT = 1

    for doc in coll.find({}):
        df = pd.DataFrame(doc, index=range(len(doc.keys())))
        df.drop(['target', '_id'], inplace=True, axis=1)
        NUM_INPUTS = df.shape[1]
        break

    # MODEL
    model = NeuralNet(NUM_INPUTS, math.floor(NUM_INPUTS / 2), NUM_OUTPUT)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters())

    # NEURAL NET UTIL
    docs = []
    BATCH_SIZE = 10000
    NUM_EPOCHS = 10

    for epoch in range(NUM_EPOCHS):

        epoch_loss = 0
        total_docs = 0

        for doc in coll.find({}).limit(DOCS_LIMIT):
            df = pd.DataFrame(doc, index=range(len(doc.keys())))
            docs.append(df)
            total_docs += df.shape[0]

            if len(docs) == BATCH_SIZE:
                print(total_docs)
                # PRE PROCESS
                train_batch = pd.concat(docs)
                y = train_batch['target']
                x = train_batch.drop(['target', '_id'], axis=1)
                docs = []

                x = x.to_numpy()
                x = torch.from_numpy(x)
                x = x.to(torch.float32)

                y = y.to_numpy()
                y = torch.from_numpy(y)
                y = y.to(torch.float32)
                y = y.reshape(len(y), 1)

                x = torch.nn.functional.normalize(x)
                y = torch.nn.functional.normalize(y)

                x = torch.where(torch.isnan(
                    x), torch.zeros_like(x), x)

                # PREDICT
                outputs = model(x)

                # OPTIMIZE & BACKWARD
                loss = criterion(outputs, y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

        epoch_loss = math.sqrt(epoch_loss / total_docs)

        print(f'Epoch {epoch+1}: loss = {epoch_loss:.5f}')

    torch.save(model, 'model.pt')


train_model()
