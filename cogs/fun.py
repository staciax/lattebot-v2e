# Standard
import discord
import asyncio
from discord.ext import commands

# Third

# Local
from utils.custom_button import Random_member
from utils.game_random import APEX_RANDOM, ValorantView

class FunError(commands.CommandError):
    pass

class Fun(commands.Cog, command_attrs=dict(slash_command=True)):
    """Fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='🥳')

    @commands.command(name="voice_random", aliases=["rnv"], help="random members in voice channel")
    @commands.guild_only()
    async def random_voice_member(self, ctx, channel: discord.VoiceChannel = commands.Option(default=None, description="spectify channel")):

        # check
        if channel is None:
            if not ctx.author.voice:
                raise FunError("You must join a voice channel first.")
            channel = ctx.author.voice.channel
            in_channel = ctx.author.voice.channel.members
        else:
            in_channel = channel.members

        # get_member_in_voice
        member_list = []

        for members in in_channel:
            member_voice = members
            member_list.append(member_voice)

        p = Random_member(entries=member_list, ctx=ctx,
                          member_list=member_list)
        p.embed.title = f"Members - {channel.name}"
        p.embed.color = self.bot.white_color
        await p.start()

    @commands.command(name="apex", help="apex random legend, weapon")
    @commands.guild_only()
    async def apex(self, ctx):
        view = APEX_RANDOM(ctx)
        await view.start()

    @commands.command(name="valorant", aliases=["vlr", "valo"], help="valorant random agent, weapon")
    @commands.guild_only()
    async def valorant(self, ctx):
        view = ValorantView(ctx)
        await view.start()

    @commands.command(aliases=['lattesay','botsay'], help="Message something you give latte to say.")
    @commands.guild_only()
    async def latte_say(self, ctx, *, message=commands.Option(description="message to be latte say")):
        if ctx.clean_prefix == "/":
            await ctx.send('** **', ephemeral=True)
        await ctx.channel.send(f'{message}')

    @commands.command(help="Genshin impact map guide", aliases=["gsmap"])
    @commands.guild_only()
    async def genshinmap(self, ctx):
        embed = discord.Embed(color=0x2484d7)
        embed.set_author(name='Genshin impact Map',
                         icon_url="https://cdn.discordapp.com/emojis/892114299793842266.png")
        # start_view_button
        view = discord.ui.View()
        Off = discord.ui.Button(style=discord.ButtonStyle.gray,
                                label="Mihoyo", url="https://webstatic-sea.mihoyo.com/")
        Un = discord.ui.Button(style=discord.ButtonStyle.gray, label="genshin-impact-map",
                               url="https://genshin-impact-map.appsample.com/#/")
        view.add_item(item=Off)
        view.add_item(item=Un)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="pastel", help="pastel color")
    @commands.guild_only()
    async def pastel(self, ctx):
        await ctx.reply("https://colorhunt.co/palettes/pastel", mention_author=False)

    @commands.command(name="color", help="color hex")
    @commands.guild_only()
    async def color(self, ctx):
        await ctx.reply("https://www.color-hex.com/", mention_author=False)

def setup(bot):
    bot.add_cog(Fun(bot))
