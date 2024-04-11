import os.path
import sys
from Scripts.toolBoox import *
import zipfile


def createAmounts(formats, amountFormat, languages):
	ids = ['Sum', 'Avg']
	for k in ['Balance', 'OneTx', 'OneTxAbs', 'Sum', 'SumAbs', 'Avg', 'AvgAbs']:
		formats[k] = dict()
	for i in languages:
		tmp = amountFormat[languages.index(i) + 1].replace("\'", "")
		formats['Balance'][i] = tmp
		formats['OneTx'][i] = tmp
		if tmp.find('-') >= 0:
			formats['OneTxAbs'][i] = tmp.replace('-', '+')
		else:
			if tmp.index("#") == 0:
				formats['OneTxAbs'][i] = "+" + tmp
			formats['OneTxAbs'][i] = tmp[:tmp.index('#')] + '+' + tmp[tmp.index('#'):]

		otherTmp = tmp.replace("0", "")
		otherTmp = otherTmp.replace(otherTmp[otherTmp.rindex("#") + 1], "")
		tmpAbs = formats['OneTxAbs'][i].replace("0", "")
		tmpAbs = tmpAbs.replace(tmpAbs[tmpAbs.rindex("#") + 1], "")
		if otherTmp.index('@') + 1 < len(otherTmp):
			if otherTmp[otherTmp.index('@') + 1] == " ":
				sign = 2
			else:
				sign = 1

		else:
			if otherTmp[otherTmp.index('@') - 1] == " ":
				sign = -2
			else:
				sign = -1
		for d in ids:
			plus = d + 'Abs'
			plusTmp = formats['OneTxAbs'][i][:formats['OneTxAbs'][i].rfind("#") + 1]
			dTmp = formats['OneTx'][i][:formats['OneTx'][i].rfind("#") + 1]
			if sign < 0:
				plusTmp = plusTmp + formats['OneTxAbs'][i][formats['OneTxAbs'][i].rfind("#") + 4:]
				dTmp = dTmp + formats['OneTx'][i][formats['OneTx'][i].rfind("#") + 4:]

			formats[plus][i] = plusTmp
			formats[d][i] = dTmp

	return formats


def copyJson(corePath, solution, fileName):
	try:
		zipDir = searchInsightInCore(corePath, 'SEntities')

		insightCorePath = os.path.join(corePath, zipDir)
		if zipDir == FileNotFoundError:
			return
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	finally:
		with zipfile.ZipFile(insightCorePath) as z:
			srcFiles = filesInZip(corePath, zipDir, 'Core/Insights/')
			for file in srcFiles:
				if file.split('/')[-1] == fileName:
					try:
						with z.open(file) as j:
							formats = jsonifyZip(j.read())
							if os.path.exists(os.path.join(solution, fileName)):
								updateJson(os.path.join(solution, fileName), formats)
							else:
								writeJson(os.path.join(solution, fileName), formats)

					except Exception as e:
						error(e.__str__())
	return


def updateFormats(solution, formats, mainJson, fileName):
	for i in range(len(mainJson['formats'])):
		if mainJson['formats'][i]['id'] in formats.keys() or mainJson['formats'][i]['name'] in formats.keys():
			mainJson['formats'][i]['formats'] = formats[mainJson['formats'][i]['id']]
	try:
		updateJson(os.path.join(solution, fileName), mainJson)
	except Exception as e:
		error(e.__str__())


def main(argv):
	startLog()
	fileName = 'SExpressionsFormats.json'
	try:
		solution = os.path.join(getSolution(getPath('solution')), 'Insights', 'SEntities')
	except:
		error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
		return
	try:
		corePath = createPath(getPath('solution'), 'package\\target\\DataLoad')
	except Exception as e:
		error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
		return

	languages = getRow(argv[0], 0)
	ids = getCol(argv[0], languages[0])
	languages = languages[1:]
	formats = dict()
	prettyPrintJson(formats)
	ids[ids.index("Month long")] = "Month"
	ids[ids.index("Month short")] = "ShortMonth"
	for i in range(len(ids) - 1):
		data = getRow(argv[0], i + 1)
		key = ids[i].replace(" ", "")
		formats[key] = dict()
		for n in range(len(languages)):
			formats[key][languages[n]] = data[n + 1]
	prettyPrintJson(formats)
	prettyPrintJson(formats)
	formats = createAmounts(formats, getRow(argv[0], len(ids)), languages)
	if not os.path.exists(os.path.join(solution, 'fileName')):
		copyJson(corePath, solution, fileName)
	mainJson = readJson(os.path.join(solution, fileName))
	prettyPrintJson(formats)
	updateFormats(solution, formats, mainJson, fileName)

	endLog()

	if __name__ == "__main__":
		main(sys.argv[1:])

# 0 - excel file
