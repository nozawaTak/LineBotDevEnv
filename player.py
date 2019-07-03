import pymysql
import config

class Player:
    def __init__(self, userId):
        self.userId = userId
        dbinfo = config.getInfoToConnectDB()
        self.connection = pymysql.connect(host = dbinfo['host'],
                                        user = dbinfo['user_name'],
                                        password = dbinfo['password'],
                                        db = dbinfo['db_name'],
                                        charset = 'utf8',
                                        cursorclass = pymysql.cursors.DictCursor)
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * from USER WHERE id = %s", (self.userId))
            userInfo = cursor.fetchone()
            self.__hp = userInfo['hp']
            self.name = userInfo['name']
            self.__money = userInfo['money']
            self.__position_x = userInfo['position_x']
            self.__position_y = userInfo['position_y']
            self.__state = userInfo['state']
            self.__battleID = userInfo['battleID']
            self.equipment = userInfo['equipment']
            cursor.execute("SELECT * from EQUIPMENT WHERE id = %s", (self.equipment))
            equipInfo = cursor.fetchone()
            cursor.execute("SELECT attack from WEAPON WHERE id = %s", (equipInfo['equip_weapon']))
            weaponInfo = cursor.fetchone()
            self.attack = weaponInfo['attack']
            cursor.execute("SELECT * from ARMOR WHERE id = %s", (equipInfo['equip_armor']))
            armorInfo = cursor.fetchone()
            self.defense = armorInfo['defense']
            self.speed = armorInfo['speed']

    @property
    def hp(self):
        return self.__hp

    @property
    def money(self):
        return self.__money

    @property
    def state(self):
        return self.__state

    @property
    def position_x(self):
        return self.__position_x
    
    @property
    def position_y(self):
        return self.__position_y

    @property
    def battleID(self):
        return self.__battleID

    @hp.setter
    def hp(self, hp):
        self.__hp = hp
        with self.connection.cursor() as cursor:
            sql = "UPDATE USER SET hp = %s WHERE id = %s"
            cursor.execute(sql, (hp, self.userId))
        self.connection.commit()

    @money.setter
    def money(self, money):
        self.__money = money
        with self.connection.cursor() as cursor:
            sql = "UPDATE USER SET money = %s WHERE id = %s"
            cursor.execute(sql, (money, self.userId))
        self.connection.commit()
    
    @state.setter
    def state(self, state):
        self.__state = state
        with self.connection.cursor() as cursor:
            sql = "UPDATE USER SET state = %s WHERE id = %s"
            cursor.execute(sql, (state, self.userId))
        self.connection.commit()
    
    @position_x.setter
    def position_x(self, position_x):
        if self.__position_x != position_x:
            self.__position_x = position_x
            with self.connection.cursor() as cursor:
                sql = "UPDATE USER SET position_x = %s WHERE id = %s"
                cursor.execute(sql, (position_x, self.userId))
            self.connection.commit()

    @position_y.setter
    def position_y(self, position_y):
        if self.__position_y != position_y:
            self.__position_y = position_y
            with self.connection.cursor() as cursor:
                sql = "UPDATE USER SET position_y = %s WHERE id = %s"
                cursor.execute(sql, (position_y, self.userId))
            self.connection.commit()

    @battleID.setter
    def battleID(self, battleID):
        self.__battleID = battleID
        with self.connection.cursor() as cursor:
            sql = "UPDATE USER SET battleID = %s WHERE id = %s"
            cursor.execute(sql, (battleID, self.userId))
        self.connection.commit()
    
    def _testPrint(self):
        print(self.__hp)
        print(self.name)
        print(self.__money)
        print(self.__position_x)
        print(self.__position_y)
        print(self.__state)
        print(self.equipment)
        print(self.attack)
        print(self.defense)
        print(self.speed)