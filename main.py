import datetime
import os
import tkinter as tk
from tkinter import filedialog
from kaki.app import App
from kivy.app import App as KvApp
from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory

from Scripts import newFactField
from Scripts.addingUsers import demoData
from Scripts.categoryGroups import categoryGroups
from Scripts.enableInsights import enable_insights, transfer, sEditorVisible
from Scripts.newFactField import fact_update
from Scripts.newProject import newProject
from Scripts.thFactor import thFactor
from Scripts.toolBoox.toolBoox import rewriteText, verifyPath, openKB, getFile, currentPath, valPath, readJson

Builder.load_file('Scripts/Source/alerts.kv')
root = tk.Tk()
root.withdraw()
root.destroy()


class MenuWindow(Screen):
    # Builder.load_file('main.kv')
    Window.minimum_width, Window.minimum_height = (860, 660)
    solutionPath = ObjectProperty(None)
    
    def openFile(self, name):
        os.startfile(os.path.normpath(getFile(name + "_raw")), 'edit')
    
    def selected(self, name, filterX):
        verifyPath(name, filterX,
                   filedialog.askdirectory(initialdir=os.path.normpath(SettingsWindow().currentDefaultPath)))
    
    def refreshPath(self, name, filterX, path):
        currentPath(name, filterX, path)
    
    def openKB(self, root):
        openKB(root.name)
    
    pass


class enableInsightsWindow(Screen):
    Builder.load_file('Scripts/enableInsights/enableInsights.kv')
    corePath = ObjectProperty(None)
    solutionPath = ObjectProperty(None)
    
    def runFunc(self, corePath, solutionPath):
        if valPath(corePath) and valPath(solutionPath):
            transfer.main([self.name, 'active'])
            status = enable_insights.main([corePath, solutionPath, getFile(self.name)])
            self.ids.corePath.text = status
    
    pass


class categoryGroupsWindow(Screen):
    Builder.load_file('Scripts/categoryGroups/categoryGroups.kv')
    solutionPath = ObjectProperty(None)
    
    def checkBoxClick(self, instance):
        self.ids.checkBoxs.text = instance
    
    def runFunc(self):
        canRun = False
        num_of_lang = self.ids.langNum.text
        languages = [
            self.ids.language1.text, self.ids.language2.text, self.ids.language3.text, self.ids.language4.text
        ]
        if self.ids.checkBoxs.text != "" and languages.count("") != 4:
            canRun = True
        
        if canRun:
            categoryGroups.main(
                [self.ids.solutionPath.text, getFile(self.name + "_raw"), num_of_lang, languages,
                 self.ids.checkBoxs.text]
            )
        else:
            print("Please fill up relevant values")
    
    pass


class newFieldToFactWindow(Screen):
    Builder.load_file('Scripts/newFactField/new_fact_field.kv')
    solutionPath = ObjectProperty(None)
    
    def runFunc(self):
        newFactField.fact_update.main(
            [self.ids.solutionPath.text, self.fact.text, self.field.text, self.type.text, self.description.text])
    
    pass


class batchesWindow(Screen):
    Builder.load_file('Scripts/batches/batches.kv')
    corePath = ObjectProperty(None)
    solutionPath = ObjectProperty(None)
    checkBoxs = ObjectProperty(None)
    
    def checkBoxClick(self, batch):
        self.ids.checkBoxs.text = batch
    
    def update(self, me, check):
        if ImplementationApp.batch_use == 'data-assets':
            me.ids.batchId.text = 'data-assets'
            me.ids.batchId.hint_text = 'data-assets'
            print(me.ids.batchId.text)
    
    pass


class demoDataWindow(Screen):
    Builder.load_file('Scripts/addingUsers/demoData.kv')
    corePath = ObjectProperty(None)
    solutionPath = ObjectProperty(None)
    
    def runFunc(self):
        bUsers = self.ids.BUsers.active
        modified = self.ids.modified.active
        properties = {"LocalCurrency": self.ids.LocalCurrency.text, "ForeignCurrency": self.ids.ForeignCurrency.text,
                      "CountryName": self.ids.CountryName.text, "CountryCode": self.ids.CountryCode.text}
        
        demoData.main([self.ids.corePath.text, self.ids.solutionPath.text, properties, bUsers, modified,
                       getFile(self.name + "_raw")])
    
    pass


class batchesPropertiesWindow(Screen):
    Builder.load_file('Scripts/batches/batchesProperties.kv')
    batchId = ObjectProperty(None)
    disabled = BooleanProperty(False)
    
    def methods_update(self, value):
        print(self)
        if value == "autoRegister":
            self.ids.API.disabled = False
            self.ids.Context.disabled = False
        else:
            self.ids.API.disabled = True
            self.ids.Context.disabled = True
        
        pass
    
    def autoFill(self):
        data = readJson(getFile(self.name))
        print(batchesWindow.ids.checkBoxs.text)
    
    def runFunc(self):
        print(ImplementationApp.batch_use)
    
    pass


class dataLibraryWindow(Screen):
    Builder.load_file('Scripts/dataLibrary/dataLibrary.kv')
    solutionPath = ObjectProperty(None)
    
    pass


class sEditorVisibleWindow(Screen):
    Builder.load_file('Scripts/enableInsights/sEditorVisible.kv')
    solutionPath = ObjectProperty(None)
    
    def runFunc(self, path):
        if valPath(path):
            status = sEditorVisible.main([path, self.name])
            print(status)
    
    pass


class breakingChangeWindow(Screen):
    Builder.load_file('Scripts/breakingChange/breakingChange.kv')
    
    # def runFunc(self, path):
    #     if valPath(path):
    #         status = sEditorVisible.main([path, self.name])
    #         print(status)
    
    pass


class newProjectWindow(Screen):
    Builder.load_file('Scripts/newProject/newProject.kv')
    solutionPath = ObjectProperty(None)
    
    def checkBoxClick(self, check):
        pass
    
    def runFunc(self):
        path = self.ids.solutionPath.text
        if valPath(path):
            newProject.main([path, self.ids.channel.text, self.ids.projectDir.text])
    
    pass


class PostManWindow(Screen):
    Builder.load_file('Scripts/postMan/postMan.kv')
    solutionPath = ObjectProperty(None)
    
    def checkBoxDate(self, date):
        if date in ('01/03/2017', '12/22/2016'):
            self.ids.checkBoxs.text = date
        else:
            self.ids.date.disabled = False
    
    def submit(self, date):
        self.ids.checkBoxs.text = date
    
    def checkDate(self, date):
        dateFormat = '%m/%d/%Y'
        try:
            datetime.datetime.strptime(date, dateFormat)
        except ValueError:
            print("Incorrect data format, should be MM-DD-YYYY")


class RequestsWindow(Screen):
    Builder.load_file('Scripts/postMan/requests.kv')
    
    def runFunc(self, api):
        path = PostManWindow.solutionPath.text
        print(path)
        # print(api)
    
    pass


class ThFactorWindow(Screen):
    Builder.load_file('Scripts/thFactor/thFactor.kv')
    solutionPath = ObjectProperty(None)
    
    def runFunc(self):
        path = self.ids.solutionPath.text
        factor = float(self.ids.factor.text)
        thFactor.main([path, factor])
    
    pass


class SettingsWindow(Screen):
    currentDefaultPath = readJson(getFile('settings'))['pathRoot']
    currentIntelliJPath = readJson(getFile('settings'))['intelliJRoot']
    currentCorePath = readJson(getFile('settings'))['corePath']
    
    def dpath(self, path, path_filter):
        rewriteText(getFile(self.name), path, path_filter)
    
    pass


class WindowManger(ScreenManager):
    Window.size = (1000, 800)
    Window.minimum_height, Window.minimum_width = (660,860)
    
    pass


class ImplementationApp(App, KvApp):
    # KV_FILES = [
    #     os.path.join(os.getcwd(), 'main.kv'),
    #     "Scripts/enableInsights/enableInsights.kv",
    #     'Scripts/categoryGroups/categoryGroups.kv',
    #     'Scripts/newFactField/new_fact_field.kv',
    #     'Scripts/batches/batches.kv',
    #     'Scripts/addingUsers/demoData.kv',
    #     'Scripts/batches/batchesProperties.kv',
    #     'Scripts/dataLibrary/dataLibrary.kv',
    #     'Scripts/enableInsights/sEditorVisible.kv',
    #     'Scripts/breakingChange/breakingChange.kv',
    # ]
    # CLASSES = {
    #     "WindowManger": "main",
    #     "MenuWindow": "main",
    #     "enableInsightsWindow": "main",
    #     "categoryGroupsWindow": "main",
    #     "newFieldToFactWindow": "main",
    #     "batchesWindow": "main",
    #     "demoDataWindow": "main",
    #     "batchesPropertiesWindow": "main",
    #     "dataLibraryWindow": "main",
    #     "sEditorVisibleWindow": "main",
    #     "breakingChangeWindow": "main",
    #     "newProjectWindow": "main",
    #     "PostManWindow": "main",
    #     "RequestsWindow": "main",
    #     "ThFactorWindow": "main",
    #     "SettingsWindow": "main"
    # }
    # AUTORELOADER_PATHS = [
    #     (".", {"recursive": True})
    # ]
    #
    # def build_app(self, first=False):
    #     return Factory.WindowManger()
    def build(self):
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    ImplementationApp().run()
