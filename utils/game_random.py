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
        if self.atkordef:
            await self.atkordef.delete()
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
        embed.description = "Use **Selection** for choose type random."
        embed.add_field(name=f'\u200B', value=f'• <:jetthappy:914210940084424744> **Agent**', inline=True)
        embed.add_field(name=f'\u200B', value=f'• <:weapon:914212537531248720> **Weapon**', inline=True)
        embed.add_field(name=f'\u200B', value=f'• <:map2:914213385984421968> **Map**' , inline=True)
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

class APEX_RANDOM(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=1800)
        self.ctx = ctx
        self.weapon_type = None
        self.message = ''
        self.embeds_legend = None
        self.embeds_weapon = None
        self.logging = ''
        self.counts = 0

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    @discord.ui.select(custom_id="Select Weapon type", placeholder="Weapon type (default=random)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Random', value="random"),
        discord.SelectOption(label='Assault rifles', value="ar"),
        discord.SelectOption(label='Sub machine guns', value="sub"),
        discord.SelectOption(label='Light machine guns', value="light"),
        discord.SelectOption(label='Marksman weapons', value="marksman"),
        discord.SelectOption(label='Sniper rifles', value="sniper"),
        discord.SelectOption(label='Shotguns', value="shotgun"),
        discord.SelectOption(label='Pistols', value="pistol"),
    ])
    async def callback_a_k(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0] == 'random':
            self.weapon_type = None
        elif select.values[0]:
            self.weapon_type = f'{str(select.values[0])}'
    
    @discord.ui.button(label="Legend", style=discord.ButtonStyle.blurple)
    async def apex_legend(self, button, interaction):
        self.w_log.disabled = False
        await self.message.edit(view=self)
        
        embed = apex_random_legends()
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Req by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Req by {interaction.user.display_name}')
        a_logging = str(embed.description.split('**' )[1])
        if self.embeds_legend is None:
            self.embeds_legend = await self.ctx.channel.send(embed=embed)
            if self.counts > 100:
                return
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.display_name}: {a_logging}'
        else:
            await self.embeds_legend.edit(embed=embed)
            if self.counts > 100:
                return
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.display_name}: {a_logging}'
    
    @discord.ui.button(label="Weapon", style=discord.ButtonStyle.blurple)
    async def apex_weapon(self, button, interaction):
        self.w_log.disabled = False
        await self.message.edit(view=self)
        embed = apex_random_weapon(category=self.weapon_type)

        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Req by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Req by {interaction.user.display_name}')
        a_logging = str(embed.description.split('**' )[1])
        if self.embeds_weapon is None:
            self.embeds_weapon = await self.ctx.channel.send(embed=embed)
            if self.counts > 100:
                return
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.name}: {a_logging}'
        else:
            await self.embeds_weapon.edit(embed=embed)
            if self.counts > 100:
                return
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.name}: {a_logging}'
    
    @discord.ui.button(label="Log", style=discord.ButtonStyle.gray)
    async def w_log(self, button, interaction):
        embed = discord.Embed(color=0xffffff)
        embed.description = ''
        weapon_log_list = []

        data = self.logging
        if data:
            await interaction.response.send_message(self.logging, ephemeral=True)
    
    async def start(self):
        self.w_log.disabled = True
        embed = discord.Embed(title="Apex Legend")
        embed.description = '`apex legend random`\n`-legend`\n`-weapon`'
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/417245049315655690/902169368744566784/apex-legends.png')
        embed.color = 0xFFA500
        if embed:
            self.message = await self.ctx.send(embed=embed, view=self, mention_author=False)

def apex_random_weapon(category):
    #embed
    embed = discord.Embed(color=0xFFA500)

    #list_of_weapon
    Assault_rifles = ["HAVOC Rifle", "VK-47 Flatline", "Hemlok Burst AR" , "R-301 Carbine"]
    Submachine_guns = ["Alternator SMG","Prowler Burst PDW","R-99 SMG","Volt SMG","C.A.R. SMG"]
    Light_machine_guns = ["Devotion LMG" , "L-STAR EMG", "M600 Spitfire" , "Rampage"]
    Marksman_weapons = ["G7 Scout", "Triple Take", "30-30 Repeater", "Bocek Compound Bow"]
    Sniper_rifles = ["Charge Rifle", "Longbow DMR", "Kraber .50-Cal Sniper", "Sentinel"]
    Shotguns = ["EVA-8 Auto", "Mastiff Shotgun", "Mozambique Shotgun", "Peacekeeper"]
    Pistols = ["RE-45 Auto","P2020","Wingman"]
    all_weapon = ["HAVOC Rifle", "VK-47 Flatline", "Hemlok Burst AR" , "R-301 Carbine","Alternator SMG","Prowler Burst PDW","R-99 SMG","Volt SMG","C.A.R. SMG","Devotion LMG" , "L-STAR EMG", "M600 Spitfire" , "Rampage","G7 Scout", "Triple Take", "30-30 Repeater", "Bocek Compound Bow","Charge Rifle", "Longbow DMR", "Kraber .50-Cal Sniper", "Sentinel","EVA-8 Auto", "Mastiff Shotgun", "Mozambique Shotgun", "Peacekeeper","RE-45 Auto","P2020","Wingman"]

    #category
    if category == None:
        random_gun = random.choice(all_weapon)
    elif category == "ar":
        random_gun = random.choice(Assault_rifles)
    elif category == "sub":
        random_gun = random.choice(Submachine_guns)
    elif category == "light":
        random_gun = random.choice(Light_machine_guns)
    elif category == "marksman":
        random_gun = random.choice(Marksman_weapons)
    elif category == "sniper":
        random_gun = random.choice(Sniper_rifles)
    elif category == "shotgun":
        random_gun = random.choice(Shotguns)
    elif category == "pistol":
        random_gun = random.choice(Pistols)
    
    #picture_of_gun
    if random_gun == "HAVOC Rifle":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/ec/HAVOC_Rifle.png/revision/latest/scale-to-width-down/1000?cb=20190304144136")
    elif random_gun == "VK-47 Flatline":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f1/VK-47_Flatline.png/revision/latest/scale-to-width-down/1000?cb=20190304143943")
    elif random_gun == "Hemlok Burst AR":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/7/74/Hemlok_Burst_AR.png/revision/latest/scale-to-width-down/1000?cb=20190304144048")
    elif random_gun == "R-301 Carbine":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f1/R-301_Carbine.png/revision/latest/scale-to-width-down/1000?cb=20190304143302")
    elif random_gun == "Alternator SMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/e9/Alternator_SMG.png/revision/latest/scale-to-width-down/688?cb=20190304180240")
    elif random_gun == "Prowler Burst PDW":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/b/bf/Prowler_Burst_PDW.png/revision/latest/scale-to-width-down/996?cb=20190304180338")
    elif random_gun == "R-99 SMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/d/d5/R-99_SMG.png/revision/latest/scale-to-width-down/1000?cb=20190304180412")
    elif random_gun == "Volt SMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f5/Volt.png/revision/latest/scale-to-width-down/1000?cb=20210717062422")
    elif random_gun == "C.A.R. SMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/1/13/C.A.R._SMG.png/revision/latest/scale-to-width-down/1000?cb=20211018182120")
    elif random_gun == "Devotion LMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/8/8c/Devotion_LMG.png/revision/latest/scale-to-width-down/1000?cb=20190304180450")
    elif random_gun == "L-STAR EMG":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/0/01/L-STAR_EMG.png/revision/latest/scale-to-width-down/1000?cb=20190709153859")
    elif random_gun == "M600 Spitfire":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f2/M600_Spitfire.png/revision/latest/scale-to-width-down/1000?cb=20190304180514")
    elif random_gun == "Rampage":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/e4/Rampage.png/revision/latest/scale-to-width-down/1000?cb=20210807042402")
    elif random_gun == "G7 Scout":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/eb/G7_Scout.png/revision/latest/scale-to-width-down/1000?cb=20190304181016")
    elif random_gun == "Triple Take":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/d/d9/Triple_Take.png/revision/latest/scale-to-width-down/1000?cb=20210823030642")
    elif random_gun == "30-30 Repeater":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/8/86/30-30_Repeater.png/revision/latest/scale-to-width-down/1000?cb=20210710054145")
    elif random_gun == "Bocek Compound Bow":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/0/02/Bocek_Compound_Bow.png/revision/latest/scale-to-width-down/777?cb=20210710045232")
    elif random_gun == "Charge Rifle":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/2/2b/Charge_Rifle.png/revision/latest/scale-to-width-down/1000?cb=20210130154504")
    elif random_gun == "Longbow DMR":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/4/46/Longbow_DMR.png/revision/latest/scale-to-width-down/1000?cb=20190304181103")
    elif random_gun == "Kraber .50-Cal Sniper":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f5/Kraber_.50-Cal_Sniper.png/revision/latest/scale-to-width-down/1000?cb=20190304181037")
    elif random_gun == "Sentinel":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/9/91/Sentinel.png/revision/latest/scale-to-width-down/1000?cb=20210710095136")
    elif random_gun == "EVA-8 Auto":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/9/97/EVA-8_Auto.png/revision/latest/scale-to-width-down/1000?cb=20210817041450")
    elif random_gun == "Mastiff Shotgun":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/c/c9/Mastiff_Shotgun.png/revision/latest/scale-to-width-down/1000?cb=20210818084651")
    elif random_gun == "Mozambique Shotgun":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/a/ae/Mozambique_Shotgun.png/revision/latest/scale-to-width-down/1000?cb=20210813094328")
    elif random_gun == "Peacekeeper":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/6/64/Peacekeeper.png/revision/latest/scale-to-width-down/1000?cb=20210814095843")
    elif random_gun == "RE-45 Auto":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/2/25/RE-45_Auto.png/revision/latest/scale-to-width-down/1000?cb=20210816090119")
    elif random_gun == "P2020":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/c/c1/P2020.png/revision/latest/scale-to-width-down/1000?cb=20210815055000")
    elif random_gun == "Wingman":
        embed.set_image(url="https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/0/09/Wingman.png/revision/latest/scale-to-width-down/1000?cb=20210813090820")
    
    embed.description = f"**{random_gun}**"

    return embed

def apex_random_legends():
    #embed
    embed = discord.Embed(color=0xFFA500)

    #list_of_legends
    legends_list = ['Ash','Bangalore','Bloodhound','Caustic','Crypto','Fuse','Gibraltar','Horizon','Lifeline','Loba','Mirage','Octane','Pathfinder','Rampart','Revenant','Seer','Valkyrie','Wattson','Wraith']
    
    random_legends = random.choice(legends_list)

    #picture_of_agent
    if random_legends == "Ash":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/common/legends/ash/apex-grid-tile-legends-ash.png.adapt.crop16x9.png")
    elif random_legends == "Bangalore":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-bangalore.png.adapt.crop16x9.png")
    elif random_legends == "Bloodhound":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-bloodhound.png.adapt.crop16x9.png")
    elif random_legends == "Caustic":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-caustic.png.adapt.crop16x9.png")
    elif random_legends == "Crypto":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-crypto.png.adapt.crop16x9.png")
    elif random_legends == "Fuse":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2021/01/apex-grid-tile-legends-fuse.png.adapt.crop16x9.png")
    elif random_legends == "Gibraltar":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-gibraltar.png.adapt.crop16x9.png")
    elif random_legends == "Horizon":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2020/10/horizon/apex-grid-tile-legends-horizon.png.adapt.crop16x9.png")
    elif random_legends == "Lifeline":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-lifeline.png.adapt.crop16x9.png")
    elif random_legends == "Loba":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2020/05/apex-grid-tile-legends-loba.png.adapt.crop16x9.png")
    elif random_legends == "Mirage":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-mirage.png.adapt.crop16x9.png")
    elif random_legends == "Octane":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-octane.png.adapt.crop16x9.png")
    elif random_legends == "Pathfinder":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-pathfinder.png.adapt.crop16x9.png")
    elif random_legends == "Rampart":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2020/08/rampart/apex-grid-tile-legends-rampart.png.adapt.crop16x9.png")
    elif random_legends == "Revenant":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2020/02/apex-legend-revenant-grid-tile.png.adapt.crop16x9.png")
    elif random_legends == "Seer":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2021/07/seer-assets/apex-grid-tile-legends-seer.png.adapt.crop16x9.png")
    elif random_legends == "Valkyrie":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2021/04/apex-grid-tile-legends-valkyrie.png.adapt.crop16x9.png")
    elif random_legends == "Wattson":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-wattson.png.adapt.crop16x9.png")
    elif random_legends == "Wraith":
        embed.set_thumbnail(url="https://media.contentapi.ea.com/content/dam/apex-legends/images/2019/01/legends-character-tiles/apex-grid-tile-legends-wraith.png.adapt.crop16x9.png")
    
    embed.description = f"**{random_legends}**"

    return embed