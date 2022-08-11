#%%
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
import matplotlib.pyplot as plt


def create_dataset():
    np.random.seed(0)

    centers = [[1, 1], [-1, -1], [1, -1]]
    X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.7)
    return (X, labels_true)


def plot_centers(X, n_clusters, k_means_labels,
            k_means_cluster_centers, i):
    plt.figure(figsize=(8, 3))
    colors = ["#4EACC5", "#FF9C34", "#4E9A06"]

    for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], "w", markerfacecolor=col, marker=".")
        plt.plot(
            cluster_center[0],
            cluster_center[1],
            "o",
            markerfacecolor=col,
            markeredgecolor="k",
            markersize=6,
        )
    plt.title(f"KMeans Iteração {i}")
    plt.savefig(f"{i}.png")
    plt.show()
    
    
def train(X, iters=10):
    n_clusters = 3
    init = np.random.random([3, 2])
    k_means_labels = pairwise_distances_argmin(X, init)
    k_means = KMeans(init=init,
        n_init=1,n_clusters=n_clusters, max_iter=1)
    plot_centers(X, n_clusters, k_means_labels, 
                     init, 0)
    for i in range(iters):
        k_means.fit(X)
        k_means_cluster_centers = k_means.cluster_centers_
        k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
        plot_centers(X, n_clusters, k_means_labels, 
                     k_means_cluster_centers, i+1)
        k_means = KMeans( 
            n_clusters=n_clusters, max_iter=1,
            init=k_means_cluster_centers)


X, y = create_dataset()

train(X)
# %%
