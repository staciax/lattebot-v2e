# Standard
import discord
import asyncio
import random
from discord.ext import commands

# Third

# Local
from utils.checks import is_latte_guild
from utils.errors import UserInputErrors

class Latte(commands.Cog, command_attrs = dict(slash_command=True, slash_command_guilds=[840379510704046151])):
    """Commands only latte server"""
    def __init__(self, bot):
        self.bot = bot
        self.latte_bot = [861874852050894868, 840381588704591912, 844462710526836756]
        self.underworldx = [873677543453126676, 873679362082369546]
        self.moonlightx = [875037193196945409, 875038018736644166]
        self.deathx = [883025077610876958, 883059509810040884]
        self.angelx = [873696566165250099, 883027485455941712]
        self.tempx = [879260123665682482, 879260241286549525]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='latte_icon_new', id=907030425011109888, animated=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild == self.bot.latte:
                if message.channel.id in self.latte_bot:
                    if message.content.startswith('uw'):
                        if message.author.voice:
                            channel = message.guild.get_channel(self.underworldx[1])
                            await message.author.move_to(channel)
                            await message.delete()
                    if message.content.startswith('temp'):
                        if message.author.voice:
                            channel = message.guild.get_channel(self.tempx[1])
                            await message.author.move_to(channel)
                            await message.delete()
                    if message.content.startswith('moonlight'):
                        if message.author.voice:
                            channel = message.guild.get_channel(self.moonlightx[1])
                            await message.author.move_to(channel) 
                            await message.delete()
                    if message.content.startswith('angel'):
                        if message.author.voice:
                            channel = message.guild.get_channel(self.angelx[1])
                            await message.author.move_to(channel) 
                            await message.delete()

                if message.content.startswith('ร้องไห้'):
                    sticker_list = [872926712776777768, 872922021036707901]
                    sticker_choice = random.choice(sticker_list)
                    stick = self.bot.get_sticker(sticker_choice)
                    await message.channel.send(stickers = [stick])
                
                if message.content.startswith('shadowplay'):
                    stick = self.bot.get_sticker(878702176413810699)
                    await message.channel.send(stickers = [stick])
                
                if message.content.startswith(('เอาซันไลต์มาล้างตาดิ','เอาซันไลมา','ล้างตา','ซันไล')):
                    stick = self.bot.get_sticker(872926576847777842)
                    await message.channel.send(stickers = [stick])

                if message.channel.id == self.tempx[0]:
                    await asyncio.sleep(60)
                    await message.delete()

        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
        except discord.HTTPException:
            pass
        except Exception as ex:
            print(ex)

    @commands.command(name='template', aliases=['lt'], help="latte server template")
    @commands.guild_only()
    @is_latte_guild()
    async def latte_template(self, ctx):
        if ctx.clean_prefix == "/":
            await ctx.send('** **', ephemeral=True)
        await ctx.channel.send("https://discord.new/sFYKgkknRN5f")

    @commands.command(name='temprole', aliases=['ltemp'], help="lattte temp role")
    @commands.guild_only()
    @is_latte_guild()
    async def latte_temp_role(self, ctx, member: discord.Member = commands.Option(default=None, description="Give role to member")):
        if not member:
            member = ctx.author
        role = discord.utils.get(ctx.guild.roles, id=879258879987449867)
        member_role = discord.utils.get(
            member.roles, id=879258879987449867)
        if member_role:
            raise UserInputErrors(f"{member.name} is already a temp role!")
        await member.add_roles(role)
        embed = discord.Embed(
            description="Temp is ready\n`This role will disappear within 2 hour.`", color=self.bot.white_color)
        await ctx.send(embed=embed, ephemeral=True)
        await asyncio.sleep(7200)
        await member.remove_roles(role)
    
    @commands.command(help="Custom role color")
    @commands.guild_only()
    @is_latte_guild()
    async def colors(self, ctx, color=commands.Option(description="Specify the color you want to change.")):
        embed = discord.Embed(color=0xffffff, timestamp=ctx.message.created_at)
        embed.set_author(name=f'{ctx.guild.name} | Color Request', icon_url=ctx.guild.icon.url)
        embed.description = f"**Color:** {color}"
        embed.set_footer(text="Requested by", icon_url=ctx.author.avatar or ctx.author.default_avatar)
        await self.bot.renly.send(embed=embed)

        embed_send = discord.Embed(color=0xffffff, timestamp=ctx.message.created_at)
        embed_send.description = 'I have sent your request to the moderator. <3'
        await ctx.send(embed=embed_send)
    
def setup(bot):
    bot.add_cog(Latte(bot))