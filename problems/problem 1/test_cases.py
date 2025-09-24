import unittest, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOLUTION_PATH = os.path.join(SCRIPT_DIR, "solution.py")

class TestQ1(unittest.TestCase):
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
        self.assertEqual(self.run_solution("leetcode\n"), "l")
        self.assertEqual(self.run_solution("aabb\n"), "None")

    def test_hidden(self):
        self.assertEqual(self.run_solution("abcabcde\n"), "d")
        self.assertEqual(self.run_solution("aabbccddeeff\n"), "None")
        self.assertEqual(self.run_solution("swiss\n"), "w")

if __name__ == "__main__":
    unittest.main()
