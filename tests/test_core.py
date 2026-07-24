import unittest

from crisprradar.core import DEMO, analyze, reverse_complement


class CrisprRadarTest(unittest.TestCase):
    def test_reverse_complement(self):
        self.assertEqual(reverse_complement("ACGT"), "ACGT")

    def test_demo_finds_exact_and_near_matches(self):
        result = analyze(DEMO)
        self.assertGreaterEqual(result["exact_sites"], 1)
        self.assertGreaterEqual(result["off_target_sites"], 2)
        self.assertEqual(result["highest_off_target_risk"]["mismatches"], 1)

    def test_rejects_bad_guide(self):
        with self.assertRaisesRegex(ValueError, "exactly 20"):
            analyze({"guide": "ACGT", "genome": "A" * 40})


if __name__ == "__main__":
    unittest.main()
