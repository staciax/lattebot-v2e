# Standard
import discord
import contextlib
from discord.ext import commands
from utils.formats import count_python
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta, timezone

# Local
from utils.json_loader import latte_read

class HelpDropdown(discord.ui.Select):
    def __init__(self, ctx, view):
        self.ctx = ctx
        self.view_ = view # i hope that works
        options = []
        if ctx.guild.id == ctx.bot.latte_guild_id:
            ignoredCogs = ['Error', 'Events', 'Help', 'Jishaku', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Testing']
        else:
            ignoredCogs = ['Error', 'Events', 'Help', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Tags', 'Testing', 'Todo']

        botCogs = ctx.bot.cogs
        for cog in botCogs:
            if cog not in ignoredCogs:
                cog = ctx.bot.get_cog(cog)
                options.append(discord.SelectOption(label=cog.qualified_name, description=cog.description, emoji=cog.display_emoji))
        super().__init__(placeholder='Select a category...', min_values=1, max_values=1, options=options)
                    
    def get_minimal_command_signature(self, command):
        if isinstance(command, commands.Group):
            return '%s%s %s' % (self.ctx.clean_prefix, command.qualified_name, command.signature)
        return '%s%s %s' % (self.ctx.clean_prefix, command.qualified_name, command.signature)
        # return '[G] %s%s %s' % (self.ctx.clean_prefix, command.qualified_name, command.signature)
        # return '(c) %s%s %s' % (self.ctx.clean_prefix, command.qualified_name, command.signature)

    def get_command_name(self, command):
        return "%s" % (command.qualified_name)

    async def callback(self, interaction: discord.Interaction):
        cog = self.ctx.bot.get_cog(self.values[0])
                
        entries = cog.get_commands()
        command_signatures = [self.get_minimal_command_signature(c) for c in entries]

        if command_signatures == [f'{self.ctx.clean_prefix}waifu_im_sfw <"waifu"|"maid"|"all">', f'{self.ctx.clean_prefix}waifu_im_nsfw <"ass"|"ecchi"|"ero"|"hentai"|"maid"|"milf"|"oppai"|"oral"|"paizuri"|"selfies"|"uniform">', f'{self.ctx.clean_prefix}waifu_pisc <"sfw"|"nsfw">']:
            command_signatures = f'{self.ctx.clean_prefix}waifu_im_sfw <tags>', f'{self.ctx.clean_prefix}waifu_im_nsfw <tags>', f'{self.ctx.clean_prefix}waifu_pisc <"sfw"|"nsfw">'
        if command_signatures:
            val = "\n".join(command_signatures)
            
        embed = discord.Embed(title=f"{cog.display_emoji} {cog.qualified_name} commands", color=0xffffff)
        embed.add_field(name=f"Category: {cog.qualified_name}", value=f"{cog.description}\n\n`{val}`")
        #timestamp=discord.utils.utcnow()
        embed.set_footer(text="<> = required argument | [] = optional argument")
        
        await interaction.message.edit(embed=embed, view = self.view_) 

class Stuff(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.add_item(HelpDropdown(ctx, self))

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        role = discord.utils.get(self.ctx.guild.roles, id=842304286737956876)
        if interaction.user in (self.ctx.author, self.ctx.bot.renly) or role in interaction.user.roles:
            return True
        await interaction.response.send_message('This menus cannot be controlled by you, sorry!', ephemeral=True)
        return False
    
    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                item.placeholder = "Select menu disabled due to timeout."
            item.disabled = True
        
        await self.message.edit(view=self)
        
class LatteBotHelp(commands.HelpCommand):
    """Help commands"""

    def __init__(self):
        attrs = {
            'help': 'Help commands',
            'slash_command': True
        }
        super().__init__(command_attrs=attrs)

    def get_command_signature(self, command, ctx):
        return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)

    def get_minimal_command_signature(self, command):
        if isinstance(command, commands.Group):
            return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)
    
    def get_minimal_command_signature_custom(self, command, ctx):
        if isinstance(command, commands.Group):
            return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)
        return '%s%s %s' % (ctx.clean_prefix, command.qualified_name, command.signature)

    def get_minimal_command_usage(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)
    
    def get_command_name(self, command):
        return '%s' % (command.qualified_name)

    async def send_bot_help(self, mapping):
        ctx = self.context

        guild_prefix = await ctx.bot.command_prefix(ctx.bot, ctx.message)
                    
        embed = discord.Embed(color=ctx.bot.white_color)
        #title=f"{ctx.bot.user.display_name} Help", 
        embed.set_author(name=f'{ctx.bot.user.display_name} Help', icon_url=ctx.bot.user.avatar.url)
        embed.description = f"Total commands: `{len(await self.filter_commands(list(self.context.bot.commands), sort=True))}`\n"
        embed.description += f"Bot prefix: `/`, `{guild_prefix[2]}`\n"
        embed.description += "Use **Selection** for more informations about a category."
        
        # embed.description = f"""
        # Total commands: `{len(await self.filter_commands(list(self.context.bot.commands), sort=True))}`
        # Bot prefix: `/` , `{ctx.clean_prefix}`
        # Use **Selection** for more informations about a category."""

        year, mouth, day = ctx.bot.last_update
        lastup = datetime(year, mouth, day)
        dt = lastup.strftime("%d %B %Y")
        embed.set_footer(text=f"v{ctx.bot.bot_version} Recently updated • {dt}", icon_url=ctx.bot.user.avatar.url)

        # embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
        # embed.timestamp = discord.utils.utcnow()

        #        Written with only `{count_python('.'):,}` lines
        #{len(await self.filter_commands(list(self.context.bot.commands), sort=True))} = commands can use 
        #{len(list(self.context.bot.commands))} = all commands
        # ```diff
        # + Type {self.context.clean_prefix}help [command/category] for help on a command/category
        # - <> = required argument
        # - [] = optional argument
        # ```

        allcogs = []
        cogindex = []

        cogs = []
        cogs_description = []

        if ctx.guild.id == ctx.bot.latte_guild_id:
            ignored_cogs = ['Error', 'Events', 'Help', 'Jishaku', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Testing']
        else:
            ignored_cogs = ['Error', 'Events', 'Help', 'Jishaku', 'Latte', 'Leveling', 'NSFW', 'Owner', 'Reaction', 'Reference', 'Star', 'Tags', 'Testing', 'Todo']
        
        iter = 1
        #if cog is None or cog.qualified_name in ignored_cogs: continue
        
        for cog, commands in mapping.items():
            # print(cog.qualified_name)
            if cog is None or cog.qualified_name in ignored_cogs: continue
            # print(cog.qualified_name)
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_name(c) for c in filtered]
            if command_signatures:
                cogs.append(f'{cog.display_emoji} {cog.qualified_name}')
                cogs_description.append(cog.description)
                # cogindex.append(cog.qualified_name)
                # allcogs.append(f"**{cog.qualified_name}**{len(commands)} \n`{cog.description}`")
                #allcogs.append(f"{cog.description} `help {cog.qualified_name}`")
                iter+=1
        nl = '\n'

        # print(len(cogs))
        # print(cogs)
        if ctx.guild.id == ctx.bot.latte_guild_id:
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**\n•**%s**\n•**%s**' % (cogs[0],cogs[3],cogs[6],cogs[9]) , inline=True)
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**\n•**%s**' % (cogs[1],cogs[4],cogs[7]) , inline=True)
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**\n•**%s**' % (cogs[2],cogs[5],cogs[8]) , inline=True)
        else:
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**' % (cogs[0],cogs[3]) , inline=True)
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**' % (cogs[1],cogs[4]), inline=True)
            embed.add_field(name=f'** **', value='•**%s**\n•**%s**' % (cogs[2],cogs[5]), inline=True)

        embed.set_image(url=(latte_read('latte_events'))['help_thumbnail'])
    
        # for x,y in zip(cogs, cogs_description):
        #     embed.add_field(name=x, value=y , inline=False)

        # embed.add_field(name=f"**Select a Category:** **[{len(allcogs)}]**", value=f"{nl.join(allcogs)}")
#        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        view = Stuff(ctx)

        view.message = await ctx.send(embed=embed, view=view) #without this line 233 would not work

    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")
        # source = PaginatedCogHelp(entries=[self.get_minimal_command_signature(c) for c in cog.get_commands()],
        #                           per_page=15, cog=cog, ctx=self.context,
        #                           usable=len(await self.filter_commands(cog.get_commands(), sort=True)))
        # menu = menus.views.ViewMenuPages(source=source, timeout=120, clear_reactions_after=True, check_embeds=True)
        # await menu.start(self.context)

    async def send_command_help(self, command):
        ctx = self.context
        
        # <---- Command Information ---->
        
        aliases = command.aliases
        description = command.help
        
        commandInformation = []
        
        #commandInformation.append(f"Usage: {self.get_minimal_command_usage(command)}")
        commandInformation.append(f"Category: {command.cog_name}")
            
        if aliases:
            aliases = ', '.join(aliases)
            commandInformation.append(f"Aliases: {aliases}")
            
        #if description:
            #commandInformation.append(f"\nDescription: {command.help}")
            
        commandInformation = '\n'.join(commandInformation)
        
        # <---- Command Information ---->
        
        # <---- Command Checks ---->
            
        commandChecks = []
        
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                commandChecks.append("Usable by you: Yes")
            else:
                commandChecks.append("Usable by you: No")

        try:
            slowmode = command._buckets._cooldown.per
            commandChecks.append(f"Slowmode: {slowmode}s")
                
        except:
            pass
        
        commandChecks = '\n'.join(commandChecks)
                
        embed = discord.Embed(title=f"{self.get_minimal_command_usage(command)}", description=f"""
        {command.help}
        """)

        embed.add_field(name="Command Information", value=f"""
        ```yaml
        {commandInformation}
        ```
                """, inline=False)

        embed.add_field(name="Command Checks", value=f"""
        ```yaml
        {commandChecks}
        ```
        """, inline=False)

        if command.brief:
            embed.set_image(url=command.brief)
            
        embed.set_footer(text="<> = required argument | [] = optional argument")

        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        prefix = self.context.clean_prefix
        entries = group.commands
        command_signatures = [self.get_minimal_command_signature(c) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            embed=discord.Embed(title=f"Help - {group.qualified_name}", color=0xffffff)
            # embed.description=f"""
            # Total commands: {len(group.commands)}
            # Commands usable by you (in this server): {len(await self.filter_commands(group.commands, sort=True))}"""
            embed.add_field(name=f" Category: {group.qualified_name}", value=f"{group.short_doc}\n```yalm\n{val}\n```")
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.send(embed = embed)
    
    async def send_group_help_custom(self, group, ctx):
        entries = group.commands
        command_signatures = [self.get_minimal_command_signature_custom(c, ctx) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            embed=discord.Embed(title=f"Help - {group.qualified_name}", color=0xffffff)
            embed.add_field(name=f" Category: {group.qualified_name}", value=f"{group.short_doc}\n```yalm\n{val}\n```")
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.send(embed = embed)
    
    async def send_group_help_user(self, signatures, ctx, command_name, description):
        command_signatures = signatures
        if command_signatures:
            val = "\n".join(command_signatures)
            embed=discord.Embed(title=f"Help - {str(command_name).capitalize()}", color=0xffffff)
            embed.add_field(name=f" Category: {str(command_name).capitalize()}", value=f"{description}\n```yalm\n{val}\n```")
            embed.set_footer(text="<> = required argument | [] = optional argument")
            await ctx.send(embed = embed)

    async def send_error_message(self, error):
        pass
        #raise errors.CommandDoesntExist

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(description=f"{str(error.original)}")
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

class Help(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
        help_command = LatteBotHelp()
        help_command.cog = self
        bot.help_command = help_command

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{PERSONAL COMPUTER}')
        
def setup(bot):
    bot.add_cog(Help(bot))