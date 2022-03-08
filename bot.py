# Standard 
import discord
import os
import datetime
import asyncio
from discord.ext import commands, tasks
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
from utils.errors import Blacklisted_user
from utils.latte_converter import LatteVerifyView, LatteSupportVerifyView
from utils_valorant.useful import *

#json_loader
data = read_json('bot_var')

#env_loader
dotenv_path = join(dirname(__file__), 'data/secrets/settings.env')
load_dotenv(dotenv_path)

#get_prefix
async def get_prefix(bot, message):
    prefix = 're'
    if message.guild.id in [bot.latte.id, 937967814889848853, 949987281505255454]:
        prefix = '.'
    return commands.when_mentioned_or(prefix)(bot,message)

class LatteBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.bot_version = '1.0.0a'
        self.last_update = [2022, 2, 11]
        self.launch_time = datetime.utcnow()
        self.latte_avtivity = 'nyanpasu ♡ ₊˚'
        # self.allowed_mentions = discord.AllowedMentions.none()

        # Bot based stuff
        self.latte_guild_id = 840379510704046151
        self.latte_sup_guild_id = 887274968012955679
        self.latte_log_id = 941514797571256360
        self.latte_starbot_id = 909485607359758337
        self.latte_invite_url = os.getenv('LATTE_URL', None)
        self.latte_supprt_url = os.getenv('SUPPORT_URL', None)
        self.bot_join = 943379664280387646
        self.bot_leave = 943379695033016380
        self.white_color = 0xffffff
        self.error_color = 0xFF7878
        self.token = data["token"]
        self.mongo_url = data["mongo"]

        # Cache stuff
        self.blacklist = {}
        self.afk_user = {}
        self.sniped = {}
        self.sniped_embed = {}
        self.sleeping = {}
        self.reminding = {}
        self.channel_sleep = {}
        self.current_streamers = list()
        self.latte_invite_code = {}
        self.no_prefix = False

        # events stuff
        self.auto_kick_user = {}
        self.auto_kick = False

        # Extra stuff
        self.tester = ''
        self.github = 'https://github.com/staciax'
        self.defaul_prefix = 're'
        self.format_version = 1

        super().__init__(command_prefix=get_prefix, *args, **kwargs)
        # Bot view
        self.latte_verify_view = False
        self.latte_support_view = False

    @property
    def renly(self) -> Optional[discord.User]:
        """Returns discord.User of the owner"""
        return self.get_user(self.owner_id)
    
    @property
    def latte(self) -> Optional[discord.Guild]:
        """Returns discord.Guild of the owner guild"""
        return self.get_guild(self.latte_guild_id)
    
    @property
    def latte_support(self) -> Optional[discord.Guild]:
        """Returns discord.Guild of the owner guild"""
        return self.get_guild(self.latte_sup_guild_id)
    
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
        
    async def on_ready(self):
        if not get_version.is_running():
            get_version.start()

        if not self.latte_verify_view:
            print('LatteVerify is ready')
            self.add_view(LatteVerifyView(self))
            self.latte_verify_view = True
        
        if not self.latte_support_view:
            print('LatteSupport is ready')
            self.add_view(LatteSupportVerifyView(self))
            self.latte_verify_view = True
        
        self.latte_invite_code = await self.latte.invites()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=self.latte_avtivity))
        print(f"\nName : {self.user}\nActivity : {self.latte_avtivity}\nServers : {len(self.guilds)}\nUsers : {len(set(self.get_all_members()))}")
        print("\nCog loaded\n---------\n")

bot = LatteBot(intents = discord.Intents(
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
), help_command = None, case_insensitive = True, owner_id=240059262297047041)

@tasks.loop(minutes=30)
async def get_version():
    bot.game_version = get_valorant_version()

    # data_store
    data = data_read('skins')
    data['formats'] = bot.format_version
    data['gameversion'] = bot.game_version
    data_save('skins', data)
    
    try:
        if data['skins']["version"] != bot.game_version: fetch_skin()
        if data['tiers']["version"] != bot.game_version: fetch_tier()
    except KeyError:
        fetch_skin()
        pre_fetch_price()
        fetch_tier()

#prepare_verify_view
@bot.command()
@commands.is_owner()
async def prepare_verify(ctx: commands.Context):
    file = discord.File("data/assets/latte_verify_bg.png", filename='latte-verify.png')
    await ctx.send(file=file, view=LatteVerifyView(bot=bot) or None)
    await ctx.message.delete()

@bot.command()
@commands.is_owner()
async def prepare_support_verify(ctx: commands.Context):
    file = discord.File("data/assets/latte_verify_bg.png", filename='latte-verify.png')
    await ctx.send(file=file, view=LatteSupportVerifyView(bot=bot) or None)
    await ctx.message.delete()

#database
async def create_db_pool():
    if not bot.tester or len(bot.tester) == 0:
        bot.pg_con = await asyncpg.create_pool(host=data['dbhost'], user=data['dbuser'], password=data['dbpassword'], database=data['database'], min_size=1, max_size=5)
        print("Connected to PostgreSQL")

#blacklist_user
async def run_once_when_ready():
    await bot.wait_until_ready()
    if not bot.tester or len(bot.tester) == 0:
        banuser = await bot.pg_con.fetch("SELECT user_id, is_blacklisted FROM public.blacklist;")
        for value in banuser:
            bot.blacklist[value['user_id']] = (value['is_blacklisted'] or False)
        print("\nBlacklist database loaded")

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
# def user_blacklisted(ctx: CustomContext):
#     if not bot.blacklist.get(ctx.author.id, None) or ctx.author.id == bot.owner_id:
#         return True
#     if ctx.command.root_parent and ctx.command.root_parent.name == 'pit':
#         return True
#     raise errors.UserBlacklisted

#jishaku
bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

if __name__ == "__main__":
    #database
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.mongo_url))
    bot.latte_db = bot.mongo["latteonly"]
    bot.db_level = bot.mongo["discord"]
    
    bot.latte_tags = Document(bot.latte_db, "tags")
    bot.latte_todo = Document(bot.latte_db, "todo")
    bot.latte_stars = Document(bot.latte_db, "stars")
    bot.custom_roles = Document(bot.latte_db, "custom_roles")
    bot.latte_ping = Document(bot.latte_db, "latency")
    # bot.genshin_db = Document(bot.latte_db, "genshin")
    bot.latte_level = Document(bot.db_level, "levelling")
    
    # bot.notifys = Document(bot.latte_db, "notifys")
    
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            if not file == 'snipe.py':
                bot.load_extension(f'cogs.{file[:-3]}')
        
    bot.loop.run_until_complete(create_db_pool())
    bot.loop.create_task(run_once_when_ready())
    bot.run(bot.token)