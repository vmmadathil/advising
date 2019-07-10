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

courseDict = OrderedDict()
courseDict["name"] = []
courseDict["type"] = []
courseDict["rules"] = None
courseDict["sets"] = []
courseDict["special_req"] = " "
allSets = []
isEnd = False
totCol = len(course_data.columns)
totRow = len(course_data.index)
rowPosition = 0
colPosition = 0
allCourses = []



def incrementLine():

def incrementCol():

def printDict():
def createDict():
def createRules():
def createCourses():
def createSets():
def createName():
def checkType():
def createAll():
    while(isEnd == False):
        checkType(course_data[colPosition][rowPosition])
def main():
    createAll()
