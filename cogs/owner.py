# Standard 
import discord
import os
import json
from discord.ext import commands , tasks
from time import time
from datetime import datetime, timedelta, timezone
from typing import Literal

# Third party
# Local
from utils.emoji import emoji_converter
from utils.buttons import Confirm
from utils.json_loader import latte_read, latte_write
from utils.formats import format_dt , format_relative
from utils.time import relativedelta

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
        type: Literal["playing", "streaming", "listening", "watching"] = commands.Option(description="status type"),
        status = commands.Option(description="Status text"),
        streaming_url = commands.Option(default=None, description="streaming status url"),
    ): 

        if type == "playing":  # Setting `Playing ` status
            await self.bot.change_presence(activity=discord.Game(name=status))
        elif type == "streaming": # Setting `Streaming ` status
            await self.bot.change_presence(activity=discord.Streaming(name=status, url=streaming_url))
        elif type == "listening": # Setting `Listening ` statu
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        elif type == "watching": # Setting `Watching ` status
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        
        embed = discord.Embed(title="Status Changed!",description=f"**type:** {type}\n**status:** `{status}`", color=self.bot.white_color)
        await ctx.send(embed=embed)
    
    @commands.command(help="enable command")
    @commands.guild_only()
    @commands.is_owner()
    async def enable(self, ctx, command = commands.Option(description="command name")):
        command = self.bot.get_command(command)
        if command.enabled:
            return await ctx.send(f"`{command}` is already enabled.")
        command.enabled = True
        await ctx.send(f"Successfully enabled the `{command.name}` command.")
    
    @commands.command(help="disable command")
    @commands.guild_only()
    @commands.is_owner()
    async def disable(self, ctx, command = commands.Option(description="command name")):
        command = self.bot.get_command(command)
        if not command.enabled:
            return await ctx.send(f"`{command}` is already disabled.")
        command.enabled = False
        await ctx.send(f"Successfully disabled the `{command.name}` command.")

    @commands.command(help="load cog")
    @commands.guild_only()
    @commands.is_owner()
    async def load(self, ctx, extension = commands.Option(description="extension")):
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
    async def unload(self, ctx, extension = commands.Option(description="extension")):
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