# SRO Mobile Center v0.93 - Plugin for phBot - Silkroad Online Game
# Copyright ILKERC - Under MIT License
# https://sromobilecenter.com/

from phBot import *
import phBotChat
import QtBind
import threading
import os
import random

# Global Variables
appName = 'SROMC'
appFullName = 'SRO Mobile Center'
appVersion = 'v0.93'
appAuthor = 'ILKERC'
appRunning = False
accountCreated = False
apiEndpoint = 'https://sromobilecenter.com/api/'

# Create GUI 
gui = QtBind.init(__name__, appName + ' ' + appVersion)
QtBind.createLabel(gui, appFullName + ' ' + appVersion, 10, 10)
QtBind.createLabel(gui, 'Generate a pairing code with the button below and enter it in the mobile app', 10, 40)
btnReset = QtBind.createButton(gui, 'reset_click', 'Reset and Stop', 10, 70)
btnCreate = QtBind.createButton(gui, 'showCode_click', 'Generate Pairing Code', 10, 70)
lblCode = QtBind.createLabel(gui, '', 10, 120)
lblPassword = QtBind.createLabel(gui, '', 10, 140)
lblCodeDesc = QtBind.createLabel(gui, '', 10, 180)
    

# Run app
def showCode_click():
    global accountCreated
    global appRunning
    char = get_character_data()
    status = get_status()
    accountId = str(char['account_id'])
    
    # Before created
    if(accountCreatedBefore() == True):
        accountCreated = True
    
    # Check character is in the game
    if isCharInGame() == False:
        QtBind.setText(gui, lblCode, 'Error!')
        QtBind.setText(gui, lblCodeDesc, 'Make sure the character is in the game.')
    else:
        server = str(char['server'])
        charName = str(char['name'])
        playerId = str(char['player_id'])
        randomNumber = str(random.randint(100000,999999))
        
        # Create account and get userid
        if accountCreated == False:
            userId = str('19238923')
            randomPassword = str(randomNumber)
            secret = str('98snkjnjkan983h98fn98fhn39fnsdkjfnsjkfns4329fn349fn34uf944f')
            QtBind.setText(gui, lblCode, 'Char ID: ' + userId)
            QtBind.setText(gui, lblPassword, 'Password: ' + randomPassword)
            QtBind.setText(gui, lblCodeDesc, 'You can log in to the mobile application with the above information. \nSave your password in a secure area. It will not be shown again')
            accountCreated = True
            
            # Save text file
            saveAccount(server, charName, userId, secret)
            
            # Message
            writeMessage('New account successfuly created. (' + server + '/' + charName + ')')
            appRunning = True
            connectApi()
            
        else:
            alreadyHave()
        
        start()
    
# Reset and delete account
def reset_click():
    global accountCreated
    global appRunning
    char = get_character_data()
    os.remove('Plugins/SROMC_'+ char['server'] + '_' + char['name'] + '.txt')
    writeMessage('Account successfuly deleted.')
    accountCreated = False
    appRunning = False
    start()

# Already have account message
def alreadyHave():    
    QtBind.setText(gui, lblCode, 'Char ID: ' + getUserId())
    QtBind.setText(gui, lblPassword, 'Password: XXXXXX')
    QtBind.setText(gui, lblCodeDesc, 'You have already created a user account.')
    
      
# If account created before, get user id
def getUserId():
    char = get_character_data()
    try:
        lines = list(open('Plugins/SROMC_'+ char['server'] + '_' + char['name'] + '.txt', 'r'))
        if len(lines) == 2:
            return str(lines[0]).replace('\n', '')
        else:
            return ''
    except:
        pass
    return ''
    

    
# Get token of user
def getToken():
    char = get_character_data()
    try:
        lines = list(open('Plugins/SROMC_'+ char['server'] + '_' + char['name'] + '.txt', 'r'))
        if len(lines) == 2:
            return str(lines[1]).replace('\n', '')
        else:
            return ''
    except:
        pass
    return ''

# Check account created before
def accountCreatedBefore():
    char = get_character_data()
    try:
        lines = list(open('Plugins/SROMC_'+ char['server'] + '_' + char['name'] + '.txt', 'r'))
        if len(lines) == 2:
            return True
        else:
            return False
    except:
        pass
    return False
    
# Save account info to file
def saveAccount(server, charName, userId, secret):
    lines = [userId, secret]
    with open('Plugins/SROMC_' + server + '_' + charName + '.txt', 'w') as f:
        f.write('\n'.join(lines))
        f.close()

# Check is char in game
def isCharInGame():
    accountId = str(get_character_data()['account_id'])
    if accountId == "0":
        return False
        
    return True

# Important events
def handle_event(t, data):
    if t == 5:
        log('Rare item drop')
    elif t == 6:
        log('Under attack by player')
    elif t == 7:
        log('Died')
    elif t == 8:
        log('Alhchemy completed')
    
# Message received
def handle_chat(t, player, msg):
    log(t + ' / ' +msg)
    
# Send PM
def sendPM(message, to, player):
    if to == 'party':
        phBotChat.Party(message)
    elif to == 'guild':
        phBotChat.Guild(message)
    elif to == 'union':
        phBotChat.Union(message)
    elif to == 'private':
        phBotChat.Private(player, message)
    else:
        phBotChat.All(message)

# Send info to api
def sendInfo():
    global appRunning
    
    # Re-run function if active
    # if appRunning == True:
    #    threading.Timer(3.0, sendInfo).start()
    
    # Get all neccesary info
    status = str(get_status())
    char = str(get_character_data())
    guild = str(get_guild())
    party = str(get_party())
    inventory = str(get_inventory())
    storage = str(get_storage())
    academy = str(get_academy())
    pets = str(get_pets())
    monsters = str(get_monsters())
    drops = str(get_drops())
    quests = str(get_quests())
    token = str(getToken())
    user_id = str(getUserId())
    requestJson = '{ userId: "' + user_id + '", token: "' + token + '", status: "' + status + '", character: ' + char + ', inventory: ' + inventory + ', storage: ' + storage + ', drops: ' + drops + ', guild: ' + guild + ', party: ' + party + ', quests: ' + quests + ', monsters: ' + monsters + ', pets: ' + pets + ', academy: ' + academy + ' }'
    
    # send JSON to server
    #log(requestJson)
    
# Write message    
def writeMessage(message):
    log('[' + appName + '] : ' + message)
    
# Send data
def connectApi():
    sendInfo()

# accountCreatedBefore
if(accountCreatedBefore() == True):
    alreadyHave()
    connectApi()
   
# First load check char has account
def start():
    if(accountCreatedBefore() == True):
        QtBind.move(gui, btnCreate, 10, -70)
        QtBind.move(gui, btnReset, 10, 70)
    else:
        QtBind.move(gui, btnCreate, 10, 70)
        QtBind.move(gui, btnReset, 10, -70)
        QtBind.setText(gui, lblCode, '')
        QtBind.setText(gui, lblPassword, '')
        QtBind.setText(gui, lblCodeDesc, '')
       

start()

# start_bot() // Start bot
# stop_bot() // Stop bot
# start_trace(char) // Trace a player
# stop_trace() // Stops trace
# set_training_position(0, 6400.0, 800.0, 0.0) // Region, x, y, z float
# set_training_radius(50.0) // radius float
# move_to(6400.0, 800.0, 0.0) // Move action x,y,z (z must 0)
# start_script(script) // walk,6435,1087,-32, ... and runs script
# stop_script() // Stops script
