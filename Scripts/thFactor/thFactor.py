import codecs
import json
import sys, os

from Scripts.toolBoox.toolBoox import getInsightsDir, getFile, readJson, fixPath, checkEndCode

searchedFolders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                   os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]


def searchForInsight(core, insight):
    for coreDir in searchedFolders:
        currentDir = os.path.join(core, coreDir, "Core", "Insights")
        if insight in os.listdir(currentDir):
            currentDir = os.path.join(currentDir, insight)
            if 'SThresholds.json' in os.listdir(currentDir) or 'SParameters.json' in os.listdir(currentDir):
                if os.path.exists(os.path.join(currentDir, 'SThresholds.json')):
                    currentDir = os.path.join(currentDir, 'SThresholds.json')
                else:
                    currentDir = os.path.join(currentDir, 'SParameters.json')
                
                print(readJson(currentDir).read())
                
                # print(checkEndCode(currentDir))
                # for parameter in readJson(currentDir):
                #     if 'Amount' in parameter['name']:
                #         print(insight)
                #         break
                #     else:
                #         print(insight + " has the json but don't have Amount")
            else:
                print(insight + " has not SThresholds.json or SParameters.json to modify")


def main(argv):
    core = os.path.join(readJson(getFile('settings'))['corePath'], 'product-bizpack')
    solution = getInsightsDir(argv[0])
    for insight in os.listdir(solution):
        searchForInsight(core, insight)
    # print(core)
    # print(solution)
    # print(argv[1])
    # print(insights)
    # # print(path)


if __name__ == "__main__":
    main(sys.argv[1:])

# argv[0] = solution path
# argv[1] = factor
