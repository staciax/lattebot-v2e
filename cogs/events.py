# Standard
import discord
import random
import datetime
import io
import asyncio
import contextlib
from discord import Embed
from discord.ext import commands , tasks
from datetime import datetime, timezone , timedelta
from re import search

# Third
# from googletrans import Translator

# Local
from utils.json_loader import latte_read
from utils.converter import status_icon, find_invite_by_code
from utils.formats import format_dt

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, 'commands_used'):
            self.bot.commands_used = 0
        self.json_read = latte_read("latte_events")
        self.latte_chat = [861883647070437386, 840398821544296480]
        self.latte_bot = [861874852050894868, 840381588704591912, 844462710526836756]
        self.secret_channel = 886966133176017017
        self.secret_users = [240059262297047041, 240137834349068290, 188653422864498688, 240350375201341442, 687174446263304324, 507870438135955464] #371230466319187969
        self.underworldx = [873677543453126676, 873679362082369546]
        self.moonlightx = [875037193196945409, 875038018736644166]
        self.deathx = [883025077610876958, 883059509810040884]
        self.angelx = [873696566165250099, 883027485455941712]
        self.tempx = [879260123665682482, 879260241286549525]
        self.translatex = 882993073364279326
        self.total_ = 0
        self.member_ = 0
        self.bot_ = 0
        self.role_ = 0
        self.channel_ = 0
        self.text_ = 0
        self.voice_ = 0
        self.boost_ = 0
        self.counted.start()
        self.afk_check.start()
        self.clear_message_log.start()
        
    def cog_unload(self):
        self.counted.cancel()
        self.afk_check.cancel()
        self.clear_message_log.cancel()
    
    @commands.Cog.listener()
    async def on_ready(self):
        # self.latte_invite_code = await self.latte.invites()
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')

    @tasks.loop(hours=1)
    async def counted(self):
        try:
            guild = self.bot.get_guild(self.bot.latte_guild_id)
            total_count = guild.member_count
            if self.total_ != total_count:
                self.total_ = total_count
                total_channel = guild.get_channel(876738880282431489)
                total_name = f"ᴛᴏᴛᴀʟ‌・{self.total_}"
                await total_channel.edit(name=total_name)
            
            member_count = len([member for member in guild.members if not member.bot])
            if self.member_ != member_count:
                self.member_ = member_count
                member_channel = guild.get_channel(876712142160678923)
                member_name = f"ᴍᴇᴍʙᴇʀs・{self.member_}"
                await member_channel.edit(name=member_name)

            bot_count = len([Member for Member in guild.members if Member.bot])
            if self.bot_ != bot_count:
                self.bot_ = bot_count
                bot_channel = guild.get_channel(876724022686150687)
                bot_name = f"ʙᴏᴛs‌・{self.bot_}"
                await bot_channel.edit(name=bot_name)
            
            role_count = len(guild.roles)
            if self.role_ != role_count:
                self.role_ = role_count
                role_channel = guild.get_channel(876712169662742588)
                role_name = f"ʀᴏʟᴇs‌・{self.role_}"
                await role_channel.edit(name=role_name)
            
            channel_count = len(guild.channels)
            if self.channel_ != channel_count:
                self.channel_ = channel_count
                channel_channel = guild.get_channel(876712200214024192)
                channel_name = f"ᴄʜᴀɴɴᴇʟs・{self.channel_}"
                await channel_channel.edit(name=channel_name)
            
            text_channel_count = len(guild.text_channels)
            if self.text_ != text_channel_count:
                self.text_ = text_channel_count
                text_channel = guild.get_channel(876740437505871922)
                text_name = f"ᴛᴇxᴛ・{self.text_}"
                await text_channel.edit(name=text_name)
            
            voice_channel_count = len(guild.voice_channels)
            if self.voice_ != voice_channel_count:
                self.voice_ = voice_channel_count
                voice_channel = guild.get_channel(876740515863879711)
                voice_name = f"ᴠᴏɪᴄᴇ・{self.voice_}"
                await voice_channel.edit(name=voice_name)
            
            boost_count = guild.premium_subscription_count
            if self.boost_ != boost_count:
                self.boost_ = boost_count
                boost_channel = guild.get_channel(876737270051389470)
                boost_name = f"ʙᴏᴏꜱᴛꜱ・{self.boost_}"
                await boost_channel.edit(name=boost_name)
        except:
            pass

    @counted.before_loop
    async def before_counted(self):
        await self.bot.wait_until_ready()

    #ต้องเอาออกในอนาคต
    @tasks.loop(minutes=30)
    async def afk_check(self):
        try:
            if self.bot.afk_user or len(self.bot.afk_user):
                return

            guild = self.bot.get_guild(self.bot.latte_guild_id)
            member_all = guild.members
            for x in member_all:
                if x.display_name.startswith('[AFK]'):
                    await x.edit(nick=None)
        except:
            pass

    @afk_check.before_loop
    async def before_afk_check(self):
        await self.bot.wait_until_ready()
    
    #clear_message_log_latte_guild
    @tasks.loop(hours=1)
    async def clear_message_log(self):
        def is_me(m):
            return m.author.id != 240059262297047041
        guild = self.bot.latte
        message_log = guild.get_channel(self.json_read["message-log"])
        time = (datetime.utcnow() + timedelta(seconds=25200)).strftime("%H")
        if int(time) == 0:
            try:
                await message_log.purge(limit=15, check=is_me)
            except Exception as Ex:
                print(f"Error clear message-log : {Ex}")
            # except discord.Forbidden:
            #     pass
            # except discord.HTTPException:
            #     pass
            
    @clear_message_log.before_loop
    async def before_clear_message_log(self):
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener()
    async def on_command(self, ctx):

        if ctx.author.id in [240059262297047041, 879361086724386837, 834834946832203776]:
            return

        self.bot.commands_used = self.bot.commands_used +1
        channel_log = self.bot.get_channel(self.bot.latte_log_id)
        
        if ctx.guild == self.bot.latte:
            return

        server = ctx.guild
        channel = ctx.channel
        owner = ctx.guild.owner
        author = ctx.author
        message = ctx.message
                
        embed = discord.Embed(color=self.bot.white_color, timestamp=discord.utils.utcnow())
        

        embed.description = f"[**{ctx.command}**](https://discord.gg/hE8x7S2fR5 '{message.content}') - has been used\n"
        embed.add_field(name="Server:",value=f"Name: {server} | `{server.id}`\nOwner: {owner} | `{owner.id}`", inline=False)
        embed.add_field(name="User:",value=f"Name: {author} | `{author.id}`", inline=False)
        
        await channel_log.send(embed=embed)
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith((f'.afk',f'{self.bot.defaul_prefix}afk',f'/afk')):
            return
                    
        for user_id in self.bot.afk_user.keys():
            if message.author.id == user_id:
                try:
                    await message.author.edit(nick=self.bot.afk_user[user_id]['name'])
                except:
                    pass
                del self.bot.afk_user[user_id]
                embed_back = discord.Embed(color=self.bot.white_color)
                embed_back.description = f"Welcome back {message.author.mention} , i've removed your **AFK** status."
                return await message.channel.send(embed=embed_back, delete_after=15)
            
            member = message.guild.get_member(user_id)
            if member.mentioned_in(message):
                embed = discord.Embed(description=f'**{member.display_name}** is afk for: {self.bot.afk_user[user_id]["reason"]}' , color=self.bot.white_color)
                await message.channel.send(embed=embed, delete_after=15)
                    
        # #google_translator
        # if message.channel.id == self.translatex:
        #     translator = Translator()
        #     try:
        #         result =  translator.translate(f'{message.clean_content}' , dest='th')
        #     except:
        #         return await message.channel.send("An unknown error occurred, sorry" , delete_after=10)

        #     await message.channel.send(result.text)
        #     # await message.reply(result.text)

    @commands.Cog.listener()
    async def on_message_edit(self, before , after):   
        if after.author.bot:
            return
        if before.channel.id in self.latte_chat:
            try:
                self.message_log = self.bot.get_channel(self.json_read["message-log"])
                if self.message_log is None:
                    print("on_message_edit error")
                    return

                if before.content != after.content:
                    embed = discord.Embed(description=f"**Edited in**: {after.channel.mention}\n**Message link:** ||[click]({after.jump_url})||",
                                colour=0xFF8C00, 
                                timestamp=datetime.now(timezone.utc))
                    if after.author.avatar is not None:           
                        embed.set_author(name=after.author.display_name , url=after.jump_url ,icon_url=after.author.avatar.url)
                    else:
                        embed.set_author(name=after.author.display_name , url=after.jump_url)
                    embed.set_footer(text="Message edit")
                    embed.add_field(name="**Before**", value=f"```{before.content}```", inline=False)
                    embed.add_field(name="**After**", value=f"```{after.content}```", inline=False)
                    
                    await self.message_log.send(embed=embed)
            
            except TypeError: 
                pass
            
            except KeyError: 
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):                   
        # if message.author.bot:
        #     return

        #snipe
        if message.content.startswith(f'{self.bot.defaul_prefix}snipe'):
            return

        self.bot.sniped[message.guild.id] = message, message.content , message.author , message.channel , message.created_at 
    
        if message.embeds:
            if message.author == self.bot:
                return
            self.bot.sniped_embed[message.guild.id] = message.embeds[0], message.content or None

        #latte_log_message
        self.message_log = self.bot.get_channel(self.json_read["message-log"])
    
        try:
            if self.message_log is None:
                print("on_message_delete error")
                return

            if message.author.bot:
                return
            
            if message.channel.id in self.latte_chat:
                im = None
                # if message.guild.id == self.bot.latte_guild_id:
                embed = discord.Embed(color=0xDC143C , timestamp=datetime.now(timezone.utc))
                if message.author.avatar is not None:
                    embed.set_author(name=message.author.display_name, url=message.jump_url , icon_url=message.author.avatar.url)
                else:
                    embed.set_author(name=message.author.display_name, url=message.jump_url)

                if message.content is not None and len(message.content) != 0:
                    embed.description = f"**Deleted in:** {message.channel.mention}"
                    embed.add_field(name=f"**Content:**", value=f"```{message.clean_content}```", inline=False)
                    embed.set_footer(text="Message delete")

                if message.attachments is not None:
                    if len(message.attachments) > 1:
                        im = [x.proxy_url for x in message.attachments]
                        embed.add_field(name='\uFEFF',value = f"This Message Contained {len(message.attachments)} Message Attachments, Please see below.")
                        # await self.message_log.send(' '.join(im))
                        # return await self.message_log.send(embed=embed)

                    elif message.attachments:
                        image = message.attachments[0].proxy_url
                        embed.description = f"**Deleted in:** {message.channel.mention}"
                        embed.set_image(url=image)
                        embed.set_footer(text="Message delete")

                await self.message_log.send(embed=embed)
                if im is not None:
                    await self.message_log.send(' '.join(im))

                if message.embeds:
                    embed_del = message.embeds[0]
                    await self.message_log.send(content=message.clean_content or None, embed=embed_del)
                
        except TypeError: 
            pass
        
        except KeyError: 
            pass
      
    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     self.welcome = self.bot.get_channel(self.json_read["welcome_channel"])
    #     self.welcome_image = self.json_read["welcome_image"]
    #     self.welcome_footer = self.json_read["welcome_footer"]
        
    #     try:
    #         if self.welcome is None:
    #             print("on_member_join error")
    #             return

    #         if member.guild.id == self.bot.latte_guild_id:
    #             embed=discord.Embed(
    #                         description=f"**Welcome to ₊˚ {member.guild.name}**\n\n₊˚don’t forget to check out . . .\n﹒<#861883647070437386> \n﹒<#840380566862823425>", 
    #                         timestamp=datetime.now(timezone.utc),
    #                         color=0xCCCCFF
    #             )

    #             embed.set_author(name=member)
    #             if member.avatar is not None:
    #                 embed.set_author(name=member, icon_url=member.avatar.url)
    #                 embed.set_thumbnail(url=member.avatar.url)
                
    #             if self.welcome_image is not None:
    #                 embed.set_image(url=self.welcome_image)

    #             # embed.set_thumbnail(url=member.guild.icon.url)
                
    #             footer_text = f"You're our {member.guild.member_count} members ෆ"
    #             if self.welcome_footer is not None:
    #                 embed.set_footer(text=footer_text, icon_url=self.welcome_footer)
    #             else:
    #                 embed.set_footer(text=footer_text)

    #             try:
    #                 invites_before_join = self.latte_invite_code
    #                 invites_after_join = await member.guild.invites()
    #                 if invites_before_join:
    #                     for invite in invites_before_join:
    #                         if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
    #                             if invite.code == 'jhK46N6QWU':
    #                                 latte_roles = discord.utils.get(member.guild.roles, id = 842309176104976387) #name="Latte・・ ♡")
    #                                 bar_role = discord.utils.get(member.guild.roles, id = 854503426977038338) #name="・ ───────꒰ ・ ♡ ・ ꒱─────── ・")
    #                                 await member.add_roles(latte_roles, bar_role)
    #                                 chat_channel = self.bot.latte.get_channel(861883647070437386)
    #                                 await chat_channel.send(f'୨୧・━━⋄✩ ₊ ˚・\nwelcome to our latte . .\n⸝⸝・{member.mention}', allowed_mentions=discord.AllowedMentions.none())
            
    #             except Exception as es:
    #                 print(es)
    #                 pass

    #             if member.bot:
    #                 role = discord.utils.get(member.guild.roles, id=840677855460458496)
    #                 if role:
    #                     await member.add_roles(role)
    #             await self.welcome.send(embed=embed)
        
    #     except TypeError: 
    #         pass
        
    #     except KeyError: 
    #         pass
            
    #     except Exception as ex:
    #         print(ex)

    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     self.welcome = self.bot.get_channel(self.json_read["welcome_channel"])
    #     self.leave = self.bot.get_channel(self.json_read["leave_channel"])

    #     if member.guild.id == self.bot.latte_guild_id:
        
    #         embed = discord.Embed()
    #         embed.color = 0xDEBA9D
    #         embed.description = f"**{member.name}** see you next time ♡"

    #         await self.welcome.send(embed=embed)
            
    #         embed_log = discord.Embed(
    #                     description=f"**Leave Server\n`{member}`**",
    #                     color=0xdbd7d2)
    #         # if member.avatar.url is not None:
    #         #     embed_log.set_thumbnail(url=member.avatar.url)
    #         if member.avatar is not None:
    #             embed_log.set_thumbnail(url=member.avatar or member.default_avatar)
    #         embed_log.set_footer(text="—・see you next time ♡")
    #         embed_log.timestamp = datetime.now(timezone.utc)

    #         await self.leave.send(embed = embed_log)
    
    @commands.Cog.listener()
    async def on_invite_update(self, member, invite):
        self.server_log = self.bot.get_channel(self.json_read["server-log"])
        try:
            if self.server_log is None:
                print("on_invite_update error")
                return
            
            if member.guild.id == self.bot.latte_guild_id:

                self.latte_invite_code = await self.bot.latte.invites()
                
                embed = discord.Embed(color=self.bot.white_color)
                embed.title = "Member joined"
                embed.add_field(name=f"Name", value=f"{member.name}", inline=False)
                embed.add_field(name=f"Created at", value=f"{format_dt(member.created_at, style='F')} ({format_dt(member.created_at, style='R')})", inline=False)
                embed.set_footer(text=f"{member.guild.member_count}th to join")

                if invite:
                    expiresAt = "Never" if not invite.expires_at else format_dt(invite.expires_at)
                    values = f"Inviter: {invite.inviter} **|** {invite.inviter.mention}"
                    values =+ f"\nInvite code: [{invite.code}]({invite.url})"
                    values =+ f"\nExpires at: {expiresAt}\nUses: {invite.uses}"
                    
                    if invite:
                        embed.add_field(name="Invited by:", value=values)

                await self.server_log.send(embed=embed)
            
        except TypeError: #if  no records found for that guild
            pass
        
        except KeyError: # records exist but not set up a logging channel
            pass
            
        except Exception as Ex:
            print(f'on_invite_update - {Ex}')

    @commands.Cog.listener()
    async def on_invite_create(self, invite:discord.Invite):
        self.server_log = self.bot.get_channel(self.json_read["server-log"])
        try:
            if self.server_log is None:
                print("on_invite_create error")
                return
                
            if invite.guild.id == self.bot.latte_guild_id:

                self.latte_invite_code = await self.bot.latte.invites()

                expiresAt = "Never" if not invite.expires_at else format_dt(invite.expires_at)
                max_use_count = "Unlimited" if invite.max_uses == 0 else invite.max_uses
                                
                embed = discord.Embed(title=f"Created an invite.", timestamp=datetime.now(timezone.utc), colour=self.bot.white_color)
                embed.add_field(name="Inivte Code:", value=f"||{invite.code}||")
                embed.add_field(name=f"Expires", value=f"{expiresAt}")
                embed.add_field(name="Max Uses:", value=f"{max_use_count}")
                embed.add_field(name="Channel:", value=f"#{invite.channel}")
                # embed.add_field(name=f"temporary membership?", value=f"{ctx.tick(invite.temporary)}")
                if invite.inviter.avatar is not None:
                    embed.set_footer(text = f'Created by {invite.inviter.name}', icon_url =invite.inviter.avatar.url)
                else:
                    embed.set_footer(text = f'Created by {invite.inviter.name}')
                await self.server_log.send(embed=embed)
        
        except TypeError: #if  no records found for that guild
            pass
        
        except KeyError: # records exist but not set up a logging channel
            pass
            
        except Exception as Ex:
            print(f'on_invite_create - {Ex}')
    
    # @commands.Cog.listener()
    # async def on_user_update(self, before, after):
    #     #load_json
    #         self.server_log = self.bot.get_channel(self.json_read["server-log"])

    #         if self.server_log is None:
    #             print("on_user_update error")
    #             return
            
    #         if self.bot.latte not in before.mutual_guilds:
    #             return

    #         #username_log
    #         if before.name != after.name:
    #             embed = discord.Embed(title="Username change",colour=after.colour, timestamp=datetime.now(timezone.utc))  
    #             embed.add_field(name="**Before**", value=f"```{before.name}```", inline=False)
    #             embed.add_field(name="**After**", value=f"```{after.name}```", inline=False)

    #             if after.avatar is not None:
    #                 embed.set_thumbnail(url=after.avatar.url)
    #                 embed.set_footer(text=after, icon_url=after.avatar.url)
    #             else:
    #                 embed.set_footer(text=after)
            
    #             await self.server_log.send(embed=embed)

    #         #discriminator_log
    #         if before.discriminator != after.discriminator:
    #             embed = discord.Embed(title="Discriminator change",
    #                                 colour=0xffffff, #after.colour
    #                                 timestamp=datetime.now(timezone.utc))

    #             embed.add_field(name="**Before**", value=f"```#{before.discriminator}```", inline=False)
    #             embed.add_field(name="**After**", value=f"```#{after.discriminator}```", inline=False)
                
    #             if after.avatar is not None:
    #                 embed.set_footer(text=after, icon_url=after.avatar)
    #             else:
    #                 embed.set_footer(text=after)
            
    #             await self.server_log.send(embed=embed)

    #         #avatar_log
    #         if before.avatar != after.avatar:
    #             embed = discord.Embed(title="Avatar change", colour=0xf3d4b4, timestamp=datetime.now(timezone.utc))
    #             try:
    #                 embed.set_thumbnail(url=before.avatar.url)
    #                 embed.description = "New image is below, old to the right."
    #             except:
    #                 pass
    #             embed.set_image(url=after.avatar.url)
    #             embed.set_footer(text=after, icon_url=after.avatar.url)

    #             await self.server_log.send(embed=embed)
    
    # @commands.Cog.listener()
    # async def on_member_update(self, before, after):
        
    #     if before.guild.id == self.bot.latte_guild_id:
    #         #load_json
    #         self.server_log = self.bot.get_channel(self.json_read["server-log"])
    #         self.roles_log = self.bot.get_channel(self.json_read["role-log"])

    #         if self.server_log is None and self.roles_log is None:
    #             print("on_member_update error")
    #             return

    #         #nickname_log
    #         if before.display_name != after.display_name:
    #             embed = discord.Embed(title="Nickname change",
    #                                 colour=0xFFDF00, #colour=after.colour,
	# 					            timestamp=datetime.now(timezone.utc))                               
                
    #             embed.add_field(name="**Before**", value=f"```{before.display_name}```", inline=False)
    #             embed.add_field(name="**After**", value=f"```{after.display_name}```", inline=False)

    #             if after.avatar is not None:    
    #                 embed.set_thumbnail(url=after.avatar.url)
    #             # embed.set_footer(text="", icon_url=after.avatar.url)

    #             await self.server_log.send(embed=embed)

    #         #role_log
    #         elif before.roles != after.roles:
    #             new_role = [x.mention for x in after.roles if x not in before.roles]
    #             old_role = [x.mention for x in before.roles if x not in after.roles]
    #             update_role = new_role[0] if new_role else old_role[0]
    #             if update_role == '<@&886193080997384222>':
    #                 return
    #             member_role = ' '.join(reversed([r.mention for r in after.roles if r.name != '@everyone']))
                
    #             values = "**NEW**" if new_role else "**REMOVE**"
    #             color_embed = discord.Colour.green() if new_role else discord.Colour.red()

    #             embed = discord.Embed(colour=color_embed, timestamp=datetime.now(timezone.utc))
    #             embed.set_author(name=f"{after.display_name} | Roles update")
    #             if after.avatar is not None:
    #                 embed.set_author(name=f"{after.display_name} | Roles update", icon_url=after.avatar.url)
                
    #             if update_role and member_role:
    #                 embed.add_field(name="**ROLE**", value=member_role or '\u200B', inline=False)
    #                 embed.add_field(name=values, value=update_role, inline=False)
    #                 await self.roles_log.send(embed=embed)

    #         elif before.display_avatar != after.display_avatar:
    #             embed = discord.Embed(title="Server avatar change", colour=0xf3d4b4, timestamp=datetime.now(timezone.utc))
    #             embed.description = "New image is below, old to the right."
                
    #             if before.display_avatar is not None:
    #                 embed.set_thumbnail(url=before.display_avatar.url)
                
    #             if after.display_avatar is not None:
    #                 embed.set_image(url=after.display_avatar.url)
    #                 embed.set_footer(text=after, icon_url=after.display_avatar.url)
        
    #             await self.server_log.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after):
        self.voice_log = self.bot.get_channel(self.json_read["voice-log"])

        try:

            if self.voice_log is None:
                print("on_voice_state_update error")
                return

            if member.guild.id == self.bot.latte_guild_id:
                                
                if str(member.id) in self.bot.auto_kick_user.keys():
                
                    onlyfans_role = self.bot.latte.get_role(863434675133087746)
                    if onlyfans_role in member.roles:
                        return

                    try:
                        cooldown = self.bot.auto_kick_user[str(member.id)]['time']
                        current = datetime.timestamp(datetime.utcnow())
                        if cooldown > current:
                            await member.move_to(channel=None)
                        elif cooldown < current:
                            del self.bot.auto_kick_user[str(member.id)]
                    except Exception as e:
                        print(e)
                                
                embed = discord.Embed(timestamp=datetime.now(timezone.utc))
                if member.avatar is not None:
                    embed.set_footer(text=member , icon_url=member.display_avatar.url)
                else:
                    embed.set_footer(text=member)

                #voice_log
                if not before.channel and after.channel:
                    embed.description = f"**JOIN CHANNEL** : `{after.channel.name}`"
                    embed.color=0x77dd77            
                    await self.voice_log.send(embed=embed)
            
                if before.channel and not after.channel:
                    embed.description = f"**LEFT CHANNEL** : `{before.channel.name}`"
                    embed.color=0xd34e4e
                    await self.voice_log.send(embed=embed)
            
                if before.channel and after.channel: #and before.channel != after.channel
                    if before.channel.id != after.channel.id:
                        embed.description = f"**SWITCHED CHANNELS** : `{before.channel.name}` to `{after.channel.name}`"
                        embed.color=0xfcfc64
                        await self.voice_log.send(embed=embed)

                # stream_log           
                if before.self_stream != after.self_stream:
                    if after.self_stream:
                        embed.description = f"**STREAMING in `{before.channel.name}`**"
                        embed.colour=0x8A2BE2
                        await self.voice_log.send(embed=embed)
                    if before.self_stream:
                        embed.description = f"**LEAVE STREAMING**"
                        embed.colour=0x8A2BE2
                        await self.voice_log.send(embed=embed)
                
                # deaf_log      
                if before.deaf != after.deaf:
                    if after.deaf:
                        embed.description = f"**MEMBER DEAF**"
                        embed.colour=0xFF7878
                        await self.voice_log.send(embed=embed)
                    if before.deaf:
                        embed.description = f"**MEMBER UNDEAF**"
                        embed.colour=0x77dd77
                        await self.voice_log.send(embed=embed)

                if before.mute != after.mute:
                    if after.mute:
                        embed.description = f"**MEMBER MUTED**"
                        embed.colour=0xFF7878
                        await self.voice_log.send(embed=embed)
                    if before.mute:
                        embed.description = f"**MEMBER UNMUTED**"
                        embed.colour=0x77dd77
                        await self.voice_log.send(embed=embed)

                if after.channel is not None:
                    temp_channel = {
                        '873677543453126676': 873679362082369546,
                        '875037193196945409': 875038018736644166,
                        '873696566165250099': 883027485455941712,
                        '883025077610876958': 883059509810040884
                    }
                    with contextlib.suppress(Exception):
                        channel_move = temp_channel[str(after.channel.id)]
                        channel_voice =  member.guild.get_channel(channel_move)
                        return await member.move_to(channel_voice)

                    if after.channel.id == self.secret_channel:
                        if member.id in self.secret_users:
                            return
                        else:
                            await member.move_to(channel=None)
                   
        except TypeError: #if no records found for that guild
            pass

        except KeyError: # records exist but not set up a logging channel
            pass
            
        except Exception as Ex:
            print(f'on_voice_state_update - {Ex}')
        
    # @commands.Cog.listener()
    # async def on_presence_update(self, before, after):
    #     # role = discord.utils.find(lambda r: r.name == 'ᴴ ᴱ ᴸ ᴬ・・ ♡', guild.roles)

    #     #add_offline_role
    #     if before.guild.id == self.bot.latte_guild_id:
    #         try:
    #             # role = discord.utils.get(before.guild.roles, id = 886193080997384222)
    #             # if str(after.status) == "online" or "dnd" and "idle":
    #             #     await before.remove_roles(role)
    #             # if str(after.status) == "offline":
    #             #     await after.add_roles(role)

    #             #server_log
    #             self.status_log = self.bot.get_channel(self.json_read["status-log"])

    #             #status
    #             if before.status != after.status:
    #                 embed = discord.Embed(
    #                     colour=after.colour,
    #                     timestamp=datetime.now(timezone.utc)
    #                 )
    #                 if after.avatar is not None:
    #                     embed.set_author(name=after, icon_url=after.avatar.url)
    #                 else:
    #                     embed.set_author(name=after)
    #                 embed.set_footer(text=f"{str(after.status)}", icon_url=status_icon(after.status))
    #                 await self.status_log.send(embed=embed)
    #         except:
    #             pass
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channels = [channel for channel in guild.channels]
        roles = roles= [role for role in guild.roles]
        embed = Embed(title="Bot just joined: "+str(guild.name), color=self.bot.white_color)
        embed.add_field(name='Server Name:',value=f'{guild.name}')
        embed.add_field(name='Server ID:',value=f'{guild.id}')
        # embed.add_field(name='Server region:',value=f'{guild.region}')
        embed.add_field(name='Server Creation Date:',value=f'{format_dt(guild.created_at)}')
        embed.add_field(name='Server Owner:',value=f'{guild.owner}')
        embed.add_field(name='Server Owner ID:',value=f'{guild.owner_id}')
        embed.add_field(name='Member Count:',value=f'{guild.member_count}')
        embed.add_field(name='Amount of Channels:',value=f"{len(channels)}")
        embed.add_field(name='Amount of Roles:',value=f"{len(roles)}")

        if guild.icon:
            embed.set_thumbnail(url=guild.icon)    

        join_guild = self.bot.get_channel(self.bot.bot_join)
        await join_guild.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channels = [channel for channel in guild.channels]
        roles = roles= [role for role in guild.roles]
        embed = Embed(title="Bot just left: "+str(guild.name), color=self.bot.white_color)
        embed.add_field(name='Server Name:',value=f'{guild.name}')
        embed.add_field(name='Server ID:',value=f'{guild.id}')
        embed.add_field(name='Server Creation Date:',value=f'{format_dt(guild.created_at)}')
        embed.add_field(name='Server Owner:',value=f'{guild.owner}')
        embed.add_field(name='Server Owner ID:',value=f'{guild.owner_id}')
        try:
            embed.add_field(name='Member Count:',value=f'{guild.member_count}')
        except:
            pass
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon)    

        embed.add_field(name='Amount of Channels:',value=f"{len(channels)}")
        embed.add_field(name='Amount of Roles:',value=f"{len(roles)}")
        
        leave_guild = self.bot.get_channel(self.bot.bot_leave)
        await leave_guild.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))