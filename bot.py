# Standard 
import discord
import os
import datetime
from discord.ext import commands
from os import environ
from os.path import join, dirname
from typing import Union, List, Optional
from datetime import datetime

# Third party
from dotenv import load_dotenv
import motor.motor_asyncio

# Local
from utils.json_loader import latte_read, read_json , write_json
from utils.mongo import Document

#json_loader
data = read_json('bot_var')

dotenv_path = join(dirname(__file__), 'data/settings.env')
load_dotenv(dotenv_path)

async def get_prefix(bot, message):
    if message.guild.id == 840379510704046151:
        prefix = '.'
    else:
        prefix = 're'
    return commands.when_mentioned_or(prefix)(bot,message)

class LatteBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.bot_version = "0.0.3s.fix1"
        self.last_update = [2021, 11, 10]
        self.launch_time = datetime.utcnow()
        self.tester = ''
        self.github = "https://github.com/staciax"
        self.defaul_prefix = 're'
        self.blacklisted_users = []
        self.afk_user = {}
        self.sniped = {}
        self.sniped_embed = {}
        self.sleeping = {}
        self.reminding = {}
        self.channel_sleep = {}
        self.current_streamers = list()
        self.no_prefix = False
        self.latte_id = 887274968012955679
        self.latte_guild_id = 840379510704046151
        self.latte_sup_guild_id = 887274968012955679
        self.latte_invite_url = os.getenv('LATTE_URL', None)
        self.latte_supprt_url = os.getenv('SUPPORT_URL', None)
        self.new_members = {}
        self.bot_join = 893695417320087573
        self.bot_leave = 893695447309369345
        self.white_color = 0xffffff
        self.error_color = 0xFF7878
        self.token = data["token"]
        self.mongo_url = data["mongo"]
        super().__init__(command_prefix=get_prefix, *args, **kwargs)
    
    @property
    def renly(self) -> Optional[discord.User]:
        """Returns discord.User of the owner"""
        return self.get_user(self.owner_id)

    #thank_stella_bot
    def get_command_signature(self, ctx, command_name: Union[commands.Command, str]) -> str:
        if isinstance(command_name, str):
            if not (command := self.get_command(command_name)):
                raise Exception("Command does not exist for signature.")
        else:
            command = command_name
        #return self.help_command.get_command_signature(command)
        return self.help_command.get_command_signature(command, ctx)
        
bot = LatteBot(intents=discord.Intents(
    guild_reactions=True,  # reaction add/remove/clear
    guild_messages=True,  # message create/update/delete
    guilds=True,  # guild/channel join/remove/update
    integrations=True,  # integrations update
    voice_states=True,  # voice state update
    dm_reactions=True,  # reaction add/remove/clear
    guild_typing=True,  # on typing
    dm_messages=True,  # message create/update/delete
    presences=True,  # member/user update for games/activities
    dm_typing=True,  # on typing
    webhooks=True,  # webhook update
    members=True,  # member join/remove/update
    invites=True,  # invite create/delete
    emojis=True,  # emoji update
    bans=True  # member ban/unban
),help_command = None, case_insensitive = True , slash_commands = True, owner_id=240059262297047041) #, slash_command_guilds=[840379510704046151]
 
# botdata = {
#     "token": "this token",
#     "color": 0xffcccb,
#     "wtf": "testing",
# }
# a = testing(**botdata)

@bot.event
async def on_ready():
    # await bot.http.bulk_upsert_guild_commands(bot.application_id, 840379510704046151, [])
    # await bot.http.bulk_upsert_global_commands(bot.application_id, [])
    bot_avtivity = "with my friends ♡ ₊˚"
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=bot_avtivity
    ))
    print(f"\nName : {bot.user}\nActivity : {bot_avtivity}\nServers : {len(bot.guilds)}\nUsers : {len(set(bot.get_all_members()))}")
    print("\nCog loaded\n---------\n")

#bot.load_extension('jishaku')

if __name__ == "__main__":
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.mongo_url))

    #db_tag
    bot.latte_db = bot.mongo["latteonly"]
    bot.latte_tags = Document(bot.latte_db, "tags")

    #db_testing
    bot.db_ping = bot.mongo["lattebot"]
    bot.latte_ping = Document(bot.db_ping, "latency")

    #db_leveling
    bot.db_level = bot.mongo["discord"]
    bot.latte_level = Document(bot.db_level, "levelling")
    
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f'cogs.{file[:-3]}')
    
    bot.run(bot.token)