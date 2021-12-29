# Standard 
import discord
from discord.ext import commands 

# Third party

# Local
from utils.xp_pillow import level_images
from utils.buttons import NewSimpage
from utils.checks import is_latte_guild
from utils.errors import UserInputErrors

# xp_channel

colorlvl = {
    3:0xeedad1,
    5:0xc39b7d,
    10:0xffbfd7,
    15:0xc5ffff,
    20:0xdbc6eb,
    25:0xcaf7e3,
    30:0xfdffbc,
    40:0xc1e7b8,
    45:0x99fdfd,
    50:0xec6fc1,
    55:0xb98fe4
}

class Leveling(commands.Cog, command_attrs = dict(slash_command=True, slash_command_guilds=[840379510704046151])):
    """Leveling system"""

    def __init__(self, bot):
        self.bot = bot
        self.level = ["level 3 ꮺ","level 5 ꮺ","level 10 ꮺ","level 15 ꮺ","level 20 ꮺ","level 25 ꮺ","level 30 ꮺ","level 40 ꮺ","level 45 ꮺ","level 50 ꮺ","Nebula ꮺ"]
        self.levelnum = [3,5,10,15,20,25,30,40,45,50,55]
        self.chat_channel = 861883647070437386, 840398821544296480 , 863438518981361686 , 859960606761549835 #chat,game,anime,kdbot
        self.text_channel = 20
        self.voice_channel = 10

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='lutoarakablush', id=903360992103268403, animated=False)

    async def xp_update(self, member, guilds, get_xp, channel=None):
        if channel is None:
            member_guild = member.guild
            channel = member_guild.get_channel(861883647070437386)

        data = await self.bot.latte_level.find_by_custom({"id": member.id, "guild_id": guilds.id})            
        if data is None:
            data = {
                "id" : member.id,
                "xp" : 50,
                "guild_id": guilds.id
            }
            #add_role_xp_bar
            guild = guilds
            lvl_bar = discord.utils.get(guild.roles, id = 854503041775566879)#・ ──────꒰ ・ levels ・ ꒱────── ・
            await member.add_roles(lvl_bar)

        xp = data["xp"]
        data["xp"] += get_xp
        await self.bot.latte_level.update_by_custom({"id": member.id, "guild_id": guilds.id}, data)
        lvl = 0 
        while True:
            if xp < ((50*(lvl**2))+(50*lvl)):
                break
            lvl += 1
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        try:
            em_color = colorlvl[lvl]
        except:
            em_color = 0xffffff
        if xp in range(get_xp):
            emlvup = discord.Embed(description=f"{member.mention} you leveled up to **level {lvl}.**!", color=em_color)
            msg = await channel.send(embed=emlvup)
            for i in range(len(self.level)):
                if lvl == self.levelnum[i]:
                    role = discord.utils.get(member.guild.roles, name=self.level[i])
                    await member.add_roles(role)
                    embed = discord.Embed(description=f"{member.mention} you leveled up to {role.mention}.!", color=em_color) #**!\nyou have gotten role **{self.level[i]}**!!!
                    await msg.edit(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.tester or len(self.bot.tester) == 0:
            if message.author.bot:
                return
            if message.channel.id in self.chat_channel:
                try:
                    await self.xp_update(message.author, message.guild, self.text_channel, message.channel)
                except:
                    pass
            
    @commands.command(help="Level ranking", aliases=['rank','leaderboard'])
    @commands.guild_only()
    @is_latte_guild()
    async def ranking(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
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
            raise UserInputErrors('An unknown error occurred, please try again !')

    @commands.command(help="Shows exp the specified member.", aliases=['lvl' , 'exp'])
    @commands.guild_only()
    @is_latte_guild()
    async def xp(self, ctx, member: discord.Member = None):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        try:
            if ctx.clean_prefix != "/":
                await ctx.trigger_typing()
            member = member or ctx.author
            member_id = member.id 
            stats = await self.bot.latte_level.find_by_custom({"id": member_id, "guild_id": ctx.guild.id})
            
            if stats is None:
                raise UserInputErrors("You haven't sent any messages, **no xp**!!")
            
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
            if ctx.channel.id in self.chat_channel:
                if ctx.clean_prefix != "/":
                    await ctx.message.delete()
                return await ctx.reply(file=level_images(member, final_xp, lvl, rank, xp), embed=embedlv, ephemeral=True, delete_after=15, mention_author=False)
            await ctx.reply(file=level_images(member, final_xp, lvl, rank, xp), embed=embedlv, mention_author=False)
        except:
            raise UserInputErrors('An unknown error occurred, please try again !')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if member.guild == self.bot.latte:
                if not before.channel and after.channel:
                    await self.xp_update(member, member.guild, self.voice_channel)
        except:
            pass

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