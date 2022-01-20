# Standard 
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from utils.formats import format_dt 

# Third party
# Local
from utils.checks import is_latte_guild
from utils.latte_converter import fancy_text

class No_slash(commands.Cog, command_attrs = dict(slash_command=False)):
    """Only message command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='createthread', id=903346472509141023, animated=False)

    @commands.command(name="pastel", help="pastel color")
    @commands.guild_only()
    @is_latte_guild()
    async def pastel(self, ctx):
        await ctx.reply("https://colorhunt.co/palettes/pastel", mention_author=False)

    @commands.command(name="hex", help="color hex")
    @commands.guild_only()
    @is_latte_guild()
    async def hex_(self, ctx):
        await ctx.reply("https://www.color-hex.com/", mention_author=False)
    
    @commands.command(name='uptime', help="Gets the uptime of the bot")
    @commands.guild_only()
    @is_latte_guild()
    async def uptime(self, ctx):
        uptime = datetime.utcnow() - self.bot.launch_time
        futuredate = datetime.now(timezone.utc) - timedelta(seconds=int(uptime.total_seconds())) 
        embed = discord.Embed(description=f"🕘 I started {format_dt(futuredate, style='R')}", color=self.bot.white_color)
        await ctx.send(embed=embed)

    @commands.command(name='ftext')
    @commands.guild_only()
    @is_latte_guild()
    async def ftext(self, ctx, *, text):
        if len(text) == 0 or len(text) > 200:
            return
        
        def split(word):
            return list(word)

        text_list = split(text)
        output = ''
        for x in text_list:
            try:
                output += fancy_text[x]
            except:
                output += x

        if text_list:
            await ctx.send(output)
    
    # @commands.command(name="reactionrole")
    # @commands.guild_only()
    # @commands.is_owner()
    # async def reactionrole(self, ctx):
    #     await ctx.message.delete()
    #     await ctx.send('https://i.imgur.com/ZmjnNaS.png')
    #     await ctx.send("˚｡ *╭ <a:ab_purplesparklingstar:859370464711278612>  **__ let's reaction__** <a:ab_purplesparklingstar:859370464711278612>   ʕつ ͡◔ ᴥ ͡◔ʔつ\n<:aa_dash:859370894177992704>  react on emotes to assign roles.\n<:aa_dash:859370894283505664>  react again to remove roles.\n  ୨୧ －－－－－－－－－ ꒷꒦")

    #     emoji_role = ['860075723501994004;933777267149119611','860069154291843082;933777267249803384','860069184084115476;933777267325300856','860069205772337172;933777267442733076','860069252526506004;933777267245580348','926512578732105768;933777267228807259','860069771679891457;933777267379798056','860069691271020564;933777267342073886','926512582083362856;933777267505627136','860069256904572928;933777266989748255','926741228010229820;933777267279163443','926741417366269952;933777267396575342','926512582553120769;933777267488854066']

    #     blank = '<:blank:926496177418043392>'
    #     embed1 = discord.Embed(color=0xffffff)
    #     embed1.title=f' {blank} <:bubblegumheartu:903339950353813595> <:blueberryheartu:903339950337032212> **C o l o r s** <a:dp_heart2:926492924831756319>'
    #     embed1.description = '<a:dp_arrowright:926495510372683796> Choose your favourite color!\n'
    #     embed1.description += f'{blank} ﹒﹒﹒﹒ <:chocolateheartu:903339950223806526> ﹒﹒﹒﹒\n'
        
    #     for x in emoji_role:
    #         emorole = x.split(";")
    #         embed1.description += f'{blank} {self.bot.get_emoji(int(emorole[1]))} <@&{emorole[0]}>\n'

    #     embed1.description += f'{blank} ﹒﹒﹒﹒ <:chocolateheartu:903339950223806526> ﹒﹒﹒﹒\n'
    #     # embed1.set_image(url='https://i.imgur.com/hrD5f9N.png')

    #     msg = await ctx.send(embed=embed1, allowed_mentions=discord.AllowedMentions.none())
    #     print(msg.id)

    #     for x in emoji_role:
    #         emoji = x.split(";")
    #         get_emoji = self.bot.get_emoji(int(emoji[1]))
    #         await msg.add_reaction(get_emoji)

    # @commands.command(help="Happy new year 2022")
    # @commands.guild_only()
    # @is_latte_guild()
    # async def happynewyear(self, ctx):
    #     embed = discord.Embed(color=0xbab6fd)
    #     embed.description = "┏━━┓┏━━┓┏━━┓   ┃┃\n┗━┓┃┃┏┓┃┗━┓┃   ┗┛\n┏━┛┃┃┃┃┃┏━┛┃ ┏━━┓\n┃┏━┛┃┃┃┃┃┏━┛ ┗━┓┃ \n┃┗━┓┃┗┛┃┃┗━┓ ┏━┛┃\n┗━━┛┗━━┛┗━━┛ ┃┏━┛"
        
    #     spacial_role = self.bot.latte.get_role(926471814757113946)
    #     role2021 = self.bot.latte.get_role(926470373573271583)

    #     # guild_member = ctx.guild.members
    #     # for member in guild_member:
    #     #     try:
    #     #         await member.add_roles(spacial_role, role2021)
    #     #     except:
    #     #         pass
        
    #     chat_channel = self.bot.latte.get_channel(861883647070437386)
    #     await chat_channel.send(content='<a:purplestar:902673752976941066> **Happy New Year 2022** <a:purplestar:902673752976941066>', embed=embed, allowed_mentions=discord.AllowedMentions.none())

    # @commands.command(help="Happy new year 2022")
    # @commands.guild_only()
    # @is_latte_guild()
    # async def member_2021(self, ctx):
    #     embed=discord.Embed(color=0xbab6fd)
    #     role2021 = self.bot.latte.get_role(926470373573271583)
    #     embed.description = f'{role2021.mention}'
    #     chat_channel = self.bot.latte.get_channel(861883647070437386)
    #     await chat_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(No_slash(bot))