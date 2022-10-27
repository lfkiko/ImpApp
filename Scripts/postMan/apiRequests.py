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
