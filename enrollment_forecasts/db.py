from lib.ca_db import CaDb
from lib.process_input import ProcessInputCSV
import numpy as np

caDb = CaDb()
allDistricts = caDb.getDistricts()

print "=========================="

for row in allDistricts:
  district = []

  print "Running forecast on ", row[1], " ( ", row[0], " )"

  gradeCountResults = caDb.getSchoolGradeCounts(row[0])

  for count in gradeCountResults:
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

  #print newTuple

  district = [newTuple] + district

  inputData = np.asarray(district).transpose()[1:]

  for data in inputData:
    newInputData.append(tuple(data))

  weights = [1,1,1]
  parser = ProcessInputCSV('data/rose_valley.csv', weights)

  #print newInputData
  parser.setMatrix(newInputData, weights)
  parser.createForecast()

  if parser.didForecast() == 1:
    # LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
    #for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
    #  print g, v, d, a

    # THIS PRINTS OUT THE COLUMNS SUMS
    #print parser.getSums()

    # THIS PRINTS OUT THE FORECAST
    #print parser.getForecast()
    print parser.getForecastSums() 
  else:
    print "Not enough information to do forecast"

  print "==================================="


