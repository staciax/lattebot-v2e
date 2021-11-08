# Standard 
import discord
import random
import asyncio
import json
from discord.ext import commands 
from datetime import datetime, timedelta, timezone

# Third party
import requests
from PIL import Image, ImageDraw , ImageFont , ImageEnhance , ImageFilter
from io import BytesIO

# Local
from utils.xp_pillow import level_images
from utils.paginator import SimplePages
from utils.buttons import NewSimpage
from utils.useful import RenlyEmbed
from utils.checks import is_latte_guild

# xp_channel
chat_channel = 861883647070437386 , 840398821544296480 , 863438518981361686 , 859960606761549835 , 840405578618109952 #chat,game,anime,kdbot,game-chat

# lvl_data
level = ["level 3 ꮺ","level 5 ꮺ","level 10 ꮺ","level 20 ꮺ","level 25 ꮺ","level 30 ꮺ","level 40 ꮺ","level 45 ꮺ","level 50 ꮺ","Nebula ꮺ"]
levelnum = [3,5,10,20,25,30,40,45,50,55]
colorlvl = [0xeedad1,0xc39b7d,0xffbfd7,0xdbc6eb,0xcaf7e3,0xfdffbc,0xc1e7b8,0xc5ffff,0xec6fc1,0xb98fe4]

class Leveling(commands.Cog):
    """Leveling system"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='lutoarakablush', id=903360992103268403, animated=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.tester or len(self.bot.tester) == 0:
            if message.author.bot:
                return
            if message.channel.id in chat_channel: #แก้ไขเป็น json
                data = await self.bot.latte_level.find_by_custom({"id": message.author.id, "guild_id": message.guild.id})            
                if data is None:
                    data = {
                        "id" : message.author.id,
                        "xp" : 100,
                        "guild_id": message.guild.id
                    }
                    #add_role_xp_bar
                    guild = message.guild
                    lvl_bar = discord.utils.get(guild.roles, id = 854503041775566879)#・ ──────꒰ ・ levels ・ ꒱────── ・
                    await message.author.add_roles(lvl_bar)

                xp = data["xp"]
                # print(xp)
                data["xp"] += 5
                await self.bot.latte_level.update_by_custom(
                    {"id": message.author.id, "guild_id": message.guild.id}, data
                )

                lvl = 0 
                while True:
                    if xp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp == 0:
                    emlvup = discord.Embed(description=f"**Congratulations**, {message.author.mention} you leveled up to **level {lvl}.**!",color=0xffffff)
                    msg = await message.channel.send(embed=emlvup)
                    for i in range(len(level)):
                        if lvl == levelnum[i]:
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                            embed = discord.Embed(description=f"**Congratulations**, {message.author.mention} you leveled up to **level {lvl}.**!\nyou have gotten role **{level[i]}**!!!",color=0xffffff)
                            await msg.edit(embed=embed)
            
    @commands.command(help="Level ranking", aliases=['rank','leaderboard'])
    @commands.guild_only()
    @is_latte_guild()
    async def ranking(self, ctx):
        try:
            filter_member = await self.bot.latte_level.find_many_by_custom({"guild_id": ctx.guild.id})
            filter_member = sorted(filter_member, key=lambda x: x["xp"] , reverse=True)

            filter_xp = []
            for x in filter_member:
                try:
                    member_name = ctx.guild.get_member(x["id"]).name
                    member_xp = x["xp"]  
                    lvl = 0
                    while True:
                        if member_xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    #member_xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    #final_xp = (200*((1/2)*lvl))
                    #({member_xp}/{int(final_xp)})
                    message = f"**{member_name}**\nLevel : {lvl} (Total XP: {member_xp})\n"
                    filter_xp.append(message)

                except:
                    pass
                    
            #view_button
            p = NewSimpage(entries=filter_xp, per_page=5, ctx=ctx)
            if ctx.guild.icon.url is not None:
                p.embed.set_author(name=f"{ctx.guild.name} Rankings", url=ctx.guild.icon.url , icon_url=ctx.guild.icon.url)
            else:
                p.embed.set_author(name=f"{ctx.guild.name} Rankings")
            p.embed.set_footer(text = f'{self.bot.user.name}') 
            p.embed.color = 0x77dd77
            await p.start()
        except:
            raise commands.BadArgument('error')

    @commands.command(help="Shows exp the specified member.", aliases=['lvl' , 'exp'])
    @commands.guild_only()
    @is_latte_guild()
    async def xp(self, ctx, member: discord.Member = None):
        if ctx.channel.id in chat_channel:
            embed = RenlyEmbed.to_error(description="Please use bot command in <#861874852050894868>")
            embed.color = self.bot.white_color
            return await ctx.send(embed=embed , ephemeral=True)
        try:
            async with ctx.typing():
                if not member:
                    member = ctx.author
                member_id = member.id 
                stats = await self.bot.latte_level.find_by_custom({"id": member_id, "guild_id": ctx.guild.id})
                if stats is None:
                    embed = discord.Embed(description="You haven't sent any messages, **no xp**!!",color=0xffffff)
                    await ctx.send(embed=embed)
                else:
                    xp = stats["xp"]
                    lvl = 0
                    rank = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    filter_member = await self.bot.latte_level.find_many_by_custom({"guild_id": ctx.guild.id})
                    filter_member = sorted(filter_member, key=lambda x: x["xp"] , reverse=True)
                    for x in filter_member:
                        rank += 1
                        if stats["id"] == x["id"]:
                            break
                    final_xp = (200*((1/2)*lvl))
                    
                    embedlv = discord.Embed(title=f"{member.name}'s level stats | {ctx.guild.name}",color=0x77dd77)
                    embedlv.set_image(url="attachment://latte-level.png")
                    
                    await ctx.send(file=level_images(member, final_xp, lvl, rank, xp), embed=embedlv)
        except:
            raise commands.BadArgument('error')
  
    # @commands.command(description="Crete xp role")
    # @commands.guild_only()
    # @commands.has_permissions(administrator = True)
    # async def xprole(self, ctx):
    #     embed = discord.Embed(description="", color=0xffffff)
    #     embed.title = "✧ LATTE XP ROLE!"
    #     lvlbar = "・ ──────꒰ ・ levels ・ ꒱────── ・"
    #     lvlbar2 = discord.utils.get(ctx.author.guild.roles, name=lvlbar)
    #     if not lvlbar2:
    #         await ctx.guild.create_role(name=lvlbar , colour=0x18191c)
    #         embed.description += f"{lvlbar.mention}\n"
    #         embed.description += f"{lvlbar2.mention}\n"
        
    #         for x, y in zip(reversed(level), reversed(colorlvl)):
    #             checkrole = discord.utils.get(ctx.author.guild.roles, name=level)
    #             if not checkrole:
    #                 await ctx.guild.create_role(name=x , colour=y)
    #             else:
    #                 return
    #     elif lvlbar2:
    #         for i in reversed(range(len(level))):
    #             roles = discord.utils.get(ctx.author.guild.roles, name=level[i])
    #             if roles:
    #                 embed.description += f"{roles.mention}\n"

    #         await ctx.channel.send(embed=embed)

def setup(bot):

    bot.add_cog(Leveling(bot))