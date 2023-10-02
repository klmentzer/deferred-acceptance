import ctypes
import timeit
import numpy as np

# import da_cython  # Assuming you named the Cython version this way
# import da_cpp  # Assuming you create a Python wrapper for the C++ version
import da_python


# Generate data
def generate_data(n_students, n_schools):
    students_preferences = np.array(
        [
            np.random.choice(n_schools, size=n_schools, replace=False)
            for _ in range(n_students)
        ],
        dtype=np.int32,
    )
    schools_preferences = np.array(
        [
            np.random.choice(n_students, size=n_students, replace=False)
            for _ in range(n_schools)
        ],
        dtype=np.int32,
    )
    capacities = np.random.randint(
        1, n_students // n_schools + 1, size=n_schools, dtype=np.int32
    )
    return students_preferences, schools_preferences, capacities


students_preferences, schools_preferences, capacities = generate_data(1000, 100)

import ctypes

_lib = ctypes.cdll.LoadLibrary("./da_cpp.so")


def deferred_acceptance_cpp(men_preferences, women_preferences, capacites):
    n = len(men_preferences)
    m = len(women_preferences)
    result = np.empty(n, dtype=np.int32)

    _lib.da_cpp(
        ctypes.c_void_p(men_preferences.ctypes.data),
        ctypes.c_void_p(women_preferences.ctypes.data),
        ctypes.c_void_p(capacites.ctypes.data),
        ctypes.c_void_p(result.ctypes.data),
        ctypes.c_int(n),
        ctypes.c_int(m),
    )

    return result.tolist()


# Warm-up runs
pymatch = da_python.deferred_acceptance_python(
    students_preferences, schools_preferences, capacities
)
print(pymatch)
print("done python warmup")
# _lib = ctypes.cdll.LoadLibrary("./da_cpp.so")
# da_cython.deferred_acceptance(students_preferences, schools_preferences, capacities)
deferred_acceptance_cpp(students_preferences, schools_preferences, capacities)
print("done cpp warmup")
# da_cpp.deferred_acceptance(students_preferences, schools_preferences, capacities)

# Benchmark
n_runs = 100
python_time = timeit.timeit(
    lambda: da_python.deferred_acceptance_python(
        students_preferences, schools_preferences, capacities
    ),
    number=n_runs,
)
# cython_time = timeit.timeit(
#     lambda: da_cython.deferred_acceptance(
#         students_preferences, schools_preferences, capacities
#     ),
#     number=n_runs,
# )
cpp_time = timeit.timeit(
    lambda: deferred_acceptance_cpp(
        students_preferences, schools_preferences, capacities
    ),
    number=n_runs,
)

print(f"Python: {python_time / n_runs:.6f} seconds per run")
# print(f"Cython: {cython_time / n_runs:.6f} seconds per run")
print(f"C++: {cpp_time / n_runs:.6f} seconds per run")
