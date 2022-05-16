import sys
import pandas as pd
import csv

from Scripts.toolBoox.toolBoox import getFile


def activated_insights(file_name, process):
    data = pd.read_excel(file_name, usecols=['Insight', 'Activated'])
    insights = [['insight', 'UC']]
    temp = list()
    if process == "active":
        for i in data.index:
            if data['Activated'][i] == 'v':
                temp.append(data['Insight'][i])
    elif process == "visible":
        for i in data.index:
            temp.append(data['Insight'][i])
    mid_data = sorted(set(temp))
    for i in mid_data:
        insights.append([i, 'x'])
    
    return insights


def ucs_activation(file_name, insights_list):
    data = pd.read_excel(file_name, usecols=['UC'])
    insights = insights_list
    name = str
    uc = int
    for i in data['UC']:
        if i[:3] != "SUB":
            ins = i.rsplit("_")
            name = ins[0]
            uc = ins[1][2:]
        elif i[:3] == "SUB":
            ins = i.rsplit("_", 1)
            name = ins[0]
            uc = ins[1][2:]
        for j in insights:
            if j[0] == name:
                if j[1] == 'x':
                    j[1] = str(uc)
                    # print(j[1])
                else:
                    num = str(j[1]) + "," + uc
                    # print(num)
                    j[1] = num
    
    return insights


def reformatList(insights_list):
    insights = insights_list
    for i in insights:
        if len(i[1]) == 1:
            num = '\'' + str(1) + '\''
            i[1] = num
    
    return insights


def write_input_insights(insights_list, csv_file):
    header = insights_list[0]
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(1, len(insights_list) - 1):
            writer.writerow(insights_list[i])


def main(argv):
    file_raw = getFile(argv[0] + "_raw")
    file_name = getFile(argv[0])
    insights = activated_insights(file_raw, argv[1])
    ucs = ucs_activation(file_raw, insights)
    insights_list = reformatList(ucs)
    write_input_insights(insights_list, file_name)


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # [file name, active/visible]
