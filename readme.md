# Requirements

* Create an application on Discord's developer portal: https://discordapp.com/developers/applications/
* Get credentials for usage of the google sheets API either by clicking the big blue button in this page https://developers.google.com/sheets/api/quickstart/python or at https://console.developers.google.com/. You should end up with a credentials.json file in the same directory
* Install pip (python packet manager) and run `pip install -U google-api-python-client google-auth-httplib2 google-auth-oauthlib discord.py`

# Setup

* Add the bot to your server using the link created at the discord dev page for the app, under OAuth2 submenu
* Modify config.py to your liking
* Create a secrets.py file with the content:

```
BOT_TOKEN = <your bot token here, as a string. for example "AabB123...">
SPREADSHEET_IDS = <your spreadsheet ids here, as a list of strings, for example ["AabB123...","CabB123..."]>
```

* Spreadsheet IDs can be found in the url. Bot token in the discord dev page.

# Run

python ./keyboy.py

# Usage

React with a key emoji (or whichever you set up in cofig) to a message in the keybeg channel to automatically send that user a key. 
* If the delivery is successful the bot will react with a thumbs up, and log the result in the logs channel
* In case of failure the bot may reply in the channel to the user if they have dms blocked or left the server, and laso log the result in the logs channel

Use !reload in the commands channel to reload keys during runtime.
