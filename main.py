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

    for i in range(len(F)): # row
        for j in range(len(F[i])): # column
            value = 0 # compiler was complaining
            if F[i][j] == 0:
                if j < weightList[i]:
                    value = F[i-1][j]
                else:
                    value = max(F[i-1][j], valueList[i] + F[i-1][j-weightList[i]])
            F[i][j] = value
            # print value

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


def main():
    capacity = loadFile('KnapsackTestData/p00_c.txt')
    capacity = int(capacity[0])
    value = loadFile('KnapsackTestData/p00_v.txt')
    weight = loadFile('KnapsackTestData/p00_w.txt')

    # Number of items in the list
    numOfItems = len(value)

    # Initializing array
    vec = [[0]*capacity for i in range(numOfItems)]
    optimalList = []
    # for i in range(numOfItems):
    #     vec[i][0] = 0

    knapSack(vec, capacity, optimalList, value, weight)
    for i in vec:
        print i

    greedyKnap = knapSackGreedy(capacity, value, weight, True)

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
    greedyOptSubStr = '{'
    for i in range(len(greedyOptSubset) - 1):
        greedyOptSubStr += (str(greedyOptSubset[i]) + ', ')
    greedyOptSubStr += str(greedyOptSubset[len(greedyOptSubset) - 1])
    greedyOptSubStr += '}'




    print "Greedy Approach Optimal value: " + str(greedyOptVal)
    print "Greedy Approach Optimal subset: " + greedyOptSubStr
    print "Greedy Approach Time Taken:"


main()
