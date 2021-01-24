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