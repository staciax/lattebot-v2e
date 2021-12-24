# Standard 
import discord
import os
import datetime
import asyncio
from discord.ext import commands
from os import environ
from os.path import join, dirname
from typing import Union, List, Optional
from datetime import datetime

# Third party
from dotenv import load_dotenv
import motor.motor_asyncio
import asyncpg
import aiohttp

# Local
from utils.json_loader import read_json
from utils.mongo import Document

#json_loader
data = read_json('bot_var')

dotenv_path = join(dirname(__file__), 'data/settings.env')
load_dotenv(dotenv_path)

async def get_prefix(bot, message):
    prefix = 're'
    if message.guild.id == bot.latte_guild_id:
        prefix = '.'
    return commands.when_mentioned_or(prefix)(bot,message)

class LatteBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.bot_version = '0.0.1s'
        self.last_update = [2021, 12, 23]
        self.launch_time = datetime.utcnow()
        self.latte_avtivity = 'mirror ♡ ₊˚'
        self.tester = ''
        self.github = 'https://github.com/staciax'
        self.defaul_prefix = 're'
        self.blacklist = {}
        self.afk_user = {}
        self.sniped = {}
        self.sniped_embed = {}
        self.sleeping = {}
        self.reminding = {}
        self.channel_sleep = {}
        self.current_streamers = list()
        self.no_prefix = False
        self.latte_guild_id = 840379510704046151
        self.latte_sup_guild_id = 887274968012955679
        self.latte_log_id = 909301335743143946
        self.latte_starbot_id = 909485607359758337
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
    
    @property
    def latte(self) -> Optional[discord.Guild]:
        """Returns discord.Guild of the owner guild"""
        return self.get_guild(self.latte_guild_id)
    
    #thank_stella_bot
    def get_command_signature(self, ctx, command_name: Union[commands.Command, str]) -> str:
        if isinstance(command_name, str):
            if not (command := self.get_command(command_name)):
                raise Exception("Command does not exist for signature.")
        else:
            command = command_name
        return self.help_command.get_command_signature(command, ctx)
    
    async def start(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)
    
    async def close(self):
        await self.session.close()
        await super().close() 
            
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
),help_command = None, case_insensitive = True, owner_id=240059262297047041) #slash_commands = True, slash_command_guilds=[840379510704046151]
 
# botdata = {
#     "token": "this token",
#     "color": 0xffcccb,
# }
# a = testing(**botdata)

@bot.event
async def on_ready():
    # await bot.http.bulk_upsert_guild_commands(bot.application_id, 840379510704046151, [])
    # await bot.http.bulk_upsert_global_commands(bot.application_id, [])
    bot_avtivity = bot.latte_avtivity
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=bot_avtivity
    ))
    print(f"\nName : {bot.user}\nActivity : {bot_avtivity}\nServers : {len(bot.guilds)}\nUsers : {len(set(bot.get_all_members()))}")
    print("\nCog loaded\n---------\n")

async def create_db_pool():
    if not bot.tester or len(bot.tester) == 0:
        bot.pg_con = await asyncpg.create_pool(host=data['dbhost'], user=data['dbuser'], password=data['dbpassword'], database=data['database'], min_size=1, max_size=5)
        print("Connected to PostgreSQL")

async def run_once_when_ready():
    await bot.wait_until_ready()
    if not bot.tester or len(bot.tester) == 0:
        banuser = await bot.pg_con.fetch("SELECT user_id, is_blacklisted FROM public.blacklist;")
        for value in banuser:
            bot.blacklist[value['user_id']] = (value['is_blacklisted'] or False)
        print("\nBlacklist database loaded")

class Blacklisted_user(commands.CheckFailure):
    pass

@bot.check
def blacklist(ctx):
    if not bot.tester or len(bot.tester) == 0:
        try:
            is_blacklisted = bot.blacklist[ctx.author.id]
        except KeyError:
            is_blacklisted = False
        
        if ctx.author.id == bot.owner_id:
            is_blacklisted = False
        
        if is_blacklisted is False:
            return True
        else:
            raise Blacklisted_user
    return True

# @bot.check
# async def blacklist(ctx):
#     if ctx.author.id in blacklisted:
#         return False # or raise an error
#     return True

bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

if __name__ == "__main__":
    
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.mongo_url))

    #db_tag
    bot.latte_db = bot.mongo["latteonly"]
    bot.latte_tags = Document(bot.latte_db, "tags")
    bot.latte_todo = Document(bot.latte_db, "todo")
    bot.latte_stars = Document(bot.latte_db, "stars")

    #db_testing
    bot.db_ping = bot.mongo["lattebot"]
    bot.latte_ping = Document(bot.db_ping, "latency")

    #db_leveling
    bot.db_level = bot.mongo["discord"]
    bot.latte_level = Document(bot.db_level, "levelling")
    
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f'cogs.{file[:-3]}')
    
    bot.loop.run_until_complete(create_db_pool())
    bot.loop.create_task(run_once_when_ready())
    bot.run(bot.token)