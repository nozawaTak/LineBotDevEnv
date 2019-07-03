from player import Player
from battle import Battle
from world import World
import pymysql 
import config

class Game():
    def __init__(self, userID, userName):
        self.player = None
        dbinfo = config.getInfoToConnectDB()
        self.connection = pymysql.connect(host = dbinfo['host'],
                            user = dbinfo['user_name'],
                            password = dbinfo['password'],
                            db = dbinfo['db_name'],
                            charset = 'utf8',
                            cursorclass = pymysql.cursors.DictCursor)
        if self._exist(userID):
            self.player = Player(userID)
        else:
            self._registUser(userID, userName)

    def _exist(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM USER WHERE id = %s", (id))
            recordNum = cursor.fetchone()['count(*)']
        if recordNum == 0:
            return False
        else:
            return True

    def _registUser(self, userID, userName):
        with self.connection.cursor() as cursor:
            name = userName
            money = 1000
            position_x = 200
            position_y = 200
            hp = 30
            state = "BATTLE"
            battleID = None
            sql = "INSERT INTO EQUIPMENT(equip_weapon, equip_armor) VALUES(1, 1)"
            cursor.execute(sql)
            equipID = cursor.lastrowid
            sql = "INSERT INTO USER VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (userID, name, money, position_x, position_y, hp, state, battleID, equipID)
            print(values)
            cursor.execute(sql, values)
        self.connection.commit()
        
    def step(self, text):
        if self.player is not None:
            if self.player.state == "BATTLE":
                battle = Battle(self.player.userId)
                return battle.battle()
            elif self.player.state == "WORLD":
                world = World(self.player.userId)
                imageURI = world.move(text)
                return {"img": imageURI}
            else:
                return {"text": ["still not implemented"]}
        else:
            return {"text": ["あなたのセーブデータを作成しました！"]}