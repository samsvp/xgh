#%%
import numpy as np
import matplotlib. pyplot as plt


def plot_map(m, robot_pos, size):
    map = np.zeros(size)
    for x in m:
        map[x[1], x[0]] = 1

    map[robot_pos[1], robot_pos[0]] = 2

    plt.imshow(map)



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


# %%
if __name__ == "__main__":
    zt = np.array([2, 2, 2, 3, 2])

    # theta = 0 is looking to the left
    xt = [0, 0, np.pi / 2]
    xt_sensor = np.array([[0.1, 0.1, 0], [0.1, 0.1, 0],
        [0.1, 0.1, 0], [0.1, 0.1, 0], [0.1, 0.1, 0]])

    m = np.array([[0, 2], [3, 3], [2, 1]])
    sigma_squared = 0.5

    plot_map(m, xt, (10,10))

    z_hit = 0.6
    z_rand = 0.2
    z_max = 0.2

    print(lfield_ranger_model(zt, xt, xt_sensor, m, 
        sigma_squared, z_hit, z_rand, z_max))
# %%
