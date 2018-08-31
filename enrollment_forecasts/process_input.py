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
    values_len = len(npvalues[0])

    # FIRST GRADE
    loopDiffs = []
    for i in range(values_len-1):
      if i == 0:
        diff = np.diff(np.diagonal(npvalues, i, 1, 0)[0:2])[0]
        loopDiffs.append(diff)
      elif i == values_len-2:
        diff = np.diff(np.diagonal(npvalues, -i, 1, 0)[-i+1:])[0]
        loopDiffs.append(diff)
      else:
        diff = np.diff(np.diagonal(npvalues, -i, 1, 0)[0:2])[0]
        loopDiffs.append(diff)

    tempDiffs.append(loopDiffs)

    # SECOND GRADE
    loopDiffs = []
    startNum = 1
    for i in range(values_len-1):
      if i == 0:
        diff = np.diff(np.diagonal(npvalues, startNum, 1, 0)[0:2])[0]
        loopDiffs.append(diff)
      elif i == values_len-2:
        diff = np.diff(np.diagonal(npvalues, startNum, 1, 0)[-2:])[0]
        loopDiffs.append(diff)
      else:
        diff = np.diff(np.diagonal(npvalues, startNum, 1, 0)[1:3])[0]
        loopDiffs.append(diff)

      startNum -= 1

    tempDiffs.append(loopDiffs)

    # THIRD THROUGH THE LAST GRADE CAN BE DONE IN A LOOP; START WITH THE THIRD GRADE; SKIP K, 1 & 2
    startGrade = 3
    gradeLoops = len(npvalues) - startGrade
    cellCount = len(npvalues[0])
    cellCalcNum = cellCount - 1

    for loopNum in range(gradeLoops):

      grade = loopNum + startGrade

      cellDiffs = []
      for cell in range(cellCalcNum):
        if cell == cellCalcNum -1:
          diff = np.diff(np.diagonal(npvalues, grade - cellCalcNum, 1, 0)[-2:])[0]
        else:
          diff = np.diff(np.diagonal(npvalues, grade - cell - 1, 1, 0)[cell:cell+2])[0]

        cellDiffs.append(diff)
      
      tempDiffs.append(cellDiffs)

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
    self.forecastSums = self.generateSums(self.forecast)

  def getForecastSums(self):
    return self.forecastSums

  def generateSums(self, data):
    return np.sum(np.asarray(data), 0)

