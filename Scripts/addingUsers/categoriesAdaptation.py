import os
import sys
import warnings
from logging import info, error

from Scripts.toolBoox.excelJsonToolBox import readCsv, writeCsv, readJson
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath


def updateUsers(product, users, categories):
    defaultCg = 'CG0'
    
    def updateCategoryGroupId(currentCatrgory):
        if currentCatrgory in categories:
            return currentCatrgory
        else:
            return defaultCg
    
    def updateColumn(dTransactionsPath, func):
        col = readCsv(dTransactionsPath)
        col['categoryGroupId'] = col['categoryGroupId'].apply(func)
        writeCsv(dTransactionsPath, col)
    
    for user in users:
        try:
            dtPath = os.path.join(product, user, 'DTransaction.csv')
            os.path.exists(dtPath)
        except:
            warnings(user + ' DTransaction.csv do not exists')
            continue
        
        updateColumn(dtPath, updateCategoryGroupId)


def getCategories(cgPath):
    categories = []
    try:
        cgJsonPath = createPath(cgPath, '\\SEntities\\SCategoryGroups.json')
    except:
        error('somthing went wrong with the SCategoryGroups.json path: ' + cgPath)
        return categories
    
    try:
        cdJson = readJson(cgJsonPath)
    except:
        error('couldn\'t read: ' + cgJsonPath)
        return categories
    for cg in cdJson['categoryGroups']:
        categories.append(cg['id'])
    return categories


def main(argv):
    info('starting categoriesAdaptation')
    try:
        solution = os.pathsep.join(argv[0], 'Demodata')
    except:
        error('Demodata don\'t exsists')
        return
    users = os.listdir(solution)
    categories = getCategories(getSolution(getPath('solution')))
    if len(categories) == 0:
        error('problem with getCategories')
        return
    else:
        updateUsers(solution, users, categories)
        info("categoriesAdaptation finished updating users users")


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 demo data path
