# editing workspace.xml to match Directorie's name must rerun IntelliJ after update
# adding to the project modified properties with the Channels name
import os
import sys
from shutil import copyfile
import xml.dom.minidom

from Scripts.toolBoox.toolBoox import getFile, readJson


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
            if line != '\n':
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
    pass


def checkForProperties(dir_path):
    path = os.path.join(dir_path, 'profiles\\local')
    if 'personetics.properties' in os.listdir(path):
        path = os.path.join(path, 'personetics.properties')
        return True
    
    else:
        properties = getFile('projectProperties')
        file_name = os.path.basename(properties)
        copyfile(properties, os.path.join(path, file_name))
        path = os.path.join(dir_path, path, 'personetics.properties')
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
    pass


def main(argv):
    path = findProfile(argv[0])
    if checkForProperties(path):
        editProperties(os.path.join(path, 'profiles\\local\\personetics.properties'), argv[1])
        updateConfigurations(argv[2], readJson(getFile('settings'))['intelliJRoot'])
        print("Project configuration complete")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # [Path, Channel's name, project's dir name, IntelliJ project path/name]
