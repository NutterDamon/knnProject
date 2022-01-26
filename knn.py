#Damon Nutter
#006315383
#CSE 5160
#kNN implementation
import math


#Function that finds the classification of a test instance.
#k is the number of nearest neighbors to check.
def classifier(trainingSet, test, k):
    distance = []
    for classification in trainingSet:
        for attributes in trainingSet[classification]:
            #calc euclidean distance of 7 attributes.
            i = 0
            values = []
            while i < len(attributes) - 1:
                values.append((attributes[i] - test[i])**2)
                i += 1
            e_distance = math.sqrt(sum(values))
            distance.append((e_distance,classification))
    distance = sorted(distance)[:k] #sort distance and select the first k distances

    count1 = 0; #how many match classification 1
    count2 = 0; #how many match classification 2
    count3 = 0; #how many match classification 3
    #loop over i = k distances to see which classification fits.
    for i in distance:
        if i[1] == 1:
            count1 += 1
        elif i[1] == 2:
            count2 += 1
        elif i[1] == 3:
            count3 += 1
    if count1>count2 and count1>count3:
        return 1
    elif count2>count1 and count2>count3:
        return 2
    else:
        return 3
#function to min-max normalize the dataset
def normalizeData(dataSet):
    #find max and minimum values
    maxVals = [0,0,0,0,0,0,0]
    minVals = [0,0,0,0,0,0,0]
    for classification in dataSet:
        for attributes in dataSet[classification]:
            i = 0
            while i < len(attributes) - 1:
                if maxVals[i] < attributes[i]:
                    maxVals[i] = attributes[i]
                if minVals[i] > attributes[i]:
                    minVals[i] = attributes[i]
                i += 1
    #normalize the values
    for classification in dataSet:
        for attributes in dataSet[classification]:
            i = 0
            while i < len(attributes) - 1:
                attributes[i] = (attributes[i] - minVals[i])/(maxVals[i] - minVals[i])
                i += 1
    return dataSet
#Read data into a dictionary with number of keys = number of different classifications
def readData(filename):
    dataSet ={1:[],2:[],3:[]}
    with open(filename, 'r') as reader:
        line = reader.readline() #read each line of data
        while line != '':
            attributes = line.split() #split each attribute
            for i in range(0, len(attributes)): 
                attributes[i] = float(attributes[i]) #convert each attribute from string to float
            if attributes[len(attributes)-1] == 1:
                dataSet[1].append(attributes)
            elif attributes[len(attributes)-1] == 2:
                dataSet[2].append(attributes)
            elif attributes[len(attributes)-1] == 3:
                dataSet[3].append(attributes)
            else:
                print("error, classification value should be 1, 2, or 3")
            line = reader.readline()
    return dataSet
#Splits the data into a training set and a test set. Test set has 1/m % of the data.
#training set has the remaining 1-1/m % of the data.
def splitSet(dataSet, m):
    count = 0
    trainingSet = {1:[],2:[],3:[]}
    testSet = {1:[],2:[],3:[]}
    percent = round(1/m,2)* 100
    for classification in dataSet:
        for attributes in dataSet[classification]:
            count += 1
            if count%m != 0:
                trainingSet[classification].append(attributes)
            else:
                testSet[classification].append(attributes)
    #print("Running classifier using " + str(percent) + " percent of the data as the test set")
    return [trainingSet, testSet];
#Function that runs the test set against the training set.
#function also returns the classification error                
def runClassifier(trainingSet, testSet, k):
    classifications=[]
    correct = 0
    wrong = 0
    for classification in testSet:
        for attributes in testSet[classification]:
            cl = classifier(trainingSet,attributes,k)#calling classification function
            classifications.append(cl)
            if cl == attributes[len(attributes)-1]:
                correct += 1
            else:
                wrong += 1
    total = correct + wrong
    percentCorrect = correct/total

    #print(str(correct) + " correct classifications.\n" + str(wrong) + " incorrect classifications.\n" +\
     #     "Percent correct is " + str(percentCorrect))
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return percentCorrect        
def main():
    file = "seeds_dataset.txt"  #data file
    dataSet = readData(file)    #data set from data file
    normData = normalizeData(dataSet)   #normalize the dataset
    #Run the data starting with m = 7 and k = 3
    avgs = []
    percentCorrect = []
    m = 7
    total = 0
    while m < 35:
        percentCorrect.clear()
        k = 3
        while k < 25:
            split = splitSet(normData, m)       #split the dataset into training and test set using m = 1/m % of the data.
            correct = runClassifier(split[0], split[1], k)   #run classifier on 2 data sets.
            percentCorrect.append(correct)
            k += 2
            total += 1
        if(len(percentCorrect)!= 0):
            avg = sum(percentCorrect)/len(percentCorrect)
            avgs.append(avg)
        else:
            print("div by zero")
        m += 1
    print("For k from 3 to 25.")
    m = 7
    i = 0
    while i < len(avgs):
        print("m = " + str(m) + ", average correct classification was: " + str(avgs[i]))
        m += 1
        k += 2
        i += 1
    print("The average accuracy for all testing sizes and k values: " + str(sum(avgs)/len(avgs)))
    print("Total tests ran: " + str(total))
if __name__ == '__main__':
    main()
