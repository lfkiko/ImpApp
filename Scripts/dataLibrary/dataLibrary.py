import json
import os
import sys
from logging import info, error, warning

import pandas

from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath, getCol, getheader, getRow, writeJson


def getCostumeAttributes(EBPath, attributes, excel):
    costumeAttributes = {}
    categories = getheader(excel)
    for a in attributes:
        aJson = a + ".json"
        if aJson not in os.listdir(EBPath):
            library = getRow(excel, attributes.index(a) + 1)
            costumeAttributes[aJson] = dict()
            dictionary = costumeAttributes[aJson]
            dictionaryAttribute = ''
            for x in range(len(categories)):
                if library[x] != 'noData':
                    if categories[x] in ['dataItemLocation', 'tags', 'factName']:
                        dictionary.update({categories[x]: library[x].split(",")})
                    elif categories[x] == 'visibleLogic':
                        dictionary.update({categories[x]: library[x]})
                        dictionary.update({'triggerLogic': {}})
                        dictionary['triggerLogic'].update({'type': 'attribute'})
                        dictionary['triggerLogic'].update({'attribute': {}})
                        dictionaryAttribute = dictionary['triggerLogic']['attribute']
                        dictionaryAttribute.update({'id': dictionary['displayName']})
                        dictionaryAttribute.update({'type': dictionary['type']})
                        dictionaryAttribute.update({'dynamic': True})
                        dictionaryAttribute.update({'evalOnly': True})
                    elif categories[x] == 'techType':
                        dictionaryAttribute.update({categories[x]: library[x]})
                    else:
                        dictionary.update({categories[x]: library[x]})
            tmp = dictionary['triggerLogic']
            dictionary.pop('triggerLogic')
            dictionary.update({'triggerLogic': tmp})
    return costumeAttributes


def createCostumeAttributes(solution, costumeAttributes):
    info('Start writing costumed attributes ')
    dataAttribute = createPath(solution, 'SEditorDefinition\\DataAttribute')
    for jsonName in costumeAttributes:
        try:
            newJson = open(jsonName, "x")
        except:
            warning('all ready exist: ' + jsonName)
        
        jsonData = json.dumps(costumeAttributes[jsonName], indent=4)
        try:
            writeJson(newJson, jsonData)
        except:
            error('there was a problem writing: ' + jsonName)
        print(jsonName)
        print(jsonData)


def createAttribures(engagementBuilderPath, solution, attributes, costumeAttributes):
    for attribute in attributes:
        pass
    pass
    


def main(argv):
    info("updating DataAttribute")
    try:
        solution = getSolution(getPath('solution'))
    except:
        error(getPath('solution') + ' is not a correct path Data library didn\'t run')
        return
    
    try:
        engagementBuilderPath = createPath(getPath('EBPath'),
                                           "editor-product-bizpack\\product-editor-engage-biz-unit\\Core\\SEditorDefinition\\DataAttribute")
    except:
        error(getPath('EBPath') + ' is not a correct path Data library didn\'t run')
        return
    attributes = getCol(argv[0], 'id')
    costumeAttributes = getCostumeAttributes(engagementBuilderPath, attributes, argv[0])
    for a in list(attributes):
        if a + '.json' in costumeAttributes.keys():
            attributes.remove(a)
    # createCostumeAttributes(solution, costumeAttributes)
    createAttribures(engagementBuilderPath, solution, attributes, costumeAttributes)
    print(attributes)
    # print(os.listdir(engagementBuilderPath))
    # print(costumAttributes)
    info("DataAttribute was updated")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
