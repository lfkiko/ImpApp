import os
import webbrowser
import zipfile
from logging import error

import PySimpleGUI as Sg

import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from kivy.app import App

from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson

fileManger = 'Scripts/Source/fileManger.json'

searchedCoreFolders = ['product-act-biz-unit.zip', 'product-budgets-biz-unit.zip',
					   'product-data-and-assets-biz-unit.zip', 'product-debt-biz-unit.zip',
					   'product-engage-biz-unit.zip', 'product-goals-biz-unit.zip', 'product-mt-biz-unit.zip']


def createDirectory(solutionsPath, path):
	directories = path.split(os.sep)
	for p in directories:
		try:
			os.mkdir(solutionsPath + os.sep + p)
		except Exception as e:
			error(e.__str__())
			pass
		solutionsPath = solutionsPath + os.sep + p


def fixPath(path):
	return path.replace('\\', '/')


def valPath(path):
	if 'perso-core' in path:
		return True
	elif 'bank-biz' in path:
		# Factory.ERROR1().open()
		return False
	elif path == readJson(getFile('settings'))['pathRoot']:
		# Factory.ERROR2().open()
		return False
	else:
		return True


def rewriteText(filePath, new_text, path_filter):
	data = readJson(filePath)
	data[path_filter] = new_text
	updateJson(filePath, data)


def currentPath(self, filterX, path):
	if filterX == 'c':
		self.ids.corePath.text = path
	elif filterX == 's':
		self.ids.solutionPath.text = path


def verifyPath(self, filterX, path):
	fixedPath = os.path.normpath(path)
	if filterX == 'c':
		self.ids.corePath.text = fixedPath
	elif filterX == 's':
		if valPath(fixedPath):
			self.ids.solutionPath.text = fixedPath


def openKB():
	webbrowser.open('https://track.personetics.com/youtrack/articles/S-A-306/Solution-Imp--')


def getFile(filePath):
	file = readJson(fileManger)
	return file[filePath]


def findDir(path, direction):
	path_back = str()
	dirs = direction.split('/')
	for i in dirs:
		path_back = os.path.join(path, i)
		if os.path.exists(path_back):
			pass
		else:
			os.mkdir(path_back)
	return path_back


def createPath(path, extra):
	newPath = path
	addOns = extra.rsplit('\\')
	for x in addOns:
		newPath = os.path.join(newPath, x)
	return newPath


def getSolution(path, checkTime: bool = False):
	solutionsPath = path
	dirs = ['biz-units', 'perso-biz', 'Projects']
	for d in dirs:
		if d in os.listdir(solutionsPath):
			solutionsPath = os.path.join(solutionsPath, d)
	if checkTime:
		return solutionsPath
	for x in os.listdir(solutionsPath):
		checkPath = os.path.join(solutionsPath, x)
		if os.path.isdir(checkPath) and '$' in x:
			return os.path.join(solutionsPath, x[:x.index('$')])
	return path


def getPath(pathName):
	if pathName == 'corePath':
		return readJson(getFile('settings'))['corePath']
	elif pathName == 'modelPath':
		return readJson(getFile('settings'))['modelPath']
	elif pathName == 'intelliJ':
		return readJson(getFile('settings'))['intelliJRoot']
	elif pathName == 'EBPath':
		return readJson(getFile('settings'))['EBPath']
	elif pathName == 'solution':
		return App.get_running_app().root.ids.Menu_Window.ids.solutionPath.text
	elif pathName == 'DataLoad':
		return os.path.join(getPath('solution'), 'package', 'target', 'DataLoad')


def modelVersion(projectPath):
	if 'pom.xml' in os.listdir(projectPath):
		with open(os.path.join(projectPath, 'pom.xml'), 'r') as f:
			pom = f.read()
			data = str(BeautifulSoup(pom, 'xml').find('version'))
			version = data[(data.find('>')) + 1: data.find('<', 1)].split('.')
			if int(version[0]) >= 5 and int(version[1]) > 5:
				return True

			return False


def filesInZip(path, zippedDir, pathTo):
	zippedPath = os.path.join(path, zippedDir)
	files = []
	with zipfile.ZipFile(zippedPath) as z:
		for names in z.namelist():
			if pathTo in names and pathTo != names:
				files.append(names)
	return files


def getChannels(solution, getLive: bool = False):
	path = os.path.dirname(solution)
	channels = []
	for x in os.listdir(path):
		if os.path.isdir(os.path.join(path, x)) and x != "Configuration":
			channels.append(x)
	if getLive:
		for x in channels:
			if x.find("$LIVE") > 0:
				return x.replace("$", "_")
	return channels


def chooseChanel(channels):
	listLayout = [[Sg.Text('Select one->'), Sg.Listbox(channels, size=(30, 10), key='LB')], [Sg.Button('Ok')]]
	event, values = Sg.Window('Choose an option', listLayout).read(close=True)
	channel = values["LB"][0]
	if '$' in channel:
		channel = channel[channel.index('$'):]
	else:
		channel = ""

	return channel

def chooseClient():
	listLayout = [[Sg.Text('Select one->'), Sg.Listbox(['V1','V2','V3'], size=(30, 10), key='LB')], [Sg.Button('Ok')]]
	event, values = Sg.Window('Choose an option', listLayout).read(close=True)
	client = values["LB"][0]

	return client


def searchInsightInCore(corePath, insightName):
	zips = os.listdir(corePath)
	if 'perso-biz.zip' in zips:
		zips.remove('perso-biz.zip')
	zipToRemove = list()
	for dirZip in zips:
		if 'bank' in dirZip or 'docs' in dirZip:
			zipToRemove.append(dirZip)
	for badZip in zipToRemove:
		zips.remove(badZip)
	for zipDir in zips:
		insightsInPath = filesInZip(corePath, zipDir, 'Core/Insights/' + insightName)
		if len(insightsInPath) != 0:
			if '-docs' in zipDir:
				zipDir = zipDir[0:zipDir.rindex('-')] + zipDir[zipDir.rindex('.'):]
			return zipDir
	return FileNotFoundError


def getStarterVersion(solutionPath):
	pomPath = os.path.join(solutionPath, "pom.xml")
	ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
	ns = '{http://maven.apache.org/POM/4.0.0}'
	pom = ET.parse(pomPath)
	root = pom.getroot()
	tags = ['parent', 'version']
	for tag in tags:
		root = root.find(f'{ns}{tag}')
	version = '.'.join(root.text.split('.')[:2])
	return version
