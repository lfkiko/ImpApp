import codecs
import json
import os
import sys
from logging import error
from tkinter.messagebox import askyesno

from Scripts.addingUsers import categoriesAdaptation
from Scripts.toolBoox.excelJsonToolBox import getCol, readJson, getheader
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, getFile


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


def getFromSource(categoryId, value):
    SCategoryGroupsSource = readJson(getFile('categoryGroups_source'))
    for categories in SCategoryGroupsSource['categoryGroups']:
        if categories['id'] == categoryId:
            return categories[value]
    pass


def createSCategoryGroups(categories, direction, languages, numOfLang, listOfLanguages, CType):
    try:
        langs = int(numOfLang)
    except Exception as e:
        error(e.__str__())
        return -1
    data = {}
    if CType == 'SCategoryGroups':
        data = {'categoryGroups': []}
        sub = False
    elif CType == 'SSubCategories':
        data = {'subCategories': []}
        sub = True
    for i in range(len(categories)):
        new_cg = {'id': categories[i],
                  'description': {'langMap': {}}}
        for j in range(langs):
            new_cg['description']['langMap'][listOfLanguages[j]] = languages[i][j]
        if not sub:
            new_cg['clientCategoryId'] = getFromSource(categories[i], 'clientCategoryId')
            if direction[i] in ["Both", "Income", "Expenses"]:
                new_cg['direction'] = direction[i]
            else:
                new_cg['direction'] = getFromSource(categories[i], 'direction')
            data['categoryGroups'].append(new_cg)
        elif sub:
            data['subCategories'].append(new_cg)
    return data


# Due to multi-lingual content we can't use toolbox.writeJson.
# this is why we have this method
def writeCategoriesJson(fileName, json_object):
    if os.path.exists(fileName):
        try:
            os.remove(fileName)
        except Exception as e:
            error(e)
    with codecs.open(fileName, 'a+', 'utf-8') as f:
        f.write(json.dumps(json_object, ensure_ascii=False, indent=4))


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEntities')
        try:
            os.path.exists(solution)
        except:
            os.mkdir(solution)
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    jsonName = os.path.join(solution, argv[1] + ".json")
    categories = getCol(argv[0], 'CG')
    direction = getCol(argv[0], 'direction')
    lanNames = getheader(argv[0])[1:-1]
    langNum = len(lanNames)
    languages = createLanguages(argv[0], lanNames)
    categoryGroups = createSCategoryGroups(categories, direction, languages, langNum, lanNames, argv[1])
    if categoryGroups == -1:
        error('Stop while running: SCategoryGroups.json stopped without completing the task')
        return
    writeCategoriesJson(jsonName, categoryGroups)
    if askyesno('Confirmation', 'Would you like to run categoriesAdaptation.py?') and argv[1] == 'SCategoryGroups':
        try:
            solution = getSolution(getPath('solution')) + '$QA'
        except Exception as e:
            error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
            return
        categoriesAdaptation.main([solution])
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 excel file
    # 1 type
