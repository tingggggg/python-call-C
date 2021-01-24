import numpy as np
import ctypes
import time
from numpy.ctypeslib import ndpointer


def nms(bbox, thresh, score=None, limit=None):
    """Suppress bounding boxes according to their IoUs and confidence scores.
    Args:
        bbox (array): Bounding boxes to be transformed. The shape is
            :math:`(R, 4)`. :math:`R` is the number of bounding boxes.
        thresh (float): Threshold of IoUs.
        score (array): An array of confidences whose shape is :math:`(R,)`.
        limit (int): The upper bound of the number of the output bounding
            boxes. If it is not specified, this method selects as many
            bounding boxes as possible.
    Returns:
        array:
        An array with indices of bounding boxes that are selected. \
        They are sorted by the scores of bounding boxes in descending \
        order. \
        The shape of this array is :math:`(K,)` and its dtype is\
        :obj:`numpy.int32`. Note that :math:`K \\leq R`.
    from: https://github.com/chainer/chainercv
    """

    if len(bbox) == 0:
        return np.zeros((0,), dtype=np.int32)

    if score is not None:
        order = score.argsort()[::-1]
        bbox = bbox[order]

    bbox_area = np.prod(bbox[:, 2:] - bbox[:, :2], axis=1)   

    selec = np.zeros(bbox.shape[0], dtype=bool)
    for i, b in enumerate(bbox):
        tl = np.maximum(b[:2], bbox[selec, :2])
        br = np.minimum(b[2:], bbox[selec, 2:])
        area = np.prod(br - tl, axis=1) * (tl < br).all(axis=1)

        iou = area / (bbox_area[i] + bbox_area[selec] - area)

        if (iou >= thresh).any():
            continue

        selec[i] = True
        if limit is not None and np.count_nonzero(selec) >= limit:
            break

    selec = np.where(selec)[0]
    if score is not None:
        selec = order[selec]
    print(selec.astype(np.int32).shape)
    print(selec.astype(np.int32)[:10])
    return selec.astype(np.int32)

def nms_c(bbox, thresh, score=None, limit=None):
    bbox = bbox.flatten()

    clib = ctypes.CDLL("./lib/NMS.so")
    clib.NMS.argtypes = [ctypes.POINTER(ctypes.c_float), 
                        ctypes.c_float, 
                        ctypes.POINTER(ctypes.c_float),
                        ctypes.c_int,
                        ctypes.c_int]
    clib.NMS.restype = ndpointer(dtype=ctypes.c_int, shape=(len(score), ))

    bbox_ptr = bbox.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    score_ptr = score.ctypes.data_as(ctypes.POINTER(ctypes.c_float)) 

    nms_res = clib.NMS(bbox_ptr, thresh, score_ptr, 0, len(score))

    return nms_res[nms_res != -1].astype(np.int32)

if __name__ == "__main__":
    np.random.seed(5345)
    bbox = np.random.randn(10647, 4).astype("float32")
    bbox = np.array([
        [30, 20, 230, 200], 
        [50, 50, 260, 220],
        [210, 30, 420, 5],
        [430, 280, 460, 360]
    ], dtype="float32")
    score = np.random.randn(10647, ).astype('float32')
    score = np.array([0.1, 0.08, 0.8, 0.7], dtype="float32")
    thresh = 0.45
    # py_nms(bbox, score, thresh)
    start = time.time()
    nms(bbox, thresh, score=score)
    print(f'python cost time: {time.time() - start} s')

    print("\n***** \'C\' ***** \n")

    start = time.time()
    nms_c(bbox, thresh, score)
    print(f"C cost time: {time.time() - start} s")