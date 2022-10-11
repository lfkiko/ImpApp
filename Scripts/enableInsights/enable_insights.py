import json
import os
import shutil
import sys
from logging import info, error

from Scripts.toolBoox.toolBoox import valPath, readCsv, getSolution, modelVersion, getPath

searchedCoreFolders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                       os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]
searchedModleFolders = ['product-subscriptions-biz-unit', 'product-portfolio-biz-unit']


def valid_insight(insight_name):
    try:
        int(insight_name)
        return False
    except:
        pass
    for char in insight_name:
        if char in (' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            return False
    return True


def get_ucs_list(insight_name, ucs):
    try:
        return [insight_name + "_UC" + str(int(ucs))]
    except:
        return [insight_name + "_UC" + uc for uc in ucs.split(',')]


def build_sinsights(insight_name, ucs, insight_product_path):
    sinsight = {"id": insight_name,
                "insightMetadata": {
                    "activated": "TRUE"
                },
                "useCases": []
                }
    for uc in ucs:
        sinsight["useCases"].append({"id": uc, "activated": "TRUE"})
    
    with open(os.path.join(insight_product_path, "SInsight.json"), "w") as f:
        json.dump(sinsight, f, indent=4)


def search_insight_in_core(core, modelPath, insight_name, useModel):
    for core_folder in searchedCoreFolders:
        try:
            curr_folder = os.path.join(core, core_folder, "Core", "Insights")
        except:
            if useModel:
                curr_folder = os.path.join(modelPath, core_folder, "Core", "Insights")
            else:
                error('Couldn\'t find ' + core_folder + 'in the perso-core')
        
        if insight_name in os.listdir(curr_folder):
            return os.path.join(curr_folder, insight_name)


def overwrite_insight(core, solution, modelPath, insight_name, ucs, useModel):
    insight_core_path = search_insight_in_core(core, modelPath, insight_name, useModel)
    try:
        os.mkdir(os.path.join(solution, insight_name))
    except:
        info(os.path.join(solution, insight_name) + ' already exits')
        pass
    ucs_list = get_ucs_list(insight_name, ucs)
    for uc in ucs_list:
        try:
            shutil.copytree(os.path.join(insight_core_path, uc), os.path.join(solution, insight_name, uc))
        except Exception as e:
            if len(e.args) > 1 and 'Cannot create a file when that file already exists' == e.args[1]:
                print('insight uc already exists in solution', os.path.join(insight_core_path, uc))
            else:
                print("insight is not presented in the core: " + insight_name)
    build_sinsights(insight_name, ucs_list, os.path.join(solution, insight_name))


def runOverInsights(core, product, modelPath, enableCsv, useModel):
    for i in enableCsv.index:
        insightName = enableCsv['insight'][i]
        if not valid_insight(insightName):
            print("insight name is illegal: {}".format(insightName), "row: {}".format(i + 2))
        ucs = enableCsv['UC'][i]
        
        overwrite_insight(core, product, modelPath, insightName, ucs, useModel)


def main(argv):
    info("Starting Enable insights")
    corePath = os.path.join(getPath('corePath'), 'product-bizpack')
    modelPath = os.path.join(getPath('modelPath'), 'product-models-bizpack')
    try:
        solutionPath = os.path.join(getSolution(getPath('solution')), 'Insights')
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    
    if not os.path.exists(solutionPath):
        error(solutionPath + ' dosn\'t exists')
        return
    useModel = modelVersion(getPath('solution'))
    inputFile = argv[0]
    enableCsv = readCsv(inputFile)
    runOverInsights(corePath, solutionPath, modelPath, enableCsv, useModel)
    
    info('Enable Insights finished overwriting relevant insights')


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 file with the list of insights to enable
