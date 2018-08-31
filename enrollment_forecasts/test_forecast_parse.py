#!/usr/local/bin/python

from process_input import ProcessInputCSV

weights = [3,2,1]
parser = ProcessInputCSV('data/small_rose_valley.csv', weights)
parser.createForecast()

# LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
  print g, v, d, a

# THIS PRINTS OUT THE COLUMNS SUMS
print parser.getSums()

# THIS PRINTS OUT THE FORECAST
print parser.getForecast()
print parser.getForecastSums()

