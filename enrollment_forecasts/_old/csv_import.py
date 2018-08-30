#!/usr/local/bin/python

import numpy as np
import time

class ProcessInputCSV:

  inputFile = ''
  matrix = []
  diffs = []
  diffAvgs = []
  grades = []
  gradeValues = []
  sums = []
  forecast = []
  forecastSums = []

  weights = []
  weightSum = 0

  forecastYears = 10

  def __init__ (self, inputFile, weights):
    self.inputFile = inputFile
    self.matrix = np.genfromtxt(self.inputFile ,delimiter=',', skip_header=0, names=True, dtype=None)

    self.setWeights(weights)
    self.setGrades()
    self.setGradeValues()
    self.setDiffs()
    self.setDiffAvgs()
    self.setSums()

  def getMatrix(self):
    return self.matrix

  def setWeights(self, weights):
    self.weights = weights
    self.weightSum = sum(weights)

  def getWeights(self):
    return self.weights

  def createForecast(self):
    self.forecast = []
    self.forecastSums = []
    self.diffAvgs = []

    self.setDiffAvgs()
    self.setForecast()
    self.setForecastSums()

  def setGrades(self):
      self.grades = [i[0] for i in self.getMatrix()]

  def getGrades(self):
    return self.grades

  def setGradeValues(self):
      self.gradeValues = [el[1:] for el in (tuple(x) for x in self.getMatrix())]

  def getGradeValues(self):
    return self.gradeValues

  def setDiffs(self):
    tempDiffs = []

    # DO KINDERGARDEN
    tempDiffs.append(np.diff(self.gradeValues[0]))

    columnSize = len(self.gradeValues[0])

    counter = 0

    # DO ALL OTHER GRADES
    npvalues = np.asarray(self.gradeValues)

    # FIRST GRADE
    fourthDiff = np.diff(np.diagonal(npvalues, -3, 1, 0)[-2:])[0]
    thirdDiff = np.diff(np.diagonal(npvalues, -2, 1, 0)[0:2])[0]
    secondDiff = np.diff(np.diagonal(npvalues, -1, 1, 0)[0:2])[0]
    firstDiff = np.diff(np.diagonal(npvalues, 0, 1, 0)[0:2])[0]
    tempDiffs.append([firstDiff, secondDiff, thirdDiff, fourthDiff])

    # SECOND GRADE
    fourthDiff = np.diff(np.diagonal(npvalues, -2, 1, 0)[-2:])[0]
    thirdDiff = np.diff(np.diagonal(npvalues, -1, 1, 0)[1:3])[0]
    secondDiff = np.diff(np.diagonal(npvalues, 0, 1, 0)[1:3])[0]
    firstDiff = np.diff(np.diagonal(npvalues, 1, 1, 0)[0:2])[0]
    tempDiffs.append([firstDiff, secondDiff, thirdDiff, fourthDiff])

    # THIRD THROUGH THE LAST GRADE CAN BE DONE IN A LOOP
    start = 3
    loops = len(npvalues) - start

    fourthIndex = -1
    thirdIndex = 0
    secondIndex = 1
    firstIndex = 2

    for i in range(loops):
      fourthDiff = np.diff(np.diagonal(npvalues, fourthIndex, 1, 0)[-2:])[0]
      thirdDiff = np.diff(np.diagonal(npvalues, thirdIndex, 1, 0)[2:4])[0]
      secondDiff = np.diff(np.diagonal(npvalues, secondIndex, 1, 0)[1:3])[0]
      firstDiff = np.diff(np.diagonal(npvalues, firstIndex, 1, 0)[0:2])[0]
      tempDiffs.append([firstDiff, secondDiff, thirdDiff, fourthDiff])

      fourthIndex += 1
      thirdIndex += 1
      secondIndex += 1
      firstIndex += 1

    self.diffs = np.asarray(tempDiffs)

  def getDiffs(self):
    return self.diffs

  def setDiffAvgs(self):
    # THIS WAY ONLY WORKS FOR KINDERGARDEN
    weightsValues = np.array(self.weights) * np.array(np.flipud(self.diffs[0])[0:3])
    self.diffAvgs.append(sum(weightsValues) / float(self.weightSum))

    # NEED TO FIGURE OUT SOMETHING FOR ALL OTHER GRADES - THIS DOESNT WORK
    for row in self.diffs[1:]:
      firstThreeValues = (np.flipud(row)[0:3])
      weightsValues = np.array(self.weights) * np.array(firstThreeValues)
      self.diffAvgs.append(sum(weightsValues) / float(self.weightSum))
  
  def getDiffAvgs(self):
    return self.diffAvgs

  def setSums(self):
    self.sums = self.generateSums(self.gradeValues)

  def getSums(self):
    return self.sums

  def setForecast(self):
    # KINDERGARDEN
    kinderStartNum = self.gradeValues[0][-1]
    kinderYears = []
    for i in range(self.forecastYears):
      kinderStartNum += self.diffAvgs[0]
      kinderYears.append(kinderStartNum)

    self.forecast.append(kinderYears)

    for i in range(len(self.diffAvgs)):
      if i == 0:
        continue
      else:
        values = []
        for j in range(self.forecastYears):
          if j == 0:
            values.append(self.gradeValues[i-1][-1] + self.diffAvgs[i])
          else:
            values.append(self.forecast[i-1][j-1] + self.diffAvgs[i])
        self.forecast.append(values)

  def getForecast(self):
    return self.forecast

  def setForecastSums(self):
    print "SET FORECAST SUMS"
    self.forecastSums = self.generateSums(self.forecast)

  def getForecastSums(self):
    return self.forecastSums

  def generateSums(self, data):
    return np.sum(np.asarray(data), 0)

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

