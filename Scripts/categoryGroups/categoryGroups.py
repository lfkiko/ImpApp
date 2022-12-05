import codecs
import json
import os
import sys
from logging import info, error
from tkinter.messagebox import askyesno

from Scripts.addingUsers import categoriesAdaptation
from Scripts.toolBoox.excelJsonToolBox import getCol, readJson, readCsv, getRow, getColCsv
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, getFile, createPath


def categoriesMerge(fileExcel, CType):
    solution = createPath(getSolution(getPath('solution')), 'Enrichment\\SEntities\\CategoryAggregation.csv')
    cgs = getCol(fileExcel, 'CG')
    if CType == 'CType':
        if os.path.exists(solution):
            MergedCategory = getColCsv(solution, 'aggregatedCategoryGroup')
            for x in cgs:
                if x in MergedCategory:
                    cgs.remove(x)
    
    return cgs


def createLanguages(fileName):
    languages = list()
    lang1 = getCol(fileName, 'language 1')
    lang2 = getCol(fileName, 'language 2')
    lang3 = getCol(fileName, 'language 3')
    lang4 = getCol(fileName, 'language 4')
    for i in range(len(lang1)):
        languages.append([lang1[i], lang2[i], lang3[i], lang4[i]])
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
    elif CType == 'SSubCategories':
        data = {'subCategories': []}
    for i in range(len(categories)):
        new_cg = {'id': categories[i],
                  'description': {'langMap': {}}}
        for j in range(langs):
            new_cg['description']['langMap'][listOfLanguages[j]] = languages[i][j]
        if CType == "SCategoryGroups":
            new_cg['clientCategoryId'] = getFromSource(categories[i], 'clientCategoryId')
            if direction[i] in ["Both", "Income", "Expenses"]:
                new_cg['direction'] = direction[i]
            else:
                new_cg['direction'] = getFromSource(categories[i], 'direction')
            data['categoryGroups'].append(new_cg)
        elif CType == "SSubCategories":
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


def warnings(param):
    pass


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEntities')
        try:
            os.path.exists(solution)
        except:
            os.mkdir(solution)
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    
    jsonName = os.path.join(solution, argv[3] + ".json")
    categories = categoriesMerge(argv[0], argv[3])
    direction = getCol(argv[0], 'direction')
    languages = createLanguages(argv[0])
    langNum = argv[1]
    if type(langNum) == 'Choose number of languages':
        error('langNum is not an integer')
        warnings("SCategoryGroups.json wasn't overridden")
        return
    lanNames = argv[2]
    categoryGroups = createSCategoryGroups(categories, direction, languages, langNum, lanNames, argv[3])
    if categoryGroups == -1:
        error('Stop while running: SCategoryGroups.json stopped without completing the task')
        return
    writeCategoriesJson(jsonName, categoryGroups)
    if askyesno('Confirmation', 'Would you like to run categoriesAdaptation.py?') and argv[3] == 'SCategoryGroups':
        try:
            solution = getSolution(getPath('solution')) + '$QA'
        except Exception as e:
            error('Path Error:' + e.__str__()[e.index(']') + 1:])
            return
        categoriesAdaptation.main([solution])
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 excel file
    # 1 number of languages
    # 2 list of languages
    # 3 type
