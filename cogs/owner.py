# Standard 
import discord
import os
import json
from discord.ext import commands , tasks
from time import time
from datetime import datetime, timedelta, timezone
from typing import Literal , Union

# Third party
# Local
from utils.emoji import emoji_converter
from utils.buttons import Confirm
from utils.json_loader import latte_read, latte_write
from utils.buttons import NewSimpage

class Owner(commands.Cog, command_attrs = dict(slash_command_guilds=[887274968012955679])):
    """Owner"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='owner', id=903339979130949683, animated=False)

    # async def add_blacklist(self, ctx, user, reason, connection=None):
        
    #     con = connection or self.bot.pg_con

    #     #check_user
    #     query = "SELECT user_id FROM public.blacklist WHERE user_id = $1;"
    #     row = await con.fetchrow(query, user.id)
    #     if row:
    #         if row['user_id'] == user.id:
    #             return await ctx.send('This user already exists.')

    #     #create_blacklist
    #     try:
    #         query = "INSERT INTO public.blacklist(user_id, reason, is_blacklisted) VALUES ($1, $2, $3);"
    #         await con.execute(query, user.id, reason[:1000], True)
    #         embed = discord.Embed(color=self.bot.white_color)
    #         embed.description = f"**{user}** has been blacklisted with the reason {reason[:1000]}"
    #         self.bot.blacklist[user.id] = True
    #         await ctx.send(embed=embed)
    #     except:
    #         return await ctx.send('Could not blacklist this user.')

    @commands.command(aliases=['bla'], help="Adds the user to the blacklist.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_add(self,
            ctx,
            user : Union[discord.User, discord.Member] = commands.Option(description="Spectify member"),
            reason = commands.Option(default=None, description="Reason to blacklist")
        ):
        embed_error = discord.Embed(color=0xFF7878)

        if user == self.bot.user:
            embed_error.description = "You cannot blacklist the bot"
            return await ctx.send(embed=embed_error, ephemeral=True)
        
        if user == ctx.author:
            embed_error.description = "You cannot blacklist yourself."
            return await ctx.send(embed=embed_error, ephemeral=True)
        
        if reason is None:
            reason = "no reason"

        con = self.bot.pg_con
        #check_user
        query = "SELECT user_id FROM public.blacklist WHERE user_id = $1;"
        row = await con.fetchrow(query, user.id)
        if row:
            if row['user_id'] == user.id:
                embed_error.description = 'This user already exists.'
                return await ctx.send(embed=embed_error, ephemeral=True)

        #create_blacklist
        try:
            query = "INSERT INTO public.blacklist(user_id, reason, is_blacklisted) VALUES ($1, $2, $3);"
            await con.execute(query, user.id, reason[:1000] or None, True)
            embed = discord.Embed(color=self.bot.white_color)
            embed.description = f"**{user}** has been blacklisted with the reason {reason[:1000]}"
            self.bot.blacklist[user.id] = True
            await ctx.send(embed=embed)
        except:
            embed_error.description = 'Could not blacklist this user.'
            return await ctx.send(embed=embed_error, ephemeral=True)

    @commands.command(aliases=['blr'], help="Removes the user from the blacklist.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_remove(self, ctx, user : Union[discord.User, discord.Member] = commands.Option(description="Spectify member")):
        embed_error = discord.Embed(color=0xFF7878)

        user_id = user.id
        query = "SELECT user_id FROM public.blacklist WHERE user_id = $1;"
        
        row = await self.bot.pg_con.fetchrow(query, user_id)
        if row != None:
            try:
                query = "DELETE FROM public.blacklist WHERE user_id = $1;"
                await self.bot.pg_con.execute(query, user_id)
                await ctx.send(f"**{user}** has been removed from the blacklist")
                self.bot.blacklist[user.id] = False
            except:
                embed_error.description = 'Could not remove this user. Please try again!'
                return await ctx.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description = 'User not found!'
            return await ctx.send(embed=embed_error, ephemeral=True)

    @commands.command(aliases=['blc'], help="Checks if the user is blacklisted.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_check(self, ctx, user : Union[discord.User, discord.Member] = commands.Option(description="Spectify member")):
        try:
            status = self.bot.blacklist[user.id]
        except KeyError:
            status = False

        color=0xFF7878
        description = f"{user} isn't blacklisted"
            
        if status is True:
            color=self.bot.white_color
            query = "SELECT reason FROM public.blacklist WHERE user_id = $1;"
            reason = await self.bot.pg_con.fetchval(query, user.id)
            description = f"**User:** {user}\nBlacklist: True\n**Reason:** {reason}"
            
        embed = discord.Embed(description=f"{description}", timestamp=discord.utils.utcnow(), color=color)
        return await ctx.send(embed=embed)
    
    @commands.command(aliases=['bll'], help="List all blacklisted users.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_list(self, ctx):
        embed_error = discord.Embed(color=0xFF7878)

        blacklist_users = []
        query = "SELECT * FROM public.blacklist;"
        blacklist = await self.bot.pg_con.fetch(query)
        
        if blacklist is None:
            embed_error.description = "Not found blacklisted users."
            return await ctx.send(embed=embed_error, ephemeral=True)

        for data in blacklist:
            user = self.bot.get_user(data["user_id"])
            reason = data["reason"]
            blacklist_users.append(f"{user.name} | `{user.id}`")

        p = NewSimpage(ctx=ctx, entries=blacklist_users, per_page=10)
        p.embed.color = self.bot.white_color
        await p.start()

    @commands.command(name="view_config", help="view config files")
    @commands.guild_only()
    @commands.is_owner()
    async def latte_view_config(self, ctx, file_target:Literal['channel_sleep','latte_events','remind','sleeping']=commands.Option(description="file name")):
        embed = discord.Embed(color=self.bot.white_color)
        try:
            data = latte_read(str(file_target))
            embed.description=f"{file_target}.json\n```json\n{json.dumps(data, indent = 1)}```"
            return await ctx.send(embed=embed, ephemeral=True)
        except:
            embed.description=f"file not found!"
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command(name="config_set", help="edit config files")
    @commands.guild_only()
    @commands.is_owner()
    async def latte_config_set(
            self,
            ctx,
            file_target:Literal['channel_sleep','latte_events','remind','sleeping'] = commands.Option(description="file name"),
            keys = commands.Option(description="json key"), value=commands.Option(default=None, description="json value"),
            type: Literal['str','int']=commands.Option(default=None, description="type of value")
        ):
        data = latte_read(f"{str(file_target)}")
        if type == 'str':
            data[f"{str(keys)}"] = str(value)
        elif type == 'int':
            data[f"{str(keys)}"] = int(value)

        embed = discord.Embed(color=self.bot.white_color)
        
        try:
            latte_write(data, str(file_target))
            embed.add_field(name="file", value=f"```fix\n{file_target}.json```", inline=False)
            embed.add_field(name="config", value=f'```css\n"{keys}":"{value}"```', inline=False)
            return await ctx.send(embed=embed)
        except:
            embed.description = "write json error"
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command(help="logout bot")
    @commands.guild_only()
    @commands.is_owner()
    async def logout(self, ctx):
        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} Logout",icon_url=self.bot.user.avatar.url)
        embed.description = f"are you sure?"

        #edit
        embed_e = discord.Embed(color=self.bot.white_color)
        embed_e.timestamp = datetime.now(timezone.utc)

        view = Confirm(ctx)
        msg = await ctx.send(embed=embed, view=view, ephemeral=True)
        await view.wait()
        view.clear_items()
        if view.value is None:
            return
        elif view.value:
            embed_e.description = f"Shuting down..."
            await msg.edit(embed=embed_e, view=view, ephemeral=True)
            print('Shuting down...')
            await self.bot.logout()
        else:
            print('Cancelled...')
            embed_e.description = f"Cancelled..."
            await msg.edit(embed=embed_e, view=view, ephemeral=True)


    @commands.command(name="bot_status",help="change bot status")
    @commands.guild_only()
    @commands.is_owner()
    async def botstatus(
        self,
        ctx,
        status: Literal["online", "idle", "dnd", "offline"] = commands.Option(description="status type"),
        activity: Literal["playing", "streaming", "listening", "watching"] = commands.Option(description="activity type"),
        streaming_url = commands.Option(default=None, description="streaming status url"),
    ):  
        if status == "online":
            bot_status = discord.Status.online
        elif status == "idle":
            bot_status = discord.Status.idle
        elif status == "dnd":
            bot_status = discord.Status.dnd
        elif status == "offline":
            bot_status = discord.Status.offline

        if activity == "playing":  # Setting `Playing ` status
            await self.bot.change_presence(status=bot_status,activity=discord.Game(name=status))
        elif activity == "streaming": # Setting `Streaming ` status
            await self.bot.change_presence(status=bot_status, activity=discord.Streaming(name=status, url=streaming_url))
        elif activity == "listening": # Setting `Listening ` statu
            await self.bot.change_presence(status=bot_status, activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        elif activity == "watching": # Setting `Watching ` status
            await self.bot.change_presence(status=bot_status, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        
        embed = discord.Embed(title="Status Changed!",description=f"**type:** {type}\n**status:** `{status}`", color=self.bot.white_color)
        await ctx.send(embed=embed)
    
    # @commands.command(help="enable command")
    # @commands.guild_only()
    # @commands.is_owner()
    # async def enable(self, ctx, command = commands.Option(description="command name")):
    #     command = self.bot.get_command(command)
    #     if command.enabled:
    #         return await ctx.send(f"`{command}` is already enabled.")
    #     command.enabled = True
    #     await ctx.send(f"Successfully enabled the `{command.name}` command.")
    
    # @commands.command(help="disable command")
    # @commands.guild_only()
    # @commands.is_owner()
    # async def disable(self, ctx, command = commands.Option(description="command name")):
    #     command = self.bot.get_command(command)
    #     if not command.enabled:
    #         return await ctx.send(f"`{command}` is already disabled.")
    #     command.enabled = False
    #     await ctx.send(f"Successfully disabled the `{command.name}` command.")

    @commands.command(help="Toggle command")
    @commands.guild_only()
    @commands.is_owner()
    async def toggle(self, ctx, command = commands.Option(description="Command name")):
        command = self.bot.get_command(command)
        command.enabled = not command.enabled
        ternary = "Enabled" if command.enabled else "disabled"
        toggle_color = 0x8be28b if command.enabled else 0xFF7878
        embed = discord.Embed(color=toggle_color)
        embed.description = f"Successfully {ternary} the `{command.name}` command."
        await ctx.send(embed=embed)

    @commands.command(help="load cog")
    @commands.guild_only()
    @commands.is_owner()
    async def load(
            self,
            ctx,
            extension: Literal['anime','error_handler','events','fun','help','infomation','latte_guild','leveling','misc','moderator','nsfw','owner','reaction','stars','tags','testing','todo','utility'] = commands.Option(description="extension")
        ):
        embed = discord.Embed()
        try:
            self.bot.load_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Load : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not load")
            embed.color = 0xFF7878
            return await ctx.send(embed=embed)

        await ctx.send(embed=embed)
    
    @commands.command(help="unload cog")
    @commands.guild_only()
    @commands.is_owner()
    async def unload(
            self,
            ctx,
            extension: Literal['anime','error_handler','events','fun','help','infomation','latte_guild','leveling','misc','moderator','nsfw','owner','reaction','stars','tags','testing','todo','utility'] = commands.Option(description="extension")
        ):
        embed = discord.Embed()
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Unload : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not unload")
            embed.color = 0xFF7878
            return await ctx.send(embed=embed)

        await ctx.send(embed=embed)
    
    @commands.command(help="reload cog")
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, extension= commands.Option(description="extension")):
        embed = discord.Embed()
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Reload : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not reload")
            embed.color = 0xFF7878
            return await ctx.send(embed=embed)

        await ctx.send(embed=embed)
    
    @commands.command(help="reload all cogs")
    @commands.guild_only()
    @commands.is_owner()
    async def reloadall(self, ctx):
        embed = discord.Embed()
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                if not filename == "owner.py":
                    try:
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                        embed.description = f"{emoji_converter('greentick')} Reloaded all"
                        embed.color = 0x8be28b
                    except Exception as e:
                        self.bot.load_extension(f"cogs.{filename[:-3]}")
                        return await ctx.send(f"{e}")

        await ctx.send(embed=embed)
         
def setup(bot):
    bot.add_cog(Owner(bot))