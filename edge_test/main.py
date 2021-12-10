#%%
import cv2
import numpy as np
from skimage.feature import canny
from skimage.filters import sobel
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
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
    return np.append(img, img_labels[:,:,None], axis=-1)


#%%
img = cv2.imread("../flower_single.jpg")
seg = get_segmentation(img, 30, 100)
plt.imshow(seg)

#%%
segmentation, labeled_img = get_segmentation(img, 30, 100, True)
plt.imshow(labeled_img)
plt.show()
labeled_filter = filter_label(img,labeled_img, 2)
plt.imshow(labeled_filter)
plt.show()

# %%
rev = cv2.imread("../Reserva.jpg")
rev_gray = cv2.cvtColor(rev, cv2.COLOR_BGR2GRAY)
rev_edges = canny(rev_gray)
plt.imshow(rev_edges)
# %%
indexes = np.array(np.where(rev_edges)).T
indexes[2450]
# %%
x, y = indexes[2450]
s_x = labeled_filter.shape[0] // 2
s_y = labeled_filter.shape[1] // 2
rev[x-s_x:x+s_x+1, y-s_y:y+s_y, :] = labeled_filter
plt.plot(rev)
# %%
img = cv2.imread("eu.jpg")
seg = get_edges(img, False)
plt.imshow(seg)
# %%
img = cv2.imread("john.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
edges = cv2.Canny(image=img_blur, threshold1=30, threshold2=100) 
plt.imshow(edges, cmap="gray")
# %%
