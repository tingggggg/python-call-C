# python-call-C
python to speed up with call C function example [Non Maximum Suppression (MNS)]

A Bounding Box array of length 10647 to compare NMS cost time both on python and C function

In this example, C is approximately 12 times faster than python

## python use setup & Extension to build *.so 
* build_ext --inplace for build .so to `./`

`python setup.py build_ext --inplace`

## python use ctypes to load .so 
* load module

`clib = ctypes.CDLL("./lib/NMS.so")`

* set input & out type

`clib.NMS.argtypes = [ctypes.POINTER(ctypes.c_float), 
                        ctypes.c_float, 
                        ctypes.POINTER(ctypes.c_float),
                        ctypes.c_int,
                        ctypes.c_int]`

corresponding to C function input args

`int* NMS(float* bbox, float thresh, float* score, int limit,int len)
`

---
need to set output type if C function not void func()

`from numpy.ctypeslib import ndpointer`

`clib.NMS.restype = ndpointer(dtype=ctypes.c_int, shape=(ARRAY_LENGTH, ))`

use numpy library to set output pointer to numpy array
must set static output array shape before call C function

## call C function from module

* convert args for c before call C function

convert arg for c follow below steps if your arg is list or array ... type

1. if your array number of dim > 1, flatten it first 

`bbox = bbox.flatten()`

2. convert numpy array to pointer to C

`bbox_ptr = bbox.ctypes.data_as(ctypes.POINTER(ctypes.c_float))`

* call C function

`res = clib.NMS(bbox_ptr, thresh, score_ptr, 0, len(score))`

type of res is numpy array that corresponding to set `restype`




