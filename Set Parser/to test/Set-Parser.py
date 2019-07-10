'''
This script parses degree requirements from excel files and outputs a json 
file containing all the relevant information.

Author: Visakh Madathil

Notes: Still need to build special_req functionality

Requires: More robust error checking
'''

#import statements
import json
import pandas as pd
import sys
from collections import OrderedDict

#read Excel file
course_data = pd.read_excel(sys.argv[1], header = None)
course_data = course_data.append(pd.Series(), ignore_index=True)
course_data = course_data.append(pd.Series(), ignore_index=True)
course_data = course_data.fillna(' ')
#print(course_data.tail())




'''
global variables
this will do for now, but I should write better code moving forward 
and minimize the number of these

courseDict (dict): a dictionary object to represent the information being
parsed
allSets (list)
position (int)
tot (int)
isEnd (boolean): indicated if end of the file has been reached 
'''
courseDict = OrderedDict()
courseDict["name"] = []
courseDict["type"] = []
courseDict["rules"] = []
courseDict["sets"] = []
courseDict["special_req"] = []
allSets = []
position = 0
tot = len(course_data.index)
isEnd = False
totCol = len(course_data.columns)
totRow = len(course_data.index)
rowPosition = 0
colPosition = 0
allCourses = []
courseNumber = 1

def writeCourses():
   #print(allCourses)
    
    with open('Cox-Classes/courses.json', 'w') as f:
        json.dump(allCourses , f)
    
'''
Function to append the sets and rules to the Course Dictionary

Args:
    sets (list): a list of all the sets their respective courses
    rules (list): a list of all the rules of the degree
'''
def createDict(sets, rules):
    global courseDict
    global allCourses
    global courseNumber
    #adding rules and sets to the Course Dictionary
    courseDict["rules"] = rules
    courseDict["sets"] = sets
    fileName = 'courses' + str(courseNumber) + '.json'
    #writing to json file
    with open (fileName, 'w') as f:
        json.dump(courseDict, f)
    
    #allCourses.append(courseDict.copy())
    #print(allCourses)
    courseDict.update((key, []) for key in courseDict)
    courseNumber = courseNumber + 1

'''
def createSpecReq(line):
    specList = []
    while(course_data[colPosition][rowPosition] != ' '):
        #append rule to the rulesList
        specList.append(line)
        #increment to next line
        incrementLine()
        line = course_data[colPosition][rowPosition]
    
    courseDict["special_req"] = specList
'''


'''
Function to create a list of rules for the degree

Args:
    line (str): the contents of the current cell being processed from 
    course_data
    rulesList (list): an empty list to store the rules in after being 
    par sed
'''
def createRules(line, rulesList):
    #calling global variables for position and total number of entries
    global rowPosition
    global colPosition
    #the loop should execute until all the lines are being read
    while(course_data[colPosition][rowPosition] != ' '):
        #append rule to the rulesList
        rulesList.append(line)
        #increment to next line
        incrementLine()
        line = course_data[colPosition][rowPosition]
    
    nextLine = course_data[colPosition][rowPosition + 1]
    nextKey = nextLine.split(' ', 1)[0]

'''
    if(nextKey == 'SPECIAL'):
        incrementLine()
        createSpecReq(nextLine)

    return rulesList
'''


'''
Function to create lists of courses

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createCourses(line):
    #initalize empty list 
    courseList = []
    print('creating courses')
    '''
    creating key from the first word of the line. This key will be used 
    to know when to stop storing the contents into the courseList
    '''
    key = line.split(' ', 1)[0]
    #loop should execute until the word "SET" is found in the line
    while (key != 'SET'):
        #add line to the courseList 
        courseList.append(line)
        #increent to next line
        incrementLine()
        #reassign variables 
        print(key)
        print(colPosition, rowPosition)
        line = course_data[colPosition][rowPosition]
        key = line.split(' ', 1)[0]
    return (courseList)


'''
Function to create set objects for the course dictionary

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createSets(line):
    global rowPosition
    global colPosition
    #parsing and assigning the name of the set
    setName = "SET " + line.split()[1]
    incrementLine()
    line = course_data[colPosition][rowPosition]
    #calling createCourses function to parse Courses for the set
    courseSet = createCourses(line)
    incrementLine()
    setDict = OrderedDict()
    setDict["name"] = setName 
    setDict["courses"] = courseSet
    return setDict


'''
Function to create name and type objects for each degree

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createName(line):
    print('creating name')
    #empty lists
    degree = []
    degreeType = []
    #appending to lists
    degree.append(line.split(',', 1)[0])
    degreeType.append(line.split(', ', 1)[1])
    #assigning to courseDict
    courseDict["name"] = degree
    courseDict["type"] = degreeType
    incrementLine()


'''
Function to ensure the correct action is taken for each line
    EX: if the line indicates a beginning of a set, this 
    function ensures the process for creating a set is taken

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def checkType(line):
    global allSets
    global rowPosition
    global colPosition
    global totCol
    global totRow
    global isEnd
    if(rowPosition == 0):
        createName(course_data[colPosition][rowPosition])
    else:
        #initalize empty set for rules
        rulesList = []
        #creating a key from the first word of the line
        #print(course_data[colPosition][rowPosition], course_data[colPosition][rowPosition + 1])
        if(course_data[colPosition][rowPosition] == ' ' and course_data[colPosition][rowPosition + 1] == ' '):
            #print("check where this was printed")
            if(colPosition == (totCol-1)):
                isEnd = True
            else:
                incrementCol()
                print('Next course being processed, this is course ', colPosition)
                rowPosition = 0
        else:
            key = line.split(' ', 1)[0]
            print(key)
            #print('you hitting?')
            #taking actions depending on what the key is
            if key == 'SET':
                print('creating sets')
                tempSet = createSets(line)
                print(tempSet)
                allSets.append(tempSet.copy())
                #tempSet.clear()
            if key == 'RULES':
                print('creating rules')
                incrementLine()
                line = course_data[colPosition][rowPosition]
                rulesList = createRules(line, rulesList)
                createDict(allSets.copy(), rulesList)
                allSets.clear()
            
            else:
                incrementLine()


def incrementCol():
    global colPosition
    colPosition = colPosition + 1

'''
Function to increment the line being parsed
'''
def incrementLine():
    global rowPosition
    rowPosition = rowPosition + 1




def createAll():
    #pass to checkType as long as processing is still happening
    #counter = 0
    global isEnd
    while(isEnd == False):
        #print('checking')
        if(totCol != colPosition and totRow != rowPosition):
            checkType(course_data[colPosition][rowPosition])
        else:
            isEnd = False
        #print(colPosition, rowPosition)
        #print(course_data[colPosition][rowPosition])
        #counter = counter + 1
        


def main():
    print("you have ", totCol, " courses to process")
    createAll()
    #writeCourses()


main()
