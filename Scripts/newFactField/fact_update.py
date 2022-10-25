import json
import sys
import os
from Scripts.toolBoox.excelJsonToolBox import readJson

def write_json(path, json_object):
    with open(path, "w") as f:
        json.dump(json_object, f, indent=2, ensure_ascii=False)


def get_insight_list(insight_path):
    with open(insight_path, "r") as f:
        insights = f.read()
    return insights.split('\n')


def update_misc_jinsight_facts(insight_path, insight_uc, fact, new_field, new_dis, att):
    jinsightfacts_path = insight_path + "\\" + insight_uc + "\\JInsightFacts.json"
    jinsightfacts = readJson(jinsightfacts_path)
    jinsightfacts[fact]['cols'].append(new_field)
    for item in jinsightfacts[fact]['rows']:
        item.append(new_dis)
    jinsightfacts[fact]['attributesTypes'].append(att)
    
    write_json(jinsightfacts_path, jinsightfacts)


def update_sstory_dif(insight_path, insight_uc):
    sstoryDiff_path = insight_path + "\\" + insight_uc + "\\SStoryDefinition.json"
    sstoryDiff = readJson(sstoryDiff_path)
    mydialog = ""
    for dialog in sstoryDiff['dialogs']:
        for block in dialog['blocks']:
            if block.get('type', '') == 'tranList':
                block.update({"subType": "dateComment", "dateComment": "dateCommentTxt"})
                mydialog = dialog['id']
    
    write_json(sstoryDiff_path, sstoryDiff)
    return mydialog


def update_sstory_text(insight_path, insight_uc, dialog):
    sstoryText_path = insight_path + "\\" + insight_uc + "\\SStoryText.json"
    sstoryText = readJson(sstoryText_path)
    
    if sstoryText.get(dialog):
        sstoryText[dialog]["en"].update({"dateCommentTxt": "{{misc}}"})
    else:
        sstoryText.update({dialog: {"en": {"dateCommentTxt": "{{misc}}"}}})
    write_json(sstoryText_path, sstoryText)


def run_misc_update(solution, insights, fact, new_field, new_dis, att):
    for insight in insights:
        insight_ucs = []
        insight_path = solution + "\\Insights\\" + insight
        for root, dirnames, filenames in os.walk(insight_path):
            insight_ucs = dirnames
            break
        for insight_uc in insight_ucs:
            try:
                update_misc_jinsight_facts(insight_path, insight_uc, fact, new_field, new_dis, att)
            except Exception as e:
                print('could not update jinsight facts for: ', insight_uc)
                continue


def main(argv):
    solution = argv[0]
    fact = argv[1]
    new_field = argv[2]
    att = argv[3]
    new_dis = " ".join(argv[4:])
    insights = get_insight_list('insights.txt')
    run_misc_update(solution, insights, fact, new_field, new_dis, att)


if __name__ == "__main__":
    main(sys.argv[1:])

# solution = C:\GIT\[project_name]\biz-units\perso-biz\Projects\[project_name] [fact] [new_field] [type] [dis]
