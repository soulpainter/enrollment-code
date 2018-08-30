#!/usr/local/bin/python

from process_input import ProcessInputCSV
import time

use = 3
maxnum = 101 

weights = [3,2,1]
parser = ProcessInputCSV('data/rose_valley.csv', weights)

parser.createForecast()

print parser.getSums()
print parser.getForecast()
print parser.getForecastSums()

exit()

print "TIME START: " + (time.strftime("%H:%M:%S"))
for x in range(1, maxnum):
  print "TIME X START: " + (time.strftime("%H:%M:%S"))
  for y in range(1, maxnum):
    for z in range(1, maxnum):
      weights = [x,y,z]
      msg = '{}, {}, {}'.format(x,y,z)
      #print msg

      parser.setWeights(weights)
      parser.createForecast()
      #print parser.getForecast()
      #print parser.getSums()

print "TIME END: " + (time.strftime("%H:%M:%S"))
exit()

weights = [3,2,1];
parser = ProcessInputCSV('data/rose_valley.csv', weights)
parser.createForecast()

grades = parser.getGrades()
gradeValues = parser.getGradeValues()
diffs = parser.getDiffs()
sums = parser.getSums()
diffAvgs = parser.getDiffAvgs()
forecast = parser.getForecast()

# LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
for g, v, d, a in zip(grades, gradeValues, diffs, diffAvgs):
  print g, v, d, a

# THIS PRINTS OUT THE COLUMNS SUMS
print sums

print forecast

exit()

