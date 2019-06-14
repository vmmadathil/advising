#Need to build special_req functionality

#import statements
import json
import pandas as pd
import sys

#read Excel file
course_data = pd.read_excel(sys.argv[1], header = None)

'''
global variables
this will do for now, but I should write better code moving forward 
and minimize the number of these

courseDict (dict): a dictionary object to represent the information being
parsed
allSets (list)
position (int)
tot (int)
'''
courseDict = {"name": [], "type": [], "rules": None, "sets": [], "special_req": " "}
allSets = []
position = 0
tot = len(course_data.index)


'''
Function to append the sets and rules to the Course Dictionary

Args:
    sets (list): a list of all the sets their respective courses
    rules (list): a list of all the rules of the degree
'''
def createDict(sets, rules):
    global courseDict
    #adding rules and sets to the Course Dictionary
    courseDict["rules"] = rules
    courseDict["sets"] = sets
    #writing to json file
    with open('courseDict.json', 'w') as fp:
        json.dump(courseDict, fp)


'''
Function to create a list of rules for the degree

Args:
    line (str): the contents of the current cell being processed from 
    course_data
    rulesList (list): an empty list to store the rules in after being 
    parsed
'''
def createRules(line, rulesList):
    #calling global variables for position and total number of entries
    global position
    global tot
    #the loop should execute until all the lines are being read
    while(position < tot):
        #append rule to the rulesList
        rulesList.append(line)
        #increment to next line
        incrementLine()
        #reassign line if still parsing
        if (position < tot):
            line = course_data[0][position]
    return rulesList


'''
Function to create lists of courses

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createCourses(line):
    #initalize empty list 
    courseList = []
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
        line = course_data[0][position]
        key = line.split(' ', 1)[0]
    return (courseList)


'''
Function to create set objects for the course dictionary

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createSets(line):
    global position
    #parsing and assigning the name of the set
    setName = "SET " + line.split()[1]
    incrementLine()
    line = course_data[0][position]
    #calling createCourses function to parse Courses for the set
    courseSet = createCourses(line)
    incrementLine()
    setDict = {"name" : setName, "courses": courseSet}
    return setDict


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
    global position
    global tot
    #initalize empty set for rules
    rulesList = []
    #creating a key from the first word of the line
    key = line.split(' ', 1)[0]
    #taking actions depending on what the key is
    if key == 'SET':
        tempSet = createSets(line)
        allSets.append(tempSet)
    if key == 'RULES':
        incrementLine()
        line = course_data[0][position]
        rulesList = createRules(line, rulesList)
    #create dictionary object when all lines are parsed
    if tot == position:
        createDict(allSets, rulesList)


'''
Function to increment the line being parsed
'''
def incrementLine():
    global position
    position = position + 1


'''
Function to create name and type objects for each degree

Args:
    line (str): the contents of the current cell being processed from 
    course_data
'''
def createName(line):
    global position
    global tot
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
    #pass to checkType as long as processing is still happening
    while(position < tot):
        checkType(course_data[0][position])


def main():
    createName(course_data[0][0])


main()