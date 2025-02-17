from gale_shapley import match_students_to_schools

# Simple example with 2 students and 2 schools
student_preferences = [
    [0, 1],  # Student 0 prefers School 0 over School 1
    [1]      # Student 1 only wants School 1
]

school_preferences = [
    [0],     # School 0 only wants Student 0
    [1, 0]   # School 1 ranks both students
]

school_capacities = [1, 1]  # Each school can accept 1 student

matches = match_students_to_schools(student_preferences, school_preferences, school_capacities)
print(matches)  # Output: {0: 0, 1: 1}  # {student_id: school_id}