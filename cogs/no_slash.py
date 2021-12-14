# Standard 
import discord
from discord.ext import commands

# Third party
# Local


class No_slashError(commands.CommandError):
    pass

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
         
def setup(bot):
    bot.add_cog(No_slash(bot))