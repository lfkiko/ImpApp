import os
import shutil
import sys

from Scripts.toolBoox.toolBoox import readJson, readCsv, writeCsv, getCol


def find_relevant_users(core_path, extraUsers, Busers, modified):
    relevant_user = []
    core_demo_data_path = core_path + "\\product-demo-data-biz-unit\\Core\\DemoData"
    if Busers:
        for file in os.listdir(core_demo_data_path):
            if file.startswith("B_1") or file.startswith("B_2"):
                relevant_user.append(file)
    if modified:
        for x in extraUsers:
            relevant_user.append(x)
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
    core = argv[0]
    product = argv[1] + "$QA"
    extraUsers = getCol(argv[5], 'USERS')
    relevant_user = find_relevant_users(core, extraUsers, argv[3], argv[4])
    copy_users(relevant_user, core, product)
    modify_users_in_solution(product, os.listdir(product + "\DemoData"), argv[2])
    print("Overwriting finished")


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 core_path = C:\GIT\perso-core\product-bizpack
# 1 solution = C:\GIT\boc\biz-units\perso-biz\Projects\BOC$QA
# 2 properties dictionary
# 3 B_users checkBox bool
# 4 modified checkBox bool
# 5 file name
