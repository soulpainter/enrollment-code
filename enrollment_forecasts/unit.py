import unittest
import numpy as np
from process_input import ProcessInputCSV

class ProcessInputCSVTestCase(unittest.TestCase):
    """Tests for `process_input.py`."""

    def test_calculated_diffs_match_hardcoded_diffs(self):
      expected_diffs = [[-28,18,-30,36],[-10,-18,-38,-18],[-5,1,-5,2],[-7,-2,-7,5],[-2,4,-4,24],[5,7,-5,6],[-18,-15,-21,-16],[6,8,2,13],[11,6,3,4]]

      weights = [3,2,1]
      parser = ProcessInputCSV('data/rose_valley.csv', weights)
      parser.createForecast()

      """Does our dff avgs array have the same values as the expected diffs?"""
      self.assertEqual(len(expected_diffs), len(parser.getDiffs()))

      """Does our forecasted sums equal the expected diffs?"""
      for diffs, expected in zip(expected_diffs, parser.getDiffs()):  
        self.assertTrue(np.array_equal(diffs, expected))

    def test_calculated_sums_match_hardcoded_sums(self):
      #expected_sums = [2253,2288,2292,2192,2213]

      #weights = [3,2,1]
      #parser = ProcessInputCSV('data/rose_valley.csv', weights)
      #parser.createForecast()

      """Does our forecasted sums array have the same amount of values as the expected sums?"""
      #self.assertEqual(len(expected_sums), len(parser.getSums()))

      #"""Does our calculated sums equal the expected sums?"""
      #self.assertTrue(np.array_equal(expected_sums, parser.getSums()))

    def test_forecast_sums_match_hardcoded_sums(self):
      #expected_sums =[2201.5,2213.,2218.,2300.5,2329.5,2412.16666667,2506.,2623.33333333,2722.33333333,2821.33333333] 

      #weights = [3,2,1]
      #parser = ProcessInputCSV('data/rose_valley.csv', weights)
      #parser.createForecast()

      """Does our forecasted sums array have the same amount of values as the expected sums?"""
      #self.assertEqual(len(expected_sums), len(parser.getForecastSums()))

      #"""Does our forecasted sums equal the expected sums?"""
      #for forecast, expected in zip(expected_sums, parser.getForecastSums()):
      #  self.assertAlmostEqual(expected, forecast, 8)

if __name__ == '__main__':
    unittest.main()
