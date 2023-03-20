#%%
import os
import numpy as np
import pandas as pd


def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']

DATA_FOLDER = "csvs"
csvs = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER)]
df = pd.concat([pd.read_csv(_csv) for _csv in csvs])


train_dataset = df.sample(frac=0.8,random_state=0)
test_dataset = df.drop(train_dataset.index)

train_labels = train_dataset['wind_speed_y']
test_labels = test_dataset['wind_speed_y']

train_dataset = train_dataset.drop(columns=["wind_speed_y", "wind_speed_x"])
test_dataset = test_dataset.drop(columns=["wind_speed_y", "wind_speed_x"])

train_stats = train_dataset.describe()
train_stats = train_stats.transpose()

normed_train_data = norm(train_dataset, train_stats)
normed_test_data = norm(test_dataset, train_stats)


#%%
from sklearn.neural_network import MLPRegressor
regr_nn = MLPRegressor(random_state=1)
regr_nn.fit(normed_train_data, train_labels)
regr_nn.score(normed_test_data, test_labels)

# %%
