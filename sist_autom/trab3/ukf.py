#%%
import matplotlib.pyplot as plt
import numpy as np
from numpy import matmul as mm
from numpy.linalg import inv as mat_inv
import conf_ellipse as ce


def get_fwd_propogation(vt, wt, theta, dt):    
    move_forward = np.array([
        [-vt/wt * np.sin(theta) + vt/wt * np.sin(theta + (wt*dt))],
        [vt/wt * np.cos(theta) - vt/wt * np.cos(theta + (wt*dt))],
        [wt * dt]
    ])

    return move_forward


def get_mu_t_a(state_vec):
    mu_t_a = np.zeros((7,1))
    mu_t_a[0:3,0] = state_vec[:,0]
    return mu_t_a


def get_sigma_a(sigma, m, q):
    sig_a = np.zeros((7,7))
    sig_a[0:3,0:3] = sigma
    sig_a[3:5,3:5] = m
    sig_a[5: ,5: ] = q
    return sig_a


def get_chi_a(mu_a, sigma_a, gamma):
    chi_a = np.zeros((7,15))
    chi_a[:,0] = mu_a[:,0]
    mat_sq_root = gamma * np.linalg.cholesky(sigma_a)
    chi_a[:,1:8] = mu_a + mat_sq_root
    chi_a[:,8:] = mu_a - mat_sq_root
    return chi_a


def get_chi_bar_x(v, om, augmented_chi):
    chi_b_x = np.zeros((3,15))
    for pt in range(chi_b_x.shape[1]):
        # (get new input based on original input and sampled inputs)
        v_new = augmented_chi[3,pt] + v
        om_new = augmented_chi[4,pt] + om
        angle = augmented_chi[2,pt]
        # (save how model propogates forward with new input)
        forward_input = get_fwd_propogation(v_new, om_new, angle, dt)
        # (save new state based on propogation and previously sampled state)
        chi_b_x[:,pt] = augmented_chi[0:3,pt] + forward_input[:,0]
    return chi_b_x


def get_mean_and_covar_weights(alpha, beta, lmbda, L):
    # a = alpha, b = beta, dimensionality = L
    weights_mean = np.zeros((1,15))
    weights_mean[0,0] = lmbda / (L + lmbda)
    weights_covar = np.zeros((1,15))
    weights_covar[0,0] = weights_mean[0,0] + (1 - (alpha * alpha) + beta)
    val = 1 / ( 2 * (L + lmbda) )
    weights_mean[0,1:] = val
    weights_covar[0,1:] = val
    return weights_mean, weights_covar


def get_mu_and_sig_bar(dimensionality_bound, w_m, w_c, chi_b_x):
    new_bel = np.zeros((3,1))
    for pt in range(dimensionality_bound):
        new_bel += w_m[0,pt] * np.reshape(chi_b_x[:,pt], new_bel.shape)

    new_sig = np.zeros((3,3))
    for pt in range(dimensionality_bound):
        state_diff = np.reshape(chi_b_x[:,pt], new_bel.shape) - new_bel
        new_sig += w_c[0,pt] * mm(state_diff, np.transpose(state_diff))

    return new_bel, new_sig


def ukf(mu_l: np.ndarray, sigma: np.ndarray, 
        zts: np.ndarray, u_t: np.ndarray, cts: np.ndarray) -> np.ndarray:
    
    mu = mu_l.reshape(-1, 1)

    # control inputs
    vt, wt = u_t

    M_t = np.array([
        [(alphas[0] * vt * vt) + (alphas[1] * wt * wt), 0],
        [0, (alphas[2] * vt * vt) + (alphas[3] * wt * wt)]
    ])

    for i in range(len(cts)):
        mx, my = cts[i]
        zt = zts[i]

        # generate augmented mean and covariance
        mu_t_a = get_mu_t_a(mu)
        sigma_a = get_sigma_a(sigma, M_t, Q_t)
        # (save dimensionality for later)
        L = mu_t_a.shape[0]
        two_L_bound = (2*L) + 1
        # (ut parameters)
        lmbda = ((ut_alpha * ut_alpha) * (L + kappa)) - L
        gamma = np.sqrt(L + lmbda)

        # generate sigma points
        chi_aug = get_chi_a(mu_t_a, sigma_a, gamma)

        # pass sigma points through motion model and compute gaussian statistics
        chi_bar_x = get_chi_bar_x(vt, wt, chi_aug)
        weights_m, weights_c = get_mean_and_covar_weights(ut_alpha, beta, lmbda, L)
        mu_bar, sigma_bar = \
            get_mu_and_sig_bar(two_L_bound, weights_m, weights_c, chi_bar_x)

        # predict observations at sigma points and compute gaussian statistics
        Z_bar_t = np.zeros((2,15))
        for pt in range(Z_bar_t.shape[1]):
            bel_x = chi_bar_x[0,pt]
            bel_y = chi_bar_x[1,pt]
            bel_theta = chi_bar_x[2,pt]
            x_diff = mx - bel_x
            y_diff = my - bel_y
            q = ( x_diff * x_diff ) + ( y_diff * y_diff )
            Z_bar_t[0,pt] = np.sqrt(q)
            Z_bar_t[1,pt] = np.arctan2(y_diff, x_diff) - bel_theta
        Z_bar_t += chi_aug[-2:,:]
        z_hat = np.zeros((2,1))
        for pt in range(two_L_bound):
            z_hat += weights_m[0,pt] * np.reshape(Z_bar_t[:,pt], z_hat.shape)
        S_t = np.zeros((2,2))
        for pt in range(two_L_bound):
            meas_diff = np.reshape(Z_bar_t[:,pt], z_hat.shape) - z_hat
            S_t += weights_c[0,pt] * mm(meas_diff, np.transpose(meas_diff))
        sigma_t = np.zeros((3,2))
        for pt in range(two_L_bound):
            state_diff = np.reshape(chi_bar_x[:,pt], mu_bar.shape) - mu_bar
            meas_diff = np.reshape(Z_bar_t[:,pt], z_hat.shape) - z_hat
            sigma_t += weights_c[0,pt] * mm(state_diff, np.transpose(meas_diff))

        # update mean (belief) and covariance
        K_t = mm(sigma_t, mat_inv(S_t))
        mu = mu_bar + mm(K_t, zt - z_hat)
        sigma = sigma_bar - mm(K_t, mm(S_t, np.transpose(K_t)))

    return mu, sigma
        


if __name__ == "__main__":
    dt = .1
    t = np.arange(0, 10+dt, dt)

    # belief (estimates from EKF)
    mu_x = np.zeros(t.shape)
    mu_y = np.zeros(t.shape)
    mu_theta = np.zeros(t.shape)   # radians

    # noise in the command velocities (translational and rotational)
    alphas = [0.1, 0.01, 0.01, 0.1]

    # initial uncertainty in the belief
    sigma = 0.2 * np.array([
        [1, 0, 0],  # x
        [0, 1, 0],  # y
        [0, 0, .1]  # theta
    ])
    # unscented transform params
    ut_alpha = .4
    kappa = 4
    beta = 2
    ########################################################################################
    ########################################################################################

    # landmarks (x and y coordinates)
    ct = np.array([[6, 4], [10, 0], [0, 10]])

    # noise free inputs (NOT ground truth)
    v_c = 1 + (.5*np.sin(2*np.pi*.2*t))
    w_c = -.2 + (2*np.cos(2*np.pi*.6*t))

    # ground truth
    x_pos = np.zeros(t.shape)
    y_pos = np.zeros(t.shape)
    x_pos_true = np.zeros(t.shape)
    y_pos_true = np.zeros(t.shape)
    theta_true = np.zeros(t.shape)  # radians

    # control inputs (truth ... with noise)
    vt = v_c + np.random.normal(scale=np.sqrt( (alphas[0]*(v_c**2)) + (alphas[1]*(w_c**2)) ))
    wt = w_c + np.random.normal(scale=np.sqrt( (alphas[2]*(v_c**2)) + (alphas[3]*(w_c**2)) ))

    # uncertainty due to measurement noise
    Q_t = np.array([
        [(0.001), 0],
        [0, (0.00025)]
    ])

    # set ground truth data
    # make new ground truth data

    # robot has initial condition of position (-5,-3) and 90 degree orientation
    x_pos[0] = -5
    y_pos[0] = -3
    x_pos_true[0] = -5
    y_pos_true[0] = -3
    theta_true[0] = np.pi / 2

    # create my own ground truth states and input
    for timestep in range(1, t.size):
        # get previous ground truth state
        prev_state = np.array([x_pos_true[timestep-1], 
                                y_pos_true[timestep-1],
                                theta_true[timestep-1]])
        prev_state = np.reshape(prev_state, (-1,1))
        theta_prev = theta_true[timestep-1]

        # get next ground truth state using previous ground truth state
        # and next ground truth input
        next_state = prev_state + get_fwd_propogation(
                vt[timestep], wt[timestep], theta_prev, dt)
        x_pos_true[timestep] = next_state[0,0]
        y_pos_true[timestep] = next_state[1,0]
        theta_true[timestep] = next_state[2,0]

        # update non true labels
        prev_state = np.array([x_pos[timestep-1], 
                                y_pos[timestep-1],
                                theta_true[timestep-1]])
        prev_state = np.reshape(prev_state, (-1,1))
        theta_prev = theta_true[timestep-1]

        # get next ground truth state using previous ground truth state
        # and next ground truth input
        next_state = prev_state + get_fwd_propogation(
                v_c[timestep], w_c[timestep], theta_prev, dt)
        x_pos[timestep] = next_state[0,0]
        y_pos[timestep] = next_state[1,0]

    # needed for plotting kalman gains
    K_t = None # the kalman gain matrix that gets updated with measurements

    # run UKF
    sigmas = [sigma]
    mu_x[0] = x_pos_true[0]
    mu_y[0] = y_pos_true[0]
    mu_theta[0] = (np.pi / 2) - .05
    mu = np.array([x_pos_true[0], y_pos_true[0], mu_theta[0]])
    for t_step in range(1,t.size):
        u_t = [v_c[t_step], w_c[t_step]]

        # (get the true measurement for the given landmark)
        zts = []
        for _ct in ct:
            true_x = x_pos_true[t_step]
            true_y = y_pos_true[t_step]
            true_theta = theta_true[t_step]
            zt = np.zeros((2, 1))
            x_diff = _ct[0] - true_x
            y_diff = _ct[1] - true_y
            q = ( x_diff * x_diff ) + ( y_diff * y_diff )
            zt[0,0] = np.sqrt(q) + np.random.normal(scale=0.01)
            zt[1,0] = np.arctan2(y_diff, x_diff) - true_theta + np.random.normal(scale=0.05)
            zts.append(zt)


        mu, sigma = ukf(mu, sigma, zts,  u_t, ct)

        sigmas.append(sigma)

        # save belief, covariances
        mu_x[t_step] = mu[0 , 0]
        mu_y[t_step] = mu[1 , 0]
        mu_theta[t_step] = mu[2 , 0]


    ###############################################################################
    ###############################################################################
    # show plots and animation

    # plot the states over time
    fig, ax_nstd = plt.subplots(figsize=(6, 6))
    ax_nstd.plot(x_pos_true, y_pos_true, label="true")
    ax_nstd.plot(x_pos, y_pos, label="no ukf")
    ax_nstd.plot(mu_x, mu_y, "o--", label="predicted")
    ax_nstd.legend()

    for i in range(1, len(sigmas)):
        mean = [mu_x[i], mu_y[i]]
        ce.cconfidence_ellipse(mean, sigmas[i], 
            ax_nstd, n_std=1, edgecolor='firebrick')
        ce.cconfidence_ellipse(mean, sigmas[i], 
            ax_nstd, n_std=2, edgecolor='fuchsia')
        ce.cconfidence_ellipse(mean, sigmas[i], 
            ax_nstd, n_std=3, edgecolor='blue')

    plt.savefig("ukf.png")
    plt.show()

    plt.title("X-axis error")
    plt.plot(x_pos_true - mu_x, label="ukf")
    plt.plot(x_pos_true - x_pos, label="no ukf")
    plt.plot(x_pos_true - x_pos_true, "b--")
    plt.legend()

    plt.savefig("ukf_error_x.png")
    plt.show()


    plt.title("Y-axis error")
    plt.plot(y_pos_true - mu_y, label="ukf")
    plt.plot(y_pos_true - y_pos, label="no ukf")
    plt.plot(y_pos_true - y_pos_true, "b--")
    plt.legend()

    plt.savefig("ukf_error_y.png")
    plt.show()
# %%
