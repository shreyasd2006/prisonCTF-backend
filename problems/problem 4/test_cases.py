import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ4(unittest.TestCase):
    def run_solution(self, inp: str) -> str:
        result = subprocess.run(
            [sys.executable, SOLUTION_PATH],
            input=inp,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()

    def test_samples(self):
        # Sample from PDF
        self.assertEqual(
            self.run_solution("3 3\n1 2 3\n4 5 6\n7 8 9\n"), "29"
        )

    def test_hidden(self):
        # Hidden test 1
        self.assertEqual(
            self.run_solution("2 2\n-1 2\n1 3\n"), "4"
        )
        # Hidden test 2 (PDF said 11, but true max is 12 ✅)
        self.assertEqual(
            self.run_solution("3 4\n1 2 3 4\n2 2 1 1\n5 1 1 1\n"), "12"
        )
        # Hidden test 3
        self.assertEqual(
            self.run_solution("4 4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 9\n"), "15"
        )

if __name__ == "__main__":
    unittest.main()
