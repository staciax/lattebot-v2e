# Standard
import discord
import re
from discord.ext import commands
# Third

# Local

class Star(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spoilers = re.compile(r'\|\|(.+?)\|\|')
        self.latte_star_channel = [861883647070437386, 840398821544296480, 863438518981361686, 850507964938715196, 908360879769272350, 877489788188499998, 861874852050894868, 859960606761549835, 872139991436890132]
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{WHITE MEDIUM STAR}')

    async def get_starboard(self, message_id):
        data = await self.bot.latte_stars.find_by_custom({"message_id": message_id})    
        return data
    
    def star_emoji(self, stars):
        if 5 > stars >= 0:
            return '\N{WHITE MEDIUM STAR}'
        elif 10 > stars >= 5:
            return '\N{GLOWING STAR}'
        elif 25 > stars >= 10:
            return '\N{DIZZY SYMBOL}'
        else:
            return '\N{SPARKLES}'
   
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    def star_gradient_colour(self, stars):
        p = stars / 13
        if p > 1.0:
            p = 1.0

        red = 255
        green = int((194 * p) + (253 * (1 - p)))
        blue = int((12 * p) + (247 * (1 - p)))
        return (red << 16) + (green << 8) + blue
    
    def is_url_spoiler(self, text, url):
        spoilers = self.spoilers.findall(text)
        for spoiler in spoilers:
            if url in spoiler:
                return True
        return False

    def get_emoji_message(self, message, stars):
        emoji = self.star_emoji(stars)

        if stars > 1:
            content = f'{emoji} **{stars}** {message.channel.mention} ID: {message.id}'
        else:
            content = f'{emoji} {message.channel.mention} ID: {message.id}'

        embed = discord.Embed(description=message.content)
        if message.embeds:
            data = message.embeds[0]
            if data.type == 'image' and not self.is_url_spoiler(message.content, data.url):
                embed.set_image(url=data.url)

        if message.attachments:
            file = message.attachments[0]
            spoiler = file.is_spoiler()
            if not spoiler and file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                embed.set_image(url=file.url)
            elif spoiler:
                embed.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
            else:
                embed.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)

        ref = message.reference
        if ref and isinstance(ref.resolved, discord.Message):
            embed.add_field(name='Replying to...', value=f'[{ref.resolved.author}]({ref.resolved.jump_url})', inline=False)

        embed.add_field(name='Original', value=f'[Jump!]({message.jump_url})', inline=False)
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url or message.author.default_avatar.url)
        embed.timestamp = message.created_at
        embed.colour = self.star_gradient_colour(stars)
        return content, embed
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id == self.bot.latte_guild_id:
            if payload.channel_id not in self.latte_star_channel:
                return
            if str(payload.emoji) != '\N{WHITE MEDIUM STAR}':
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.author.bot and payload.member.id != message.author.id or payload.member == 240059262297047041:
                data = await self.bot.latte_stars.find_by_custom({"message_id": message.id})            
                if data is None:
                    count = 1
                    content, embed = self.get_emoji_message(message, stars=count)
                    starboard_channel = self.bot.get_channel(self.bot.latte_starbot_id)
                    msg = await starboard_channel.send(content=content, embed=embed)

                    data = {
                        "stars": 1,
                        "channel_id": message.channel.id,
                        "jump_url": message.jump_url,
                        "message_bot": msg.id,
                        "channel_bot_id": msg.channel.id
                    }
                    return await self.bot.latte_stars.update_by_custom({"message_id": message.id}, data)
                
                else:
                    message_bot = await self.bot.get_channel(data["channel_bot_id"]).fetch_message(data["message_bot"])
                    count = data["stars"] + 1
                    content, embed = self.get_emoji_message(message, stars=count)
                    await message_bot.edit(content=content,embed=embed)
                    return await self.bot.latte_stars.update_by_custom({"message_id": message.id}, {"stars": count})

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id == self.bot.latte_guild_id:
            if payload.channel_id not in self.latte_star_channel:
                return
            if str(payload.emoji) != '\N{WHITE MEDIUM STAR}':
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.author.bot and payload.user_id != message.author.id or payload.user_id == 240059262297047041:
                data = await self.bot.latte_stars.find_by_custom({"message_id": message.id})          
                if data is not None:
                    message_bot = await self.bot.get_channel(data["channel_bot_id"]).fetch_message(data["message_bot"])
                    count = data["stars"] - 1
                    if count == 0:
                        await message_bot.delete()
                        await self.bot.latte_stars.delete_by_custom({"message_id": message.id})
                        return
                    content, embed = self.get_emoji_message(message, stars=count)
                    await message_bot.edit(content=content,embed=embed)
                    return await self.bot.latte_stars.update_by_custom({"message_id": message.id}, {"stars": count})
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id == self.bot.latte_guild_id:
            if payload.channel_id not in self.latte_star_channel:
                return
            data = await self.get_starboard(message_id=payload.message_id)
            if data is not None:
                try:
                    star_message = data["message_id"]
                    if payload.message_id == star_message:
                        message_bot = await self.bot.get_channel(data["channel_bot_id"]).fetch_message(data["message_bot"])
                        await self.bot.latte_stars.delete_by_custom({"message_id": payload.message_id})
                        await message_bot.delete()
                except TypeError: 
                    pass
                except KeyError: 
                    pass

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):    
        if payload.guild_id == self.bot.latte_guild_id:
            if payload.channel_id not in self.latte_star_channel:
                return
            for msg_id in payload.message_ids:
                data = await self.get_starboard(message_id=msg_id)
                if data is not None:
                    try:
                        star_message = data["message_id"]
                        if msg_id == star_message:
                            message_bot = await self.bot.get_channel(data["channel_bot_id"]).fetch_message(data["message_bot"])
                            await self.bot.latte_stars.delete_by_custom({"message_id": msg_id})
                            await message_bot.delete()
                    except TypeError: 
                        pass
                    except KeyError: 
                        pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload):
        if payload.guild_id == self.bot.latte_guild_id:
            if payload.channel_id not in self.latte_star_channel:
                return
            data = await self.get_starboard(message_id=payload.message_id)
            if data is not None:
                try:
                    star_message = data["message_id"]
                    if payload.message_id == star_message:
                        message_bot = await self.bot.get_channel(data["channel_bot_id"]).fetch_message(data["message_bot"])
                        await self.bot.latte_stars.delete_by_custom({"message_id": payload.message_id})
                        await message_bot.delete()
                except TypeError: 
                    pass
                except KeyError: 
                    pass
            
def setup(bot):
    bot.add_cog(Star(bot))