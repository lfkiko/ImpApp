from logging import warning

from Scripts.toolBoox import *
import os
import sys
import zipfile


def cleanSInsight(ucsList, SInsightPath):
	try:
		SInsightData = readJson(SInsightPath)
	except Exception as e:
		print(SInsightPath)
		error(e.__str__())
		return
	if 'dependencies' in SInsightData.keys():
		SInsightData.pop('dependencies')

	keysToRemove = list(SInsightData['insightMetadata'].keys())
	for key in ['activated', 'name', 'description']:
		keysToRemove.remove(key)

	for key in keysToRemove:
		SInsightData['insightMetadata'].pop(key)

	SInsightData['insightMetadata']['activated'] = 'TRUE'
	ucs = len(SInsightData['useCases'])
	toRemove = []
	for uc in range(ucs):
		if SInsightData['useCases'][uc]['id'] in ucsList:
			SInsightData['useCases'][uc]['activated'] = 'TRUE'
		else:
			toRemove.append(uc)
	if len(toRemove) == 0:
		for i in reversed(toRemove):
			SInsightData['useCases'].remove(i)
	updateJson(SInsightPath, SInsightData)


def createInsightDirectory(solutionPath, insights):
	for i in insights:
		try:
			os.mkdir(os.path.join(solutionPath, i))
		except Exception as e:
			if 'already exists' in e.__str__():
				warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


def createUcDirectory(solutionPath, ucs):
	for u in ucs:
		try:
			insight = u[0: u.rindex('_')]
		except Exception as e:
			error(e + "for " + u)

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


def overwriteInsight(solution, corePath, insight, allUcs):
	insightCorePath = ""
	try:
		insightZipDir = searchInsightInCore(corePath, insight)
		insightCorePath = os.path.join(corePath, insightZipDir)
		if insightZipDir == FileNotFoundError:
			return
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	finally:
		insightPath = os.path.join(solution, insight)
		if insightCorePath == "":
			return
		with zipfile.ZipFile(insightCorePath) as z:
			srcFiles = filesInZip(corePath, insightZipDir, 'Core/Insights/' + insight + '/')
			for file in srcFiles:
				if file.split('/')[-1] == 'SInsight.json':
					try:
						with z.open(file) as j:
							sInsight = jsonifyZip(j.read())
							if os.path.exists(os.path.join(insightPath, 'SInsight.json')):
								updateJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
							else:
								writeJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
					except Exception as e:
						error(e.__str__())
					cleanSInsight(allUcs[insight], os.path.join(insightPath, 'SInsight.json'))
				if file.split('/')[-2] in allUcs[insight] and file.split('/')[-1] != '':
					tempInsightPath = os.path.join(insightPath, file.split('/')[-2], file.split('/')[-1])
					try:
						with z.open(file) as ucj:
							jsonFile = jsonifyZip(ucj.read())
							if os.path.exists(tempInsightPath):
								updateJsonMultiLang(tempInsightPath, jsonFile)
							else:
								writeJsonMultiLang(tempInsightPath, jsonFile)
					except Exception as e:
						print('here - ' + file.split('/')[-2] + '/' + file.split('/')[-1])
						error(e.__str__())


def main(argv):
	startLog()
	try:
		solution = getSolution(getPath('solution'))
	except:
		error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
		return
	try:
		corePath = createPath(getPath('solution'), 'package\\target\\DataLoad')
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return
	channels = getChannels(solution)
	if len(channels) > 3:
		theChannel = chooseChanel(channels)
		try:
			solution = os.path.join(solution + theChannel, 'Insights')
		except Exception as e:
			error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
			return
	else:
		try:
			solution = os.path.join(getSolution(getPath('solution')), 'Insights')
		except Exception as e:
			error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
			return
	# print(argv[0])
	insights = getCol(argv[0], 'Insight')
	ucs = getCol(argv[0], 'UC')
	print(insights)
	print(ucs)

	activated = getCol(argv[0], 'Activated')
	tmpInsights = list()
	tmpUcs = list()
	for i in range(len(insights)):
		if activated[i] == 'V':
			tmpInsights.append(insights[i])
			tmpUcs.append(ucs[i])
	insights = tmpInsights
	ucs = tmpUcs
	insights = set(insights)
	createInsightDirectory(solution, insights)
	createUcDirectory(solution, ucs)
	ucsDictionary = ucsDict(list(insights), ucs)
	for insight in insights:
		overwriteInsight(solution, corePath, insight, ucsDictionary)
	endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

#   0 - file with the list of insights to enable by use cases
