import json
import os
import webbrowser
import pandas as pd
from bs4 import BeautifulSoup

fileManger = 'Scripts/Source/fileManger.json'


def getCol(fileName, colCategories):
    data = pd.read_excel(fileName, usecols=[colCategories])
    column = list()
    for i in data.index:
        column.append(data[colCategories][i])
    return column


def readJson(input_file):
    with open(input_file, "r", encoding=checkEndCode(input_file)) as f:
        input_json = json.load(f)
    return input_json


def writeJson(filePath, json_object):
    with open(filePath, "w") as f:
        f.write(json_object)


def updateJson(filePath, json_object):
    with open(filePath, "w") as f:
        json.dump(json_object, f, indent=4)


def createDirectory(solutionsPath, path):
    directories = path.split(os.sep)
    for p in directories:
        try:
            os.mkdir(solutionsPath + os.sep + p)
        except:
            pass
        solutionsPath = solutionsPath + os.sep + p


def fixPath(path):
    return path.replace('\\', '/')


def valPath(path):
    if 'perso-core' in path:
        return True
    elif 'bank-biz' in path:
        # Factory.ERROR1().open()
        return False
    elif path == readJson(getFile('settings'))['pathRoot']:
        # Factory.ERROR2().open()
        return False
    else:
        return True


def checkEndCode(filePath):
    with open(filePath) as raw_data:
        return raw_data.encoding


def readCsv(filePath):
    df = pd.read_csv(filePath, keep_default_na=False, encoding=checkEndCode(filePath), dtype=object)
    return df


def writeCsv(filePath, df):
    df.to_csv(filePath, index=False, encoding=checkEndCode(filePath))


def printExcel(filePath):
    data = pd.read_excel(filePath)
    print(data)


def rewriteText(filePath, new_text, path_filter):
    data = readJson(filePath)
    data[path_filter] = new_text
    print(data)
    updateJson(filePath, data)


def currentPath(self, filterX, path):
    if filterX == 'c':
        self.ids.corePath.text = path
    elif filterX == 's':
        self.ids.solutionPath.text = path


def verifyPath(self, filterX, path):
    fixedPath = os.path.normpath(path)
    if filterX == 'c':
        self.ids.corePath.text = fixedPath
    elif filterX == 's':
        if valPath(fixedPath):
            self.ids.solutionPath.text = fixedPath


def openKB(self):
    webbrowser.open('https://track.personetics.com/youtrack/articles/S-A-306/Solution-Imp--')


def getFile(filePath):
    file = readJson(fileManger)
    return file[filePath]


def findDir(path, direction):
    path_back = str()
    dirs = direction.split('/')
    for i in dirs:
        path_back = os.path.join(path, i)
        if os.path.exists(path_back):
            pass
        else:
            os.mkdir(path_back)
    return path_back


def createPath(path, extra):
    newPath = path
    addOns = extra.rsplit('\\')
    for x in addOns:
        newPath = os.path.join(newPath, x)
    return newPath


def getSolution(path):
    solutionsPath = path
    dirs = ['biz-units', 'perso-biz', 'Projects']
    for d in dirs:
        if d in os.listdir(solutionsPath):
            solutionsPath = os.path.join(solutionsPath, d)
    for x in os.listdir(solutionsPath):
        checkPath = os.path.join(solutionsPath, x)
        if os.path.isdir(checkPath) and '$' not in x:
            return os.path.join(solutionsPath, x)
    return path


def getPath(pathName):
    if pathName == 'corePath':
        return readJson(getFile('settings'))['intelliJRoot']
    elif pathName == 'modelPath':
        return readJson(getFile('settings'))['modelPath']


def modelVersion(projectPath):
    if 'pom.xml' in os.listdir(projectPath):
        with open(os.path.join(projectPath, 'pom.xml'), 'r') as f:
            pom = f.read()
            data = str(BeautifulSoup(pom, 'xml').find('version'))
            version = data[(data.find('>')) + 1: data.find('<', 1)].split('.')
            if version[0] > 5 and version[1] > 5:
                return True
            
            return False


def getInsightsDir(path):
    projectName = path.split('\\')[-1].upper()
    currPath = os.path.join(path, 'biz-units\\perso-biz\\Projects')
    if os.path.exists(currPath):
        for x in os.listdir(currPath):
            if x == projectName:
                currPath = os.path.join(currPath, projectName + '\\Insights')
                try:
                    os.path.exists(currPath)
                    return currPath
                except FileNotFoundError:
                    print("Directory: {0} does not exist".format(currPath))
