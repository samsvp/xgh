import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Wedge

from typing import *


radius = .5

world_bounds = [-20, 20]



def animate(true_states, pose_particles, markers, lm_pred_uncertainty, 
    lm_pred_locs, fov):
    mu_x = [np.mean(pose_particles[0,:,i]) for i in range(pose_particles.shape[2])]
    mu_y = [np.mean(pose_particles[1,:,i]) for i in range(pose_particles.shape[2])]
    
    x_tr, y_tr, th_tr = true_states
    fov_bound = np.deg2rad(fov)/2

    lm_pred_x = lm_pred_locs[0]
    lm_pred_y = lm_pred_locs[1]
    
    radius = .5
    
    fig = plt.figure()

    ax = plt.axes(xlim=world_bounds, ylim=world_bounds)
    ax.set_title("Fast Slam")
    ax.set_aspect('equal')
    ax.plot(markers[0], markers[1], '+', color="k", label="Landmarks")

    actual_path, = ax.plot([], [], color='b', label="True")
    pred_path, = ax.plot([], [], color='r', label="Predicted")
    heading, = ax.plot([], [], color="k")

    particles, = ax.plot([], [], '.', color='b')

    robot = plt.Circle((x_tr[0], y_tr[0]), radius=radius, color=(0, 0, 1, .5), ec="k")
    pred_robot = plt.Circle((mu_x[0], mu_y[0]), radius=radius, color=(1, 0, 0, .5), ec="k")

    ax.add_artist(robot)
    ax.add_artist(pred_robot)

    landmark_unc = [ax.plot([], [], color=(0.0, 0, 0.5))[0] for i in range(len(markers[0]))]

    vision_beam = Wedge((x_tr[0],y_tr[0]), 1000, np.rad2deg(th_tr[0] - fov_bound), 
        np.rad2deg(th_tr[0] + fov_bound), zorder=-5, alpha=.1, color='m')

    ax.add_artist(vision_beam)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    def init():
        actual_path.set_data([], [])
        pred_path.set_data([], [])
        heading.set_data([], [])
        particles.set_data([], [])
        return (actual_path, pred_path, heading, particles, 
            robot, pred_robot, vision_beam, *landmark_unc)


    def animate(i):
        # landmarks
        for j in range(len(landmark_unc)):
            x_lm = lm_pred_x[j,i]
            y_lm = lm_pred_y[j,i]

            # haven't seen landmark yet
            if (x_lm == 0) and (y_lm == 0):
                continue
            
            # create confidence ellipse
            U, S, _ = np.linalg.svd(lm_pred_uncertainty[j][:,:,i])
            C = U * 2*np.sqrt(S)
            theta = np.linspace(0, 2*np.pi, 100)
            circle = np.array([np.cos(theta), np.sin(theta)])
            e = C @ circle
            e[0,:] += x_lm
            e[1,:] += y_lm
            landmark_unc[j].set_data(e[0,:], e[1,:])
            

        actual_path.set_data(x_tr[:i+1], y_tr[:i+1])
        pred_path.set_data(mu_x[:i+1], mu_y[:i+1])

        heading.set_data([x_tr[i], x_tr[i] + radius*np.cos(th_tr[i])], 
            [y_tr[i], y_tr[i] + radius*np.sin(th_tr[i])])

        particles.set_data(pose_particles[0,:,i], pose_particles[1,:,i])

        robot.center = (x_tr[i],y_tr[i])
        pred_robot.center = (mu_x[i], mu_y[i])

        vision_beam.set_center((x_tr[i],y_tr[i]))
        vision_beam.theta1 = np.rad2deg(th_tr[i] - fov_bound)
        vision_beam.theta2 = np.rad2deg(th_tr[i] + fov_bound)

        return (actual_path, pred_path, heading, particles, 
            robot, pred_robot, vision_beam, *landmark_unc)


    anim = animation.FuncAnimation(fig, animate, init_func=init,
        frames=len(x_tr), interval=60, blit=True, repeat=False)
    
    plt.pause(.1)
    input("<Hit enter to close>")


def sample(b):
    return b / 6 * np.sum(
        [random.uniform(-1,1) for i in range(12)])


def get_next_pos(mu_l: np.ndarray, ut: np.ndarray, dt: float) -> np.ndarray:
    theta = mu_l[-1, 0]
    vt, wt = ut
    mut = mu_l + np.array([
        [-vt / wt * np.sin(theta) + vt/wt * np.sin(theta + wt * dt)],
        [vt / wt * np.cos(theta) - vt / wt * np.cos(theta + wt * dt)],
        [wt * dt]])
    return mut


def get_ft(ct, xt):
    xc, yc = ct
    x, y, theta = xt
    r = np.sqrt((xc - x)**2 + (yc - y)**2) + 0.01 * np.random.rand()
    phi = np.arctan2(yc - y, xc - x) - theta + 0.01 * np.random.rand()
    return np.array([[r], [phi]])


def sample_motion_model_vel(ut, xtm1, alphas, dt):
    v, w = ut
    x, y, theta = xtm1

    v_hat = v + sample(alphas[0]*v**2 + alphas[1]*w**2)
    w_hat = w + sample(alphas[2]*v**2 + alphas[3]*w**2)
    gamma_hat = sample(alphas[4]*v**2 + alphas[5]*w**2)

    x_line = x - v_hat / w_hat * np.sin(theta) + v_hat / w_hat * np.sin(theta + w_hat * dt)
    y_line = y + v_hat / w_hat * np.cos(theta) - v_hat / w_hat * np.cos(theta + w_hat * dt)
    theta_line = theta + w_hat * dt + gamma_hat * dt

    return np.array([[x_line], [y_line], [theta_line]])


def wrap(angle: float) -> float:
    return (angle + np.pi) % (2 * np.pi) - np.pi


def sample_p(p: np.ndarray, x: float) -> int:
    """
    Returns the index of a sample from the given distribution 
    'p' given a single value 'x' between 0 and 1
    """
    pp = 0
    for i, pi in enumerate(p):
        if x < pp: return i
        pp += pi
    return p.shape[0] - 1


def sample_particles(chi: np.ndarray, lm_x_locs: np.ndarray, 
        lm_y_locs: np.ndarray, lm_sigmas: np.ndarray) -> \
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    new_particles = np.zeros( (chi.shape[0]-1,chi.shape[1]) )
    
    new_x_lm_locs = np.zeros(lm_x_locs.shape)
    new_y_lm_locs = np.zeros(lm_y_locs.shape)
    new_lm_sigmas = np.zeros(lm_sigmas.shape)

    M = chi.shape[1]
    r = random.uniform(0, 1/M)
    for m in range(M):
        U = r + m * (1/M)
        i = sample_p(chi[-1,:], U)
        new_particles[:,m] = chi[:-1,i]
        new_x_lm_locs[:,m] = lm_x_locs[:,i]
        new_y_lm_locs[:,m] = lm_y_locs[:,i]
        p_new, p_old = 2*m, 2*i
        new_lm_sigmas[:,p_new:p_new+2] = lm_sigmas[:,p_old:p_old+2]

    return new_particles, new_x_lm_locs, new_y_lm_locs, new_lm_sigmas


def get_avg_uncertainty(lm_uncertainty_matrix):
    avgs = []
    for lm in range(0,lm_uncertainty_matrix.shape[0],2):
        total = np.zeros((2,2))
        for p in range(0,lm_uncertainty_matrix.shape[1],2):
            total += lm_uncertainty_matrix[lm:lm+2 , p:p+2]
        total /= lm_uncertainty_matrix.shape[1]/2
        avgs.append(total)
    return avgs


def fast_slam(chi_bar_t: np.ndarray, particle_poses: np.ndarray,
    v_c: float, w_c: float, xt: np.ndarray, alphas:np.ndarray,
    seen_lm: np.ndarray, dt: float) -> np.ndarray:

    uv = v_c + \
        np.random.normal(scale=np.sqrt( (alphas[0]*(v_c**2)) + (alphas[1]*(w_c**2)) ))
    uw = w_c + \
        np.random.normal(scale=np.sqrt( (alphas[2]*(v_c**2)) + (alphas[3]*(w_c**2)) ))
    u_t = np.array([[uv], [uw]])
    for k in range(num_particles):
        prev_state = particle_poses[:,k].reshape(-1,1)
        
        next_state = sample_motion_model_vel(u_t, prev_state, alphas, dt)
        chi_bar_t[0,k] = next_state[0,0]
        chi_bar_t[1,k] = next_state[1,0]
        chi_bar_t[2,k] = next_state[2,0]

        weight = 1
        for lm_i in range(n_ldm):
            bel_x = chi_bar_t[0,k]
            bel_y = chi_bar_t[1,k]
            bel_theta = chi_bar_t[2,k]

            z_true = get_ft(landmarks[:, lm_i], xt)

            # make sure the landmark is in the field of view (bearing vs FOV)
            if np.abs(wrap(z_true[1,0])) > perception_bound:
                continue

            if not seen_lm[lm_i, k]:
                seen_lm[lm_i, k] = True
                # initialize mean
                r = z_true[0,0]
                bearing = z_true[1,0]
                lm_x_bar = bel_x + (r * np.cos(bearing + bel_theta))
                lm_y_bar = bel_y + (r * np.sin(bearing + bel_theta))
                ldm_loc_est_x[lm_i,k] = lm_x_bar
                ldm_loc_est_y[lm_i,k] = lm_y_bar
                # calculate jacobian
                diff_x = lm_x_bar - bel_x
                diff_y = lm_y_bar - bel_y
                H_t = np.array([
                    [r*diff_x, r*diff_y],
                    [-diff_y, diff_x]
                ])
                H_t *= 1 / (r*r)
                # initialize covariance
                H_inv = np.linalg.pinv(H_t)
                sigma = H_inv @ Qt @ H_inv.T
                lm_sig_i = 2*lm_i
                p_sig_i = 2*k
                ldm_unc[lm_sig_i:lm_sig_i+2 , p_sig_i:p_sig_i+2] = sigma
                # default importance weight
                weight *= p0
            else:
                # measurement prediction
                lm_x_bar = ldm_loc_est_x[lm_i,k]
                lm_y_bar = ldm_loc_est_y[lm_i,k]
                diff_x = lm_x_bar - bel_x
                diff_y = lm_y_bar - bel_y
                q = (diff_x * diff_x) + (diff_y * diff_y)
                r = np.sqrt(q)
                bearing = np.arctan2(diff_y,diff_x) - bel_theta
                z_hat = np.array([[r], [bearing]])
                # calculate jacobian
                diff_x = lm_x_bar - bel_x
                diff_y = lm_y_bar - bel_y
                H_t = np.array([
                    [r*diff_x, r*diff_y],
                    [-diff_y, diff_x]
                ]) / r ** 2

                # measurement covariance
                lm_sig_i = 2*lm_i
                p_sig_i = 2*k
                prev_sig = ldm_unc[lm_sig_i:lm_sig_i+2 , p_sig_i:p_sig_i+2]
                Q_t = H_t @ prev_sig @ H_t.T + Qt
                # calculate kalman gain
                K_t = prev_sig @ H_t.T @ np.linalg.pinv(Q_t)
                # update mean
                z_diff = z_true - z_hat
                z_diff[1,0] = wrap(z_diff[1,0])
                mu_lm = np.array([lm_x_bar,lm_y_bar]).reshape(z_diff.shape) + \
                    K_t @ z_diff
                ldm_loc_est_x[lm_i,k] = mu_lm[0,0]
                ldm_loc_est_y[lm_i,k] = mu_lm[1,0]
                # update covariance
                temp = np.identity(K_t.shape[0]) - K_t @ H_t
                sigma = temp @ prev_sig
                ldm_unc[lm_sig_i:lm_sig_i+2 , p_sig_i:p_sig_i+2] = sigma
                # importance factor
                w_a = np.linalg.det(2 * np.pi * Q_t) ** -.5
                w_b = -.5*z_diff.T @ np.linalg.pinv(Q_t) @ z_diff
                w_b = np.exp(w_b).item(0)
                weight *= w_a * w_b

        chi_bar_t[-1,k] = weight

    # normalize weights
    chi_bar_t[-1,:] /= np.sum(chi_bar_t[-1,:])
    return chi_bar_t



if __name__ == "__main__":
    dt = .1
    total_time = 30 # seconds
    t = np.arange(0, total_time+dt, dt)

    np.random.seed(None)

    # std deviation of range and bearing sensor noise for each landmark
    std_dev_range = .1
    std_dev_bearing = .05
    
    # number of landmarks
    n_ldm = 10
    landmarks = np.random.randint(low=world_bounds[0]+1, 
        high=world_bounds[1], size=(2,n_ldm))
    lm_x = landmarks[0,:]
    lm_y = landmarks[1,:]

    # uncertainty due to measurement noise
    Qt = np.array([
        [(std_dev_range * std_dev_range), 0],
        [0, (std_dev_bearing * std_dev_bearing)]
    ])

    # particles for MCL
    num_particles = 50

    # default importance weight
    p0 = 1 / num_particles

    # (put None as first parameter so that indexing matches alpha name)
    alphas = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

    v_c = 1 + (.5 * np.sin(2*np.pi*.2*t))
    w_c = -.2 + (2 * np.cos(2*np.pi*.6*t))

    # control inputs
    v = v_c + np.random.normal(scale=np.sqrt( 
        (alphas[0]*(v_c**2)) + (alphas[1]*(w_c**2)) ))
    w = w_c + np.random.normal(scale=np.sqrt( 
        (alphas[2]*(v_c**2)) + (alphas[3]*(w_c**2)) ))

    # ground truth states
    x_pos_true = np.zeros(t.shape)
    y_pos_true = np.zeros(t.shape)
    theta_true = np.zeros(t.shape)  # radians

    x_pos_true[0] = 0
    y_pos_true[0] = 0
    theta_true[0] = np.pi / 2

    for ts in range(1, t.size):
        # get previous ground truth state
        prev_state = np.array([[x_pos_true[ts-1]], [y_pos_true[ts-1]], [theta_true[ts-1]]])

        # get next ground truth state unp.sing previous ground truth state
        # and next ground truth input
        next_state = get_next_pos(prev_state, [v[ts], w[ts]], dt)

        x_pos_true[ts] = next_state[0,0]
        y_pos_true[ts] = next_state[1,0]
        theta_true[ts] = next_state[2,0]

    # generate particles
    p_poses = np.zeros((3,num_particles,t.size))
    p_poses[0,:,0] = x_pos_true[0]
    p_poses[1,:,0] = y_pos_true[0]
    p_poses[2,:,0] = theta_true[0]

    ldm_unc = np.zeros((2*n_ldm,2*num_particles))
    lm_unc_hist = {k: np.zeros((2,2,t.size)) for k in range(n_ldm)}

    # landmark location estimates (current time)
    ldm_loc_est_x = np.zeros((n_ldm, num_particles))
    ldm_loc_est_y = np.zeros((n_ldm, num_particles))

    # landmark locations over all times (avg of all particle location estimates)
    all_lm_loc_estimates_x = np.zeros((n_ldm, t.size))
    all_lm_loc_estimates_y = np.zeros((n_ldm, t.size))

    # seen landmarks for each particle
    seen_lm = np.zeros((n_ldm, num_particles), dtype=bool)

    FOV = 60
    perception_bound = np.deg2rad(FOV / 2)
    for ts in range(1,t.size):
        # next state/evolution of particles
        # extra row for chi_bar_t is the weight of each particle
        chi_bar_t = np.zeros((p_poses.shape[0]+1,p_poses.shape[1]))

        chi_bar_t = fast_slam(chi_bar_t, p_poses[...,ts-1], v_c[ts], w_c[ts], 
            [x_pos_true[ts], y_pos_true[ts], theta_true[ts]], alphas, 
            seen_lm, dt)

        # resample, factoring in the weights
        p_poses[:,:,ts], ldm_loc_est_x, ldm_loc_est_y, ldm_unc = sample_particles(
            chi_bar_t, ldm_loc_est_x, ldm_loc_est_y, ldm_unc)

        # save average lm uncertanty and location of all particles
        avg_uncertainty = get_avg_uncertainty(ldm_unc)
        for k in range(n_ldm):
            lm_unc_hist[k][:,:,ts] = avg_uncertainty[k]
            all_lm_loc_estimates_x[k,ts] = np.mean(ldm_loc_est_x[k,:])
            all_lm_loc_estimates_y[k,ts] = np.mean(ldm_loc_est_y[k,:])


    animate((x_pos_true, y_pos_true, theta_true), p_poses, (lm_x, lm_y),
        lm_unc_hist, (all_lm_loc_estimates_x, all_lm_loc_estimates_y), FOV)
