import json
import os
import sys
from logging import info, error, warning

from Scripts.toolBoox.excelJsonToolBox import getheader, getRow, writeJson, readJson, updateJson, getCol, checkEndCode, \
    readJsonUtf8Sig
from Scripts.toolBoox.toolBoox import createPath, getSolution, getPath


def getCostumeAttributes(EBPath, attributes, excel):
    costumeAttributes = {}
    categories = getheader(excel)
    for a in attributes:
        aJson = a + ".json"
        if aJson not in os.listdir(EBPath):
            row = getRow(excel, attributes.index(a) + 1)
            costumeAttributes[aJson] = dict()
            dictionary = costumeAttributes[aJson]
            dictionaryAttribute = ''
            for x in range(len(categories)):
                if row[x] != 'noData':
                    if categories[x] in ['dataItemLocation', 'tags', 'factName', '']:
                        dictionary.update({categories[x]: row[x].split(",")})
                    elif categories[x] == 'visibleLogic':
                        dictionary.update({categories[x]: row[x]})
                        dictionary.update({'triggerLogic': {}})
                        dictionary['triggerLogic'].update({'type': 'attribute'})
                        dictionary['triggerLogic'].update({'attribute': {}})
                        dictionaryAttribute = dictionary['triggerLogic']['attribute']
                        dictionaryAttribute.update({'id': dictionary['displayName']})
                        dictionaryAttribute.update({'type': dictionary[row[categories.index('type')]]})
                        dictionaryAttribute.update({'dynamic': True})
                        dictionaryAttribute.update({'evalOnly': True})
                    elif categories[x] == 'techType':
                        dictionaryAttribute.update({categories[x]: row[x]})
                    elif categories[x] == 'availableValues':
                        dictionaryAttribute.update({'dynamic': {}})
                        dictionaryAttribute['dynamic'].update({'sourceOfData': 'list'})
                        dictionaryAttribute['dynamic'].update({'values': [row[x].split(",")]})
                    else:
                        dictionary.update({categories[x]: row[x]})
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


def createAttributes(engagementBuilderPath, solution, attributes, costumeAttributes, updatedAttribute, excel):
    info('Start writing new attributes')
    relevantAttributes = list()
    solutionPath = createPath(solution, 'SEditorDefinition\\DataAttribute')
    categories = getheader(excel)
    for attribute in attributes:
        if attribute in updatedAttribute or attribute + '.json' in costumeAttributes:
            relevantAttributes.append(attribute)
    for attribute in relevantAttributes:
        attributeFileName = attribute + '.json'
        attributePath = os.path.join(engagementBuilderPath, attributeFileName)
        attributeJson = readJson(attributePath)
        attributeJson.pop('triggerLogic')
        row = getRow(excel, attributes.index(attribute))
        for x in range(len(categories)):
            if categories[x] in attributeJson.keys():
                if row[x] != 'noData':
                    if categories[x] in ['dataItemLocation', 'tags', 'factName']:
                        attributeJson[categories[x]] = row[x].split(",")
                    else:
                        attributeJson[categories[x]] = row[x]
                else:
                    attributeJson.pop(categories[x])
        attributeJson.pop('dataAttributeId')
        try:
            updateJson(os.path.join(solutionPath, attributeFileName), attributeJson)
        except:
            error('couldn\'t overwrite ' + attributeFileName)
    
    info('New attributes were written')


def updateAttributes(attributes, solution, excel):
    info('Start updating overridden attributes ')
    updatedAttribute = list()
    activate = getCol(excel, 'activate')
    dataAttribute = createPath(solution, 'SEditorDefinition\\DataAttribute')
    for a in list(attributes):
        if a + '.json' in os.listdir(dataAttribute):
            jsonFile = os.path.join(dataAttribute, a + '.json')
            aJson = readJson(jsonFile)
            if aJson['activate'] != activate[attributes.index(a)]:
                aJson['activate'] = activate[attributes.index(a)]
                updateJson(jsonFile, aJson)
                updatedAttribute.append(a)
    return updatedAttribute


def removeDeactivated(solution):
    info('Start remove deactivated from solution')
    countFalse = 0
    countAll = 0
    dataAttributePath = createPath(solution, 'SEditorDefinition\\DataAttribute')
    for attribute in [j for j in os.listdir(dataAttributePath) if os.path.isfile(os.path.join(dataAttributePath, j))]:
        countAll += 1
        jsonPath = os.path.join(dataAttributePath, attribute)
        dataAttribute = readJsonUtf8Sig(jsonPath)
        
        # print(readJsonUtf8Sig(jsonPath))
        if dataAttribute['activate'] == 'FALSE':
            countFalse += 1
            # os.remove(jsonPath)
    print(str(countFalse) + " out of " + str(countAll))
    info('Finished remove deactivated from solution')


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
    if argv[1]:
        attributes = getCol(argv[0], 'id')
        costumeAttributes = getCostumeAttributes(engagementBuilderPath, attributes, argv[0])
        updatedAttribute = updateAttributes(attributes, solution, argv[0])
        createCostumeAttributes(solution, costumeAttributes)
        createAttributes(engagementBuilderPath, solution, attributes, costumeAttributes, updatedAttribute, argv[0])
    if argv[2]:
        removeDeactivated(solution)
    info("DataAttribute was updated")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
    # 1 - update data library - boolean
    # 2 - remove deactivated - boolean
