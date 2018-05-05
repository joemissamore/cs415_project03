import time
# class Item:
#     def __init__(self):
#         self.weight

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

def knapSack(F, capacity, optimalList, valueList, weightList):
    """
    This must start at i = 1 & j = 1.
    Input:
        F = initalized list of values
        capacity = capacity of knapsack
        valueList = list of values
        weightList = list of weights

    This is a void function and just edits F.
    """
    timetime = []
    for i in range(len(F)): # row
        start = time.time()

        for j in range(len(F[i])): # column (# of items)
            value = 0 # compiler was complaining
            # if F[i][j] == 0:
            print 'i:', i
            print 'j:', j
            print 'weightList[i]:', weightList[i]
            if j < weightList[i]:
                print 'inside (j < weightList[i])'
                value = F[i-1][j]

            else:
                print 'inside (else)'
                firstChoice = F[i-1][j]
                secondChoice = valueList[i] + F[i-1][j-weightList[i]]
                print 'firstChoice:', firstChoice
                print 'secondChoice:', secondChoice
                value = max(firstChoice, secondChoice)

            print 'value:', value, '\n'
            F[i][j] = value
            # print value
        timetime.append(time.time()-start)
        # print (time.time() - start) * 1000000
    for i in range(len(timetime)):
        print 'Number of elements: ' + str(i) + ': ' + str(timetime[i] * 1000000)

    # return F[i][j]

    # return F

def knapSackGreedy(capacity, valueList, weightList, debug=False):
    ratio = []
    for i in range(len(valueList)):
        ratio.append([float(valueList[i] / weightList[i]), weightList[i], valueList[i], int(i)])

    ratio.sort(reverse=True) # Sort from highest to lowest value

    if debug:
        print '\nPrinting ratio...'
        for i in ratio:
            print i

    sack = []
    for i in ratio:
        if i[1] <= capacity:
            sack.append(i)
            capacity -= i[1]

        if capacity == 0:
            break

    if debug:
        print "\nPrinting sack..."
        for i in sack:
            print i

    return sack


def subset(F,capacity,valueList, weightList):
    subset = []
    i = len(F) - 1  # Value list
    j = capacity  # Weight list, no minus 1, after changing initialization

    while i >= 0:

        val = F[i][j]

        if (valueList[i] + F[i - 1][j - weightList[i]]) == val:
            subset.append(i + 1)
            j = j - weightList[i]

        i = i - 1

        # done

    return subset

def makeString(aList):
    aStr = '{'
    for i in range(len(aList) - 1):
        aStr += (str(aList[i]) + ', ')
    aStr += str(aList[len(aList) - 1])
    aStr += '}'

    return aStr

def main():
    capacity = loadFile('KnapsackTestData/p01_c.txt')
    capacity = int(capacity[0])
    value = loadFile('KnapsackTestData/p01_v.txt')
    weight = loadFile('KnapsackTestData/p01_w.txt')

    # Number of items in the list
    numOfItems = len(value)

    # Initializing array, needs to be capacity + 1 because
    # postion 0 doesnt count
    vec = [[0]*(capacity + 1) for i in range(numOfItems)]
    optimalList = []
    # for i in range(numOfItems):
    #     vec[i][0] = 0

    knapsackStartTime = time.time()
    knapSack(vec, capacity, optimalList, value, weight)
    knapSackTime = (time.time() - knapsackStartTime) * 1000000
    # for i in vec:
    #     print i

    greedyKnapStartTime = time.time()
    greedyKnap = knapSackGreedy(capacity, value, weight, False)
    greedyKnapTime =  (time.time() - greedyKnapStartTime) * 1000000

    # Getting greety optimal value
    greedyOptVal = 0
    for i in range(len(greedyKnap)):
        greedyOptVal += greedyKnap[i][2]

    # Getting greety optimal subset
    greedyOptSubset = []
    for i in range(len(greedyKnap)):
        greedyOptSubset.append(greedyKnap[i][3])

    greedyOptSubset.sort()

    # Turn into appropriate string
    # greedyOptSubStr = '{'
    # for i in range(len(greedyOptSubset) - 1):
    #     greedyOptSubStr += (str(greedyOptSubset[i]) + ', ')
    # greedyOptSubStr += str(greedyOptSubset[len(greedyOptSubset) - 1])
    # greedyOptSubStr += '}'

    greedyOptSubStr = makeString(greedyOptSubset)

    print "\nKnapsack capacity =", (str(capacity) + '.'), "Total number of items =", (str(len(value)) + '.\n')

    lenOfVecRow = len(vec) - 1
    lenOfVecCol = len(vec[lenOfVecRow]) - 1

    print "Dynamic Programming Optimal value: ", str(vec[lenOfVecRow][lenOfVecCol])

    sub = subset(vec, capacity, value, weight)
    sub.sort()

    subSetStr = makeString(sub)

    print "Dynamic Programming Optimal subset:", subSetStr
    print "Dynamic Programming Time Taken:", knapSackTime, '(microseconds)'
    print

    print "Greedy Approach Optimal value:", str(greedyOptVal)
    print "Greedy Approach Optimal subset:", greedyOptSubStr
    print "Greedy Approach Time Taken:", greedyKnapTime, '(microseconds)'


main()
