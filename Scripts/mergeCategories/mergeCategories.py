from Scripts.toolBoox import *
import os
import sys
import warnings


def mergedCategories(mergingFile):
	oldCg = getCol(mergingFile, 'CG')
	mergedTo = getCol(mergingFile, 'MergedTo')
	mergedJ = dict()
	for x in range(len(oldCg)):
		mergedJ[oldCg[x]] = mergedTo[x]
	return mergedJ


def getIndex(cols):
	categoryNames = ['category', 'budgetCategoryKey', ]
	for name in categoryNames:
		if name in categoryNames:
			return cols.index(name)
	return -1


def updateFacts(insightsPath, mergedTo):
	startLog()
	insightsList = os.listdir(insightsPath)
	if 'SEntities' in insightsList:
		insightsList.remove('SEntities')
	for insight in insightsList:
		insightPath = os.path.join(insightsPath, insight)
		ucList = os.listdir(insightPath)
		noUcs = True
		for uc in ucList:
			ucPath = os.path.join(insightPath, uc)
			if os.path.isdir(ucPath):
				try:
					jInsightFacts = os.path.join(ucPath, 'JInsightFacts.json')
					facts = readJsonMultilingual(jInsightFacts)
					noUcs = False
				except Exception as e:
					error(e.__str__())
					continue

				for fact in facts.keys():
					if fact == 'categoryGroup' or fact == 'categories':
						rowsToReturn = []
						ind = 0
						for row in fact['rows']:
							if row[ind] not in mergedTo.keys():
								rowsToReturn.append(row)
						facts[fact] = rowsToReturn
					elif fact != 'storyId':
						ind = getIndex(fact['cols'])
						if ind >= 0:
							for row in fact['rows']:
								if fact['rows'][row][ind] in mergedTo.keys():
									fact['rows'][row][ind] = mergedTo[fact['rows'][row][ind]]
				try:
					updateJsonMultiLangUtf8Sig(jInsightFacts, facts)
				except Exception as e:
					error(e.__str__())
					continue
			if noUcs:
				info("There are no JInsightFacts.json files in " + insight)

	endLog()


def updateUsersCategories(demoDataPath, mergedTo):
	startLog()
	users = os.listdir(demoDataPath)

	def updateCategoryGroupId(currentCategory):
		if currentCategory in mergedTo.keys():
			return mergedTo[currentCategory]
		else:
			return currentCategory

	def updateColumn(dTransactions, func):
		col = readCsv(dTransactions)
		col['categoryGroupId'] = col['categoryGroupId'].apply(func)
		writeCsv(dTransactions, col)

	for user in users:
		try:
			dTransactionsPath = os.path.join(demoDataPath, user, 'DTransaction.csv')
			os.path.exists(dTransactionsPath)
		except:
			warnings(user + ' DTransaction.csv do not exists')
			continue
		finally:
			try:
				updateColumn(dTransactionsPath, updateCategoryGroupId)
			except Exception as e:
				error(e.__str__())
	endLog()


def main(argv):
	startLog()
	try:
		solution = getSolution(getPath('solution'))
		try:
			os.path.exists(solution)
		except:
			os.mkdir(solution)
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	mergedTo = mergedCategories(argv[0])
	if argv[1]:
		try:
			demoData = getSolution(getPath('solution'))
			demoData = demoData + '$QA'
			demoData = os.path.join(demoData, 'DemoData')
		except:
			error('Demodata don\'t exsists')
			return
		print(demoData)  # updateUsersCategories(demoData, mergedTo)

	if argv[2]:
		try:
			insights = os.path.join(getSolution(getPath('solution')), 'Insights')
		except:
			error('Insights don\'t exsists')
			return
		updateFacts(insights, mergedTo)
	endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

# 0 - excel file
