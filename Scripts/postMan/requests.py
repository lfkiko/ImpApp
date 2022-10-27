import json
import os
import sys
import pandas
import requests
import threading
from logging import info, error
from subprocess import call
from Scripts.postMan.apiRequests import apis
from Scripts.toolBoox.excelJsonToolBox import prettyPrintJson
from Scripts.toolBoox.toolBoox import createPath, getSolution, getPath

csvName = 'allUsersInsights'
csvPath = 'Scripts/Source/postMan'

apiRequests = ['getInsights']


def getCsvPath():
    version = 0
    try:
        os.mkdir(csvPath)
    except Exception as e:
        error(e.__str__())
    newCsvName = csvName + 'Vol' + str(version)
    newCsvPath = os.path.join(csvPath.replace('/', '\\'), newCsvName + '.csv')
    while os.path.exists(newCsvPath):
        version += 1
        newCsvName = newCsvName[:-1] + str(version)
        newCsvPath = os.path.join(csvPath.replace('/', '\\'), newCsvName + '.csv')
    try:
        f = open(newCsvPath, "x")
    except Exception as e:
        error(e)
    return newCsvPath


def addToCsv(user, insights, path):
    insightList = list()
    for i in insights:
        insightList.append(i['useCaseId'])
    
    try:
        df = pandas.read_csv(path)
        df[user] = pandas.Series(insightList)
        df.to_csv(path, index=False)
    except pandas.errors.EmptyDataError:
        df = pandas.DataFrame({user: insightList})
        df.to_csv(path, index=False)


def requesting(api, url, headers, context, solution):
    def sendRequest(completeApi):
        response = requests.post(url, headers=headers, json=completeApi)
        return json.loads(response.text)
    
    tmpUser = headers['authToken'].lower()
    postman = apis()
    insightsApi = postman.request(api, context)
    if tmpUser == 'all':
        currentCsvPath = getCsvPath()
        for B in os.listdir(solution):
            headers['authToken'] = B
            apiResponse = sendRequest(insightsApi)
            if apiResponse['ok'] and int(apiResponse['numberOfInsights']) > 0:
                # print(apiResponse['numberOfInsights'])
                addToCsv(B, apiResponse['insights'], currentCsvPath)
        
        if os.name == "nt":
            os.startfile(insightsApi)
        else:
            call(("open", currentCsvPath))
    
    else:
        apiResponse = sendRequest(api)
        prettyPrintJson(apiResponse)
    print('its alive!!!')


def main(argv):
    info("updating DataAttribute")
    
    try:
        solution = createPath(getSolution(getPath('solution')) + '$QA', 'DemoData')
    
    except Exception as e:
        print(e)
        error('Path Error:' + getPath('solution') + ' is not a correct path Data library didn\'t run')
        return
    
    url = 'http://' + argv[0] + ':8080/pserver/execute?channel=' + argv[1].upper()
    headers = {'Content-Type': 'application/json', 'authToken': argv[4], 'effectiveTime': argv[2]}
    if argv[5] is not None:
        useContext = argv[5]
    else:
        useContext = "showAll"
    
    requesting(argv[3], url, headers, useContext, solution)
    info("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - IP
    # 1 - CHANNEL
    # 2 - DATE
    # 3 - API
    # 4- USER
    # 5 - CONTEXT
    # 6 - ID
