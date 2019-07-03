from player import Player
from enemy import Enemy
from enemyInstance import EnemyInstance
import config
import pymysql
import random

class Battle():
    def __init__(self, userID):
        self.player = Player(userID)
        if self.player.battleID is None:
            self.player.battleID = self.spawnNewBattle(self._randomEnemyID())
        self.enemy = EnemyInstance(self.player.battleID)
        self.result = []

    def spawnNewBattle(self, enemyID):
        enemy = Enemy(enemyID)
        dbinfo = config.getInfoToConnectDB()
        connection = pymysql.connect(host = dbinfo['host'],
                                    user = dbinfo['user_name'],
                                    password = dbinfo['password'],
                                    db = dbinfo['db_name'],
                                    charset = 'utf8',
                                    cursorclass = pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "INSERT INTO BATTLEINFO (enemyHP, enemyAttack, enemyDefense, enemySpeed, enemyMoney, enemyName) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (enemy.hp, enemy.attack, enemy.defense, enemy.speed, enemy.money, enemy.name)
            cursor.execute(sql, values)
            battleID = cursor.lastrowid
            connection.commit()
        connection.close()
        return battleID


    def battle(self):
        if (self.player.speed >= self.enemy.speed):
            self._playerAttackTurn()
            if (self.enemy.hp <= 0):
                return self._defeat()
            self._enemyAttackTurn()
            if (self.player.hp <= 0):
                return self._defeated()
            reply = self.result
            self.result = []
            return reply
        else:
            self._enemyAttackTurn()
            if (self.player.hp <= 0):
                return self._defeated()
            self._playerAttackTurn()
            if (self.enemy.hp <= 0):
                return self._defeat()
            reply = self.result
            self.result = []
            return reply

    def _playerAttackTurn(self):
        damage = self._calcDamage(self.player.attack, self.enemy.defense)
        self._damageProcess(self.enemy, damage)

    def _enemyAttackTurn(self):
        damage = self._calcDamage(self.enemy.attack, self.player.defense)
        self._damageProcess(self.player, damage)

    def _calcDamage(self, attack, defense):
        damage = attack - defense
        return damage if damage > 0 else 1

    
    def _defeat(self):
        text = self.enemy.name + "に勝った！\n"
        text += str(self.enemy.money) + "円獲得した!\n"
        self.player.money = self.player.money + self.enemy.money
        self.result.append(text)
        self._finishBattle()
        reply = self.result
        self.result = []
        return reply

    def _defeated(self):
        loss = self.player.money // 3
        text = self.enemy.name + "に負けてしまった...\n"
        text += str(loss) + "円失ってしまった...\n"
        self.player.money = self.player.money - loss
        self.result.append(text)
        self._finishBattle()
        reply = self.result
        self.result = []
        return reply

    def _damageProcess(self, character, damage):
        text = character.name + "に" + str(damage) + "のダメージ！！"
        self.result.append(text)
        newHP = character.hp - damage
        character.hp = newHP
    
    def _finishBattle(self):
        self.player.state = "WORLD"
        self.player.battleID = None

    def _randomEnemyID(self):
        enemyIDs = []
        dbinfo = config.getInfoToConnectDB()
        connection = pymysql.connect(host = dbinfo['host'],
                                    user = dbinfo['user_name'],
                                    password = dbinfo['password'],
                                    db = dbinfo['db_name'],
                                    charset = 'utf8',
                                    cursorclass = pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sql = "SELECT id FROM ENEMY"
            cursor.execute(sql)
            results = cursor.fetchall()
            for r in results:
                enemyIDs.append(r['id'])
        connection.close()
        index = random.randint(0, len(enemyIDs)-1)
        return enemyIDs[index]