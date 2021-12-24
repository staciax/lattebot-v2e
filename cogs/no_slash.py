# Standard 
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from utils.formats import format_dt 

# Third party
# Local

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
    async def pastel(self, ctx):
        await ctx.reply("https://colorhunt.co/palettes/pastel", mention_author=False)

    @commands.command(name="color", help="color hex")
    @commands.guild_only()
    async def color(self, ctx):
        await ctx.reply("https://www.color-hex.com/", mention_author=False)
    
    @commands.command(name='uptime', help="Gets the uptime of the bot")
    @commands.guild_only()
    async def uptime(self, ctx):
        uptime = datetime.utcnow() - self.bot.launch_time
        futuredate = datetime.now(timezone.utc) - timedelta(seconds=int(uptime.total_seconds())) 
        embed = discord.Embed(description=f"🕘 I started {format_dt(futuredate, style='R')}", color=self.bot.white_color)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(No_slash(bot))