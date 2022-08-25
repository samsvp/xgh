#%%
import numpy as np
import matplotlib.pyplot as plt

from grid_localization import MCL, get_next_pos


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


def p_max(zt: np.ndarray, z_max: float, tol=0.001) -> np.ndarray:
    return np.isclose(zt, z_max, tol).astype(float)


def p_rand(zt: np.ndarray, z_max: float) -> np.ndarray:
    p = 1 / z_max * np.ones(zt.shape)
    p[zt > z_max] = 0
    p[zt < 0] = 0
    return p


def test_range_m(zt: np.ndarray, zt_star: np.ndarray, 
        z_hit: float, z_short: float, zp_max: float, 
        z_rand: float, z_max: float, lmbda: float, 
        sigma: float) -> np.ndarray:


    p = np.sum(z_short * p_short(zt, zt_star, lmbda))
    q = np.sum(z_hit * p_hit(zt, zt_star, sigma, z_max) \
        + z_short * p_short(zt, zt_star, lmbda) \
        + zp_max * p_max(zt, z_max) \
        + z_rand * p_rand(zt, z_max))

    return p / q <= 0.2


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

    

nx = [0, 0, 0]
dt = 0.5
ct = [[0.5, 0.5, 0], [0.7, 0.2, 0], [0.2, 0.6, 0]]
n = 20
Xt = 2.0 * np.array([(x, y, 0) for x in np.arange(0,n)
    for y in np.arange(0,n)]) / n - 1.0
n = len(Xt)

min_x = np.min(Xt)
max_x = np.max(Xt)
for ut in [[-1., 1.], [-0.5, -0.5]]:#, [-0.1, -0.2]]:
    nx = get_next_pos(nx, ut, dt)
    Xt, _ = MCL(Xt, ut, ct, dt, nx, n)

    figure, axis = plt.subplots(1, 2)
    axis[0].hist([x[0] for x in Xt], range=[min_x, max_x], bins=50)
    axis[1].hist([x[1] for x in Xt], range=[min_x, max_x], bins=50)
    print(nx)
    plt.show()


Xt = np.array(Xt)

# simulate ray going up
zx_star = 1 - Xt[:,1]
#%%
z_max = 2
step = 0.01
zt = np.arange(0, z_max + step, step)
zt_star = 1 - nx[1]
sigma = 0.1
lmbda = .5

p_h = p_hit(zt, zt_star, sigma, z_max)
p_s = p_short(zt, zt_star, lmbda)
p_m = p_max(zt, z_max)
p_r = p_rand(zt, z_max)

z_hit, z_small, zp_max, z_rand = 0.5, 0.2, 0.2, 0.1
p = z_hit * p_h + z_small * p_s + zp_max * p_m + z_rand * p_r
p /= p.sum()
plt.plot(zt, p)
plt.title("p = p_hit + p_short + p_random + p_max")
plt.show()


r = np.random.rand(100000)
zt = np.arange(0, z_max+step, step)
pi = [zt[sample_p(p, _r)] for _r in r]
plt.hist(pi, bins=100)
plt.title("Sample distribution")
plt.show()

#%%
n = 1000
r = [test_range_m(z * np.ones(zx_star.shape[0]), 
        zx_star, z_hit, z_small, 
        zp_max, z_rand, z_max, lmbda, sigma)
        for z in pi[:n]]

y = np.array(pi[:n])
x = np.array(range(n))
fy = y[r[:n]]
fx = x[r[:n]]
plt.scatter(x, y)
plt.scatter(fx, fy)
# %%
