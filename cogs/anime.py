# Standard
import discord
import typing
import random
from discord.ext import commands , tasks
from typing import Literal
# Third

# Local
from utils.api import base_waifu_im_api , base_waifu_pisc_api , base_waifu_pisc_api_nsfw # , base_waifu_im_api_nsfw

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
    
    @commands.command(help="Display waifu im sfw.")
    @commands.guild_only()
    async def waifu_im_sfw(self, ctx, tags: Literal["waifu", "maid", "all"] = commands.Option(description="choose tags")):

        # @property
        # def display_emoji(self) -> discord.PartialEmoji:
        #     return discord.PartialEmoji(name='nono', id=890369747273793556, animated=True)
        
        if tags == "waifu":
            waifu_url = "https://api.waifu.im/sfw/waifu"
        elif tags == "maid":
            waifu_url = "https://api.waifu.im/sfw/maid"
        elif tags == "all":
            waifu_url = "https://api.waifu.im/sfw/all"
        else:
            tags_list = ["waifu", "maid", "all"]
            tags_random = random.choice(tags_list)
            waifu_url = f"https://api.waifu.im/nsfw/{tags_random}"
          
        if waifu_url:
            view = base_waifu_im_api(ctx=ctx, url=waifu_url)
            return await view.api_start()
    
    @commands.command(help="Display waifu im nsfw.")
    @commands.guild_only()
    @commands.is_nsfw()
    async def waifu_im_nsfw(self, ctx, tags: Literal["ass","ecchi","ero","hentai","maid","milf","oppai","oral","paizuri","selfies","uniform"] = commands.Option(description="choose tags")):
        if tags == "ass":
            waifu_url = "https://api.waifu.im/nsfw/ass"
        elif tags == "ecchi":
            waifu_url = "https://api.waifu.im/nsfw/ecchi"
        elif tags == "ero":
            waifu_url = "https://api.waifu.im/nsfw/ero"
        elif tags == "hentai":
            waifu_url = "https://api.waifu.im/nsfw/hentai"
        elif tags == "maid":
            waifu_url = "https://api.waifu.im/nsfw/maid"
        elif tags == "milf":
            waifu_url = "https://api.waifu.im/nsfw/milf"
        elif tags == "oral":
            waifu_url = "https://api.waifu.im/nsfw/oral"
        elif tags == "oral":
            waifu_url = "https://api.waifu.im/nsfw/oral"
        elif tags == "paizuri":
            waifu_url = "https://api.waifu.im/nsfw/paizuri"
        elif tags == "selfies":
            waifu_url = "https://api.waifu.im/nsfw/selfies"
        elif tags == "uniform":
            waifu_url = "https://api.waifu.im/nsfw/uniform"
        else:
            tags_list = ["ass","ecchi","ero","hentai","maid","milf","oppai","oral","paizuri","selfies","uniform"]
            tags_random = random.choice(tags_list)
            waifu_url = f"https://api.waifu.im/nsfw/{tags_random}"

        if waifu_url:
            view = base_waifu_im_api(ctx=ctx, url=waifu_url)
            return await view.api_start()
        
        # if type == "sfw":
        #     waifu_url = "https://api.waifu.im/sfw/waifu/"
        #     view = base_waifu_im_api(ctx=ctx, url=waifu_url)
        #     return await view.api_start()
        # elif type == "nsfw":
        #     if ctx.channel.is_nsfw():
        #         nsfw = ["ass","ecchi","ero","hentai","maid","milf","oppai","oral","paizuri","selfies","uniform"]
        #         random_nsfw = random.choice(nsfw)
        #         waifu_url = f"https://api.waifu.im/nsfw/{random_nsfw}/"
        #         view = base_waifu_im_api_nsfw(ctx=ctx, url=waifu_url)
        #         return await view.api_start()  
            # raise commands.NSFWChannelRequired(ctx.channel)

    @commands.command(help="Display waifu pisc.")
    @commands.guild_only()
    async def waifu_pisc(self, ctx, type: Literal["sfw", "nsfw"] = commands.Option(description="choose type")):
        if type == "sfw":
            view = base_waifu_pisc_api(ctx=ctx)
            return await view.api_start()
        elif type == "nsfw":
            if ctx.channel.is_nsfw():
                view = base_waifu_pisc_api_nsfw(ctx=ctx)
                return await view.api_start()      
            raise commands.NSFWChannelRequired(ctx.channel)
            
def setup(bot):
    bot.add_cog(Anime(bot))