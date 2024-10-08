import os
import sys
import zipfile
import Scripts.toolBoox as Tool
from logging import info, warning, error

from Scripts.addingUsers import categoriesAdaptation

def findRelevantUsers(corePath, extraUsers, bUsers, modified):
	relevantUser = []
	coreUsers = Tool.filesInZip(corePath, 'product-data-and-assets-biz-unit.zip', 'Core/DemoData')
	if bUsers:
		for d in coreUsers:
			user = os.path.normpath(d).replace('Core' + os.sep + 'DemoData' + os.sep, '').split(os.sep)[0]
			if user.startswith("B_") and user.split("_")[1].isnumeric():
				if user not in relevantUser:
					relevantUser.append(user)
	if modified:
		for x in extraUsers:
			relevantUser.append(x)
	return relevantUser


def copyUsers(relevantUser, corePath, solutionQaPath):
	errors = False
	solutionDemoData = Tool.createPath(solutionQaPath, 'DemoData')
	coreDemoDataPath = os.path.join(corePath, 'product-data-and-assets-biz-unit.zip')
	try:
		os.mkdir(solutionDemoData)
	except:
		warning('all ready exist: ' + solutionDemoData)
		errors = True
	finally:
		for user in relevantUser:
			trgPath = os.path.join(solutionDemoData, user)
			try:
				os.mkdir(trgPath)
			except:
				warning("User: " + user + " is all ready exists in the solution level from ")
			finally:
				with zipfile.ZipFile(coreDemoDataPath) as z:
					srcFiles = Tool.filesInZip(corePath, 'product-data-and-assets-biz-unit.zip', 'Core/DemoData/' + user + '/')
					for file in srcFiles:
						try:
							with z.open(file) as f:
								tf = open(os.path.join(trgPath, file.split('/')[-1]), 'w')
								tf.write(f.read().decode(encoding='utf-8-sig'))
						except:
							errors = True
							error("Something went wrong while copping: " + file + ' to ' + user)
					if not srcFiles:
						errors = True
						warning("User: " + user + " do not exists in the core ")
						# os.rmdir(trgPath)
						pass

	if errors:
		warning("Copying users finished with warnings")
	else:
		info("Copying users finished")
	return errors


def modifyUser(usersPath, user, localCurrency, foreignCurrency, countryName, countryCode, factor):
	def updateCurrency(currentCurrency):
		if currentCurrency == "USD":
			return localCurrency
		elif currentCurrency == "EUR":
			return foreignCurrency
		else:
			return currentCurrency

	def updateCountryCode(currentCountry):
		if currentCountry != countryCode:
			return countryCode
		else:
			return currentCountry

	def updateCountryName(currentCountry):
		if currentCountry != countryName:
			return countryName
		else:
			return currentCountry

	def updateFactor(currentValue):
		if factor != 1 and currentValue != '':
			try:
				newVal = float(currentValue.replace(",", ""))
				newVal = newVal * float(factor)
				return str(round(newVal, 2))
			except:
				print(currentValue)
				error('Can\'t convert to float in :' + usersPath)

		return currentValue

	def updateColumn(column, file, func):
		try:
			df = Tool.readCsv(os.path.join(usersPath, file))
		except:
			warning('col ' + column + ' don\'t exists in - ' + os.path.join(usersPath, file))
			return

		df[column] = df[column].apply(func)
		Tool.writeCsv(os.path.join(usersPath, file), df)

	for thisFile in os.listdir(usersPath):
		try:
			csvFile = Tool.readCsv(os.path.join(usersPath, thisFile))
		except:
			error('Problem opening ' + thisFile + ' for ' + user)
			continue

		for col in ['currencyCd', 'currencyCdOriginal', 'countryCd', 'countryName', 'availableBalance',
					'availableCredit', 'availableCreditCash', 'amount', 'amountChargeCurrency', 'amountLocalCurrency',
					'amountOriginal', 'amountOriginalCurrency', 'currencyAmount']:
			if col in csvFile:
				if 'currency' in col and 'currencyAmount' != col:
					updateColumn(col, thisFile, updateCurrency)
				else:
					if 'Cd' in col:
						updateColumn(col, thisFile, updateCountryCode)
					elif 'Name' in col:
						updateColumn(col, thisFile, updateCountryName)
					elif factor != 1:
						updateColumn(col, thisFile, updateFactor)


def modifyUsersInSolution(solutionDemoDataPath, input_json, relevantUser):
	for user in relevantUser:
		if user in os.listdir(solutionDemoDataPath):
			modifyUser(os.path.join(solutionDemoDataPath, user), user, input_json['LocalCurrency'], input_json['ForeignCurrency'], input_json['CountryName'], input_json['CountryCode'], input_json['Factor'])
		else:
			warning("User: " + user + " do not exists in the core ")


def main(argv):
	Tool.startLog()
	try:
		solution = Tool.getSolution(Tool.getPath('solution')) + '$QA'
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return
	try:
		corePath = Tool.createPath(Tool.getPath('solution'), 'package\\target\\DataLoad')
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return
	extraUsers = Tool.getCol(argv[3], 'USERS')
	relevantUser = findRelevantUsers(corePath, extraUsers, argv[1], argv[2])
	err: bool = copyUsers(relevantUser, corePath, solution)
	modifyUsersInSolution(os.path.join(solution, 'DemoData'), argv[0], relevantUser)
	categoriesAdaptation.main([solution])
	Tool.endLog(err)


if __name__ == "__main__":
	main(sys.argv[1:])

# 0 properties dictionary
# 1 B_users checkBox bool
# 2 modified checkBox bool
# 3 file name
# os.listdir(product + "\\DemoData")
