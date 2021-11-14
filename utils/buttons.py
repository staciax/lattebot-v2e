# Standard
from __future__ import annotations

import discord
import asyncio
from typing import Any, Dict, Optional
from discord.ext import commands
from discord.ext.commands import Paginator as CommandPaginator
from utils.useful import RenlyEmbed

# Third
from discord.ext import menus

class BaseNewButton(discord.ui.View):
    def __init__(
        self,
        source: menus.PageSource,
        *,
        ctx: commands.Context,
        check_embeds: bool = True,
        compact: bool = False,
    ):
        super().__init__()
        self.source: menus.PageSource = source
        self.check_embeds: bool = check_embeds
        self.ctx: commands.Context = ctx
        self.message: Optional[discord.Message] = None
        self.current_page: int = 0
        self.compact: bool = compact
        self.input_lock = asyncio.Lock()
        self.is_command = ctx.command is not None
        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:
        if not self.compact:
            self.stop_pages.row = 1

        if self.source.is_paginating():
            max_pages = self.source.get_max_pages()
            use_last_and_first = max_pages is not None and max_pages >= 2
            if use_last_and_first:
                self.add_item(self.go_to_first_page)  # type: ignore
            self.add_item(self.go_to_previous_page)  # type: ignore
            self.add_item(self.go_to_next_page)  # type: ignore
            if use_last_and_first:
                self.add_item(self.go_to_last_page)  # type: ignore
            self.add_item(self.stop_pages)  # type: ignore

    async def _get_kwargs_from_page(self, page: int) -> Dict[str, Any]:
        value = await discord.utils.maybe_coroutine(self.source.format_page, self, page)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {'content': value, 'embed': None}
        elif isinstance(value, discord.Embed):
            return {'embed': value, 'content': None}
        else:
            return {}

    async def show_page(self, interaction: discord.Interaction, page_number: int) -> None:
        page = await self.source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(page_number)
        if kwargs:
            if interaction.response.is_done():
                if self.message:
                    await self.message.edit(**kwargs, view=self)
            else:
                await interaction.response.edit_message(**kwargs, view=self)

    def _update_labels(self, page_number: int) -> None:
        if page_number == 0:
            self.go_to_first_page.disabled = True
            self.go_to_previous_page.disabled = True
        else:
            self.go_to_first_page.disabled = False
            self.go_to_previous_page.disabled = False

        if self.compact:
            max_pages = self.source.get_max_pages()
            self.go_to_last_page.disabled = max_pages is None or (page_number + 1) >= max_pages
            self.go_to_next_page.disabled = max_pages is not None and (page_number + 1) >= max_pages
            self.go_to_previous_page.disabled = page_number == 0
            return

        max_pages = self.source.get_max_pages()
        if max_pages is not None:
            self.go_to_last_page.disabled = (page_number + 1) >= max_pages
            self.go_to_next_page.disabled = (page_number + 1) >= max_pages
 
    async def show_checked_page(self, interaction: discord.Interaction, page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages is None:
                await self.show_page(interaction, page_number)
            elif max_pages > page_number >= 0:
                await self.show_page(interaction, page_number)
        except IndexError:
            pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
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

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    async def start(self) -> None:
        if self.check_embeds and not self.ctx.channel.permissions_for(self.ctx.me).embed_links:
            await self.ctx.send('Bot does not have embed links permission in this channel.')
            return

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(0)
        self.message = await self.ctx.send(**kwargs, view=self)

    @discord.ui.button(label='≪', style=discord.ButtonStyle.grey, custom_id='1')
    async def go_to_first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.show_page(interaction, 0)

    @discord.ui.button(label='Back', style=discord.ButtonStyle.blurple, custom_id='2')
    async def go_to_previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.show_checked_page(interaction, self.current_page - 1)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.blurple, custom_id='3')
    async def go_to_next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.show_checked_page(interaction, self.current_page + 1)

    @discord.ui.button(label='≫', style=discord.ButtonStyle.grey, custom_id='4')
    async def go_to_last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.show_page(interaction, self.source.get_max_pages() - 1)

    @discord.ui.button(label='Quit', style=discord.ButtonStyle.red, custom_id='5')
    async def stop_pages(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()

class SimplePageSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{index + 1}. {entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            menu.embed.set_footer(text=footer)

        menu.embed.description = '\n'.join(pages)
        return menu.embed

class NewSimpage(BaseNewButton):

    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 12):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.blurple())

class TodoPageSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} lists)'
            menu.embed.set_footer(text=footer)

        menu.embed.description = '\n'.join(pages)
        return menu.embed

class Confirm(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This menus cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        # await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        # await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()