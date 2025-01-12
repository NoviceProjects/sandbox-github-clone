#!/usr/bin/env python
# coding = utf-8
#
# Author: Archer Reilly
# Date: 23/DEC/2014
# File: CVKNN.py
# Desc: KNN -- K Nearest Neighbours, use KNN classifier
#
# Produced By CSRGXTU
import cv2
import numpy as np

from Utility import loadMatrixFromFile, loadSeasons, loadTeamIds

# buildTrainingSets
# build training sets from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTrainingSets(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    if (float(row[1]) - float(row[2])) < 0:
      leaguerank = 0
    else:
      leaguerank = 1
    res.append([row[0], leaguerank])

  return np.array(res).astype(np.float32)

# buildTrainingLabels
# build training labels from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTrainingLabels(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    if row[3] == 'W':
      WIN = 1
    else:
      WIN = 0
    res.append([[WIN]])

  return np.array(res).astype(np.float32)

# buildTestingSets
# build testing sets from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTestingSets(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    if (float(row[1]) - float(row[2])) < 0:
      leaguerank = 0
    else:
      leaguerank = 1
    res.append([row[0], leaguerank])

  return np.array(res).astype(np.float32)

# buildTestingLabels
# build testing labels from raw data file
#
# @param inputFile
# @return numpy.ndarray
def buildTestingLabels(inputFile):
  res = []
  mat = loadMatrixFromFile(inputFile)
  for row in mat:
    if row[3] == 'W':
      WIN = 1
    else:
      WIN = 0
    res.append([[WIN]])

  return np.array(res).astype(np.float32)

# teamMain
# train and test for team
def teamMain():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  teamIds = loadTeamIds(DIR + 'teamidshortname.csv')
  teamNames = [x[1] for x in loadMatrixFromFile(DIR + 'teamidshortname.csv')]
  countTotal = 0
  total = 0

  for team in teamIds:
    trainData = buildTrainingSets(DIR + team + '-train.csv')
    trainLabels = buildTrainingLabels(DIR + team + '-train.csv')
    testData = buildTestingSets(DIR + team + '-test.csv')
    testLabels = buildTestingLabels(DIR + team + '-test.csv')
    total = total + len(testLabels)

    knn = cv2.KNearest()
    knn.train(trainData, trainLabels)

    # Accuracy
    count = 0
    for i in range(len(testLabels)):
      ret, results, neighbours, dist = knn.find_nearest(np.array([testData[i]]), 11)
      if results[0][0] == testLabels[i][0]:
        count = count + 1

    countTotal = countTotal + count
    print 'INFO: Accuracy(', teamNames[teamIds.index(team)], ')', count/float(len(testLabels))
  print 'INFO: Total Accuracy: ', countTotal/float(total)

# seasonMain
# train and test for seasons
def seasonMain():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  seasons = loadSeasons(DIR + 'seasons-18-Nov-2014.txt')
  countTotal = 0
  total = 0

  for season in seasons:
    trainData = buildTrainingSets(DIR + season + '-train.csv')
    testData = buildTestingSets(DIR + season + '-test.csv')
    trainLabels = buildTestingLabels(DIR + season + '-train.csv')
    testLabels = buildTestingLabels(DIR + season + '-test.csv')
    total = total + len(testLabels)

    knn = cv2.KNearest()
    knn.train(trainData, trainLabels)

    # Accuracy
    count = 0
    for i in range(len(testLabels)):
      ret, results, neighbours, dist = knn.find_nearest(np.array([testData[i]]), 11)
      if results[0][0] == testLabels[i][0]:
        count = count + 1

    countTotal = countTotal + count
    print 'INFO: Accuracy(', season, ')', count/float(len(testLabels))

  print 'INFO: Total Accuracy: ', countTotal/float(total)

# main
# train and test for all
def main():
  DIR = '/home/archer/Documents/maxent/data/basketball/leaguerank/'
  seasons = loadSeasons(DIR + 'seasons-18-Nov-2014.txt')
  total = 0
  count = 0
  trainData = []
  trainLabels = []
  testData = []
  testLabels = []

  for season in seasons:
    tmpTrainData = buildTrainingSets(DIR + season + '-train.csv').tolist()
    tmpTrainLabels = buildTestingLabels(DIR + season + '-train.csv').tolist()
    tmpTestData = buildTestingSets(DIR + season + '-test.csv').tolist()
    tmpTestLabels = buildTestingLabels(DIR + season + '-test.csv').tolist()
    
    trainData.extend(tmpTrainData)
    trainLabels.extend(tmpTrainLabels)
    testData.extend(tmpTestData)
    testLabels.extend(tmpTestLabels)

  trainData = np.array(trainData).astype(np.float32)
  trainLabels = np.array(trainLabels).astype(np.float32)
  testData = np.array(testData).astype(np.float32)
  testLabels = np.array(testLabels).astype(np.float32)
  total = len(testLabels)

  knn = cv2.KNearest()
  knn.train(trainData, trainLabels)

  for i in range(len(testLabels)):
    ret, results, neighbours, dist = knn.find_nearest(np.array([testData[i]]), 21)
    if results[0][0] == testLabels[i][0]:
      count = count + 1
  
  print 'INFO: Total Accuracy: ', count/float(total)

if __name__ == '__main__':
  print "+++++++++++++++++Main+++++++++++++++++++++++++"
  main()
  print "+++++++++++++++++teamMain+++++++++++++++++++++++++"
  teamMain()
  print "+++++++++++++++++seasonMain+++++++++++++++++++++++++"
  seasonMain()
