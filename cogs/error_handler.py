# Standard
import discord
from discord.ext import commands

# Third party
from difflib import get_close_matches

# Local

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')
    
    @commands.Cog.listener()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def on_command_error(self , ctx, error):
        embed = discord.Embed()
        embed.color = self.bot.white_color
        if isinstance(error, commands.CommandNotFound):
            # cm_error = f"I couldn't find that command."
            command_names = [str(x) for x in ctx.bot.commands]
            matches = get_close_matches(ctx.invoked_with, command_names)
            if matches:
                matches = "\n".join(matches)
                cm_error = f"I couldn't find that command. Did you mean...\n`{matches}`"
            else:
                return
        elif isinstance(error, commands.DisabledCommand):
            cm_error = f"Command is disabled"
        elif isinstance(error, commands.CommandOnCooldown):
            cm_error = f"You are on cooldown, try again in {error.retry_after:.0f} seconds"
        elif isinstance(error, commands.MessageNotFound):
            cm_error = "I can't find that message!"
        elif isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
            cm_error = "I can't find that user!"
        elif isinstance(error, commands.ChannelNotFound):
            cm_error = "I can't find that channel!"
        elif isinstance(error, commands.ChannelNotReadable):
            cm_error = "I don't have acces to read anything in that channel!"
        elif isinstance(error, commands.RoleNotFound):
            cm_error = "I can't find that role!"
        elif isinstance(error, commands.EmojiNotFound):
            cm_error = "I can't find that emoji!"
        elif isinstance(error, commands.MissingPermissions):
            cm_error = f"You don't have **{str(error)[15:-35]}** **permission(s)** to run this command!"
        elif isinstance(error, commands.MissingRole):
            cm_error = f"You don't have **{error.missing_role}** role(s) to run this command!"
        elif isinstance(error, commands.MissingAnyRole):
            cm_error = f"You don't have **{error.missing_role}** role(s) to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            cm_error = "You didn't pass a required argument!"
        elif isinstance(error, commands.NSFWChannelRequired):
            cm_error = f"This channel isn't NSFW"
        elif isinstance(error, commands.CheckFailure):
            cm_error = f"You can't use this command."
        elif isinstance(error, commands.DisabledCommand):
            cm_error = f"This command is restricted to slash commands." 
        elif isinstance(error, commands.CommandError):
            cm_error = f"{error}"
        else:
            print(error)
            return
        embed.description = cm_error
        await ctx.send(embed=embed, delete_after=20, ephemeral=True)
    
def setup(bot):
    bot.add_cog(Error(bot))