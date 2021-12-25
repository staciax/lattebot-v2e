# Standard
import discord
import asyncio
import random
from discord.ext import commands
from typing import Literal
from re import search
# Third

# Local
from utils.json_loader import latte_read
from utils.checks import is_latte_guild
from utils.errors import UserInputErrors
from utils.latte_converter import latte_voice
from utils.useful import Embed

class Latte(commands.Cog, command_attrs = dict(slash_command=True, slash_command_guilds=[840379510704046151])):
    """Commands only latte server"""
    def __init__(self, bot):
        self.bot = bot
        self.json_read = latte_read("latte_events")
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
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
            if message.guild == self.bot.latte:#only_image_channel
                only_image = self.json_read["only-image"]
                if message.channel.id == only_image:
                    if message.content and message.attachments:
                        return
                    elif search(self.url_regex, message.content):
                        return
                    elif message.content:
                        await message.delete()
                
                #only_link_channel
                only_link = self.json_read["only-link"]
                if message.channel.id == only_link:
                    if search(self.url_regex, message.content):
                        return
                    else:
                        await message.delete()

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
                
                if message.content.startswith(('latte','ลาเต้')):
                    stick = self.bot.get_sticker(872931348912947261)
                    await message.channel.send(content="เรียกเราหยอออ?", stickers = [stick])
            
                if message.content.startswith(('invite','invites','เชิญ','autorole')):
                    await message.reply('https://discord.gg/jhK46N6QWU\n**Auto role** : <@&842309176104976387>', allowed_mentions=discord.AllowedMentions.none(), mention_author=False, delete_after=600)
                
                # if message.content.startswith('tempinvite'):
                #     await message.delete()
                #     await message.channel.send('https://discord.gg/f6adY5B8k2' , delete_after=60)

                if message.channel.id == self.tempx[0]:
                    await asyncio.sleep(60)
                    await message.delete()

        except (discord.Forbidden, discord.NotFound, discord.HTTPException):
            pass
        except Exception as ex:
            print(ex)

    @commands.command(name='template', aliases=['lt'], help="latte server template")
    @commands.guild_only()
    @is_latte_guild()
    async def latte_template(self, ctx):
        if ctx.clean_prefix == "/":
            await ctx.reply('** **', ephemeral=True, mention_author=False)
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
        await ctx.reply(embed=embed, ephemeral=True, mention_author=False)
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
        await ctx.reply(embed=embed_send, mention_author=False)

    @commands.command(help="Move all members in your current channel")
    @commands.guild_only()
    async def move(self, ctx, to_channel:Literal['Totsuki','general','game','music - 1','music - 2','listen only','movie','working','afk',"don't know",'underworld','moonlight','angel','death','temp']=commands.Option(description="Spectify channel")):        
        try:
            now_channel = ctx.author.voice.channel
            in_channel = now_channel.members
        except:
            raise UserInputErrors('You must join a voice channel first.')
        
        to_channels = ctx.guild.get_channel(latte_voice[to_channel])
        if now_channel.id == to_channels.id:
            raise UserInputErrors(f'You cannot move from {now_channel.mention} to {to_channels.mention}.')

        try:
            for x in in_channel:
                await x.move_to(channel=to_channels)
        except discord.Forbidden:
            raise UserInputErrors("I don't have the permissions to move member")
        except discord.HTTPException as e:
            raise UserInputErrors(f'Failed to move member - {e}')
        except Exception as e:
            raise UserInputErrors(f'Failed to move member')
        
        embed = Embed(description = f'You moved `{len(in_channel)}` members to {to_channels.mention}')
        await ctx.reply(embed=embed, mention_author=False)

        
    
def setup(bot):
    bot.add_cog(Latte(bot))