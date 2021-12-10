# Standard
import discord
import random
from discord.ext import commands
from typing import List

ALL_AGENT = ['Jett','Phoenix','Raze','Reyna','Yoru', 'Astra','Brimston','Omen','Viper', 'Breach','KAY/O','Skye','Sova','Chamber','Cypher','Killjoy','Sage']
DUELIST = ['Jett','Phoenix','Raze','Reyna','Yoru']
CONTROLLER = ['Astra','Brimston','Omen','Viper']
INITIATOR = ['Breach','KAY/O','Skye','Sova']
SENTINEL = ['Chamber','Cypher','Killjoy','Sage']
MALEE = ['Melee']
SIDEARM = ['Classic', 'Shorty', 'Frenzy', 'Ghost', 'Sheriff']
SMGS = ['Stinger', 'Spectre']
SHOTGUN = ['Bucky', 'Judge']
RIFLES = ['Bulldog', 'Guardian', 'Phantom', 'Vandal']
SNIPER = ['Marshal', 'Operator']
MACHINE = ['Ares', 'Odin']
MAP = ['Ascent', 'Bind','Breeze','Fracture','Haven','Icebox','Split']

AGENT_TYPES = {
    'Jett': 'Duelist',
    'Phoenix': 'Duelist',
    'Raze': 'Duelist',
    'Reyna': 'Duelist',
    'Yoru': 'Duelist',
    'Astra': 'Controller',
    'Brimston': 'Controller',
    'Omen': 'Controller',
    'Viper': 'Controller',
    'Breach': 'Initiator',
    'KAY/O': 'Initiator',
    'Skye': 'Initiator',
    'Sova': 'Initiator',
    'Chamber': 'Sentinel',
    'Cypher': 'Sentinel',
    'Killjoy': 'Sentinel',
    'Sage': 'Sentinel',
}

WEAPON_TYPES = {
  'Melee': 'Melee',
  'Classic': 'Sidearms',
  'Shorty': 'Sidearms',
  'Frenzy': 'Sidearms',
  'Ghost': 'Sidearms',
  'Sheriff': 'Sidearms',
  'Stinger': 'SMGs',
  'Spectre': 'SMGs',
  'Bucky': 'Shotguns',
  'Judge': 'Shotguns',
  'Bulldog': 'Rifles',
  'Guardian': 'Rifles',
  'Phantom': 'Rifles',
  'Vandal': 'Rifles',
  'Marshal': 'Sniper Rifles',
  'Operator': 'Sniper Rifles',
  'Ares': 'Machine Guns',
  'Odin': 'Machine Guns',
}

AGENT_ICON = {
  'Jett': 'https://static.wikia.nocookie.net/valorant/images/3/35/Jett_icon.png',
  'Phoenix': 'https://static.wikia.nocookie.net/valorant/images/1/14/Phoenix_icon.png',
  'Raze': 'https://static.wikia.nocookie.net/valorant/images/9/9c/Raze_icon.png',
  'Reyna': 'https://static.wikia.nocookie.net/valorant/images/b/b0/Reyna_icon.png',
  'Yoru': 'https://static.wikia.nocookie.net/valorant/images/d/d4/Yoru_icon.png',
  'Astra': 'https://static.wikia.nocookie.net/valorant/images/0/08/Astra_icon.png',
  'Brimston': 'https://static.wikia.nocookie.net/valorant/images/4/4d/Brimstone_icon.png',
  'Omen': 'https://static.wikia.nocookie.net/valorant/images/b/b0/Omen_icon.png',
  'Viper': 'https://static.wikia.nocookie.net/valorant/images/5/5f/Viper_icon.png',
  'Breach': 'https://static.wikia.nocookie.net/valorant/images/5/53/Breach_icon.png',
  'KAY/O': 'https://static.wikia.nocookie.net/valorant/images/f/f0/KAYO_icon.png',
  'Skye': 'https://static.wikia.nocookie.net/valorant/images/3/33/Skye_icon.png',
  'Sova': 'https://static.wikia.nocookie.net/valorant/images/4/49/Sova_icon.png',
  'Chamber': 'https://static.wikia.nocookie.net/valorant/images/0/09/Chamber_icon.png',
  'Cypher': 'https://static.wikia.nocookie.net/valorant/images/8/88/Cypher_icon.png',
  'Killjoy': 'https://static.wikia.nocookie.net/valorant/images/1/15/Killjoy_icon.png',
  'Sage': 'https://static.wikia.nocookie.net/valorant/images/7/74/Sage_icon.png',
}

WEAPON_ICON = {
  'Melee': 'https://static.wikia.nocookie.net/valorant/images/0/0c/Knife_icon.png',
  'Classic': 'https://static.wikia.nocookie.net/valorant/images/d/d8/Classic_killfeed.png',
  'Shorty': 'https://static.wikia.nocookie.net/valorant/images/5/59/Shorty_icon.png',
  'Frenzy': 'https://static.wikia.nocookie.net/valorant/images/0/0b/Frenzy_icon.png',
  'Ghost': 'https://static.wikia.nocookie.net/valorant/images/8/82/Ghost_icon.png',
  'Sheriff': 'https://static.wikia.nocookie.net/valorant/images/b/b4/Sheriff_icon.png',
  'Stinger': 'https://static.wikia.nocookie.net/valorant/images/c/c7/Stinger_icon.png',
  'Spectre': 'https://static.wikia.nocookie.net/valorant/images/f/ff/Spectre_icon.png',
  'Bucky': 'https://static.wikia.nocookie.net/valorant/images/b/b0/Bucky_icon.png',
  'Judge': 'https://static.wikia.nocookie.net/valorant/images/4/43/Judge_icon.png',
  'Bulldog': 'https://static.wikia.nocookie.net/valorant/images/6/61/Bulldog_icon.png',
  'Guardian': 'https://static.wikia.nocookie.net/valorant/images/c/cc/Guardian_icon.png',
  'Phantom': 'https://static.wikia.nocookie.net/valorant/images/f/f8/Phantom_icon.png',
  'Vandal': 'https://static.wikia.nocookie.net/valorant/images/b/b4/Vandal_icon.png',
  'Marshal': 'https://static.wikia.nocookie.net/valorant/images/f/f9/Marshal_icon.png',
  'Operator': 'https://static.wikia.nocookie.net/valorant/images/1/17/Operator_icon.png',
  'Ares': 'https://static.wikia.nocookie.net/valorant/images/2/2f/Ares_icon.png',
  'Odin': 'https://static.wikia.nocookie.net/valorant/images/3/35/Odin_icon.png',
}

MAP_ICON = {
  'Ascent':'https://static.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png',
  'Bind':'https://static.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png',
  'Breeze':'https://static.wikia.nocookie.net/valorant/images/1/10/Loading_Screen_Breeze.png',
  'Fracture':'https://static.wikia.nocookie.net/valorant/images/f/fc/Loading_Screen_Fracture.png',
  'Haven':'https://static.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png',
  'Icebox':'https://static.wikia.nocookie.net/valorant/images/1/13/Loading_Screen_Icebox.png',
  'Split':'https://static.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png',
}

ICON = 'https://cdn.discordapp.com/attachments/417245049315655690/902173852401025074/valorant.jpg'

AGENT_LIST = {
    'Duelist': 'Jett, Phoenix, Raze, Reyna, Yoru',
    'Controller': 'Astra, Brimston, Omen, Viper',
    'Initiator': 'Breach, KAY/O, Skye, Sova',
    'Sentinel': 'Chamber, Cypher, Killjoy, Sage',
}

WEAPON_LIST = {
    'Melee': 'Melee',
    'Sidearms': 'Classic, Shorty, Frenzy, Ghost, Sheriff',
    'SMGs': 'Stinger, Spectre',
    'Shotguns': 'Bucky, Judge',
    'Rifles': 'Bulldog, Guardian, Phantom, Vandal',
    'Sniper Rifles': 'Marshal, Operator',
    'Machine Guns': 'Ares, Odin'
}

def toggle_emoji(name):
  emoji_name = {
    "True" : "<:Toggle_ON:915251919348436993>",
    "False" : "<:Toggle_OFF:915251895063425044>",
  }
  return emoji_name.get(name)

# Local
# from utils.values import MAP, WEAPON_TYPE, AGENT_TYPE, ICON, toggle_emoji, AGENT_ICON , AGENT_Duelist, AGENT_Controller, AGENT_Initiator, AGENT_Sentinel, AGENT_TYPES, ALL_AGENT, MALEE, SIDEARM, SMGS, SHOTGUN, RIFLES, SNIPER, MACHINE, WEAPON_TYPES, WEAPON_ICON, MAP_ICON

class ValorantLog(discord.ui.View):
    def __init__(self, log, owner):
        super().__init__()
        self.log = log
        self.owner = owner
        self.current_page = 0

    def build_embeds(self) -> List[discord.Embed]:
        embeds = []
        embed = discord.Embed(color=0xffffff)
        for x, y in zip(self.log, self.owner):
            embed.add_field(name=x, value=y, inline=False)
            if len(embed.fields) == 5:
                embeds.append(embed)
                embed = discord.Embed(color=0xffffff)
        if len(embed.fields) > 0:
            embeds.append(embed)
        return embeds
    
    @discord.ui.button(label='≪', style=discord.ButtonStyle.blurple)
    async def go_to_first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = 0
        self._update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Back")
    async def previous(self, _, interaction: discord.Interaction):
        self.current_page -= 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Next")
    async def next(self, _, interaction: discord.Interaction):
        self.current_page += 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label='≫', style=discord.ButtonStyle.blurple)
    async def go_to_last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        last = len(self.embeds) - 1
        self.current_page = last
        self._update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    def _update_buttons(self):
        styles = {True: discord.ButtonStyle.gray, False: discord.ButtonStyle.blurple}
        page = self.current_page
        total = len(self.embeds) - 1
        self.next.disabled = page == total
        self.previous.disabled = page == 0
        self.go_to_first_page.disabled = page == 0
        self.go_to_last_page.disabled = page == total
        self.next.style = styles[page == total]
        self.go_to_last_page.style = styles[page == total]
        self.previous.style = styles[page == 0]
        self.go_to_first_page.style = styles[page == 0]
    
    async def on_timeout(self) -> None:
        self.clear_items()
        self.add_item(self.category_select)
        self.category_select.placeholder = "Timeout."
        self.category_select.disabled = True
        await self.message.edit(view=self)

    async def start(self, interaction: discord.Interaction):
        self.embeds = self.build_embeds()
        self._update_buttons()
        await interaction.response.send_message(embed=self.embeds[0], ephemeral=True, view=self)

class AgentView(discord.ui.View):
    def __init__(self, ctx: commands.context, other_view: discord.ui.View):
        super().__init__()
        self.embed: discord.Embed = None
        self.ctx = ctx
        self.bot = ctx.bot
        self.other_view = other_view
        self.category_select: discord.ui.Select
        self.category_select.options = []
        self.duelist:bool = True
        self.controller:bool = True
        self.initiator:bool = True
        self.sentinel:bool = True
        self.agent_embed = self.build_agent_page()
        self.send_agent = None
        self.send_shuffle = None
        self.log = []
        self.owner_log = []
        self.count = 0
    
    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red, row=1)
    async def go_back(self, button:discord.Button, interaction: discord.Interaction):
        if self.send_agent:
            await self.send_agent.delete()
        if self.send_shuffle:
            await self.send_shuffle.delete()
        await interaction.response.edit_message(embed=self.embed, view=self.other_view)
        self.stop()

    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple)
    async def random_agent(self, button, interaction):
        List_random = (DUELIST if self.duelist else []) + (CONTROLLER if self.controller else []) + (INITIATOR if self.initiator else []) + (SENTINEL if self.sentinel else [])
        agent = random.choice(List_random)
        embed = self.build_embed(agent, AGENT_TYPES[agent], interaction)
        self.count += 1
        if len(self.log) <= 100:
            self.log.append(f'{self.count}. {agent}')
            self.owner_log.append(f'{interaction.user.display_name}')
        if len(self.log) > 0:
            self.log_button.disabled = False
            await interaction.response.edit_message(view=self)
        if not self.send_agent:
            self.send_agent = await self.ctx.send(embed=embed)
            return
        await self.send_agent.edit(embed=embed)
    
    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.blurple)
    async def shuffle_agent(self, button, interaction):
        embed = discord.Embed(description='',color=0xfa4454)
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')
        random.shuffle(ALL_AGENT)
        i = 0
        for x in ALL_AGENT:
            i+= 1
            embed.description += f"{i}. {x}\n"
        if not self.send_shuffle:
            self.send_shuffle = await self.ctx.send(embed=embed)
            return
        await self.send_shuffle.edit(embed=embed)

    @discord.ui.button(label="Log", style=discord.ButtonStyle.gray)
    async def log_button(self, button, interaction):
        if self.log:
            view = ValorantLog(log=self.log, owner=self.owner_log)
            await view.start(interaction)
        
    @discord.ui.select(placeholder="Toggle Agent type", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if not (getattr(self, f'{select.values[0]}', None)):
            setattr(self, f'{select.values[0]}', True)
        else:
            setattr(self, f'{select.values[0]}', False)
        new_embed = self.build_agent_page()
        await interaction.response.edit_message(embed=new_embed, view=self)
          
    def build_agent_page(self) -> discord.Embed:
        embed = discord.Embed(color=0xfa4454)
        embed.title = "Valorant Agent"
        embed.set_thumbnail(url=ICON)
        embed.description = f'{toggle_emoji(str(self.duelist))} • **Duelist**\n'
        embed.description += f'{toggle_emoji(str(self.controller))} • **Controller**\n'
        embed.description += f'{toggle_emoji(str(self.initiator))} • **Initiator**\n'
        embed.description += f'{toggle_emoji(str(self.sentinel))} • **Sentinel**\n'
        return embed
    
    def build_embed(self, agent, agent_type, interaction) -> discord.Embed:
        embed = discord.Embed(title=f'{agent}', description=f'{agent_type}', color=0xfa4454)
        embed.set_thumbnail(url=AGENT_ICON[agent])
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')
        return embed

    async def start(self, interaction: discord.Interaction):
        for x in AGENT_LIST:
            self.category_select.add_option(label=x, value=x.lower(), description=AGENT_LIST[x])
        self.embed = interaction.message.embeds[0]
        self.log_button.disabled = True
        await interaction.response.edit_message(embed=self.agent_embed, view=self)

    async def on_timeout(self) -> None:
        await self.other_view.on_timeout()
        self.other_view.stop()

class WeaponView(discord.ui.View):
    def __init__(self, ctx: commands.context, other_view: discord.ui.View):
        super().__init__()
        self.embed: discord.Embed = None
        self.ctx = ctx
        self.bot = ctx.bot
        self.other_view = other_view
        self.category_select: discord.ui.Select
        self.category_select.options = []
        self.sidearms:bool = True
        self.smgs:bool = True
        self.shotguns:bool = True
        self.rifles:bool = True
        self.sniperrifles:bool = True
        self.machineguns:bool = True
        self.melee:bool = True
        self.weapon_embed = self.build_page()
        self.count = 0
        self.log = []
        self.owner_log = []
        self.send_embed = None
    
    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red, row=1)
    async def go_back(self, button:discord.Button, interaction: discord.Interaction):
        if self.send_embed:
            await self.send_embed.delete()
        await interaction.response.edit_message(embed=self.embed, view=self.other_view)
        self.stop()
        
    @discord.ui.select(placeholder="Select a category...", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if not (getattr(self, f'{select.values[0]}', None)):
            setattr(self, f'{select.values[0]}', True)
        else:
            setattr(self, f'{select.values[0]}', False)
        embed = self.build_page()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple)
    async def random_button(self, button, interaction):
        List_random = (MALEE if self.melee else []) + (SIDEARM if self.sidearms else []) + (SMGS if self.smgs else []) + (SHOTGUN if self.shotguns else []) + (RIFLES if self.rifles else []) + (SNIPER if self.sniperrifles else []) + (MACHINE if self.machineguns else [])
        finish = random.choice(List_random)
        embed = self.build_embed(finish, WEAPON_TYPES[finish], interaction)
        self.count += 1
        if len(self.log) <= 100:
            self.log.append(f'{self.count}. {finish}')
            self.owner_log.append(f'{interaction.user.display_name}')
        if len(self.log) > 0:
            self.log_button.disabled = False
            await interaction.response.edit_message(view=self)
        if not self.send_embed:
            self.send_embed = await self.ctx.send(embed=embed)
            return
        await self.send_embed.edit(embed=embed)
    
    @discord.ui.button(label="Log", style=discord.ButtonStyle.gray)
    async def log_button(self, button, interaction):
        if self.log:
            view = ValorantLog(log=self.log, owner=self.owner_log)
            await view.start(interaction)
    
    def build_page(self) -> discord.Embed:
        embed = discord.Embed(color=0xfa4454)
        embed.title = "Valorant Weapon"
        embed.set_thumbnail(url=ICON)
        embed.description = f'{toggle_emoji(str(self.melee))} • **Melee**\n'
        embed.description += f'{toggle_emoji(str(self.sidearms))} • **Sidearms**\n'
        embed.description += f'{toggle_emoji(str(self.smgs))} • **SMGs**\n'
        embed.description += f'{toggle_emoji(str(self.shotguns))} • **Shotguns**\n'
        embed.description += f'{toggle_emoji(str(self.rifles))} • **Rifles**\n'
        embed.description += f'{toggle_emoji(str(self.sniperrifles))} • **Sniper rifles**\n'
        embed.description += f'{toggle_emoji(str(self.machineguns))} • **Machine guns**\n'
        return embed
    
    def build_embed(self, key, value, interaction) -> discord.Embed:
        data = WEAPON_ICON
        embed = discord.Embed(title=f'{key}', description=f'{value}', color=0xfa4454)
        embed.set_thumbnail(url=data[key])
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')
        return embed

    async def start(self, interaction: discord.Interaction):
        for x in WEAPON_LIST.keys():
            self.category_select.add_option(label=x, value=x.replace(" ", "").lower(), description=WEAPON_LIST[x])
        self.embed = interaction.message.embeds[0]
        self.log_button.disabled = True
        await interaction.response.edit_message(embed=self.weapon_embed, view=self)

    async def on_timeout(self) -> None:
        await self.other_view.on_timeout()
        self.other_view.stop()

class MapView(discord.ui.View):
    def __init__(self, ctx: commands.context, other_view: discord.ui.View):
        super().__init__()
        self.embed: discord.Embed = None
        self.ctx = ctx
        self.bot = ctx.bot
        self.other_view = other_view
        self.category_select: discord.ui.Select
        self.category_select.options = []
        # self.category_select.max_values = len(MAP) + 1
        self.ascent:bool = True
        self.bind:bool = True
        self.breeze:bool = True
        self.fracture:bool = True
        self.haven:bool = True
        self.icebox:bool = True
        self.split:bool = True
        self.weapon_embed = self.build_page()
        self.count = 0
        self.send_embed = None
        self.send_shuffle = None
        self.atkordef = None
        self.log = []
        self.owner_log = []

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red, row=1)
    async def go_back(self, button:discord.Button, interaction: discord.Interaction):
        if self.send_embed:
            await self.send_embed.delete()
        if self.send_shuffle:
            await self.send_shuffle.delete()
        await interaction.response.edit_message(embed=self.embed, view=self.other_view)
        self.stop()
        
    @discord.ui.select(placeholder="Select a category...", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if not (getattr(self, f'{select.values[0]}', None)):
            setattr(self, f'{select.values[0]}', True)
        else:
            setattr(self, f'{select.values[0]}', False)
        embed = self.build_page()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple)
    async def random_button(self, button, interaction):        
        List_random = (['Ascent'] if self.ascent else []) + (['Bind'] if self.bind else []) + (['Breeze'] if self.breeze else []) + (['Fracture'] if self.fracture else []) + (['Haven'] if self.haven else []) + (['Icebox'] if self.icebox else []) + (['Split'] if self.split else []) 
        finish = random.choice(List_random)
        embed = self.build_embed(finish, interaction)
        self.count += 1
        if len(self.log) <= 100:
            self.log.append(f'{self.count}. {finish}')
            self.owner_log.append(f'{interaction.user.display_name}')
        if len(self.log) > 0:
            self.log_button.disabled = False
            await interaction.response.edit_message(view=self)
        if not self.send_embed:
            self.send_embed = await self.ctx.send(embed=embed)
            return
        await self.send_embed.edit(embed=embed)
    
    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.blurple)
    async def shuffle_agent(self, button, interaction):
        embed = discord.Embed(description='',color=0xfa4454)
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')
        
        random.shuffle(MAP)
        i = 0
        for x in MAP:
            i+= 1
            embed.description += f"{i}. {x}\n"
        if not self.send_shuffle:
            self.send_shuffle = await self.ctx.send(embed=embed)
            return
        await self.send_shuffle.edit(embed=embed)
    
    @discord.ui.button(label="attacker or defending", style=discord.ButtonStyle.blurple)
    async def atk_or_def_button(self, button, interaction):
        embed = discord.Embed()
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')

        def get_color(key):
            color = 0x66c2a9
            if key == 'Attacker':
                color = 0xf05c57
            return color
        
        atk_or_def = ['Attacker','Defending']
        atk_def = random.choice(atk_or_def)
        embed.color = get_color(atk_def)
        embed.description = f'**{atk_def}**'
        if not self.atkordef:
            self.atkordef = await self.ctx.send(embed=embed)
            return
        await self.atkordef.edit(embed=embed)
    
    @discord.ui.button(label="Log", style=discord.ButtonStyle.gray)
    async def log_button(self, button, interaction):
        if self.log:
            view = ValorantLog(log=self.log, owner=self.owner_log)
            await view.start(interaction)
    
    def build_embed(self, key, interaction) -> discord.Embed:
        data = MAP_ICON
        embed = discord.Embed(title=f'{key}', color=0xfa4454)
        embed.set_thumbnail(url=data[key])
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Requested by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Requested by by {interaction.user.display_name}')
        return embed
    
    def build_page(self) -> discord.Embed:
        embed = discord.Embed(color=0xfa4454)
        embed.title = "Valorant Map"
        embed.set_thumbnail(url=ICON)
        embed.description = f'{toggle_emoji(str(self.ascent))} • **Ascent**\n'
        embed.description += f'{toggle_emoji(str(self.bind))} • **Bind**\n'
        embed.description += f'{toggle_emoji(str(self.breeze))} • **Breeze**\n'
        embed.description += f'{toggle_emoji(str(self.fracture))} • **Fracture**\n'
        embed.description += f'{toggle_emoji(str(self.haven))} • **Haven**\n'
        embed.description += f'{toggle_emoji(str(self.icebox))} • **Icebox**\n'
        embed.description += f'{toggle_emoji(str(self.split))} • **Split**\n'
        return embed
    
    async def start(self, interaction: discord.Interaction):
        for x in MAP:
            self.category_select.add_option(label=x, value=x.lower())
        self.embed = interaction.message.embeds[0]
        self.log_button.disabled = True
        await interaction.response.edit_message(embed=self.weapon_embed, view=self)

    async def on_timeout(self) -> None:
        await self.other_view.on_timeout()
        self.other_view.stop()

class ValorantView(discord.ui.View):
    def __init__(self, ctx: commands.context):
        super().__init__()
        self.ctx = ctx
        self.bot = ctx.bot
        self.category_select: discord.ui.Select
        self.category_select.options = []
        self.main_embed = self.build_main_page()
                
    @discord.ui.select(placeholder="Select a category", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == "agent":
            view = AgentView(self.ctx, self)
            await view.start(interaction)
        elif select.values[0] == "weapon":
            view = WeaponView(self.ctx, self)
            await view.start(interaction)
        elif select.values[0] == "map":
            view = MapView(self.ctx, self)
            await view.start(interaction)
            
    def build_select(self) -> None:
        self.category_select.add_option(label='Agent', value='agent', emoji='<:jetthappy:914210940084424744>')
        self.category_select.add_option(label='Weapon', value='weapon', emoji='<:weapon:914212537531248720>')
        self.category_select.add_option(label='Map', value='map', emoji='<:map2:914213385984421968>')
            
    def build_main_page(self) -> discord.Embed:
        embed = discord.Embed(color=0xfa4454)
        embed.title = "Valorant Random"
        embed.description = "Click **Button** for choose type random."
        embed.add_field(name=f'\u200B', value=f'• **Agent**', inline=True)
        embed.add_field(name=f'\u200B', value=f'• **Weapon**', inline=True)
        embed.add_field(name=f'\u200B', value=f'• **Map**' , inline=True)
        embed.set_thumbnail(url=ICON)
        return embed
            
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user == self.ctx.author:
            return True
        await interaction.response.defer()
        return False

    async def on_timeout(self) -> None:
        self.clear_items()
        self.add_item(self.category_select)
        self.category_select.placeholder = "Timeout."
        self.category_select.disabled = True
        await self.message.edit(view=self)

    async def start(self):
        self.build_select()
        self.message = await self.ctx.send(embed=self.main_embed, view=self)