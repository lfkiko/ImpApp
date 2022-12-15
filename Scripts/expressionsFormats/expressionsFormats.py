import os
import sys
from logging import error

from Scripts.toolBoox.excelJsonToolBox import readJsonZip, prettyPrintJson, getCol, getheader, isNan
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution


def createLanguages(fileName, lanNames):
    languages = list()
    tmpLanguages = dict()
    for i in range(len(lanNames)):
        print(getCol(fileName, lanNames[i]))
        tmpLanguages["lang" + str(i + 1)] = getCol(fileName, lanNames[i])
    for j in range(len(tmpLanguages["lang1"])):
        tmpList = []
        for lang in tmpLanguages.keys():
            tmpList.append(tmpLanguages[lang][j])
        languages.append(tmpList)
    return languages


def createSExpressionsFormats(jsonData: dict, expressions, languages, langNum, lanNames):
    newJsonData = jsonData
    afterDecimal = list()
    amountFormats = list()
    for j in range(langNum):
        try:
            after = int(languages[expressions.index('No. of Digits after decimal')][j])
        except Exception as e:
            error(e.__str__())
            return -1
        num = languages[expressions.index('Decimal Symbol')][j]
        for x in range(after):
            num += '0'
        afterDecimal.append(num)
        
        groupSign = languages[expressions.index('Digit grouping')][j][1:][3]
        amountFormat = '###' + groupSign + '###' + groupSign + '###'
        currencySign = languages[expressions.index('Currency Symbol Location')][j]
        currencyLocation = '@'
        if currencySign[0] == '$':
            for space in currencySign[1:]:
                if not space.isnumeric():
                    currencyLocation += space
                else:
                    break
            amountFormat = currencyLocation + amountFormat
        elif currencySign[-1] == '$':
            for space in currencySign[-2::-1]:
                if not space.isnumeric():
                    currencyLocation = space + currencyLocation
                else:
                    break
            amountFormat = amountFormat + currencyLocation
        amountFormats.append(amountFormat)
    
    for key in range(len(jsonData['formats'])):
        tmp = {}
        if newJsonData['formats'][key]['name'] in expressions:
            if newJsonData['formats'][key]['type'] == 'Date':
                for i in range(langNum):
                    tmp[lanNames[i]] = languages[expressions.index(newJsonData['formats'][key]['name'])][i]
        if newJsonData['formats'][key]['type'] == 'Amount':
            for i in range(langNum):
                if newJsonData['formats'][key]['id'] == 'Balance':
                    tmp[lanNames[i]] = amountFormats[i][:amountFormats[i].rindex('#') + 1] + afterDecimal[i] + \
                                       amountFormats[i][amountFormats[i].rindex('#') + 1:]
                elif 'Abs' in newJsonData['formats'][key]['id']:
                    tmp[lanNames[i]] = '+' + amountFormats[i]
                else:
                    tmp[lanNames[i]] = amountFormats[i]
        if len(tmp) > 0:
            check = True
            for x in tmp.keys():
                if isNan(tmp[x]):
                    check = False
            if check:
                newJsonData['formats'][key]['formats'] = tmp
    
    return newJsonData


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'Insights', 'SEntities')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    jsonData = readJsonZip(getPath('DataLoad'), 'product-engage-biz-unit.zip', 'SExpressionsFormats.json')
    expressions = getCol(argv[0], 'format')
    lanNames = getheader(argv[0])[1:]
    langNum = len(lanNames)
    
    languages = createLanguages(argv[0], lanNames)
    sExpressionsFormats = createSExpressionsFormats(jsonData, expressions, languages, langNum, lanNames)
    if sExpressionsFormats == -1:
        error('Stop while running: SCategoryGroups.json stopped without completing the task')
        return
    # for x in range(len(sExpressionsFormats['formats'])):
    #     if len(sExpressionsFormats['formats'][x]['formats']) == 0:
    #         sExpressionsFormats['formats'][x].update({'formats': jsonData['formats'][x]['formats']})
    prettyPrintJson(sExpressionsFormats)
    endLog()
    
    if __name__ == "__main__":
        main(sys.argv[1:])
        
        # 0 - excel file
