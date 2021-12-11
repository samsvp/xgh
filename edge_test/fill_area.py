#%%
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt

from typing import Callable, List, Tuple


# utility functions
def load_bin_image(path: str, inv=False) -> np.ndarray:
    """
    Loads image and turn it into an image of 0s and 1s
    """
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray[img_gray <= 10] = inv
    img_gray[img_gray > 10] = 1 - inv
    img_gray = img_gray.astype(np.int8)
    return img_gray


def mcircle_mask(image: np.ndarray) -> Callable:
    """
    Defines variables used inside circle_mask
    """
    x = np.arange(image.shape[0]).reshape(1,-1)
    y = np.arange(image.shape[1]).reshape(-1,1)
    img_shape = image.shape
    def _circle_mask(cx: int, cy: int, r: int) -> np.ndarray:
        mask = (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2
        circle = np.zeros(img_shape, dtype=np.int8)
        circle[mask] = 1
        return circle
    
    return _circle_mask


def rec_mask(image: np.ndarray, 
        cx: int, cy: int, r: int) -> np.ndarray:
    x = np.arange(image.shape[0]).reshape(1,-1)
    y = np.arange(image.shape[1]).reshape(-1,1)
    mask = ((x + r > cx) & (x - r < cx)) & \
        ((y + r > cy) & (y - r < cy))
    return mask


def area_outside(img: np.ndarray, cx: int, cy: int, r: int) -> int:
    """
    Returns the circle area outside the image
    """
    circle = circle_mask(cx, cy, r)
    return np.sum(circle | img) - AREA


image = load_bin_image("Reserva_preto.jpg", True)
circle_mask = mcircle_mask(image)

R = np.array([8, 16, 24, 32, 48, 64], dtype=np.int16) # circle radius
P_X, P_Y = np.where(image == 1) # possible circle centers

AREA = np.sum(image == 1)

print(AREA)
print(area_outside(image, 300, 200, 50))

# plt.imshow(image, cmap="gray")
# plt.show()
# plt.imshow(circle_mask(300, 200, R[0]), cmap="gray")
# plt.show()
plt.imshow(rec_mask(image, 184, 306, 8), cmap="gray")
plt.show()
# %%
# remaining centers to pick
def pick_center(picked_centers: List[Tuple[int, int, int]],
        image: np.ndarray, _R_copy = []) -> np.array:
    """
    Picks a random valid center from the image.
    picked_centers: array in the form (cx, cy, r). 
        Represents points already taken
    """
    if not _R_copy:
        R_copy = list(R)
        random.shuffle(R_copy)
    else:
        R_copy = _R_copy[:]

    while len(R_copy) > 0:
        r = R_copy.pop()
    
        circles = np.array(
            [circle_mask(p[0], p[1], p[2] + r) for p in picked_centers]
        ).sum(0)
        
        # possible locations to pick the center
        x, y = np.where(image - circles == 1)

        if (l:=len(x)) == 0:
            continue # if current radius doesn't fit go to next one

        idx = random.randrange(l)
        center = (y[idx], x[idx], r)

        return center
    
    return None # no radius fits the image


picked_centers = []
while (center:= pick_center(picked_centers, image)) is not None:
    picked_centers += [center]

# %%
def minimize_circle_loss(center: Tuple[int, int, int],
        image: np.ndarray, 
        _picked_centers: List[Tuple[int, int, int]]) -> \
            Tuple[List[Tuple[int, int, int]], bool]:
    """
    Tries to minize the given circle loss by moving its
    center, lowering its radius and/or spliting it up 
    into more circles. Returns new centers and a boolean,
    which flags whether the new centers changed or not
    """
    # create a copy of the picked centers
    picked_centers = _picked_centers[:]
    picked_centers.remove(center)

    R_copy = list(R)
    # remove bigger radius
    R_copy = R_copy[:R_copy.index(center[2])]

    if len(R_copy) == 0:
        return (picked_centers, False)
    
    while (center:= pick_center(picked_centers, image, R_copy)) is not None:
        picked_centers.append(center)
    
    return (picked_centers, True)


def circle_cost(center: Tuple[int, int, int],
        image: np.ndarray) -> int:
    """
    Circle loss is defined as the area outside the image
    """
    return area_outside(image, *center)


def total_cost(picked_centers: List[Tuple[int, int, int]],
        image: np.ndarray) -> int:
    """
    Sum of circle's area outside the image and gaps 
    between circles
    """
    circles = np.array(
        [circle_mask(*p) for p in picked_centers]
    ).sum(0)
    cost = np.sum(image ^ circles)
    return cost


t_cost = total_cost(picked_centers, image)
c_costs = [circle_cost(c, image) for c in picked_centers]
print(t_cost)
print(c_costs)

#%%
c = np.array(
    [circle_mask(*p) for p in picked_centers]
).sum(0)

plt.imshow(image - c, cmap="gray")
plt.show()
plt.imshow(c)
plt.show()

# %%
# optimize circles
n_picked_centers = picked_centers
for i in range(50):
    m = np.argmax(c_costs)
    _n_picked_centers, changed = minimize_circle_loss(
        n_picked_centers[m], image, n_picked_centers)
    
    if changed:
        n_picked_centers = _n_picked_centers
    else:
        break

    c_costs = [circle_cost(c, image) for c in n_picked_centers]
    print(i)


nc = np.array(
    [circle_mask(*p) for p in n_picked_centers]
).sum(0)

plt.imshow(image - nc, cmap="gray")
plt.show()
plt.imshow(nc, cmap="gray")
plt.show()
# %%
# pass flower style to circles
from skimage.feature import canny
from skimage.filters import sobel
from scipy import ndimage as ndi
from skimage.segmentation import watershed


# https://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
def get_edges(img: np.ndarray, blur=False) -> np.ndarray:
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if blur:
        img_gray = cv2.GaussianBlur(img_gray, (5,5), 0)

    edges = canny(img_gray / 255)
    return edges


def get_markers(img_gray: np.ndarray,
        low_thresh = 30, high_thresh = 150) -> np.ndarray:

    if len(img_gray.shape) == 3:
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)

    markers = np.zeros_like(img_gray)
    markers[img_gray < low_thresh] = 1
    markers[img_gray > high_thresh] = 2
    return markers


def get_segmentation(img: np.ndarray, 
        low_thresh = 30, high_thresh = 150,
        return_labels=False) -> np.ndarray:

    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img

    markers = get_markers(img_gray, low_thresh, high_thresh)
    elevation_map = sobel(img_gray)

    segmentation = watershed(elevation_map, markers)
    segmentation = ndi.binary_fill_holes(segmentation - 1)

    if return_labels:
        labeled_img, _ = ndi.label(segmentation)
        return segmentation, labeled_img
    else:
        return segmentation


def filter_label(_img: np.ndarray, _img_labels: np.ndarray,
        label: int) -> np.ndarray:
    img = _img.copy()
    img_labels = _img_labels.copy()

    img_labels[img_labels != label] = 0
    img_labels[img_labels == label] = 255

    rows_mask = (img_labels != 0).any(axis=1)
    img = img[rows_mask, :]
    img_labels = img_labels[rows_mask, :]

    cols_mask = (img_labels != 0).any(axis=0)
    img = img[:, cols_mask]
    img_labels = img_labels[:, cols_mask]
    
    # return the mask as alpha channel
    return np.append(img, img_labels[:,:,None], axis=-1).astype(np.uint8)


_flower = cv2.imread("flower.jpeg")
flower = cv2.cvtColor(_flower, cv2.COLOR_BGR2RGB)
seg, labeled_img = get_segmentation(flower, 30, 150, True)
plt.imshow(flower)
plt.show()
plt.imshow(labeled_img)
plt.show()

# check if we filtered the image
img_gray = cv2.cvtColor(flower, cv2.COLOR_BGR2GRAY)
labeled_filter = filter_label(flower, labeled_img, 1)
plt.imshow(labeled_filter)
# %%
def overlay(_img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """
    Overlays img2 into img1
    """
    img1 = _img1.copy() if _img1.shape == img2.shape \
        else _img1.reshape(img2.shape)

    mask = img2[:,:,-1] >= 200
    img1[mask] = img2[mask]
    return img1

# resize image
flower_images = {}

for r in R:
    h = 4*r
    w = 4*r
    flower_images[r] = cv2.resize(labeled_filter, (w+1, h+1))

# create new image
synthetic_img = np.zeros((*image.shape, 4), dtype=np.uint8)
n_picked_centers.sort(key=lambda c: c[-1])
for center in n_picked_centers:
    x, y, r = center
    flower_img = flower_images[r]
    mask = rec_mask(image, x, y, (2*r)+1)

    overlayed = overlay(synthetic_img[mask], flower_img)
    synthetic_img[mask] = overlayed.reshape(-1,4)

plt.imshow(synthetic_img)


# %%
