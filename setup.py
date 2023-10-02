# from setuptools import setup
# from Cython.Build import cythonize
import numpy as np

# setup(ext_modules=cythonize("da_cython.pyx"), include_dirs=[np.get_include()])
from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the C++ extension
extensions = [
    Extension(
        name="da_cpp",  # The name of the resulting .so file and the Python import name
        sources=[
            # "da_cython.pyx",
            "da_cpp.cpp",
        ],  # The .pyx file and your C++ source files
        language="c++",  # This tells Cython it's dealing with C++ code
        extra_compile_args=[
            "-std=c++11"
        ],  # Make sure to specify the correct C++ version
        include_dirs=[
            ".",
            np.get_include(),
        ],  # Adjust this if your headers are in a different directory
    )
]

setup(
    name="Deferred Acceptance",
    # ext_modules=cythonize(extensions),
)
