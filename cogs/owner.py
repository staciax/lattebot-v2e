# Standard 
import discord
import os
import json
from discord.ext import commands
import socket
from time import time
from datetime import datetime, timedelta, timezone
from typing import Literal , Union

# Third party
# Local
from utils.emoji import emoji_converter
from utils.buttons import Confirm
from utils.json_loader import latte_read, latte_write
from utils.buttons import NewSimpage
from utils.errors import UserInputErrors
from utils.checks import is_my_friend

# class PrivateLiteral(commands.Converter):
#     """A class for custom Literal"""
#     values: tuple[str, ...] | str

#     def __class_getitem__(cls, item):
#         self = cls()
#         self.values = item
#         return self

#     async def convert(self, ctx, argument):
#         """Converts the argument to any of the exact value given"""
#         if argument in self.values:
#             return argument
#         raise UserInputErrors(f"An unknown error occurred, sorry")

class Owner(commands.Cog):
    """Owner related commands."""
    
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

    #     # create_blacklist
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
            user : Union[discord.Member, discord.User] = commands.Option(description="Spectify member"),
            *,
            reason = commands.Option(default=None, description="Reason to blacklist")
        ):

        if user == self.bot.user:
            raise UserInputErrors("You cannot blacklist the bot")
        
        if user == ctx.author:
            raise UserInputErrors("You cannot blacklist yourself.")
        
        if reason is None:
            reason = "no reason"

        con = self.bot.pg_con
        #check_user
        query = "SELECT user_id FROM public.blacklist WHERE user_id = $1;"
        row = await con.fetchrow(query, user.id)
        if row:
            if row['user_id'] == user.id:
                raise UserInputErrors('This user already exists.')

        #create_blacklist
        try:
            query = "INSERT INTO public.blacklist(user_id, reason, is_blacklisted) VALUES ($1, $2, $3);"
            await con.execute(query, user.id, reason[:1000] or None, True)
            embed = discord.Embed(color=self.bot.white_color)
            embed.description = f"**{user}** has been blacklisted with the reason {reason[:1000]}"
            self.bot.blacklist[user.id] = True
            await ctx.send(embed=embed)
        except:
            raise UserInputErrors('Could not blacklist this user.')

    @commands.command(aliases=['blr'], help="Removes the user from the blacklist.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_remove(self, ctx, user : Union[discord.Member, discord.User] = commands.Option(description="Spectify member")):
        user_id = user.id
        query = "SELECT user_id FROM public.blacklist WHERE user_id = $1;"
        
        row = await self.bot.pg_con.fetchrow(query, user_id)
        if row != None:
            embed = discord.Embed(color=self.bot.white_color)
            try:
                query = "DELETE FROM public.blacklist WHERE user_id = $1;"
                await self.bot.pg_con.execute(query, user_id)
                embed.description = f"**{user}** has been removed from the blacklist"
                await ctx.send(embed=embed)
                self.bot.blacklist[user.id] = False
            except:
                raise UserInputErrors('Could not remove this user. Please try again!')
        else:
            raise UserInputErrors('User not found!')

    @commands.command(aliases=['blc'], help="Checks if the user is blacklisted.")
    @commands.guild_only()
    @commands.is_owner()
    async def blacklist_check(self, ctx, user : Union[discord.Member, discord.User] = commands.Option(description="Spectify member")):
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
        blacklist_users = []
        query = "SELECT * FROM public.blacklist;"
        blacklist = await self.bot.pg_con.fetch(query)
        
        if blacklist or len(blacklist) != 0:
            for data in blacklist:
                user_id = data["user_id"]
                user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
                # reason = data["reason"]
                blacklist_users.append(f"{user} | `{user.id}`")

            p = NewSimpage(ctx=ctx, entries=blacklist_users, per_page=10)
            p.embed.color = self.bot.white_color
            return await p.start()

        raise UserInputErrors("Not found blacklisted users.")

    @commands.command(name="view_config", aliases=['configview'], help="view config files")
    @commands.guild_only()
    @commands.is_owner()
    async def latte_view_config(self, ctx, file_target:Literal['channel_sleep','latte_events','remind','sleeping']=commands.Option(description="file name")):
        embed = discord.Embed(color=self.bot.white_color)
        try:
            data = latte_read(str(file_target))
            embed.description=f"{file_target}.json\n```json\n{json.dumps(data, indent = 1)}```"
            return await ctx.reply(embed=embed, ephemeral=True, mention_author=False, delete_after=15)
        except:
            raise UserInputErrors("file not found!")

    @commands.command(name="config_set", aliases=['configedit'], help="edit config files", slash_command=True, slash_command_guilds=[887274968012955679])
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
            return await ctx.reply(embed=embed, mention_author=False)
        except:
            raise UserInputErrors('Write json error')

    @commands.command(help="logout bot")
    @commands.guild_only()
    @commands.is_owner()
    async def logout_bot(self, ctx):
        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} Logout",icon_url=self.bot.user.avatar.url)
        embed.description = f"are you sure?"

        #edit
        embed_e = discord.Embed(color=self.bot.white_color)
        embed_e.timestamp = datetime.now(timezone.utc)

        view = Confirm(ctx)
        msg = await ctx.reply(embed=embed, view=view, mention_author=False)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            embed_e.description = f"Shuting down..."
            await msg.edit(embed=embed_e, view=None)
            await self.bot.close()
        else:
            await msg.delete()
            raise UserInputErrors("Cancelled...")

    @commands.command(name="bot_status", help="change bot status", slash_command=True, slash_command_guilds=[887274968012955679])
    @commands.guild_only()
    @commands.is_owner()
    async def botstatus(
        self,
        ctx,
        status: Literal["online", "idle", "dnd", "offline"] = commands.Option(description="status type"),
        activity: Literal["playing", "streaming", "listening", "watching"] = commands.Option(description="activity type"),
        text:str = commands.Option(default=None, description="status text"),
        streaming_url = commands.Option(default=None, description="streaming status url"),
    ):  
        if text == 'default':
            text = self.bot.latte_avtivity
        bot_status = getattr(discord.Status, status)
        try:
            if activity == "playing":  # Setting `Playing ` status
                await self.bot.change_presence(status=bot_status,activity=discord.Game(name=text))
            elif activity == "streaming": # Setting `Streaming ` status
                await self.bot.change_presence(status=bot_status, activity=discord.Streaming(name=text, url=streaming_url))
            elif activity == "listening": # Setting `Listening ` statu
                await self.bot.change_presence(status=bot_status, activity=discord.Activity(type=discord.ActivityType.listening, name=text))
            elif activity == "watching": # Setting `Watching ` status
                await self.bot.change_presence(status=bot_status, activity=discord.Activity(type=discord.ActivityType.watching, name=text))
        except:
            raise UserInputErrors("Change status error")

        embed = discord.Embed(color=self.bot.white_color)
        embed.title = "Status Changed!"
        embed.add_field(name="Status:", value=f"`{status}`")
        embed.add_field(name="Activity:", value=f"`{activity}`")
        embed.add_field(name="Text:", value=f"`{text}`")
        if activity == "watching" and streaming_url is not None:
            embed.add_field(name="URL:", value=f"`{streaming_url}`")

        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(help="Toggle command", slash_command=True, slash_command_guilds=[887274968012955679])
    @commands.guild_only()
    @commands.is_owner()
    async def toggle(self, ctx, command = commands.Option(description="Command name")):
        command = self.bot.get_command(command)
        command.enabled = not command.enabled
        ternary = "Enabled" if command.enabled else "disabled"
        toggle_color = 0x8be28b if command.enabled else 0xFF7878
        embed = discord.Embed(color=toggle_color)
        embed.description = f"Successfully {ternary} the `{command.name}` command."
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Loaded cog")
    @commands.guild_only()
    @commands.is_owner()
    async def load(
            self,
            ctx,
            extension: str
        ):
        embed = discord.Embed()
        try:
            self.bot.load_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Load : `{extension}`"
            embed.color = 0x8be28b
            return await ctx.reply(embed=embed, mention_author=False)
        except commands.ExtensionNotFound:
            raise UserInputErrors("Extension Not Found")
        except commands.ExtensionAlreadyLoaded:
            raise UserInputErrors("The extension is already loaded.")
        except commands.NoEntryPointError:
            raise UserInputErrors("The extension does not have a setup function.")
        except commands.ExtensionFailed:
            raise UserInputErrors("The extension load failed")
        except Exception as ex:
            print(ex)
            raise UserInputErrors("The extension load failed")
           
    @commands.command(help="Unloaded cog")
    @commands.guild_only()
    @commands.is_owner()
    async def unload(
            self,
            ctx,
            extension:str
        ):
        embed = discord.Embed()
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Unload : `{extension}`"
            embed.color = 0x8be28b
            return await ctx.reply(embed=embed, mention_author=False)
        except commands.ExtensionNotFound:
            raise UserInputErrors("Extension Not Found")
        except commands.ExtensionNotLoaded:
            raise UserInputErrors("The extension was not loaded.")
        except Exception as ex:
            print(ex)
            raise UserInputErrors("The extension unload failed")

    @commands.command(help="Reloaded cog")
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, extension:str):
        embed = discord.Embed()
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Reload : `{extension}`"
            embed.color = 0x8be28b
            return await ctx.send(embed=embed)
        except commands.ExtensionNotLoaded:
            raise UserInputErrors("The extension was not loaded.")
        except commands.ExtensionNotFound:
            raise UserInputErrors("TExtension Not Found")
        except commands.NoEntryPointError:
            raise UserInputErrors("The extension does not have a setup function.")
        except commands.ExtensionFailed:
            raise UserInputErrors("The extension reload failed")
        except Exception as ex:
            print(ex)
            raise UserInputErrors("The extension reload failed")
    
    @commands.command(help="Reload all cogs")
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

    # @commands.command(help="shutdown stacia pc")
    # @commands.guild_only()
    # @is_my_friend()
    # async def shutdown(self, ctx):
    #     embed = discord.Embed(color=self.bot.white_color)
    #     embed.description = f"Are you sure you want to shutdown stacia computer?"

    #     #edit
    #     embed_e = discord.Embed(color=self.bot.white_color, timestamp=ctx.message.created_at)
    #     embed_e.description = f"Shuting down in 2 minutes"
    #     embed_e.set_footer(text="shutdown by", icon_url=ctx.author.display_avatar or ctx.author.default_avatar)

    #     view = Confirm(ctx)
    #     msg = await ctx.reply(embed=embed, view=view, mention_author=False)
    #     await view.wait()
    #     if view.value is None:
    #         return
    #     elif view.value:
    #         s = socket.socket()
    #         host = 'RENLY'
    #         port = 4869
    #         s.connect((host, port))
    #         await msg.edit(embed=embed_e, view=None)
    #     else:
    #         await msg.delete()
         
def setup(bot):
    bot.add_cog(Owner(bot))