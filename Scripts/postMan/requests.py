import sys

import requests


# def runApi(url, headers, api, id, context):
def getInsights(url, headers, id, context):
    if headers[2] is not None:
        getInsightsApi = {
            "type": "getInsights",
            "protocolVersion": "2.5",
            "autoGenerate": "true",
            "ctxId": context,
            "lang": "en"
        }
    rFinal = requests.post(url, headers=headers, json=getInsightsApi)
    print(rFinal)
    # api()


def main(argv):
    url = 'http://' + argv[0] + ':8080/pserver/execute?channel=' + argv[1]
    headers = {'Content-Type': 'application/json', 'authToken': argv[4], 'effectiveTime': argv[2]}
    if argv[6] is not None:
        useContext = argv[6]
    else:
        useContext = "showAll"
    argv[3](url, headers, argv[5], useContext)


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # [IP, CHANNEL, DATE, API, USER, ID, CONTEXT]
