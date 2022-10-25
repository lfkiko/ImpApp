import json

import pandas as pd

fileManger = 'Scripts/Source/fileManger.json'


def getheader(fileName):
    data = pd.read_excel(fileName).columns
    categoris = list()
    for c in data:
        if c == 'dynamicTechType':
            categoris.append('t' + c[8:])
        else:
            categoris.append(c)
    return categoris


def getRow(fileName, index):
    data = pd.read_excel(fileName, skiprows=index, nrows=1).columns
    row = list()
    for a in data:
        if 'Unnamed' in str(a):
            row.append('noData')
        elif str(a)[-2] == '.':
            row.append(str(a)[:-2])
        else:
            row.append(a)
    return row


def getCol(fileName, colCategories):
    data = pd.read_excel(fileName, usecols=[colCategories])
    column = list()
    for i in data.index:
        column.append(data[colCategories][i])
    return column


def readJson(filePath):
    with open(filePath, "r") as f:
        inputJson = json.load(f)
        return inputJson


def readJsonUtf8Sig(filePath):
    with open(filePath, "r", encoding='utf-8-sig') as f:
        inputJson = json.loads(f.read())
        return inputJson


def writeJson(filePath, json_object):
    with open(filePath, "w") as f:
        f.write(json_object)


def updateJson(filePath, jsonObject):
    with open(filePath, "w", encoding=checkEndCode(filePath)) as f:
        json.dump(jsonObject, f, indent=4)


def readCsv(filePath):
    df = pd.read_csv(filePath, keep_default_na=False, encoding=checkEndCode(filePath), dtype=object)
    return df


def writeCsv(filePath, df):
    df.to_csv(filePath, index=False, encoding=checkEndCode(filePath))


def printExcel(filePath):
    data = pd.read_excel(filePath)
    print(data)


def checkEndCode(filePath):
    with open(filePath) as rawData:
        return rawData.encoding
