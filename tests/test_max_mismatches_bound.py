import random
import unittest

from crisprradar.core import DEMO, analyze


class MaxMismatchesBoundTest(unittest.TestCase):
    """analyze() previously accepted any max_mismatches value with no
    bound check. A uniform-random 20nt sequence matches a fixed guide by
    chance at ~15/20 positions (P(match)=1/4 per base), so a threshold
    anywhere near that noise floor turns "off-target scan" into "list
    every NGG site in the genome": every candidate passes regardless of
    any real similarity to the guide, and the specificity ranking becomes
    meaningless noise."""

    def test_rejects_max_mismatches_above_the_biologically_meaningful_ceiling(self):
        with self.assertRaisesRegex(ValueError, "max_mismatches must be between 0 and 8"):
            analyze({**DEMO, "max_mismatches": 15})

    def test_rejects_negative_max_mismatches(self):
        with self.assertRaisesRegex(ValueError, "max_mismatches must be between 0 and 8"):
            analyze({**DEMO, "max_mismatches": -1})

    def test_accepts_the_full_valid_range(self):
        for value in (0, 4, 8):
            result = analyze({**DEMO, "max_mismatches": value})
            self.assertIsInstance(result["candidate_hits"], int)

    def test_looser_threshold_finds_at_least_as_many_candidates(self):
        """A looser mismatch threshold always finds a superset of hits.
        Demonstrates why an unbounded ceiling matters: on a genome with no
        exact or near matches, tightening from 8 down to 0 mismatches
        eliminates candidates that share almost nothing with the guide."""
        rng = random.Random(2)
        genome = "".join(rng.choice("ACGT") for _ in range(4000))
        guide = "".join(rng.choice("ACGT") for _ in range(20))
        tight = analyze({"guide": guide, "genome": genome, "max_mismatches": 0})
        loose = analyze({"guide": guide, "genome": genome, "max_mismatches": 8})
        self.assertLessEqual(tight["candidate_hits"], loose["candidate_hits"])
        self.assertGreater(loose["candidate_hits"], 0)


if __name__ == "__main__":
    unittest.main()
