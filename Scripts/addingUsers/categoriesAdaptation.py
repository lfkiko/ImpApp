import os
import sys
import warnings
from logging import error

from Scripts.toolBoox.excelJsonToolBox import readCsv, writeCsv, readJson
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath


def updateUsers(product, users, categories):
    defaultCg = 'CG0'
    
    def updateCategoryGroupId(currentCategory):
        if currentCategory in categories:
            return currentCategory
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
        
        finally:
            try:
                updateColumn(dtPath, updateCategoryGroupId)
            except Exception as e:
                error(e.__str__())


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
    startLog()
    try:
        solution = os.path.join(argv[0], 'Demodata')
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
    
    endLog(not (len(categories) == 0))


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 demo data path
