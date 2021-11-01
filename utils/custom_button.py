# Standard 
import discord
import random
from discord.ext import commands

# Local
from utils.paginator import SimplePages
from utils.useful import RenlyEmbed
from utils.buttons import BaseNewButton, SimplePageSource

class roleinfo_view(discord.ui.View):
    def __init__(self, ctx, embed, entries, role):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.embed = embed
        self.entries = entries
        self.role = role
        self.message = ""
        self.is_command = ctx.command is not None

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @discord.ui.button(label="Member list", style=discord.ButtonStyle.blurple)
    async def member_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        p = SimplePages(entries=self.entries, per_page=10, ctx=self.ctx)
        p.embed.title = f"{self.role.name} : members list"
        p.embed.color = self.role.color
        self.message = await p.start()

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.red)
    async def stop_pages(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()
    
    async def start(self):
        if not self.entries:
            if self.children[0].label == 'Member list':
                self.children[0].disabled = True
        self.message = await self.ctx.reply(embed=self.embed, view=self , mention_author=False)


class channel_info_view(discord.ui.View):
    def __init__(self, ctx, embed, channel , role_list, member_list):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.embed = embed
        self.channel = channel
        self.role_list = role_list
        self.member_list = member_list
        self.message = ""
        self.is_command = ctx.command is not None

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)
    
    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        ctx = self.ctx
        author = ctx.author
        if interaction.user == ctx.bot.renly:
            return True
        if interaction.user != ctx.author:
            if self.is_command:
                command = ctx.bot.get_command_signature(ctx, ctx.command)
                content = f"Only `{author}` can use this menu. If you want to use it, use `{command}`"
            else:
                content = f"Only `{author}` can use this."
            embed = RenlyEmbed.to_error(description=content)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Roles access", style=discord.ButtonStyle.blurple)
    async def roles_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author.id == interaction.user.id:
            p = SimplePages(entries=self.role_list, per_page=10, ctx=self.ctx)
            p.embed.title = f"Roles in {self.channel.name}"
            p.embed.color = 0xffffff
            await p.start()
    
    @discord.ui.button(label="Member access", style=discord.ButtonStyle.blurple)
    async def member_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        p = SimplePages(entries=self.member_list, per_page=10, ctx=self.ctx)
        p.embed.title = f"Members in {self.channel.name}"
        p.embed.color = 0xffffff
        await p.start()

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.red)
    async def stop_pages(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()
    
    async def start_text(self):
        if not self.role_list:
            if self.children[0].label == 'Roles access':
                self.remove_item(item=self.children[0])
        if not self.member_list:
            if self.children[0].label == 'Member access':
                self.remove_item(item=self.children[0])

        self.message = await self.ctx.reply(embed=self.embed, view=self, mention_author=False)
    
    async def start_voice(self):
        for item in self.children:
            if item.label == 'Member access':
                self.remove_item(item)
        self.message = await self.ctx.reply(embed=self.embed, view=self, mention_author=False)


class base_Button_URL(discord.ui.View):
    def __init__(self, label:str, url):
        super().__init__()
        self.label = label
        self.url = url
        self.clear_items()
        self.fill_items()
    
    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    def fill_items(self):
        if self.label and self.url:
            self.add_item(discord.ui.Button(label=self.label, url=self.url))

class base_Button_URL2(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()
        self.label = label
        self.url = url
        self.clear_items()
        self.fill_items()

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    def fill_items(self):
        for x,y in zip(self.label, self.url):
            self.add_item(discord.ui.Button(label=x, url=y))

class button_random(discord.ui.Button):
    def __init__(self, ctx, member_list, label : str): #, style : discord.ButtonStyle
        super().__init__(label=label , style=discord.ButtonStyle.green) #, style=style)
        self.member_list = member_list
        self.ctx = ctx

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    async def callback(self, interaction):
        embed = discord.Embed()
        member = random.choice(self.member_list)
        if member.color:
            embed.color = member.color
        else:
            embed.color = 0xffffff

        if member.avatar:
            embed.set_author(name=member.name , icon_url=member.avatar.url)
        else:
            embed.set_author(name=member.name)

        await self.ctx.channel.send(embed=embed)
                
        # await interaction.response.send_message(embed=embed)

class Random_member(BaseNewButton):

    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 12 , member_list):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        for items in self.children:
            if items.custom_id in ['1','4']:
                self.remove_item(item=items)
        self.embed = discord.Embed(colour=discord.Colour.blurple())
        self.add_item(item=button_random(ctx, member_list, 'Random'))