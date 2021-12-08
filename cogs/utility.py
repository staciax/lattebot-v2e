# Standard
import discord
import asyncio
import random
import json
from discord import Embed
from discord.ext import commands , tasks
from datetime import datetime, timedelta, timezone
from typing import Union , Literal

# Third
import humanize
from googletrans import Translator

# Local
from utils.json_loader import latte_read, latte_write
from utils.converter import TimeConverter
from utils.formats import format_dt , format_relative
from utils.buttons import Confirm
from utils.useful import RenlyEmbed
from utils.emoji import emoji_converter
from utils.custom_button import base_Button_URL

class UtilityError(commands.CommandError):
    pass

class Utility(commands.Cog, command_attrs = dict(slash_command=True)):
    """Some useful commands"""

    def __init__(self, bot):
        self.bot = bot
        self.sleeped.start()
        self.reminded.start()
        self.channel_sleeped.start()
    
    def cog_unload(self):
        self.sleeped.cancel()
        self.reminded.cancel()
        self.channel_sleeped.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='gift', id=903339694098628618, animated=False)

    @tasks.loop(minutes=1)
    async def sleeped(self):
        guild = self.bot.latte
        data = latte_read("sleeping")
        if not data:
            return
        for key in data.keys():
            dt = datetime.now(timezone.utc).strftime("%d%m%Y%H%M")
            if data[key]["time"] is None:
                return
            elif int(data[key]["time"]) <= int(dt):
                member_sleep = guild.get_member(int(key))
                if member_sleep:
                    try:
                        await member_sleep.move_to(channel=None)
                        del data[key]
                        latte_write(data, "sleeping")
                        # break
                    except Exception as ex:
                        print(f"error sleep {ex}")

    @tasks.loop(minutes=1)
    async def reminded(self):
        guild = self.bot.latte
        data = latte_read("remind")
        raw_date = datetime.now(timezone.utc)
        if not data:
            return
        try:
            for key in data.keys():
                dt = datetime.now(timezone.utc).strftime("%d%m%Y%H%M")
                if int(data[key]["time"]) <= int(dt):
                    channel = guild.get_channel(int(data[key]["channel"]))
                    member = guild.get_member(int(key))
                    message = data[key]["message"]
                    message_url = data[key]["url"]
                    view = base_Button_URL(label="Go to original message", url=message_url)
                    embed_response = discord.Embed(color=self.bot.white_color)
                    embed_response.title = "Reminder"
                    embed_response.description = f"{member.mention}, {format_relative(raw_date)}\n{message}"
                    await channel.send(embed=embed_response, view=view)
                    del data[key]
                    latte_write(data, "remind")
                    # break
                   
        except Exception as Ex:
            print(f"remind error {Ex}")
    
    @tasks.loop(minutes=1)
    async def channel_sleeped(self):
        guild = self.bot.latte
        data = latte_read("channel_sleep")
        if not data:
            return
        for key in data.keys():
            dt = datetime.now(timezone.utc).strftime("%d%m%Y%H%M")
            if data[key]["time"] is None:
                return
            elif int(data[key]["time"]) <= int(dt):
                channel = guild.get_channel(int(key))
                member_list = channel.members
                if member_list is not None:
                    try:
                        for x in member_list:
                            await x.move_to(channel=None)
                        del data[key]
                        latte_write(data, "channel_sleep")
                        # break
                    except Exception as Ex:
                        print(f"error  channel sleep {Ex}")

    @sleeped.before_loop
    async def before_sleeped(self):
        await self.bot.wait_until_ready()

    @reminded.before_loop
    async def before_reminded(self):
        await self.bot.wait_until_ready()   

    @channel_sleeped.before_loop
    async def before_channel_sleeped(self):
        await self.bot.wait_until_ready()       

    @commands.command(help="Set your afk")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def afk(self, ctx, *, reason=commands.Option(default=None, description="Reason (default = personal problems)")):
        member = ctx.author

        if member.id in self.bot.afk_user.keys():
            embed_time = RenlyEmbed.to_error(title="You already have afk status", description=f"**reason:** {self.bot.afk_user[member.id]['reason']}")
            return await ctx.send(embed=embed_time, ephemeral=True, delete_after=15)

        embed = Embed(color=self.bot.white_color)
        if reason is None:
            reason = "personal problems"
        elif len(reason) > 100:
            raise UtilityError("**reason** is a maximum of 100 characters.")
        
        self.bot.afk_user[member.id] = {"reason": reason, "name": member.display_name}
        try:
            await member.edit(nick=f'[AFK] {member.display_name}')
        except:
            pass
        # embed.title = f"{member.name} is now AFK"
        embed.description = f"I have set your afk: {reason}"

        await ctx.send(embed=embed)

    @commands.command(help="clear afk status", aliases=["afkclear"])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def afk_clear(self, ctx, member:discord.Member=commands.Option(default=None,description="spectify member")):
        if member is None:
            member = ctx.author

        embed = discord.Embed(color=self.bot.white_color)
        if member.id in self.bot.afk_user.keys() is not None:
            try:
                if self.bot.afk_user[member.id]['name'] is not None:
                    await member.edit(nick=self.bot.afk_user[member.id]['name'])
                else:
                    await member.edit(nick=None)
            except:
                pass

            del self.bot.afk_user[member.id]
            embed.description = f"Welcome back {member.mention} , i've removed your **AFK** status."
            return await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(help="your message to saybot")
    @commands.guild_only()
    async def saybot(
        self,
        ctx,
        message = commands.Option(description="message"),
        member: discord.Member = commands.Option(default=None, description="member")
    ):
        member = member or ctx.author

        webhook = await ctx.channel.create_webhook(name=member.display_name)
        if member.display_avatar.url is not None:
            await webhook.send(message, username=member.display_name, avatar_url=member.display_avatar.url)
        else:
            await webhook.send(message, username=member.display_name)
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
            if ctx.clean_prefix == "/":
                await ctx.send("\u200b", ephemeral=True)

    @commands.command(help="snipe message")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def snipe(self, ctx, type: Literal["message", "embed"] = commands.Option(description="choose type")):

        embed = Embed()
        embed.color = self.bot.white_color

        if type == 'message':
            
            try:
                message , content, author, channel , time = self.bot.sniped[ctx.guild.id]
            except:
                embed.description = "Couldn't find a message to snipe!"
                return await ctx.send(embed=embed, ephemeral=True, delete_after=15)

            embed.timestamp = time
                            
            if content is not None or len(content) > 0:
                embed.description = content

            if author.avatar.url is not None:
                embed.set_author(name=f"{author} | {channel.name}", icon_url=author.avatar.url)
                
            elif author.avatar.url is None:
                embed.set_author(name=f"{author} | {channel.name}")
                
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)

            await ctx.send(embed=embed, ephemeral=True)
        
        if type == 'embed':
            try:
                embed_snipe = self.bot.sniped_embed[ctx.guild.id]
            except:
                raise UtilityError("Couldn't find a embed to snipe!")

            await ctx.send(embed=embed_snipe, ephemeral=True)

    @commands.command(help="Converter text to binary")
    @commands.guild_only()
    async def binary(self, ctx, *, message = commands.Option(description="message converter to the binary")):
        res = ''.join(format(i, '08b') for i in bytearray(message, encoding ='utf-8'))
        await ctx.send(str(res))
    
    @commands.command(help="Reverse message")
    @commands.guild_only()
    async def reverse(self, ctx, *, message = commands.Option(description="message to reverse")):
        res = ''.join(reversed(message))
        await ctx.send(str(res))
    
    @commands.command(name="random_number", help="takes smallest and largest numbers then does a random number between.", aliases=['rn'])
    @commands.guild_only()
    async def random_number(self , ctx , lowest:Union[int,str] = commands.Option(description="Lowest number"), highest:Union[int,str] = commands.Option(description="Highest number")):
        embed = Embed(title=f"Random Number: {random.randint(lowest,highest)} ",color=self.bot.white_color)
        embed.add_field(name="Lowest Number:",value=f"{lowest}")
        embed.add_field(name="Highest Number:",value=f"{highest}")
        await ctx.send(embed=embed)
    
    @commands.command(name="random", help="random", aliases=['r'])
    @commands.guild_only()
    async def random_(self, ctx, *, message = commands.Option(description="enter a split message")):
        #convert_to_split
        input_value = message 
        list_input = list(input_value.split())

        if len(list_input) == 1:
            raise UtilityError("There must be at least 2 split messages.")

        #try_random
        try:
            await ctx.send(random.choice(list_input))
        except ValueError:
            raise UtilityError("Invalid Range")

    @commands.command(help="create poll")
    @commands.guild_only()
    async def poll(self, ctx, *, message= commands.Option(description="poll message")):

        if len(message) > 2000:
            raise UtilityError('poll message is a maximum of 2000 characters.')

        
        poll_color = ctx.author.color
        if poll_color == discord.Colour.default():
            poll_color = self.bot.white_color
        
        embed = discord.Embed(title="POLL", description=f"{message}",color=poll_color)
        embed_success = RenlyEmbed.to_success(description="Poll created successful")
        if ctx.clean_prefix == "/":
            await ctx.send(embed=embed_success, ephemeral=True)
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction(emoji_converter('greentick'))
        await msg.add_reaction(emoji_converter('redtick'))

    @commands.command(help="Member sleep timer", aliases=['sl'])
    @commands.guild_only()
    async def sleep(self, ctx, time:TimeConverter = commands.Option(description="specify duration"), member: discord.Member = commands.Option(default=None, description="specify member")):    
        if member is None:
            member = ctx.author

        if int(time) > 86400:
            raise UtilityError("You can't set timer duration more than 24 hours")

        timewait = int(time)
        futuredate = datetime.now(timezone.utc) + timedelta(seconds=timewait) 
        futuredate_ = futuredate.strftime("%d%m%Y%H%M")

        #fixed_utc+7
        fix_date = futuredate + timedelta(seconds=25200)
        fix_date = fix_date.strftime("%H:%M %d/%m/%Y")

        cooldown = humanize.naturaldelta(timedelta(seconds=timewait))

        embed = discord.Embed(color=self.bot.white_color)
        embed.add_field(name="Datetime sleep:", value=f"** **\n`{fix_date}({cooldown})`" , inline=False)
        if member.avatar.url is not None:
            embed.set_footer(text=member , icon_url=member.avatar.url)
        else:
            embed.set_footer(text=member)

        view = Confirm(ctx)
        m = await ctx.reply(embed=embed, view=view , mention_author=False)
        await view.wait()
        view.clear_items()
        if view.value is None:
            return await m.delete()
        elif view.value:
            embed_edit = discord.Embed(color=member.colour , timestamp=futuredate)
            embed_edit.description = f"**TIME TO SLEEP** {emoji_converter('sleeping')}\n{format_dt(futuredate, style='f')}({format_dt(futuredate, style='R')})"
            if member.avatar.url is not None:
                embed_edit.set_footer(text=member , icon_url=member.avatar.url)
            else:
                embed_edit.set_footer(text=member)
            
            if timewait > 600:
                if member == ctx.author:
                    embed_edit.description += f"\n||**Cancel timer** : `{ctx.clean_prefix}sleep_stop`||"
                if ctx.author != member:
                    embed_edit.description += f"\n||**Cancel timer** : `{ctx.clean_prefix}sleep_stop @{member.display_name}`||"
                await m.edit(embed=embed_edit, view=None)
                self.bot.sleeping[str(member.id)] = {"time": futuredate_}
                with open("latte_config/sleeping.json", "w") as fp:
                    json.dump(self.bot.sleeping, fp , indent=4)
            else:
                embed_edit.description += f"\n||`Timer can't be stopped.`||"
                await m.edit(embed=embed_edit, view=None)
                await asyncio.sleep(timewait)
                await member.move_to(channel=None)
        else:
            await m.delete()
            raise UtilityError("Cancelling sleep time!")

    @commands.command(help="stop sleep timer", aliases=['slstop'])
    @commands.guild_only()
    async def sleep_stop(self, ctx, member: discord.Member = commands.Option(default=None, description="specify member")):
        if member is None:
            member = ctx.author

        data = latte_read("sleeping")

        if f'{str(member.id)}' in data:
            try:
                del data[str(member.id)]
                latte_write(data, "sleeping")
                embed = discord.Embed(description=f"{member.mention} has stopped the timer." , color=self.bot.white_color)
                return await ctx.reply(embed=embed, mention_author=False)
            except:
                raise UtilityError("Error stop timer")

        else:
            raise UtilityError(f"**{member}** : sleep timer not found")

    @commands.command(help="Reminder")
    @commands.guild_only()
    async def remind(self, ctx, time:TimeConverter = commands.Option(description="specify duration"), *, message=commands.Option(default=None,description="message to remind")):
        if time == 0:
            embed_time = RenlyEmbed.to_error(description="Time is invalid")
            return await ctx.send(embed=embed_time, ephemeral=True, delete_after=15)
        if message is None:
            message = "..."
        elif len(message) > 2000:
            raise UtilityError('Remind message is a maximum of 2000 characters.')
        
        channel = ctx.channel
        
        #time_converter
        try:
            future = int(time)
            remind_time = datetime.now(timezone.utc) + timedelta(seconds=future)
            remind_timed = remind_time.strftime("%d%m%Y%H%M")
            future_data = humanize.naturaldelta(future, minimum_unit='milliseconds')
        except:
            raise UtilityError("Time is invalid")
        
        embed = discord.Embed(color=self.bot.white_color)
        embed.description = f'Alright {ctx.author.mention}, {future_data} : {message}'
        msg = await ctx.send(embed=embed)

        if time > 600:
            self.bot.reminding[str(ctx.author.id)] = {"message":message,"channel": channel.id,"url": msg.jump_url,"time": remind_timed}
            with open("latte_config/remind.json", "w") as fp:
                json.dump(self.bot.reminding, fp, indent=4)
        else:
            view = base_Button_URL(label="Go to original message", url=msg.jump_url)
            await discord.utils.sleep_until(remind_time)
            embed_response = discord.Embed(color=self.bot.white_color)
            embed_response.title = "Reminder"
            embed_response.description = f"{ctx.author.mention}, {format_relative(remind_time)}\n{message}"
            await ctx.channel.send(embed=embed_response, view=view)

    @commands.command(help="Disconnect timer for Voice channel", aliases=['slch'])
    @commands.guild_only()
    async def sleep_channel(self, ctx, time:TimeConverter=commands.Option(description="specify duration"), channel:discord.VoiceChannel=commands.Option(default=None,description="specify channel")):

        embed = discord.Embed()
        embed.color = self.bot.white_color

        if int(time) > 86400:
            raise UtilityError("You can't set timer duration more than 24 hours")

        if time == 0:
            raise UtilityError("Time is invalid")

        if channel is None:
            try:
                channel = ctx.author.voice.channel
                in_channel = ctx.author.voice.channel.members
            except:
                raise UtilityError('You must join a voice channel first.')

        else:
            in_channel = channel.members
        
        if channel and len(in_channel) == 0:
            raise UtilityError(f'No members found in {channel.mention}')

        timewait = int(time)
        futuredate = datetime.now(timezone.utc) + timedelta(seconds=timewait) 
        futuredate_ = futuredate.strftime("%d%m%Y%H%M")

        #fixed_utc+7
        fix_date = futuredate + timedelta(seconds=25200)
        fix_date = fix_date.strftime("%H:%M %d/%m/%Y")

        cooldown = humanize.naturaldelta(timedelta(seconds=timewait))
        
        embed.color = 0xFFFF00
        embed.add_field(name=f"**BOMB CHANNEL** {emoji_converter('sleeping')}" , value=f"** **\n**CHANNEL** : {channel.mention}\n\n`{fix_date}({cooldown})`" , inline=False)
        embed.set_footer(text=f"Total member: {len(in_channel)}")

        view = Confirm(ctx)
        m = await ctx.reply(embed=embed, view=view, mention_author=False)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            view.clear_items()
            embed_edit = discord.Embed(color=ctx.author.colour)
            embed_edit.description = f"**BOMB CHANNEL** {emoji_converter('sleeping')}\n\n**CHANNEL**: {channel.mention}\n{format_dt(futuredate, style='f')}({format_dt(futuredate, style='R')})"
            if ctx.author.avatar is not None:
                embed_edit.set_footer(text='Requested by %s' % (ctx.author) , icon_url=ctx.author.avatar.url)
            else:
                embed_edit.set_footer(text='Requested by %s' % (ctx.author))

            #chat_send
            chat_channel = ctx.guild.get_channel(861883647070437386)            
            await chat_channel.send(embed=embed_edit)

            if timewait > 600:
                self.bot.channel_sleep[str(channel.id)] = {"time": futuredate_}
                with open("latte_config/channel_sleep.json", "w") as fp:
                    json.dump(self.bot.channel_sleep, fp , indent=4)
                await m.edit(embed=embed_edit, view=view)

            else:
                await m.edit(embed=embed_edit, view=view)
                await asyncio.sleep(timewait)
                for member in in_channel:
                    await member.move_to(channel=None)
        else:
            await m.delete()
            raise UtilityError("*Cancelling!*")
    
    @commands.command(help="Stop disconnect timer", aliases=['slchstop'])
    @commands.guild_only()
    async def sleep_channel_stop(self, ctx, channel:discord.VoiceChannel=None):
        if channel is None:
            channel = ctx.author.voice.channel

        data = latte_read("channel_sleep")
        check_data = data[str(channel.id)]["time"]

        if check_data is not None:
            try:
                del data[str(channel.id)]
                latte_write(data, "channel_sleep")
                embed = discord.Embed(description=f"{channel.mention} has stopped the timer." , color=self.bot.white_color)
                return await ctx.reply(embed=embed, mention_author=False)
            except:
                UtilityError("Error stop timer")

        else:
            UtilityError("Timer not found")

    @commands.command(aliases=["trans"], help="Translate your message")
    @commands.guild_only()
    async def translate(self, ctx, to_lang=commands.Option(description="language you want to translate. like en, th, jp"), *, source=commands.Option(description="The source language you want to translate.")):
        if len(source) > 2000:
            raise UtilityError(f"The message character a maximum of 2000 characters.")
    
        translator = Translator()
        try:
            a = translator.detect(str(source))
        except:
            raise UtilityError(f"**{to_lang}** <- This language is not found")

        try:
            result =  translator.translate(f'{source}' , dest=f'{to_lang}')
            b = translator.detect(str(result.text))
        except:
            raise UtilityError("An unknown error occurred, sorry")

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name="Translate" , icon_url="https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png")
        embed.add_field(name=f"Original ({str(a.lang)})", value=f"```{source}```", inline=False)
        embed.add_field(name=f"Translated ({str(b.lang)})", value=f"```{result.text}```", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(Utility(bot))