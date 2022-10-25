import os
import shutil
import sys
from logging import info, warning, error

from Scripts.toolBoox.excelJsonToolBox import getCol, readCsv, writeCsv
from Scripts.toolBoox.toolBoox import createPath, getSolution, getPath


def find_relevant_users(core_path, extraUsers, Busers, modified):
    relevant_user = []
    core_demo_data_path = createPath(core_path, 'product-demo-data-biz-unit\\Core\\DemoData')
    if Busers:
        for d in os.listdir(core_demo_data_path):
            if d.startswith("B_1") or d.startswith("B_2"):
                relevant_user.append(d)
    if modified:
        for x in extraUsers:
            relevant_user.append(x)
    info('Relevant users list:')
    info(relevant_user)
    return relevant_user


def copyUsers(relevantUser, corePath, solutionQaPath):
    errors = False
    solutionDemoData = createPath(solutionQaPath, 'DemoData')
    coreDemoDataPath = createPath(corePath, "product-demo-data-biz-unit\\Core\\DemoData")
    try:
        os.mkdir(solutionDemoData)
    except:
        info('all ready exist: ' + solutionDemoData)
        errors = not errors
    
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
                        error("Something went wrong while copping: " + file + ' to ' + user)
            else:
                error("User: " + user + " do not exists in the core ")
                pass
    if errors:
        info("Copying users finished with warnings")
    else:
        info("Copying users finished")


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
                newVal = float(currentValue)
                newVal = newVal * factor
                return round(newVal, 2)
            except:
                error('Can\'t convert to float in :' + usersPath)
        
        return currentValue
    
    def updateColumn(column, file, func):
        try:
            df = readCsv(os.path.join(usersPath, file))
        except:
            info('col ' + column + ' don\'t exists in - ' + os.path.join(usersPath, file))
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
        # info(user + ' was updated')


def main(argv):
    info("Starting Demo data override")
    core = os.path.join(getPath('corePath'), 'product-bizpack')
    try:
        solution = getSolution(getPath('solution')) + '$QA'
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    
    extraUsers = getCol(argv[3], 'USERS')
    relevantUser = find_relevant_users(core, extraUsers, argv[1], argv[2])
    copyUsers(relevantUser, core, solution)
    modifyUsersInSolution(os.path.join(solution, 'DemoData'), argv[0], relevantUser)
    info("Demo data finished overwriting the users")


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 properties dictionary
# 1 B_users checkBox bool
# 2 modified checkBox bool
# 3 file name

# os.listdir(product + "\\DemoData")
