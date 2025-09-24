import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ3(unittest.TestCase):
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
        expected = "0 2\n1 3"
        self.assertEqual(self.run_solution("5\n1 2 3 2 4\n4\n"), expected)

    def test_hidden(self):
        # ✅ changed to 0-based
        self.assertEqual(self.run_solution("6\n3 3 4 7 5 2\n10\n"), "0 3\n1 3")
        self.assertEqual(self.run_solution("4\n0 0 0 0\n0\n"), "0 1\n0 2\n0 3\n1 2\n1 3\n2 3")
        self.assertEqual(self.run_solution("5\n-1 -2 -3 -4 -5\n-8\n"), "2 4")

if __name__ == "__main__":
    unittest.main()
