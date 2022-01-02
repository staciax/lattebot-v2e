# Standard 
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from utils.formats import format_dt 

# Third party
# Local
from utils.checks import is_latte_guild
from utils.latte_converter import fancy_text

class No_slash(commands.Cog, command_attrs = dict(slash_command=False)):
    """Only message command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='createthread', id=903346472509141023, animated=False)

    @commands.command(name="pastel", help="pastel color")
    @commands.guild_only()
    @is_latte_guild()
    async def pastel(self, ctx):
        await ctx.reply("https://colorhunt.co/palettes/pastel", mention_author=False)

    @commands.command(name="hex", help="color hex")
    @commands.guild_only()
    @is_latte_guild()
    async def hex_(self, ctx):
        await ctx.reply("https://www.color-hex.com/", mention_author=False)
    
    @commands.command(name='uptime', help="Gets the uptime of the bot")
    @commands.guild_only()
    @is_latte_guild()
    async def uptime(self, ctx):
        uptime = datetime.utcnow() - self.bot.launch_time
        futuredate = datetime.now(timezone.utc) - timedelta(seconds=int(uptime.total_seconds())) 
        embed = discord.Embed(description=f"🕘 I started {format_dt(futuredate, style='R')}", color=self.bot.white_color)
        await ctx.send(embed=embed)

    @commands.command(name='ftext')
    @commands.guild_only()
    @is_latte_guild()
    async def ftext(self, ctx, *, text):
        if len(text) == 0 or len(text) > 200:
            return
        
        def split(word):
            return list(word)

        text_list = split(text)
        output = ''
        for x in text_list:
            try:
                output += fancy_text[x]
            except:
                pass

        await ctx.send(output)

    # @commands.command(help="Happy new year 2022")
    # @commands.guild_only()
    # @is_latte_guild()
    # async def happynewyear(self, ctx):
    #     embed = discord.Embed(color=0xbab6fd)
    #     embed.description = "┏━━┓┏━━┓┏━━┓   ┃┃\n┗━┓┃┃┏┓┃┗━┓┃   ┗┛\n┏━┛┃┃┃┃┃┏━┛┃ ┏━━┓\n┃┏━┛┃┃┃┃┃┏━┛ ┗━┓┃ \n┃┗━┓┃┗┛┃┃┗━┓ ┏━┛┃\n┗━━┛┗━━┛┗━━┛ ┃┏━┛"
        
    #     spacial_role = self.bot.latte.get_role(926471814757113946)
    #     role2021 = self.bot.latte.get_role(926470373573271583)

    #     # guild_member = ctx.guild.members
    #     # for member in guild_member:
    #     #     try:
    #     #         await member.add_roles(spacial_role, role2021)
    #     #     except:
    #     #         pass
        
    #     chat_channel = self.bot.latte.get_channel(861883647070437386)
    #     await chat_channel.send(content='<a:purplestar:902673752976941066> **Happy New Year 2022** <a:purplestar:902673752976941066>', embed=embed, allowed_mentions=discord.AllowedMentions.none())

    # @commands.command(help="Happy new year 2022")
    # @commands.guild_only()
    # @is_latte_guild()
    # async def member_2021(self, ctx):
    #     embed=discord.Embed(color=0xbab6fd)
    #     role2021 = self.bot.latte.get_role(926470373573271583)
    #     embed.description = f'{role2021.mention}'
    #     chat_channel = self.bot.latte.get_channel(861883647070437386)
    #     await chat_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(No_slash(bot))