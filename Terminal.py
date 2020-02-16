"""
Module responsibly for all graphics output to the terminal.
Will also be able to sort data and produce new views based on that. Will therefore also contain the "App loop" that
can accept some input. 
Is often called the "view" aswell in MVC Pattern.
"""

from tabulate import tabulate

allLabels = None
allLabelsHeaders = None


def getAllLabels(labels):
    """
    Arguments: labels: List - A list of lists, where the nested lists contain betting labels
    Description: Sends all labels to the Terminal Module
    """
    #Saying I want to asign something to a global variable inside this functions scope
    global allLabels
    allLabels = labels

def getAllLabelsHeaders(labelHeaders):
    """
    Arguments: labelHeaders: List - A list of lists, where the nested list contains betting label headers
    Description: Sends all label headers to the Terminal Module
    """
    global allLabelsHeaders
    allLabelsHeaders = labelHeaders


"""
Description: Prints out a table in terminal from a list of labels
"""
def display(listOfLabels, headers):
    print(tabulate(listOfLabels, headers=headers, tablefmt="grid"))


"""
In python a single underscore means that this is a private function/variable and
should not be accesses from outside of this module. But this is only an instruction,
it doesnt actually prevent it from being called elsewhere in the codebase.
"""
def _newTableOrder(index):
    """
    Arguments: 
        index: int - Which list index(column) to sort on.

    Description: sorts a list of bettingLabels and prints them out again.
    """
    headerIndex = 0
    for bettingLabels in allLabels:
        if (index < len(bettingLabels[0])):
            try:
                bettingLabels.sort(key = lambda nestedList: nestedList[index])
            except TypeError:
                pass
        
        display(bettingLabels, allLabelsHeaders[headerIndex])
        headerIndex += 1
        

def filterOut(threshold, bl, index):
    filteredBL = filter(lambda odds: float(odds) >= threshold, bl[0][index])
    display(filteredBL, allLabelsHeaders[0])



def appLoop():
    """
    Description: Terminal application loop - Mainly for sorting and then viewing data in a new view
    """
    stop = False
    while stop is not True:
        i = input("Insert index-number to be sorted on or q to quit: ")
        if i == "q":
            stop = True
            break
        if i == "f":
            ii = input("Insert which MO to filter on")
            iii = int(ii)
            filterOut(1.4, allLabels, iii)
            stop = True
            break
        index = int(i)
        _newTableOrder(index)