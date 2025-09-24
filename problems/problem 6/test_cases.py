import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ6(unittest.TestCase):
    def run_solution(self, inp: str) -> str:
        result = subprocess.run(
            [sys.executable, SOLUTION_PATH],
            input=inp,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()

    def test_hidden(self):
        self.assertEqual(self.run_solution("madam\n"), "True")
        self.assertEqual(self.run_solution("abba\n"), "True")
        self.assertEqual(self.run_solution("abc\n"), "False")

if __name__ == "__main__":
    unittest.main()
