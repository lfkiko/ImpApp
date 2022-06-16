import json
import os
import shutil
import sys

from Scripts.toolBoox.toolBoox import valPath, readCsv

searched_folders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                    os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]


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


def search_insight_in_core(core, insight_name):
    for core_folder in searched_folders:
        curr_folder = os.path.join(core, core_folder, "Core", "Insights")
        if insight_name in os.listdir(curr_folder):
            return os.path.join(curr_folder, insight_name)


def overwrite_insight(core, product, insight_name, ucs):
    insight_core_path = search_insight_in_core(core, insight_name)
    try:
        os.mkdir(os.path.join(product, insight_name))
    except:
        pass
    ucs_list = get_ucs_list(insight_name, ucs)
    for uc in ucs_list:
        try:
            shutil.copytree(os.path.join(insight_core_path, uc), os.path.join(product, insight_name, uc))
        except Exception as e:
            if len(e.args) > 1 and 'Cannot create a file when that file already exists' == e.args[1]:
                print('insight uc already exists in solution', os.path.join(insight_core_path, uc))
            else:
                print("insight is not presented in the core: " + insight_name)
    build_sinsights(insight_name, ucs_list, os.path.join(product, insight_name))


def run_over_insights(core, product, df):
    for i in df.index:
        insight_name = df['insight'][i]
        if not valid_insight(insight_name):
            print("insight name is illegal: {}".format(insight_name), "row: {}".format(i + 2))
        ucs = df['UC'][i]
        
        overwrite_insight(core, product, insight_name, ucs)


def main(argv):
    print("Starting....")
    core = os.path.join(argv[0], 'product-bizpack')
    product = os.path.join(argv[1], 'Insights')
    if not valPath(product):
        return "fuck my life"
    input_file = argv[2]
    df = readCsv(input_file)
    run_over_insights(core, product, df)
    return "Overwriting finished"


if __name__ == "__main__":
    main(sys.argv[1:])

# core_path = C:\GIT\perso-core
# product_path = C:\GIT\boc\biz-units\perso-biz\Projects\BOC
