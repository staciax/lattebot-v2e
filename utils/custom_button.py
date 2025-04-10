# Standard 
import discord
import random
from discord.ext import commands
from typing import List

# Third
import requests
from io import BytesIO
from colorthief import ColorThief

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
        self.is_command = ctx.command is not None
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        """Only allowing the context author to interact with the view"""
        ctx = self.ctx
        author = ctx.author
        if interaction.user == ctx.bot.renly:
            return True
        if interaction.user != ctx.author:
            bucket = self.cooldown.get_bucket(ctx.message)
            if not bucket.update_rate_limit():
                if self.is_command:
                    command = ctx.bot.get_command_signature(ctx, ctx.command)
                    content = f"Only `{author}` can use this menu. If you want to use it, use `{command}`"
                else:
                    content = f"Only `{author}` can use this."
                embed = RenlyEmbed.to_error(description=content)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Member list", style=discord.ButtonStyle.blurple)
    async def member_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        p = SimplePages(entries=self.entries, per_page=10, ctx=self.ctx)
        p.embed.title = f"{self.role.name} : members list"
        p.embed.color = self.role.color
        await p.start()

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.red)
    async def stop_pages(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()
    
    async def start(self):
        if not self.entries:
            self.member_list.disabled = True
        self.message = await self.ctx.reply(embed=self.embed, view=self , mention_author=False)

class channel_info_view(discord.ui.View):
    def __init__(self, ctx, embed, channel , role_list, member_list):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.embed = embed
        self.channel = channel
        self.role_list = role_list
        self.member_list = member_list
        self.is_command = ctx.command is not None
        self.cooldown = commands.CooldownMapping.from_cooldown(2, 10, commands.BucketType.user)
        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:
        if self.role_list is not None:
            self.add_item(self.roles_list_button)
        if self.member_list is not None:
            self.add_item(self.member_list_button)
        self.add_item(self.quit_button)

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
                await self.message.edit(view=self)
        except:
            if self.message:
                self.clear_items()
                return await self.message.edit(view=self)
    
    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        """Only allowing the context author to interact with the view"""
        ctx = self.ctx
        author = ctx.author
        if interaction.user == ctx.bot.renly:
            return True
        if interaction.user != author:
            bucket = self.cooldown.get_bucket(ctx.message)
            if not bucket.update_rate_limit():
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
    async def roles_list_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        p = SimplePages(entries=self.role_list, per_page=10, ctx=self.ctx)
        p.embed.title = f"Roles in {self.channel.name}"
        p.embed.color = 0xffffff
        await p.start()
    
    @discord.ui.button(label="Member access", style=discord.ButtonStyle.blurple)
    async def member_list_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        p = SimplePages(entries=self.member_list, per_page=10, ctx=self.ctx)
        p.embed.title = f"Members in {self.channel.name}"
        p.embed.color = 0xffffff
        await p.start()

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.red)
    async def quit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.on_timeout()
        # await interaction.response.defer()
        # await interaction.delete_original_message()
        # self.stop()
    
    async def start_text(self):
        self.message = await self.ctx.reply(embed=self.embed, view=self, mention_author=False)
    
    async def start_voice(self):
        self.remove_item(self.member_list_button)
        self.message = await self.ctx.reply(embed=self.embed, view=self, mention_author=False)


class base_Button_URL(discord.ui.View):
    def __init__(self, label:str, url, emoji=None):
        super().__init__()
        self.label = label
        self.url = url
        self.emoji = emoji
        self.clear_items()
        self.fill_items()
    
    def fill_items(self):
        if self.label and self.url and self.emoji is not None:
            self.add_item(discord.ui.Button(label=self.label, url=self.url, emoji=self.emoji))
        elif self.label and self.url:
            self.add_item(discord.ui.Button(label=self.label, url=self.url))

class Button_URL(discord.ui.View):
    def __init__(self, label, url):
        super().__init__()
        self.label = label
        self.url = url
        self.clear_items()
        self.fill_items()

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    def fill_items(self):
        for x,y in zip(self.label, self.url):
            self.add_item(discord.ui.Button(label=x, url=y))

class button_random(discord.ui.Button):
    def __init__(self, ctx, member_list, label : str): #, style : discord.ButtonStyle
        super().__init__(label=label , style=discord.ButtonStyle.green) #, style=style)
        self.member_list = member_list
        self.ctx = ctx

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

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

class content_button(discord.ui.View):
    def __init__(self, ctx, content=None):
        super().__init__()
        self.ctx = ctx
        self.content = content
        self.is_command = ctx.command is not None
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        self.clear_items()
        self.fill_items()
        
    def fill_items(self) -> None:
        if self.content is not None:
            self.add_item(self.content_button)
    
    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        """Only allowing the context author to interact with the view"""
        ctx = self.ctx
        author = ctx.author
        mystic_role = discord.utils.get(interaction.user.roles, id=842304286737956876)
        if interaction.user == ctx.bot.renly:
            return True
        if bool(mystic_role) == True:
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

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
        
    @discord.ui.button(label="Content", style=discord.ButtonStyle.primary)
    async def content_button(self, button, interaction):
        await interaction.response.send_message(self.content, ephemeral=True)

class AvatarView(discord.ui.View):
    def __init__(self, ctx, member):
        super().__init__()
        self.ctx = ctx
        self.member = member
        self.avatar_url = member.avatar
        self.avatar_display_url = member.display_avatar if member.avatar != member.display_avatar else None
        self.embeds: List[discord.Embed] = []
        self.clear_items()

    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        """Only allowing the context author to interact with the view"""
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
    
    def display_view(self) -> None:
        self.clear_items()
        if len(self.embeds) > 0:
            self.add_item(self.category_select)
            self.category_select: discord.ui.Select
            self.category_select.options = []
            self.category_select.add_option(label="User Avatar", value='avatar')
            self.category_select.add_option(label="Server Avatar", value='display')

    def avatar_url_button(self):
        self.add_item(discord.ui.Button(label="Avatar URL", url=self.avatar_url))

    @discord.ui.select(placeholder="Select avatar", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.display_view()
        if select.values[0] == 'avatar':
            self.avatar_url_button()
            await interaction.response.edit_message(embed=self.embeds[0], view=self)
        elif select.values[0] == 'display':
            self.add_item(discord.ui.Button(label="Server avatar URL", url=self.avatar_display_url))
            await interaction.response.edit_message(embed=self.embeds[1], view=self)
    
    def get_color(self, member, avatar_url) -> None:
        try:
            url = avatar_url.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            if member.color != discord.Colour.default():
                dominant_color = member.colour
            else:
                dominant_color = self.ctx.bot.white_color
        return dominant_color

    def avatar_embed(self) -> discord.Embed:
        member = self.member
        embed = discord.Embed()
        embed.title = f"{member.name}'s Avatar:"
        embed.set_image(url=self.avatar_url)
        embed.color = self.get_color(member, self.avatar_url)
        self.embeds.append(embed)

    def display_embed(self) -> discord.Embed:
        member = self.member
        embed = discord.Embed()
        embed.title = f"{member.name}'s Server avatar:"
        embed.set_image(url=self.avatar_display_url)
        embed.color = self.get_color(member, self.avatar_display_url)
        self.embeds.append(embed)

    async def start(self) -> None:
        self.avatar_embed()
        if self.avatar_display_url:
            self.display_embed()
            self.display_view()
        self.avatar_url_button()
        await self.ctx.reply(embed=self.embeds[0], view=self, mention_author=False)