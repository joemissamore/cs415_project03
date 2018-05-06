import time
import random
import matplotlib.pyplot as plt

def graph(n, cap):
    """
    Time the graph
    Capacity will be fixed
    Number of elements will increase by 1
    An element defined has:
        - Weight
        - Value
    The weight and value have no bearing on the calculation performed.
    What impacts the run time of this algorithm are 2 things:
        1. The capacity
        2. The number of items.
    Initially:
        The weight per item will be 1.
        The value per item will be 1.
    """
    capacity = cap

    X = []
    XrandValue = [] # random data
    XrandWeight = [] # rand weight
    Y = []
    Ygreedy = []
    for i in range(1, n):
        X.append(i)  #number of items
        XrandWeight.append(random.randint(1,10))
        XrandValue.append(random.randint(1,10))

        #initialize the vector
        vec = [[0]*(capacity + 1) for x in range(i)]
        startTime = time.time()
        knapSack(vec, capacity, X, X, True)
        Y.append((time.time() - startTime) * 1000000) # time

        startTimeGreedy = time.time()
        knapSackGreedy(capacity, X, X, debug=False)
        Ygreedy.append((time.time() - startTimeGreedy) * 1000000)


    graph1 = plt
    graph1.scatter(X, Y, color='red', label="Knapsack Dynamic")
    graph1.scatter(X, Ygreedy, color='blue', label="Knapsack Greedy")
    graph1.xlabel('Number of elements')
    graph1.ylabel('Amount of time (microseconds)')
    graph1.legend(loc=0)
    graph1.show()


def loadFile(filename):
    """
    Input:
        Filename
    Return:
        A list of integer values read in from a file
    """
    a = []
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip() # strip all white spaces
            a.append(line) # append the 'string'

    a = [int(x) for x in a] # take the 'string' and turn it into an int

    return a # return the list of ints

def knapSack(F, capacity, valueList, weightList, isTimingSub=False, debug=False):
    """
    Input:
        F = initalized list of values
        capacity = capacity of knapsack
        valueList = list of values
        weightList = list of weights
    This is a void function and just edits F.
    """
    if isTimingSub:
        timetime = []

    for i in range(len(F)): # row
        if isTimingSub:
            start = time.time()

        for j in range(len(F[i])): # column (# of items)
            value = 0 # compiler was complaining

            if j < weightList[i]:
                value = F[i-1][j]

            else:
                firstChoice = F[i-1][j]
                secondChoice = valueList[i] + F[i-1][j-weightList[i]]
                value = max(firstChoice, secondChoice)

            F[i][j] = value

        if isTimingSub:
            timetime.append(time.time()-start)

    if isTimingSub and debug:
        for i in range(len(timetime)):
            print ('Number of elements: ' + str(i) + ': ' + str(timetime[i] * 1000000))


def knapSackGreedy(capacity, valueList, weightList, debug=False):
    """
    Input:
        capacity = capacity of knapsack
        valueList = list of values
        weightList = list of weights
        debug = display debugging information

    Return: A knapsack using the greedy approach
    """
    #********************************************
    # List of list(s)
    # [ratio, weight, value, original position]
    ratio = []
    #********************************************

    for i in range(len(valueList)):
        ratio.append([float(valueList[i] / weightList[i]), weightList[i], valueList[i], int(i)])

    ratio.sort(reverse=True) # Sort from highest to lowest value

    sack = []
    for i in ratio:
        if i[1] <= capacity:
            sack.append(i)
            capacity -= i[1]

        if capacity == 0:
            break

    #********************************************
    # Purely debugging

    if debug:
        print ('\nPrinting ratio...')
        for i in ratio:
            print (i)

        print ("\nPrinting sack...")
        for i in sack:
            print (i)
    #********************************************

    return sack


def subset(F,capacity,valueList, weightList):
    """
    Input:
        F = Vector that has already been populated by
            dynamic knapsack function
        capacity = knapsack capacity
        valueList = List of values
        weightList = List of weights

    Output: Optimal subset
    """
    subset = []
    i = len(F) - 1  # Value list
    j = capacity  # Weight list, no minus 1, after changing initialization

    while i >= 0:

        val = F[i][j]

        if (valueList[i] + F[i - 1][j - weightList[i]]) == val:
            subset.append(i + 1)
            j = j - weightList[i]

        i = i - 1

    return subset

def makeString(aList):
    """
    Input: List
    Output: A string that is wrapped in curly brackets
    """
    aStr = '{'
    for i in range(len(aList) - 1):
        aStr += (str(aList[i]) + ', ')
    aStr += str(aList[len(aList) - 1])
    aStr += '}'

    return aStr

def main():

    #********************************************
    #static file names for testing
    # capacity = loadFile('p01_c.txt')
    # capacity = int(capacity[0])
    # value = loadFile('p01_v.txt')
    # weight = loadFile('p01_w.txt')
    #********************************************



    #********************************************
    # Dynamic file name
    cText = input("Enter file containing the capacity: ").strip()
    wText = input("Enter file containing the weights: ").strip()
    vText = input("Enter file containing the values: ").strip()
    capacity = loadFile(cText)
    capacity = int(capacity[0])
    value = loadFile(vText)
    weight = loadFile(wText)
    #********************************************

    #********************************************
    # Number of items in the list
    numOfItems = len(value)

    #********************************************
    # Initializing array, needs to be capacity + 1 because
    # postion 0 doesnt count
    vec = [[0]*(capacity + 1) for i in range(numOfItems)]
    #********************************************


    #********************************************
    # Performing dynamic knapsack calculation

    knapsackStartTime = time.time()
    knapSack(vec, capacity, value, weight)
    knapSackTime = (time.time() - knapsackStartTime) * 1000000
    #********************************************


    #********************************************
    # Performing greedy knapsack method

    greedyKnapStartTime = time.time()
    greedyKnap = knapSackGreedy(capacity, value, weight, False)
    greedyKnapTime =  (time.time() - greedyKnapStartTime) * 100000

    # Getting greedy optimal value
    greedyOptVal = 0
    for i in range(len(greedyKnap)):
        greedyOptVal += greedyKnap[i][2]

    # Getting greedy optimal subset
    greedyOptSubset = []
    for i in range(len(greedyKnap)):
        greedyOptSubset.append(greedyKnap[i][3] + 1)

    greedyOptSubset.sort()

    greedyOptSubStr = makeString(greedyOptSubset)
    #********************************************

    #********************************************
    # Printing information

    print ("\nKnapsack capacity =", (str(capacity) + '.'), "Total number of items =", (str(len(value)) + '.\n'))

    lenOfVecRow = len(vec) - 1
    lenOfVecCol = len(vec[lenOfVecRow]) - 1

    print ("Dynamic Programming Optimal value: ", str(vec[lenOfVecRow][lenOfVecCol]))

    sub = subset(vec, capacity, value, weight)
    sub.sort()

    subSetStr = makeString(sub)

    print ("Dynamic Programming Optimal subset:", subSetStr)
    print ("Dynamic Programming Time Taken:", knapSackTime, '(microseconds)')
    print ("\n")

    print ("Greedy Approach Optimal value:", str(greedyOptVal))
    print ("Greedy Approach Optimal subset:", greedyOptSubStr)
    print ("Greedy Approach Time Taken:", greedyKnapTime, '(microseconds)')

    #********************************************

    #********************************************
    # If you would like a graph to display uncomment graph(n, capacity)
    # n = # of elements you would like generated
    # capacity = capacity of knapsack

    # graph(100, 5)
    #********************************************

main()
