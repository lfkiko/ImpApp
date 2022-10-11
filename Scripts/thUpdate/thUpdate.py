import json
import os
import sys


def checkEndCode(file_name):
    with open(file_name) as raw_data:
        return raw_data.encoding


def readJson(input_file):
    with open(input_file, "r") as f:
        input_json = json.load(f)
    return input_json


def updateJson(file_name, json_object):
    with open(file_name, "w") as f:
        json.dump(json_object, f, indent=4)


def getList(path):
    allInsights = os.listdir(path)
    filteredInsights = []
    for x in allInsights:
        currentPath = os.path.join(path, x)
        if x == 'ProgramTracker':
            continue
        if 'SQuiz.json' in os.listdir(currentPath):
            filteredInsights.append(x)
            continue
        elif 'SThresholds.json' in os.listdir(currentPath):
            try:
                jData = readJson(os.path.join(currentPath, 'SThresholds.json'))
            except:
                print(x + ' SThresholds.json is not readable')
                continue
            for par in jData['thresholds']:
                # print(par)
                if 'A' in par['thresholdId']:
                    filteredInsights.append(x)
                    continue
        elif 'SParameters.json' in os.listdir(currentPath):
            try:
                jData = readJson(os.path.join(currentPath, 'SParameters.json'))
            except:
                print(x + ' SParameters.json is not readable')
                continue
            for par in jData['parameters']:
                if 'amount' in par['name']:
                    filteredInsights.append(x)
    
    return filteredInsights


def updateTh(path, InsList, factor):
    count = 0
    # print(factor)
    for j in InsList:
        # print(j)
        currentPath = os.path.join(path, j)
        if 'SThresholds.json' in os.listdir(currentPath):
            try:
                jData = readJson(os.path.join(currentPath, 'SThresholds.json'))
            except:
                print(j + ' SThresholds.json is not readable')
            for t in jData['thresholds']:
                if 'A' in t['thresholdId']:
                    newVal = int(int(t['value']) / factor)
                    t['value'] = str(newVal)
                    print(str(newVal))
            try:
                updateJson(os.path.join(currentPath, 'SThresholds.json'), jData)
                count += 1
            except:
                print(j + ' SThresholds.json wasn\'t updated')
        
        # if 'SParameters.json' in os.listdir(currentPath):
        #     try:
        #         jData = readJson(os.path.join(currentPath, 'SParameters.json'))
        #     except:
        #         print(j + ' SParameters.json is not readable')
        #     for p in jData['parameters']:
        #         if 'amount' in t['name']:
        #             p['value'] = str(int(float(p['value']) * factor))
        #     try:
        #         updateJson(os.path.join(currentPath, 'SParameters.json'), jData)
        #         count += 1
        #     except:
        #         print(j + ' SParameters.json wasn\'t updated')
        #
        # if 'SQuiz.json' in os.listdir(currentPath):
        #     try:
        #         jData = readJson(os.path.join(currentPath, 'SQuiz.json'))
        #     except:
        #         print(j + ' SQuiz.json is not readable')
        #     nextFrom = int(jData['ranges'][0]['from']) / factor
        #     for r in jData['ranges']:
        #         r['from'] = str(nextFrom)
        #         nextFrom = (int(r['to']) / factor) + 1
        #         r['to'] = str(int(r['to']) / factor)
        #     try:
        #         updateJson(os.path.join(currentPath, 'SQuiz.json'), jData)
        #         count += 1
        #     except:
        #         print(j + ' SQuiz.json wasn\'t updated')
    return count


def main(argv):
    print("Starting....")
    solution = os.path.join(argv[0], 'Insights')
    insightList = getList(solution)
    for x in insightList:
        currenPath = os.path.join(solution, x)
        if 'SThresholds.json' in os.listdir(currenPath):
            os.remove(os.path.join(currenPath, 'SThresholds.json'))
        if 'SParameters.json' in os.listdir(currenPath):
            os.remove(os.path.join(currenPath, 'SParameters.json'))
        if 'SQuiz.json' in os.listdir(currenPath):
            os.remove(os.path.join(currenPath, 'SQuiz.json'))
    print(len(insightList))


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 1 - solution_path = C:\GIT\boc\biz-units\perso-biz\Projects\BOC
    # 2 - factor
