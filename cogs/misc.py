# Standard
import discord
import platform
import time
from discord.ext import commands , tasks
from datetime import datetime, timedelta, timezone

# Local
from utils.emoji import emoji_converter
from utils.formats import format_dt , count_python

class Misc(commands.Cog, command_attrs = dict(slash_command=True)):
    """Misc commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='⚙️')

    @commands.command(help="Invite me")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def invite(self, ctx):
        view = discord.ui.View()
        invite_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Invite me", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands") 
        view.add_item(item=invite_button)
        embed = discord.Embed(title="Support server")
        embed.description = "Note: `some features may not be available, sorry.`"
        embed.color = self.bot.white_color
        await ctx.send(embed=embed, view=view)
    
    # @commands.command(help="Vote for me")
    # @commands.guild_only()
    # @commands.bot_has_permissions(send_messages=True , embed_links=True)
    # async def vote(self, ctx):
    #     view = discord.ui.View()
    #     vote_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Vote for me", url="") 
    #     view.add_item(item=vote_button)
    #     await ctx.send(view=view)
    
    @commands.command(help="Sends the support server of the bot.")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def support(self, ctx):
        view = discord.ui.View()
        support_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Server support", url=self.bot.latte_invite_url) 
        view.add_item(item=support_button)

        embed = discord.Embed(title="Support server")
        embed.color = self.bot.white_color
        await ctx.send(embed=embed, view=view)

    @commands.command(help="Shows the bot's prefixes")
    @commands.guild_only()
    async def prefix(self, ctx):
        embed = discord.Embed(color=self.bot.white_color)
        embed.title = "My prefixes for this server:"
        embed.description = f"{self.bot.user.mention}\n/\n{self.bot.defaul_prefix}"
        await ctx.send(embed=embed, ephemeral=True)
    
    @commands.command(aliases=["botinfo"], help="Shows basic information about the bot.")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def about(self, ctx):
        owner_bot = self.bot.renly

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"About Me", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=owner_bot.avatar.url)

        #stats
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        # totalcogs = len(self.bot.cogs)
        totalcommands = len(self.bot.commands)

        fields = [
            ("About Developer" , f"Owner: [{owner_bot}](https://discord.com/users/{owner_bot.id})" , False),
            ("Stats " , f"{emoji_converter('cursor')} Line count : `{count_python('.'):,}`\n{emoji_converter('latte_icon')} Servers : `{serverCount}`\n{emoji_converter('member')} Users : `{memberCount}`\n{emoji_converter('bot_commands')} Commands : `{totalcommands}`" , False), #{platform.system()}
            ("Bot Info" , f"{emoji_converter('latte_icon')} {self.bot.user.name} : `{self.bot.bot_version}`\n{emoji_converter('python')} Python : `{platform.python_version()}`\n{emoji_converter('dpy')} Enhanced-discord.py : `{discord.__version__}`\n{emoji_converter('mongo')} Database : `MongoDB`" , False),
            ]
        
        for name , value , inline in fields:
           embed.add_field(name=name , value=value , inline=inline)

        # embed.add_field(name="Bot created" , value=f"{format_dt(self.bot.user.created_at)}" , inline=False)
                
        #start_view_button
        # view = discord.ui.View()
        # style = discord.ButtonStyle.gray
        #Source_code = discord.ui.Button(emoji=f"{utils.emoji_converter('github')}",style=style, label="Source code", url=self.bot.latte_source)
        #Vote.gg = discord.ui.Button(style=style, label="Source code", url=self.bot.latte_source)
        # view.add_item(item=Source_code)
    
        await ctx.send(embed=embed)

    @commands.command(name='uptime', help="Gets the uptime of the bot")
    @commands.guild_only()
    async def uptime(self, ctx):
        uptime = datetime.utcnow() - self.bot.launch_time
        futuredate = datetime.now(timezone.utc) - timedelta(seconds=int(uptime.total_seconds())) 

        embed = discord.Embed(description=f"🕘 I started {format_dt(futuredate, style='R')}", color=self.bot.white_color)
        await ctx.send(embed=embed)
        # delta_uptime = relativedelta(datetime.utcnow(), self.bot.launch_time)
        # days, hours, minutes, seconds = delta_uptime.days, delta_uptime.hours, delta_uptime.minutes, delta_uptime.seconds

        # uptimes = {x[0]: x[1] for x in [('days', days), ('hours', hours),
        #                                 ('minutes', minutes), ('seconds', seconds)] if x[1]}

        # last = "".join(value for index, value in enumerate(uptimes.keys()) if index == len(uptimes)-1)
        # uptime_string = "".join(
        #     f"{v} {k} " if k != last else f" and {v} {k}" if len(uptimes) != 1 else f"{v} {k}"
        #     for k, v in uptimes.items()
        # )
        # embed = discord.Embed(description=f"I started {uptime_string} ago.", color=self.bot.white_color)
        # await ctx.send(embed=embed)

    @commands.command(help="Shows the latency of the bot")
    @commands.guild_only()
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)

        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = round((typinge - typings) * 1000)

        dbstart = time.monotonic()
        await self.bot.latte_ping.find_by_custom({"stacia_id": 240059262297047040})
        dbend = time.monotonic()
       
        embed = discord.Embed(color=self.bot.white_color)
        embed.add_field(name=f"{emoji_converter('latte_icon')} Latency", value=f"```nim\n{bot_latency} ms```", inline=True)
        embed.add_field(name=f"{emoji_converter('cursor')} Typing", value=f"```nim\n{typingms} ms```", inline=True)
        embed.add_field(name=f"{emoji_converter('mongo')} Database", value=f"```nim\n{(dbend-dbstart)*1000:,.0f} ms```", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))