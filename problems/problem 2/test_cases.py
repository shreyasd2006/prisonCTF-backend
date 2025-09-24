import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ2(unittest.TestCase):
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
        self.assertEqual(self.run_solution("3\nflower\nflow\nflight\n"), "fl")

    def test_hidden(self):
        self.assertEqual(self.run_solution("4\ninterspecies\ninterstellar\ninterstate\ninternet\n"), "inter")
        self.assertEqual(self.run_solution("3\ndog\nracecar\ncar\n"), "")
        self.assertEqual(self.run_solution("2\nabcd\nabc\n"), "abc")

if __name__ == "__main__":
    unittest.main()
