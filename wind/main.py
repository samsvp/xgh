#%%
import numpy as np
import pandas as pd

def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']


def rpy_to_quaternion(roll, pitch, yaw):
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    return np.array([cr * cp * cy + sr * sp * sy,
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy]).T

#%%
df = pd.read_csv("flights.csv")

corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')

dataset = df.iloc[:, 2:-6].dropna()

train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_labels = train_dataset['wind_angle']
test_labels = test_dataset['wind_angle']

train_dataset = train_dataset.iloc[:, 5:]
test_dataset = test_dataset.iloc[:, 5:]

train_stats = train_dataset.describe()
train_stats = train_stats.transpose()


normed_train_data = norm(train_dataset, train_stats)
normed_test_data = norm(test_dataset, train_stats)

train_labels = np.array(
    [np.cos(np.deg2rad(train_labels)),
     np.sin(np.deg2rad(train_labels))]).T


test_labels = np.array(
    [np.cos(np.deg2rad(test_labels)), 
     np.sin(np.deg2rad(test_labels))]).T

# %%
dataset = pd.read_csv("flights_new.csv")

corr = dataset.corr()
corr.style.background_gradient(cmap='coolwarm')

q = rpy_to_quaternion(dataset["roll"], 
    dataset["pitch"], dataset["yaw"])

mdataset = dataset.loc[:,:-3]
mdataset["orientation_w"] = q[:,0]
mdataset["orientation_x"] = q[:,1]
mdataset["orientation_y"] = q[:,2]
mdataset["orientation_z"] = q[:,3]

train_dataset = mdataset.sample(frac=0.8,random_state=0)
test_dataset = mdataset.drop(train_dataset.index)

train_labels = train_dataset["wind_angle"]
test_labels = test_dataset["wind_angle"]

train_dataset = train_dataset.iloc[:, 2:]
test_dataset = test_dataset.iloc[:, 2:]

train_stats = train_dataset.describe().transpose()

normed_train_data = norm(train_dataset, train_stats)
normed_test_data = norm(test_dataset, train_stats)

#%%
df = pd.read_csv("m600_flight.csv")

train_dataset = df.sample(frac=0.8,random_state=0)
test_dataset = df.drop(train_dataset.index)

train_labels = train_dataset["wind_speed_x"]
test_labels = test_dataset["wind_speed_x"]

train_dataset = train_dataset.iloc[:, 3:-2]
test_dataset = test_dataset.iloc[:, 3:-2]

train_stats = train_dataset.describe().transpose()

normed_train_data = norm(train_dataset, train_stats)
normed_test_data = norm(test_dataset, train_stats)


# %%
from sklearn.ensemble import RandomForestRegressor

regr = RandomForestRegressor(random_state=0)
regr.fit(normed_train_data, train_labels)
regr.score(normed_test_data, test_labels)
# %%
from sklearn.neural_network import MLPRegressor
regr_nn = MLPRegressor(random_state=1)
regr_nn.fit(normed_train_data, train_labels)
regr_nn.score(normed_test_data, test_labels)

# %%
from sklearn.ensemble import GradientBoostingRegressor
regr_gb = GradientBoostingRegressor(random_state=0)
regr_gb.fit(normed_train_data, train_labels)
regr_gb.score(normed_test_data, test_labels)

#%%
from sklearn.linear_model import BayesianRidge
regr_br = BayesianRidge()
regr_br.fit(normed_train_data, train_labels)
regr_br.score(normed_test_data, test_labels)


# %%
import matplotlib.pyplot as plt

y = regr.predict(normed_test_data)
plt.plot(test_labels.tolist())
plt.plot(y)
# %%
y = regr_nn.predict(normed_test_data)
plt.plot(test_labels.tolist())
plt.plot(y)
# %%
