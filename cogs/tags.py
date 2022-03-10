# Standard
import discord
import asyncio
from discord.ext import commands 
from difflib import get_close_matches
from typing import Optional

# Third

# Local
from utils.paginator import SimplePages
from utils.checks import is_latte_guild
from utils.custom_button import content_button
from utils.converter import is_url_image
from utils.errors import UserInputErrors

class Cancel_button(discord.ui.View):
    def __init__(self, ctx, content=None):
        super().__init__()
        self.value = True
        self.ctx = ctx
        self.content = content
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        self.clear_items()
        self.fill_items()
    
    def fill_items(self) -> None:
        if self.content is not None:
            self.add_item(self.content_button)
        self.add_item(self.cancel_button_)

    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This menus cannot be controlled by you, sorry!', ephemeral=True)
        return False

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    @discord.ui.button(label="Content before edit", style=discord.ButtonStyle.green)
    async def content_button(self, button, interaction):
        data = self.content
        if data:
            await interaction.response.send_message(data, ephemeral=True)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel_button_(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await self.message.delete()

    async def on_timeout(self):
        self.value = False
        if self.message:
            try:
                await self.message.edit(view=None)
            except:
                pass

    async def delete_message(self):  
        self.value = False
        try:
            await self.message.delete()
        except:
            return

class TagName(commands.clean_content):
    def __init__(self, *, lower=False):
        self.lower = lower
        super().__init__()

    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if not lower:
            raise commands.BadArgument('Missing tag name.')

        if len(lower) > 100:
            raise commands.BadArgument('Tag name is a maximum of 100 characters.')

        first_word, _, _ = lower.partition(' ')

        # # get tag command. #group commands
        # root = ctx.bot.get_command('tag')
        # if first_word in root.all_commands:
        #     raise commands.BadArgument('This tag name starts with a reserved word.')

        return converted if not self.lower else lower

class Tags(commands.Cog, command_attrs = dict(slash_command=True, slash_command_guilds=[840379510704046151])):
    """Commands to fetch something by a tag name"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='createthread', id=903346472509141023, animated=False)

    async def find_data(self, tag, guild_id):
        find_data = await self.bot.latte_tags.find_by_custom({"guild_id": guild_id, "tag": str(tag)})
        if find_data is None:
            raise RuntimeError('Tag not found')
        else:
            return find_data

    async def remove_data(self, tag, guild_id, tag_name):
        data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": guild_id, "tag": str(tag)})
        if data_deleted and data_deleted.acknowledged:
            embed = discord.Embed(color=0xFF7878)
            embed.description=f"You have successfully deleted **{tag_name}**."
            embed.timestamp = discord.utils.utcnow()
            return embed
        else:
            raise RuntimeError('I could not find tag')

    async def get_tag(self, guild_id, tag):  
        def disambiguate(rows):
            # if rows is None or len(rows) == 0:
            #     raise RuntimeError('Tag not found.')
            names = (r['tag'] for r in rows)
            matches = get_close_matches(tag, names)
            if matches:
                matches = "\n".join(matches)
                raise RuntimeError(f"Tag not found. Did you mean...\n`{matches}`")
            raise RuntimeError('Tag not found.')

        query = {"guild_id": guild_id, "tag": str(tag)}
        row = await self.bot.latte_tags.find_by_custom(query)
        if row is None:
            query = {"guild_id": guild_id}
            rows = await self.bot.latte_tags.find_many_by_custom(query)
            return disambiguate(rows)
        else:
            return row
            
    @commands.command(help="Tag command")
    @commands.guild_only()
    @is_latte_guild()
    async def tag(self, ctx, *, name:TagName = commands.Option(description="Input name")):
        try:
            tag = await self.get_tag(ctx.guild.id, name)
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')
        
        content = tag['content']
        if ctx.clean_prefix != "/" or content.lower().endswith(('png','jpeg','jpg','gif','webp','mp4')):
            return await ctx.send(tag['content'])
        await ctx.send(f"**`{tag['tag']}`**\n{content}")
            
    @commands.command(aliases=['tagcreate','tagc','tagadd'], help="Creates a new tag owned by you.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_create(self, ctx, *, name: TagName(lower=True) = commands.Option(description="Input name")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        embed = discord.Embed(color=0xfdfd96)

        #data_user_count
        data_user = await self.bot.latte_tags.find_by_custom({"user_id": ctx.author.id})
        if len(data_user) >= 50 and ctx.author != self.bot.renly:
            raise UserInputErrors("You can't have more than 50 tags at the moment.")

        #find_data
        data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": name})
        if bool(data_check) == True:
            raise UserInputErrors('This tag already exists, please use another tag.')
        
        #data_count
        data_tags = await self.bot.latte_tags.find_many_by_custom({})
        data_count = reversed(data_tags)
        
        #create_id
        try:
            some_id = []
            i = 0
            for x in data_count:
                i += 1 
                next_id = x['tag_id']
                some_id.append(next_id)
                if i == 10:
                    break
            next_num = max(some_id) + 1
        except:
            next_num = 1

        #response
        view = Cancel_button(ctx)
        embed.description = "Please enter the content within your tag (within 5 minutes)"
        view.message = await ctx.reply(embed=embed, view=view, mention_author=False)
        
        try:
            message_response = await self.bot.wait_for('message', timeout=300, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            embed_error.description = 'Create tag was canceled due to timeout.'
            return await view.message.edit(embed=embed_error, view=None)
        
        content = message_response.content
        #when_content_more_2000
        if len(content) > 2000:
            raise UserInputErrors('Tag content is a maximum of 2000 characters.')
        
        if not view.value:
            return
        elif view.value:

            tag_filter = {"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag_id": next_num}
            tag_data = {"tag": name, "content": content}

            #upsert_data
            await self.bot.latte_tags.upsert_custom(tag_filter, tag_data)

            #reponse
            embed_edit = discord.Embed(description=f"Tag **{name}** successfully created.", timestamp=discord.utils.utcnow(), color=0x77dd77)
            # await message_response.delete()
            # await view.message.edit(embed=embed_edit, view=None)
            await view.delete_message()
            await ctx.channel.send(embed=embed_edit)

    @commands.command(aliases=['tagremove','tagr','tagdelete'], help="remove your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_remove(self, ctx, *, name: TagName = commands.Option(description="Input your tag name")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
    
        try:
            data = await self.find_data(name, ctx.guild.id)
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')

        #check_owner_tag
        if data["user_id"] != ctx.author.id:
            raise UserInputErrors("You are not the owner of the tag")

        try:
            deleted = await self.remove_data(name, ctx.guild.id, data['tag'])
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')
        
        await ctx.reply(embed=deleted, mention_author=False)

    @commands.command(aliases=['tagrename','tagre'], help="rename your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_rename(self, ctx, name_old:TagName = commands.Option(description="tag old name"), *, name_new:TagName=commands.Option(description="tag new name")):
        try:
            data = await self.find_data(name_old, ctx.guild.id)
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')

        #check_owner_tag
        if str(data["user_id"]) != str(ctx.author.id):
            raise UserInputErrors("You are not the owner of the tag")

        #find_again
        data = await self.bot.latte_tags.find_by_custom({"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag": name_old})
        
        #update_data
        data["tag"] = name_new                 
        await self.bot.latte_tags.update_by_custom(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag": name_old}, data
        )

        #reponse
        embed = discord.Embed(description=f"You have successfully renamed **{name_old}** to **{data['tag']}**", color=0xFCFFA6)
        embed.timestamp = discord.utils.utcnow()
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"Rename by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"Rename by {ctx.author.display_name}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['tagedit','tage'], help="edit your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_edit(self, ctx, *, tag:TagName =commands.Option(description="Input your tag name")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        embed = discord.Embed(color=0xfdfd96)
        
        try:
            data_check = await self.find_data(tag, ctx.guild.id)
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')

        #check_owner_tag
        if data_check["user_id"] != ctx.author.id:
            raise UserInputErrors('You are not the owner of this tag.')

        old_content = data_check['content'] or None

        #response
        view = Cancel_button(ctx, content=old_content)
        embed.description = "Please enter the new content (within 5 minutes)"
        view.message = await ctx.send(embed=embed, view=view)

        #waiting_message
        try:
            message_response = await self.bot.wait_for('message', timeout=300, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            embed_error.description = 'Edit tag was canceled due to timeout.'
            return await view.message.edit(embed=embed_error, view=None)

        content = message_response.content
        #when_content_more_2000
        if len(content) > 2000:
            raise UserInputErrors('Tag content is a maximum of 2000 characters.')

        if not view.value:
            return
        elif view.value:
            data_check["content"] = content
            await self.bot.latte_tags.update_by_custom(
                {"guild_id": ctx.guild.id, "tag": str(tag)}, data_check)
            embed_edit = discord.Embed(description=f"You have successfully edited **{data_check['tag']}**", timestamp=discord.utils.utcnow())
            embed_edit.color = 0x77dd77
            if ctx.author.avatar is not None:
                embed_edit.set_footer(text=f"Edited by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            else:
                embed_edit.set_footer(text=f"Edited by {ctx.author.display_name}")
            await view.delete_message()
            await ctx.channel.send(embed=embed_edit)

    @commands.command(aliases=['taglist','tagl'], help="Lists all the tags that belong to you or someone else.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_list(self, ctx, member: discord.Member = commands.Option(default=None, description="Spectify member")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        if member is None:
            member = ctx.author

        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id, "user_id": member.id})

        #check_data
        if bool(data) == False:
            raise UserInputErrors(f"**{member.display_name}** doesn't have any tags.")
        data = sorted(data, key=lambda x: x["tag"])
        
        #count_tag
        all_tag = []
        for x in data:
            tags = f'{x["tag"]} (ID : {x["tag_id"]})'
            all_tag.append(tags)
        
        #view_button
        if all_tag:
            p = SimplePages(entries=all_tag, per_page=10, ctx=ctx)
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            raise UserInputErrors(f"**{member.display_name}** doesn't have any tags.")
    
    @commands.command(aliases=['tagall'], help="Lists all server-specific tags for this server.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_all(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})

        #check_data
        if bool(data) == False:
            raise UserInputErrors('Not found tag from this server.')
        data = sorted(data, key=lambda x: x["tag"])
        
        #count_tag
        all_tag = []
        for x in data:
            tags = f'{x["tag"]} (ID : {x["tag_id"]})'
            all_tag.append(tags)
        
        #view_button
        if all_tag:
            p = SimplePages(entries=all_tag, ctx=ctx)
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            raise UserInputErrors(f"This server doesn't have any tags.")

    @commands.command(aliases=['tagsearch','tags'], help="Searches for a tag.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_search(self, ctx, *, name:TagName(lower=True) = commands.Option(description="Input tag name")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        #find_name_tag
        not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
        
        total:int = len(not_found)
        names = (r['tag'] for r in not_found)
        matches = get_close_matches(name , names , n=total)

        #coverter_to_string
        tag_found = []
        for x in matches:
            data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id, "tag": x})
            find_id = '\n'.join(f'{i["tag_id"]}' for i in data)
            tag_name_id = f'{x} (ID : {find_id})'
            tag_found.append(tag_name_id)

        if tag_found:
            #view_button
            p = SimplePages(entries=tag_found, per_page=10, ctx=ctx)
#            p.embed.title = "Tags search"
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            raise UserInputErrors(f"**{name}** This tag not found")

    @commands.command(aliases=['taginfo','tagi'], help="Shows information about the specified tag.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_info(self, ctx, *, tag:TagName =commands.Option(description="Input your tag name or id")):        
        try:
            data = await self.find_data(tag, ctx.guild.id)
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')

        #found_or_not_found
        if data is not None:
            view = content_button(ctx=ctx , content=data['content'])
            owner_tag = ctx.guild.get_member(int(data['user_id']))
            embed = discord.Embed(color=self.bot.white_color)
            embed.title = f"Tag Info"
            embed.description = f"**Tag name:** {data['tag']}\n**Author:** {owner_tag.mention}"
            embed.set_footer(text=f"ID : {data['tag_id']}")
            return await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
            names = (r['tag'] for r in not_found)
            matches = get_close_matches(tag , names)
            description = f"Tag not found."
            if matches:
                matches = "\n".join(matches)
                description = f"Tag not found. Did you mean...\n`{matches}`"
            raise UserInputErrors(description)

    # @commands.command(aliases=['tag_count'], help="Total tag in your server")
    # @commands.guild_only()
    # @is_latte_guild()
    # async def tagcount(self, ctx):            
    #     data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
    #     if bool(data) == False:
    #         raise UserInputErrors("This server doesn't have any tags.")

    #     embed = discord.Embed(description=f"Total tags : `{len(data)}`",color=0x77dd77)
    #     await ctx.reply(embed=embed, mention_author=False)
  
def setup(bot):
    bot.add_cog(Tags(bot))