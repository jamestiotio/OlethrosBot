# Olethros Bot [![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/?repository=https://github.com/jamestiotio/OlethrosBot)

**Made with ❤️ by @jamestiotio**

Olethros Bot is a utility bot that provides multiple functions for the purposes of SUTD Class 19F07 Telegram Group.

This bot is deployed on Microsoft Azure as a Flask Web App (in a Linux Docker Container) under its App Services (I'm using my `Azure for Students` free subscription).

## Settings

- Operating System: Debian 9
- Runtime Stack: Python 3.7
- Deployment Method (`ScmType`): `LocalGit` (for Kudu Build Server)
- Startup Command: `gunicorn --bind=0.0.0.0 --timeout 0 application:app`
- HTTP Version: 2.0
- HTTPS Only: On
- Minimum TLS Version: 1.2
- Application Settings:
  ``` json
  [
  {
    "name": "ADMIN_LIST",
    "value": "[]",
    "slotSetting": false
  },
  {
    "name": "BOT_TOKEN",
    "value": "<id>:<token>",
    "slotSetting": false
  },
  {
    "name": "EMAIL",
    "value": "",
    "slotSetting": false
  },
  {
    "name": "main_chat",
    "value": "-1",
    "slotSetting": false
  },
  {
    "name": "MONGODB_ATLAS_CONNECTION_STRING",
    "value": "mongodb+srv://<username>:<password>@<app-name>.azure.mongodb.net/<database>?retryWrites=true&w=majority",
    "slotSetting": false
  },
  {
    "name": "private_chat",
    "value": "0",
    "slotSetting": false
  },
  {
    "name": "WEBHOOK_URL",
    "value": "",
    "slotSetting": false
  },
  {
    "name": "WEBSITE_HTTPLOGGING_RETENTION_DAYS",
    "value": "30",
    "slotSetting": false
  },
  {
    "name": "WEBSITE_TIME_ZONE",
    "value": "Asia/Singapore",
    "slotSetting": false
  }
  ]
  ```

MongoDB Atlas schema is coming soon.

Reminder to set your commit credentials (username and password) for deployment authentication purposes.

You can import a local `.json` file to a MongoDB Atlas collection by running: `mongoimport --host <replSetName>/<hostname1><:port>,<hostname2><:port>,<hostname3><:port>,<...> --ssl --username <USERNAME> --password <PASSWORD> --authenticationDatabase <DBNAME> --db <DATABASE> --collection <COLLECTION> --type json --file <FILENAME>.json --jsonArray`.

The `cert.pem` and `key.pem` files are required for the upcoming webhook implementation as I will be using a self-signed SSL certificate.

After successful deployment, start the web app (if it is not yet started) and run the bot by going to `https://<app-name>.azurewebsites.net/<bot-token>`. It should return an `OK`. The purpose of putting `<bot-token>` there is to prevent anyone else from just running the bot as and when they like it. This is also to prevent exposing too much obvious endpoints of the bot to the Internet for security purposes. After running the bot, **do not** go to the homepage (`https://<app-name>.azurewebsites.net/`) as it will disable the bot. Alternatively, you can disable the homepage route entirely.

NOTE: If the bot sleeps after a few hours without any HTTP requests (even with the `Always On` setting enabled), use [Uptime Robot](https://uptimerobot.com/) to schedule a free HTTP request at a regular interval (I used a 1-hour interval).



## Functions
Currently, these are the available functions of this bot:

### Birthday Tracking
Start tracking using the `/track` command.

### Feel-good Message
Send a feel-good message by using the `/feelgood` command.

### Dice Roller
Credit to [@treetrnk](https://github.com/treetrnk/rollem-telegram-bot) for this feature. Roll dices using the `/roll <args>`, `/r <args>` or `/rf [<args>]` commands.
Please follow the proper <a href="https://en.wikipedia.org/wiki/Dice_notation">dice notation</a>.

### Code Tester
Credit to [@veetaw](https://github.com/veetaw/rextester) and [@GingerPlusPlus](https://github.com/GingerPlusPlus/Rextester-bot-v3) for this feature. Execute snippets of code of various programming languages by using the `/run <language> <code> [\stdin <stdin>]` command.
Might be useful for SUTD 10.009 Digital World.



## Upcoming Features

### User Message Frequency
Generate an Excel sheet with a table and a pie chart of the Telegram group's message frequency from the group members. The `openpyxl` library would be needed.

### Reminder
Set and (auto-)delete reminders for each school day or in a specified timing. An Azure-based MongoDB Atlas database was established for this particular function. Add your Azure App's Outbound IP Addresses to MongoDB Atlas' IP Whitelist. To set a reminder, use the `/remindme <time> <"to"/"that"> <reminder-text>` command.

### Internal Voting System
Establish a voting system internally within the group so as to not depend on an external voting bot such as [@countmeinbot](https://t.me/countmeinbot).

### Karma Credit System
Implement a karma credit system (similar to a social credit system) using upvotes and downvotes (similar to Reddit) or possibly, through the use of designated stickers. A karma leaderboard can be displayed if requested. Extra care needs to be taken for this system to not go horribly wrong as it might lead to the destruction of some friendships.
