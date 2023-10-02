def deferred_acceptance_python(students_prefs, schools_prefs, capacities):
    n_students = len(students_prefs)
    n_schools = len(schools_prefs)

    # Initialize an empty list of schools' current students
    schools_students = [[] for _ in range(n_schools)]

    # Initialize all students as not yet assigned to a school
    students_assigned = [False] * n_students

    # Each student's pointer to the school they will propose to next
    propose_index = [0] * n_students

    while not all(students_assigned):
        for student, assigned in enumerate(students_assigned):
            if not assigned:
                school = students_prefs[student][propose_index[student]]

                if (
                    len(schools_students[school]) < capacities[school]
                ):  # If there's available capacity
                    schools_students[school].append(student)
                    students_assigned[student] = True
                else:
                    current_students = schools_students[school]
                    for preferred_student in schools_prefs[school]:
                        if (
                            preferred_student == student
                        ):  # If the school prefers the current student over its least preferred student
                            least_preferred_student = (
                                current_students.pop()
                            )  # Remove the least preferred student
                            schools_students[school].append(
                                student
                            )  # Add the new student
                            students_assigned[least_preferred_student] = False
                            propose_index[
                                least_preferred_student
                            ] += 1  # Increase the propose index for the removed student
                            students_assigned[student] = True
                            break
                        if preferred_student in current_students:
                            break

                if not students_assigned[student]:  # If the student wasn't assigned
                    propose_index[student] += 1  # Try the next school

                # Check if student has run out of preferences
                if propose_index[student] == len(students_prefs[student]):
                    students_assigned[student] = True

    # Convert list of students for each school into the result format
    result = [-1] * n_students
    for school, students in enumerate(schools_students):
        for student in students:
            result[student] = school

    return result
