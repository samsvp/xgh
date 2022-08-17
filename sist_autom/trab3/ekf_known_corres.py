#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import sqrtm
import conf_ellipse as ce


def get_next_pos(mu_l: np.ndarray, ut: np.ndarray, dt: float) -> np.ndarray:
    theta = mu_l[-1]
    vt, wt = ut
    mut = mu_l + np.array([
        -vt / wt * np.sin(theta) + vt/wt * np.sin(theta + wt * dt),
        vt / wt * np.cos(theta) - vt / wt * np.cos(theta + wt * dt),
        wt * dt])
    return mut


def get_z(pos: np.ndarray, cts: np.ndarray) -> np.ndarray:
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


def angle_diff(angle: float) -> float:
    a = np.rad2deg(angle)
    a = (a + 180) % 360 - 180
    return np.deg2rad(a)


def get_Gt(vt: float, wt: float, theta: float, dt: float) -> np.ndarray:
    return np.array([
        [1, 0, -vt/wt * np.cos(theta) + vt/wt * np.cos(theta + wt*dt)],
        [1, 0, -vt/wt * np.sin(theta) + vt/wt * np.sin(theta + wt*dt)],
        [0, 0, 1]
    ])


def get_Mt(vt: float, wt: float, alphas: np.ndarray) -> np.ndarray:
    return np.array([
        [alphas[0] * vt ** 2 + alphas[1] * wt ** 2, 0],
        [0, alphas[2] * vt ** 2 + alphas[3] * wt ** 2]
    ])


def get_Vt(vt: float, wt: float, theta: float, dt: float) -> np.ndarray:
    return np.array([
        [(-np.sin(theta) + np.sin(theta + wt*dt)) / wt, 
         vt*(np.sin(theta) - np.sin(theta + wt*dt)) / wt ** 2 + vt * np.cos(theta + wt*dt) * dt / wt],
        [(np.cos(theta) - np.cos(theta + wt * dt) / wt), 
         -vt * (np.cos(theta) - np.cos(theta + wt * dt)) / wt ** 2 + vt * np.sin(theta + wt * dt) * dt / wt],
        [0, dt]
    ])


def get_sigmat(sigma_l: np.ndarray, Gt: np.ndarray, 
        Vt: np.ndarray, Mt: np.ndarray) -> np.ndarray:
    return Gt @ sigma_l @ Gt.T + Vt @ Mt @ Vt.T


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
    Gt = get_Gt(vt, wt, theta, dt)
    Vt = get_Vt(vt, wt, theta, dt)

    # noise matrix 
    Mt = get_Mt(vt, wt, alphas)

    # motion update
    mut = get_next_pos(mu_l, ut, dt)
    sigmat = get_sigmat(sigma_l, Gt, Vt, Mt)

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
        mut = mut + Kt @ dz
        sigmat = (np.eye(3) - Kt @ Ht) @ sigmat

    return mut, sigmat


def ekf_localization(mu_l: np.ndarray, sigma_l: np.ndarray, 
        ut: np.ndarray, zt: np.ndarray, cts: np.ndarray, 
        m: np.ndarray, dt: float, alphas: np.ndarray) -> \
            np.array:
    """
    Ekf localization where you don't know the zt - ct correspondence.
    Highly unstable.
    Parameters
    mu: gaussian estimate of the robot pose at time t-1
    sigma: gaussian covariance matrix of the robot pose at time t-1
    ut: current control signal
    zt: current features measurements vector
    cts: list of landmarks in the map, same size as zt
    m: map
    dt: time passed since the last measurement
    alphas: noise constants
    """
    theta = mu_l[-1]
    vt, wt = ut
    # jacobians calculation
    Gt = get_Gt(vt, wt, theta, dt)
    Vt = get_Vt(vt, wt, theta, dt)

    # noise matrix 
    Mt = get_Mt(vt, wt, alphas)

    # motion update
    mut = get_next_pos(mu_l, ut, dt)
    sigmat = get_sigmat(sigma_l, Gt, Vt, Mt)

    Qt = np.array([[0.001, 0, 0], [0, 0.00001, 0], [0, 0, 0]])

    for z in zt:
        Ht: np.ndarray = None
        St: np.ndarray = None
        max_likelihood = np.NINF
        dz: np.ndarray = None
        for ct in cts:
            mx, my, s = ct
            mu_x, mu_y, mu_theta = mut
            q = (mx - mu_x) ** 2 + (my - mu_y) ** 2
            _z_hat = np.array([
                np.sqrt(q),
                np.arctan2(my - mut[1], mx - mut[0]) - mut[2],
                s
            ])

            # measurement jacobian
            _Ht = np.array([
                [- (mx - mut[0]) / np.sqrt(q), - (my - mut[1]) / np.sqrt(q), 0],
                [(my - mut[1]) / q, - (mx - mut[0]) / q, -1],
                [0, 0, 0]
            ])

            # uncertainty
            _St = _Ht @ sigmat @ _Ht.T + Qt
            _dz = (z - _z_hat)
            _dz[1] = angle_diff(_dz[1])
            inv_square_St = np.linalg.pinv(_St[:2, :2])
            likelihood = np.log(np.linalg.det(2 * np.pi * sqrtm(inv_square_St))) \
                + (-0.5 * _dz[:2].reshape(1,-1) @ inv_square_St @ _dz[:2].reshape(-1,1))
            
            if max_likelihood < likelihood[0][0]:
                max_likelihood = likelihood
                St = _St
                Ht = _Ht
                dz = _dz
        
        Kt = sigmat @ Ht.T @ np.linalg.pinv(St)
        mut = mut + Kt @ dz
        sigmat = (np.eye(3) - Kt @ Ht) @ sigmat

    return mut, sigmat


exp_poses = [np.array([0, 0, 0])]
true_poses = [np.array([0, 0, 0])]
ekf_poses = [np.array([0, 0, 0])]
ekf_unknown_poses = [np.array([0, 0, 0])]

ct = np.array([[0, 0, 0], [10, 10, 0], [20, 0, 0]])
m = []
dt = 1
alphas = [0.001, 0.001, 0.001, 0.001]
cov = 1. * np.eye(3)
cov_u = cov

covs = [cov]
covs_u = [cov_u]

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
    ekf_u_pos, cov_u = ekf_localization(
        ekf_unknown_poses[-1], cov_u, ut, zt, ct, m, dt, alphas)
    
    covs.append(cov)
    covs_u.append(cov_u)
    ekf_poses.append(ekf_pos)
    ekf_unknown_poses.append(ekf_u_pos)

exp_poses = np.array(exp_poses)
true_poses = np.array(true_poses)
ekf_poses = np.array(ekf_poses)
ekf_unknown_poses = np.array(ekf_unknown_poses)



fig, ax_nstd = plt.subplots(figsize=(6, 6))
ax_nstd.set_title = "Robot predicted path"
ax_nstd.plot(true_poses[:,0], true_poses[:,1], "o-", label="true")
ax_nstd.plot(exp_poses[:,0], exp_poses[:,1], "ro--", label="no ekf")
ax_nstd.plot(ekf_poses[:,0], ekf_poses[:,1], "go--", label="ekf")
ax_nstd.plot(ekf_unknown_poses[:,0], ekf_unknown_poses[:,1], 
    "mo--", label="efk unknown", alpha=0.25)

for i in range(1, len(covs)):
    mean = ekf_poses[i][:2]
    ce.cconfidence_ellipse(mean, covs[i], 
        ax_nstd, n_std=1, edgecolor='firebrick')
    ce.cconfidence_ellipse(mean, covs[i], 
        ax_nstd, n_std=2, edgecolor='fuchsia')
    ce.cconfidence_ellipse(mean, covs[i], 
        ax_nstd, n_std=3, edgecolor='blue')

for i in range(1, len(covs_u)):
    mean = ekf_unknown_poses[i][:2]
    ce.cconfidence_ellipse(mean, covs_u[i], 
        ax_nstd, n_std=1, edgecolor='firebrick')
    ce.cconfidence_ellipse(mean, covs_u[i], 
        ax_nstd, n_std=2, edgecolor='fuchsia')
    ce.cconfidence_ellipse(mean, covs_u[i], 
        ax_nstd, n_std=3, edgecolor='blue')
ax_nstd.legend()

plt.show()

plt.title("X-axis error")
plt.plot(true_poses[:,0] - ekf_poses[:,0], label="ekf")
plt.plot(true_poses[:,0] - exp_poses[:,0], label="no ekf")
plt.plot(true_poses[:,0] - ekf_unknown_poses[:,0], label="ekf unknown")
plt.plot(true_poses[:,0] - true_poses[:,0], "b--")
plt.legend()

plt.show()
plt.title("Y-axis error")
plt.plot(true_poses[:,1] - ekf_poses[:,1], label="ekf")
plt.plot(true_poses[:,1] - exp_poses[:,1], label="no ekf")
plt.plot(true_poses[:,1] - ekf_unknown_poses[:,1], label="ekf unknown")
plt.plot(true_poses[:,0] - true_poses[:,0], "b--")
plt.legend()
# %%
fig, ax_nstd = plt.subplots(figsize=(6, 6))
ce.cconfidence_ellipse(ekf_poses[-1][:2], cov, ax_nstd,n_std=1, edgecolor='firebrick')
ce.cconfidence_ellipse(ekf_poses[-1][:2], cov, ax_nstd, n_std=2,edgecolor='fuchsia')
ce.cconfidence_ellipse(ekf_poses[-1][:2], cov, ax_nstd, n_std=3,edgecolor='blue')
plt.plot(ekf_poses[-1][0], ekf_poses[-1][1])
# %%
