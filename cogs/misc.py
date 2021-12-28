# Standard
import discord
import platform
import time
import re
import os
import io
import zlib
from discord.ext import commands
from datetime import datetime, timedelta, timezone

# Third

# Local
from utils.emoji import emoji_converter
from utils.formats import format_dt , count_python
from utils import fuzzy
from utils.errors import UserInputErrors

class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')

class Misc(commands.Cog, command_attrs = dict(slash_command=True)):
    """Misc commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='misc', id='914142887854358588', animated=False)

    @commands.command(help="Invite me")
    # @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def invite(self, ctx):
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=1101273620486&scope=bot%20applications.commands"
        view = discord.ui.View()
        invite_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Invite me", url=invite_url) 
        view.add_item(item=invite_button)

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} Invite", icon_url=self.bot.user.avatar.url, url=invite_url)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    
    @commands.command(help="Vote for me")
    # @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def vote(self, ctx):
        view = discord.ui.View()
        vote_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Vote for me", url="https://top.gg/bot/894156599906689095/vote") 
        view.add_item(item=vote_button)
        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} Vote for me", icon_url=self.bot.user.avatar.url, url=self.bot.latte_supprt_url)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    
    @commands.command(help="Sends the support server of the bot.")
    # @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def support(self, ctx):
        view = discord.ui.View()
        support_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Click to join", url=self.bot.latte_supprt_url) 
        view.add_item(item=support_button)

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} Support server", icon_url=self.bot.user.avatar.url, url=self.bot.latte_supprt_url)
        await ctx.reply(embed=embed, view=view, mention_author=False)

    @commands.command(help="Shows the bot's prefixes")
    @commands.guild_only()
    async def prefix(self, ctx):
        prefix = await self.bot.command_prefix(self.bot, ctx.message)

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"{self.bot.user.name} prefixes:" , icon_url=self.bot.user.avatar.url)
        embed.description = f"{self.bot.user.mention}\n/\n{prefix[2]}"
        await ctx.reply(embed=embed, ephemeral=True, mention_author=False)
    
    @commands.command(aliases=["botinfo"], help="Shows basic information about the bot.")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def about(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        owner_bot = self.bot.renly
        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"About Me", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=owner_bot.avatar.url)

        #stats
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        # totalcogs = len(self.bot.cogs)
        totalcommands = len(self.bot.commands)
        totalslash = f"\n{emoji_converter('bot_commands')} Slash : `{len([c for c in self.bot.commands if c.slash_command == True])}`"

        if ctx.guild.id == self.bot.latte_guild_id:
            latte_db = f"\n{emoji_converter('mongo')} Database : `MongoDB`"

        embed.add_field(name="About Developer", value=f"Owner: [{owner_bot}](https://discord.com/users/{owner_bot.id})", inline=False)
        embed.add_field(name="Stats ", value=f"{emoji_converter('cursor')} Line count : `{count_python('.'):,}`\n{emoji_converter('latte_icon')} Servers : `{serverCount}`\n{emoji_converter('member')} Users : `{memberCount}`\n{emoji_converter('bot_commands')} Commands : `{totalcommands}`" + [totalslash if ctx.author == self.bot.renly else '\u200B'], inline=False)
        embed.add_field(name="Bot Info",value=f"{emoji_converter('latte_icon')} {self.bot.user.name} : `{self.bot.bot_version}`\n{emoji_converter('python')} Python : `{platform.python_version()}`\n{emoji_converter('dpy')} Discord.py : `{discord.__version__}`{latte_db or '\u200B'}", inline=False)
        
        await ctx.reply(embed=embed, mention_author=False)
        
        # embed.add_field(name="Bot created" , value=f"{format_dt(self.bot.user.created_at)}" , inline=False)    
        #start_view_button
        # view = discord.ui.View()
        # style = discord.ButtonStyle.gray
        #Source_code = discord.ui.Button(emoji=f"{utils.emoji_converter('github')}",style=style, label="Source code", url=self.bot.latte_source)
        #Vote.gg = discord.ui.Button(style=style, label="Source code", url=self.bot.latte_source)
        # view.add_item(item=Source_code)
    


    @commands.command(help="Shows the latency of the bot")
    @commands.guild_only()
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)

        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = round((typinge - typings) * 1000)

        dbstart = time.monotonic()
        await self.bot.latte_ping.find_by_custom({"stacia_id": 240059262297047040})
        dbend = time.monotonic()

        sqlstart = time.monotonic()
        await self.bot.pg_con.fetch("SELECT * FROM public.blacklist;")
        sqlend = time.monotonic()
       
        embed = discord.Embed(color=self.bot.white_color)
        embed.add_field(name=f"{emoji_converter('latte_icon')} Latency", value=f"```nim\n{bot_latency} ms```", inline=True)
        embed.add_field(name=f"{emoji_converter('cursor')} Typing", value=f"```nim\n{typingms} ms```", inline=True)
        if ctx.guild.id == self.bot.latte_guild_id:
            embed.add_field(name=f"{emoji_converter('mongo')} Database", value=f"```nim\n{(dbend-dbstart)*1000:,.0f} ms```", inline=True)
        embed.add_field(name=f"{emoji_converter('postgresql')} Postgresql", value=f"```nim\n{round((sqlend-sqlstart)*1000)} ms```", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(help="Report to owner bot")
    @commands.guild_only()
    async def report(self, ctx, *, message=commands.Option(description="Input report message")):
        embed = discord.Embed(color=0xffffff, timestamp=ctx.message.created_at)
        embed.set_author(name=f'{ctx.guild.name} | User report',)
        if ctx.guild.icon:
            embed.set_author(name=f'{ctx.guild.name} | User report', icon_url=ctx.guild.icon.url)
        embed.description = f"{message}"
        embed.set_footer(text="Reported by", icon_url=ctx.author.avatar or ctx.author.default_avatar)
        try:
            await self.bot.renly.send(embed=embed)
        except (discord.HTTPException, discord.HTTPException, discord.InvalidArgument):
            raise UserInputErrors('Failed to send message to owner bot')

        embed_send = discord.Embed(color=0xffffff, timestamp=ctx.message.created_at)
        embed_send.description = 'Thanks you, Message successfully sent! <3"'
        await ctx.reply(embed=embed_send, mention_author=False)
    
# ---------- Search the documentation ---------- #

    def parse_object_inv(self, stream, url):
        # key: URL
        # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
        result = {}

        # first line is version info
        inv_version = stream.readline().rstrip()

        if inv_version != '# Sphinx inventory version 2':
            raise RuntimeError('Invalid objects.inv file version.')

        # next line is "# Project: <name>"
        # then after that is "# Version: <version>"
        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]

        # next line says if it's a zlib header
        line = stream.readline()
        if 'zlib' not in line:
            raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

        # This code mostly comes from the Sphinx repository.
        entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(':')
            if directive == 'py:module' and name in result:
                # From the Sphinx Repository:
                # due to a bug in 1.1 and below,
                # two inventory entries are created
                # for Python modules, and the first
                # one is correct
                continue

            # Most documentation pages have a label
            if directive == 'std:doc':
                subdirective = 'label'

            if location.endswith('$'):
                location = location[:-1] + name

            key = name if dispname == '-' else dispname
            prefix = f'{subdirective}:' if domain == 'std' else ''

            if projname == 'discord.py':
                key = key.replace('discord.ext.commands.', '').replace('discord.', '')

            result[f'{prefix}{key}'] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.bot.session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError('Cannot build rtfm lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'edpy': 'https://enhanced-dpy.readthedocs.io/en/latest',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
            'master': 'https://discordpy.readthedocs.io/en/master',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_rtfm_cache'):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._rtfm_cache[key].items())
        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            raise UserInputErrors('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.reply(embed=e, mention_author=False)

    @commands.group(help="Search the documentation", aliases=["rtd", "rtfs"], invoke_without_command=True)
    @commands.guild_only()
    async def rtfm(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.bot.help_command.send_group_help_custom(ctx.command, ctx)

    @rtfm.command(name='dpy', aliases=['discord'], help='Search the Discord.py docs')
    @commands.guild_only()
    async def rtfm_dpy(self, ctx, *, search: str = commands.Option(description='Item to search for')):
        await self.do_rtfm(ctx, 'latest', search)

    @rtfm.command(name='edpy', help='Search the Enhanced-dpy docs')
    @commands.guild_only()
    async def rtfm_edpy(self, ctx, *, search: str = commands.Option(description='Item to search for')):
        await self.do_rtfm(ctx, 'edpy', search)
    
    @rtfm.command(name='python', aliases=['py'], help='Search the Python docs')
    @commands.guild_only()
    async def rtfm_python(self, ctx, *, search: str = commands.Option(description='Item to search for')):
        """Gives you a documentation link for a Python entity."""
        await self.do_rtfm(ctx, 'python', search)
    
def setup(bot):
    bot.add_cog(Misc(bot))