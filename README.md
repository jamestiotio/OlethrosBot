# Olethros Bot [![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/?repository=https://github.com/jamestiotio/OlethrosBot)

**Made with ❤️ by @jamestiotio**

Olethros Bot is a utility bot that provides multiple functions for the purposes of SUTD Class 19F07 Telegram Group.

This bot is deployed on Microsoft Azure as a Flask Web App under its App Services (I'm using my `Azure for Students` free subscription).

## Settings

- Operating System: Debian 9
- Runtime Stack: Python 3.7
- Deployment Method (`ScmType`): `LocalGit`
- Startup Command: `gunicorn --bind=0.0.0.0 --timeout 0 application:app`
- HTTP Version: 2.0
- HTTPS Only: On
- Minimum TLS Version: 1.2

Reminder to set your commit credentials (username and password) for deployment authentication purposes.

Additionally, you will need to configure your `botinfo.py` and `class_list.json` files properly. (The `cert.pem` and `key.pem` files are required for the upcoming webhook implementation as I will be using a self-signed certificate.)



## Functions
Currently, these are the available functions of this bot:

### Birthday Tracking
Start tracking using the `/track` command.

### Feel-good Message
Send a feel-good message by using the `/feelgood` command.

### Dice Roller
Credit to [@treetrnk](https://github.com/treetrnk/rollem-telegram-bot) for this feature. Roll dices using `/roll`, `/r` or `/rf` commands.
Please follow the proper <a href="https://en.wikipedia.org/wiki/Dice_notation">dice notation</a>.



## Upcoming Features

### User Message Frequency
Generate an Excel sheet with a table and a pie chart of the Telegram group's message frequency from the group members. The `openpyxl` library would be needed.

### Reminder
Set and (auto-)delete reminders for each school day.

### Internal Voting System
Establish a voting system internally within the group so as to not use an external voting bot such as [@countmeinbot](https://t.me/countmeinbot).

### Code Tester
Execute snippets of code. Might be useful for SUTD 10.009 Digital World.