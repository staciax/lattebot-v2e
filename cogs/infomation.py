# Standard
import discord
import asyncio
import typing
from discord import Embed
from discord.ext import commands
from typing import Union

# Third party
import requests
from PIL import Image , ImageColor
from io import BytesIO
from colorthief import ColorThief

# Local
from utils.custom_button import roleinfo_view , channel_info_view , base_Button_URL , AvatarView
from utils.emoji import profile_converter, emoji_converter , status_converter
from utils.converter import *
from utils.formats import format_dt , deltaconv
from utils.custom_button import base_Button_URL
from utils.buttons import NewSimpage
from utils.errors import UserInputErrors

class Infomation(commands.Cog, command_attrs = dict(slash_command=True)):
    """All informative commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='infomation', id=903339421758292008, animated=False)

    @commands.group(help="Server commands")
    @commands.guild_only()
    async def server(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.bot.help_command.send_group_help_custom(ctx.command, ctx)

    @server.command(name="info", help="Show server infomation", aliases=["si", "serverinformation", "serverinformations" , "guildinfo" , "gi"])
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server_info(self, ctx):
        #member_status and emoji_member_status
        statuses = member_status(ctx)
        
        #emoji_count
        emoji_total = len(ctx.guild.emojis)
        emoji_regular = len([emoji for emoji in ctx.guild.emojis if not emoji.animated])
        emoji_animated = len([emoji for emoji in ctx.guild.emojis if emoji.animated])
        stickers = len(ctx.guild.stickers)

        #boost_checker
        boost = check_boost(ctx)
        
        #get_embed_color
        dominant_color = get_dominant_color(url=ctx.guild.icon.replace(format='png'))

        embed = discord.Embed(title=f"Server infomation - {ctx.guild.name}", color=dominant_color)
        fields = [("Server name",ctx.guild.name, True),
				("Server Owner",f"{ctx.guild.owner}", True),
                ("Server Region",str(ctx.guild.region).title(), True),
                ("Server Member",len([member for member in ctx.guild.members if not member.bot]), True),
                ("Server Bots",len([Member for Member in ctx.guild.members if Member.bot]), True),
                ("Server Roles",len(ctx.guild.roles), True),
                ("Text Channels",len(ctx.guild.text_channels), True),
                ("Voice Channels",len(ctx.guild.voice_channels), True),
                ("Stage Chennels",len(ctx.guild.stage_channels), True),
                ("Category size",len(ctx.guild.categories), True),
                ("AFK Chennels",ctx.guild.afk_channel or '\u200B', True),
                ("AFK Timer", f"{int(ctx.guild.afk_timeout / 60)} Minutes" if ctx.guild.afk_channel else '\u200B',True),
                ("Rules Channel", ctx.guild.rules_channel.mention if ctx.guild.rules_channel else '\u200B',True),
                ("System Channel", ctx.guild.system_channel.mention if ctx.guild.system_channel else '\u200B',True),
                ("Verification Level", ctx.guild.verification_level or '\u200B', True),
                ("Activity",f"{emoji_converter('member')} **Total:** {str(ctx.guild.member_count)}\n{status_converter('online')} **Online:** {statuses[0]} \n{status_converter('idle')} **Idle:** {statuses[1]} \n{status_converter('dnd')} **Dnd:** {statuses[2]} \n{status_converter('offline')} **Offline:** {statuses[3]}",True),
                ("Boosts",boost,True),
                ("Emoji",f"**Total:** {emoji_total}\n**Regular:** {emoji_regular}\n**Animated:** {emoji_animated}\n**Sticker:** {stickers}",True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
    
        await ctx.send(embed=embed)
     
    @server.command(name="icon", help="Shows the server icon.", aliases=["servericon","guildicon" ,"sic"])
    @commands.guild_only()
    async def server_icon(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title = f"{guild.name}'s Icon:")

        #get_embed_color
        dominant_color = get_dominant_color(url=guild.icon.replace(format='png'))

        try:
            embed.color = dominant_color
            embed.set_image(url = guild.icon.url)

            view = base_Button_URL(label="Server icon URL", url=guild.icon.url)
        except:
            raise UserInputErrors('Server icon not found')

        await ctx.send(embed=embed, view=view)

    
    @server.command(name="banner", help="Shows the server banner.", aliases=["serverbanner","sb","guildbanner"], message_command=False)
    @commands.guild_only()
    async def server_banner(self, ctx):
        guild = ctx.guild
        try:
            embed = discord.Embed(title = f"{guild.name}'s Banner:", color=self.bot.white_color).set_image(url = guild.banner.url)
            view = base_Button_URL(label="Server banner URL", url=guild.banner.url)
            await ctx.send(embed = embed, view=view)
        except:
            raise UserInputErrors('Server banner not found')
    
    @server.command(name="splash", help="Shows the server invite banner.", aliases=["serversplash","ssp","invitebanner"], message_command=False)
    @commands.guild_only()
    async def server_splash(self, ctx):
        guild = ctx.guild
        try:
            embed = discord.Embed(title = f"{guild.name}'s Splash banner:", color=self.bot.white_color).set_image(url = guild.splash.url)
            view = base_Button_URL(label="Splash URL", url=guild.splash.url)
            await ctx.send(embed=embed , view=view)
        except:
            raise UserInputErrors('Server splash not found')

    @commands.command(name="userinfo", help="Shows information about the specified member.", aliases=["ui", "userinformation","memberinfo"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.guild.get_member(ctx.author.id)
        
        #member_status
        m_mobile = f"{status_converter(str(member.mobile_status))} Moblie"
        m_desktop = f"{status_converter(str(member.desktop_status))} Desktop"
        m_Web = f"{status_converter(str(member.web_status))} Web"
        
        #member_badge
        flags = member.public_flags.all()
        badges ="\u0020".join(profile_converter(f.name) for f in flags)
        if member.bot: badges = f"{badges} {profile_converter('bot')}"
        if member.premium_since: badges = f"{badges} {profile_converter('guildboost')}"

        #member_info
        member_joined = format_dt(member.joined_at, style='d')
        member_created = format_dt(member.created_at, style='d')
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        member_activity = f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "** **"
        roles = [role for role in member.roles]
        role_str = []
        if len(member.roles) > 1: role_string = ' '.join(reversed([r.mention for r in member.roles][1:]))
        else: role_string = "this user don't have a role"
        
        #fetch_banner
        fetch_member = await self.bot.fetch_user(member.id)
        #if fetchedMember.banner.is_animated() == True:

        #dominant_colour_user_info
        try:
            url = member.avatar.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            dominant_color = self.bot.white_color
            if member.color != discord.Colour.default():
                dominant_color = member.colour

        #start_view
        view = discord.ui.View()
        style = discord.ButtonStyle.gray 

        embed = discord.Embed(title=f"{member}'s Infomation",colour=dominant_color)  #timestamp=ctx.message.created_at
        fields = [("Nickname",f"{member.display_name}", True),
                ("Is bot?","Yes" if member.bot else "No", True),
                ("Activity",member_activity, True),
                ("Join position",f"{str(members.index(member)+1)}/{ctx.guild.member_count}", True),
                ("Joined",f"{member_joined}", True),
                ("Registered",f"{member_created}", True),
                ("Status",f"{m_desktop}\n{m_mobile}\n{m_Web}", True),
                ("Badge",f"{badges}** **", True),
                ("Top Role",member.top_role.mention, False),
                ("Roles ({})\n".format(len(member.roles)-1), role_string , False)]

        for name , value , inline in fields:
            embed.add_field(name=name , value=value , inline=inline)

        if member.avatar.url is not None:
            embed.set_thumbnail(url=member.avatar.url)
            item = discord.ui.Button(style=style, label="Avatar URL", url=member.avatar.url)
            view.add_item(item=item)
        if fetch_member.banner:
            embed.set_image(url=fetch_member.banner.url)
            item2 = discord.ui.Button(style=style, label="Banner URL", url=fetch_member.banner.url) 
            view.add_item(item=item2)
        elif fetch_member.accent_color:
            embed.add_field(name=f"Banner color" , value=f"{fetch_member.accent_color} (HEX)", inline=False)
            embed.set_footer(text=f"ID: {member.id}")

        await ctx.send(embed=embed , view=view)

    @commands.command(help="Shows the user avatar of the specified member.", aliases=["av"])
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.author
        if member.avatar is not None:
            view = AvatarView(ctx, member)
            await view.start()
        else:
            raise UserInputErrors(f'**{member.display_name}** must have a avatar.')

    @commands.command(help="Shows the banner of the specified member.", aliases=["bn"])
    @commands.guild_only()
    async def banner(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.author
        fetch_member = await self.bot.fetch_user(member.id)
        
        embed = discord.Embed(title=f"{member.name}'s Banner:")
        if fetch_member.banner:
            embed.set_image(url=fetch_member.banner.url)
            
            #dominant_colour_banner
            dominant_color = get_dominant_color(url=fetch_member.banner.replace(format='png'))
            
            #dominant_color
            embed.color = dominant_color

            view = base_Button_URL(label="Banner URL", url=fetch_member.banner.url)
            await ctx.send(embed=embed , view=view)
        elif fetch_member.accent_color:
            img = Image.new("RGB", (256, 144), ImageColor.getrgb(f"{fetch_member.accent_color}"))
            buffer = BytesIO()
            img.save(buffer, 'png')
            buffer.seek(0)
            f = discord.File(buffer, filename='banner.png')

            embed.color = fetch_member.accent_color
            embed.set_image(url="attachment://banner.png")
            embed.add_field(name=f"this user don't have banner\n\nAccent color:" , value=f"{fetch_member.accent_color} (HEX)", inline=False)
            await ctx.send(file=f, embed=embed)
        else:
            raise UserInputErrors("this user don't have a banner.")

    @commands.group(help="Role commands")
    @commands.guild_only()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.bot.help_command.send_group_help_custom(ctx.command, ctx)

    @role.command(name="info",aliases=["ri"], help="Shows information about the specified role.")
    @commands.guild_only()
    async def role_info(self, ctx, role: discord.Role = commands.Option(description="Mention role")):
        embed_role = discord.Embed(color=role.color)
        role_perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
        info = f"""
        **Mention**: {role.mention}
        **ID**: {role.id}
        **Name**: {role.name}
        **Color**: {role.color}
        **Create**: {format_dt(role.created_at)}
        **Positon**: {role.position}
        **Members**: {len(role.members)}
        **Permission**: {role_perm_string}
        """
        embed_role.description = f"{info}"

        role_member_list = []

        for x in role.members:
            member_role = f"{x} | `{x.id}`"
            role_member_list.append(member_role)

        view = roleinfo_view(ctx=ctx, embed=embed_role, entries=role_member_list, role=role)
        view.message = await view.start()
    
    @commands.group(help="Emoji commands")
    @commands.guild_only()
    async def emoji(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.bot.help_command.send_group_help_custom(ctx.command, ctx)
    
    @emoji.command(name="info", help="Shows information about a emoji.")
    @commands.guild_only()
    async def emoji_info(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, UnicodeEmojiConverter] = commands.Option(description="Emoji")):
        if isinstance(emoji, discord.Emoji):
            try:
                emoji = await emoji.guild.fetch_emoji(emoji.id)
            except discord.NotFound:
                raise UserInputErrors("I could not find this emoji in the given server.")
            except discord.HTTPException:
                raise UserInputErrors("An error occurred fetching the emoji.")
            is_managed = "Yes" if emoji.managed else "No"
            is_animated = "Yes" if emoji.animated else "No"
            is_available = "Yes" if emoji.available else "No"
            requires_colons = "Yes" if emoji.require_colons else "No"
            creation_time = format_dt(emoji.created_at)
            can_use_emoji = (
                "Everyone"
                if not emoji.roles
                else " ".join(role.name for role in emoji.roles)
            )

            description = f"""
            **Name:** {emoji.name}
            **Id:** {emoji.id}
            **Aimated:** {is_animated}
            **Managed:** {is_managed}
            **Available** {is_available}

            **Author:** {emoji.user.mention}
            **Time Created:** {creation_time}
            **Guild Name:** {emoji.guild.name}
            **Guild Id:** {emoji.guild.id}
            """
            embed = discord.Embed(
                title=f"**Emoji Information for:** `{emoji.name}`",
                description=description,
                colour=self.bot.white_color,
            )
            embed.set_thumbnail(url=emoji.url)
            view = base_Button_URL(label="Emoji URL", url=emoji.url)
            await ctx.send(embed=embed , view=view)
        elif isinstance(emoji, discord.PartialEmoji):
            url = f"{emoji.url}"
            is_animated = "Yes" if emoji.animated else "No"
            creation_time = format_dt(emoji.created_at)
            
            description = f"""
            **Name:** {emoji.name}
            **Id:** {emoji.id}
            **Aimated:** {is_animated}
            """

            embed = discord.Embed(
                title=f"**Emoji Information for:** `{emoji.name}`",
                description=description,
                colour=self.bot.white_color,
            )
            embed.set_thumbnail(url=emoji.url)

            view = base_Button_URL(label="Emoji URL", url=emoji.url)
            await ctx.send(embed=embed , view=view)

        else:
            raise UserInputErrors(f"{emoji} <- This is unicode emoji")

    @emoji.command(name="list",help="Shows you a list of emotes from the server.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def emotelist(self, ctx):
        guild = ctx.guild
        guildEmotes = guild.emojis
        if not guildEmotes or len(guildEmotes) == 0:
            raise UserInputErrors("This server don't have emoji")

        emotes = []

        for emoji in guildEmotes:
            if emoji.animated:
                emotes.append(f"<a:{emoji.name}:{emoji.id}> **|** `{emoji.name}` **|** [`<a:{emoji.name}:{emoji.id}>`]({emoji.url})")
            if not emoji.animated:
                emotes.append(f"<:{emoji.name}:{emoji.id}> **|** `{emoji.name}` **|** [`<:{emoji.name}:{emoji.id}>`]({emoji.url})")

        p = NewSimpage(entries=emotes, ctx=ctx)
        p.embed.title = f"{guild.name} emojis ({len(guildEmotes)})"
        p.embed.color = self.bot.white_color
        await p.start()
        
    @commands.command(help="Shows information about the specified channel.")
    @commands.guild_only()
    async def channel_info(self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel] = commands.Option(description="Channel infomation")):
        embed = Embed(color=self.bot.white_color)
        embed.title = f"{channel.name}'s Info"
        if str(channel.type) == "voice": embed.add_field(
            name="infomation:",
            value=f"**Type:** voice channel\n**Birate:** {int(channel.bitrate / 1000)}kbps\n**Region:** {channel.rtc_region}\n**Connected:** {len(channel.members)} connected",
            inline=False
        )
        else: embed.add_field(
            name="infomation:", 
            value=f"**Type:** {channel.type} channel\n**Topic** : {channel.topic}\n**NSFW** : {channel.nsfw}",
            inline=False
        )
        
        role_list = []
        member_list = []
        for role in channel.changed_roles:
            role_msg = f"{role.mention} | `{role.id}`"
            role_list.append(role_msg)
        for member in channel.members:
            member_msg = f"{member.name} | `{member.id}`"
            member_list.append(member_msg)
              
        embed.add_field(name="Category:" , value=f"{channel.category}" , inline=False)
        embed.add_field(name="Create date:" , value=f"{format_dt(channel.created_at)}" , inline=False)
        embed.set_thumbnail(url=channel.guild.icon.url)
        embed.set_footer(text=f"ID : {channel.id}")

        if str(channel.type) == 'voice':
            view = channel_info_view(ctx=ctx, embed=embed, channel=channel, role_list=role_list, member_list=member_list)
            view.message = await view.start_voice()
        else:
            view = channel_info_view(ctx=ctx, embed=embed, channel=channel, role_list=role_list, member_list=member_list)
            view.message = await view.start_text()
        
    @commands.command(help="Shows the first message of the specified channel.")
    @commands.guild_only()
    async def first_message(self, ctx, channel : discord.TextChannel = commands.Option(description="mention channel")):
        async for message in channel.history(limit=1, oldest_first=True):
            content = message.content
            if len(content) > 25:
                content = f"`please click button 'Go to message'`"

            view = base_Button_URL(label="Go to original message", url=message.jump_url)

            embed = discord.Embed(color=0xffffff)
            embed.title = f"First message in #{channel.name}"
            embed.url = message.jump_url
            embed.description = f"**Content:** {content}\n**Author:** {message.author.mention}\n**Sent at:** {discord.utils.format_dt(message.created_at, style='F')} ({discord.utils.format_dt(message.created_at, style='R')})"
            embed.set_footer(text=f"Message ID : {message.author.id}")

            return await ctx.send(embed=embed, view=view)

    @commands.command(name="status", help="Shows status about the specified member.")
    @commands.guild_only()
    async def status_(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):

        member = member or ctx.guild.get_member(ctx.author.id)

        def status_converter(name):
            names_to_status = {
                "online" : "<:online:900262151992774717>",
                "dnd" : "<:dnd:900262199828824095>",
                "idle" : "<:idle:900262218619289650>",
                "offline" : "<:offline:900262246276538369>",
            }
            return names_to_status.get(name)

        m = status_converter(str(member.mobile_status))
        d = status_converter(str(member.desktop_status))
        w = status_converter(str(member.web_status))

        #embed
        embed = discord.Embed(color=member.colour)
        embed.set_author(name=member , icon_url=ctx.author.avatar or ctx.author.default_avatar)
        embed.description = f"{d} Desktop\n{m} Mobile\n{w} Web"

        await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(help="Shows info about the song the specified member is currently listening to.")
    @commands.guild_only()
    async def spotify(self, ctx, member: discord.Member=commands.Option(default=None, description="Spectify member")): 
        
        member = member or ctx.guild.get_member(ctx.author.id)
        spotify = discord.utils.find(lambda act: isinstance(act, discord.Spotify), member.activities)

        if spotify:
            duration = f"Duration: {deltaconv((ctx.message.created_at - spotify.start).total_seconds())} / {deltaconv(spotify.duration.total_seconds())}"
            embed = discord.Embed()
            embed.title = f"{member.name} is listening to {spotify.title}"
            embed.description = f"Title: [{spotify.title}]({spotify.track_url})\n{duration}\nArtists: {', '.join(spotify.artists)}\nTrack ID: `{spotify.track_id}`"
            embed.color = spotify.color
            embed.set_image(url=spotify.album_cover_url)
            speac = '\u2001'*6
            view = discord.ui.View()
            view.add_item(discord.ui.Button(emoji=f"{emoji_converter('spotify')}",label=f"Listen on spoify{speac}",url=spotify.track_url))
            view.add_item(discord.ui.Button(label="≡"))
            for x in view.children:
                if x.label == '≡':
                    x.disabled = True

            await ctx.send(embed=embed, view=view)

        else:
            raise UserInputErrors("That member doesn't have a spotify status!")
            
    @commands.command(
    help="Shows you a list of members from the server.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def memberlist(self, ctx):
        guild = ctx.guild
        guildMembers = guild.members
        members = []
        for member in guildMembers:
            members.append(f"{member.name} **|** {member.mention} **|** `{member.id}`")
        
        p = NewSimpage(entries=members, ctx=ctx)
        p.embed.title = f"{guild.name} members ({len(guildMembers)})"
        p.embed.color = self.bot.white_color
        await p.start()
            
def setup(bot):
    bot.add_cog(Infomation(bot))