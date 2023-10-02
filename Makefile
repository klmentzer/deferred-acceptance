# Compiler settings
CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall

# Python and Cython settings
CYTHON = cython
PYSETUP = python setup.py

# Targets
all: cpp_build cython_build

cpp_build: da_cpp.cpp
	$(CXX) $(CXXFLAGS) -shared -o da_cpp.so -fPIC da_cpp.cpp

cython_build: da_cython.pyx setup.py
	$(PYSETUP) build_ext --inplace

clean:
	rm -f *.so *.o
	rm -rf build
