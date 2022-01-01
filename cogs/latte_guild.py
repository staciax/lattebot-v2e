# Standard
import discord
import asyncio
import random
from discord.ext import commands
from typing import Literal
from re import search
from datetime import datetime, timedelta
# Third

# Local
from utils.json_loader import latte_read
from utils.checks import is_latte_guild, mystic_role
from utils.emoji import status_converter
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
        # while True:
        #     await asyncio.sleep(10)
        #     with open("data/spam_detect.txt", "r+") as file:
        #         file.truncate(0)

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='latte_icon_new', id=907030425011109888, animated=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild == self.bot.latte:
                #only image channel
                only_image = self.json_read["only-image"]
                if message.channel.id == only_image:
                    if message.content and message.attachments:
                        return
                    elif search(self.url_regex, message.content):
                        return
                    await message.delete()
                    # elif message.content:
                        
                #only_link_channel
                only_link = self.json_read["only-link"]
                if message.channel.id == only_link:
                    if search(self.url_regex, message.content):
                        return
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
                    sticker_list = [872926712776777768, 872922021036707901, 920521517035573259]
                    stick = self.bot.get_sticker(random.choice(sticker_list))
                    await message.channel.send(stickers = [stick])
                
                if message.content.startswith('shadowplay'):
                    stick = self.bot.get_sticker(878702176413810699)
                    await message.channel.send(stickers = [stick])
                
                if message.content.startswith(('เอาซันไลต์มาล้างตาดิ','เอาซันไลมา','ล้างตา','ซันไล','sunline')):
                    stick = self.bot.get_sticker(872926576847777842)
                    await message.channel.send(stickers = [stick], delete_after=30)
                
                if message.content.startswith(('latte','ลาเต้','ลาตู้','ลาติเอ้','ลาตี้','ลาติน่า','ลาติเอ้')):
                    stick = self.bot.get_sticker(random.choice([872921663803621406, 872927105799843871, 872931499324887070, 872933457418940466]))
                    await message.channel.send(content="เรียกเราหยอออ?", stickers = [stick], delete_after=30)
            
                if message.content.startswith(('invite','invites','เชิญ','autorole','latterole')):
                    await message.reply('https://discord.gg/jhK46N6QWU\n**Auto role** : <@&842309176104976387>', allowed_mentions=discord.AllowedMentions.none(), mention_author=False, delete_after=600)
                
                # if message.content.startswith('','น้องปอน','ปอน'):
                #     await message.channel.send(random.choice(['เด็กดี','อย่าบูลี้ดิ','รักคนดูนะครับ','น้ำยาหมดละ','สวัสดีครับ น๊องๆ !']))

                if message.content.startswith(('แรงค์', 'แร้ง', 'วาโล', 'เอเปก', 'rank', 'ปอนลงแรงค์', 'ลงแรงค์', 'ปอนลงแร้ง')):
                    choice_list = random.choice(['เล่นด้วยๆ แต่เราขอกินข้าวก่อนนะ', 'ลืมรากเหง้าแล้ววว', 'แม่เรียกกินข้าวไปละ', 'ลงแรงค์ไรค้าบ ไม่เอาา', 'ลงแรงค์ไรค้าบคุณ', 'ดูก่อนๆ', 'อย่าบอกใครนะ'])
                    await message.channel.send(choice_list, delete_after=60)
                    
                # if message.content.startswith('tempinvite'):
                #     await message.delete()
                #     await message.channel.send('https://discord.gg/f6adY5B8k2', delete_after=60)

                if message.channel.id == self.tempx[0]:
                    await asyncio.sleep(60)
                    await message.delete()

                # def _check(m):
                #     return (m.author == message.author
                #             and len(m.mentions)
                #             and (datetime.utcnow() - m.created_at).seconds < 30)
                
                # if not message.author.bot:
                #     if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 4:
                #         embedspam = discord.Embed(description="Don't spam mentions!", color=0xffffff)
                #         await message.channel.send(embed=embedspam, delete_after=10)
                
                # if message.author != self.bot.renly and not message.author.bot:                             
                #     counter = 0
                #     with open("data/spam_detect.txt", "r+") as file:
                #         for lines in file:
                #             if lines.strip("\n") == str(message.author.id):
                #                 counter+=1

                #         file.writelines(f"{str(message.author.id)}\n")
                #         if counter > 7:
                #             future_date = datetime.utcnow() + timedelta(seconds=60)
                #             await message.author.edit(timeout_until=future_date, reason='spam detect')
                            
        except (discord.Forbidden, discord.NotFound, discord.HTTPException):
            pass
        except Exception as ex:
            print(f'on_message - {ex}')

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
    async def color(self, ctx, color=commands.Option(description="Specify the color you want to change. (Color such as #ffa01b, #e8476a, f1eee6, ffa01b)")):
        member = ctx.author
        guild = ctx.guild
        if color.startswith('#'):
            color = color.replace('#', '')
        color_name = f'#{color}'
            
        try:
            color_int = int(color, 16)
        except:
            raise UserInputErrors('Color is valid (Color such as #ffa01b, #e8476a, f1eee6, ffa01b)')
        
        request = await self.bot.session.get(f'https://api.color.pizza/v1/?values={color}')
        api = await request.json()
        if request.status == 200:
            color_name = api.get('colors')[0].get('name')
        final_name = f'⠀{color_name.lower()} ♡ ₊˚'

        data = await self.bot.custom_roles.find_by_custom({"id": member.id})            
        if data is None:        
            color_bar = guild.get_role(854506876674244608).position
            role = await guild.create_role(name=final_name, color=color_int)
            data = {
                "id" : member.id,
                "role_id": role.id
            }
            positions = {role: color_bar}
            await guild.edit_role_positions(positions=positions)
            await member.add_roles(role)

            await self.bot.custom_roles.update_by_custom({"id": member.id}, data)
            embed = discord.Embed(description=role.mention, color=color_int)
            return await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none(), mention_author=False)

        role_id = int(data["role_id"])
        role = guild.get_role(role_id)
        await role.edit(name=final_name, color=color_int)
        embed = discord.Embed(description=role.mention, color=color_int)
        await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none(), mention_author=False)
    
    @commands.command(help="remove custom role color")
    @commands.guild_only()
    @is_latte_guild()
    async def color_remove(self, ctx):
        member = ctx.author
        guild = ctx.guild
        
        data = await self.bot.custom_roles.find_by_custom({"id": member.id})            
        if data is None:        
            raise UserInputErrors("You don't have custom color role")

        role_id = int(data["role_id"])
        role = guild.get_role(role_id)
        embed = discord.Embed(description=f'**Successfully removed:** {role.mention}', color=role.color or 0xffffff)
        data_deleted = await self.bot.custom_roles.delete_by_custom({"id": member.id})
        if data_deleted and data_deleted.acknowledged:
            await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none(), mention_author=False)
            await role.delete()
        else:
            raise UserInputErrors("I could not remove your custom color")
        
    @commands.command(help="Move all members in your current channel")
    @commands.guild_only()
    @is_latte_guild()
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
    
    @commands.command(name="status", help="Shows status about the specified member.")
    @commands.guild_only()
    @is_latte_guild()
    async def status_(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):

        member = member or ctx.guild.get_member(ctx.author.id)
        #member_status
        m_mobile = f"{status_converter(str(member.mobile_status))} Moblie"
        m_desktop = f"{status_converter(str(member.desktop_status))} Desktop"
        m_Web = f"{status_converter(str(member.web_status))} Web"
        #embed
        embed = discord.Embed(color=member.colour)
        embed.set_author(name=member, icon_url=ctx.author.avatar or ctx.author.default_avatar)
        embed.description = f"{m_desktop}\n{m_mobile}\n{m_Web}"
        await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(name="giverole", help="Latte give verify role")
    @commands.guild_only()
    @is_latte_guild()
    @mystic_role()
    async def autorole(self, ctx):
        sort_member = [g for g in sorted(ctx.guild.members, key=lambda g: g.joined_at, reverse=True)]
        member = sort_member[0]
        latte_roles = self.bot.latte.get_role(842309176104976387)
        bar_role = self.bot.latte.get_role(854503426977038338)
        if latte_roles not in member.roles:
            await member.add_roles(latte_roles, bar_role)
            chat_channel = self.bot.latte.get_channel(861883647070437386)
            embed = discord.Embed(color=0xffffff)
            embed.description = f'{member.mention} gets a role {latte_roles.mention}'
            await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())
            return await chat_channel.send(f'୨୧・━━⋄✩ ₊ ˚・\nwelcome to our latte . .\n⸝⸝・{member.mention}', allowed_mentions=discord.AllowedMentions.none())
        raise UserInputErrors("Member's already have a mute role.")
    
    @commands.command(name="reactionrole")
    @commands.guild_only()
    @commands.is_owner()
    async def reactionrole(self, ctx):
        blank = '<:blank:926496177418043392>'
        
        embed1 = discord.Embed(color=0xffffff)
        embed1.title=f'> {blank} <:bubblegumheartu:903339950353813595> <:blueberryheartu:903339950337032212> **C o l o r s** <a:bw_white_Hearts_White:859399024558080020>'
        embed1.description = '<a:dp_arrowright:926495510372683796> Choose your favourite color!\n'
        embed1.description += f'{blank} ﹒﹒﹒﹒ <:chocolateheartu:903339950223806526> ﹒﹒﹒﹒\n'
        
        embed1.description += f'{blank} <emoji_color> <role>\n'

        embed1.description += f'{blank} ﹒﹒﹒﹒ <:chocolateheartu:903339950223806526> ﹒﹒﹒﹒\n'

        await ctx.send(embed=embed1, allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(Latte(bot))