import threading
import pandas
import tkinter as tk
from tkinter import simpledialog
from logging import error


class threadingRequests(threading.Thread):
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()
    
    def addToCsv(self, user, insights, path):
        self.lock.acquire()
        insightList = list()
        for i in insights:
            insightList.append(i['useCaseId'])
        try:
            df = pandas.read_csv(path)
            df[user] = pandas.Series(insightList)
            df.to_csv(path, index=False)
        except pandas.errors.EmptyDataError:
            df = pandas.DataFrame({user: insightList})
            df.to_csv(path, index=False)
        self.lock.release()


class apis:
    defaultContext = 'showAll'
    
    def request(self, apisData, context):
        apis.defaultContext = context
        default = 'wait what'
        return getattr(self, apisData, lambda: default)()
    
    def getInsights(self):
        getInsightsApi = {
            "type": "getInsights",
            "protocolVersion": "2.5",
            "autoGenerate": "true",
            "ctxId": apis.defaultContext,
            "lang": "en"
        }
        return getInsightsApi
    
    def generateInsights(self):
        getInsightsApi = {
            "type": "generateInsights",
            "protocolVersion": "2.5",
            "autoGenerate": "true",
            "ctxId": apis.defaultContext,
            "lang": "en"
        }
        return getInsightsApi
    
    def getInsightDetails(self):
        insightsId = simpledialog.askstring(title='Api request', prompt='Enter insights id: ')
        getInsightsApi = {
            "type": "getInsightDetails",
            "protocolVersion": "2.5",
            "autoGenerate": "true",
            "insightId": insightsId,
            "ctxId": apis.defaultContext,
            "lang": "en"
        }
        return getInsightsApi
    
    def generateInsights(self):
        pass
    
    def generateInsights(self):
        pass
    
    def generateInsights(self):
        pass
    
    def generateInsights(self):
        pass


def apiErrors(errorsText, user):
    if 'Failed to retrieve DParty from DataSource' in errorsText:
        error('API ERROR: {0} do not exits'.format(user))
    
