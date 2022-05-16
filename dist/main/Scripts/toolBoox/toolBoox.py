import json
import os
import webbrowser

import pandas as pd
from kivy.factory import Factory
from kivy.properties import ObjectProperty

solutionPath = ObjectProperty(None)
fileManger = 'Scripts/Source/fileManger.json'


def getCol(fileName, colCategories):
    data = pd.read_excel(fileName, usecols=[colCategories])
    column = list()
    for i in data.index:
        column.append(data[colCategories][i])
    return column


def readJson(input_file):
    with open(input_file, "r") as f:
        input_json = json.load(f)
    return input_json


def writeJson(file_name, json_object):
    with open(file_name, "w") as f:
        f.write(json_object)


def updateJson(file_name, json_object):
    with open(file_name, "w") as f:
        json.dump(json_object, f, indent=4)


def createDirectory(solution_path, path):
    directories = path.split(os.sep)
    for p in directories:
        try:
            os.mkdir(solution_path + os.sep + p)
        except:
            pass
        solution_path = solution_path + os.sep + p


def fixPath(path):
    return path.replace('\\', '/')


def valPath(path):
    if 'perso-core' in path:
        return True
    elif 'bank-biz' in path:
        Factory.ERROR1().open()
        return False
    elif path == readJson(getFile('settings'))['pathRoot']:
        Factory.ERROR2().open()
        return False
    else:
        return True


def readCsv(file_name):
    df = pd.read_csv(file_name)
    return df


def printExcel(file_name):
    data = pd.read_excel(file_name)
    print(data)


def rewriteText(file_name, new_text, path_filter):
    data = readJson(file_name)
    if path_filter == 'm':
        data["pathRoot"] = new_text
    elif path_filter == 'j':
        data["pathRoot"] = new_text
    print(data)
    updateJson(file_name, data)


def currentPath(self, filterX, path):
    if filterX == 'c':
        self.ids.corePath.text = path
    elif filterX == 's':
        self.ids.solutionPath.text = path


def verifyPath(self, filterX, path):
    if filterX == 'c':
        self.ids.corePath.text = path
    elif filterX == 's':
        if valPath(path):
            self.ids.solutionPath.text = path


def openKB(self):
    webbrowser.open('https://track.personetics.com/youtrack/articles/S-A-306/Solution-Imp--')


def getFile(file_name):
    file = readJson(fileManger)
    return file[file_name]


def FindDir(path, direction):
    path_back = str()
    dirs = direction.split('/')
    for i in dirs:
        path_back = os.path.join(path, i)
        if os.path.exists(path_back):
            pass
        else:
            os.mkdir(path_back)
    return path_back
