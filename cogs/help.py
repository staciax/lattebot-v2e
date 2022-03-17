# Standard
import discord
import contextlib
from discord.ext import commands
from utils.formats import count_python
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta, timezone

# Local
from utils.json_loader import latte_read
from bot import LatteBot
from utils.useful import RenlyEmbed
from utils.errors import UserInputErrors

class HelpView(discord.ui.View):
    def __init__(self, ctx: commands.context, data: Dict[commands.Cog, List[commands.Command]]=None, help_command: commands.HelpCommand=None):
        super().__init__()
        self.ctx = ctx
        self.data = data
        self.help_command = help_command
        self.total_cmd = help_command.total_commands if help_command is not None else None
        self.bot: LatteBot = ctx.bot
        self.main_embed = self.build_main_page()
        self.current_page = 0
        self.message: discord.Message = None
        self.embeds: List[discord.Embed] = [self.main_embed]
        self.check_view = True
        self.is_command = ctx.command is not None
        self.clear_items()
        self.fill_items()
    
    def fill_items(self) -> None:
        self.add_item(self.category_select)
            
    @discord.ui.select(placeholder="Select a category", row=0)
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == "index":
            self.current_page = 0
            self.embeds = [self.main_embed]
            self._update_buttons()
            self.clear_items()
            self.add_item(self.category_select)
            self.check_view = True
            return await interaction.response.edit_message(embed=self.main_embed, view=self)
        cog = self.bot.get_cog(select.values[0])
        if not cog:
            embed = discord.Embed(color=0xffffff)
            embed.description = 'Somehow, that category was not found?'
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            self.embeds = self.build_embeds(cog)
            self.current_page = 0
            self._update_buttons()
            self.update_button_cog()
            return await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    def build_embeds(self, cog: commands.Cog) -> List[discord.Embed]:
        embeds = []
        commands = cog.get_commands()
        commands = sorted(commands, key=lambda c: c.name)
        embed = discord.Embed(title=f"{cog.display_emoji} {cog.qualified_name} commands [{len(commands)}]", color=0xffffff,
                              description=cog.description or "No description provided")
        for command in commands:
            cmd_sig = f' {command.signature}'
            signature = f'{command.qualified_name}'
            if self.ctx.clean_prefix != '/':
                signature += cmd_sig
            embed.add_field(name='> %s' % signature, value=command.short_doc or 'No help given...', inline=False)
            embed.set_footer(text="<> = required argument | [] = optional argument")
            if len(embed.fields) == 5:
                embeds.append(embed)
                embed = discord.Embed(title=f"{cog.qualified_name} commands [{len(commands)}]", color=0xffffff,
                                      description=cog.description or "No description provided")
        if len(embed.fields) > 0:
            embeds.append(embed)
        return embeds

    def build_select(self) -> None:
        self.category_select: discord.ui.Select
        self.category_select.options = []
        self.category_select.add_option(label='Main Page', value='index', emoji=self.help_command.display_emoji)
        botCogs = self.ctx.bot.cogs
        for cog in sorted(botCogs):
            if cog not in self.help_command.ignored_cog:
                cog = self.ctx.bot.get_cog(cog)
                emoji = cog.display_emoji or None
                description = cog.description or None
                self.category_select.add_option(label=cog.qualified_name, value=cog.qualified_name, emoji=emoji, description=description)
            
    def build_main_page(self) -> discord.Embed:
        ctx = self.ctx
        embed = discord.Embed(color=0xffffff)
        embed.set_author(name=f'{self.bot.user.display_name} - Help', icon_url=self.bot.user.avatar.url)
        embed.description = "Use **Selection** for more informations about a category."
        embed.description += f"\nTotal commands: `{self.total_cmd}`"
        
        def get_cog(name):
            cog = ctx.bot.get_cog(name)
            if cog:
                cog = f'•{cog.display_emoji} **{cog.qualified_name}**\n'
            return cog or '\u200B'
        
        #Log_list   
        anime = get_cog('Anime')
        fun = get_cog('Fun')
        infomation = get_cog('Infomation')
        latte = get_cog('Latte')
        leveling = get_cog('Leveling')
        misc = get_cog('Misc')
        mod = get_cog('Mod')
        tags = get_cog('Tags')
        todo = get_cog('Todo')
        utility = get_cog('Utility')
        valorant = get_cog('Valorant')

        if ctx.guild.id == ctx.bot.latte_guild_id:
            embed.add_field(name=f'\u200B', value=f'{anime}{latte}{mod}{utility}', inline=True)
            embed.add_field(name=f'\u200B', value=f'{fun}{leveling}{misc}{valorant}', inline=True)
            embed.add_field(name=f'\u200B', value=f'{infomation}{tags}{todo}' , inline=True)
        else:
            embed.add_field(name=f'\u200B', value=f'{anime}{misc}{valorant}', inline=True)
            embed.add_field(name=f'\u200B', value=f'{fun}{mod}', inline=True)
            embed.add_field(name=f'\u200B', value=f'{infomation}{utility}', inline=True)
        embed.set_image(url=(latte_read('latte_events'))['help_thumbnail'])
        year, mouth, day = ctx.bot.last_update
        lastup = datetime(year, mouth, day)
        dt = lastup.strftime("%d %B %Y")
        embed.set_footer(text=f"v{ctx.bot.bot_version} Recently updated • {dt}", icon_url=ctx.bot.user.avatar.url)
        return embed
    
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
    
    @discord.ui.button(label='Home', style=discord.ButtonStyle.green)
    async def home_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = 0
        self.embeds = [self.main_embed]
        self._update_buttons()
        self.clear_items()
        self.add_item(self.category_select)
        self.check_view = True
        return await interaction.response.edit_message(embed=self.main_embed, view=self)

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
    
    def update_button_cog(self):
        if self.check_view:
            self.add_item(self.go_to_first_page)
            self.add_item(self.previous)
            self.add_item(self.next)
            self.add_item(self.go_to_last_page)
            self.add_item(self.home_button)
            self.check_view = False

    async def on_timeout(self) -> None:
        self.clear_items()
        self.add_item(self.category_select)
        self.category_select.placeholder = "Timeout."
        self.category_select.disabled = True
        try:
            await self.message.edit(view=self)
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def start(self):
        self.build_select()
        self._update_buttons()
        self.message = await self.ctx.reply(embed=self.main_embed, view=self, mention_author=False)
    
    async def cog_view(self, cog:commands.Cog):
        self.remove_item(self.category_select)
        self.embeds = self.build_embeds(cog)
        self._update_buttons()
        self.update_button_cog()
        self.remove_item(self.home_button)
        self.message = await self.ctx.reply(embed=self.embeds[self.current_page], view=self, mention_author=False)

class MyHelp(commands.HelpCommand):
    def __init__(self, **options):
        attrs = {
            'help': 'Help commands',
            'slash_command': True
        }
        super().__init__(command_attrs=attrs, **options)
        self.context: commands.context = None
        self.ignored_cog = []
    
    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='latte_', id='902674566655139881', animated=False)

    def get_command_signature(self, command, ctx):
        return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)

    def get_bot_mapping(self):
        ctx = self.context
        bot = self.context.bot
        if ctx.guild.id == ctx.bot.latte_guild_id:
            ignored_cogs = ['Error', 'Events', 'Help', 'Jishaku', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Testing', 'No_slash','SNIPE']
        else:
            ignored_cogs = ['Error', 'Events', 'Help', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Tags', 'Testing', 'Todo', 'No_slash','SNIPE']
        self.ignored_cog = ignored_cogs
        mapping = {cog: cog.get_commands() for cog in
                   sorted(bot.cogs.values(), key=lambda c: c.qualified_name, reverse=False) if
                   cog.qualified_name not in ignored_cogs}
        return mapping

    def get_minimal_command_signature(self, command, ctx:commands.context=None):
        ctx = ctx or self.context
        if isinstance(command, commands.Group):
            return '[G] %s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)
        return '(c) %s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)
    
    def get_minimal_command_signature_custom(self, command, ctx):
        if isinstance(command, commands.Group):
            return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)
        return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)

    def get_minimal_command_usage(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        self.total_cmd = len(await self.filter_commands(list(self.context.bot.commands), sort=True))
        view = HelpView(self.context, data=mapping, help_command=self)
        await view.start()
    
    @property
    def total_commands(self):
        return self.total_cmd

    async def send_command_help(self, command):
        ctx = self.context
        aliases = command.aliases
        description = command.help

        ignored_cogs = ['Error', 'Events', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Star', 'Tags', 'Testing', 'Todo', 'No_slash','SNIPE']
        if command.cog_name in ignored_cogs and ctx.author != ctx.bot.renly:
            raise UserInputErrors(f'Command not found')

        command_cd = []
        try:
            cmd_per = command._buckets._cooldown.per
            command_cd.append(f"\n**Cooldown:**\n{cmd_per:,.0f}s")
        except:
            pass

        can_run = []
        try:
            await command.can_run(self.context)
        except Exception as Ex:
            # print(f"Command help error - {Ex}")
            can_run.append('\n**Can be used?:** No')
        
        cmd_cd = ''.join(command_cd)
        cmd_can_run = ''.join(can_run)
        
        embed = discord.Embed(color=self.context.bot.white_color)
        embed.title = f"{command.name} - Help command"
        embed.description = f"{description}" + f"{cmd_cd}"
        embed.add_field(name="Category:", value=f"```{command.cog_name}```", inline=False)
        if aliases:
            aliases = ', '.join(aliases)
            embed.add_field(name="Aliases:", value=f"```{aliases}```", inline=False)
        embed.add_field(name="Usage:", value=f"```{self.get_minimal_command_usage(command)}```" + f"{cmd_can_run}", inline=False)
        embed.set_footer(text="<> = required argument | [] = optional argument")
        await ctx.reply(embed=embed, mention_author=False)
        
    async def send_cog_help(self, cog):
        ctx = self.context
        ignored_cogs = ['Error', 'Events', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Star', 'Tags', 'Testing', 'Todo', 'No_slash', 'SNIPE']
        if cog.qualified_name in ignored_cogs and ctx.author != ctx.bot.renly:
            raise UserInputErrors(f'Command not found')
        
        view = HelpView(self.context)
        await view.cog_view(cog=cog)
        
        # entries = cog.get_commands()
        # ctx = self.context
        
        # ignored_cogs = ['Error', 'Events', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Star', 'Tags', 'Testing', 'Todo', 'No_slash']
        # if cog.qualified_name in ignored_cogs and ctx.author != ctx.bot.renly:
        #     raise UserInputErrors(f'Command not found')
        #     # raise UserInputErrors(f'No commands found in "{cog.qualified_name}"')

        # if entries:
        #     command_signatures = [self.get_minimal_command_signature(entry) for entry in entries]
        #     val = "\n".join(command_signatures)
        #     embed = discord.Embed(color=self.context.bot.white_color)
        #     embed.title = f"{cog.qualified_name} - Help category"
        #     embed.description = f"**Description:**\n{cog.description}\n"
        #     embed.description += f"**Commands:**\n```yalm\n{val}\n```\n`(C)` : command\n`[G]` : group command"
        #     # embed.add_field(name="Description:", value=f'{cog.description}', inline=False)
        #     # embed.add_field(name="Commands:", value=f'```yalm\n{val}\n```\n`(C)` : command\n`[G]` : group command', inline=False)
        #     embed.set_footer(text="<> = required argument | [] = optional argument")
        #     await self.context.reply(embed=embed, mention_author=False)
        # else:
        #     raise UserInputErrors(f'Command not found')
        #     # raise UserInputErrors(f'No commands found in {cog.qualified_name}')

    async def send_group_help(self, group):
        ctx = self.context
        # prefix = self.context.clean_prefix
        entries = group.commands

        ignored_cogs = ['Error', 'Events', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Star', 'Tags', 'Testing', 'Todo', 'No_slash', 'SNIPE']
        if group.cog_name in ignored_cogs and ctx.author != ctx.bot.renly:
            raise UserInputErrors(f'Command not found')

        command_signatures = [self.get_minimal_command_signature(c) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            embed=discord.Embed(title=f"{group.qualified_name} - Help group", color=self.context.bot.white_color)  
            command_cd = []
            try:
                cmd_per = group._buckets._cooldown.per
                command_cd.append(f"\n**Cooldown:**\n{cmd_per:,.0f}s")
            except:
                pass
            
            can_run = []
            try:
                await group.can_run(self.context)
            except Exception as Ex:
                print(f"Group help error - {Ex}")
                can_run.append('\n**Can be used?:** No')

            command_checks = ''.join(command_cd)
            can_run_checks = ''.join(can_run)
            embed.add_field(name="Description:", value=f"{group.help or 'No Description.' + f'{command_checks}'}", inline=False)
            embed.add_field(name="Category:", value=f"```{group.cog_name}```", inline=False)
            if group.aliases:
                embed.add_field(name="Aliases:", value=f'`{"`, `".join(group.aliases)}`', inline=False)
            embed.add_field(name="Sub-commands:", value=f"{group.short_doc}\n```yalm\n{val}\n```{can_run_checks}", inline=False)
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.reply(embed = embed, mention_author=False)
            
    async def send_group_help_custom(self, group, ctx):
        entries = group.commands
        command_signatures = [self.get_minimal_command_signature(c, ctx) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            embed=discord.Embed(title=f"{group.qualified_name} - Help group", color=ctx.bot.white_color)  
            embed.add_field(name="Description:", value=f"{group.help or 'No Description.'}", inline=False)
            embed.add_field(name="Category:", value=f"```{group.cog_name}```", inline=False)
            embed.add_field(name="Sub-commands:", value=f"{group.short_doc}\n```yalm\n{val}\n```", inline=False)
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.reply(embed = embed, mention_author=False)
    
    async def send_group_help_user(self, cog_name, ctx):
        cog = ctx.bot.get_cog(cog_name)
        entries = cog.get_commands()
        command_signatures = [self.get_minimal_command_signature_custom(c, ctx) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures[1:])
            embed=discord.Embed(title=f"{str(ctx.command.name).capitalize()} - Help group", color=ctx.bot.white_color)
            embed.add_field(name="Description:", value=f"{ctx.command.help or 'No Description.'}", inline=False)
            embed.add_field(name=f"Category:", value=f"{ctx.command.cog_name}", inline=False)
            embed.add_field(name="Sub-commands:", value=f"{ctx.command.short_doc}\n```yalm\n{val}\n```", inline=False)
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.reply(embed=embed, mention_author=False)

    def command_not_found(self, string):
        return string

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return command.qualified_name + string
        return command.qualified_name

    async def send_error_message(self, error):
        # print(f"Help error - {error}")
        raise UserInputErrors("Command not found")
        
    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(description=f"{str(error.original)}")
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed, mention_author=False)
    
    async def command_callback(self, ctx, *, command=commands.Option(default=None, description="Command name")):
        """|coro|

        The actual implementation of the help command.

        It is not recommended to override this method and instead change
        the behaviour through the methods that actually get dispatched.

        - :meth:`send_bot_help`
        - :meth:`send_cog_help`
        - :meth:`send_group_help`
        - :meth:`send_command_help`
        - :meth:`get_destination`
        - :meth:`command_not_found`
        - :meth:`subcommand_not_found`
        - :meth:`send_error_message`
        - :meth:`on_help_command_error`
        - :meth:`prepare_help_command`
        """
        await self.prepare_help_command(ctx, command)
        bot = ctx.bot

        if command is None:
            mapping = self.get_bot_mapping()
            return await self.send_bot_help(mapping)

        # Check if it's a cog
        cog = bot.get_cog(command.capitalize())
        if cog is not None:
            return await self.send_cog_help(cog)

        maybe_coro = discord.utils.maybe_coroutine

        # If it's not a cog then it's a command.
        # Since we want to have detailed errors when someone
        # passes an invalid subcommand, we need to walk through
        # the command group chain ourselves.
        keys = command.split(" ")
        cmd = bot.all_commands.get(keys[0])
        if cmd is None:
            string = await maybe_coro(self.command_not_found, self.remove_mentions(keys[0]))
            return await self.send_error_message(string)

        for key in keys[1:]:
            try:
                found = cmd.all_commands.get(key)
            except AttributeError:
                string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
                return await self.send_error_message(string)
            else:
                if found is None:
                    string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
                    return await self.send_error_message(string)
                cmd = found

        if isinstance(cmd, commands.Group):
            return await self.send_group_help(cmd)
        else:
            return await self.send_command_help(cmd)

class Help(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
        help_command = MyHelp()
        help_command.cog = self
        bot.help_command = help_command

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='latte_icon_new', id=907030425011109888, animated=False)
     
def setup(bot):
    bot.add_cog(Help(bot))