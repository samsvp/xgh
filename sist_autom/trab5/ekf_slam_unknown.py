#%%
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Wedge


from typing import *


world_bounds = [-20, 20]


def animate(true_states, belief_states, markers, uncertanties, fov):
    x_tr, y_tr, th_tr = true_states
    x_bl, y_bl, th_bl = belief_states[:3, :]
    fov_bound = np.deg2rad(fov)/2
    
    radius = .5
    
    fig = plt.figure()

    ax = plt.axes(xlim=world_bounds, ylim=world_bounds)
    ax.set_title("EKF Slam Unknown corr")
    ax.set_aspect('equal')
    ax.plot(markers[0], markers[1], '+', color="k", label="Landmarks")

    actual_path, = ax.plot([], [], color='b', label="True")
    pred_path, = ax.plot([], [], color='r', label="Predicted")
    heading, = ax.plot([], [], color="k")
    pred_heading, = ax.plot([], [], color="k")

    robot = plt.Circle((x_tr[0], y_tr[0]), radius=radius, color=(0, 0, 1, .5), ec="k")
    pred_robot = plt.Circle((x_bl[0], y_bl[0]), radius=radius, color=(1, 0, 0, .5), ec="k")
    
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
        return (actual_path, pred_path, heading, pred_heading, 
            robot, pred_robot, vision_beam) + tuple(landmark_unc)


    def animate(i):
        # landmarks
        for j in range(len(landmark_unc)):
            lm_idx = 3 + (2*j)
            x_lm = belief_states[lm_idx,i]
            y_lm = belief_states[lm_idx+1,i]

            # haven't seen landmark yet
            if (x_lm == 0) and (y_lm == 0):
                continue
            
            # create confidence ellipse
            U, S, _ = np.linalg.svd(uncertanties[lm_idx:lm_idx+2, lm_idx:lm_idx+2, i])
            C = U * 2*np.sqrt(S)
            theta = np.linspace(0, 2*np.pi, 100)
            circle = np.array([np.cos(theta), np.sin(theta)])
            e = C @ circle
            e[0,:] += x_lm
            e[1,:] += y_lm
            landmark_unc[j].set_data(e[0,:], e[1,:])

        actual_path.set_data(x_tr[:i+1], y_tr[:i+1])
        pred_path.set_data(belief_states[0,:i+1], belief_states[1,:i+1])

        heading.set_data([x_tr[i], x_tr[i] + radius * np.cos(th_tr[i])], 
            [y_tr[i], y_tr[i] + radius * np.sin(th_tr[i])])
        pred_heading.set_data([x_bl[i], x_bl[i] + radius * np.cos(th_bl[i])], 
            [y_bl[i], y_bl[i] + radius * np.sin(th_bl[i])])
        
        robot.center = (x_tr[i], y_tr[i])
        pred_robot.center = (x_bl[i], y_bl[i])
        
        vision_beam.set_center((x_tr[i],y_tr[i]))
        vision_beam.theta1 = np.rad2deg(th_tr[i] - fov_bound)
        vision_beam.theta2 = np.rad2deg(th_tr[i] + fov_bound)
        
        return (actual_path, pred_path, heading, pred_heading, 
            robot, pred_robot, vision_beam) + tuple(landmark_unc)


    anim = animation.FuncAnimation(fig, animate, init_func=init,
        frames=len(x_tr), interval=40, blit=True, repeat=False)
    
    plt.pause(.1)
    input("<Hit enter to close>")



def get_Gt(vt: float, wt: float, theta: float, 
        dt: float, Fx: np.ndarray) -> np.ndarray:
    _Gt = np.array([
        [0, 0, -vt/wt * np.cos(theta) + vt/wt * np.cos(theta + wt*dt)],
        [0, 0, -vt/wt * np.sin(theta) + vt/wt * np.sin(theta + wt*dt)],
        [0, 0, 0]
    ])
    return np.eye(Fx.shape[1]) + Fx.T @ _Gt @ Fx


def get_Mt(vt: float, wt: float, alphas: np.ndarray) -> np.ndarray:
    return np.array([
        [alphas[0] * vt ** 2 + alphas[1] * wt ** 2, 0],
        [0, alphas[2] * vt ** 2 + alphas[3] * wt ** 2]
    ])


def get_Vt(vt: float, wt: float, theta: float, 
        dt: float) -> np.ndarray:
    return np.array([
        [(-np.sin(theta) + np.sin(theta + wt*dt)) / wt, 
         vt*(np.sin(theta) - np.sin(theta + wt*dt)) / wt ** 2 + vt * np.cos(theta + wt*dt) * dt / wt],
        [(np.cos(theta) - np.cos(theta + wt * dt) / wt), 
         -vt * (np.cos(theta) - np.cos(theta + wt * dt)) / wt ** 2 + vt * np.sin(theta + wt * dt) * dt / wt],
        [0, dt]
    ])


def get_mu_bar(mu: np.ndarray, vt: float, wt: float, 
        theta: float, dt: float, 
        Fx: np.ndarray) -> np.ndarray:
    m = np.array([
        [(-vt / wt * np.sin(theta)) + (vt / wt * np.sin(theta + (wt * dt)))],
        [(vt / wt * np.cos(theta)) - (vt / wt * np.cos(theta + (wt * dt)))],
        [wt * dt]
    ])
    return mu + Fx.T @ m


def wrap(angle: float) -> float:
    # map angle between -pi and pi
    return (angle + np.pi) % (2 * np.pi) - np.pi


def noise(Qt: np.ndarray) -> np.ndarray:
    # assume distribution is zero-centered
    mnoise = np.random.multivariate_normal(
        np.zeros(Qt.shape[0]), Qt
    )
    return mnoise.reshape(-1,1)


def get_ft(ct, xt):
    xc, yc = ct
    x, y, theta = xt
    r = np.sqrt((xc - x)**2 + (yc - y)**2)
    phi = np.arctan2(yc - y, xc - x) - theta
    return np.array([r, phi])


def efk_slam(mu: np.ndarray, sigma: np.ndarray, vt: float, wt: float,
        true_x: np.ndarray, cts: np.ndarray, dt: float, Fx: np.ndarray,
        alphas: np.ndarray, Qt: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    prev_theta = mu[2,0]

    mu_bar = get_mu_bar(mu, vt, wt, prev_theta, dt, Fx)

    Gt = get_Gt(vt, wt, prev_theta, dt, Fx)

    Vt = get_Vt(vt, wt, prev_theta, dt) 
    Mt = get_Mt(vt, wt, alphas)
    Rt = Vt @ Mt @ Vt.T
    sigma_bar = Gt @ sigma @ Gt.T + Fx.T @ Rt @ Fx

    # correction (updating belief based on landmark readings)
    for j in range(cts.shape[0]):
        bel_x = mu_bar[0 , 0]
        bel_y = mu_bar[1 , 0]
        bel_theta = mu_bar[2 , 0]

        # get the sensor measurement
        z_true = get_ft(cts[j], true_x).reshape(-1,1)
        z_true += noise(Qt)

        # make sure the landmark is in the field of view (bearing vs FOV)
        if np.abs(wrap(z_true[1,0])) > perception_bound:
            continue

        pi_k = np.inf
        H_t = None
        phi_k = None
        z_hat = None

        if not seen_landmark[j]:
            r = z_true[0,0]
            bearing = z_true[1,0]
            lm_idx = 3 + (2*j)
            mu_bar[lm_idx, 0] = bel_x + (r * np.cos(bearing + bel_theta))     # lm_x_bar
            mu_bar[lm_idx + 1, 0] = bel_y + (r * np.sin(bearing + bel_theta)) # lm_y_bar
            
            seen_landmark[j] = True

        for k in range(cts.shape[0]):
            #if j != k: continue

            lm_idx = 3 + (2*k) # where we index the mu vector for the j'th landmark

            if not seen_landmark[k]:
                continue
            
            # diff_x, diff_y
            delta_x = mu_bar[lm_idx, 0] - bel_x
            delta_y = mu_bar[lm_idx + 1, 0] - bel_y
            
            q = delta_x ** 2 + delta_y ** 2

            _z_hat = np.array([
                [np.sqrt(q)],
                [np.arctan2(delta_y, delta_x) - bel_theta]
            ])
            
            F_x_j = np.zeros((5, pose_map_size))
            F_x_j[0:3,0:3] = np.identity(3)
            F_x_j[3:,lm_idx:lm_idx+2] = np.identity(2)

            sqrt_q = np.sqrt(q)
            x_sqrt = sqrt_q * delta_x
            y_sqrt = sqrt_q * delta_y
            dh = np.array([
                [-x_sqrt, -y_sqrt, 0, x_sqrt, y_sqrt],
                [delta_y, -delta_x, -q, -delta_y, delta_x]
            ])
            _H_t = (1 / q) * dh @ F_x_j

            _phi_k = _H_t @ sigma_bar @ _H_t.T + Qt
            _pi_k = (z_true - _z_hat).T @ np.linalg.pinv(_phi_k) @ (z_true - _z_hat)
            _pi_k = _pi_k[0][0]
            if _pi_k < pi_k:
                pi_k = _pi_k
                H_t = _H_t
                phi_k = _phi_k
                z_hat = _z_hat


        K_t = sigma_bar @ H_t.T @ np.linalg.pinv(phi_k)
        
        z_diff = z_true - z_hat
        z_diff[1,0] = wrap(z_diff[1,0])
        mu_bar = mu_bar + K_t @ z_diff
        
        sigma_bar = (np.eye(sigma_bar.shape[0]) - K_t @ H_t) @ sigma_bar

    return mu_bar, sigma_bar


if __name__ == "__main__":
    # landmarks (x and y coordinates)
    # np.random.seed(1) # robot gets lost
    np.random.seed(0)

    num_landmarks = 10
    world_markers = np.random.randint(low=world_bounds[0]+1, 
        high=world_bounds[1], size=(2,num_landmarks)).T

    seen_landmark = {}
    for i in range(num_landmarks):
        seen_landmark[i] = False

    # pose (x,y,theta) and landmarks (x,y)
    pose_map_size = 3 + (2*num_landmarks)

    dt = .1 
    total_time = 75 # seconds
    t = np.arange(0, total_time+dt, dt).reshape(1, -1)

    mu = np.zeros((pose_map_size, 1))

    alphas = [.01, .001, .001, .01]

    std_dev_range = .1
    std_dev_bearing = .05

    mu[0 , 0] = 0
    mu[1 , 0] = 0
    mu[2 , 0] = np.pi / 2

    sigma = np.identity(pose_map_size) * 5000
    sigma[0,0] = 0
    sigma[1,1] = 0
    sigma[2,2] = 0

    Fx = np.zeros((3, pose_map_size))
    Fx[0:3,0:3] = np.identity(3)

    v_c = 1 + (.5 * np.sin(2*np.pi*.2*t))
    om_c = -.2 + (2 * np.cos(2*np.pi*.6*t))

    # control inputs
    velocity = v_c + np.random.normal(scale=np.sqrt( 
        (alphas[0]*(v_c**2)) + (alphas[1]*(om_c**2)) ))
    omega = om_c + np.random.normal(scale=np.sqrt( 
        (alphas[2]*(v_c**2)) + (alphas[3]*(om_c**2)) ))
    
    # uncertainty due to measurement noise
    Qt = np.array([
        [(std_dev_range * std_dev_range), 0],
        [0, (std_dev_bearing * std_dev_bearing)]
    ])

    x_pos_true = np.zeros(t.shape)
    y_pos_true = np.zeros(t.shape)
    theta_true = np.zeros(t.shape)  # radians

    x_pos_true[0 , 0] = 0
    y_pos_true[0 , 0] = 0
    theta_true[0 , 0] = np.pi / 2
    for timestep in range(1, t.size):
        # get previous ground truth state
        prev_state = np.zeros(mu.shape)
        prev_state[0,0] = x_pos_true[0 , timestep-1]
        prev_state[1,0] = y_pos_true[0 , timestep-1]
        prev_state[2,0] = theta_true[0, timestep-1]
        theta_prev = theta_true[0 , timestep-1]

        # get next ground truth state using previous ground truth state
        # and next ground truth input
        next_state = get_mu_bar(prev_state, velocity[0,timestep], 
            omega[0,timestep], theta_prev, dt, Fx)
        x_pos_true[0,timestep] = next_state[0,0]
        y_pos_true[0,timestep] = next_state[1,0]
        theta_true[0,timestep] = next_state[2,0]

    # a record of the pose and world estimates at each timestep
    combined_state_vecs = np.zeros((mu.shape[0],t.size))
    combined_state_vecs[:,0] = mu[:,0]

    # a record of uncertainties over time
    all_sigmas = np.zeros((sigma.shape[0], sigma.shape[1], t.size))
    all_sigmas[:,:,0] = sigma

    FOV = 60
    perception_bound = np.deg2rad(FOV / 2)
    for i in range(1,t.size):
        vt = v_c[0,i]
        wt = om_c[0,i]

        real_x = x_pos_true[0 , i]
        real_y = y_pos_true[0 , i]
        real_theta = theta_true[0 , i]

        # update belief/uncertainty
        mu, sigma = efk_slam(mu, sigma, vt, wt, [real_x, real_y, real_theta],
            world_markers, dt, Fx, alphas, Qt)

        combined_state_vecs[:,i] = mu[:,0]
        all_sigmas[:,:,i] = sigma

    # make things a list (easier for plotting)
    x_pos_true = x_pos_true.tolist()[0]
    y_pos_true = y_pos_true.tolist()[0]
    theta_true = theta_true.tolist()[0]
    t = t.tolist()[0]

    animate((x_pos_true, y_pos_true, theta_true), combined_state_vecs, 
        (world_markers[:, 0], world_markers[:, 1] ), all_sigmas, FOV)

# %%
