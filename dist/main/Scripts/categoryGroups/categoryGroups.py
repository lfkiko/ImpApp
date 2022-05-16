import json
import sys

from Scripts.toolBoox.toolBoox import getCol, fixPath, writeJson, valPath, FindDir


def createLanguages(fileName):
    langages = list()
    lang1 = getCol(fileName, 'language 1')
    lang2 = getCol(fileName, 'language 2')
    lang3 = getCol(fileName, 'language 3')
    lang4 = getCol(fileName, 'language 4')
    for i in range(len(lang1)):
        langages.append([lang1[i], lang2[i], lang3[i], lang4[i]])
    return langages


def createSCategoryGroups(categories, direction, languages, numOfLang, listOfLanguages):
    langs = int(numOfLang)
    data = {'categoryGroups': []}
    for i in range(len(categories)):
        new_cg = {'id': categories[i],
                  'description': {'langMap': {}},
                  'clientCategoryId': "C" + categories[i]}
        for j in range(langs):
            new_cg['description']['langMap'][listOfLanguages[j]] = languages[i][j]
        if direction[i] in ["Both", "Income", "Expenses"]:
            new_cg['direction'] = direction[i]
        data['categoryGroups'].append(new_cg)
    return data


def main(argv):
    path = fixPath(FindDir(argv[0], 'SEntities'))
    json_name = path + "/SCategoryGroups.json"
    categories = getCol(argv[1], 'CG')
    direction = getCol(argv[1], 'direction')
    languages = createLanguages(argv[1])
    lang_num = argv[2]
    lan_names = argv[3]
    s_category_groups = createSCategoryGroups(categories, direction, languages, lang_num, lan_names)
    json_data = json.dumps(s_category_groups, indent=4)
    writeJson(json_name, json_data)


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # [Path, excel file, number of languages, list of languages]
