# python-call-C
python to speed up with call C function


## python use setup & Extension to build *.so 
* build_ext --inplace for build .so to `./`

`python setup.py build_ext --inplace`

## python use ctypes to load .so and call function form module
* load module

`clib = ctypes.CDLL("./lib/NMS.so")`

* set input & out type

`clib.NMS.argtypes = [ctypes.POINTER(ctypes.c_float), 
                        ctypes.c_float, 
                        ctypes.POINTER(ctypes.c_float),
                        ctypes.c_int,
                        ctypes.c_int]`

corresponding to C function input args

`int* NMS(float* bbox, float thresh, float* score, int limit, int len)
`

---
need to set output type if C function not void func()

`from numpy.ctypeslib import ndpointer`
`clib.NMS.restype = ndpointer(dtype=ctypes.c_int, shape=(ARRAY_LENGTH, ))`

use numpy library to set output pointer to numpy array
must  set static output array shape before call C function