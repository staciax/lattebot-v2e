# Standard 
import discord
from discord.ext import commands

# Third party
# Local

class Reaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.latte_verify = 861849112386469908
        self.latte_color = 861212646057443338
        self.matcha_verify = 873042881189920809
        self.matcha_color = 878847610616700928

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = payload.member
        guild = member.guild
        emoji = str(payload.emoji.id)
        # chat_channel = guild.get_channel(861883647070437386)
        
        #latte_color
        if self.latte_color == payload.message_id:

            if emoji == '861130565804621835':
                role = discord.utils.get(guild.roles, id = 860075723501994004)
            if emoji == '861128977828806686':
                role = discord.utils.get(guild.roles, id = 860069154291843082)
            if emoji == '861128979418447942':
                role = discord.utils.get(guild.roles, id = 860069184084115476)
            if emoji == '861128977410293761':
                role = discord.utils.get(guild.roles, id = 860069205772337172)
            if emoji == '861128978902024192':
                role = discord.utils.get(guild.roles, id = 860069252526506004)
            if emoji == '861128979309133844':
                role = discord.utils.get(guild.roles, id = 860069771679891457)
            if emoji == '861128977603231765':
                role = discord.utils.get(guild.roles, id = 860069691271020564)
            if emoji == '861128979313328128':
                role = discord.utils.get(guild.roles, id = 860069256904572928)

            # color_main = discord.utils.get(guild.roles, id = 854506876674244608) #name="・ ──────꒰ ・ colors ・ ꒱────── ・")

            await member.add_roles(role)
        
        #latte_verify
        if self.latte_verify == payload.message_id:
            if emoji == '861800747293212672':    
                role = discord.utils.get(guild.roles, id = 842309176104976387) #name="Latte・・ ♡")
                role2 = discord.utils.get(guild.roles, id = 854503426977038338) #name="・ ───────꒰ ・ ♡ ・ ꒱─────── ・")
                role3 = discord.utils.get(guild.roles, id = 854503041775566879) #name="・ ──────꒰ ・ levels ・ ꒱────── ・")

            self.bot.new_members[str(member.id)] = True
            await member.add_roles(role , role2 , role3)

        """ MATCHA SERVER """
        if self.matcha_color == payload.message_id:
            emoji = str(payload.emoji.name)
            if emoji == '🍓':
                role = discord.utils.get(guild.roles, id=837729400241520640)
            elif emoji == '🍊':
                role = discord.utils.get(guild.roles, id=837729404548284487)
            elif emoji == '🍌':
                role = discord.utils.get(guild.roles, id=837729407643811861)
            elif emoji == '🍏':
                role = discord.utils.get(guild.roles, id=837729411272540211)
            elif emoji == '🖤':
                role = discord.utils.get(guild.roles, id=837729413259984906)
            elif emoji == '🥶':
                role = discord.utils.get(guild.roles, id=837729413826347120)
            elif emoji == '🍇':
                role = discord.utils.get(guild.roles, id=837729414099894273)
            elif emoji == '☁️':
                role = discord.utils.get(guild.roles, id=837729506226864180)
            elif emoji == '🌺':
                role = discord.utils.get(guild.roles, id=837729508378935326)
            elif emoji == '🌸':
                role = discord.utils.get(guild.roles, id=854262148062511135)
            elif emoji == '🌊':
                role = discord.utils.get(guild.roles, id=854261956408246323)
            elif emoji == '🥤':
                role = discord.utils.get(guild.roles, id=854316816805527553) 

            await member.add_roles(role)

        if self.matcha_color == payload.message_id:
            if emoji == '873028548724670555':
                role = discord.utils.get(guild.roles, id = 735500646882607156) #name="♡ ~ 𝙈𝘼𝙄𝘿𝙀𝙉 ~♡")
            if emoji == '873029782592446464':
                role = discord.utils.get(guild.roles, id = 858186876494151716) # name="✭ : 𝘽𝙐𝙏𝙇𝙀𝙍 : ✭")

            await member.add_roles(role)
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await(self.bot.fetch_guild(payload.guild_id))
        emoji = str(payload.emoji.id)
        member = await(guild.fetch_member(payload.user_id))

        #latte_color
        if self.latte_color == payload.message_id:

            if emoji == '861130565804621835':
                role = discord.utils.get(guild.roles, id = 860075723501994004)
            if emoji == '861128977828806686':
                role = discord.utils.get(guild.roles, id = 860069154291843082)
            if emoji == '861128979418447942':
                role = discord.utils.get(guild.roles, id = 860069184084115476)
            if emoji == '861128977410293761':
                role = discord.utils.get(guild.roles, id = 860069205772337172)
            if emoji == '861128978902024192':
                role = discord.utils.get(guild.roles, id = 860069252526506004)
            if emoji == '861128979309133844':
                role = discord.utils.get(guild.roles, id = 860069771679891457)
            if emoji == '861128977603231765':
                role = discord.utils.get(guild.roles, id = 860069691271020564)
            if emoji == '861128979313328128':
                role = discord.utils.get(guild.roles, id = 860069256904572928)

        #            role_lvl = discord.utils.get(guild.roles, id = 854506876674244608) #name="・ ──────꒰ ・ colors ・ ꒱────── ・")

            if member is not None:
                await member.remove_roles(role)# , role_lvl)
            else:
                print("Member Not Fount")

        #latte_verify
        if self.latte_verify == payload.message_id:
            if emoji == '861800747293212672':    
                role = discord.utils.get(guild.roles, id = 842309176104976387) #name="Latte・・ ♡")
                role2 = discord.utils.get(guild.roles, id = 854503426977038338) #name="・ ───────꒰ ・ ♡ ・ ꒱─────── ・")
                role3 = discord.utils.get(guild.roles, id = 854503041775566879) #name="・ ──────꒰ ・ levels ・ ꒱────── ・")
                
            if member is not None:
                await member.remove_roles(role , role2 , role3)
            else:
                print("Member Not Fount")

        """ MATCHA SERVER """

        if self.matcha_color == payload.message_id:
            emoji = str(payload.emoji.name)
            if emoji == '🍓':
                role = discord.utils.get(guild.roles, id=837729400241520640)
            elif emoji == '🍊':
                role = discord.utils.get(guild.roles, id=837729404548284487)
            elif emoji == '🍌':
                role = discord.utils.get(guild.roles, id=837729407643811861)
            elif emoji == '🍏':
                role = discord.utils.get(guild.roles, id=837729411272540211)
            elif emoji == '🖤':
                role = discord.utils.get(guild.roles, id=837729413259984906)
            elif emoji == '🥶':
                role = discord.utils.get(guild.roles, id=837729413826347120)
            elif emoji == '🍇':
                role = discord.utils.get(guild.roles, id=837729414099894273)
            elif emoji == '☁️':
                role = discord.utils.get(guild.roles, id=837729506226864180)
            elif emoji == '🌺':
                role = discord.utils.get(guild.roles, id=837729508378935326)
            elif emoji == '🌸':
                role = discord.utils.get(guild.roles, id=854262148062511135)
            elif emoji == '🌊':
                role = discord.utils.get(guild.roles, id=854261956408246323)
            elif emoji == '🥤':
                role = discord.utils.get(guild.roles, id=854316816805527553) 

            if member is not None:
                await member.remove_roles(role)
            else:
                print("Member Not Fount")

        if self.matcha_verify == payload.message_id:
            if emoji == '873028548724670555':
                role = discord.utils.get(guild.roles, id = 735500646882607156) #name="♡ ~ 𝙈𝘼𝙄𝘿𝙀𝙉 ~♡")
            if emoji == '873029782592446464':
                role = discord.utils.get(guild.roles, id = 858186876494151716) # name="✭ : 𝘽𝙐𝙏𝙇𝙀𝙍 : ✭")

            if member is not None:
                await member.remove_roles(role)
            else:
                print("Member Not Fount")
        
def setup(bot):
    bot.add_cog(Reaction(bot))