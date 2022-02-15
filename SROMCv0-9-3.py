# SRO Mobile Center v0.93 - Plugin for phBot - Silkroad Online Game
# Copyright ILKERC - Under MIT License
# https://sromc.com/


from locale import getlocale
from phBot import *
import phBotChat
import QtBind
import os
import random
import urllib.request
import json
import struct
import string
import sqlite3
from datetime import datetime
from types import SimpleNamespace


# Global Variables
appName = 'SROMC'
appFullName = 'SRO Mobile Center'
appVersion = 'v0.93'
appAuthor = 'ILKERC'
appRunning = False
accountCreated = False
apiEndpoint = 'https://api.sromc.com'
apiRequests = 0
taskCompleted = False
deadCounter = 0
itemCounter = 0
rareItemCounter = 0
messages = []


# Create GUI
gui = QtBind.init(__name__, appName + ' ' + appVersion)
QtBind.createLabel(gui, '<b>' + appFullName + ' ' +
                   appVersion + '</b>', 10, 10)
QtBind.createLabel(gui, '', 10, 40)
QtBind.createLabel(
    gui, 'Generate a character login info with the button below and enter it in the mobile app. Visit <a href="https://sromc.com/">https://sromc.com</a>', 10, 40)
btnReset = QtBind.createButton(gui, 'reset_click', 'Reset and Stop', 10, 70)
btnCreate = QtBind.createButton(
    gui, 'showCode_click', 'Create Character', 10, 70)
lblCode = QtBind.createLabel(gui, '', 10, 120)
lblPassword = QtBind.createLabel(gui, '', 10, 140)
lblCodeDesc = QtBind.createLabel(gui, '', 10, 180)


# Run app
def showCode_click():
    global accountCreated
    global appRunning
    global apiRequests
    char = get_character_data()
    status = get_status()
    accountId = str(char['account_id'])
    apiRequests = 0

    # Before created
    if(accountCreatedBefore() == True):
        accountCreated = True

    # Check character is in the game
    if isCharInGame() == False:
        QtBind.setText(gui, lblCode, 'Error!')
        QtBind.setText(gui, lblCodeDesc,
                       'Make sure the character is in the game.')
    else:
        server = str(char['server'])
        charName = str(char['name'])
        playerId = str(char['player_id'])
        randomNumber = str(get_random_string())

        # Create account and get userid
        if accountCreated == False:
            response = requestApi(
                '/account/create', {'PlayerId': playerId, 'Server': server, 'CharName': charName, 'Password': randomNumber})
            _result = json.loads(response)
            userId = str(_result["charId"])
            randomPassword = str(randomNumber)
            secret = str(_result["token"])
            QtBind.setText(gui, lblCode, 'Char ID: <b>' + userId + '</b>')
            QtBind.setText(gui, lblPassword, 'Password: <b>' +
                           randomPassword + '</b> (Password will be hidden in 60 seconds)')
            QtBind.setText(
                gui, lblCodeDesc, 'You can log in to the mobile application with the above information. \nSave your password in a secure area. It will not be shown again')
            accountCreated = True
            saveAccount(server, charName, userId, secret)
            writeMessage('New account successfuly created. (' +
                         server + '/' + charName + ')')
            appRunning = True
        else:
            alreadyHave()

        toggleButtons()


# Reset and delete account
def reset_click():
    global accountCreated
    global appRunning
    char = get_character_data()
    os.remove('Plugins/SROMC_' + char['server'] + '_' + char['name'] + '.txt')
    writeMessage('Account successfuly deleted.')
    accountCreated = False
    appRunning = False
    toggleButtons()


# Already have account message
def alreadyHave():
    QtBind.setText(gui, lblCode, 'Char ID: <b>' + getUserId() + '</b>')
    QtBind.setText(
        gui, lblPassword, 'Password: XXXXXX <i>(If you forgot, reset and create new account)</i>')
    QtBind.setText(gui, lblCodeDesc,
                   'You have already created a user account.')

# Random password
def get_random_string():
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

# If account created before, get user id
def getUserId():
    char = get_character_data()
    try:
        lines = list(
            open('Plugins/SROMC_' + char['server'] + '_' + char['name'] + '.txt', 'r'))
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
        lines = list(
            open('Plugins/SROMC_' + char['server'] + '_' + char['name'] + '.txt', 'r'))
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
        lines = list(
            open('Plugins/SROMC_' + char['server'] + '_' + char['name'] + '.txt', 'r'))
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
    global deadCounter
    global itemCounter
    global rareItemCounter
    if t == 5:
       rareItemCounter += 1
    elif t == 4:
        log('Under attack by player')
    elif t == 6:
        itemCounter += 1
    elif t == 7:
        deadCounter += 1


# Test
def handle_joymax(opcode, data):
    if opcode == 0xB504:
        log(data)


# Messages
class Message:
    def __init__(self, message, player, type, typeInt, date):
        self.message = message
        self.player = player
        self.type = type
        self.typeInt = typeInt
        self.date = date
    def toDict(self):
      return {"message": self.message, "player": self.player, "type": self.type, "typeInt": self.typeInt, "date": self.date}


# Chat message received
def handle_chat(t, player, msg):
    global messages
    max_messages = 120
    message = str(msg)
    message = urllib.parse.quote(message)
    currentDate = datetime.now()
    type = str(messageType(t))
    sender = str(player)
    _m = Message(message, sender, type, t, currentDate.strftime("%d/%m/%Y %H:%M:%S"))
    messages.append(_m.toDict())
    if len(messages) > max_messages :
        messages.pop(len(messages) - max_messages - 1)


#Message type
def messageType(type):
    if type == 1:
        return "all"
    elif type == 2:
        return "private"
    elif type == 3:
        return "gm"
    elif type == 4:
        return "party"
    elif type == 5:
        return "guild"
    elif type == 6:
        return "global"
    elif type == 7:
        return "notice"
    elif type == 9:
        return "stall"
    elif type == 11:
        return "union"
    elif type == 16:
        return "academy"
    else:
        return "all"


# Send PM
def sendPM(message, to, player):
    if to == 'party':
        phBotChat.Party(message)
    elif to == 'guild':
        phBotChat.Guild(message)
    elif to == 'union':
        phBotChat.Union(message)
    elif to == 'stall':
        phBotChat.Stall(message)
    elif to == 'global':
        phBotChat.Global(message)
    elif to == 'private':
        phBotChat.Private(player, message)
    else:
        phBotChat.All(message)


# Event loop 500ms
def event_loop():
    global appRunning
    if isCharInGame() == True and accountCreatedBefore() == True:
        sendInfo()
        appRunning = True
    else:
        appRunning = False
        
        
def training_area():
    t = str(get_training_area())
    if t == "None":
        t = "{'x': 0, 'y': 0, 'z': 0, 'region': 24305, 'path': '', 'radius': 0, 'pick_radius': 0}"
    return t


# Send info to api
def sendInfo():
    global appRunning
    global apiRequests
    global taskCompleted
    global messages
    global deadCounter
    global itemCounter
    global rareItemCounter
    if ((appRunning == True) and (isCharInGame() == True)):
        char_data = get_character_data();
        char_data_str = str(char_data);
        char_data_str = char_data_str[:len(char_data_str)-1] + ", 'regionName':'" + get_zone_name(char_data['region']) + "', 'items': " + str(itemCounter) + ", 'rareItems': " + str(rareItemCounter) + ", 'trainingArea': " + str(training_area()) + ", 'dies': " + str(deadCounter) + " }"
        game = str(get_locale())
        status = str(get_status())
        char = char_data_str
        guild = str(get_guild())
        guild_union = str(get_guild_union())
        party = str(get_party())
        inventory = str(get_inventory())
        storage = str(get_storage())
        storage_guild = str(get_guild_storage())
        academy = str(get_academy())
        pets = str(get_pets())
        players = str(get_players())
        taxi = str(get_taxi())
        monsters = str(get_monsters())
        drops = str(get_drops())
        quests = str(get_quests())
        skills = str(get_active_skills())
        token = str(getToken())
        user_id = str(getUserId())
        _messages = str(messages)
        requestJson = {
            'charId': user_id,
            'token': token,
            'status': status,
            'game': game,
            'character': char,
            'inventory': inventory,
            'storage': storage,
            'storage_guild': storage_guild,
            'quests': quests,
            'drops': drops,
            'guild': guild,
            'guild_union': guild_union,
            'party': party,
            'taxi': taxi,
            'monsters': monsters,
            'pets': pets,
            'skills': skills,
            'players': players,
            'academy': academy,
            'messages': _messages,
            'taskCompleted': str(taskCompleted)
        }

        toggleButtons()
        apiRequests += 1
        if apiRequests % 5 == 0:
            try:
                response = requestApi('/charinfo/create', requestJson)
                hasTask = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
                tasks = str(hasTask.tasks.command)
                if tasks == "start_bot":
                    start_bot()
                    writeMessage("Task > Bot start")
                elif tasks == "stop_bot":
                    stop_bot()
                    writeMessage("Task > Bot stop")
                elif tasks == "set_training_radius":
                    set_training_radius(float(hasTask.tasks.arg1))
                    writeMessage("Task > Set training radius")
                elif tasks == "set_training_position":
                    set_training_position(0, float(hasTask.tasks.arg1), float(hasTask.tasks.arg2), float(hasTask.tasks.arg3))
                    writeMessage("Task > Set training position")
                elif tasks == "start_trace":
                    start_trace(str(hasTask.tasks.arg1))
                    writeMessage("Task > Start tracing (" + str(hasTask.tasks.arg1) + ")")
                elif tasks == "start_script":
                    start_script(str(hasTask.tasks.arg1))
                    writeMessage("Task > Start script")
                elif tasks == "stop_script":
                    stop_script()
                    writeMessage("Task > Stop script")
                elif tasks == "stop_trace":
                    stop_trace()
                    writeMessage("Task > Stop tracing")
                elif tasks == "send_global":
                    sendPM(str(hasTask.tasks.arg1), 'global', '')
                    writeMessage("Task > Sent global message")
                elif tasks == "guild_invite":
                    isSuccess = phBotChat.Private(str(hasTask.tasks.arg1), str(hasTask.tasks.arg2))
                    data = b'\x08\x00'
                    for c in str(hasTask.tasks.arg1):
                        data += struct.pack('b', ord(c))
                    if isSuccess:
                        inject_joymax(0x70F3, data, False)
                        writeMessage("Task > Invite guild")
                elif tasks == "guild_kick":
                    isSuccess = phBotChat.Private(str(hasTask.tasks.arg1), str(hasTask.tasks.arg2))
                    data = b'\x08\x00'
                    for c in str(hasTask.tasks.arg1):
                        data += struct.pack('b', ord(c))
                    if isSuccess:
                        inject_joymax(0x70F4, data, False)
                        writeMessage("Task > Kick from guild")
                elif tasks == "leave_party":
                    if get_party():
                        inject_joymax(0x7061, b'', False)
                        writeMessage("Task > Leave from party")
                elif tasks == "move_to":
                    move_to(float(hasTask.tasks.arg1), float(hasTask.tasks.arg2), 0)
                    writeMessage("Task > Moving target X and Y")
                elif tasks == "send_message":
                    sendPM(str(hasTask.tasks.arg1), str(hasTask.tasks.arg2), str(hasTask.tasks.arg3))
                    if str(hasTask.tasks.arg2) == "private":
                        charName = str(char_data['name'])
                        toCharName = str(hasTask.tasks.arg3)
                        message = str(hasTask.tasks.arg1)
                        message = urllib.parse.quote(message)
                        currentDate = datetime.now()
                        _m = Message(str(message), charName + "|" + toCharName, str("private"), 2, currentDate.strftime("%d/%m/%Y %H:%M:%S"))
                        messages.append(_m.toDict())
                    writeMessage("Task > Message sent. (" + hasTask.tasks.arg2 + ")")
                elif tasks == "reverse_return":
                    reverse_return(int(hasTask.tasks.arg1), str(hasTask.tasks.arg2))
                    writeMessage("Task > Reverse scroll")
                elif tasks == "disconnect":
                    disconnect()
                    writeMessage("Task > Disconnect from server")

                if tasks != "":
                    taskCompleted = True
                else:
                    taskCompleted = False
            except Exception as e:
                writeMessage('API Error.' + str(e))

            if apiRequests >= 60:
                alreadyHave()
                writeMessage('Data sent and received (' + user_id + ')')
                apiRequests = 0


# Disconnected from game
def disconnected():
    global appRunning
    appRunning = False
    writeMessage('Disconnected from game')
    

# Finished
def finished():
    global appRunning
    appRunning = False
    writeMessage('Exit from SROMC')


# Request API
def requestApi(path, _data):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    data = json.dumps(_data).encode("utf-8")
    req = urllib.request.Request(apiEndpoint + path, data, headers)
    with urllib.request.urlopen(req) as f:
        res = f.read()
    return res


# Connected to game
def joined_game():
    global appRunning
    appRunning = True
    writeMessage('Connected to game')


# Write message
def writeMessage(message):
    log('[' + appName + '] : ' + message)


# First load check char has account
def start():
    global appRunning
    if accountCreatedBefore() == True:
        appRunning = True
        alreadyHave()
    else:
        appRunning = False


# Get .db3 file for game locale
def getDBFile():
    bot_path = os.getcwd()
    locale = get_locale()
    if locale == 56:
        return bot_path + "/Data/TRSRO.db3"
    

# Toggle buttons on click
def toggleButtons():
    if accountCreatedBefore() == True:
        QtBind.move(gui, btnCreate, 10, -70)
        QtBind.move(gui, btnReset, 10, 70)
    else:
        QtBind.move(gui, btnCreate, 10, 70)
        QtBind.move(gui, btnReset, 10, -70)
        QtBind.setText(gui, lblCode, '')
        QtBind.setText(gui, lblPassword, '')
        QtBind.setText(gui, lblCodeDesc, '')


start()
toggleButtons()

# WARNING
# If you want to edit this code, read carefully. 
# There are some limits we set for storing data. 
# If you make any changes above these limits, your character will be banned from the system and you will not be able to use it again.
