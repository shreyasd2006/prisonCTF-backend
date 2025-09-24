import unittest
import subprocess
import os
import sys

# Get the absolute path of the directory where this test script is located.
# This is the key to finding solution.py reliably.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, 'solution.py')

class TestQ5(unittest.TestCase):

    def run_solution(self, inp: str) -> str:
        """
        Runs the student's solution.py file as a subprocess,
        passing the input string to it.
        """
        if not os.path.exists(SOLUTION_PATH):
            return "Error: solution.py not found."

        try:
            # We provide the full, absolute path to the solution file.
            result = subprocess.run(
                [sys.executable, SOLUTION_PATH],
                input=inp.encode(),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                return f"Error in solution code: {result.stderr.strip()}"
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Error: Solution timed out."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    # These are your specific tests for Problem 5
    def test_samples(self):
        self.assertEqual(self.run_solution("hello123\n"), "igopt321")

    def test_hidden(self):
        self.assertEqual(self.run_solution("programming2025!\n"), "qsphsbnnjoh5202!")
        self.assertEqual(self.run_solution("AeiOu\n"), "DhpRx")
        self.assertEqual(self.run_solution("testCASE123\n"), "uftuDBTF321")

if __name__ == '__main__':
    unittest.main()