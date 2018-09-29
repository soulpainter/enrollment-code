import numpy as np

def checkIgnore(weight, scores, counter):
  #print "WEIGHTS: ", weight
  check = [1 if num%10==0 else 0 for num in weight]
  if np.sum(check) == 3:
    print "IGNORE COUNTER: " , counter
    return 1
  else:
    return 0
    #for score in scores:
      #print "SCORES: ", score

    # avg = np.asarray(weight) * score / np.sum(weight)
    #  print "AVG: ", avg

#weights = ([3,2,1],[1,1,1])
weights = ([3.0,2.0,1.0], [30.0, 20.0, 10.0], [20.0,15.0,40.0],[200.0,150.0,400.0])

#scores = ([1,2,3], [10,20,30],[100,200,300])
scores = ([1,2,3],)

maxNum = 101
counter = 0

for i in range(1,maxNum):
  for j in range(1, maxNum):
    for k in range(1, maxNum):
      weight = [float(i), float(j), float(k)]
      if checkIgnore(weight, scores, counter):
        counter = counter+1

print "TOTAL IGNORES: ", counter

