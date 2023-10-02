#include <iostream>
#include <vector>
#include "da_cpp.hpp" // Ensure you have included the appropriate header

int main() {
    int numStudents = 4;
    int numSchools = 3;

    std::vector<std::vector<int>> studentPreferences =  {{0, 1, 2}, {1, 0, 2}, {0, 2, 1}, {2, 1}};
    // int studentPreferences[4][] =  {{0, 1, 2}, {1, 0, 2}, {0, 2, 1}, {2, 1}};
    // int studentPreferences[4][3] =  {{0, 1, 2}, {1, 0, 2}, {0, 2, 1}, {2, 1, 0}};
    std::cout << studentPreferences[0][0] << std::endl;

        
    std::vector<std::vector<int>> schoolPreferences = {
        {2, 1, 3, 0},
        {0, 2, 1, 3},
        {1, 2, 0, 3}
    };

   int schoolCapacities[3] = {1, 1, 1};

    // set up the result vector
    int match[numStudents];
    
    deferred_acceptance(studentPreferences, schoolPreferences, schoolCapacities, match, numStudents, numSchools);

    // Print the results
    for (int i = 0; i < numStudents; ++i) {
        std::cout << "Student " << i << " matched with School " << match[i] << std::endl;
    }

    return 0;
}
