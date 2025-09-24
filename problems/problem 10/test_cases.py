import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ10(unittest.TestCase):
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
        self.assertEqual(
            self.run_solution("make_board 2 2\nset 0 0 X\n"),
            "[['X', ' '], [' ', ' ']]"
        )
        self.assertEqual(
            self.run_solution("make_board 3 3\nset 1 2 O\n"),
            "[[' ', ' ', ' '], [' ', ' ', 'O'], [' ', ' ', ' ']]"
        )

if __name__ == "__main__":
    unittest.main()
