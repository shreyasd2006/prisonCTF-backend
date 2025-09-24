import unittest
import subprocess
import os
import sys

# Get the absolute path of the directory where this test script is located.
# This is the key to finding solution.py reliably.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, 'solution.py')

class TestQ9(unittest.TestCase):

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

    # These are your specific tests for Problem 9
    def test_samples(self):
        # I've added a sample test based on your hidden cases for a better user experience.
        out = self.run_solution("alice\n")
        self.assertIn("alice", out)

    def test_hidden(self):
        out = self.run_solution("bob\n")
        self.assertIn("bob", out)
        
        # This test checks if either '1' or 'i' is in the output, which is an interesting case.
        out = self.run_solution("1\n")
        self.assertTrue("1" in out or "i" in out)
        
        out = self.run_solution("alice\n")
        self.assertNotIn("bob", out)


if __name__ == '__main__':
    unittest.main()