import unittest
import numpy as np
from process_input import ProcessInputCSV

class ProcessInputCSVTestCase(unittest.TestCase):
    """Tests for `process_input.py`."""

    def test_calculated_sums_match_hardcoded_sums(self):
      expected_sums = [2253,2288,2292,2192,2213]

      weights = [3,2,1]
      parser = ProcessInputCSV('data/rose_valley.csv', weights)
      parser.createForecast()

      """Does our calculated sums equal the expected sums?"""
      self.assertTrue(np.array_equal(expected_sums, parser.getSums()))

if __name__ == '__main__':
    unittest.main()
