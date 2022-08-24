#%%
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

    return prob(v - v_hat, 0.001)\
        * prob(w - w_hat, 0.001)\
        * prob(gamma_hat, 0.001)


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

def grid_localization(p, ut, zt, Xt, dt):
    
    for k in range(len(Xt)):
        for i in range(len(Xt)):
            mv = motion_model_vel(Xt[k], ut, Xt[i], dt)
            if np.isnan(mv) : continue
            #print(mv)
            p[k] += p[i] * mv
        print(p[k])
    return p
        

n = 50
p = np.ones((n, n)) / n ** 2
plt.imshow(p)

Xt = np.array([(x, y, 0) for x in np.arange(0,n)
    for y in np.arange(0,n)])
p = grid_localization(p.reshape(-1,1), [1, 1], [], Xt, 5)
print(p)
# %%
class localization():
    """Performing Bayesian Updating to Produce a Distribution of Likely Positions in the Environment"""

    def __init__(self, colours, measurements, motions, sensor_right, p_move):
        self.world = colours
        self.measurements = measurements
        self.motions = motions
        self.sensor_right = sensor_right
        self.p_move = p_move

        # Initialate Uniform Prior
        pinit = 1.0 / float(len(colours)) / float(len(colours[0]))
        self.p = [[pinit for row in range(len(colours[0]))] for col in range(len(colours))]

    def sense(self, p, world, measurement):
        """Compute probabilities after sensing the world (with some confidence)"""
        q = [[0.0 for row in range(len(world[0]))] for col in range(len(world))]

        s = 0.0
        for i in range(len(p)):
            for j in range(len(p[i])):
                hit = (measurement == world[i][j])
                q[i][j] = p[i][j] * (hit * self.sensor_right + (1-hit)*(1-self.sensor_right))
                s += q[i][j]

        # normalize
        for i in range(len(q)):
            for j in range(len(p[0])):
                q[i][j] /= s

        return q


    def move(self, p, motion):
        """Compute probabilities after moving through world (with some confidence)"""
        q = [[0.0 for row in range(len(self.world[0]))] for col in range(len(self.world))]

        for i in range(len(p)):
            for j in range(len(p[0])):
                q[i][j] = (self.p_move * p[(i-motion[0]) % len(p)][(j-motion[1]) % len(p[i])]) + ((1-self.p_move) * p[i][j])
        return q


    def compute_posterior(self):
        """Call Computation"""
        p = self.p
        for i in range(len(self.measurements)):
            p = self.move(p, self.motions[i])
            p = self.sense(p, self.world, self.measurements[i])

        return p


    def show(self, p):
        rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
        print('[' + ',\n '.join(rows) + ']')
        

colours = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

localization = localization(colours=colours, measurements=measurements, motions=motions, sensor_right=0.7, p_move=0.8)
posterior = localization.compute_posterior()
localization.show(posterior)
# %%
