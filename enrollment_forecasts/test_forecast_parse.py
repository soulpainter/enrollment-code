#!/usr/local/bin/python

from process_input import ProcessInputCSV
import time
import sys

# FIRST GET OUR FULL FORECAST WITH CURRENT DATA
weights = [3,2,1]
realParser = ProcessInputCSV('data/rose_valley.csv', weights)
realParser.createForecast()

lastYearRealSum = realParser.getSums()[-1]

# NOW GET OUR TEST DATA FORECAST; WE WILL COMPARE THE SUM THIS
# FORECAST GETS FOR THIS YEAR WITH THE ACTUAL NUMBERS
weights = [3,2,1]
parser = ProcessInputCSV('data/small_rose_valley.csv', weights)
parser.createForecast()

use = 3
maxnum = 101

closestSum = 0
closestWeights = []

defaultWeights = {}

counter = 0

print "TIME START: " + (time.strftime("%H:%M:%S"))
for x in range(1, maxnum):
  #print "TIME X START: " + (time.strftime("%H:%M:%S"))
  sys.stdout.write('.')
  sys.stdout.flush()
  for y in range(1, maxnum):
    for z in range(1, maxnum):
      weights = [x,y,z]
      msg = '{}, {}, {}'.format(x,y,z)
      #print msg

      parser.setWeights(weights)
      parser.createForecast()
      #print parser.getForecast()
      #print parser.getSums()
      firstYearForecastSum = parser.getForecastSums()[0]
      #print "FORECAST & REAL SUM: " , firstYearForecastSum, lastYearRealSum

      if weights == [3,2,1]:
        defaultWeights["3_2_1"] = firstYearForecastSum
      elif weights == [1,1,1]:
        defaultWeights["1_1_1"] = firstYearForecastSum
      elif weights == [1,2,3]:
        defaultWeights["1_2_3"] = firstYearForecastSum

      absoluteDiff = abs(lastYearRealSum - firstYearForecastSum)
      if absoluteDiff < abs(lastYearRealSum - closestSum):
        closestSum = firstYearForecastSum
        closestWeights = weights

      counter += 1

print "LAST YEAR REAL: ", lastYearRealSum
print "# OF WEIGHTS RUN: ", counter
print "NUMBERS RUN THROUGH: 1 -" , maxnum - 1
print "FORECAST: ", closestSum
print "FORECASE WEIGHTS: ", closestWeights
print "DEFAULT WEIGHTS: ", defaultWeights

print "TIME END: " + (time.strftime("%H:%M:%S"))

# LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
#for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
#  print g, v, d, a

# THIS PRINTS OUT THE COLUMNS SUMS
#print parser.getSums()

# THIS PRINTS OUT THE FORECAST
#print parser.getForecast()
#print parser.getForecastSums()

