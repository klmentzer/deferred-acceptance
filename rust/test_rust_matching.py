import pytest
from gale_shapley import match_students_to_schools

def verify_matching_stability(matching, student_prefs, school_prefs, capacities):
    """
    Verify that a matching is stable by checking for blocking pairs.
    Returns (is_stable, blocking_pair) where blocking_pair is None if stable.
    """
    # Convert matching to school -> list of students
    school_matches = {i: [] for i in range(len(school_prefs))}
    for student, school in matching.items():
        school_matches[school].append(student)
    
    # Check each student-school pair for blocking pairs
    for student in range(len(student_prefs)):
        student_school = matching.get(student)
        if student_school is None:
            continue
            
        student_prefs_list = student_prefs[student]
        if not student_prefs_list:  # Skip students with empty preferences
            continue
            
        current_school_rank = student_prefs_list.index(student_school)
        
        # Check each school that student prefers to current match
        for preferred_school in student_prefs_list[:current_school_rank]:
            school_students = school_matches[preferred_school]
            school_preferences = school_prefs[preferred_school]
            
            # Skip if school doesn't list student in preferences
            if student not in school_preferences:
                continue
                
            # If school has space, it's a blocking pair
            if len(school_students) < capacities[preferred_school]:
                return False, (student, preferred_school)
                
            # Check if school would prefer this student to any current student
            student_rank = school_preferences.index(student)
            
            for current_student in school_students:
                # Skip if current student isn't in school's preferences
                if current_student not in school_preferences:
                    continue
                current_rank = school_preferences.index(current_student)
                if student_rank < current_rank:
                    return False, (student, preferred_school)
                    
    return True, None

def test_incomplete_preferences():
    """Test with incomplete preference lists"""
    student_prefs = [
        [0],      # Student 0 only wants school 0
        [1, 0],   # Student 1 wants both schools
        []        # Student 2 has no preferences
    ]
    school_prefs = [
        [0, 1],   # School 0 ranks students 0 and 1
        [1]       # School 1 only ranks student 1
    ]
    capacities = [1, 1]
    
    result = match_students_to_schools(student_prefs, school_prefs, capacities)
    is_stable, blocking_pair = verify_matching_stability(result, student_prefs, school_prefs, capacities)
    
    assert is_stable, f"Matching not stable, found blocking pair: {blocking_pair}"
    assert result.get(2) is None, "Student with empty preferences was matched"
    assert len(result) == 2, "Wrong number of students matched"

def test_mutual_incomplete_preferences():
    """Test when both sides have incomplete preferences"""
    student_prefs = [
        [0],      # Student 0 only ranks school 0
        [1],      # Student 1 only ranks school 1
        [0, 1]    # Student 2 ranks both schools
    ]
    school_prefs = [
        [2],      # School 0 only ranks student 2
        [1, 2]    # School 1 ranks students 1 and 2
    ]
    capacities = [1, 1]
    
    result = match_students_to_schools(student_prefs, school_prefs, capacities)
    is_stable, blocking_pair = verify_matching_stability(result, student_prefs, school_prefs, capacities)
    
    assert is_stable, f"Matching not stable, found blocking pair: {blocking_pair}"

def test_invalid_inputs():
    """Test that invalid inputs raise appropriate errors"""
    with pytest.raises(ValueError):
        # Duplicate preferences
        match_students_to_schools(
            [[0, 0]], 
            [[0]], 
            [1]
        )
    
    with pytest.raises(ValueError):
        # Invalid school ID
        match_students_to_schools(
            [[1]], 
            [[0]], 
            [1]
        )
    
    with pytest.raises(ValueError):
        # Invalid capacity
        match_students_to_schools(
            [[0]], 
            [[0]], 
            [0]
        )

def test_varying_preference_lengths():
    """Test with varying preference list lengths"""
    student_prefs = [
        [0, 1, 2],    # Complete preferences
        [1],          # Single preference
        [0, 2],       # Partial preferences
        []            # No preferences
    ]
    school_prefs = [
        [0, 1],       # Partial student rankings
        [1, 2, 0, 3], # Complete student rankings
        [2]           # Single student ranking
    ]
    capacities = [1, 2, 1]
    
    result = match_students_to_schools(student_prefs, school_prefs, capacities)
    is_stable, blocking_pair = verify_matching_stability(result, student_prefs, school_prefs, capacities)
    
    assert is_stable, f"Matching not stable, found blocking pair: {blocking_pair}"
    assert result.get(3) is None, "Student with empty preferences was matched"

if __name__ == "__main__":
    pytest.main([__file__])