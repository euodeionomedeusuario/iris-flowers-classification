import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getTable(testSet, predictions):
	setosa = {"name": "Iris-setosa", "vp": 0, "vn": 0, "fn": 0, "fp": 0}
	versicolor = {"name": "Iris-versicolor", "vp": 0, "vn": 0, "fn": 0,"fp": 0}
	virginica = {"name": "Iris-virginica", "vp": 0, "vn": 0, "fn": 0, "fp": 0}

	for x in range(len(testSet)):
		#Verdadeiramente Positivo
		if testSet[x][-1] == predictions[x]:
			if(predictions[x] == "Iris-setosa"):
				setosa["vp"] += 1
			elif(predictions[x] == "Iris-versicolor"):
				versicolor["vp"] += 1
			elif(predictions[x] == "Iris-virginica"):
				virginica["vp"] += 1
				setosa["fp"] += 1
				versicolor["fp"] += 1
		#Falso Positivo
		else:
			if(predictions[x] == "Iris-setosa"):
				setosa["vn"] += 1
				versicolor["fp"] += 1
				virginica["fp"] += 1
			elif(predictions[x] == "Iris-versicolor"):
				versicolor["vn"] += 1
				setosa["fp"] += 1
				virginica["fp"] += 1
			elif(predictions[x] == "Iris-virginica"):
				virginica["vn"] += 1
				setosa["fp"] += 1
				versicolor["fp"] += 1
			if(testSet[x][-1] == "Iris-setosa"):
				setosa["fn"] += 1
			elif(testSet[x][-1] == "Iris-versicolor"):
				versicolor["fn"] += 1
			elif(testSet[x][-1] == "Iris-virginica"):
				virginica["fn"] += 1

	return [setosa, versicolor, virginica]

def getPrecision(table):
	for x in table:
		#Precision = VP / VP + FP

		precision = x["vp"] / (x["vp"] + x["fp"])

		print(x)
		print("Precision - " + str(precision))


def getSensitivity(table):
	for x in table:
		#sensitivity = VP / VP + FN

		sensitivity = x["vp"] / (x["vp"] + x["fn"])

		print(x)
		print("Sensitivity - " + str(sensitivity))

def getSpecificity(table):
	for x in table:
		#specificity = VP / VP + FN

		specificity = x["vn"] / (x["vn"] + x["fp"])

		print(x)
		print("Specificity - " + str(specificity))

def getFMeasure(table):
	for x in table:
		#Precision = VP / VP + FP
		precision = x["vp"] / (x["vp"] + x["fp"])

		#sensitivity = VP / VP + FN
		sensitivity = x["vp"] / (x["vp"] + x["fn"])

		f = 2 * (precision * sensitivity) / (precision + sensitivity)

		print(x)
		print("F Measure - " + str(f))

def getAccuracy(table):
	for x in table:
		accuracy = (x["vp"] + x["vn"]) / (x["vp"] + x["vn"] + x["fp"] + x["fn"])

		print(x)
		print("Accuracy - " + str(accuracy))


def main():
	trainingSet=[]
	testSet=[]
	split = 0.67

	loadDataset('iris.data', split, trainingSet, testSet)

	print('Train set: ' + repr(len(trainingSet)))
	print('Test set: ' + repr(len(testSet)))

	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))


	table = getTable(testSet, predictions)

	getPrecision(table)
	getSensitivity(table)
	getSpecificity(table)
	getFMeasure(table)
	getAccuracy(table)

main()
