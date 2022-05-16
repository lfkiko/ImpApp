import os
import win32timezone

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from Scripts import newFactField
from Scripts.categoryGroups import categoryGroups
from Scripts.enableInsights import enable_insights, transfer, sEditorVisible
from Scripts.newFactField import fact_update
from Scripts.newProject import newProject
from Scripts.toolBoox.toolBoox import rewriteText, verifyPath, openKB, getFile, currentPath, valPath, readJson

MST = win32timezone.TimeZoneInfo('Mountain Standard Time')

Builder.load_file('Scripts/Source/alerts.kv')


class MenuWindow(Screen):
    
    def openFile(self, name):
        os.startfile(os.path.normpath(getFile(name + "_raw")), 'edit')
    
    def selected(self, name, filterX, path):
        verifyPath(name, filterX, path)
    
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
    
    def runFunc(self):
        num_of_lang = self.ids.langNum.text
        languages = [
            self.ids.language1.text, self.ids.language2.text, self.ids.language3.text, self.ids.language4.text
        ]
        categoryGroups.main([self.ids.solutionPath.text, getFile(self.name + "_raw"), num_of_lang, languages])
    
    pass


class newFieldToFactWindow(Screen):
    Builder.load_file('Scripts/newFactField/new_fact_field.kv')
    solutionPath = ObjectProperty(None)
    
    def runFunc(self, path):
        newFactField.fact_update.main([path, self.fact.text, self.field.text, self.type.text, self.description.text])
    
    pass


class batchesWindow(Screen):
    Builder.load_file('Scripts/batches/batches.kv')
    corePath = ObjectProperty(None)
    solutionPath = ObjectProperty(None)
    
    def checkBoxClick(self, batch):
        ImplementationApp.batch_use = batch
    
    def update(self, me):
        if ImplementationApp.batch_use == 'data-assets':
            me.ids.batchId.text = 'data-assets'
            me.ids.batchId.hint_text = 'data-assets'
            print(me.ids.batchId.text)
    
    pass


class batchesDataWindow(Screen):
    Builder.load_file('Scripts/batches/batches.kv')
    batchId = ObjectProperty(None)
    disabled = BooleanProperty(False)
    
    def methods_update(self, value):
        if value == "autoRegister":
            self.ids.API.disabled = False
            self.ids.Context.disabled = False
        else:
            self.ids.API.disabled = True
            self.ids.Context.disabled = True
        
        pass
    
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


class newProjectWindow(Screen):
    Builder.load_file('Scripts/newProject/newProject.kv')
    solutionPath = ObjectProperty(None)
    
    def checkBoxClick(self, check):
        pass
    
    def runFunc(self, path):
        if valPath(path):
            newProject.main([path, self.ids.channel.text, self.ids.projectDir.text])
    
    pass


class SettingsWindow(Screen):
    currentDefaultPath = readJson(getFile('settings'))['pathRoot']
    currentIntelliJPath = readJson(getFile('settings'))['intelliJRoot']
    def restart
    
    def dpath(self, path, path_filter):
        if path_filter == 'm':
            self.ids.defaultPath.text = path
            rewriteText(getFile(self.name), path, path_filter)
        elif path_filter == 'j':
            rewriteText(getFile(self.name), path, path_filter)
            pass


class WindowManger(ScreenManager):
    Window.size = 1000, 800
    Window.minimum_height = 660
    Window.minimum_width = 860
    
    pass


class ImplementationApp(App):
    batch_use = str()
    
    def build(self):
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    ImplementationApp().run()
