// da_cpp.cpp

#include "da_cpp.hpp"

extern "C"
{
    void da_cpp(
        // std::vector<std::vector<int>> students_pref,
        // std::vector<std::vector<int>> schools_pref,
        // int *capacities,
        // int *result,
        // int n_students,
        // int n_schools);
        int students_preferences[][MAX_STUDENT_PREFERENCES],
        int schools_preferences[][MAX_SCHOOL_PREFERENCES],
        int *capacities,
        int *result,
        int n_students,
        int n_schools);
}

void da_cpp(
    int students_preferences[][MAX_STUDENT_PREFERENCES],
    int schools_preferences[][MAX_SCHOOL_PREFERENCES],
    int *capacities,
    int *result,
    int n_students,
    int n_schools)
// void deferred_acceptance(
//     std::vector<std::vector<int>> students_pref,
//     std::vector<std::vector<int>> schools_pref,
//     int *capacities,
//     int *result,
//     int n_students,
//     int n_schools)
{
    std::vector<std::vector<int>> students_pref(n_students, std::vector<int>(n_schools));
    std::vector<std::vector<int>> schools_pref(n_schools, std::vector<int>(n_students));
    std::vector<std::vector<int>> priority_order(n_schools, std::vector<int>(n_students));
    std::vector<std::vector<int>> school_students(n_schools);
    std::vector<int> proposals_remaining(n_students, 0);

    std::queue<int> free_students;
    std::vector<int> student_next(n_students, 0);

    // print preferences
    // std::cout << "first pref " << students_pref.size() << std::endl;
    // std::cout << "Student preferences: " << std::endl;
    // for (int i = 0; i < n_students; i++)
    // {
    //     std::cout << "length of pref " << i << " " << students_pref[i].size() << std::endl;
    //     for (int j = 0; j < students_pref[i].size(); j++)
    //     {

    //         std::cout << students_pref[i][j] << " ";
    //     }
    //     std::cout << std::endl;
    // }
    // std::cout << "School preferences: " << std::endl;
    // for (int i = 0; i < n_schools; i++)
    // {
    //     for (int j = 0; j < schools_pref[i].size(); j++)
    //     {
    //         std::cout << schools_pref[i][j] << " ";
    //     }
    //     std::cout << std::endl;
    // }

    for (int i = 0; i < n_students; i++)
    {
        // std::cout << "Student " << i << " preferences: " << sizeof(students_preferences[i])/sizeof(*students_preferences[i]) << std::endl;
        for (int j = 0; j < std::end(students_preferences[i]) - std::begin(students_preferences[i]); j++)
        {
            students_pref[i][j] = students_preferences[i][j];
            // proposals_remaining[i]++;
        }
        free_students.push(i);
    }
    // std::cout << "number of schools ranked ";
    // for (int i = 0; i < n_students; i++)
    // {
    //     std::cout << students_pref[i].size() << " ";
    // }
    // std::cout << std::endl;

    for (int i = 0; i < n_schools; i++)
    {
        for (int j = 0; j < n_students; j++)
        {
            schools_pref[i][j] = schools_preferences[i][j];
            priority_order[i][schools_pref[i][j]] = j;
        }
    }

    while (!free_students.empty())
    {
        int student = free_students.front();
        int school = students_pref[student][student_next[student]];

        if (school_students[school].size() < static_cast<std::vector<int>::size_type>(capacities[school]))
        {
            school_students[school].push_back(student);
            free_students.pop();
            // std::cout << "Student " << student << " matched with School " << school << std::endl;
        }
        else
        {
            // Find least preferred student in school's list
            int least_preferred_idx = 0;
            for (size_t i = 1; i < school_students[school].size(); i++)
            {
                if (priority_order[school][school_students[school][i]] > priority_order[school][school_students[school][least_preferred_idx]])
                {
                    least_preferred_idx = i;
                }
            }

            // If new student is preferred over the least preferred student in school's list
            if (priority_order[school][student] < priority_order[school][school_students[school][least_preferred_idx]])
            {
                int displaced_student = school_students[school][least_preferred_idx];
                school_students[school].erase(school_students[school].begin() + least_preferred_idx);
                school_students[school].push_back(student);
                free_students.push(displaced_student);
                free_students.pop();
                // std::cout << "Student " << student << " displaces" << displaced_student << " at School " << school << std::endl;
            }
            // else
            // {
            //     // std::cout << "Student " << student << " rejected by School " << school << std::endl;
            // }
        }

        student_next[student]++;
        if (static_cast<std::vector<int>::size_type>(student_next[student]) >= students_pref[student].size())
        {
            free_students.pop();
            // std::cout << "Student " << student << " has no more schools to apply to" << std::endl;
        }
    }

    for (int i = 0; i < n_students; i++)
    {
        result[i] = -1; // Indicates student has not been assigned a school
    }

    for (int i = 0; i < n_schools; i++)
    {
        for (int student : school_students[i])
        {
            result[student] = i;
        }
    }
}
