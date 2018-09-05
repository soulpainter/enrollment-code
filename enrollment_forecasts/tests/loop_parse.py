#!/usr/local/bin/python

from lib.process_input import ProcessInputCSV
import time

use = 3
maxnum = 11 

weights = [3,2,1];
parser = ProcessInputCSV('data/rose_valley.csv', weights)
parser.createForecast()

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


