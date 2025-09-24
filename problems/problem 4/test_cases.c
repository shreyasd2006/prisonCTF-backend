#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int maxPathSum(int** grid, int m, int n);

int failures = 0;

void check(int **grid, int m, int n, int expected) {
    int result = maxPathSum(grid, m, n);
    if (result == expected) {
        printf("PASS\n");
    } else {
        printf("FAIL Expected=%d Got=%d\n", expected, result);
        failures++;
    }
}

int main() {
    // Sample test
    int g1_data[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    int* g1[3] = {g1_data[0], g1_data[1], g1_data[2]};
    check(g1, 3, 3, 29);

    // Hidden test 1
    int g2_data[2][2] = {{-1,2},{1,3}};
    int* g2[2] = {g2_data[0], g2_data[1]};
    check(g2, 2, 2, 4);

    // Hidden test 2 (PDF says 11, but real max path is 12 ✅)
    int g3_data[3][4] = {{1,2,3,4},{2,2,1,1},{5,1,1,1}};
    int* g3[3] = {g3_data[0], g3_data[1], g3_data[2]};
    check(g3, 3, 4, 12);

    // Hidden test 3
    int g4_data[4][4] = {
        {1,1,1,1},
        {1,1,1,1},
        {1,1,1,1},
        {1,1,1,9}
    };
    int* g4[4] = {g4_data[0], g4_data[1], g4_data[2], g4_data[3]};
    check(g4, 4, 4, 15);

    if (failures > 0) return 1;
    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int maxPathSum(int** grid, int m, int n);

int failures = 0;

void check(int **grid, int m, int n, int expected) {
    int result = maxPathSum(grid, m, n);
    if (result == expected) {
        printf("PASS\n");
    } else {
        printf("FAIL Expected=%d Got=%d\n", expected, result);
        failures++;
    }
}

int main() {
    // Sample test
    int g1_data[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    int* g1[3] = {g1_data[0], g1_data[1], g1_data[2]};
    check(g1, 3, 3, 29);

    // Hidden test 1
    int g2_data[2][2] = {{-1,2},{1,3}};
    int* g2[2] = {g2_data[0], g2_data[1]};
    check(g2, 2, 2, 4);

    // Hidden test 2 (PDF says 11, but real max path is 12 ✅)
    int g3_data[3][4] = {{1,2,3,4},{2,2,1,1},{5,1,1,1}};
    int* g3[3] = {g3_data[0], g3_data[1], g3_data[2]};
    check(g3, 3, 4, 12);

    // Hidden test 3
    int g4_data[4][4] = {
        {1,1,1,1},
        {1,1,1,1},
        {1,1,1,1},
        {1,1,1,9}
    };
    int* g4[4] = {g4_data[0], g4_data[1], g4_data[2], g4_data[3]};
    check(g4, 4, 4, 15);

    if (failures > 0) return 1;
    return 0;
}
