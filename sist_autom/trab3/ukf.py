#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import sqrtm
import conf_ellipse as ce

def get_z(pos: np.ndarray, ct) -> np.ndarray:
    q = (ct[0] - pos[0]) ** 2 + (ct[1] - pos[1]) ** 2
    zt = np.array([
        np.sqrt(q),
        np.arctan2(ct[1] - pos[1], ct[0] - pos[0]) - pos[2],
        ct[2]
    ])
    return zt


def get_Mt(vt: float, wt: float, alphas: np.ndarray) -> np.ndarray:
    return np.array([
        [alphas[0] * vt ** 2 + alphas[1] * wt ** 2, 0],
        [0, alphas[2] * vt ** 2 + alphas[3] * wt ** 2]
    ])


def get_sigma_aug(sigma: np.ndarray, M_t: np.ndarray, Q_t: np.ndarray) -> np.ndarray:
    sig_a = np.zeros((7,7))
    sig_a[0:3,0:3] = sigma
    sig_a[3:5,3:5] = M_t
    sig_a[5: ,5: ] = Q_t
    return sig_a


def get_movement(ut, theta, dt):
    vt, wt = ut

    move_forward = np.array([
        -vt / wt * np.sin(theta) + vt/wt * np.sin(theta + wt * dt),
        vt / wt * np.cos(theta) - vt / wt * np.cos(theta + wt * dt),
        wt * dt])

    return move_forward


def get_chi_aug(mu_a: np.ndarray, sigma_a: np.ndarray, g: float) -> np.ndarray:
    chi_a = np.zeros((7,15))
    chi_a[:,0] = mu_a
    mat_sq_root = g * np.linalg.cholesky(sigma_a)
    chi_a[:,1:8] = mu_a + mat_sq_root
    chi_a[:,8:] = mu_a - mat_sq_root
    return chi_a


def get_weights(alpha: float, beta: float, lmbda: float, L: int):
    weights_mean = np.zeros(15)
    weights_mean[0] = lmbda / (L + lmbda)
    weights_covar = np.zeros(15)
    weights_covar[0] = weights_mean[0] + (1 - (alpha * alpha) + beta)
    val = 1 / ( 2 * (L + lmbda) )
    weights_mean[1:] = val
    weights_covar[1:] = val
    return weights_mean, weights_covar


def g(ut: np.ndarray, chi_a: np.ndarray, dt: float) -> np.ndarray:
    vt, wt = ut
    chi_b_x = np.zeros((3,15))
    for pt in range(chi_b_x.shape[1]):
        # (get new input based on original input and sampled inputs)
        v_new = chi_a[3,pt] + vt
        om_new = chi_a[4,pt] + wt
        theta = chi_a[2,pt]
        # (save how model propogates forward with new input)
        forward_input = get_movement([v_new, om_new], theta, dt)
        # (save new state based on propogation and previously sampled state)
        chi_b_x[:,pt] = chi_a[0:3,pt] + forward_input
    return chi_b_x


def get_sigma_t(wc, mu_t, chi_a_x):
    new_sig = np.zeros((3, 3))
    for i in range(len(wc)):
        state_diff = (chi_a_x[:,i] - mu_t).reshape(-1, 1)
        new_sig += wc[i] * state_diff @ state_diff.T
    return new_sig



def ukf_localization(mu_l: np.ndarray, sigma_l: np.ndarray, 
        ut: np.ndarray, zt: np.ndarray, ct: np.ndarray, 
        dt: float, alphas: np.ndarray) -> \
            np.array:
    """
    Ukf localization where you have only one feature zt and its match ct.
    Parameters
    mu: gaussian estimate of the robot pose at time t-1
    sigma: gaussian covariance matrix of the robot pose at time t-1
    ut: current control signal
    zt: current feature measurement
    ct: feature corresponding to zt
    m: map
    dt: time passed since the last measurement
    alphas: noise constants
    """
    theta = mu_l[-1]
    vt, wt = ut

    M_t = get_Mt(vt, wt, alphas)
    Q_t = np.array([[0.001, 0], [0, 0.00001]])

    # generate augmented mu and sigma
    mu_a = np.array([mu_l[0], mu_l[1], mu_l[2],
        0, 0, 0, 0])
    sigma_a = get_sigma_aug(sigma_l, M_t, Q_t)

    L = mu_a.shape[0]
    two_L_bound = (2*L) + 1

    # (ut parameters)
    # unscented transform params
    ut_alpha = .4
    k = 4
    beta = 2

    lmbda = ((ut_alpha * ut_alpha) * (L + k)) - L
    gamma = np.sqrt(L + lmbda)
    # generate sigma points
    chi_a = get_chi_aug(mu_a, sigma_a, gamma)

    # pass sigma points through motion model and compute Gaussian statistics
    chi_a_x = g(ut, chi_a, dt)
    wm, wc = get_weights(ut_alpha, beta, lmbda, L)
    mu_t = (wm * chi_a_x).sum(axis=1)
    sigma_t = get_sigma_t(wc, mu_t, chi_a_x) # line 9 of the algorithm
    # line 223 of the git code
    
    return chi_a_x, wm, wc



ct = np.array([0, 0, 0])
m = []
dt = 1
alphas = [0.001, 0.001, 0.001, 0.001]
cov = 1. * np.eye(3)
cov_u = cov
ut = [1, 1]
mut = [0, 0, 0]
zt = get_z(mut, ct)
chi_a_x, wm, wc = ukf_localization(mut, cov_u, ut, zt, ct, dt, alphas)



# %%
