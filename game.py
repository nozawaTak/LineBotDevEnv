class RPG():
    def Battle():
        if (enemySpeed <= playerSpeed):
            playerAtack = getPlayerAtack()
            enemyDefense = getEnemyDefence()
            damage = calcDamage(playerAtack, enemyDefense)
            if enemyHP - damage <= 0:      
                defeat()          
            else:
                damageProcess(damage)


                
                playerDefense = getPlayerDefence()
            damage = calcDamage(playerAtack, enemyDefense)
            else:
                setEnemyHP(enemyHP - damage)
            


    def getPlayerAtack():
        pass
    
    def getPlayerDefense():
        pass
    
    def getEnemyAtack():
        pass

    def getEnemyDefence():
        pass
    
    def calcDamage(atack, defense):
        damage = atack - defense
        return damage if damage > 0 else 1

    def defeat():
        pass

    def damageProcess(damage)
        text = enemyName + "に" + str(damage) + "のダメージ！！"
        newHP = enemyHP - damage
        
        pass
