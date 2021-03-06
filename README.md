# SROMC - phBot Plugin

![SROMC](https://i.ibb.co/whJr5wD/banner.png)

SROMC carries all the necessary data about your character to your mobile phone. You can also use simple bot functions.

## Features

- Multiple character management
- General character status, current position on the map, active skills.
- Party, guild, union, private, global messages. Instant messaging
- Instant taxi status if you are taxiing.
- Easily view character inventory, storage, guild storage and picker pet items
- View members of academy
- Party and taxi information. Party leave function
- Guild and Union information. View online members.
- Easily track your quests.
- View your pets.
- Quickly send commands to phBot.
  - Start/stop bot
  - Adjust training area size
  - Adjust the training area position
  - Trace/untrace player
  - Move to the desired location
  - Quickly use Reverse Scroll (last death location, last used location and nearby party member)
  - Set custom script and start/stop
  - Send global messages
  - Disconnect game
- Everything in one file. It doesn't need any extra library.


## App Images

#1 | #2 | #3
--- | --- | --- 
![SROMC](https://i.ibb.co/bRfwtqs/1.png) | ![SROMC](https://i.ibb.co/vwnBvBL/2.png) | ![SROMC](https://i.ibb.co/tMHPs6j/3.png)

#4 | #5 | #6
--- | --- | --- 
![SROMC](https://i.ibb.co/2nnXLh2/4.png) | ![SROMC](https://i.ibb.co/jLGDvny/5.png) | ![SROMC](https://i.ibb.co/xfN35rb/6.png)

## Installation

**Step [1]**

[Download SROMC plugin](https://github.com/ilkerccom/sromc-plugin) file from Github.

[Download Android App](https://play.google.com/store/apps/details?id=com.sromc) or [Download iOS App](https://apps.apple.com/tr/app/sromc/id1608640199) from store.


<a href="https://play.google.com/store/apps/details?id=com.sromc"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Google_Play_Store_badge_EN.svg/2560px-Google_Play_Store_badge_EN.svg.png" width="200"/></a> | <a href="https://apps.apple.com/tr/app/sromc/id1608640199"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Download_on_the_App_Store_Badge.svg/2560px-Download_on_the_App_Store_Badge.svg.png" width="200"/></a>

**Step [2]**

Copy the plugin file (SROMCv0-9-4.py) to the folder specified below.

``` C:\Users\{YOUR_USER_NAME}\AppData\Local\Programs\phBot Testing\Plugins ```

**Step [3]**

In the phBot app, go to the **"Plugins"** section and the **"Reload"** button.

**Step [4]**

Switch to the tab named SROMC. Click the **"Create Character"** button. This will create a simple account for your character on the server.

**Step [5]**

**"Character ID"** and **"Password"** will appear on the screen. Enter this information on the **"Add Character"** screen in the **mobile app** (iOS or Android).

**That's all**

Now your character will be paired with the mobile application.

## Mobile App Hits

**Map:** If you hold down on a certain point on the map, your character will move to that point. The white circle on the map indicates the size of the training area radius.

**Messages:** To send someone a private message, just click on it. You can edit the player name to which the message will go, by clicking on it.

**Actions:** Allow 3-5 seconds for a command you sent to reflect in the game. To teleport to a party member, you need to be at a party. The "Disconnect game" command requires an extra confirmation. When you use this command, if your "Manager" settings have been made, the character will re-enter the game in 2-3 minutes.


## Notes

- If you are having trouble retrieving character data, use **"Reset and Stop"** in the plugin screen. This will change the character password and token information again. In this case, **you don't need** to match your character again.
- If your character **does not send data to the server for 5 minutes**; There will be "No connection" information in the mobile application. In this case, you may not see the character information in the mobile application.
- Each character can be matched with only one mobile app account.
- Message data is cleared each time the character enters the game.
- Create an issue for the problems and issues you are experiencing. You can also create an issue for the new features you want.
- Always download the latest version of the plugin from Github (https://github.com/ilkerccom/sromc-plugin). Also get the mobile apps from the store. We never share ".apk" style app installer files.
- **Please keep it in mind; sensitive data such as character login information is _never sent_ to the server. _Do not share_ the files created by the plugin, "Char ID", "Char Pass" and "Token" information with anyone.**

## Donate

The plugin and the mobile application are completely free. It also contains no ads. If you like it, you can support the project with a donation.

**Donate with Bitcoin (BTC)**

    1eosEvvesKV6C2ka4RDNZhmepm1TLFBtw
