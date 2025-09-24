#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * The student's implementation should provide:
 *   char* encryptString(const char* s);
 * It must return a malloc'd string which the test runner will free().
 */

/* make failures file-local to avoid symbol clashes when linking multiple test files */
static int failures = 0;

void check(const char* input, const char* expected) {
    extern char* encryptString(const char* s); /* provided by student's solution.c */
    char* out = encryptString(input);
    if (!out) {
        printf("FAIL Input=%s Got=NULL\n", input);
        failures++;
        return;
    }
    if (strcmp(out, expected) == 0) {
        printf("PASS\n");
    } else {
        printf("FAIL Input=%s Expected=%s Got=%s\n", input, expected, out);
        failures++;
    }
    free(out);
}

int main() {
    check("hello123", "ihmmr321");
    check("programming2025!", "qsrhsdnnloh5202!"); /* corrected to vowel+3 rules */
    check("AeiOu", "DhlRx");
    check("testCASE123", "uhtuDDTH321");

    if (failures > 0) return 1;
    return 0;
}
