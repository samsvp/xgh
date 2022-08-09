#%%
import numpy as np


def p_hit(zt: np.ndarray, zt_star: np.ndarray, 
        sigma: float, z_max: float) -> np.ndarray:
    normal = np.exp(-.5 * (zt - zt_star) ** 2 / sigma ** 2)\
        /(np.sqrt(2 * np.pi)*sigma)

    # normal divided by the integral
    p = normal / np.sqrt(np.pi)

    p[zt > z_max] = 0
    p[zt < 0] = 0

    return p


def p_short(zt: np.ndarray, zt_star: np.ndarray, 
        lmbda: float) -> np.ndarray:
    n = 1 / (1 - np.exp(- lmbda * zt_star))
    p = n * lmbda * np.exp(- lmbda * zt)
    
    #if zt > zt_star or zt < 0: return 0
    p[zt > zt_star] = 0
    p[zt < 0] = 0

    return p


def p_max(zt: np.ndarray, z_max: float, tol=0.01) -> np.ndarray:
    return np.isclose(zt, z_max, tol).astype(float)


def p_rand(zt: np.ndarray, z_max: float) -> np.ndarray:
    p = 1 / z_max * np.ones(zt.shape)
    p[zt > z_max] = 0
    p[zt < 0] = 0
    return p



def beam_ranger_finder(zt: np.ndarray, zt_star: np.ndarray, 
        z_hit: float, z_short: float, zp_max: float, 
        z_rand: float, z_max: float, lmbda: float, 
        sigma: float) -> np.ndarray:

    p = z_hit * p_hit(zt, zt_star, sigma, z_max) \
        + z_short * p_short(zt, zt_star, lmbda) \
        + zp_max * p_max(zt, z_max) \
        + z_rand * p_rand(zt, z_max)

    # use log likelihood due to vanishing gradients
    return np.sum(np.log(p))


# %%
import matplotlib.pyplot as plt

z_max = 10
step = 0.1
zt = np.arange(0, z_max + step, step)
zt_star = 5
sigma = 0.5

p_h = p_hit(zt, zt_star, sigma, z_max)
plt.plot(p_h)
plt.show()

lmbda = 0.25
p_s = p_short(zt, zt_star, lmbda)
plt.plot(p_s)
plt.show()

p_m = p_max(zt, z_max)
plt.plot(p_m)
plt.show()

p_r = p_rand(zt, z_max)
plt.plot(p_r)
plt.show()

p = p_h + 0.5 * p_s + 0.5 * p_m + 0.1 * p_r
p /= p.sum()
plt.plot(p)
plt.show()

# %%
# create map
m = np.zeros((50, 25)) # map
m[0, :] = 1
m[-1, :] = 1
m[:, 0] = 1
m[:, -1] = 1
plt.imshow(m)

# %%

def sample_p(p: np.ndarray, x: float):
    """
    Returns the index of a sample from the given distribution 
    'p' given a single value 'x' between 0 and 1
    """
    pp = 0
    for i, pi in enumerate(p):
        if x < pp: return i
        pp += pi
    return p.shape[0] - 1

r = np.random.rand(100000)
pi = [sample_p(p, _r) for _r in r]
plt.hist(pi, bins=100)

# %%
#Calculate distance from the center of a box to the nearest
#point given an angle theta 

size = np.array([50, 25])
xi = size / 2

thetas = np.arange(-45, 45, 1)

# array of distances from center 
d1 = np.abs(size[0] / 2 / np.cos(np.deg2rad(thetas)))
d2 = np.abs(size[1] / 2 / np.cos(np.deg2rad(thetas)))
d3 = np.abs(size[0] / 2 / np.cos(np.deg2rad(thetas)))
d4 = np.abs(size[1] / 2 / np.cos(np.deg2rad(thetas)))


# apply noise to our measurements
zt_star = np.concatenate((d1, d2, d3, d4), axis=0)
z_max = 2 * np.max(zt_star)
zt = np.arange(0, z_max + 0.1, 0.1)
sigma = 2.5
lmbda = 0.05

dataset = []
z_hit = 1.0
z_small = 0.25
zp_max = 0.1
z_rand = 0.1
for ztk_star in zt_star:
    p_h = p_hit(zt, ztk_star, sigma, z_max)
    p_s = p_short(zt, ztk_star, lmbda)
    p_m = p_max(zt, z_max)
    p_r = p_rand(zt, z_max)

    p = z_hit * p_h + z_small * p_s + zp_max * p_m + z_rand * p_r
    p /= p.sum()

    dataset += [(zt[sample_p(p, np.random.rand())], ztk_star)
            for _ in range(1000)]


dataset = np.array(dataset)

# %%
# sava dataframe
import pandas as pd

df = pd.DataFrame(dataset)
df.columns = ["ztk", "ztk_star"]
df["z_hit"] = z_hit
df["z_small"] = z_small
df["zp_max"] = zp_max
df["z_rand"] = z_rand
df["sigma"] = sigma
df["lambda"] = lmbda

#df.to_csv("dataset.csv")
# %%
# vanishing gradient, ofc
zt = df["ztk"][:1000]
zt_star = df["ztk_star"][:1000]
beam_ranger_finder(zt, zt_star, z_hit, z_small, 
    zp_max, z_rand, z_max, lmbda, sigma)
# %%
