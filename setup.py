import os
import glob
import shutil
from distutils.core import setup, Extension

nms_module = Extension(
                       "NMS", 
                       sources=["./lib/nms.c"],
                  )

setup(name="NMS",
      version='1.0',
      description="Non Maximum Suppression",
      ext_modules=[nms_module])

# move ./ *.so to lib dir for use
if not os.path.isdir("./lib"):
      os.mkdir("./lib")

for so_file in glob.glob("*.so"):
      clear_name = so_file.split(".")
      clear_name = "".join([clear_name[0], ".", clear_name[-1]])
      shutil.move(so_file, "./lib/" + clear_name)
