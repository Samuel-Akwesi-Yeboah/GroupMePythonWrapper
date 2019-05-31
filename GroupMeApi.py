import requests
class GroupMeLibrary:

    baseURL = "https://api.groupme.com/v3"
    pictureURL = "https://image.groupme.com"
    def __init__(self, accesToken):
        self.accesToken = accesToken
        self.pictures = {}
        self.groupChats = {}

    def addGroup(self, groupName, groupId, botId):
        botInfo = (groupId,botId)
        self.groupChats[groupName] = botInfo

    def removeGroup(self,groupName):
        del self.groupChats[groupName]

    def sendMessage(self, groupName, message):
        botId = self.groupChats[groupName][1]
        data = {
            "bot_id" : botId,
            "text": message
        }
        response = requests.post(self.baseURL + "/bots/post", data=data)
        return response.status_code

    def uploadPicture(self, pictureName):
        headers = {
            "X-Access-Token" : self.accesToken,
            "Content-Type" : 'image/jpeg'
        }

        data = open(pictureName, 'rb').read()
        response = requests.post(self.pictureURL + "/pictures", headers = headers, data=data)
        if (response.status_code == 200):
            self.pictures[pictureName] = response
        return response.status_code

    def sendMessageAndPicture(self, groupName, pictureFileName, message):
        botId = self.groupChats[groupName][1]
        pictureURL = self.pictures[pictureFileName]
        pictureURL = pictureURL.content.decode("utf-8")
        pictureURL = eval(pictureURL)
        #print(pictureURL)
        data = {
            "bot_id": botId,
            "text": message,
            'picture_url': pictureURL['payload']['picture_url']
        }

        response = requests.post(self.baseURL + "/bots/post", data=data)
        print(response.status_code)
        return response.status_code

    def messageAllGroups(self,message):
        for groupChatName in self.groupChats:
            self.sendMessage(groupChatName,message)

    def messageAllGroupsWithPicture(self,message,pictureFileName):
        for groupChatName in self.groupChats:
            self.sendMessageAndPicture(groupChatName, pictureFileName, message)
