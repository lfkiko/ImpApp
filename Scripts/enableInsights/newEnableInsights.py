import os
import sys
from logging import info, error

from Scripts.toolBoox.excelJsonToolBox import readCsv
from Scripts.toolBoox.toolBoox import getPath, getSolution, modelVersion


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
    # runOverInsights(corePath, solutionPath, modelPath, enableCsv, useModel)
    
    info('Enable Insights finished overwriting relevant insights')


if __name__ == "__main__":
    main(sys.argv[1:])
