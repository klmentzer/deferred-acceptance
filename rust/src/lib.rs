use std::collections::{HashMap, VecDeque};
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

#[derive(Debug)]
struct School {
    capacity: usize,
    preferences: HashMap<usize, usize>,  // student id -> rank
    current_students: Vec<usize>,
}

impl School {
    fn new(capacity: usize, preferences: Vec<usize>) -> Self {
        // Convert preference list to HashMap with ranks
        let preferences: HashMap<usize, usize> = preferences
            .into_iter()
            .enumerate()
            .map(|(rank, student)| (student, rank))
            .collect();

        School {
            capacity,
            preferences,
            current_students: Vec::with_capacity(capacity),
        }
    }

    fn rank_of(&self, student: usize) -> Option<usize> {
        self.preferences.get(&student).copied()
    }

    fn would_accept(&self, student: usize) -> Option<(bool, Option<usize>)> {
        // If school doesn't have student in preferences, reject
        let student_rank = match self.rank_of(student) {
            Some(rank) => rank,
            None => return Some((false, None))
        };
        
        if self.current_students.len() < self.capacity {
            return Some((true, None));
        }

        // Find worst current student
        let mut worst_student = None;
        let mut worst_rank = 0;

        for &current in &self.current_students {
            // Schools must have ranks for all current students
            let rank = self.rank_of(current).unwrap();
            if worst_student.is_none() || rank > worst_rank {
                worst_student = Some(current);
                worst_rank = rank;
            }
        }

        Some((
            student_rank < worst_rank,
            if student_rank < worst_rank { worst_student } else { None }
        ))
    }

    fn add_student(&mut self, student: usize) {
        self.current_students.push(student);
    }

    fn remove_student(&mut self, student: usize) {
        if let Some(pos) = self.current_students.iter().position(|&s| s == student) {
            self.current_students.swap_remove(pos);
        }
    }
}

fn validate_inputs(
    student_preferences: &Vec<Vec<usize>>,
    school_preferences: &Vec<Vec<usize>>,
    school_capacities: &Vec<usize>
) -> Result<(), String> {
    let num_students = student_preferences.len();
    let num_schools = school_preferences.len();

    // Basic size checks
    if num_schools == 0 {
        return Err("Must have at least one school".to_string());
    }
    if num_students == 0 {
        return Err("Must have at least one student".to_string());
    }
    if school_capacities.len() != num_schools {
        return Err("Number of capacities must match number of schools".to_string());
    }

    // Validate school preferences
    for (school_id, prefs) in school_preferences.iter().enumerate() {
        let unique_prefs: std::collections::HashSet<_> = prefs.iter().collect();
        if unique_prefs.len() != prefs.len() {
            return Err(format!("School {} has duplicate students in preferences", school_id));
        }
        if prefs.iter().any(|&s| s >= num_students) {
            return Err(format!("School {} has invalid student ID in preferences", school_id));
        }
    }

    // Validate student preferences
    for (student_id, prefs) in student_preferences.iter().enumerate() {
        let unique_prefs: std::collections::HashSet<_> = prefs.iter().collect();
        if unique_prefs.len() != prefs.len() {
            return Err(format!("Student {} has duplicate schools in preferences", student_id));
        }
        if prefs.iter().any(|&s| s >= num_schools) {
            return Err(format!("Student {} has invalid school ID in preferences", student_id));
        }
    }

    // Validate capacities
    if school_capacities.iter().any(|&c| c == 0) {
        return Err("All school capacities must be positive".to_string());
    }

    Ok(())
}

#[pyfunction]
fn match_students_to_schools(
    student_preferences: Vec<Vec<usize>>,
    school_preferences: Vec<Vec<usize>>,
    school_capacities: Vec<usize>
) -> PyResult<HashMap<usize, usize>> {
    // Validate inputs
    if let Err(msg) = validate_inputs(&student_preferences, &school_preferences, &school_capacities) {
        return Err(PyValueError::new_err(msg));
    }

    let num_students = student_preferences.len();

    // Initialize schools
    let mut schools: Vec<School> = school_preferences
        .into_iter()
        .zip(school_capacities)
        .map(|(prefs, cap)| School::new(cap, prefs))
        .collect();

    // Initialize student state
    let mut unmatched_students: VecDeque<usize> = (0..num_students).collect();
    let mut student_next_proposal: Vec<usize> = vec![0; num_students];
    let mut student_assignments: HashMap<usize, usize> = HashMap::with_capacity(num_students);

    // Main matching loop
    while let Some(student) = unmatched_students.pop_front() {
        let student_prefs = &student_preferences[student];
        
        // Skip students with empty preference lists
        if student_prefs.is_empty() {
            continue;
        }

        // Skip if student has exhausted preferences
        if student_next_proposal[student] >= student_prefs.len() {
            continue;
        }

        let school_id = student_prefs[student_next_proposal[student]];
        student_next_proposal[student] += 1;

        let school = &mut schools[school_id];
        
        if let Some((accepted, maybe_rejected)) = school.would_accept(student) {
            if accepted {
                if let Some(rejected_student) = maybe_rejected {
                    school.remove_student(rejected_student);
                    student_assignments.remove(&rejected_student);
                    unmatched_students.push_back(rejected_student);
                }
                school.add_student(student);
                student_assignments.insert(student, school_id);
            } else {
                unmatched_students.push_back(student);
            }
        }
    }

    Ok(student_assignments)
}

#[pymodule]
fn gale_shapley(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(match_students_to_schools, m)?)?;
    Ok(())
}