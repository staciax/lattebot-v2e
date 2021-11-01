import discord
import random
from discord import Embed
from discord.ext import commands

from utils.buttons import NewSimpage

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
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

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
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.display_name}: {a_logging}'
        else:
            await self.embeds_legend.edit(embed=embed)
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
            self.counts += 1
            self.logging += f'\n{self.counts}. {interaction.user.name}: {a_logging}'
        else:
            await self.embeds_weapon.edit(embed=embed)
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

class VALORANT_RANDOM(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=1800)
        self.ctx = ctx
        self.agent_type = None
        self.weapon_type = None
        self.message = ''
        self.embeds_agent = None
        self.embeds_weapon = None
        self.log_agent = ''
        self.log_weapon = ''
        self.counts = 0

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    @discord.ui.select(custom_id="Select Agent type", placeholder="Agent type (default=random)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Random', value="random"),
        discord.SelectOption(label='Duelist', value="duelist"),
        discord.SelectOption(label='Controller', value="controller"),
        discord.SelectOption(label='Initiator', value="initiator"),
        discord.SelectOption(label='Sentinel', value="sentinel"),
    ])
    async def callback_agent(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0] == 'random':
            self.agent_type = None
        elif select.values[0]:
            self.agent_type = f'{str(select.values[0])}'
    
    @discord.ui.select(custom_id="Select Weapon type", placeholder="Weapon type (default=random)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Random', value="random"),
        discord.SelectOption(label='Sidearms', value="side"),
        discord.SelectOption(label='Sub-machine guns', value="smg"),
        discord.SelectOption(label='Shotguns', value="sg"),
        discord.SelectOption(label='Assault rifles', value="ar"),
        discord.SelectOption(label='Sniper Rifles', value="sniper"),
        discord.SelectOption(label='Machine Guns', value="mg"),
    ])
    async def callback_weapon(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0] == 'random':
            self.weapon_type = None
        elif select.values[0]:
            self.weapon_type = f'{str(select.values[0])}'
    
    @discord.ui.button(label="Agent", style=discord.ButtonStyle.blurple)
    async def valorant_agent(self, button, interaction):
        self.w_log.disabled = False
        await self.message.edit(view=self)
        
        embed = valorant_random_agent(category=self.agent_type)
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Req by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Req by {interaction.user.display_name}')
        a_logging = str(embed.description.split('**' )[1])
        if self.embeds_agent is None:
            self.embeds_agent = await self.ctx.channel.send(embed=embed)
            self.counts += 1
            self.log_weapon += f'\n{self.counts}. {self.ctx.author.name}: {a_logging}'
        else:
            await self.embeds_agent.edit(embed=embed)
            self.counts += 1
            self.log_weapon += f'\n{self.counts}. {self.ctx.author.name}: {a_logging}'
    
    @discord.ui.button(label="Weapon", style=discord.ButtonStyle.blurple)
    async def valorant_weapon(self, button, interaction):
        self.w_log.disabled = False
        await self.message.edit(view=self)

        data = self.log_weapon.split('\n')
        if len(data) == 100:
            await interaction.response.send_message("", ephemeral=True)
            
        embed = valorant_random_weapon(category=self.weapon_type)
        if interaction.user.avatar is not None:
            embed.set_footer(text=f'Req by {interaction.user.display_name}', icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text=f'Req by {interaction.user.display_name}')
        w_logging = str(embed.description.split('**' )[1])
        if self.embeds_weapon is None:
            self.embeds_weapon = await self.ctx.channel.send(embed=embed)
            self.counts += 1
            self.log_weapon += f'\n{self.counts}. {interaction.user.display_name}: {w_logging}'
        else:
            await self.embeds_weapon.edit(embed=embed)
            self.counts += 1
            self.log_weapon += f'\n{self.counts}. {interaction.user.display_name}: {w_logging}'

    @discord.ui.button(label="Log", style=discord.ButtonStyle.gray)
    async def w_log(self, button, interaction):
        embed = discord.Embed(color=0xffffff)
        embed.description = ''
        weapon_log_list = []

        data = self.log_weapon
        if data:
            await interaction.response.send_message(self.log_weapon, ephemeral=True)
            # print(self.log_weapon.split('\n'))

        # p = Custom_page(entries=self.log_weapon.split('\n'), ctx=self.ctx)
        # await p.start()

        # if data:
        #     for x in self.log_weapon.keys():
        #         member = self.ctx.guild.get_member(int(x))
        #         embed.description += f"{member}. {data[x]['weapon']}\n"
            
        #     await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # else:
        #     embed.description = 'logging not found'
        #     await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # @discord.ui.button(label="Weapon Log", style=discord.ButtonStyle.blurple)
    # async def w_log(self, button, interaction):
    #     print()

    async def start(self):
        self.w_log.disabled = True
        embed = discord.Embed(title="Valorant")
        embed.description = '`valorant random`\n`-agent`\n`-weapon`'
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/417245049315655690/902173852401025074/valorant.jpg')
        embed.color = 0xfa4454
        if embed:
            self.message = await self.ctx.send(embed=embed, view=self, mention_author=False)


def apex_random_weapon(category):
    #embed
    embed = Embed(color=0xFFA500)

    #list_of_weapon
    Assault_rifles = ["HAVOC Rifle", "VK-47 Flatline", "Hemlok Burst AR" , "R-301 Carbine"]
    Submachine_guns = ["Alternator SMG","Prowler Burst PDW","R-99 SMG","Volt SMG"]
    Light_machine_guns = ["Devotion LMG" , "L-STAR EMG", "M600 Spitfire" , "Rampage"]
    Marksman_weapons = ["G7 Scout", "Triple Take", "30-30 Repeater", "Bocek Compound Bow"]
    Sniper_rifles = ["Charge Rifle", "Longbow DMR", "Kraber .50-Cal Sniper", "Sentinel"]
    Shotguns = ["EVA-8 Auto", "Mastiff Shotgun", "Mozambique Shotgun", "Peacekeeper"]
    Pistols = ["RE-45 Auto","P2020","Wingman"]
    all_weapon = ["HAVOC Rifle", "VK-47 Flatline", "Hemlok Burst AR" , "R-301 Carbine","Alternator SMG","Prowler Burst PDW","R-99 SMG","Volt SMG","Devotion LMG" , "L-STAR EMG", "M600 Spitfire" , "Rampage","G7 Scout", "Triple Take", "30-30 Repeater", "Bocek Compound Bow","Charge Rifle", "Longbow DMR", "Kraber .50-Cal Sniper", "Sentinel","EVA-8 Auto", "Mastiff Shotgun", "Mozambique Shotgun", "Peacekeeper","RE-45 Auto","P2020","Wingman"]

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
    embed = Embed(color=0xFFA500)

    #list_of_legends
    legends_list = ['Bangalore','Bloodhound','Caustic','Crypto','Fuse','Gibraltar','Horizon','Lifeline','Loba','Mirage','Octane','Pathfinder','Rampart','Revenant','Seer','Valkyrie','Wattson','Wraith']
    
    random_legends = random.choice(legends_list)

    #picture_of_agent
    if random_legends == "Bangalore":
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

#valorant
def valorant_random_agent(category):
    #embed
    embed = discord.Embed(color=0xfa4454)

    #list_of_agent
    Duelist = ["Phoenix", "Jett", "Reyna", "Raze", "Yoru"]
    Controller = ["Brimston","Viper","Omen","Astra"]
    Initiator = ["Sova", "Breach", "KAY/O" "Skye"]
    Sentinel = ["Killjoy", "Cypher", "Sage"]
    all_agent = ["Phoenix", "Jett", "Reyna", "Raze", "Yoru", "Brimston","Viper","Omen","Astra", "Sova", "Breach", "KAY/O", "Killjoy", "Cypher", "Sage"]
    
    #category
    if category == None:
        random_agent = random.choice(all_agent)
    elif category == "duelist":
        random_agent = random.choice(Duelist)
    elif category == "controller":
        random_agent = random.choice(Controller)
    elif category == "initiator":
        random_agent = random.choice(Initiator)
    elif category == "sentinel":
        random_agent = random.choice(Sentinel)
    
    embed.description = f"**{random_agent}**\n"

    #picture_of_agent
    if random_agent == "Phoenix":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/1/14/Phoenix_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234131")
        embed.description += f"`duelist`"
    elif random_agent == "Jett":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/3/35/Jett_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234156")
        embed.description += f"`duelist`"
    elif random_agent == "Reyna":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/b/b0/Reyna_icon.png/revision/latest/scale-to-width-down/256?cb=20200607180311")
        embed.description += f"`duelist`"
    elif random_agent == "Raze":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/9/9c/Raze_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234400")
        embed.description += f"`duelist`"
    elif random_agent == "Yoru":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/d/d4/Yoru_icon.png/revision/latest/scale-to-width-down/256?cb=20210112211830")
        embed.description += f"`duelist`"
    elif random_agent == "Brimston":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/4/4d/Brimstone_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234311")
        embed.description += f"`controller`"
    elif random_agent == "Viper":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/5/5f/Viper_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234408")
        embed.description += f"`controller`"
    elif random_agent == "Omen":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/b/b0/Omen_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234318")
        embed.description += f"`controller`"
    elif random_agent == "Astra":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/0/08/Astra_icon.png/revision/latest/scale-to-width-down/256?cb=20210302164234")
        embed.description += f"`controller`"
    elif random_agent == "Sova":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/4/49/Sova_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234221")
        embed.description += f"`initiator`"
    elif random_agent == "Breach":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/5/53/Breach_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234328")
        embed.description += f"`initiator`"
    elif random_agent == "KAY/O":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/f/f0/KAYO_icon.png/revision/latest/scale-to-width-down/256?cb=20210622225019")
        embed.description += f"`initiator`"
    elif random_agent == "Skye":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/3/33/Skye_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234628")
        embed.description += f"`initiator`"
    elif random_agent == "Killjoy":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/1/15/Killjoy_icon.png/revision/latest/scale-to-width-down/256?cb=20200805002141")
        embed.description += f"`sentinel`"
    elif random_agent == "Cypher":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/8/88/Cypher_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234211")
        embed.description += f"`sentinel`"
    elif random_agent == "Sage":
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/7/74/Sage_icon.png/revision/latest/scale-to-width-down/256?cb=20201128234057")
        embed.description += f"`sentinel`"
    

    return embed

def valorant_random_weapon(category):
    #embed
    embed = Embed(color=0xfa4454)

    #list_of_weapon
    all_gun = ["Classic","Shorty","Frenzy","Ghost","Sheriff","Stinger", "Spectre","Bucky", "Judge" , "Bulldog", "Guardian", "Phantom" , "Vandal" ,"Ares", "Odin" , "Knife"]
    Sidearms = ["Classic","Shorty","Frenzy","Ghost","Sheriff"]
    SMGs = ["Stinger", "Spectre"]
    Shotguns = ["Bucky", "Judge"]
    Rifles = ["Bulldog", "Guardian", "Phantom" , "Vandal"]
    Sniper_Rifles = ["Marshal", "Operator"]
    Machine_Guns = ["Ares", "Odin"]
#   Malee = "Knife"      

    #category
    if category == None:
        random_gun = random.choice(all_gun)
    elif category in ["sidearms", "sidearm","side","sa"]:
        random_gun = random.choice(Sidearms)
    elif category in ["smg", "smgs"]:
        random_gun = random.choice(SMGs)
    elif category in ["shotgun","shotguns","sg"]:
        random_gun = random.choice(Shotguns)
    elif category in ["rifles","rifle","ar"]:
        random_gun = random.choice(Rifles)
    elif category in ["sniper","Sniper Rifles"]:
        random_gun = random.choice(Sniper_Rifles)
    elif category in ["machine","machine gun","mg"]:
        random_gun = random.choice(Machine_Guns)
            
    #picture_of_gun
    if random_gun == "Classic":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/5/57/Classic.png/revision/latest/scale-to-width-down/1000?cb=20200404154125")
    elif random_gun == "Shorty":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/7/77/Shorty.png/revision/latest/scale-to-width-down/1000?cb=20200404154222")
    elif random_gun == "Frenzy":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/f/f1/Frenzy.png/revision/latest/scale-to-width-down/1000?cb=20200404154617")
    elif random_gun == "Ghost":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/a/ab/Ghost.png/revision/latest/scale-to-width-down/1000?cb=20200404154731")
    elif random_gun == "Sheriff":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/3/3e/Sheriff.png/revision/latest/scale-to-width-down/1000?cb=20200404154438")
    elif random_gun == "Stinger":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/b/b6/Stinger.png/revision/latest/scale-to-width-down/1000?cb=20200404170849")
    elif random_gun == "Spectre":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/9/90/Spectre.png/revision/latest/scale-to-width-down/1000?cb=20200404170922")
    elif random_gun == "Bucky":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/e/eb/Bucky.png/revision/latest/scale-to-width-down/1000?cb=20200404171832")
    elif random_gun == "Judge":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/8/8a/Judge.png/revision/latest/scale-to-width-down/1000?cb=20200404171858")
    elif random_gun == "Bulldog":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/0/07/Bulldog.png/revision/latest/scale-to-width-down/1000?cb=20200404171103")
    elif random_gun == "Guardian":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/f/fd/Guardian.png/revision/latest/scale-to-width-down/1000?cb=20200404171224")
    elif random_gun == "Phantom":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/e/ec/Phantom.png/revision/latest/scale-to-width-down/1000?cb=20200404171302")
    elif random_gun == "Vandal":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/5/56/Vandal.png/revision/latest/scale-to-width-down/1000?cb=20200404171348")
    elif random_gun == "Marshal":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/b/b9/Marshal.png/revision/latest/scale-to-width-down/1000?cb=20200404172126")
    elif random_gun == "Operator":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/1/17/Operator.png/revision/latest/scale-to-width-down/1000?cb=20200404172152")
    elif random_gun == "Ares":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/0/05/Ares.png/revision/latest/scale-to-width-down/1000?cb=20200404171957")
    elif random_gun == "Odin":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/5/58/Odin.png/revision/latest/scale-to-width-down/1000?cb=20200404172022")
    elif random_gun == "Knife":
        embed.set_image(url="https://static.wikia.nocookie.net/valorant/images/d/d8/TacticalKnife.png/revision/latest/scale-to-width-down/1000?cb=20200404172248")
    
    embed.description = f"**{random_gun}**"

    return embed