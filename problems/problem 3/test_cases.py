import unittest
import subprocess
import os
import sys

# Get the absolute path of the directory where this test script is located.
# This is the key to finding solution.py reliably.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, 'solution.py')

class TestQ3(unittest.TestCase):

    def run_solution(self, inp: str) -> list[str]:
        """
        Runs the student's solution.py file as a subprocess,
        passing the input string to it and returning a list of output lines.
        """
        if not os.path.exists(SOLUTION_PATH):
            return ["Error: solution.py not found."]

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
                return [f"Error in solution code: {result.stderr.strip()}"]
            
            lines = result.stdout.strip().splitlines()
            # Handle case where output is empty or just whitespace
            if lines == ['']:
                return []
            return lines
        except subprocess.TimeoutExpired:
            return ["Error: Solution timed out."]
        except Exception as e:
            return [f"An unexpected error occurred: {e}"]

    def assertListEqualIgnoreOrder(self, list1, list2):
        """Helper to assert two lists of strings are equal ignoring order"""
        self.assertEqual(set(list1), set(list2))

    # These are your specific tests for Problem 3
    def test_samples(self):
        inp = "5\n1 2 3 2 4\n4\n"
        self.assertListEqualIgnoreOrder(self.run_solution(inp), ["0 2", "1 3"])

    def test_hidden(self):
        inp = "6\n3 3 4 7 5 2\n10\n"
        self.assertListEqualIgnoreOrder(self.run_solution(inp), ["1 3", "2 4"])
        
        inp = "4\n0 0 0 0\n0\n"
        self.assertListEqualIgnoreOrder(self.run_solution(inp),
            ["0 1", "0 2", "0 3", "1 2", "1 3", "2 3"])
        
        inp = "5\n-1 -2 -3 -4 -5\n-8\n"
        self.assertListEqualIgnoreOrder(self.run_solution(inp), ["2 4"])

if __name__ == "__main__":
    unittest.main()
