# Standard
import discord
from discord.ext import commands
from discord import Embed

# Third
import aiohttp
import requests
from io import BytesIO
from colorthief import ColorThief

# Local


def Color_Thief(url):
    resp = requests.get(url)      
    out = BytesIO(resp.content)
    out.seek(0)
    icon_color = ColorThief(out).get_color(quality=1)
    icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
    dominant_color = int(icon_hex, 16)
    return dominant_color

class Waifu_im_selection(discord.ui.Select):
    def __init__(self, types):
        self.types = types
        self.typed = ''

        if types == 'sfw':
            options = [
                discord.SelectOption(label='Waifu', description='Waifu'),
                discord.SelectOption(label='Maid', description='Maid')
                # discord.SelectOption(label='All', description='All'),
            ]
        elif types == 'nsfw':
            options = [
                discord.SelectOption(label='Ass', description='Waifu'),
                discord.SelectOption(label='Ecchi',  description='Maid'),
                discord.SelectOption(label='Ero', description='Ero'),
                discord.SelectOption(label='Hentai', description='Hentai'),
                discord.SelectOption(label='Maid', description='Maid'),
                discord.SelectOption(label='Milf',  description='Milf'),
                discord.SelectOption(label='Oppai', description='Oppai'),
                discord.SelectOption(label='Oral', description='Oral'),
                discord.SelectOption(label='Paizuri', description='Paizuri'),
                discord.SelectOption(label='Selfies', description='Selfies'),
                discord.SelectOption(label='Uniform', description='Uniform'),
            ]
        super().__init__(placeholder='Select a type...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.typed = self.values[0]

#-------------------- WAIFU IM --------------------#

    #----- base embed -----#

def Waifu_im_Embed(api_title, api_color, image_url):
    embed = Embed(title=api_title, url=image_url, color=int(api_color)) #timestamp=discord.utils.utcnow(),
    embed.set_image(url=image_url)
    embed.set_footer(text="Powered by waifu.im")
    
    return embed

    #----- SFW -----#

class base_waifu_im_api(discord.ui.View):
    def __init__(self, ctx, url):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = url
        self.image_url = ''
        self.message = None
        self.gif = False
        self.source_url = ''

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.image_url))
    
    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.im/"))

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False
    
    # @staticmethod
    # def Waifu_im_Embed(api_title, api_color, image_url):
    #     if api_title == "all": api_title = "random"
    #     embed = Embed(title=api_title, url=image_url, color=int(api_color)) #timestamp=discord.utils.utcnow(),
    #     embed.set_image(url=image_url)
    #     embed.set_footer(text="Powered by waifu.im")
        
    #     return embed

    @staticmethod
    async def base_embed(self):
        request = await self.ctx.bot.session.get(f'{self.url}/?gif={self.gif}')
        api = await request.json()
        if request.status == 200:
            api_title = api.get('images')[0].get('tags')[0].get('name')

            #color_converter
            dominant_color1 = str(api.get('images')[0].get('dominant_color')).replace('#', '')
            dominant_color = int(dominant_color1, 16)


            api_color = dominant_color
            image_url = api.get('images')[0].get('url')
            source_url = api.get('images')[0].get('source')
            self.image_url = image_url
            self.source_url = source_url
 
            embed_api = Waifu_im_Embed(api_title, api_color, image_url)
            return embed_api

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.gif = False
        embed = await self.base_embed(self)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
        if embed:
            await interaction.response.edit_message(embed=embed, view=self)
    
    # @discord.ui.button(label="GIF", style=discord.ButtonStyle.blurple, custom_id='b3')
    # async def gif_true_or_false(self, button, interaction):
    #     if self.url in ['https://api.waifu.im/sfw/maid', 'https://api.waifu.im/nsfw/maid', 'https://api.waifu.im/nsfw/selfies/']:
    #         self.gif = False
    #     else:
    #         self.gif = True
    #     embed = await self.base_embed(self)
    #     if embed:
    #         await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button:discord.ui.Button, interaction: discord.Interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    # @discord.ui.select(custom_id="Select_waifu_im", placeholder="Select category..", min_values=1, max_values=1, options=[
    #     discord.SelectOption(label='Waifu', value="waifu", description='Waifu'),
    #     discord.SelectOption(label='Maid', value="maid", description='Maid'),
    #     discord.SelectOption(label='All', value="all", description='All'),
    # ])
    # async def callback(self, select: discord.ui.select, interaction: discord.Interaction):
    #     if select.values[0]: self.url = f'https://api.waifu.im/sfw/{select.values[0]}' #/?gif={self.gif}

    async def api_start(self):
        self.gif = False
        embed = await self.base_embed(self)
        if embed:
            self.add_button()
            self.message = await self.ctx.reply(embed=embed, view=self, mention_author=False)

    #----- NSFW -----#

class base_waifu_im_api_nsfw(discord.ui.View):
    def __init__(self, ctx, url):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = url
        self.image_url = ''
        self.message = None
        self.gif = False
        self.source_url = ''

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.image_url))
    
    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.im/"))

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False
    
    @staticmethod
    async def base_embed(self):
        request = await self.ctx.bot.session.get(f'{self.url}/?gif={self.gif}')
        api = await request.json()
        if request.status == 200:
            api_title = api.get('images')[0].get('tags')[0].get('name')

            #color_converter
            dominant_color1 = str(api.get('images')[0].get('dominant_color')).replace('#', '')
            dominant_color = int(dominant_color1, 16)


            api_color = dominant_color
            image_url = api.get('images')[0].get('url')
            source_url = api.get('images')[0].get('source')
            self.image_url = image_url
            self.source_url = source_url
 
            embed_api = Waifu_im_Embed(api_title, api_color, image_url)
            return embed_api

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.gif = False
        embed = await self.base_embed(self)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
        if embed:           
            await interaction.response.edit_message(embed=embed, view=self)
    
    # @discord.ui.button(label="GIF", style=discord.ButtonStyle.blurple, custom_id='b3')
    # async def gif_true_or_false(self, button, interaction):
    #     if self.url in ['https://api.waifu.im/nsfw/maid', 'https://api.waifu.im/nsfw/selfies/']:
    #         self.gif = False
    #     else:
    #         self.gif = True
    #     embed = await self.base_embed(self)
    #     if embed:
    #         await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_im", placeholder="Select category..", min_values=1, max_values=1, options=[
        discord.SelectOption(label='Ass', value='ass'),
        discord.SelectOption(label='Ecchi', value='ecchi'),
        discord.SelectOption(label='Ero', value='ero'),
        discord.SelectOption(label='Hentai', value='hentai'),
        discord.SelectOption(label='Maid', value='maid'),
        discord.SelectOption(label='Milf', value='milf'),
        discord.SelectOption(label='Oppai', value='oppi'),
        discord.SelectOption(label='Oral', value='oral'),
        discord.SelectOption(label='Paizuri', value='paizuri'),
        discord.SelectOption(label='Selfies', value='selfies'),
        discord.SelectOption(label='Uniform', value='uniform')])
    async def callback(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.im/nsfw/{select.values[0]}'
    
    async def api_start(self):
        self.gif = False
        embed = await self.base_embed(self)
        if embed:
            self.add_button()
            self.message = await self.ctx.reply(embed=embed, view=self, mention_author=False)

#-------------------- WAIFU PISC --------------------#

    #----- base embed -----#

def Waifu_pisc_Embed(self, json, title):
    embed = discord.Embed(title=title,url=json["url"], color=0xffffff)
    embed.set_image(url=json['url'])
    embed.set_footer(text="Powered by waifu.pisc")
 
    return embed

    #----- SFW -----#

class base_waifu_pisc_api(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = 'https://api.waifu.pics/sfw/waifu'
        self.json_url = ''
        self.title = 'waifu'
        self.message = ''

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.json_url))

    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url='https://waifu.pics/'))

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @staticmethod
    async def base_api(self):
        request = await self.ctx.bot.session.get(self.url)
        api = await request.json()
        if request.status == 200:
            json = api
            self.json_url = json["url"]

        embed = Waifu_pisc_Embed(self, json, title=self.title)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()

        return embed

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = await self.base_api(self)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_pics_1", placeholder="Select category (A - K)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Awoo', value="awoo"),
        discord.SelectOption(label='Bite', value="bite"),
        discord.SelectOption(label='Blush', value="blush"),
        discord.SelectOption(label='Bonk', value="bonk"),
        discord.SelectOption(label='bully', value="bully"),
        discord.SelectOption(label='Cringe', value="cringe"),
        discord.SelectOption(label='Cry', value="cry"),
        discord.SelectOption(label='Cuddle', value="cuddle"),
        discord.SelectOption(label='Dance', value="dance"),
        discord.SelectOption(label='Glomp', value="glomp"),
        discord.SelectOption(label='Handhold', value="handhold"),
        discord.SelectOption(label='Happy', value="happy"),
        discord.SelectOption(label='Highfive', value="highfive"),
        discord.SelectOption(label='Hug', value="hug"),
        discord.SelectOption(label='Kick', value="kick"),
        discord.SelectOption(label='Kill', value="kill"),
        discord.SelectOption(label='Kiss', value="kiss"),
    ])
    async def callback_a_k(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/sfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
    
    @discord.ui.select(custom_id="Select_waifu_pics_2", placeholder="Select category (L - Z)", min_values=1, max_values=1, options=[
        discord.SelectOption(label='Lick', value="lick"),
        discord.SelectOption(label='Megumin', value="megumin"),
        discord.SelectOption(label='Neko', value="neko"),
        discord.SelectOption(label='Nom', value="nom"),
        discord.SelectOption(label='Pat', value="pat"),
        discord.SelectOption(label='Poke', value="poke"),
        discord.SelectOption(label='Shinobu', value="shinobu"),
        discord.SelectOption(label='Slap', value="slap"),
        discord.SelectOption(label='Smile', value="smile"),
        discord.SelectOption(label='Smug', value="smug"),
        discord.SelectOption(label='Waifu', value="waifu"),
        discord.SelectOption(label='Wave', value="wave"),
        discord.SelectOption(label='Wink', value="wink"),
        discord.SelectOption(label='Yeet', value="yeet"),
    ])
    async def callback_L_z(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/sfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
        
    async def api_start(self):
        request = await self.ctx.bot.session.get(self.url)
        api = await request.json()
        if request.status == 200:
            json = api
            self.json_url = json["url"]

        self.add_button()
        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)
    
    #----- NSFW -----#

class base_waifu_pisc_api_nsfw(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = 'https://api.waifu.pics/nsfw/waifu'
        self.json_url = ''
        self.title = 'waifu'
        self.message = ''

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.json_url))

    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.pics/"))

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        request = await self.ctx.bot.session.get(self.url)
        api = await request.json()
        if request.status == 200:
            json = api
            self.json_url = json["url"]

        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
        if embed1:       
            await interaction.response.edit_message(embed=embed1, view=self)

    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_pics_1", placeholder="Select category..", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Waifu', value="waifu", description='Waifu'),
        discord.SelectOption(label='Neko', value="neko", description='Waifu'),
        discord.SelectOption(label='Trap', value="trap", description='Waifu'),
        discord.SelectOption(label='Blowjob', value="blowjob", description='Waifu')
    ])
    async def callback_a_k(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/nsfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
    
    async def api_start(self):
        request = await self.ctx.bot.session.get(self.url)
        api = await request.json()
        if request.status == 200:
            json = api
            self.json_url = json["url"]

        self.add_button()
        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)