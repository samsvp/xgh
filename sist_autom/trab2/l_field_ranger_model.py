#%%
import random
import numpy as np
import matplotlib.pyplot as plt


def plot_map(m, robot_pos, size, title):
    map = np.zeros(size)
    for x in m:
        map[x[1], x[0]] = 1

    map[robot_pos[1], robot_pos[0]] = 2

    plt.title(title)
    plt.imshow(map)
    x, y, theta = robot_pos
    plt.plot([x, x + 0.5 * np.cos(theta)],
            [y, y + 0.5 * np.sin(theta)])


def sample(b):
    return b / 6 * np.sum(
        [random.uniform(-1,1) for i in range(12)])


def prob(x, sigma_squared):
    mu = 0
    denom = np.sqrt(2 * np.pi * sigma_squared)
    p = np.exp(-(x-mu)**2/(2*sigma_squared)) / denom
    return p


def lfield_ranger_model(zt, xt, xt_sensor, 
        m, sigma_squared, z_hit, z_random, z_max):
    """
    Parameters:
    zt: vector of measurements
    xt: robot position, vector of length 3
    xt_sensor: sensor position and rotation. Same shape as zt
    m: the map with the positions of the obstacles
    """
    q = 0
    x, y, theta = xt
    for i in range(xt_sensor.shape[0]):
        x_sens, y_sens, theta_sens = xt_sensor[i]
        
        x_z = x + x_sens * np.cos(theta) \
            - y_sens * np.sin(theta) \
            + zt[i] * np.cos(theta + theta_sens)
        y_z = y + y_sens * np.cos(theta) \
            + x_sens * np.sin(theta) \
            + zt[i] * np.sin(theta + theta_sens)

        x_line = m[:,0]
        y_line = m[:,1]
        dist_squared = ((x_z - x_line)**2 + (y_z - y_line) ** 2).min()

        q += np.log(
            z_hit * prob(dist_squared, sigma_squared) \
            + z_random / z_max)

    return q


def landmark_known_corr(ft, ct, xt, sigma_squared):
    """
    Parameters
    ft: vector of observed feature
    ct: true feature corresponding to ft
    xt: current robot position
    sigma_squared: prob variance
    """
    rt, phit, st = ft
    xc, yc, sc = ct
    x, y, theta = xt
    r_hat = np.sqrt((xc - x)**2 + (yc - y)**2)
    phi_hat = np.arctan2(yc - y, xc - x)
    q = prob(rt - r_hat, sigma_squared) \
        * prob(phit - phi_hat, sigma_squared)\
        * prob(st - sc, sigma_squared)
    return q


def sample_landmark_known_corr(ft, ct, 
        sigmar_squared, sigmap_squared):
    """
    Samples robot poses for a given landmark measurement ft.
    Parameters
    ft: vector of observed feature
    ct: true feature corresponding to ft
    sigma_squared: prob variance
    """
    rt, phit, st = ft
    xc, yc, sc = ct
    
    gamma_hat = np.random.rand() * 2 * np.pi
    r_hat = rt + sample(sigmar_squared)
    phi_hat = phit + sample(sigmap_squared)
    x = xc + r_hat * np.cos(gamma_hat)
    y = yc + r_hat * np.sin(gamma_hat)
    theta = gamma_hat - np.pi - phi_hat
    
    return np.array([x, y, theta])

# %%
if __name__ == "__main__":
    # theta = 0 is looking to the left
    xt = [0, 0, np.pi / 2]
    xt_sensor = np.array([[0.1, 0.1, 0], [0.1, 0.1, 0],
        [0.1, 0.1, 0], [0.1, 0.1, 0], [0.1, 0.1, 0]])

    m = np.array([[0, 2], [3, 3], [2, 1]])
    sigma_squared = 0.5

    z_hit = 0.6
    z_rand = 0.2
    z_max = 0.2

    zt = np.array([2, 2, 2, 3, 2])
    for i, xt in enumerate([[0, 0, np.pi / 2], 
               [0, 0, np.pi / 4],
               [0, 0, 0],
               [0, 0, -np.pi / 4],
               [0, 0, -np.pi / 2]]):
        p = lfield_ranger_model(zt, xt, xt_sensor, m, 
            sigma_squared, z_hit, z_rand, z_max)
        plot_map(m, xt, (10,10), f"Likelihood: {p}")
        plt.savefig(f"alg_3_{i}.png")
        plt.show()
    
    
    # theta = 0 is looking to the left
    xt_sensor = np.array([[0.1, 0.1, 0], [0.1, 0.1, 0],
        [0.1, 0.1, 0], [0.1, 0.1, 0], [0.1, 0.1, 0]])

    m = np.array([[0, 2], [3, 3], [2, 1]])
    sigma_squared = 0.5

    z_hit = 0.6
    z_rand = 0.2
    z_max = 0.2
    zt = np.array([1, 1, 1, 1, 1])
    for i, xt in enumerate([[1, 1, np.pi / 2], 
               [1, 1, np.pi / 4],
               [1, 1, 0],
               [1, 1, -np.pi / 4],
               [1, 1, -np.pi / 2]]):
        p = lfield_ranger_model(zt, xt, xt_sensor, m, 
            sigma_squared, z_hit, z_rand, z_max)
        plot_map(m, xt, (10,10), f"Likelihood: {p}")
        plt.savefig(f"alg_3_1{i}.png")
        plt.show()
# %%
    ft = [1, np.pi / 2, 0]
    ct = [1, 1, 0]
    points = np.array(
        [sample_landmark_known_corr(ft, ct, 0.5, 0.5) 
         for _ in range(1000)])
    
    # plot the positions
    plt.figure(figsize=(8, 6), dpi=80)
    plt.scatter(points[:,0], points[:,1], s=2.5)
    # plot the orientations
    for point in points:
        x, y, theta = point
        plt.plot([x, x + 0.05 * np.cos(theta)], 
            [y, y + 0.05 * np.sin(theta)])
    plt.title("Sample distribution generated from f = [1, 1.57,0]")
    plt.savefig("alg_5.png")
    plt.show()

# %%
