import codecs
import json
import os
import sys
from logging import info, error

from Scripts.toolBoox.toolBoox import getCol, getPath, getSolution


def createLanguages(fileName):
    langages = list()
    lang1 = getCol(fileName, 'language 1')
    lang2 = getCol(fileName, 'language 2')
    lang3 = getCol(fileName, 'language 3')
    lang4 = getCol(fileName, 'language 4')
    for i in range(len(lang1)):
        langages.append([lang1[i], lang2[i], lang3[i], lang4[i]])
    return langages


def createSCategoryGroups(categories, direction, languages, numOfLang, listOfLanguages, CType):
    langs = int(numOfLang)
    data = {}
    if CType is 'SCategoryGroups':
        data = {'categoryGroups': []}
    elif CType is 'SSubCategories':
        data = {'subCategories': []}
    for i in range(len(categories)):
        new_cg = {'id': categories[i],
                  'description': {'langMap': {}}}
        for j in range(langs):
            new_cg['description']['langMap'][listOfLanguages[j]] = languages[i][j]
        if CType == "SCategoryGroups":
            if direction[i] in ["Both", "Income", "Expenses"]:
                new_cg['direction'] = direction[i]
            data['categoryGroups'].append(new_cg)
        elif CType == "SSubCategories":
            data['subCategories'].append(new_cg)
    return data


# Due to multi-lingual content we can't use toolbox.writeJson.
# this is why we have this method
def writeCategoriesJson(file_name, json_object):
    with codecs.open(file_name, 'a+', 'utf-8') as f:
        f.write(json.dumps(json_object, ensure_ascii=False, indent=4))


def main(argv):
    info("Creating new SCategoryGroups.json override")
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEntities')
        try:
            os.path.exists(solution)
        except:
            os.mkdir(solution)
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    
    json_name = os.path.join(solution, argv[3] + ".json")
    categories = getCol(argv[0], 'CG')
    direction = getCol(argv[0], 'direction')
    languages = createLanguages(argv[0])
    lang_num = argv[1]
    lan_names = argv[2]
    s_category_groups = createSCategoryGroups(categories, direction, languages, lang_num, lan_names, argv[3])
    writeCategoriesJson(json_name, s_category_groups)


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 excel file
    # 1 number of languages
    # 2 list of languages
    # 3 type
