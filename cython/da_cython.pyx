# da_cython.pyx

cimport cython
import numpy as np
cimport numpy as cnp


cdef int MAX_STUDENT_PREFERENCES = 159
cdef int MAX_SCHOOL_PREFERENCES = 5200

@cython.boundscheck(False)  # Turn off bounds-checking for performance
@cython.wraparound(False)   # Turn off negative index wrapping for performance
def deferred_acceptance(cnp.int32_t[:, :] students_preferences, cnp.int32_t[:, :] schools_preferences, cnp.int32_t[:] capacities):
    cdef int n_students = students_preferences.shape[0]
    cdef int n_schools = schools_preferences.shape[0]
    cdef int i, j, student, school
    cdef cnp.int32_t[:] result = -np.ones(n_students, dtype=np.int32)
    cdef int[:, :] rank = np.empty((n_schools, n_students), dtype=np.int32)
    cdef list[:] school_students = [list() for _ in range(n_schools)]
    cdef int[:] students_next = np.zeros(n_students, dtype=np.int32)
    cdef list free_students = list(range(n_students))
    cdef int least_preferred_idx

    for i in range(n_schools):
        for j in range(n_students):
            rank[i][schools_preferences[i][j]] = j

    while free_students:
        student = free_students[0]
        school = students_preferences[student][students_next[student]]

        if len(school_students[school]) < capacities[school]:
            school_students[school].append(student)
            free_students.pop(0)
        else:
            # Find least preferred student in school's list
            least_preferred_idx = school_students[school][0]
            for s in school_students[school]:
                if rank[school][s] > rank[school][least_preferred_idx]:
                    least_preferred_idx = s

            # If new student is preferred over the least preferred student in school's list
            if rank[school][student] < rank[school][least_preferred_idx]:
                school_students[school].remove(least_preferred_idx)
                school_students[school].append(student)
                free_students.append(least_preferred_idx)
                free_students.pop(0)

        students_next[student] += 1

    for i in range(n_schools):
        for student in school_students[i]:
            result[student] = i

    return np.asarray(result)
