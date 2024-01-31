import os.path
import sys
from logging import error
from tkinter.messagebox import showwarning
from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson, prettyPrintJson, writeJsonMultiLang, \
	readJsonMultilingual, readJsonZip
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath, filesInZip


def removeAtributes(data):
	tmpData = data
	tmpData.pop("method")
	tmpData.pop("QA")
	if data["id"] == "purging":
		tmpData.pop("API")
		tmpData.pop("importMethods")
		tmpData.pop("pushNotificationOptIn")
	else:
		tmpData.pop("serverSynchronization")
		if data["importMethods"] != "autoRegister":
			tmpData.pop("API")
			tmpData.pop("context")
	return tmpData


def updateBatch(solution, batchData):
	try:
		currentBatchData = readJsonMultilingual(os.path.join(solution, batchData["id"] + ".json"))
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


# prettyPrintJson(currentBatchData)


def getSource(corePath, batchName):
	checkSourcePath = readJsonZip(corePath, "product-system-biz-unit.zip", batchName)
	return checkSourcePath


def updateProperties(solution, autoRegisterApi):
	propertiesPath = createPath(solution, 'srv-engage\\src\\main\\resources\\config\\pserver.service.properties')
	enabled = True
	method = True
	with open(propertiesPath, 'r+') as f:
		lines = f.readlines()
		f.seek(0)
		for line in lines:
			if '=' in line:
				tmpLine = line
				p, v = line.split('=')
				if p == 'AUTO_REGISTER_ENABLED':
					v = 'true'
					tmpLine = p + '=' + v + '\n'
					enabled = False
				if p == 'AUTO_REGISTER_METHOD':
					v = autoRegisterApi
					tmpLine = p + '=' + v + '\n'
					method = False
				f.write(tmpLine)
			else:
				f.write(line)
		if enabled:
			f.write('AUTO_REGISTER_ENABLED = true\n')
		if method:
			f.write('AUTO_REGISTER_METHOD = ' + autoRegisterApi + '\n')


def updateContexts(solution, context, groupName):
	insightsContextsPath = os.path.join(solution, 'Insights', 'SEntities', 'SInsightsContexts.json')
	contextJson = readJson(insightsContextsPath)
	for ctx in range(len(contextJson['insightsContexts'])):
		if contextJson['insightsContexts'][ctx]['contextId'] == context:
			contextJson['insightsContexts'][ctx]['config']['batchGroup'] = groupName
	updateJson(insightsContextsPath, contextJson)


def checkBatch(sourceFile, userFile):
	batch = dict()
	for x in userFile.key:
		if x not in ['id', 'active']:
			if x in sourceFile and userFile[x] != sourceFile[x]:
				batch[x] = userFile[x]
	return batch


def overrideBatch(solution, overrideFile, qaCopy, method):
	tmpOverrideFile = overrideFile
	filePath = os.path.join(solution, tmpOverrideFile['id'] + '.json')

	if method == "Modify":
		updateJson(filePath, tmpOverrideFile)
	else:
		writeJsonMultiLang(filePath, tmpOverrideFile)

	if qaCopy:
		qaPath = os.path.join(solution, tmpOverrideFile['id'] + '-qa.json')
		if method == "Modify":
			sourceFile = readJson(qaPath)
			overrideFile = tmpBatch(overrideFile, sourceFile)
		tmpOverrideFile['channel'] = overrideFile['channel'].replace('_LIVE', '_QA')
		tmpOverrideFile['id'] = overrideFile['id'] + '-qa'
		tmpOverrideFile['active'] = False
		if method == "Modify":
			updateJson(qaPath, tmpOverrideFile)
		else:
			writeJsonMultiLang(qaPath, tmpOverrideFile)


def tmpBatch(batchData, sourceFile):
	# tmpBatch = dict()
	tmpBatch = sourceFile
	addons = ["channel", "context", "groupName"]
	removeSameValue = list()
	for key in tmpBatch.keys():
		if key in batchData.keys():
			if tmpBatch[key] != batchData[key]:
				tmpBatch[key] = batchData[key]
			else:
				removeSameValue.append(key)
			if key in addons:
				addons.remove(key)
	# for key in removeSameValue:
	# 	tmpBatch.pop(key)
	if len(addons) > 0:
		for addon in addons:
			if addon not in tmpBatch.keys():
				tmpBatch[addon] = batchData[addon]

	return tmpBatch


def main(argv):
	startLog()
	try:
		solution = createPath(getSolution(getPath('solution')), 'Batch\\SBatch')
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return
	try:
		corePath = createPath(getPath('solution'), 'package\\target\\DataLoad')
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return
	method = argv[0]["method"]
	qa = argv[0]["QA"]
	if argv[0]["taskType"] == "adhoc":
		adhoc = True
	else:
		adhoc = False

	if method == "New Batch":
		if not os.path.exists(os.path.join(solution, argv[0]["id"] + ".json")):
			sourceFile = getSource(corePath, argv[0]["id"] + ".json")
			if adhoc:
				argv[0]['id'] = argv[0]['id'] + '-adhoc'
		else:
			print("check")
			showwarning("Batch exists", "You choosed New Batch for method but there's already a batc.\nPlease change method and press the RUN button.")
			return

	elif method == "Modify":
		if os.path.exists(os.path.join(solution, argv[0]["id"] + ".json")):
			if adhoc:
				sourceFile = readJson(os.path.join(solution, argv[0]["id"] + "-adhoc.json"))
			else:
				sourceFile = readJson(os.path.join(solution, argv[0]["id"] + ".json"))
		else:
			showwarning("No batch", "You choosed Modify for method but there's nothing to modify.\nPlease change method and press the RUN button.")
			return

	prettyPrintJson(argv[0])
	batch = tmpBatch(argv[0], sourceFile)
	prettyPrintJson(batch)
	overrideBatch(solution, batch, qa, method)

	if "autoRegister" in argv[0]['importMethods']:
		updateProperties(getPath('solution'), argv[0]['API'])
		updateContexts(getSolution(getPath('solution')), argv[0]['context'], argv[0]['groupName'])

	endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

#     0 - batch data
