#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* encryptString(const char* s);

static int failures = 0;

void check(const char* input, const char* expected) {
    char* output = encryptString(input);
    if (strcmp(output, expected) == 0) {
        printf("PASS\n");
    } else {
        printf("FAIL Input=%s Expected=%s Got=%s\n", input, expected, output);
        failures++;
    }
    free(output);
}

int main() {
    check("hello123", "ihmmr321");
    check("programming2025!", "qsrhsdnnloh5202!"); // fixed
    check("AeiOu", "DhlRx");
    check("testCASE123", "uhtuDDTH321");

    if (failures > 0) return 1;
    return 0;
}
