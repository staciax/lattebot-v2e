# Standard
import discord
import random
from discord.ext import commands , tasks
from typing import Literal
# from asyncdagpi import ImageFeatures as imageFeatures

# Third

# Local

class Image_manipulation(commands.Cog, command_attrs = dict(slash_command=True)):

    List1 = ['asciifie','balls','bomb','charcoal','delete','glitch','glitch2','hog','invert','layers','paint','pixel']
    List2 = ['patpat','polaroid','poster','radiate','rgb','sepia','shatter','sketch','swirl','trash','triangle','triggered']

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')

    # @commands.command(slash_command_guilds=[840379510704046151])
    # @commands.guild_only()
    # async def manipulation(
    #         self,
    #         ctx,
    #         type: Literal['ascii','balls','bomb','charcoal','delete','glitch','glitch2','hog','invert','layers','paint','pixel'] = commands.Option(description="type"),
    #         member: discord.Member= commands.Option(default=None, description="Spectify member")
    #     ):
    #     if member is None:
    #         if ctx.message.reference:
    #            member = ctx.message.reference.resolved.author
    #         else:
    #             member = ctx.author
               
    # #   await ctx.trigger_typing()
               
    #     url = str(member.display_avatar.replace(format="png", size=1024))
    #     image = await self.bot.dagpi.image_process(ImageFeatures.ascii(), url)
        
    #     await ctx.send(file=discord.File(fp=image.image, filename=f"ascii.{image.format}"))

    #     if type == 'ascii':
    #         print()
    #     elif type == 'balls':
    #         print()
    #     elif type == 'bomb':
    #         print()
    #     elif type == 'charcoal':
    #         print()
    #     elif type == 'delete':
    #         print()
    #     elif type == 'glitch':
    #         print()
    #     elif type == 'glitch2':
    #         print()
    #     elif type == 'hog':
    #         print()
    #     elif type == 'invert':
    #         print()
    #     elif type == 'layers':
    #         print()
    #     elif type == 'paint':
    #         print()
    #     elif type == 'pixel':
    #         print()
        
    # @commands.command(slash_command_guilds=[840379510704046151])
    # @commands.guild_only()
    # async def manipulation2(
    #         self,
    #         ctx,
    #         type: Literal['patpat','polaroid','poster','radiate','rgb','sepia','shatter','sketch','swirl','trash','triangle','triggered'] = commands.Option(description="type"),
    #         member:discord.Member= commands.Option(default=None, description="Spectify member")
    #     ):

    #     if type == 'patpat':
    #         print()
    #     elif type == 'polaroid':
    #         print()
    #     elif type == 'poster':
    #         print()
    #     elif type == 'radiate':
    #         print()
    #     elif type == 'rgb':
    #         print()
    #     elif type == 'sepia':
    #         print()
    #     elif type == 'shatter':
    #         print()
    #     elif type == 'sketch':
    #         print()
    #     elif type == 'swirl':
    #         print()
    #     elif type == 'trash':
    #         print()
    #     elif type == 'triangle':
    #         print()
    #     elif type == 'triggered':
    #         print()
    
    
def setup(bot):
    bot.add_cog(Image_manipulation(bot))