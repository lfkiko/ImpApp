# editing workspace.xml to match Directorie's name must rerun IntelliJ after update
# adding to the project modified properties with the Channels name
import os
import sys
from logging import info, error
from shutil import copyfile
import xml.dom.minidom

from Scripts.toolBoox.toolBoox import getFile, readJson, createPath, getPath, getSolution


def findProfile(path):
    current_path = path
    dir_list = os.listdir(path)
    while True:
        if 'profiles' in dir_list:
            break
        else:
            # print('profiles' in os.listdir(current_path))
            # print(current_path)
            current_path = os.path.normpath(current_path + os.sep + os.pardir)
            dir_list = os.listdir(current_path)
    
    return current_path


def editProperties(file_name, channel):
    with open(file_name, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for line in d:
            if line != '\n' and '=' in line:
                p, v = line.split('=')
                if p in ['KB_RELOAD_PROJECTS', 'KB_RELOAD_CHANNELS', 'BACKGROUND_TASK_CHANNEL']:
                    v = channel
                    tmp_line = p + '=' + v + '\n'
                    f.write(tmp_line)
                else:
                    f.write(line)
            else:
                f.write(line)
        f.truncate()


def checkForProperties(dirPath):
    path = createPath(dirPath, 'profiles\\local')
    if 'personetics.properties' in os.listdir(path):
        return True
    
    else:
        properties = getFile('projectProperties')
        file_name = os.path.basename(properties)
        copyfile(properties, os.path.join(path, file_name))
        path = os.path.join(dirPath, path, 'personetics.properties')
        return True


def updateConfigurations(project_dir_name, intelliJ_path):
    conf = xml.dom.minidom.parse(intelliJ_path)
    component = conf.getElementsByTagName('configuration')
    
    for x in component:
        new_working_dir = str()
        new_home = str()
        
        working_dir_path = x.getElementsByTagName('option')[-1]
        tmp_path = working_dir_path.getAttributeNode('value').nodeValue
        tmp_list = tmp_path.split('/')
        tmp_list[2] = project_dir_name
        for i in tmp_list:
            if i[0] == '$':
                new_working_dir += i
            else:
                new_working_dir = new_working_dir + '/' + i
        working_dir_path.getAttributeNode('value').nodeValue = new_working_dir
        
        personetics_home = x.getElementsByTagName('entry')[1]
        tmp_path = personetics_home.getAttributeNode('value').nodeValue
        tmp_list = tmp_path.split('\\')
        tmp_list[tmp_list.index('profiles') - 1] = project_dir_name
        for i in tmp_list:
            if i == 'C:':
                new_home += i
            else:
                new_home = new_home + '\\' + i
        personetics_home.getAttributeNode('value').nodeValue = new_home
        
        conf.writexml(open(intelliJ_path, 'w'))
    info('InteliJ configurations were updated')


def main(argv):
    info("Creating new SCategoryGroups.json override")
    try:
        solution = getPath('solution')
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    
    print(solution)
    projectName = os.path.basename(solution)
    print(projectName)
    if checkForProperties(solution):
        updateConfigurations(projectName, getPath('intelliJ'))
        editProperties(createPath(solution, 'profiles\\local\\personetics.properties'), argv[0])
        info("Project configuration complete")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 Channel's name
