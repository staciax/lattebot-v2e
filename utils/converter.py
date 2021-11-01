# Standard 
import discord
import re
from discord.ext import commands
from datetime import datetime, timedelta

# Third
import emojis

# Local
from utils.formats import format_relative

class UnicodeEmojiNotFound(commands.BadArgument):
    def __init__(self, argument):
        self.argument = argument
        super().__init__(f'Unicode emoji "{argument}" not found.')

class UnicodeEmojiConverter(commands.Converter):
    async def convert(self, ctx, argument):
        emoji = emojis.db.get_emoji_by_code(argument)
        if not emoji:
            raise UnicodeEmojiNotFound(argument)
        # `emoji` is a named tuple.
        # see: https://github.com/alexandrevicenzi/emojis/blob/master/emojis/db/db.py#L8
        # we already confirmed its a valid emoji, so lets return the codepoint back
        return emoji.emoji

def member_status(ctx):
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]    
    return statuses

def check_boost(ctx):
    format_relative = lambda dt: discord.utils.format_dt(dt, 'R')
    if ctx.guild.premium_tier != 0:
        boosts = f'**Level:** {ctx.guild.premium_tier}\n**Boosts:** {ctx.guild.premium_subscription_count}'
        last_boost = max(ctx.guild.members, key=lambda m: m.premium_since or ctx.guild.created_at)
        if last_boost.premium_since is not None:
            boosts = f'{boosts}\n**Last Boost:**\n{last_boost} ({format_relative(last_boost.premium_since)})'
    else:
        boosts_1 = f'**Level:** \n**Boosts:** '
        boosts = f'{boosts_1}\n**Last Boost:**\n'

    return boosts

def afk_channel_check(ctx):
    if ctx.guild.afk_channel: afk_channels = ctx.guild.afk_channel
    else: afk_channels = "⠀"
    return afk_channels

def afk_channel_timeout(ctx):
    if ctx.guild.afk_channel:
        if ctx.guild.afk_timeout: afk_time = f"{int(ctx.guild.afk_timeout / 60)} Minutes"
    else: afk_time = "⠀"
    return afk_time

def rules_channel(ctx):
    if ctx.guild.rules_channel is None: rs = "⠀"
    else: rs = ctx.guild.rules_channel.mention   
    return rs

def system_channel(ctx):
    if ctx.guild.system_channel is None: sy = "⠀"
    else: sy = ctx.guild.system_channel.mention
    return sy

def guild_verification_level(ctx):
    if str(ctx.guild.verification_level) == "none": gvl = "⠀"
    else: gvl = ctx.guild.verification_level
    return gvl

def status_icon(current_status):
    status = str(current_status)
    if status == "online":
        output = "https://cdn.discordapp.com/emojis/864171414466592788.png"
    elif status == "idle":
        output = "https://cdn.discordapp.com/emojis/864185381833277501.png"
    elif status == "dnd":
        output = "https://cdn.discordapp.com/emojis/864173608321810452.png"
    elif status == "offline":
        output = "https://cdn.discordapp.com/emojis/864171414750625812.png"

    return output

time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

def FutureTime_converter(time):
    since = time
    seconds = ("s", "sec", "secs", 'second', "seconds")
    minutes = ("m", "min", "mins", "minute", "minutes")
    hours = ("h", "hour", "hours")
    days = ("d", "day", "days")
    weeks = ("w", "week", "weeks")
    rawsince = since

    try:
        temp = re.compile("([0-9]+)([a-zA-Z]+)")
        res = temp.match(since).groups()
        time = int(res[0])
        since = res[1]

    except ValueError:
        return
        
    if since.lower() in seconds:
        timewait = time
    elif since.lower() in minutes:
        timewait = time * 60
    elif since.lower() in hours:
        timewait = time * 3600
    elif since.lower() in days:
        timewait = time * 86400
    elif since.lower() in weeks:
        timewait = time * 604800

    return timewait