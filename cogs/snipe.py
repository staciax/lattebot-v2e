# Standard
import discord
from discord.ext import commands
from utils.checks import is_snipe_guild

class SNIPE(commands.Cog, command_attrs = dict(slash_command=False)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')

    @commands.Cog.listener('on_message')
    async def snipe_guild(self, message):
        if message.author.bot:
            return
          
        channel = self.bot.get_channel(950654058379771985)

        if message.guild.id == 950089766488125471:
            # if message.channel.id == 950092028023279696:
            #     return

            im = None
            embed = discord.Embed(color=0xffffff, timestamp=discord.utils.utcnow())
            if message.author.avatar is not None:
                embed.set_author(name=message.author.display_name, url=message.jump_url , icon_url=message.author.avatar)
            else:
                embed.set_author(name=message.author.display_name, url=message.jump_url)

            if message.content is not None and len(message.content) != 0:
                embed.add_field(name=f"Content:", value=f"```{message.clean_content}```", inline=False)
                embed.set_footer(text=f'#{message.channel.name}')

            if message.attachments is not None:
                if len(message.attachments) > 1:
                    im = [x.proxy_url for x in message.attachments]
                    embed.add_field(name='\uFEFF',value = f"This Message Contained {len(message.attachments)} Message Attachments, Please see below.")
                
                elif message.attachments:
                    image = message.attachments[0].proxy_url
                    embed.set_image(url=image)
                    embed.set_footer(text=f'#{message.channel.name}')

            await channel.send(embed=embed)
            if im is not None:
                await channel.send(' '.join(im))

            if message.embeds:
                embed_img = message.embeds[0]
                await channel.send(content=message.clean_content or None, embed=embed_img)
    
    @commands.Cog.listener('on_voice_state_update')
    async def snipe_guild_voice(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
        
        channel = self.bot.get_channel(950659483095412736)
        
        if member.guild.id == 950089766488125471:
            embed = discord.Embed(timestamp=discord.utils.utcnow())
            if member.avatar is not None:
                embed.set_footer(text=member, icon_url=member.avatar)
            else:
                embed.set_footer(text=member)

            #voice_log
            if not before.channel and after.channel:
                embed.description = f"**JOIN CHANNEL** : `{after.channel.name}`"
                embed.color=0x77dd77            
                await channel.send(embed=embed)
        
            if before.channel and not after.channel:
                embed.description = f"**LEFT CHANNEL** : `{before.channel.name}`"
                embed.color=0xd34e4e
                await channel.send(embed=embed)
        
            if before.channel and after.channel: #and before.channel != after.channel
                if before.channel.id != after.channel.id:
                    embed.description = f"**SWITCHED CHANNELS** : `{before.channel.name}` to `{after.channel.name}`"
                    embed.color=0xfcfc64
                    await channel.send(embed=embed)

            # stream_log           
            if before.self_stream != after.self_stream:
                if after.self_stream:
                    embed.description = f"**STREAMING in `{before.channel.name}`**"
                    embed.colour=0x8A2BE2
                    await channel.send(embed=embed)
                if before.self_stream:
                    embed.description = f"**LEAVE STREAMING**"
                    embed.colour=0x8A2BE2
                    await channel.send(embed=embed)
            
            # deaf_log      
            if before.deaf != after.deaf:
                if after.deaf:
                    embed.description = f"**MEMBER DEAF**"
                    embed.colour=0xFF7878
                    await channel.send(embed=embed)
                if before.deaf:
                    embed.description = f"**MEMBER UNDEAF**"
                    embed.colour=0x77dd77
                    await channel.send(embed=embed)

            if before.mute != after.mute:
                if after.mute:
                    embed.description = f"**MEMBER MUTED**"
                    embed.colour=0xFF7878
                    await channel.send(embed=embed)
                if before.mute:
                    embed.description = f"**MEMBER UNMUTED**"
                    embed.colour=0x77dd77
                    await channel.send(embed=embed)

            if before.self_deaf != after.self_deaf:
                if after.self_deaf:
                    embed.description = f"**SELF DEAF**"
                    embed.colour=0xFF7878
                    await channel.send(embed=embed)
                if before.self_deaf:
                    embed.description = f"**SELF UNDEAF**"
                    embed.colour=0x77dd77
                    await channel.send(embed=embed)

            if before.self_mute != after.self_mute:
                if after.self_mute:
                    embed.description = f"**SELF MUTED**"
                    embed.colour=0xFF7878
                    await channel.send(embed=embed)
                if before.self_mute:
                    embed.description = f"**SELF UNMUTED**"
                    embed.colour=0x77dd77
                    await channel.send(embed=embed)

    @commands.command(aliases=['wru'])
    @is_snipe_guild()
    async def whareru(self, ctx):
        members = []
        channels = []
        for x in self.bot.guilds:
            try:
                member = x.get_member(371230466319187969)
                if member.voice is not None:
                    channels.append(member.voice.channel.name)
                    for i in member.voice.channel.members:
                        members.append(i.name)
            except:
                pass
                
        channel_txt = '\n'.join(channels)
        members_txt = ', '.join(members)

        if len(members) != 0 and len(channels) != 0:
            embed = discord.Embed(color=0xffffff)
            embed.description = f'**channel: **{channel_txt}\n**member: **{members_txt}'

            return await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        await ctx.send('NOPE')

def setup(bot):
    bot.add_cog(SNIPE(bot))