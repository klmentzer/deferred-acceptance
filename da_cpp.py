import ctypes
import numpy as np

_lib = ctypes.cdll.LoadLibreary("./da_cpp.so")


def deferred_acceptance(men_preferences, women_preferences, capacites, _lib):
    n = len(men_preferences)
    m = len(women_preferences)
    result = np.empty(n, dtype=np.int32)

    _lib.PyInit_da_cpp(
        ctypes.c_void_p(men_preferences.ctypes.data),
        ctypes.c_void_p(women_preferences.ctypes.data),
        ctypes.c_void_p(capacites.ctypes.data),
        ctypes.c_void_p(result.ctypes.data),
        ctypes.c_int(n),
        ctypes.c_int(m),
    )

    return result.tolist()


if __name__ == "__main__":
    men_preferences = np.array([[1, 2, 0], [0, 2, 1], [1, 2, 0]], dtype=np.int32)

    women_preferences = np.array([[2, 0, 1], [0, 1, 2], [1, 0, 2]], dtype=np.int32)

    result = deferred_acceptance(men_preferences, women_preferences)
    print(result)
