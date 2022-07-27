#%%
import numpy as np
import matplotlib.pyplot as plt

def gini(c1, c2):
    """
    c1 and c2 are the counts for each class
    after the split
    """
    p1 = c1 / (c1 + c2)
    p2 = c2 / (c1 + c2)
    return p1*(1-p1) + p2*(1-p2)


def w_gini(gl, gr, a, b):
    """
    gl is the gini index of the left leaf
    and gr of the right leaf.
    a is the number of members in the left
    leaf and b of the right
    """
    return (a * gl + b * gr) / (a + b)


n = 100
brightness = np.random.random(n)
texture = np.random.random(n)

Y = np.array([1 
    if brightness[i] > 0.5 and texture[i] < 0.5
    else 0 for i in range(n)])

scatter = plt.scatter(brightness, texture, c=Y)
plt.legend(*scatter.legend_elements())
plt.xlabel("Luminosidade")
plt.ylabel("Textura")
plt.title("Dataset")
plt.savefig("gab.png")


#%%
scatter = plt.scatter(brightness, texture, c=Y)
plt.legend(*scatter.legend_elements())
plt.xlabel("Luminosidade")
plt.ylabel("Textura")
plt.title("Dataset")
plt.axvline(x=0.5,color='r',linestyle='--')
plt.axvline(x=0.8,color='r',linestyle='--')
plt.savefig("bright_comp.png")

#%%
scatter = plt.scatter(brightness, texture, c=Y)
plt.legend(*scatter.legend_elements())
plt.xlabel("Luminosidade")
plt.ylabel("Textura")
plt.title("Dataset")
plt.axvline(x=0.5,color='r',linestyle='--')
plt.savefig("bright_05.png")



# %%
splitl = brightness > 0.5
splitr = brightness <= 0.5
gl = gini(sum(Y[splitl]), len(Y[splitl]) - sum(Y[splitl]))
gr = gini(sum(Y[splitr]), len(Y[splitr]) - sum(Y[splitr]))
w_gini(gl, gr, len(Y[splitl]), len(Y[splitr]))
# %%
splitl = brightness > 0.8
splitr = brightness <= 0.8
gl = gini(sum(Y[splitl]), len(Y[splitl]) - sum(Y[splitl]))
gr = gini(sum(Y[splitr]), len(Y[splitr]) - sum(Y[splitr]))
w_gini(gl, gr, len(Y[splitl]), len(Y[splitr]))
# %%
nY = Y[brightness > 0.5]
ntext = texture[brightness > 0.5]
#%%
splitl = ntext > 0.5
splitr = ntext <= 0.5
gl = gini(sum(nY[splitl]), len(nY[splitl]) - sum(nY[splitl]))
gr = gini(sum(nY[splitr]), len(nY[splitr]) - sum(nY[splitr]))
w_gini(gl, gr, len(nY[splitl]), len(nY[splitr]))


# %%
splitl = ntext > 0.8
splitr = ntext <= 0.8

gl = gini(sum(nY[splitl]), len(nY[splitl]) - sum(nY[splitl]))
gr = gini(sum(nY[splitr]), len(nY[splitr]) - sum(nY[splitr]))
w_gini(gl, gr, len(nY[splitl]), len(nY[splitr]))
# %%
plt.axvline(x=0.5,color='r',linestyle='--')
plt.axhline(y=0.5, color='b',linestyle='--')
plt.axhline(y=0.8, color='b',linestyle='--')
plt.scatter(brightness, texture, c=Y)
plt.legend(*scatter.legend_elements())
plt.xlabel("Luminosidade")
plt.ylabel("Textura")
plt.title("Dataset")
plt.savefig("text_comp.png")

# %%
plt.axvline(x=0.5,color='r',linestyle='--')
plt.axhline(y=0.5, color='b',linestyle='--')
plt.scatter(brightness, texture, c=Y)
plt.legend(*scatter.legend_elements())
plt.xlabel("Luminosidade")
plt.ylabel("Textura")
plt.title("Dataset")
plt.savefig("res.png")
# %%
