#%%
from functools import reduce
import random
import numpy as np
import matplotlib.pyplot as plt

alphas = [0.001,0.001,0.001,0.001,0.01,0.01]

def prob(a, b):
    return 1 / np.sqrt(2 * np.pi * b) * np.exp(-0.5 * a**2 / b)


def sample(b):
    return b / 6 * np.sum(
        [random.uniform(-1,1) for i in range(12)])


def motion_model_vel(xt, ut, xtm1, dt):
    v, w = ut
    x, y, theta = xtm1
    x_line, y_line, theta_line = xt
    if (y - y_line != 0 and x - x_line != 0):
        mu = 0.5 * ((x - x_line) * np.cos(theta) + (y - y_line) * np.sin(theta)) \
            / ((y - y_line) * np.cos(theta) - (x - x_line) * np.sin(theta))

        x_star = (x + x_line) / 2 + mu * (y - y_line)
        y_star = (y + y_line) / 2 + mu * (x_line - x)
        
        r_star = np.sqrt((x - x_star)**2 + (y - y_star)**2)

        delta_theta = np.arctan2(y_line - y_star, x_line - x_star) \
            - np.arctan2(y - y_star, x - x_star)
        v_hat = delta_theta / dt * r_star
        w_hat = delta_theta / dt

        return prob(v - v_hat, 0.001)\
            * prob(w - w_hat, 0.001)
    return 0


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


def get_ft(ct, xt):
    xc, yc, sc = ct
    x, y, theta = xt
    r = np.sqrt((xc - x)**2 + (yc - y)**2) + 0.01 * np.random.rand()
    phi = np.arctan2(yc - y, xc - x) + 0.01 * np.random.rand()
    return [r, phi, sc]


def get_next_pos(mu_l: np.ndarray, ut: np.ndarray, dt: float) -> np.ndarray:
    theta = mu_l[-1]
    vt, wt = ut
    mut = mu_l + np.array([
        -vt / wt * np.sin(theta) + vt/wt * np.sin(theta + wt * dt),
        vt / wt * np.cos(theta) - vt / wt * np.cos(theta + wt * dt),
        wt * dt])
    return mut


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


def grid_localization(p, ut, ct, Xt, dt, nx):
    """
    Calculates the probability of the localization of
    the robot in a grid
    parameters:
    p: the prior probability that the robot is at position
        (x,y)
    ut: control signal
    ct: landmark
    Xt: grid of possible positions
    dt: time by which the robot moved
    nx: the true position of the robot after moving (used
        to make the landmark measurement)
    """
    for k in range(len(Xt)):
        p[k] = sum([p[i] * mv for i in range(len(Xt)) 
            if not np.isnan((mv:=motion_model_vel(Xt[k], ut, Xt[i], dt)))])
        
        for c in ct:
            ft = get_ft(c, nx)
            p[k] = p[k] * landmark_known_corr(ft, c, Xt[k], 0.01)
    p /= p.sum()
    return p


# shout-out to http://www.u.arizona.edu/~ximyu/stuff/slides/20090324_CS645_MonteCarloLocalization.pdf
def MCL(Xtm1, ut, ct, dt, nx, n):
    """
    Monte Carlo localization
    Xtm1: last particles positions
    ut: control signal
    ct: landmarks
    dt: delta time
    n: number of particles
    nx: true next position
    """
    Xt = []
    Xt_bar = []
    W = [] # keep W and Xt separated for convenience 
    for m in range(n):
        xtm = sample_motion_model_vel(ut, Xtm1[m], dt)
        w = reduce(
            lambda x, y: x * y,
            [landmark_known_corr(
                get_ft(c, nx), c, xtm, 0.01)
                for c in ct], 1.0)
        Xt_bar.append(xtm)
        W.append(w)

    # normalize weights
    W = np.array(W)
    W /= W.sum()
    # generate particles
    Xt = [Xt_bar[sample_p(W, np.random.rand())]
        for m in range(n)]
    return (Xt, W)



def MCL_aug(Xtm1, ut, ct, dt, nx, n):
    # static variables
    if "w_slow" not in MCL_aug.__dict__:
        MCL_aug.w_slow = .0
        MCL_aug.w_fast = .0

    alpha_s = 0.1
    alpha_f = 0.99
    Xt = []
    Xt_bar = []
    w_avg = 0
    W = [] # keep W and Xt separated for convenience 
    for m in range(n):
        xtm = sample_motion_model_vel(ut, Xtm1[m], dt)
        w = reduce(
            lambda x, y: x * y,
            [landmark_known_corr(
                get_ft(c, nx), c, xtm, 0.01)
                for c in ct], 1.0)
        Xt_bar.append(xtm)
        w_avg += w / n
        W.append(w)

    MCL_aug.w_slow += alpha_s * (w_avg - MCL_aug.w_slow)
    MCL_aug.w_fast += alpha_f * (w_avg - MCL_aug.w_fast)

    print(1.0 - MCL_aug.w_fast / MCL_aug.w_slow)
    for _ in range(n):
        W.append(
            max(0, 
            1.0 - MCL_aug.w_fast / MCL_aug.w_slow))
        r = lambda: 2.0 * np.random.rand() - 1.0
        Xt_bar.append([r(), r(), r()])

    # normalize weights
    W = np.array(W)
    W /= W.sum()
    # generate particles
    Xt = [Xt_bar[sample_p(W, np.random.rand())]
        for m in range(n)]
    return Xt


def KLD_MCL(Xtm1, Wtm1, ut, ct, dt, nx, n, 
        sigma, min_x, max_x):
    """
    Monte Carlo localization with KDL sampling
    Xtm1: last particles positions
    Wtm1: weights of last particles positions
    ut: control signal
    ct: landmarks
    dt: delta time
    n: number of particles
    nx: true next position
    sigma: standard deviation of something
    min_x: minimum value of the map
    max_x: maximum value of the map
    """
    Xt = []
    W = []
    M = 0
    Mx = 0
    k = 0
    M_min = n // 10

    bh = 5
    H = np.zeros(int(n / bh))
    while (M < Mx or M < M_min):
        i = sample_p(Wtm1, np.random.rand())
        xtm = sample_motion_model_vel(ut, Xtm1[i], dt)
        w = reduce(
            lambda x, y: x * y,
            [landmark_known_corr(
                get_ft(c, nx), c, xtm, 0.01)
                for c in ct], 1.0)
        Xt.append(xtm)
        W.append(w)

        get_bin = lambda x: \
            int(((x - min_x) * max_x / (max_x - min_x) * n) / bh)
        if H[get_bin(xtm[0])] == 0:
            k += 1
            H[get_bin(xtm[0])] = 1
            if k > 1:
                Mx = (k - 1) / (2 * sigma) *\
                    (1 - 2 / (9 * (k - 1))\
                     + np.sqrt(2 / (9 * (k - 1))\
                        # delta is 0.25
                        * 0.675 * sigma) 
                     ) ** 3

        M += 1
    print(Mx)
    return (Xt, np.array(W))



if __name__ == "__main__":
    # KLD_MCL
    nx = [0, 0, 0]
    dt = 0.5
    ct = [[0.5, 0.5, 0], [0.7, 0.2, 0], [0.2, 0.6, 0]]
    n = 20
    Xt = 2.0 * np.array([(x, y, 0) for x in np.arange(0,n)
        for y in np.arange(0,n)]) / n - 1.0
    W = np.ones(Xt.shape[0])
    W /= W.sum()
    n = len(Xt)

    min_x = np.min(Xt)
    max_x = np.max(Xt)
    for i, ut in enumerate([[-1., 1.], [-0.5, -0.5], [-0.1, -0.2]]):
        nx = get_next_pos(nx, ut, dt)
        if i:
            Xt, W = KLD_MCL(Xt, W, ut, ct, dt, nx, n, 0.05, -1, 1)
            W /= W.sum()
        else: # do normal MCL the first time through
            Xt, W = MCL(Xt, ut, ct, dt, nx, n)
            W /= W.sum()

        figure, axis = plt.subplots(1, 2)
        axis[0].hist([x[0] for x in Xt], range=[min_x, max_x], bins=50)
        axis[1].hist([x[1] for x in Xt], range=[min_x, max_x], bins=50)
        print(nx, len(Xt))
        plt.show()
        plt.scatter([x[0] + 0.01 * np.random.randn() for x in Xt], [x[1] + 0.01 * np.random.randn() for x in Xt])
        plt.show()

    #%%
    # MCL
    nx = [0, 0, 0]
    dt = 0.5
    ct = [[0.5, 0.5, 0], [0.7, 0.2, 0], [0.2, 0.6, 0]]
    n = 20
    Xt = 2.0 * np.array([(x, y, 0) for x in np.arange(0,n)
        for y in np.arange(0,n)]) / n - 1.0
    n = len(Xt)

    min_x = np.min(Xt)
    max_x = np.max(Xt)
    for ut in [[-1., 1.], [-0.5, -0.5], [-0.1, -0.2]]:
        nx = get_next_pos(nx, ut, dt)
        Xt, _ = MCL(Xt, ut, ct, dt, nx, n)

        figure, axis = plt.subplots(1, 2)
        axis[0].hist([x[0] for x in Xt], range=[min_x, max_x], bins=50)
        axis[1].hist([x[1] for x in Xt], range=[min_x, max_x], bins=50)
        print(nx)
        plt.show()
        plt.scatter([x[0] + 0.01 * np.random.randn() for x in Xt], [x[1] + 0.01 * np.random.randn() for x in Xt])
        plt.show()


    #%%
    # MCL Augmented
    nx = [0, 0, 0]
    dt = 0.5
    ct = [[0.5, 0.5, 0], [0.7, 0.2, 0], [0.2, 0.6, 0]]

    n = 20
    Xt = 2.0 * np.array([(x, y, 0) for x in np.arange(0,n)
        for y in np.arange(0,n)]) / n - 1.0
    n = len(Xt)

    min_x = np.min(Xt)
    max_x = np.max(Xt)
    for ut in [[-1., 1.], [-0.5, -0.5], [-0.1, -0.2]]:
        nx = get_next_pos(nx, ut, dt)
        Xt = MCL_aug(Xt, ut, ct, dt, nx, n)

        figure, axis = plt.subplots(1, 2)
        axis[0].hist([x[0] for x in Xt], range=[min_x, max_x], bins=50)
        axis[1].hist([x[1] for x in Xt], range=[min_x, max_x], bins=50)
        print(nx)
        plt.show()
        plt.scatter([x[0] + 0.01 * np.random.randn() for x in Xt], [x[1] + 0.01 * np.random.randn() for x in Xt])
        plt.show()

    #%%
    # grid_localization
    nx = [0, 0, 0]
    ut = [-1., 1.]
    dt = 0.5

    n = 20
    ct = [[0.5, 0.5, 0], [0.7, 0.2, 0], [0.2, 0.6, 0]]
    p = np.ones(n * n) / n ** 2
    Xt = 2.0 * np.array([(x, y, 0) for x in np.arange(0,n)
        for y in np.arange(0,n)]) / n - 1.0

    plt.imshow(p.reshape((n, n)), 
        extent=[Xt.min(), Xt.max(), Xt.max(), Xt.min()])
    plt.show()

    for ut in [[1., 1.], [-0.5, -0.5], [-0.1, -0.2]]:
        nx = get_next_pos(nx, ut, dt)
        p = grid_localization(p, ut, ct, Xt, dt, nx)
        plt.imshow(p.reshape((n, n)), 
            extent=[Xt.min(), Xt.max(), Xt.max(), Xt.min()])
        print(nx)
        plt.show()

# %%
