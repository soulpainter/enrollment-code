from lib.ca_db import CaDb

# Import create_engine function
#from sqlalchemy import create_engine, text
from lib.process_input import ProcessInputCSV
import numpy as np

# Create an engine to the census database
#db = create_engine('mysql+pymysql://root:&$#$JFl23asfjA)8wfLFr29&^@localhost/CaliforniaEnrollment')

# Print the table names
#print(db.table_names())

#districtSql = "SELECT * FROM Districts d WHERE d.id = 290"
#districtSql = "SELECT d.id as districtId, d.name as districtName, s.id as schoolId, s.name as schoolName, s.cds_code as schoolCdsCode FROM Districts d JOIN Schools s ON s.district_id = d.id"
#districtSql = "SELECT d.id as districtId, d.name as districtName FROM Districts d"
#districtSql = "SELECT * FROM Districts d WHERE d.id = 35"

caDb = CaDb()
result = caDb.getDistricts()

names = []

print "=========================="

for row in result:
  district = []

  print "Running forecast on ", row[1], " ( ", row[0], " )"

  countResults = caDb.getSchoolGradeCounts(row[0])

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

  weights = [1,1,1]
  parser = ProcessInputCSV('data/rose_valley.csv', weights)

  parser.setMatrix(inputData, weights)
  parser.createForecast()

  if parser.didForecase() == 1:
    # LOOP THROUGH THE GRADES, THE VALUES OF THE GRADES, THE DIFFS BETWEEN GRADE VALUES
    for g, v, d, a in zip(parser.getGrades(), parser.getGradeValues(), parser.getDiffs(), parser.getDiffAvgs()):
      print g, v, d, a

    # THIS PRINTS OUT THE COLUMNS SUMS
    print parser.getSums()

    # THIS PRINTS OUT THE FORECAST
    print parser.getForecast()
    print parser.getForecastSums() 
  else:
    print "Not enough information to do forecast"

  print "==================================="


