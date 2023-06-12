import json
import os
import zipfile
import pandas as pd

from logging import error

fileManger = 'Scripts/Source/fileManger.json'


def getheader(fileName):
    try:
        data = pd.read_excel(fileName).columns
    except:
        data = pd.read_csv(fileName).columns
    categories = list()
    for c in data:
        if c == 'dynamicTechType':
            categories.append('t' + c[8:])
        else:
            categories.append(c)
    return categories


def getRow(fileName, index):
    data = pd.read_excel(fileName, skiprows=index, nrows=1).columns
    row = list()
    for a in data:
        if 'Unnamed' in str(a):
            row.append('noData')
        elif len(str(a)) >= 2 and str(a)[-2] == '.':
            row.append(str(a)[:-2])
        else:
            row.append(a)
    return row


def getCol(fileName, colCategories):
    try:
        data = pd.read_excel(fileName, usecols=[colCategories])
    except:
        data = pd.read_csv(fileName, usecols=[colCategories])
    column = list()
    for i in data.index:
        column.append(data[colCategories][i])
    return column


def getColCsv(fileName, colCategories):
    data = pd.read_csv(fileName, usecols=[colCategories])
    column = list()
    for i in data.index:
        column.append(data[colCategories][i])
    return column


def readJson(filePath):
    with open(filePath, "r", encoding=checkEndCode(filePath)) as f:
        inputJson = json.load(f)
    return inputJson


def readJsonMultilingual(filePath):
    try:
        with open(filePath, "r", encoding='utf-8') as f:
            inputJson = json.load(f)
    except UnicodeDecodeError:
        with open(filePath, "r", encoding='utf-8-sig') as f:
            inputJson = json.load(f)
    return inputJson


def readJsonUtf8Sig(filePath):
    with open(filePath, "r", encoding='utf-8-sig') as f:
        inputJson = json.load(f)
    return inputJson


def readJsonZip(path, zipDir, fileName):
    try:
        zipPath = os.path.join(path, zipDir)
        with zipfile.ZipFile(zipPath) as z:
            for names in z.namelist():
                if fileName in names:
                    try:
                        with z.open(names) as j:
                            inputJson = j.read().decode(encoding='utf-8-sig')
                            return json.loads(inputJson)
                    except Exception as e:
                        error(e.__str__())
                        return
    except Exception as e:
        error(e.__str__())
        return


def writeJson(filePath, jsonObject):
    f = open(filePath, "a", encoding='utf-8')
    f.write(json.dumps(jsonObject, indent=4))
    f.close()


def writeJsonMultiLang(filePath, jsonObject):
    f = open(filePath, "a", encoding='utf-8')
    f.write(json.dumps(jsonObject, ensure_ascii=False, indent=4))
    f.close()


def updateJson(filePath, jsonObject):
    with open(filePath, "w", encoding=checkEndCode(filePath)) as f:
        json.dump(jsonObject, f, indent=4)


def updateJsonUtf8Sig(filePath, jsonObject):
    with open(filePath, "w", encoding='utf-8-sig') as f:
        json.dump(jsonObject, f, indent=4)


def updateJsonMultiLang(filePath, jsonObject):
    try:
        with open(filePath, "w", encoding='utf-8') as f:
            json.dump(jsonObject, f, ensure_ascii=False, indent=4)
    except UnicodeDecodeError:
        with open(filePath, "w", encoding='utf-8-sig') as f:
            json.dump(jsonObject, f, ensure_ascii=False, indent=4)


def updateJsonMultiLangUtf8Sig(filePath, jsonObject):
    with open(filePath, "w", encoding='utf-8-sig') as f:
        json.dump(jsonObject, f, ensure_ascii=False, indent=4)


def readCsv(filePath):
    df = pd.read_csv(filePath, keep_default_na=False, encoding=checkEndCode(filePath), dtype=object)
    return df


def writeCsv(filePath, df):
    df.to_csv(filePath, index=False, encoding=checkEndCode(filePath))


def printExcel(filePath):
    data = pd.read_excel(filePath)
    print(data)


def prettyPrintJson(jsonData):
    if isinstance(jsonData, str):
        jsonPrint = json.loads(jsonData)
        prettyPrintJson(jsonPrint)
    elif type(jsonData) == dict:
        jsonPrint = json.dumps(jsonData, ensure_ascii=False, indent=4)
        print(jsonPrint)
    else:
        error('Type Error: The Object\'s type needs to be dict() or str() and not {0}'.format(type(jsonData)))


def checkEndCode(filePath):
    with open(filePath) as rawData:
        return rawData.encoding


def jsonifyZip(text):
    tmpData = text.decode(encoding='utf-8-sig')
    tmpData = tmpData.replace('\n', '')
    tmpData = tmpData.replace('\t', '')
    return json.loads(tmpData)


def isNan(val):
    return pd.isna(val)
