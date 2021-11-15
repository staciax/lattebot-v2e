# Standard
import discord
import asyncio
from discord.ext import commands

# Third

# Local
from utils.checks import is_latte_guild

class Latte(commands.Cog, command_attrs = dict(slash_command=True)):
    """Commands only latte server"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='latte_icon_new', id=907030425011109888, animated=False)
    
    @commands.command(aliases=['lt'], help="latte server template")
    @commands.guild_only()
    @is_latte_guild()
    async def latte_template(self, ctx):
        await ctx.send("https://discord.new/sFYKgkknRN5f")

    @commands.command(aliases=['ls'], help="lattte temp role")
    @commands.guild_only()
    @is_latte_guild()
    async def latte_temp_role(self, ctx, *, member: discord.Member = commands.Option(default=None, description="Give role to member")):
        if ctx.guild.id == self.bot.latte_guild_id:
            if not member:
                member = ctx.author
            role = discord.utils.get(ctx.guild.roles, id=879258879987449867)
            member_role = discord.utils.get(
                member.roles, id=879258879987449867)
            if member_role:
                embed_role = discord.Embed(
                    description=f"{member.name} is already a temp role!", color=self.bot.white_color)
                return await ctx.send(embed=embed_role, ephemeral=True, delete_after=15)
            await member.add_roles(role)
            embed = discord.Embed(
                description="Temp is ready\n`This role will disappear within 2 hour.`", color=self.bot.white_color)
            await ctx.send(embed=embed, ephemeral=True)
            await asyncio.sleep(7200)
            await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Latte(bot))