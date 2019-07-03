import cv2
import pymysql
import config
import random
from battle import Battle
import os

class World:
    def __init__(self, userID):
        self.worldMap = cv2.imread("Resources/worldMap.png")
        self.hero = cv2.imread("Resources/hero.png", cv2.IMREAD_UNCHANGED)
        self.userID = userID
        dbinfo = config.getInfoToConnectDB()
        self.connection = pymysql.connect(host = dbinfo['host'],
                            user = dbinfo['user_name'],
                            password = dbinfo['password'],
                            db = dbinfo['db_name'],
                            charset = 'utf8',
                            cursorclass = pymysql.cursors.DictCursor)
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * from USER WHERE id = %s", (userID))
            userInfo = cursor.fetchone()
            self.position_x = userInfo['position_x']
            self.position_y = userInfo['position_y']
    
    def move(self, text):
        STEPSIZE = 10
        if text == "右":
            self.position_x = self.position_x if self.position_x + STEPSIZE <= self.worldMap.shape[1] - self.hero.shape[1]//2 else self.position_x
            self.drawHeroInWorld(self.position_x, self.position_y)
        elif text == "左":
            self.position_x = self.position_x if self.position_x - STEPSIZE >= self.hero.shape[1]//2 else self.position_x
            self.drawHeroInWorld(self.position_x, self.position_y)
        elif text == "上":
            self.position_y = self.position_y if self.position_y - STEPSIZE >= self.hero.shape[0]//2 else self.position_y
            self.drawHeroInWorld(self.position_x, self.position_y)
        elif text == "下":
            self.position_y = self.position_y if self.position_y + STEPSIZE <= self.worldMap.shape[0] - self.hero.shape[0]//2 else self.position_y
            self.drawHeroInWorld(self.position_x, self.position_y)
        else:
            self.drawHeroInWorld(self.position_x, self.position_y)
        imageURI = "https://nozawa-linebot.tk/Resources/worldImg/" + self.userID + "_worldMap.jpg"
        return imageURI

    def randomEncount(self):
        rnd = random.random()
        if rnd < 0:
            battle = Battle(self.userID)
        text = battle.enemy.name + "が現れた！"
        return True, [text]

    def drawHeroInWorld(self, posX, posY):
        mask = self.hero[:,:,3]
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = mask // 255 
        self.hero = self.hero[:,:,:3]
        height, width = self.hero.shape[:2]
        height //= 2
        width //= 2
        self.worldMap[posY-height:posY+height, posX-width:posX+width] *= 1 - mask
        self.worldMap[posY-height:posY+height, posX-width:posX+width] += self.hero * mask

        cropWidth = 128
        cropHeight = 128
        cropImg = self.worldMap[posY-cropHeight:posY+cropHeight, posX-cropWidth:posX+cropWidth]
        img = cv2.resize(cropImg, (512,512))
        path = "Resources/worldImg/" + self.userID + "_worldMap.jpg"
        cv2.imwrite(path, img)


    def getNowWorldImg(self):
        return "https://nozawa-linebot.tk/Resources/worldImg/" + self.userID + "_worldMap.jpg"