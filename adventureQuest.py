#! python3

"""Adventure Quest - A small text-based adventure game

Start by choosing your character's name and then, from the main menu you can choose to:
- Explore, where you risk fighting Goblins, Wolves and Bandits at locations such as a
Castle, a Witch House, a Tavern or a Bandit's Lair, to find treasures.
- Rest, where you replenish your health points full.
- Check inventory to see what items you have.
- Shop, where you can buy new items as long as you have enough gold.
- Show scores, where you can see all the previous scores since the program was open.
- Exit game to terminate the program.

When you find a treasure, no more treasures can be found at that location. When you find
enemies, you lose the game if they kill you and if you kill them, they no longer can be
found at that location. While fighting you can take a potion to fully replenish your health
if you have one. When you find 3 treasures you win the game.
"""

import random, sys

treasureCounter = 0 # Initializing the treasure count. When it is 3 the player wins.
highScores = {} # Dictionary where the previous rounds scores are saved

def chooseLocation():
    """This function shows the locations menu and gets the user's location choice"""
    print('\n' + 'LOCATIONS'.center(13))
    print("""
1 - Castle
2 - Witch House
3 - Tavern
4 - Bandit's Lair
""")
    return input('Choose where you want to go 1 - 4: ')

def randomEncounter():
    """This function returns the 'dice roll' that determines if enemies or treasure or
nothing is found in a location"""
    choiceList = ['enemy',
            'enemy',
            'enemy',
            'enemy',
            'enemy',
            'treasure',
            'treasure',
            'treasure',
            'nothing',
            'nothing']
    return choiceList[random.randint(0, 9)]

def printHealthStats(hp):
    """This function prints the player's and the enemy's health points in between rounds of
combat"""
    print('\nPlayer\'s health points: ' + str(player['hp']))
    if hp > 0: # This if statement makes sure that negative health points aren't printed
        print('Enemy\'s health points: ' + str(hp))
    else:
        print('Enemy\'s health points: 0')

def lootToInventory(enemy, k):
    """This function updates the player's inventory and gold with the loot of a dead
enemy"""
    if 'items' in enemies[enemy]:
        print('\n' + k + "'s loot added to inventory:")
        for key, value in enemies[enemy]['items'].items():
            if key != 'gold':
                print(key + ': ' + str(value))
                player['inventory'].setdefault(key, 0)
                player['inventory'][key] += value
            else:
                print(key + ': ' + str(value))
                player['gold'] += value

def fight(enemy, k, arg):
    """"This function has the combat mechanic including randomized damage points inflicted
on the enemy, randomized damage inflicted on the player by the enemy, randomized choice of
who gets hit and drinking potion mechanic to fully repenlish the player's health"""
    hp = enemies[enemy]['hp']
    while hp > 0 and player['hp'] > 0:
        if random.randint(0, 1) == 0: # Subtracts enemy hp when hit
            damage = random.randint(1, 6)
            hp -= damage
            if damage > 1:
                print('\nYou struck the ' + k + ' and inflicted ' + str(damage) +
                      ' points of damage on it!')
            else:
                print('\nYou struck the ' + k + ' and inflicted ' + str(damage) +
                      ' point of damage on it!')
            printHealthStats(hp)  
        else: # Subracts hp when player is hit
            damage = random.randint(enemies[enemy]['damage'] - 3,
                                    enemies[enemy]['damage'] + 3)
            player['hp'] -= damage
            if player['hp'] < 0:
                player['hp'] = 0
            if damage > 1:
                print('\nThe ' + k + ' struck you and inflicted ' + str(damage) +
                      ' points of damage on you!')
            else:
                print('\nThe ' + k + ' struck you and inflicted ' + str(damage) +
                      ' point of damage on you!')
            printHealthStats(hp)
            if player['inventory'].get('potion', 0) > 0 and player['hp'] > 0: 
                while True: # Potion taking mechanic
                    potion = input('\nUse potion to restore health (y/n): ').lower().strip()
                    if potion == 'y':
                        player['inventory']['potion'] -= 1
                        player['hp'] = 99
                        printHealthStats(hp)
                        break
                    elif potion == 'n':
                        break
                    else:
                        print('\nInvalid input!')
    if player['hp'] <= 0: # Ends the game when player dies
        print('\nYou were killed by the ' + k + '!')
        defeat()
        return True
    locations[arg][k] -= 1 # Updates number of enemies after one dies
    if locations[arg][k] > 0:
        print('\nYou killed one ' + k + '! ' + str(locations[arg][k]) + ' to go!')
    else:
        print('\nYou killed the last ' + k)
    lootToInventory(enemy, k)
    
def enemy(arg):
    """"This function has the fight or flee choice when a group of enemies appears, for each
group of enemies at the location. It keeps on offering that choice until all enemies are
defeated"""
    for k, v in locations[arg].items(): # Repeats combat for each type of enemy at location
        if k != 'treasure' and v > 0:
            if k == 'Goblin':
                enemy = 0
            elif k == 'Wolf':
                enemy = 1
            elif k == 'Bandit':
                enemy = 2
            print('\n' + str(v) + ' enemies of type ' + k + ' appear!')
            while True: # Fight or flee mechanic
                choice = input('\nFight or flee (fight/flee): ').lower().strip()
                if choice == 'fight':            
                    while locations[arg][k] > 0:
                        if fight(enemy, k, arg) == True:
                            return True
                    print('\nYou killed all the enemies of type ' + k + ' in the ' +
                          arg + '!')
                    break
                elif choice == 'flee':
                    print('\nYou escaped the attack!')
                    return
                else:
                    print('\nInvalid input!')
    print('\nThere are no more enemies in the ' + arg + '!')
    # Erasing enemies at the location after all are defeated
    for i in ['Goblin', 'Wolf', 'Bandit']:
        if i in locations[arg]:
            del locations[arg][i]
                           
def treasure(arg):
    """This function erases the treasure at the location and updates the player inventory,
gold and the treasure counter when a treasure is found"""
    global treasureCounter
    treasureCounter += 1
    print('\nTreasure found!')
    print('\n' + 'Treasure'.center(10))
    for k, v in locations[arg]['treasure'].items():
        print(k.title().rjust(6) + ':' + str(v).rjust(3))
        if k != 'gold':
            player['inventory'].setdefault(k, 0)
            player['inventory'][k] += v
        else:
            player['gold'] += v
    del locations[arg]['treasure']
    print('\nTreasure added to inventory!')
    if treasureCounter == 3: # When the counter is 3 the game is won
        victory()
        return True

def playAgain():
    """This function asks the player to play again when the game ends, whether in victory or
defeat, and resets the player, shop and locations dictionaries to their initial values"""
    global player, shopInventory, locations, treasureCounter
    while True:
        choice = input('\nPlay again (y/n): ')
        if choice == 'y':
            player = {'name': 'Hero', 'hp': 99, 'gold': 0, 'inventory': {}}
            shopInventory = {'bow': [5, 5],
                             'arrow': [100, 1],
                             'dagger': [3, 10],
                             'torch': [7, 2],
                             'potion': [2, 15]}
            locations = {'castle': {'Wolf': 5,
                                    'treasure': {'gold': 15,
                                                 'bow': 1,
                                                 'arrow': 5}},
                         'witch house': {'Goblin': 4,
                                         'treasure': {'gold': 10,
                                                      'ruby': 1,
                                                      'potion': 2,
                                                      'torch': 1,
                                                      'dagger': 1}},
                         'tavern': {'Goblin': 2,
                                    'Bandit': 2,
                                    'treasure': {'gold': 18,
                                                 'rope': 2}},
                         'bandit\'s lair': {'Bandit': 3,
                                            'treasure': {'gold': 23,
                                                         'torch': 1,
                                                         'dagger': 2,
                                                         'arrow': 10}}}
            treasureCounter = 0
            player['name'] = input('\nChoose your name: ')
            return
        elif choice == 'n': # If the player chooses to not play again the program ends
            exitGame()
        else:
            print('\nInvalid input!')  

def defeat():
    """This function informs the player when the game is lost"""
    print('\nGAME OVER - YOU LOSE!')
    playAgain()

def victory():
    """This function informs the player when the game is won and has the scoring mechanic"""
    print('\nGAME OVER - YOU WIN!')
    try: # Calculates the score
        score = 30 * player['inventory']['ruby'] + player['gold']
    except KeyError:
        score = player['gold']
    highScores.setdefault(player['name'], [0])
    if highScores[player['name']] == [0]: # Adds the score to the highscores table
        highScores[player['name']] = [score]
    else:
        highScores[player['name']] += [score]
    print('\nYour score is ' + str(score))
    print('\nScore added to High Scores.')
    playAgain()
    
def returnToMainMenu():
    """This function has the return to the main menu mechanic and is called everywhere
in the program. It also shows the player health points and gold"""
    while True:
        choice = input('\nReturn to the Main Menu (y/n): ').lower().strip()
        if choice == 'y':
            print('\nUPDATED PLAYER STATS')
            print('Health Points:'.rjust(16) + str(player['hp']).rjust(3))
            print('Gold:'.rjust(16) + str(player['gold']).rjust(3))
            return
        elif choice == 'n':
            return 'n'
        else:
            print('\nInvalid input!')

def promptMenu():
    """"This function prints the main menu and gets the player's action choice."""
    print('\n' + '  MAIN MENU'.center(15))
    print("""
1 - Explore
2 - Rest
3 - Check Inventory
4 - Shop
5 - Show Scores
6 - Exit Game
""")
    return input('Choose an action 1 - 6: ')

def explore():
    """This function defines what happens next based on the location choice and the result
of the dice roll"""
    while True:
        location = chooseLocation()
        diceRoll = randomEncounter()
        if location == '1':
            if diceRoll == 'enemy' and ('Goblin' in locations['castle'] or 'Wolf' in
                                        locations['castle'] or 'Bandit' in
                                        locations['castle']):
                if enemy('castle') == True:
                    return
            elif diceRoll == 'treasure' and 'treasure' in locations['castle']:
                if treasure('castle') == True:
                    return
            else:
                print('\nNo enemies or treasure were found!')
        elif location == '2':
            if diceRoll == 'enemy' and ('Goblin' in locations['witch house'] or 'Wolf'
                                        in locations['witch house'] or 'Bandit' in
                                        locations['witch house']):
                if enemy('witch house') == True:
                    return
            elif diceRoll == 'treasure' and 'treasure' in locations['witch house']:
                if treasure('witch house') == True:
                    return
            else:
                print('\nNo enemies or treasure were found!')    
        elif location == '3':
            if diceRoll == 'enemy' and ('Goblin' in locations['tavern'] or 'Wolf' in
                                        locations['tavern'] or 'Bandit' in
                                        locations['tavern']):
                if enemy('tavern') == True:
                    return
            elif diceRoll == 'treasure' and 'treasure' in locations['tavern']:
                if treasure('tavern') == True:
                    return
            else:
                print('\nNo enemies or treasure were found!')    
        elif location == '4':
            if diceRoll == 'enemy' and ('Goblin' in locations['bandit\'s lair'] or
                                        'Wolf' in locations['bandit\'s lair'] or
                                        'Bandit' in locations['bandit\'s lair']):
                if enemy('bandit\'s lair') == True:
                    return
            elif diceRoll == 'treasure' and 'treasure' in locations['bandit\'s lair']:
                if treasure('bandit\'s lair') == True:
                    return
            else:
                print('\nNo enemies or treasure were found!')    
        else:
            print('\nThat is not a valid location!')
        if returnToMainMenu() == 'n':
            continue
        else:
            break

def rest():
    """"This function resets the player's health"""
    player['hp'] = 99
    while True:
        print('\nYou are fully recovered and ready to fight again!')
        if returnToMainMenu() == 'n':
            continue
        else:
            break

def checkInventory():
    """This function prints the player's current inventory"""
    while True:
        print('\n' + 'INVENTORY'.center(9))
        for k, v in player['inventory'].items():
            if v > 0:
                print(k.title().rjust(6) + ':' + str(v).rjust(3))
        if returnToMainMenu() == 'n':
            continue
        else:
            break
       
def shop():
    """This function has the whole shopping mechanic, printing the shop's inventory, getting
the player's choice of item and quantity to buy and updates both the player's and shops's
inventory"""
    while True:
        print('\n' + 'SHOP\'S INVENTORY'.center(22))
        for k, v in shopInventory.items(): # Prints shop inventory
            if v[0] > 0:
                print('\n' + k.title().center(22) + '\n' + 'Quantity:'.rjust(19) +
                      str(v[0]).rjust(3) + '\nPrice (gold coins):' + str(v[1]).rjust(3))
        while True: # Gets the user choice and updates inventories
            item = input('\nWhat item do you want to buy? ').lower().strip()
            if item in shopInventory:
                if player['gold'] >= shopInventory[item][1]:
                    while True:
                            while True:
                                try:
                                    quantity = int(input
                                                   ('\nHow many units do you want to buy? '))
                                    if quantity <= 0:
                                        print('\nYou must enter a positive number!')
                                    else:
                                        break
                                except ValueError:
                                    print('\nYou must enter an integer!') 
                            if (player['gold'] >= quantity * shopInventory[item][1] and
                                shopInventory[item][0] - quantity >= 0):
                                player['inventory'].setdefault(item, 0)
                                player['inventory'][item] += quantity
                                player['gold'] -= quantity * shopInventory[item][1]
                                shopInventory[item][0] -= quantity
                                break
                            elif shopInventory[item][0] - quantity < 0:
                                print('\nThe shop has only ' + str(shopInventory[item][0])
                                      + '!')
                            else:
                                print('\nYou don\'t have enough gold to buy ' +
                                      str(quantity) + ' ' + item + 's!')                 
                else: # Validates if the player has enough gold to buy the item
                    print('\nYou don\'t have enough gold to buy one ' + item + '!')
                    break
                break
            else:
                print('\nThe shop doesn\'t have that item!')
        if returnToMainMenu() == 'n':
            if player['gold'] == 0: # Validates if the player has gold
                print('\nYou don\'t have gold!')
                break
            continue
        else:
            break         
    
def showScores():
    """"This function shows the scores from all the rounds played since the program was
open"""
    while True:
        print('\nSCORES\n')
        for k, v in highScores.items():
            v.sort(reverse=True)
            string = ''
            for i in range(len(v)):
                string += str(v[i]) + '; '
            print(k + ': ' + string)
        if returnToMainMenu() == 'n':
            continue
        else:
            break

def exitGame():
    """This function exits the program"""
    print('\nSee you next time!')
    sys.exit()

def main():
    """This is the main program function. It let's the player choose the character name and
defines what happens based on the player's action choice"""
    player['name'] = input('\nChoose your name: ')
    while True:
        action = promptMenu()
        if action == '1':
            explore()
        elif action == '2':
            rest()
        elif action == '3':
            checkInventory()
        elif action == '4':
            shop()
        elif action == '5':
            showScores()
        elif action == '6':
            exitGame()
        else:
            print('\nThat is not a valid action!')

# All program's data structures with their initial values

player = {'name': 'Hero',
          'hp': 99,
          'gold': 0,
          'inventory': {}}             

enemies = [{'name': 'Goblin',
            'hp': 20,
            'damage': 5,
            'items': {'torch': 1,
                      'dagger': 1,
                      'gold': 2}},
           {'name': 'Wolf',
            'hp': 15,
            'damage': 4},
           {'name': 'Bandit',
            'hp': 25,
            'damage': 6,
            'items': {'bow': 1,
                      'arrow': 15,
                      'rope': 1,
                      'gold': 3}}]

shopInventory = {'bow': [5, 5],
                 'arrow': [100, 1],
                 'dagger': [3, 10],
                 'torch': [7, 2],
                 'potion': [2, 15]}

locations = {'castle': {'Wolf': 5,
                        'treasure': {'gold': 15,
                                     'bow': 1,
                                     'arrow': 5}},
             'witch house': {'Goblin': 4,
                             'treasure': {'gold': 10,
                                          'ruby': 1,
                                          'potion': 2,
                                          'torch': 1,
                                          'dagger': 1}},
             'tavern': {'Goblin': 2,
                        'Bandit': 2,
                        'treasure': {'gold': 18,
                                     'rope': 2}},
             'bandit\'s lair': {'Bandit': 3,
                                'treasure': {'gold': 23,
                                             'torch': 1,
                                             'dagger': 2,
                                             'arrow': 10}}}

# Short summary of the game that is shown when the program is open
print("""
Welcome to Adventure Quest!

An adventure game where you explore the Dark Woods,
fight Goblins, Wolves and Bandits and find Treasures!

Win by surviving until you find 3 treasures.

The final score is how much gold you have at the end.
""")

main()
