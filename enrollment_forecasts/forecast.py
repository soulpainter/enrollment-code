from lib.ca_db import CaDb
from lib.process_input import ProcessInputCSV
import numpy as np

caDb = CaDb()
allDistricts = caDb.getDistricts()

print "=========================="

for row in allDistricts:
  district = []
  years = []

  print "Running forecast on ", row[1], " ( ", row[0], " )"

  gradeCountResults = caDb.getSchoolGradeCounts(row[0])

  for count in gradeCountResults:
    years.append(count['year'])
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

    newTuple = tuple(j for i in (newTuple, (float(newHeader))) for j in (i if isinstance(i, tuple) else (float(i),)))
    counter += 1

  district = [newTuple] + district

  inputData = np.asarray(district).transpose()[1:]

  for data in inputData:
    newInputData.append(tuple(data))

  #print newInputData
  weights = [3,2,1]
  parser = ProcessInputCSV('data/rose_valley.csv', weights)
  #parser.setMatrix(newInputData, weights)
  #parser.createForecast()
  #print parser.getSums()
  #exit()

  numberOfColumns = len(newInputData[0])
  numberOfListItems = len(newInputData)

  sectionInputData = [] 
  sectionInputYears = []

  for i in range(numberOfColumns):
    if i==0:
      continue
 
    districtInputData = [] 
    sliceYears = []

    firstIndex = i
    secondIndex = firstIndex + 4

    sliceData = [num[firstIndex:secondIndex] for num in newInputData]
    sliceYears = years[firstIndex-1:secondIndex-1]

    for idx in range(len(newTuple)):
      if idx == 0:
        continue

      districtInputData.append(newTuple[idx:idx+1] + sliceData[idx-1])

    if(len(sliceData[0])) == 4:
      sectionInfo = {'years':sliceYears,'inputData':districtInputData}
      sectionInputData.append(sectionInfo)

  #weights = [3,2,1]
  #parser = ProcessInputCSV('data/rose_valley.csv', weights)

  for sectionData in sectionInputData:
    parser.setMatrix(sectionData['inputData'], weights)
    parser.createForecast()

    if parser.didForecast() == 1:
      # LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
      #for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
      #  print g, v, d, a

      # THIS PRINTS OUT THE COLUMNS SUMS
      #print parser.getSums()

      # THIS PRINTS OUT THE FORECAST
      #print parser.getForecast()
      #print parser.getForecastSums() 
      #print years[-1]
      #print sectionData['years'][-1]
      #exit()

      for y, f in zip(parser.getSums(), range(sectionData['years'][0]-1, sectionData['years'][0]-1+len(parser.getSums()))):
        print "Real Year & Sum: ", y, f

      for y, f in zip(parser.getForecastSums(), range(sectionData['years'][-1], sectionData['years'][-1]+len(parser.getForecastSums()))):
        print "Forecast Year & Sum: ", y, f
    else:
      print "Not enough information to do forecast"

    print "+++++++++++"

  print "==================================="



