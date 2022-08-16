#%%
import numpy as np
import matplotlib.pyplot as plt


def angle_diff(angle: float) -> float:
    a = np.rad2deg(angle)
    a = (a + 180) % 360 - 180
    return np.deg2rad(a)


def ekf_known_corres(mu_l: np.ndarray, sigma_l: np.ndarray, 
        ut: np.ndarray, zt: np.ndarray, ct: np.ndarray, 
        m: np.ndarray, dt: float, alphas: np.ndarray) -> \
            np.array:
    """
    Parameters
    mu: gaussian estimate of the robot pose at time t-1
    sigma: gaussian covariance matrix of the robot pose at time t-1
    ut: current control signal
    zt: current features measurements vector
    ct: true features corresponding to zt
    m: map
    dt: time passed since the last measurement
    alphas: noise constants
    """
    theta = mu_l[-1]
    vt, wt = ut
    # jacobians calculation
    Gt = np.array([
        [1, 0, -vt/wt * np.cos(theta) + vt/wt * np.cos(theta + wt*dt)],
        [1, 0, -vt/wt * np.sin(theta) + vt/wt * np.sin(theta + wt*dt)],
        [0, 0, 1]
    ])

    Vt = np.array([
        [(-np.sin(theta) + np.sin(theta + wt*dt)) / wt, 
         vt*(np.sin(theta) - np.sin(theta + wt*dt)) / wt ** 2 + vt * np.cos(theta + wt*dt) * dt / wt],
        [(np.cos(theta) - np.cos(theta + wt * dt) / wt), 
         -vt * (np.cos(theta) - np.cos(theta + wt * dt)) / wt ** 2 + vt * np.sin(theta + wt * dt) * dt / wt],
        [0, dt]
    ])

    # noise matrix 
    Mt = np.array([
        [alphas[0] * vt ** 2 + alphas[1] * wt ** 2, 0],
        [0, alphas[2] * vt ** 2 + alphas[3] * wt ** 2]
    ])

    # motion update
    mut = get_next_pos(mu_l, ut, dt)
    sigmat = Gt @ sigma_l @ Gt.T + Vt @ Mt @ Vt.T

    Qt = np.array([[0.001, 0, 0], [0, 0.00001, 0], [0, 0, 0]])

    for i in range(zt.shape[0]):
        mx, my, s = ct[i]

        q = (mx - mut[0]) ** 2 + (my - mut[1]) ** 2
        # predicted measurement
        z_hat = np.array([
            np.sqrt(q),
            np.arctan2(my - mut[1], mx - mut[0]) - mut[2],
            s
        ])

        # measurement jacobian
        Ht = np.array([
            [- (mx - mut[0]) / np.sqrt(q), - (my - mut[1]) / np.sqrt(q), 0],
            [(my - mut[1]) / q, - (mx - mut[0]) / q, -1],
            [0, 0, 0]
        ])
        # uncertainty
        St = Ht @ sigmat @ Ht.T + Qt
        
        # kalman gain
        Kt = sigmat @ Ht.T @ np.linalg.pinv(St)
        
        # update predictions
        
        dz = (zt[i] - z_hat)
        dz[1] = angle_diff(dz[1])
        print(dz)
        mut = mut + Kt @ dz
        sigmat = (np.eye(3) - Kt @ Ht) @ sigmat

    return mut, sigmat


def get_next_pos(mu_l, ut, dt):
    theta = mu_l[-1]
    vt, wt = ut
    mut = mu_l + np.array([
        -vt / wt * np.sin(theta) + vt/wt * np.sin(theta + wt * dt),
        vt / wt * np.cos(theta) - vt / wt * np.cos(theta + wt * dt),
        wt * dt])
    return mut


def get_z(pos: np.ndarray, cts) -> np.ndarray:
    z = []
    for ct in cts:
        q = (ct[0] - pos[0]) ** 2 + (ct[1] - pos[1]) ** 2
        zt = np.array([
            np.sqrt(q),
            np.arctan2(ct[1] - pos[1], ct[0] - pos[0]) - pos[2],
            ct[2]
        ])
        z.append(zt)
    return np.array(z)


def noise3d(s: int) -> np.ndarray:
    return np.array([
        (np.random.normal(scale=s)) * s,
        (np.random.normal(scale=s)) * s,
        0])


def noise(cov):
    return np.random.multivariate_normal(
        np.zeros(cov.shape[0]), cov)


exp_poses = [np.array([0, 0, 0])]
true_poses = [np.array([0, 0, 0])]
ekf_poses = [np.array([0, 0, 0])]

ct = np.array([[0, 0, 0], [1, 1, 0], [2, 0, 0]])
m = []
dt = 0.1
alphas = [0.001, 0.001, 0.001, 0.001]
cov = 1. * np.eye(3)

t = np.arange(0, 20+dt, dt)
v_c = 1 + (.5*np.sin(2*np.pi*.2*t))
om_c = -.2 + (2*np.cos(2*np.pi*.6*t))
velocity = v_c + np.random.normal(scale=np.sqrt( 
    (alphas[0]*(v_c**2)) + (alphas[1]*(om_c**2)) ))
omega = om_c + np.random.normal(scale=np.sqrt( 
    (alphas[2]*(v_c**2)) + (alphas[3]*(om_c**2)) ))
    
u = np.array([velocity, omega]).T
for ut in u:
    mu_l = np.array([0.0, 0.0, 0.0])

    n_pos = get_next_pos(exp_poses[-1], ut, dt)
    exp_poses.append(n_pos)

    true_pos = get_next_pos(true_poses[-1], ut, dt)
    n = noise(cov[:2, :2])
    true_pos[0] += 0.5 * n[0]
    true_pos[1] += 0.5 * n[1]
    true_poses.append(true_pos)
    zt = get_z(true_pos, ct)

    ekf_pos, cov = ekf_known_corres(
        ekf_poses[-1], cov, ut, zt, ct, m, dt, alphas)
    ekf_poses.append(ekf_pos)

exp_poses = np.array(exp_poses)
true_poses = np.array(true_poses)
ekf_poses = np.array(ekf_poses)

plt.plot(true_poses[:,0], true_poses[:,1], "o-")
plt.plot(exp_poses[:,0], exp_poses[:,1], "ro--")
plt.plot(ekf_poses[:,0], ekf_poses[:,1], "go--")

plt.show()
plt.plot(true_poses[:,0] - ekf_poses[:,0])
plt.plot(true_poses[:,0] - exp_poses[:,0])
plt.plot(true_poses[:,0] - true_poses[:,0], "b--")

plt.show()
plt.plot(true_poses[:,1] - ekf_poses[:,1])
plt.plot(true_poses[:,1] - exp_poses[:,1])
plt.plot(true_poses[:,0] - true_poses[:,0], "b--")
# %%
