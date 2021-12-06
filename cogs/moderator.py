# Standard
import discord
import datetime
import asyncio
import re
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from typing import Literal
import aiohttp
from io import BytesIO

# Third
import requests

# Local
from utils.mod_converter import do_removal , TimeConverter
from utils.paginator import SimplePages
from utils.useful import RenlyEmbed
from utils.checks import bypass_for_owner

class ModError(commands.CommandError):
    pass

class Mod(commands.Cog, command_attrs = dict(slash_command=True)):
    """Moderation related commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='mod', id=903339681779966042, animated=False)
    
    @commands.command(help="Create custom emoji with url")
    @commands.guild_only()
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def emoji_create(self, ctx, url:str = commands.Option(description="URL"), *, name = commands.Option(description="Emoji name")):
        guild = ctx.guild
        embed = discord.Embed()
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        embed.color = 0x77dd77
                        embed.description = f'Successfully created emoji: <:{name}:{emoji.id}>'
                        await ctx.send(embed=embed)
                        await ses.close()
                    else:
                        raise ModError(f'Error when making request | {r.status} response.')
                except discord.HTTPException:
                    raise ModError(f'File size is too big!')
    
    @commands.command(help="Remove custom emoji from server")
    @commands.guild_only()
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def emoji_remove(self, ctx, emoji:discord.Emoji = commands.Option(description="Spectify Emoji")):
        embed = discord.Embed()
        try:
            embed.color = 0x77dd77
            embed.description = f'Successfully deleted : {emoji}'
            await ctx.send(embed=embed)
            await emoji.delete()
        except:
            raise ModError('Error delete emoji!')

    @commands.command(name="kick", help="kick member from your server")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.dynamic_cooldown(bypass_for_owner)
    async def kick(self, ctx, member: discord.Member = commands.Option(description="Member"), *, reason= commands.Option(default=None, description="Reason")):
        if member == self.bot.user:
            raise ModError("You can't kick bot")
        
        if member == ctx.author:
            raise ModError("You can't kick yourself.")
        
        if member == ctx.guild.owner:
            raise ModError("You can't kick owner.")

        embed = discord.Embed(description=f'Member {member.mention} has been Kicked\nReason : {reason}', color=self.bot.white_color)
        
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            raise ModError('Unable to kick user.')
        except discord.HTTPException:
            raise ModError(f'Kick **{member}** is Failed')
        except Exception:
            raise ModError(f'Kick **{member}** is Failed')

    @commands.command(help="ban member from your server")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.dynamic_cooldown(bypass_for_owner)
    async def ban(self, ctx, member: discord.Member = commands.Option(description="Member"), *, reason= commands.Option(default=None, description="Reason")):
        if member == self.bot.user:
            raise ModError("You can't ban the bot")
        
        if member == ctx.author:
            raise ModError("You can't ban yourself.")
        
        if member == ctx.guild.owner:
            raise ModError("You can't ban owner.")

        embed = discord.Embed(description=f'{member} has been banned from server\nReason: {reason}', timestamp=datetime.now(timezone.utc),color=0xffffff)
        if ctx.author.display_avatar.url is not None: 
            embed.set_footer(text=f"Banned by {ctx.author}" , icon_url = ctx.author.display_avatar.url)
        else:
            embed.set_footer(text=f"Banned by {ctx.author}")
       
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            raise ModError('Unable to ban user.')
        except discord.HTTPException:
            raise ModError(f'Ban **{member}** is Failed')
        except Exception:
            raise ModError(f'Ban **{member}** is Failed')
    
    @commands.command(help="Gets the current guild's list of bans")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def bans(self, ctx) -> discord.Message:
        bans = await ctx.guild.bans()
        if not bans:
            return await ctx.send(embed=discord.Embed(description="There are no banned users in this server",color=self.bot.white_color))
        ban_list = []
        for ban_entry in bans:
            ban_list.append(f"{ban_entry.user}")
        p = SimplePages(entries=ban_list, per_page=10, ctx=ctx)
        p.embed.title = "Bans list"
        p.embed.color = self.bot.white_color
        await p.start()

    @commands.command(help="purge message")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    @commands.dynamic_cooldown(bypass_for_owner)
    async def purge(self, ctx, amount : int = commands.Option(description="Number to clear message")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)

        if amount> 500 or amount <0:
            raise ModError('Invalid amount. Maximum is 500')
        try:
            deleted = await ctx.channel.purge(limit=amount)            
        except discord.Forbidden:
            raise ModError("You do not have permissions to purge message")
        except discord.HTTPException:
            raise ModError("Purging the messages failed.")
        
        embed = discord.Embed(
                description=f" `#{ctx.channel.name}`: **{len(deleted)}** messages were cleared",
                color=self.bot.white_color
            )
        await ctx.send(embed=embed, ephemeral=True, delete_after=15)
    
    # @commands.command(help="Cleanup the bot's messages")
    # @commands.guild_only()
    # @commands.has_permissions(manage_messages=True)
    # @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    # async def cleanup(self, ctx , amount : int = commands.Option(description="Number to cleanup bot's message")):
    #     embed = discord.Embed(color=self.bot.white_color)
    #     try:
    #         await do_removal(self, ctx=ctx, limit=amount, predicate=lambda e: e.author == ctx.me)
    #         embed.description=f"`{ctx.channel.name}` : **{amount}** bot's messages were cleared"
    #     except:
    #         embed.description=f"i can't cleanup messages"
    #     await ctx.reply(embed=embed , ephemeral=True)

    @commands.command(help="clear the messages")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    @commands.dynamic_cooldown(bypass_for_owner)
    async def clear(
            self,
            ctx,
            type: Literal["all","message without pinned","bot","attachments","embed","custom emoji"] = commands.Option(description="choose type to clean message"),
            search:int = commands.Option(default=15, description="amount to search message / default = 15")
        ):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)

        embed = discord.Embed(color=self.bot.white_color)

        if type == "message without pinned":
            try:
                await do_removal(self, ctx, search, lambda e: not e.pinned)
                embed.description=f"`{ctx.channel.name}` : message NOT pinned were cleared"
            except:
                raise ModError("i can't cleanup messages")
        
        if type == "bot":
            try:
                await do_removal(self, ctx, search, lambda e: e.author.bot)
                embed.description=f"`{ctx.channel.name}` : bot message were cleared"
            except:
                raise ModError("i can't cleanup bot messages")
        
        if type == "attachments":
            try:
                await do_removal(self, ctx, search, lambda e: len(e.attachments))
                embed.description=f"`{ctx.channel.name}` : message attachments were cleared"
            except:
                raise ModError(f"i can't cleanup messages attachments")
        
        if type == "embed":
            try:
                await do_removal(self , ctx , search, lambda e: len(e.embeds))
                embed.description=f"`{ctx.channel.name}` : embed were cleared"
            except:
                raise ModError(f"i can't cleanup embed")
                
        if type == "custom emoji":
            custom_emoji = re.compile(r'<a?:[a-zA-Z0-9_]+:([0-9]+)>')
            def predicate(m):
                return custom_emoji.search(m.content)
            try:
                await do_removal(self, ctx, search, predicate)
                embed.description=f"`{ctx.channel.name}` : emoji were cleared"
            except:
                raise ModError(f"i can't custom emoji message")
    
        if type == "all":
            try:
                await do_removal(self, ctx, search, lambda e: True)
                embed.description=f"`{ctx.channel.name}` : all messsage were cleared"
            except:
                raise ModError(f"i can't message")
          
        await ctx.send(embed=embed , ephemeral=True, delete_after=15)

    @commands.command(help="Cleanup member messages")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    @commands.dynamic_cooldown(bypass_for_owner)
    async def clear_member(
            self,
            ctx,
            member:discord.Member = commands.Option(description="Mention member"),
            search:int = commands.Option(default=15, description="amount to search message / default = 15")
        ):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)
        
        embed = discord.Embed(color=self.bot.white_color)
        try:
            await do_removal(self, ctx, search, lambda e: e.author == member)
        except:
            raise ModError("i can't cleanup messages")
        embed.description=f"`{ctx.channel.name}` : {member} messages were cleared"
        await ctx.send(embed=embed , ephemeral=True, delete_after=15)
        
    @commands.command(help="Mute member")
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def mute(
            self,
            ctx,
            member: discord.Member = commands.Option(description="Mention member"),
            time: TimeConverter = commands.Option(default=None, description="duration such as 10m , 30m , 3h"),
            *,
            reason: str = commands.Option(default=None, description="reason")   
        ):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        embed = discord.Embed(color=self.bot.white_color)

        # #Remind me to delete this after release
        # if time is not None and int(time) > 21600:
        #     embed.description = "i'm sorry it's in beta testing, you can't set the timer for more than 6 hour."
        #     return await ctx.send(embed=embed, ephemeral=True)

        #mute_role
        role = discord.utils.get(ctx.guild.roles, name="⠀ mute ♡ ₊˚")

        if not role:
            raise ModError("Your server don't have : **`Muted Role`**")

        if member == self.bot.user:
            raise ModError("You cannot mute the bot")
        
        if member == ctx.author:
            raise ModError("You cannot mute yourself.")
                
        member_role = discord.utils.get(member.roles, name="⠀ mute ♡ ₊˚")
        if member_role:
            raise ModError("member's already have a mute role.")

        try:
            await member.add_roles(role)
        except:
            raise ModError("i can't mute this member")
        
        if time is not None:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            msg_format = ""
            if hours: msg_format += f"{int(hours)} hours "
            if minutes: msg_format += f"{int(minutes)} minutes "
            if seconds : msg_format += f"{int(seconds)} seconds"
            embed.add_field(name="Time:", value=msg_format , inline=False)
        
        embed.title = "Mute Member"
        embed.description = f"member: {member}"
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"Muted by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"Muted by {ctx.author.display_name}")

        await ctx.send(embed=embed)

        if time is not None and time < 6000:
            await asyncio.sleep(time)
            await member.remove_roles(role)

    @commands.command(help="Unmute member")
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(
            self,
            ctx,
            member: discord.Member = commands.Option(description="Mention member")  
        ):
        role = discord.utils.get(ctx.guild.roles, name="⠀ mute ♡ ₊˚")

        embed = discord.Embed(description=f"You has been unmute : `{member}`",color=self.bot.white_color)
        if ctx.author.display_avatar is not None:
            embed.set_footer(text=f"Unmuted by {ctx.author}", icon_url = ctx.author.display_avatar.url)
        else:
            embed.set_footer(text=f"Unmuted by {ctx.author}")

        await member.remove_roles(role)
        await ctx.send(embed=embed)
    
    @commands.command(help="Create mute role and auto setup")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def muterole(self, ctx): #role: discord.Role = commands.Option(description="Mention role")
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        guild = ctx.guild
        mutedRole = discord.utils.get(ctx.guild.roles, name="⠀ mute ♡ ₊˚")
        embed = discord.Embed(color=self.bot.white_color)

        if not mutedRole:
            mutedRole = await guild.create_role(name="⠀ mute ♡ ₊˚" , colour=self.bot.white_color)

            embed.description = f"Mute role : {mutedRole.mention}\n**Permissions auto setup**\nspeak: `false`\nsend message : `false`"
            await ctx.send(embed=embed)

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False) #read_message_history=True, read_messages=False
        else:
            raise ModError("Your server has a muted role.")

    @commands.command(aliases=["nick"], help="change nickname")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def change_nick(self, ctx , member: discord.Member = commands.Option(description="mention member"), *, nick:str = commands.Option(description="New nickname")):
        try:
            await member.edit(nick=nick)
            embed = discord.Embed(description=f"{member.mention} : Nickname was changed for `{member.display_name}`", color=self.bot.white_color)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            raise ModError('You do not have a permissions to change nickname')
        except discord.HTTPException:
            raise ModError('Change nickname failed')
        except Exception as Ex:
            print(Ex)
    
    @commands.command(aliases=["slow"], help="set slowmode channel")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_channels=True)
    async def slowmode(self, ctx , time: TimeConverter = commands.Option(description="slowmode duration / time = 0s for disable")):
        
        if time == 0:
            raise ModError("Time is invalid")
        
        if int(time) > 21600:
            raise ModError("slowmode is a maximum of 6 hours.")

        seconds = int(time)
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        time_format = ""
        if hours: time_format += f"{int(hours)} hours "
        if minutes: time_format += f"{int(minutes)} minutes "
        if seconds : time_format += f"{int(seconds)} seconds"
        
        try:
            embed = discord.Embed(color=self.bot.white_color)
            embed.description = f"Set the slowmode delay in this channel to {time_format}"
            await ctx.channel.edit(slowmode_delay=seconds)
            return await ctx.send(embed=embed)
        except:
            raise ModError(f"i can't set the slowmode this channel")

    @commands.command(help="Mutes the specified member with a specified reason.")
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(mute_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def voice_mute(
            self,
            ctx,
            member: discord.Member = commands.Option(description="Spectify member"),
            *,
            reason = commands.Option(default=None, description="reason")
        ):
        embed_error = discord.Embed(color=self.bot.error_color)

        if member.id == ctx.author.id:
            embed_error.description = "You can't Voice mute yourself!"
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

        if isinstance(member, discord.Member):
            if ctx.me.top_role < member.top_role:
                raise ModError(f"Can't mute this member")
            elif ctx.me.top_role >= member.top_role:
                pass
            if member == ctx.guild.owner:
                raise ModError(f"Can't mute The Owner")
        
        if reason == None:
            reason = "None"
        elif len(reason) > 500:
            reason = "Reason was exceeded the 500-character limit."
        try:    
            await member.edit(mute=True, reason=reason)
            embed = RenlyEmbed.to_success(title="Voice Mute", description=f"Successfully Voice muted `{member}`\n reason:**{reason}**")
            if ctx.author.avatar is not None:
                embed.set_footer(text=f"Muted by {ctx.author}", icon_url=ctx.author.avatar.url)
            else:
                embed.set_footer(text=f"Muted by {ctx.author}")
            await ctx.send(embed=embed)
        except:
            raise ModError("Target user is not connected to voice.")

    @commands.command(help="Deafens the specified member with a specified reason.")
    @commands.guild_only()
    # @commands.has_guild_permissions(mute_members=True)
    # @commands.bot_has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def voice_deafen(
            self,
            ctx,
            member: discord.Member = commands.Option(description="Spectify member"),
            *,
            reason = commands.Option(default=None, description="reason")
        ):
        if ctx.author.guild_permissions.deafen_members:
            embed_error = discord.Embed(color=self.bot.error_color)

            if member.id == ctx.author.id:
                raise ModError("You can't VC deafen yourself!")

            if isinstance(member, discord.Member):
                if ctx.me.top_role < member.top_role:
                    raise ModError(f"Can't deafen this member")
                elif ctx.me.top_role >= member.top_role:
                    pass
                if member == ctx.guild.owner:
                    raise ModError(f"Can't deafen The Owner")
            
            if reason == None:
                reason = "None"
            elif len(reason) > 500:
                reason = "Reason was exceeded the 500-character limit."
            try:
                await member.edit(deafen=True, reason=reason)
                embed = RenlyEmbed.to_success(title="Voice Deafen", description=f"Successfully Voice deafened `{member}`\n reason:**{reason}**")
                if ctx.author.avatar is not None:
                    embed.set_footer(text=f"Deafened by {ctx.author}", icon_url=ctx.author.avatar.url)
                else:
                    embed.set_footer(text=f"Deafened by {ctx.author}")
                await ctx.send(embed=embed)
            except:
                raise ModError(f"Target user is not connected to voice.")
        else:
            raise commands.MissingPermissions(['Deafen Members'])
    
    # @commands.command(help="Remove permissions for members to send messages in a channel")
    # @commands.guild_only()
    # @commands.has_permissions(manage_channels=True)
    # @commands.bot_has_guild_permissions(manage_channels=True)
    # async def lock(self, ctx, channel: discord.TextChannel=commands.Option(default=None, description="Spectify channel")):
    #     channel = channel or ctx.channel
    #     embed = discord.Embed(color=0xFF7878)
    #     embed.description = f"{channel.mention} : is **lockdown.**"
    #     await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name}", send_messages=False)
    #     await ctx.send(embed=embed)

    # @commands.command(help="Remove lockdown a channel")
    # @commands.guild_only()
    # @commands.has_permissions(manage_channels=True)
    # @commands.bot_has_guild_permissions(manage_channels=True)
    # async def unlock(self, ctx, channel: discord.TextChannel=commands.Option(default=None, description="Spectify channel")):
    #     channel = channel or ctx.channel
    #     embed = discord.Embed(color=0x8be28b)
    #     embed.description = f"{channel.mention} : **Removed lockdown!**"
    #     await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=True)
    #     await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))