#%%
import random
import numpy as np

alphas = [0.001,0.001,0.1,0.1,0.01,0.01]

def prob(a, b):
    return 1 / np.sqrt(2 * np.pi * b) * np.exp(-0.5 * a**2 / b)


def sample(b):
    return b / 6 * np.sum(
        [random.uniform(-1,1) for i in range(12)])


def motion_model_vel(xt, ut, xtm1, dt):
    v, w = ut
    x, y, theta = xtm1
    x_line, y_line, theta_line = xt
    mu = 0.5 * ((x - x_line) * np.cos(theta) + (y - y_line) * np.sin(theta)) \
        / ((y - y_line) * np.cos(theta) - (x - x_line) * np.sin(theta))

    x_star = (x + x_line) / 2 + mu * (y - y_line)
    y_star = (y + y_line) / 2 + mu * (x_line - x)
    r_star = np.sqrt((x - x_star)**2 + (y - y_star)**2)

    delta_theta = np.arctan2(y_line - y_star, x_line - x_star) \
        - np.arctan2(y - y_star, x - x_star)
    v_hat = delta_theta / dt * r_star
    w_hat = delta_theta / dt
    gamma_hat = (theta_line - theta) / dt - w_hat

    return prob(v - v_hat, alphas[0]*v**2 + alphas[1]*w**2)\
        * prob(w - w_hat, alphas[2]*v**2 + alphas[3]*w**2)\
        * prob(gamma_hat, alphas[4]*v**2 + alphas[5]*w**2)


def sample_motion_model_vel(ut, xtm1, dt):
    v, w = ut
    x, y, theta = xtm1

    v_hat = v + sample(alphas[0]*v**2 + alphas[1]*w**2)
    w_hat = w + sample(alphas[2]*v**2 + alphas[3]*w**2)
    gamma_hat = sample(alphas[4]*v**2 + alphas[5]*w**2)

    x_line = x - v_hat / w_hat * np.sin(theta) + v_hat / w_hat * np.sin(theta + w_hat * dt)
    y_line = y + v_hat / w_hat * np.cos(theta) - v_hat / w_hat * np.cos(theta + w_hat * dt)
    theta_line = theta + w_hat * dt + gamma_hat * dt

    return [x_line, y_line, theta_line]

# %%
import matplotlib.pyplot as plt

n = 10000
xi = [0,0,0]

u = [1,0]
dt = 1

s = np.array([
        sample_motion_model_vel(u, xi, dt)
    for i in range(n)])

c = np.array([
    motion_model_vel(xt, u, xi, dt)
    for xt in s
])

plt.scatter(s[:,0], s[:,1], s=0.1, c=c)
# %%
