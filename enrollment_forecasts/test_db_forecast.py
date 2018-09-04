from sqlalchemy import create_engine, text
from lib.process_input import ProcessInputCSV
import numpy as np
import time
import sys

# FIRST GET OUR FULL FORECAST WITH CURRENT DATA
weights = [3,2,1]
parser = ProcessInputCSV('data/rose_valley.csv', weights)
parser.createForecast()

lastYearRealSum = parser.getSums()[-1]

# Create an engine to the census database
db = create_engine('mysql+pymysql://root:&$#$JFl23asfjA)8wfLFr29&^@localhost/CaliforniaEnrollment')

# THIS IS THE DISTRICT I INITALLY WORKED WITH: ROSS VALLEY
districtSql = "SELECT * FROM Districts d WHERE d.id = 290"

# THIS IS ALL OF THE DISTRICTS
districtSql = "SELECT d.id as districtId, d.name as districtName FROM Districts d"

# NOT ENOUGH DATA TO CALCULATE THIS
#districtSql = "SELECT * FROM Districts d WHERE d.id = 35"

sql = text(districtSql)
result = db.engine.execute(sql)
names = []

print "TIME START: " + (time.strftime("%H:%M:%S"))
print "=========================="

for row in result:
  district = []

  print "Running forecast on ", row[1], " ( ", row[0], " )"

  countSql = text("SELECT year, sum(kdgn) as 'K', sum(gr_1) as '1', sum(gr_2) as '2', sum(gr_3) as '3', sum(gr_4) as '4', sum(gr_5) as '5', sum(gr_6) as '6', sum(gr_7) as '7', sum(gr_8) as '8', sum(gr_9) as '9', sum(gr_10) as '10', sum(gr_11) as '11', sum(gr_12) as '12' FROM Districts d JOIN Schools s ON s.district_id = d.id JOIN SchoolGradeCounts c ON c.school_id = s.id WHERE d.id =" + str(row[0]) + " GROUP BY d.id, year LIMIT 6")
  countResults = db.engine.execute(countSql)

  for count in countResults:
    headers = (count.keys())
    tmpData = []
    for item in count:
      tmpData.append(float(item))
    district.append(tmpData)

  counter = 0
  newTuple = ()
  newInputData = []
  for header in headers:
    if(header == 'year'):
      newHeader = float(9999)
    elif header.isdigit():
      newHeader = float(header)
    else:
      newHeader = float(0)
      #newHeader = str(header)

    newTuple = tuple(j for i in (newTuple, (float(newHeader))) for j in (i if isinstance(i, tuple) else (float(i),)))
    counter += 1

  district = [newTuple] + district

  inputData = np.asarray(district).transpose()[1:]

  for data in inputData:
    newInputData.append(tuple(data))

  use = 3
  maxnum = 101

  closestSum = 0
  closestWeights = []

  defaultWeights = {}

  counter = 0
  #print "TIME START: " + (time.strftime("%H:%M:%S"))
  for x in range(1, maxnum):
    #print "TIME X START: " + (time.strftime("%H:%M:%S"))
    sys.stdout.write('.')
    sys.stdout.flush()
    for y in range(1, maxnum):
      for z in range(1, maxnum):
        weights = [x,y,z]
        msg = '{}, {}, {}'.format(x,y,z)
        #print msg

        parser.setMatrix(inputData, weights)
        parser.setWeights(weights)
        parser.createForecast()
        #print parser.getForecast()
        #print parser.getSums()
        #firstYearForecastSum = parser.getForecastSums()[0]
        #print "FORECAST & REAL SUM: " , firstYearForecastSum, lastYearRealSum

        #if weights == [3,2,1]:
        #  defaultWeights["3_2_1"] = firstYearForecastSum
        #elif weights == [1,1,1]:
        #  defaultWeights["1_1_1"] = firstYearForecastSum
        #elif weights == [1,2,3]:
        #  defaultWeights["1_2_3"] = firstYearForecastSum

        #absoluteDiff = abs(lastYearRealSum - firstYearForecastSum)
        #if absoluteDiff < abs(lastYearRealSum - closestSum):
        #  closestSum = firstYearForecastSum
        #  closestWeights = weights
#
        counter += 1

    #if parser.didForecase() == 1:
      # LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
      #for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
      #  print g, v, d, a

      # THIS PRINTS OUT THE COLUMNS SUMS
      #print parser.getSums()

      # THIS PRINTS OUT THE FORECAST
      #print parser.getForecast()
    #  print parser.getForecastSums() 
    #else:
    #  print "Not enough information to do forecast"

  print ""
#  print "LAST YEAR REAL: ", lastYearRealSum
#  print "# OF WEIGHTS RUN: ", counter
#  print "NUMBERS RUN THROUGH: 1 -" , maxnum - 1
#  print "FORECAST: ", closestSum
#  print "FORECASE WEIGHTS: ", closestWeights
#  print "DEFAULT WEIGHTS: ", defaultWeights

  #print "TIME END: " + (time.strftime("%H:%M:%S"))

  print "==================================="

print "TIME END: " + (time.strftime("%H:%M:%S"))
