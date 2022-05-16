import os
import shutil
import sys

from Scripts.toolBoox.toolBoox import readJson, readCsv, writeCsv


def find_relevant_users(core_path):
    relevant_user = []
    core_demo_data_path = core_path + "\\product-demo-data-biz-unit\\Core\\DemoData"
    for file in os.listdir(core_demo_data_path):
        if file.startswith("B_1") or file.startswith("B_2"):
            relevant_user.append(file)
    return relevant_user


def copy_users(relevant_user, core_path, solution_qa_path):
    solution_demodata = solution_qa_path + "\\DemoData"
    core_demo_data_path = core_path + "\\product-demo-data-biz-unit\\Core\\DemoData"
    try:
        os.mkdir(solution_demodata)
    except:
        pass
    
    for user in relevant_user:
        try:
            shutil.copytree(core_demo_data_path + "\\" + user, solution_demodata + "\\" + user)
        except:
            raise Exception("insight use case is not presented in the core: ", user)


def modify_user(solution_qa_path, user, local_currency, foreign_currency, country_name, country_code):
    def update_currency(current_currency):
        if current_currency == "USD":
            return local_currency
        elif current_currency == "EUR":
            return foreign_currency
        else:
            return current_currency
    
    def update_country_code(current_country):
        if current_country != country_code:
            return country_code
        else:
            return current_country
    
    def update_country_name(current_country):
        if current_country != country_name:
            return country_name
        else:
            return current_country
    
    def update_column(column, file, func):
        # df = readCsv(solution_qa_path + "\\" + user + "\\" + file)
        try:
            df = readCsv(solution_qa_path + "\\" + user + "\\" + file)
            for i in range(len(df[column])):
                df.loc[i, column] = func(df[column][i])
            writeCsv(solution_qa_path + "\\" + user + "\\" + file, df)
        except:
            print(solution_qa_path + "\\" + user + "\\" + file, "col " + column + " does not exist")
    
    update_column("currencyCd", "DAccount.csv", update_currency)
    update_column("currencyCd", "DTransaction.csv", update_currency)
    update_column("currencyCdOriginal", "DTransaction.csv", update_currency)
    update_column("countryCd", "DLocation.csv", update_country_code)
    update_column("countryName", "DLocation.csv", update_country_name)


def modify_users_in_solution(solution_qa_path, users, input_json):
    for user in users:
        modify_user(solution_qa_path + "\\DemoData", user, input_json["LocalCurrency"], input_json["ForeignCurrency"],
                    input_json["CountryName"], input_json["CountryCode"])


def main(argv):
    print("Starting....")
    # NEXT LINE NEEDS TO BE CHANGED!!!!
    input_file = 'input.json'
    core = argv[0]
    product = argv[1] + "$QA"
    input_json = readJson(input_file)
    # find_relevant_users METHOD NEEDS TO BE FIXED!!!!
    relevant_user = ['BudgetSuperstar_1', 'BudgetTracker_1', 'BudgetTracker_2', 'ConsistAbove_1',
                     'ConsistBelow_1', 'Milestones_1', 'Milestones_3', 'RecommendBudget_1', 'RecommendBudget_3',
                     'RecommendBudget_5', 'RecommendBudget_7', 'RecommendBudget_9', 'RecommendBudget_11',
                     'RecommendBudgetEvents_1', 'RecommendBudgetEvents_2', 'RecommendBudgetEvents_3',
                     'RecommendBudgetEvents_4', 'RecommendBudgetEvents_5', 'RecommendBudgetEvents_7',
                     'RecommendBudgetEvents_8']
    # find_relevant_users(core)
    copy_users(relevant_user, core, product)
    modify_users_in_solution(product, relevant_user, input_json)
    print("Overwriting finished")


if __name__ == "__main__":
    main(sys.argv[1:])

# core_path = C:\GIT\perso-core\product-bizpack
# solution = C:\GIT\boc\biz-units\perso-biz\Projects\BOC$QA
#
