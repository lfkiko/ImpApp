import json
import os.path
import sys


def getInsightList(path):
    insightsList = []
    for insght in os.listdir(path):
        insghtName = str(insght).split('_details_')[-1].split('.')[0]
        if insghtName not in insightsList:
            insightsList.append(insghtName)
    insightsList.sort()
    print(len(insightsList))
    return insightsList


def userList(path):
    usersList = {}
    for user in os.listdir(path):
        try:
            with open(os.path.join(path, user), "r") as t:
                userData = json.loads(t.read())
            usersList[user.split('_')[0]] = {}
            if userData['status'] == '200':
                usersList[user.split('_')[0]]['numberOfInsights'] = userData['numberOfInsights']
                usersList[user.split('_')[0]]['unreadMessages'] = userData['unreadMessages']
                usersList[user.split('_')[0]]['numberOfUnreadInsights'] = userData['numberOfUnreadInsights']
        except Exception as u:
            print(u)
    return usersList


def main(argv):
    mainPath = os.path.curdir
    users = os.path.join(mainPath, 'getInsights')
    teasers = os.path.join(mainPath, 'teasers')
    stories = os.path.join(mainPath, 'details')
    insightsList = getInsightList(stories)
    theJason = userList(users)
    
    insightData = {}
    for teaser in os.listdir(teasers):
        user = teaser.split('_')[0]
        insight = teaser[teaser.index('_'):teaser.index('.')]
        if insight[1:] in insightsList:
            try:
                with open(os.path.join(teasers, teaser), "r") as t:
                    teaserData = json.loads(t.read())
                teaserData.pop('facts')
                insightData['teaserBlocks'] = teaserData['teaserBlocks']
                teaserData.pop('teaserBlocks')
                teaserData.pop('id')
                insightData['SInsight'] = teaserData
            except Exception as a:
                print(a)
            try:
                with open(os.path.join(stories, teaser[:teaser.index('_') + 1] + 'details' + teaser[teaser.index('_'):]), "r") as s:
                    storyData = json.loads(s.read())
                insightData['story'] = storyData['story']
                insightData['text'] = storyData['text']
                insightData['expressions'] = storyData['expressions']
                t.close()
                s.close()
                if user not in theJason.keys():
                    theJason[user] = {}

                theJason[user][insight] = insightData
                insightsList.remove(insight[1:])
            except Exception as e:
                print(e)
        if len(insightsList) == 0:
            break

    try:
        f = open(os.path.join(mainPath, 'mergedData.json'), "w")
        f.write(json.dumps(theJason, indent=4))
    except Exception as w:
        print(w)
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])

#   0 - old versioins file
#   1 - new versioins file
