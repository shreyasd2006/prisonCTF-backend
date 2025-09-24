import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ5(unittest.TestCase):
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
        self.assertEqual(self.run_solution("hello123\n"), "igopt321")

    def test_hidden(self):
        self.assertEqual(self.run_solution("programming2025!\n"), "qsphsbnnjoh5202!")
        self.assertEqual(self.run_solution("AeiOu\n"), "DhpRx")
        self.assertEqual(self.run_solution("testCASE123\n"), "uftuDBTF321")

if __name__ == "__main__":
    unittest.main()
