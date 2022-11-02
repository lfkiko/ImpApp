class batchJson:
    def jsonData(self, batchName, batchData):
        batchJson.data = batchData
        name = batchName.replace('-', '')
        default = 'problem'
        return getattr(self, name, lambda: default)()
    
    def dataassets(self):
        dataAssetsJson = {
            "id": batchJson.data.ids.batchId.text,
            "active": True,
            "channel": batchJson.data.ids.channel.text,
            "startingTime": batchJson.data.ids.startingTime.text,
            "endingTime": batchJson.data.ids.endingTime.text,
            "excludeDays": batchJson.data.ids.excludeDays.text,
            "recurrencePattern": batchJson.data.ids.recurrencePattern.text,
            "flowId": batchJson.data.ids.flowId.text,
            "maxResult": int(batchJson.data.ids.maxResult.text),
            "importPagingSize": int(batchJson.data.ids.importPagingSize.text),
            "threadSplitter": int(batchJson.data.ids.threadSplitter.text),
            "importMethods": [
                batchJson.data.ids.importMethods.text
            ],
            "taskType": batchJson.data.ids.taskType.text,
            "intervalInMin": int(batchJson.data.ids.intervalInMin.text),
            "pushNotificationOptIn": bool(batchJson.data.ids.startingTime.text),
            "groupName": batchJson.data.ids.groupName.text
        }
        if dataAssetsJson['importMethods'][0] == 'autoRegister':
            dataAssetsJson['context'] = batchJson.data.ids.Context.text
        return dataAssetsJson
    
    def pushnotificationonlysend(self):
        pushNotificationOnlySendJson = {
            "id": batchJson.data.ids.batchId.text,
            "active": True,
            "channel": batchJson.data.ids.channel.text,
            "startingTime": batchJson.data.ids.startingTime.text,
            "endingTime": batchJson.data.ids.endingTime.text,
            "excludeDays": batchJson.data.ids.excludeDays.text,
            "recurrencePattern": batchJson.data.ids.recurrencePattern.text,
            "flowId": batchJson.data.ids.flowId.text,
            "context": batchJson.data.ids.ContextA.text,
            "autoGenerate": bool(batchJson.data.ids.autoGenerate.text),
            "insightsElapsed": int(batchJson.data.ids.insightsElapsed.text),
            "maxResult": int(batchJson.data.ids.maxResult.text),
            "importPagingSize": int(batchJson.data.ids.importPagingSize.text),
            "threadSplitter": int(batchJson.data.ids.threadSplitter.text),
            "importMethods": [
                batchJson.data.ids.importMethods.text
            ],
            "taskType": batchJson.data.ids.taskType.text,
            "intervalInMin": int(batchJson.data.ids.intervalInMin.text),
            "pushNotificationOptIn": bool(batchJson.data.ids.startingTime.text),
            "groupName": batchJson.data.ids.groupName.text
        }
        return pushNotificationOnlySendJson
    
    def actdataassets(self):
        actDataAssetsJson = {
            "id": batchJson.data.ids.batchId.text,
            "active": True,
            "channel": batchJson.data.ids.channel.text,
            "startingTime": batchJson.data.ids.startingTime.text,
            "endingTime": batchJson.data.ids.endingTime.text,
            "excludeDays": batchJson.data.ids.excludeDays.text,
            "recurrencePattern": batchJson.data.ids.recurrencePattern.text,
            "flowId": batchJson.data.ids.flowId.text,
            "maxResult": int(batchJson.data.ids.maxResult.text),
            "importPagingSize": int(batchJson.data.ids.importPagingSize.text),
            "threadSplitter": int(batchJson.data.ids.threadSplitter.text),
            "importMethods": [
                batchJson.data.ids.importMethods.text
            ],
            "taskType": batchJson.data.ids.taskType.text,
            "intervalInMin": int(batchJson.data.ids.intervalInMin.text),
            "pushNotificationOptIn": bool(batchJson.data.ids.startingTime.text),
            "groupName": batchJson.data.ids.groupName.text
        }
        return actDataAssetsJson
    
    def purging(self):
        purgingJson = {
            "id": batchJson.data.ids.batchId.text,
            "active": True,
            "channel": batchJson.data.ids.channel.text,
            "startingTime": batchJson.data.ids.startingTime.text,
            "endingTime": batchJson.data.ids.endingTime.text,
            "excludeDays": batchJson.data.ids.excludeDays.text,
            "intervalInMin": int(batchJson.data.ids.intervalInMin.text),
            "flowId": batchJson.data.ids.flowId.text,
            "context": batchJson.data.ids.ContextA.text,
            "maxResult": int(batchJson.data.ids.maxResult.text),
            "importPagingSize": int(batchJson.data.ids.importPagingSize.text),
            "threadSplitter": int(batchJson.data.ids.threadSplitter.text),
            "taskType": batchJson.data.ids.taskType.text,
            "serverSynchronization": bool(batchJson.data.ids.startingTime.text),
            "recurrencePattern": batchJson.data.ids.recurrencePattern.text
        }
        return purgingJson
