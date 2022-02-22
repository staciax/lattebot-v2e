# Standard
import discord
import typing
import random
from discord.ext import commands
from typing import Literal
# Third

# Local
from utils.api import WaifuimView, WaifupiscView, WaifupiscView_nsfw # , base_waifu_im_api_nsfw

class Anime(commands.Cog, command_attrs = dict(slash_command=True)):
    """Anime commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='nekostare', id=903339723806875648, animated=False)
    
    # @commands.command(name="waifuim", help="Display waifu im sfw.", aliases=["wfim"])
    # @commands.guild_only()
    # async def waifu_im_sfw(self, ctx, tags: Literal["waifu", "maid"] = commands.Option(description="choose tags")):        
    #     if tags == "waifu":
    #         waifu_url = "https://api.waifu.im/sfw/waifu"
    #     elif tags == "maid":
    #         waifu_url = "https://api.waifu.im/sfw/maid"
          
    #     view = WaifuimView(ctx=ctx, url=waifu_url)
    #     await view.api_start()
    
    @commands.command(name="waifuim_nsfw", help="Display waifu im nsfw.", aliases=['waifuimnsfw','wfnsfw'])
    @commands.guild_only()
    @commands.is_nsfw()
    async def waifu_im_nsfw(self, ctx, tags: Literal["ass","ecchi","ero","hentai","maid","milf","oppai","oral","paizuri","selfies","uniform"] = commands.Option(description="choose tags")):

        fianl_url = 'https://api.waifu.im/random/?selected_tags={}'.format(tags)

        view = WaifuimView(ctx=ctx, url=fianl_url)
        await view.api_start()
            
    @commands.command(name="waifupisc", help="Display waifu pisc.", aliases=["wfp"])
    @commands.guild_only()
    async def waifu_pisc(self, ctx, type: Literal["sfw", "nsfw"] = commands.Option(description="choose type")):
        if type == "sfw":
            view = WaifupiscView(ctx=ctx)
            return await view.api_start()
        elif type == "nsfw":
            if ctx.channel.is_nsfw():
                view = WaifupiscView_nsfw(ctx=ctx)
                return await view.api_start()      
            raise commands.NSFWChannelRequired(ctx.channel)
            
def setup(bot):
    bot.add_cog(Anime(bot))