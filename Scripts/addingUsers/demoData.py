import os
import shutil
import sys
from logging import info, warning, error

from Scripts.addingUsers import categoriesAdaptation
from Scripts.toolBoox.excelJsonToolBox import getCol, readCsv, writeCsv
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import createPath, getSolution, getPath


def find_relevant_users(core_path, extraUsers, bUsers, modified):
    relevantUser = []
    coreDemoDataPath = createPath(core_path, 'product-demo-data-biz-unit\\Core\\DemoData')
    if bUsers:
        for d in os.listdir(coreDemoDataPath):
            if d.startswith("B_") and d[2].isnumeric():
                relevantUser.append(d)
    if modified:
        for x in extraUsers:
            relevantUser.append(x)
    return relevantUser


def copyUsers(relevantUser, corePath, solutionQaPath):
    errors = False
    solutionDemoData = createPath(solutionQaPath, 'DemoData')
    coreDemoDataPath = createPath(corePath, "product-demo-data-biz-unit\\Core\\DemoData")
    try:
        os.mkdir(solutionDemoData)
    except:
        warning('all ready exist: ' + solutionDemoData)
        errors = True
    
    for user in relevantUser:
        srcPath = os.path.join(coreDemoDataPath, user)
        trgPath = os.path.join(solutionDemoData, user)
        try:
            os.mkdir(trgPath)
        except:
            warning("User: " + user + " is all ready exists in the solution level from ")
        finally:
            if os.path.exists(srcPath):
                files = os.listdir(srcPath)
                for file in files:
                    try:
                        shutil.copy2(os.path.join(srcPath, file), trgPath)
                    except:
                        errors = True
                        error("Something went wrong while copping: " + file + ' to ' + user)
            else:
                errors = True
                error("User: " + user + " do not exists in the core ")
                pass
    
    if errors:
        info("Copying users finished with warnings")
    else:
        info("Copying users finished")
    return errors


def modifyUser(usersPath, user, localCurrency, foreignCurrency, countryName, countryCode, factor):
    def updateCurrency(currentCurrency):
        if currentCurrency == "USD":
            return localCurrency
        elif currentCurrency == "EUR":
            return foreignCurrency
        else:
            return currentCurrency
    
    def updateCountryCode(currentCountry):
        if currentCountry != countryCode:
            return countryCode
        else:
            return currentCountry
    
    def updateCountryName(currentCountry):
        if currentCountry != countryName:
            return countryName
        else:
            return currentCountry
    
    def updateFactor(currentValue):
        if factor != 1 and currentValue != '':
            try:
                newVal = float(currentValue.replace(",", ""))
                newVal = newVal * float(factor)
                return str(round(newVal, 2))
            except:
                print(currentValue)
                error('Can\'t convert to float in :' + usersPath)
        
        return currentValue
    
    def updateColumn(column, file, func):
        try:
            df = readCsv(os.path.join(usersPath, file))
        except:
            warning('col ' + column + ' don\'t exists in - ' + os.path.join(usersPath, file))
            return
        
        df[column] = df[column].apply(func)
        writeCsv(os.path.join(usersPath, file), df)
    
    for thisFile in os.listdir(usersPath):
        try:
            csvFile = readCsv(os.path.join(usersPath, thisFile))
        except:
            error('Problem opening ' + thisFile + ' for ' + user)
            continue
        
        for col in ['currencyCd', 'currencyCdOriginal', 'countryCd', 'countryName', 'availableBalance',
                    'availableCredit', 'availableCreditCash', 'amount', 'amountChargeCurrency',
                    'amountLocalCurrency', 'amountOriginal', 'amountOriginalCurrency', 'currencyAmount']:
            if col in csvFile:
                if 'currency' in col and 'currencyAmount' != col:
                    updateColumn(col, thisFile, updateCurrency)
                else:
                    if 'Cd' in col:
                        updateColumn(col, thisFile, updateCountryCode)
                    elif 'Name' in col:
                        updateColumn(col, thisFile, updateCountryName)
                    elif factor != 1:
                        updateColumn(col, thisFile, updateFactor)


def modifyUsersInSolution(solutionDemoDataPath, input_json, relevantUser):
    for user in relevantUser:
        modifyUser(os.path.join(solutionDemoDataPath, user), user, input_json['LocalCurrency'],
                   input_json['ForeignCurrency'], input_json['CountryName'], input_json['CountryCode'],
                   input_json['Factor'])


def main(argv):
    startLog()
    core = os.path.join(getPath('corePath'), 'product-bizpack')
    try:
        solution = getSolution(getPath('solution')) + '$QA'
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    
    extraUsers = getCol(argv[3], 'USERS')
    relevantUser = find_relevant_users(core, extraUsers, argv[1], argv[2])
    err: bool = copyUsers(relevantUser, core, solution)
    modifyUsersInSolution(os.path.join(solution, 'DemoData'), argv[0], os.listdir(os.path.join(solution, 'DemoData')))
    categoriesAdaptation.main([solution])
    endLog(err)


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 properties dictionary
# 1 B_users checkBox bool
# 2 modified checkBox bool
# 3 file name

# os.listdir(product + "\\DemoData")
