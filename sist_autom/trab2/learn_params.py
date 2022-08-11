#%%
import numpy as np
import pandas as pd

from beam_ranger import p_hit, p_max, p_rand, p_short


def learn_params(Z: np.ndarray, Z_star: np.ndarray, z_max: float):
    sigma = 1.0
    lmbda = 1.0
    for i in range(20):
        n = 1 / (p_hit(Z, Z_star, sigma, z_max) + p_max(Z, z_max) 
            + p_rand(Z, z_max) + p_short(Z, Z_star, lmbda))
        e_i_hit = n * p_hit(Z, Z_star, sigma, z_max)
        e_i_short = n * p_short(Z, Z_star, lmbda)
        e_i_max = n * p_max(Z, z_max)
        e_i_rand = n * p_rand(Z, z_max)

        norm_Z_inv = 1 / Z.shape[0]
        z_hit = norm_Z_inv * np.sum(e_i_hit)
        z_short = norm_Z_inv * np.sum(e_i_short)
        zp_max = norm_Z_inv * np.sum(e_i_max)
        z_rand = norm_Z_inv * np.sum(e_i_rand)

        sigma = np.sqrt( 
            np.sum(e_i_hit * ((Z - Z_star) ** 2)) 
            /  np.sum(e_i_hit))
        lmbda = np.sum(e_i_short) / np.sum(e_i_short * Z)

        print("\n")
        print(f"z_hit: {z_hit}, z_short: {z_short}, zp_max: {zp_max}, z_rand: {z_rand}, sigma: {sigma}, lambda: {lmbda}")

    return (z_hit, z_short, zp_max, z_rand, sigma, lmbda)


def learn_params2(Z: np.ndarray, Z_star: np.ndarray, z_max: float):
    sigma = 1.0
    lmbda = 0.1

    for i in range(20):
        _phit = p_hit(Z, Z_star, sigma, z_max)
        _pmax = p_max(Z, z_max) 
        _prand = p_rand(Z, z_max) 
        _pshort = p_short(Z, Z_star, lmbda)

        Zhit = []
        Zshort = []
        Zmax = []
        Zrand = []
        for i in range(_phit.shape[0]):
            idx = np.argmax([_phit[i], _pshort[i],_pmax[i], _prand[i]])
            Zhit.append(idx == 0)
            Zshort.append(idx == 1)
            Zmax.append(idx == 2)
            Zrand.append(idx == 3)

        sigma = np.sqrt(np.sum((Z[Zhit] - Z_star[Zhit]) ** 2)/  np.sum([Zhit]))
        lmbda = np.sum(Zshort) / np.sum(Z[Zshort])

        print("\n")
        print(f"sigma: {sigma}, lambda: {lmbda}")

    return (sigma, lmbda)



# load and shuffle dataset
df = pd.read_csv("dataset2.csv")

# data
ztk = df["ztk"].to_numpy()
ztk_star = df["ztk_star"].to_numpy()

# targets
z_hit = df["z_hit"][0]
z_small = df["z_small"][0]
zp_max = df["zp_max"][0]
z_rand = df["z_rand"][0]
sigma = df["sigma"][0]
lmbda = df["lambda"][0]


z_max = 10
# %%
print(learn_params(ztk, ztk_star, z_max))
# %%
