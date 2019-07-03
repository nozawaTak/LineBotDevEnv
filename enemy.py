import config
import pymysql

class Enemy:
    def __init__(self, enemyID):
        self.enemyID = enemyID
        dbinfo = config.getInfoToConnectDB()
        connection = pymysql.connect(host = dbinfo['host'],
                                    user = dbinfo['user_name'],
                                    password = dbinfo['password'],
                                    db = dbinfo['db_name'],
                                    charset = 'utf8',
                                    cursorclass = pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from ENEMY WHERE id = %s", (self.enemyID))
            enemyInfo = cursor.fetchone()
            self.name = enemyInfo['name']
            self.hp = enemyInfo['hp']
            self.attack = enemyInfo['attack']
            self.defense = enemyInfo['defense']
            self.speed = enemyInfo['speed']
            self.money = enemyInfo['money']
            self.imagePath = enemyInfo['imagePath']
        connection.close()
