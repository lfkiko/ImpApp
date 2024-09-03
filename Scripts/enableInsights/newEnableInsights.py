from logging import warning
import shutil
import os
import sys
from tkinter.messagebox import askyesno
import zipfile
import Scripts.toolBoox as Tool



def removeDeactivated(Sinsights, ucList):
	recursive = False
	ucs = ucList
	ucToRemove = int()
	for uc in range(len(Sinsights['useCases'])):
		if Sinsights['useCases'][uc]['id'] in ucs:
			ucToRemove = uc
			recursive = True
			break
	if recursive:
		ucs.remove(Sinsights['useCases'][uc]['id'])
		Sinsights['useCases'].remove(ucToRemove)
		if len(ucs) > 0:
			return removeDeactivated(Sinsights, ucs)
	return Sinsights


def cleanSInsight(ucsList, SInsightPath):
	try:
		SInsightData = Tool.readJson(SInsightPath)
	except Exception as e:
		print(SInsightPath)
		Tool.error(e.__str__())
		return
	if 'dependencies' in SInsightData.keys():
		SInsightData.pop('dependencies')

	keysToRemove = list(SInsightData['insightMetadata'].keys())
	for key in ['activated', 'name']:
		keysToRemove.remove(key)

	for key in keysToRemove:
		SInsightData['insightMetadata'].pop(key)

	SInsightData['insightMetadata']['activated'] = 'TRUE'

	ucs = len(SInsightData['useCases'])
	toRemove = []
	for uc in range(ucs):
		if SInsightData['useCases'][uc]['id'] in ucsList:
			SInsightData['useCases'][uc]['activated'] = 'TRUE'
			for k in ['insightId', 'storyId', 'description']:
				if k in SInsightData['useCases'][uc].keys():
					SInsightData['useCases'][uc].pop(k)
		else:
			toRemove.append(SInsightData['useCases'][uc]['id'])
	if len(toRemove) == 0:
		# SInsightData = removeDeactivated(SInsightData, toRemove)
		for i in reversed(toRemove):
			SInsightData['useCases'].remove(i)
	Tool.updateJson(SInsightPath, SInsightData)


def createInsightDirectory(solutionPath, insights, client):
	for i in insights:
		try:
			os.mkdir(os.path.join(solutionPath, i))
			if client != "":
				os.mkdir(os.path.join(solutionPath, i, client))
				os.mkdir(os.path.join(solutionPath, i, "facts"))
		except Exception as e:
			if 'already exists' in e.__str__():
				warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


def createUcDirectory(solutionPath, ucs, client):
	for u in ucs:
		try:
			insight = u[0: u.rindex('_')]
		except Exception as e:
			Tool.error(e + "for " + u)

		if client != "":
			try:
				os.mkdir(os.path.join(solutionPath, insight, client, u))
				os.mkdir(os.path.join(solutionPath, insight, "facts", u))
			except Exception as e:
				if 'already exists' in e.__str__():
					warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		else:
			try:
				os.mkdir(os.path.join(solutionPath, insight, u))
			except Exception as e:
				if 'already exists' in e.__str__():
					warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


def ucsDict(insights, ucs):
	tmpDict = dict()
	for i in insights:
		tmpDict[i] = list()
		for u in ucs:
			if i == u[0: u.rindex('_')]:
				tmpDict[i].append(u)
	return tmpDict


def overwriteInsight(solution, corePath, insight, allUcs, client):
	insightCorePath = ""
	try:
		insightZipDir = Tool.searchInsightInCore(corePath, insight)
		insightCorePath = os.path.join(corePath, insightZipDir)
		if insightZipDir == FileNotFoundError:
			return
	except Exception as e:
		Tool.error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	finally:
		insightPath = os.path.join(solution, insight)
		insightFacts = os.path.join(solution, insight, 'facts')
		if insightCorePath == "":
			return
		with zipfile.ZipFile(insightCorePath) as z:
			srcFiles = Tool.filesInZip(corePath, insightZipDir, 'Core/Insights/' + insight + '/')
			for file in srcFiles:
				if file.split('/')[-1] == 'SInsight.json':
					try:
						with z.open(file) as j:
							sInsight = Tool.jsonifyZip(j.read())
							if os.path.exists(os.path.join(insightPath, 'SInsight.json')):
								Tool.updateJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
							else:
								Tool.writeJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
					except Exception as e:
						Tool.error(e.__str__())
					cleanSInsight(allUcs[insight], os.path.join(insightPath, 'SInsight.json'))
				uc = file.split('/')[-2]
				fileName = file.split('/')[-1]
				copy = False
				if client in file.split('/'):
					if uc in allUcs[insight] and fileName != '':
						tempInsightPath = os.path.join(insightPath, client, file.split('/')[-2], file.split('/')[-1])
						copy = True
				elif client == '':
					if uc in allUcs[insight] and fileName != '':
						tempInsightPath = os.path.join(insightPath, file.split('/')[-2], file.split('/')[-1])
						copy = True
				elif 'facts' in file.split('/'):
					if uc in allUcs[insight] and fileName != '':
						tempInsightPath = os.path.join(insightFacts, file.split('/')[-2], file.split('/')[-1])
						copy = True

				if copy:
					try:
						with z.open(file) as ucj:
							jsonFile = Tool.jsonifyZip(ucj.read())
							if os.path.exists(tempInsightPath):
								Tool.updateJsonMultiLang(tempInsightPath, jsonFile)
							else:
								Tool.writeJsonMultiLang(tempInsightPath, jsonFile)
					except Exception as e:
						print('here - ' + file.split('/')[-2] + '/' + file.split('/')[-1])
						Tool.error(e.__str__())


def removeLayer(solution, client):
	insights = list(os.listdir(solution))
	insights.remove("SEntities")
	for insight in insights:
		insightPath = os.path.join(solution, insight)
		clientPath = os.path.join(solution, insight, client)
		shutil.copytree(clientPath, insightPath, dirs_exist_ok=True)
		for uc in os.listdir(clientPath):
			ucPath = os.path.join(clientPath, uc)
			for file in os.listdir(ucPath):
				os.remove(os.path.join(ucPath, file))
			if len(os.listdir(ucPath)) == 0:
				os.rmdir(ucPath)
		if len(os.listdir(clientPath)) == 0:
			os.rmdir(clientPath)
	Tool.endLog()


def removeFacts(solution):
	insights = list(os.listdir(solution))
	insights.remove("SEntities")
	for insight in insights:
		insightPath = os.path.join(solution, insight)
		factsPath = os.path.join(insightPath, "facts")
		for uc in os.listdir(factsPath):
			shutil.copy2(os.path.join(factsPath, uc, 'JInsightFacts.json'), os.path.join(insightPath, uc))
			os.remove(os.path.join(factsPath, uc, 'JInsightFacts.json'))
			if len(os.listdir(os.path.join(factsPath, uc))) == 0:
				os.rmdir(os.path.join(factsPath, uc))
		if len(os.listdir(factsPath)) == 0:
			os.rmdir(factsPath)
	Tool.endLog()


def main(argv):
	Tool.startLog()
	try:
		solution = Tool.getSolution(Tool.getPath('solution'))
	except:
		Tool.error(Tool.getPath('solution') + ' is not a correct path Demo data didn\'t run')
		return

	try:
		corePath = Tool.createPath(Tool.getPath('solution'), 'package\\target\\DataLoad')
	except Exception as e:
		Tool.error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	starterVersion = Tool.getStarterVersion(Tool.getPath('solution'))
	if int(starterVersion[0]) > 7 or (int(starterVersion[0]) == 7 and int(starterVersion[2]) >= 7):
		client = Tool.chooseClient()
	else:
		client = ""

	channels = Tool.getChannels(solution)
	if len(channels) > 3:
		theChannel = Tool.chooseChanel(channels)
		try:
			solution = os.path.join(solution + theChannel, 'Insights')
		except Exception as e:
			Tool.error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
			return
	else:
		try:
			solution = os.path.join(Tool.getSolution(Tool.getPath('solution')), 'Insights')
		except Exception as e:
			Tool.error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
			return
	# print(argv[0])
	insights = Tool.getCol(argv[0], 'Insight')
	ucs = Tool.getCol(argv[0], 'UC')
	# print(insights)
	# print(ucs)

	activated = Tool.getCol(argv[0], 'Activated')
	tmpInsights = list()
	tmpUcs = list()
	for i in range(len(insights)):
		if activated[i] == 'V':
			tmpInsights.append(insights[i])
			tmpUcs.append(ucs[i])
	insights = tmpInsights
	ucs = tmpUcs
	insights = set(insights)
	createInsightDirectory(solution, insights, client)
	createUcDirectory(solution, ucs, client)
	ucsDictionary = ucsDict(list(insights), ucs)
	for insight in insights:
		overwriteInsight(solution, corePath, insight, ucsDictionary, client)
	if client != '' and askyesno('Confirmation', 'Would you like to remove the clinet layer?'):
		removeLayer(solution, client)
		removeFacts(solution)
	Tool.endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

#   0 - file with the list of insights to enable by use cases
