import config
import pymysql


class EnemyInstance:
    def __init__(self, battleID):
        self.battleID = battleID
        dbinfo = config.getInfoToConnectDB()
        self.connection = pymysql.connect(host = dbinfo['host'],
                            user = dbinfo['user_name'],
                            password = dbinfo['password'],
                            db = dbinfo['db_name'],
                            charset = 'utf8',
                            cursorclass = pymysql.cursors.DictCursor)
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM BATTLEINFO WHERE id = %s", (battleID))
            enemyInfo = cursor.fetchone()
            self.__hp = enemyInfo['enemyHP']
            self.attack = enemyInfo['enemyAttack']
            self.defense = enemyInfo['enemyDefense']
            self.speed = enemyInfo['enemySpeed']
            self.money = enemyInfo['enemyMoney']
            self.name = enemyInfo['enemyName']

    @property
    def hp(self):
        return self.__hp
    
    @hp.setter
    def hp(self, newHP):
        self.__hp = newHP
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE BATTLEINFO SET enemyHP = %s WHERE id = %s", (newHP, self.battleID))
        self.connection.commit()
