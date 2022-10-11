import os
import shutil
import sys
from logging import info, warning, error

from Scripts.toolBoox.toolBoox import readCsv, writeCsv, getCol, createPath, getSolution, getPath


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


def copy_users(relevant_user, core_path, solution_qa_path):
    errors = False
    solution_demodata = createPath(solution_qa_path, 'DemoData')
    coreDemoDataPath = createPath(core_path, "product-demo-data-biz-unit\\Core\\DemoData")
    try:
        os.mkdir(solution_demodata)
    except:
        info('all ready exist: ' + solution_demodata)
    
    for user in relevant_user:
        srcPath = os.path.join(coreDemoDataPath, user)
        trgPath = os.path.join(solution_demodata, user)
        try:
            os.mkdir(trgPath)
            files = os.listdir(srcPath)
            for file in files:
                try:
                    shutil.copy2(os.path.join(srcPath, file), trgPath)
                except:
                    error("Something went wrong while copping: " + file + ' to ' + user)
        except:
            warning("User: " + user + " is all ready exists in the solution level from ")
    
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
                    'amountLocalCurrency', 'amountOriginal', 'amountOriginalCurrency']:
            if col in csvFile:
                if 'currency' in col:
                    updateColumn(col, thisFile, updateCurrency)
                else:
                    if 'Cd' in col:
                        updateColumn(col, thisFile, updateCountryCode)
                    elif 'Name' in col:
                        updateColumn(col, thisFile, updateCountryName)
                    elif factor != 1:
                        updateColumn(col, thisFile, updateFactor)


def modifyUsersInSolution(solutionDemoDataPath, input_json):
    for user in os.listdir(solutionDemoDataPath):
        modifyUser(os.path.join(solutionDemoDataPath, user), user, input_json['LocalCurrency'],
                   input_json['ForeignCurrency'], input_json['CountryName'], input_json['CountryCode'],
                   input_json['Factor'])
        # info(user + ' was updated')


def main(argv):
    info("Starting Demo data override")
    core = os.path.join(getPath('corePath'), 'product-bizpack')
    try:
        product = getSolution(getPath('solution')) + '$QA'
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    
    extraUsers = getCol(argv[3], 'USERS')
    relevant_user = find_relevant_users(core, extraUsers, argv[1], argv[2])
    copy_users(relevant_user, core, product)
    modifyUsersInSolution(os.path.join(product, 'DemoData'), argv[0],relevant_user)
    info("Demo data finished overwriting the users")


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 properties dictionary
# 1 B_users checkBox bool
# 2 modified checkBox bool
# 3 file name

# os.listdir(product + "\\DemoData")
