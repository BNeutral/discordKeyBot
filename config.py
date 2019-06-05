import logging

#LOG
LOG_LEVEL = logging.INFO
LOG_FILE = "keybot.log"

#Channels
KEYBEG_CH_ID = 573062057570861057 #testing channel
LOG_CH_ID = 573404505215991828 #testing channel
COMMAND_CH_ID = 575254643399983106 #testing channel
#KEYBEG_CH_ID = 219137754271973376
#LOG_CH_ID = 335866186787192833
#COMMAND_CH_ID = 335873079714512907

#Commands
RELOAD_COMMAND = "!reload"

#Emojis
KEY_EMOJI =	u"\U0001F511" #🔑
OK_EMOJI = u"\U0001F44D" #👍
ACTIVITY = "Solomon's Key"

#Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # If modifying these scopes, delete the file token.pickle.
SPREADSHEET_RANGE = 'Sheet1!A2:B'
SPREADSHEET_WRITE_RANGE = 'Sheet1!B{0}'

#Messages
MSG_LOADED_DATA = "Keys loaded: {0} - Users loaded: {1}" #Console message shown after data is loaded
MSG_FINISHED_LOADING = "Logged on as {0}!" #Console message shown when the bot is ready to work
MSG_FETCH_ERROR = "Error fetching message with id {0}" #Console message shown when there's a failure fetching a message
MSG_BOT_DM = "Here's your Steam key for the Steambirds Alliance beta: {0}\nServers are open during the weekends, check <#313809774217265152> for more info.\nWe would be really grateful if you posted your first impressions or any feedback you have in <#448185713746247680> in the SBA server. If you have any friends that tried the game but didn't like it, please let us know what their complaints were too.\nThis is a bot, so if you have any further questions feel free to ask on the server or send a direct message to a mod." #Message sent to users
MSG_LOG_OUT_OF_KEYS = "Couldn't deliver a key to {0}. We ran out of keys!" #Log message for when we run out of keys
MSG_LOG_DELIVERY_SUCCESS = "Delivered key {0} to {1}. Remaining keys loaded: {2}" #Log message for when a key is successfully delivered
MSG_LOG_DELIVERY_FAILURE = "Failed to deliver key {0} to {1}. Error: {2}" #Log message for when a key fails to deliver
MSG_CHANNEL_PING = "We failed to send you a key {0}. Are you still on the server and have direct messages enabled? Please check your settings and post again in this channel." #Message posted on the channel after a key fails to deliver