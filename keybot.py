#pip install -U google-api-python-client google-auth-httplib2 google-auth-oauthlib discord.py
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import discord
from config import *
from secrets import *
import logging

#Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class MyClient(discord.Client):

    def __init__(self):
        super().__init__(fetch_offline_members=True,activity=discord.Activity(name=ACTIVITY,type=discord.ActivityType.playing))
        self.loginToSheet()
        self.loadKeys()
        self.keyChannel = None
        self.logChannel = None
        self.commandsChannel = None
        print(MSG_LOADED_DATA.format(len(self.availableKeys), len(self.hasKey)))

    #Method for logging things both to console and to a channel
    async def log(self, message):
        logger.info(message)
        return await self.logChannel.send(message)

    #Overload. See discord.py's Client documentation
    async def on_ready(self):
        print(MSG_FINISHED_LOADING.format(self.user))
        self.keyChannel = self.get_channel(KEYBEG_CH_ID)
        self.logChannel = self.get_channel(LOG_CH_ID)
        self.commandsChannel = self.get_channel(COMMAND_CH_ID)

    #Overload. See discord.py's Client documentation
    async def on_message(self, message):
        if message.channel.id != COMMAND_CH_ID:
            return
        if message.content == RELOAD_COMMAND:
            self.loadKeys()
            logger.info(MSG_LOADED_DATA.format(len(self.availableKeys), len(self.hasKey)))
            await self.commandsChannel.send(MSG_LOADED_DATA.format(len(self.availableKeys), len(self.hasKey)))

    #Overload. See discord.py's Client documentation
    #payload members: message_id, user_id, channel_id, guild_id, emoji
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != KEYBEG_CH_ID:
            return
        message = await self.keyChannel.fetch_message(payload.message_id)
        if message == None:
            await self.log(MSG_FETCH_ERROR.format(payload.message_id))
            return
        author = message.author
        authorName = "{0}#{1}".format(message.author.name,message.author.discriminator)
        if len(self.hasKey) <= 0:
            await self.log(MSG_LOG_OUT_OF_KEYS.format(authorName))
            return
        #any(map(lambda role : role.id == 573412970449600542, user.roles)) #If we needed to check specific roles of reacters later
        hasKeyReaction = False
        for reaction in message.reactions:
            if reaction.emoji == KEY_EMOJI and reaction.count == 1:
                hasKeyReaction = True
                break
        if hasKeyReaction and authorName not in self.hasKey:
            self.hasKey.add(authorName)
            key = self.availableKeys.pop(0)
            self.deliveredKey[authorName] = key
            try:
                await author.send(MSG_BOT_DM.format(key))
                self.writeRow(self.keyLookup[key][1], self.keyLookup[key][0], authorName)
                logPromise = self.log(MSG_LOG_DELIVERY_SUCCESS.format(key, authorName, len(self.availableKeys)) )
                await message.add_reaction(OK_EMOJI)
                await logPromise
            except discord.HTTPException as error:
                self.availableKeys.insert(0,key)
                self.deliveredKey.pop(authorName)
                self.hasKey.remove(authorName)
                logPromise = self.log(MSG_LOG_DELIVERY_FAILURE.format(key, authorName, error.text) )
                await self.keyChannel.send(MSG_CHANNEL_PING.format(author.mention) )
                await logPromise

    # Logs into the sheets api and assigns the service to self.sheetService
    def loginToSheet(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)
        self.sheetService = service.spreadsheets()

    #Loads or relaoads all the keys and users from the sheets
    def loadKeys(self):
        self.hasKey = set() #Set of usernames#discriminators
        self.deliveredKey = {} #Dictionary 
        self.availableKeys = [] #List of keys up for grabs
        self.keyLookup = {} #Dictionary of [key] = (id, row)
        hasKey = set()
        availableKeys = []
        keyLookup = {}
        for sheetID in SPREADSHEET_IDS:
            self.fetchKeysFromSheet(sheetID, SPREADSHEET_RANGE)

    #Hits the google sheet through the previously set service and fetches the columns
    #Starts at row 2 to and expects keys on column A, usernames on column B
    #Loads things into the members previously defined in loadkeys
    def fetchKeysFromSheet(self,sheetID, range):
        result = self.sheetService.values().get(spreadsheetId=sheetID,range=range).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            exit(1)
        else:
            counter = 1
            for row in values:
                counter += 1
                key = row[0]
                if key.startswith("//"):
                    continue
                if len(row) > 1:
                    user = row[1]
                    self.hasKey.add(user)
                else:
                    self.availableKeys.append(key)
                self.keyLookup[key] = (sheetID,counter)

    #Writes a value to the cell in the row, column is preset
    def writeRow(self, rowNumber, sheetID, userName):
        self.sheetService.values().update(spreadsheetId=sheetID,range=SPREADSHEET_WRITE_RANGE.format(rowNumber),body={ "values" : [[userName]] },valueInputOption="RAW").execute()

if __name__ == '__main__':
    client = MyClient()
    client.run(BOT_TOKEN)

